# ABI-363 full-spectral BTD+SZA source-robust detail-support late36

ABI-363 is a mechanism-changing family-development continuation for GOES ABI Contrail Segmentation. It keeps provider-owned `abi_16ch_plus_sza` inputs, trusted source-balanced sampling, random mirroring, BCE-Dice loss, and Line/Centerline auxiliary targets, but broadens away from local C4-head tuning after ABI-362.

The model uses a normalized full-spectral ABI + Solar Geometry Input + approved BTD front end, a residual U-Net/ASPP backbone, and a source-agnostic multi-scale signed-detail support path. Region, axis line-support, and detail-tail evidence are fused by an architecture-internal dual-evidence calibration head to raise fixed-threshold positive-tail logits without candidate-owned thresholds, postprocessing, data loading, losses, metrics, Artifact Filters, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

This Candidate requests the approved `late_improving` budget through `budget_request.yaml` because relevant single-frame parents selected late checkpoints. If the request is denied, the exploratory fallback remains valid bounded evidence.
