# Two functions derived from the earlier recommend_paint_action logic:
# 1) get_root_cause(detected_type, issue_critical, temperature_c, humidity_pct, spray_pressure_bar)
#    - returns root_cause (string)
# 2) recommend_actions_from_root(detected_type, issue_critical, temperature_c, humidity_pct, spray_pressure_bar, root_cause)
#    - returns {"spray_parameters_to_set": {...}, "trigger": ...}
#
# Both functions respect actuator limits & step sizes. Example usages at the end.

def clamp_step(value, min_v, max_v, step):
    v = max(min_v, min(max_v, value))
    steps = round((v - min_v) / step)
    return min_v + steps * step

LIMITS = {
    "spray_pressure": {"unit": "bar", "min": 1.5, "max": 4.0, "step": 0.1, "default": 2.5},
    "paint_flow_rate": {"unit": "mL/min", "min": 10, "max": 200, "step": 1, "default": 60},
    "atomizing_air_flow": {"unit": "L/min", "min": 20, "max": 200, "step": 1, "default": 80},
    "gun_traverse_speed": {"unit": "m/s", "min": 0.05, "max": 1.5, "step": 0.01, "default": 0.5},
}

def get_root_cause(detected_type: str, issue_critical: bool,
                   temperature_c: float, humidity_pct: float, spray_pressure_bar: float) -> str:
    """
    Determine a compact root_cause string from inputs.
    """
    t = detected_type.lower().strip()
    # Basic heuristics (kept concise and deterministic)
    if t == "orange_peel":
        if temperature_c < 18 and spray_pressure_bar <= 2.3:
            return "Low ambient temperature with insufficient atomization → coarse droplets and poor leveling (orange-peel)."
        if 18 <= temperature_c <= 27 and 2.2 <= spray_pressure_bar <= 3.0:
            return "Higher paint viscosity or slightly reduced atomization → mild orange-peel."
        if temperature_c >= 28 and humidity_pct < 35 and spray_pressure_bar >= 3.1:
            return "High temperature + low humidity causing fast solvent evaporation and poor leveling; excessive spray pressure exacerbates orange-peel."
        return "General leveling/atomization imbalance causing orange-peel; tune atomization and gun speed."
    
    if t == "fisheye":
        if humidity_pct >= 60:
            return "Surface contamination (silicone/oil) combined with high humidity → fisheye formation."
        if temperature_c >= 30 and humidity_pct < 35:
            return "Possible substrate degassing or process contamination under high temperature → fisheye risk."
        if spray_pressure_bar < 2.2:
            return "Low spray pressure causing poor wetting in presence of minor contamination → localized fisheyes."
        return "Isolated contaminant in paint feed or substrate incompatibility causing localized fisheyes."
    
    if t == "overspray":
        if spray_pressure_bar >= 3.2:
            return "High spray pressure and/or nozzle wear producing wider plume and edge deposition (overspray)."
        if temperature_c < 20 and humidity_pct > 45 and spray_pressure_bar <= 2.5:
            return "Gun-to-part distance too close and high local deposit; high flow or close distance causing localized overspray."
        return "Excessive paint flow or slight misalignment causing overspray; adjust flow and speed."
    
    return f"Detected type '{detected_type}' not in mapping; recommend inspection."


