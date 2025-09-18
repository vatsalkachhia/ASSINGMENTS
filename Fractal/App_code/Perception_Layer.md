# 🏆 Approaches

---

## 1) Multimodal Deep Fusion (Image + Sensors)
- Why this approach?
  - Combines visual evidence with temperature/humidity/spray pressure to improve defect-type classification and determine criticality using both appearance and context. Aligns with real-time monitoring, root-cause reasoning, and autonomous control.
- Pros:
  - Higher accuracy and robustness, especially for look-alike defects with different causes.
  - Multi-task learning: one model can output defect type, severity score, and critical/non-critical.
  - Sensor pathways enable root-cause hints and proactive adjustments before defects become critical.
  - Can handle missing sensors via masking; attention/feature importance aids interpretability.
- Cons:
  - Time alignment and synchronization of images with sensor logs is non-trivial.
  - More complex training and MLOps; higher risk of overfitting with small labeled sets.
  - Moderate compute and memory footprint; careful optimization for edge real-time.

## 2) Pixel-Level Segmentation and Instance Detection (U-Net/DeepLab/Mask R-CNN)
- Why this approach?
  - Criticality depends on area, density, location, and count. Segmentation/detection gives precise localization to compute severity and supports multiple defects per panel.
- Pros:
  - Direct derivation of severity metrics (area, distance to edges, density) for criticality.
  - Clear visual overlays for operators; improves trust and verification.
  - Handles mixed/overlapping defects better than pure classification.
  - Enables consistent downstream rules (e.g., zone-based weights for customer-visible regions).
- Cons:
  - Costly, time-consuming pixel/instance annotations; class imbalance common.
  - Heavier compute; may require pruning/quantization for line-speed constraints.
  - Sensitive to domain shifts (lighting, color) without robust augmentation/updates.

## 3) Hybrid Ensemble with Guardrails
- Why this approach?
  - Production-grade reliability: combine a supervised segmenter/classifier for known defects, an anomaly detector for unknowns, and rule-based thresholds for criticality. Provides safety nets and graceful degradation.
- Pros:
  - Robust to novel/rare defects; anomaly layer catches unknowns.
  - Calibrated risk by fusing segmentation severity, sensor risk, and business rules.
  - Transparent guardrails for critical decisions; easier to meet quality/compliance requirements.
  - Supports phased rollout and incremental improvements without full retrains.
- Cons:
  - More components to integrate, monitor, and maintain.
  - Requires calibration and conflict-resolution logic when model votes disagree.
  - Higher inference cost if all components run concurrently; may need cascading.

# Others Approaches
- Rule-based computer vision + sensor thresholds
- Classical ML with hand-crafted features (late fusion)
- Supervised deep image classifier (image-only)
- Unsupervised/weakly supervised anomaly detection (open-set)
- Self-supervised + semi-supervised learning with active learning
- Spatiotemporal modeling (video + time-series fusion)
- Causal/Bayesian modeling for root cause and risk
- Few-shot/open-set classifiers
- Synthetic data and domain adaptation
