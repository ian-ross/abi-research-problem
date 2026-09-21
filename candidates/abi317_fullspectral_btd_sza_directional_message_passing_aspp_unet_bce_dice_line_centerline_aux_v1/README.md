# ABI-317 full-spectral BTD+SZA directional message-passing ASPP U-Net

ABI-317 is a bounded exploratory Candidate Experiment for GOES ABI Contrail Segmentation. It keeps the provider-approved single-frame `abi_16ch_plus_sza` input and an ABI-202-style signed-detail ASPP U-Net, but replaces the final consensus bridge with an architecture-internal directional message-passing continuity bridge.

The bridge propagates decoder/detail evidence along horizontal, vertical, and diagonal directions over multiple no-wrap shift distances, then gates those line messages with cross-scale and detail agreement before a bounded residual refinement. The goal is connected thin-line support without Candidate-owned thresholds, morphology, postprocessing, Artifact Filters, custom losses, metrics, data loading, sample selection, coordinates, or resource scheduling.

## Files

- `manifest.yaml` declares trusted input mode, sampling/augmentation policy, BCE-Dice training, and Line/Centerline auxiliary targets.
- `model.py` defines the PyTorch model and `build_model` entry point.
- `PROPOSAL.md` records the hypothesis, comparison targets, budget, success criteria, and fallback decision.

## Expected evidence

This is capped representative feasibility evidence only. Primary comparisons are ABI-202, ABI-249, ABI-279/280, ABI-302, and ABI-303. The branch should continue only if it gives finite source-informative evidence of improved or diagnostically distinct recall/precision/connectivity behavior.
