from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langchain_core.messages import AIMessage

from typing import TypedDict, Dict
from core.dummy import get_root_cause

# from core.pydentic_models import AgentState





# Reasoning layer tools



@tool
def root_cause_detection_tool(temperature_c: float, issue_critical: bool, humidity_pct: float, spray_pressure_bar: float, defect_type: str, **other_sensors: Dict) -> str:
    """
    Detects root cause of defects using historical data and current conditions
    args:
        temperature_c: float
        issue_critical: bool
        humidity_pct: float
        spray_pressure_bar: float
        defect_type: str
        **other_sensors: Dict 
    returns:
        root_cause: str
    """
    
    # Determine root cause
    # root_cause = infer_cause(temperature_c, humidity_pct, spray_pressure_bar, defect_type)
    root_cause = get_root_cause(defect_type, issue_critical, temperature_c, humidity_pct, spray_pressure_bar)
    

    return root_cause



## Action layer tools
@tool
def adjusts_spray_parameters_via_PLC_integration(spray_pressure: float, paint_flow_rate: float, atomizing_air_flow: float, gun_traverse_speed: float) -> str:
    """
    Adjusts spray parameters via PLC integration.
    args:
        spray_pressure: float
        paint_flow_rate: float
        atomizing_air_flow: float
        gun_traverse_speed: float
    returns:
        updated_spray_parameters: dict
    """
    # logic to adjust spray parameters via PLC integration
    updated_spray_parameters = {
        "spray_pressure": spray_pressure,
        "paint_flow_rate": paint_flow_rate,
        "atomizing_air_flow": atomizing_air_flow,
        "gun_traverse_speed": gun_traverse_speed
    }

    return f"Adjusted spray parameters to {updated_spray_parameters}"

@tool
def triggers_maintenance_workflows(defect_type: str) -> str:
    """
    Triggers maintenance workflows.
    """
    # logic to trigger maintenance workflows for defect type
    return "Maintenance workflows triggered"

@tool
def human_operators(defect_type: str) -> str:
    """
    Triggers human operators.
    """
    # logic to trigger human operators for defect type
    return "Human operators informed"

# tools sets
tools_set_reasoning_layer = [root_cause_detection_tool]
tools_set_action_layer = [adjusts_spray_parameters_via_PLC_integration, triggers_maintenance_workflows, human_operators]


# make tool node
def make_tool_node(layer_attr: str, AgentState: TypedDict, tools_list: list[tool]):
    tool_by_name = {t.name: t for t in tools_list}
    def run(state: AgentState):
        msgs = state.get(layer_attr, [])
        if not msgs:
            return {}
        last = msgs[-1]
        if not isinstance(last, AIMessage) or not getattr(last, "tool_calls", None):
            return {}
        outs = []
        for tc in last.tool_calls:
            name, args, call_id = tc["name"], tc.get("args", {}), tc["id"]
            tool = tool_by_name.get(name)
            try:
                result = tool.invoke(args) if tool else f"Tool '{name}' not found."
            except Exception as e:
                result = f"Tool error: {e}"
            outs.append(ToolMessage(content=str(result), tool_call_id=call_id))
        return {layer_attr: outs}
    return run

# old code
# def infer_cause(temperature_c: float, humidity_pct: float, spray_pressure_bar: float, defect_type: str) -> str:
#     """
#     Infer root cause of defects using historical data and current conditions
#     """
#     # Logic here
#     # infer_cause is a function that takes in the temperature, humidity, spray pressure, and defect type
#     # could be Rule based/statistical mode/NN (time series/ not depending on data) 
#     # returns the root cause based on `historical data + current condition`

    
#     return "issue in spray pressure"

# tool_by_name = {t.name: t for t in tools_set_1}
# def make_tool_node(layer_attr: str):
#     def run(state: AgentState):
#         msgs = state.get(layer_attr, [])
#         if not msgs:
#             return {}
#         last = msgs[-1]
#         if not isinstance(last, AIMessage) or not getattr(last, "tool_calls", None):
#             return {}
#         outs = []
#         for tc in last.tool_calls:
#             name, args, call_id = tc["name"], tc.get("args", {}), tc["id"]
#             tool = tool_by_name.get(name)
#             try:
#                 result = tool.invoke(args) if tool else f"Tool '{name}' not found."
#             except Exception as e:
#                 result = f"Tool error: {e}"
#             outs.append(ToolMessage(content=str(result), tool_call_id=call_id))
#         return {layer_attr: outs}
#     return run