def recommend_actions_from_root(detected_type: str, issue_critical: bool,
                                temperature_c: float, humidity_pct: float, spray_pressure_bar: float,
                                root_cause: str) -> dict:
    """
    Using root_cause (string) and sensor inputs, return spray setpoints and trigger (if critical).
    Returns:
      {
        "spray_parameters_to_set": { ... },
        "trigger": "human operators" | "triggers maintenance" | None
      }
    """
    t = detected_type.lower().strip()
    # Start from defaults
    sp = LIMITS["spray_pressure"]["default"]
    pf = LIMITS["paint_flow_rate"]["default"]
    af = LIMITS["atomizing_air_flow"]["default"]
    gs = LIMITS["gun_traverse_speed"]["default"]
    
    # Use root_cause keywords to choose actions; fall back to sensor heuristics when ambiguous
    rc = root_cause.lower()
    if "low ambient temperature" in rc or "low temp" in rc:
        sp = max(sp, 2.6)
        pf = 65
        af = 95
        gs = 0.60
    elif "higher paint viscosity" in rc or "viscosity" in rc:
        sp = 3.0
        pf = 70
        af = 110
        gs = 0.50
    elif "high temperature + low humidity" in rc or ("high temperature" in rc and "evap" in rc):
        sp = 2.8
        pf = 60
        af = 100
        gs = 0.65
    elif "surface contamination" in rc or "silicone" in rc or "oil" in rc:
        sp = 2.2
        pf = 55
        af = 90
        gs = 0.50
    elif "degassing" in rc or "process contamination" in rc:
        sp = 2.6
        pf = 50
        af = 95
        gs = 0.55
    elif "low spray pressure" in rc:
        sp = 2.4
        pf = 58
        af = 85
        gs = 0.50
    elif "nozzle wear" in rc or "widened fan" in rc or "worn" in rc:
        # increase atomizing air and slightly reduce pressure; recommend maintenance when critical
        sp = 3.0 if spray_pressure_bar >= 3.0 else 2.8
        pf = 55
        af = 110
        gs = 0.65
    elif "gun-to-part distance" in rc or "distance" in rc or "close" in rc:
        sp = 2.2
        pf = 50
        af = 90
        gs = 0.55
    elif "excessive paint flow" in rc or "misalignment" in rc:
        sp = 2.6
        pf = 55
        af = 100
        gs = 0.60
    elif "isolated contaminant" in rc or "supply" in rc:
        sp = 2.4
        pf = 58
        af = 85
        gs = 0.50
    else:
        # fallback heuristics by detected_type + sensors
        if t == "orange_peel":
            if temperature_c < 18 and spray_pressure_bar <= 2.3:
                sp, pf, af, gs = 2.6, 65, 95, 0.60
            elif temperature_c >= 28 and humidity_pct < 35 and spray_pressure_bar >= 3.1:
                sp, pf, af, gs = 2.8, 60, 100, 0.65
            else:
                sp, pf, af, gs = 2.6, 64, 90, 0.55
        elif t == "fisheye":
            if humidity_pct >= 60:
                sp, pf, af, gs = 2.2, 55, 90, 0.50
            elif temperature_c >= 30 and humidity_pct < 35:
                sp, pf, af, gs = 2.6, 50, 95, 0.55
            else:
                sp, pf, af, gs = 2.4, 58, 85, 0.50
        elif t == "overspray":
            if spray_pressure_bar >= 3.2:
                sp, pf, af, gs = 3.0, 55, 110, 0.65
            else:
                sp, pf, af, gs = 2.6, 55, 100, 0.60
        else:
            # unknown type: keep defaults
            sp, pf, af, gs = LIMITS["spray_pressure"]["default"], LIMITS["paint_flow_rate"]["default"], LIMITS["atomizing_air_flow"]["default"], LIMITS["gun_traverse_speed"]["default"]
    
    # clamp to limits & steps
    sp = clamp_step(sp, LIMITS["spray_pressure"]["min"], LIMITS["spray_pressure"]["max"], LIMITS["spray_pressure"]["step"])
    pf = int(clamp_step(pf, LIMITS["paint_flow_rate"]["min"], LIMITS["paint_flow_rate"]["max"], LIMITS["paint_flow_rate"]["step"]))
    af = int(clamp_step(af, LIMITS["atomizing_air_flow"]["min"], LIMITS["atomizing_air_flow"]["max"], LIMITS["atomizing_air_flow"]["step"]))
    gs = clamp_step(gs, LIMITS["gun_traverse_speed"]["min"], LIMITS["gun_traverse_speed"]["max"], LIMITS["gun_traverse_speed"]["step"])
    
    spray_params = {
        "spray_pressure": {"value": sp, "unit": LIMITS["spray_pressure"]["unit"]},
        "paint_flow_rate": {"value": pf, "unit": LIMITS["paint_flow_rate"]["unit"]},
        "atomizing_air_flow": {"value": af, "unit": LIMITS["atomizing_air_flow"]["unit"]},
        "gun_traverse_speed": {"value": gs, "unit": LIMITS["gun_traverse_speed"]["unit"]},
    }
    
    trigger = None
    if issue_critical:
        # Decide trigger based on root cause severity keywords and detected_type
        rc_low = rc.lower()
        if "surface contamination" in rc_low or "silicone" in rc_low or "oil" in rc_low or "nozzle wear" in rc_low or "degassing" in rc_low or "supply" in rc_low:
            trigger = "triggers maintenance"
        else:
            trigger = "human operators"
    
    return {"spray_parameters_to_set": spray_params, "trigger": trigger}

if __name__ == "__main__":
    # --- Example usage ---
    examples = [
        # (detected_type, issue_critical, temp, hum, pressure)
        ("orange_peel", False, 16.5, 40.0, 2.0),
        ("orange_peel", True, 30.0, 28.0, 3.5),
        ("fisheye", True, 22.0, 70.0, 2.5),
        ("fisheye", False, 31.0, 25.0, 2.0),
        ("overspray", False, 21.0, 45.0, 3.0),
        ("overspray", True, 24.0, 30.0, 3.5),
    ]

    for ex in examples:
        det, crit, t, h, p = ex
        rc = get_root_cause(det, crit, t, h, p)
        actions = recommend_actions_from_root(det, crit, t, h, p, rc)
        print(f"Example: {det}, critical={crit}, T={t}, H={h}, P={p}")
        print("  root_cause:", rc)
        print("  actions:", actions)
        print()

