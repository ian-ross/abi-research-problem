# ABI-318 full-spectral BTD+SZA C4 detail/support recall-router U-Net

ABI-318 is a bounded exploratory Candidate Experiment for GOES ABI Contrail Segmentation. It keeps the provider-approved single-frame `abi_16ch_plus_sza` input and a compact C4 steerable line-context U-Net lineage, but changes the recall-support mechanism after ABI-303/317.

The model uses C4 orientation-shared strip context, signed high-resolution detail, and cross-scale decoder support to route a small bounded non-negative recall lift into `mask_logits`. The lift is attenuated by learned disagreement/guard evidence but is not thresholding, morphology, connected-component logic, postprocessing, an Artifact Filter, a custom loss, a metric, data loading, sample selection, coordinates, or resource scheduling.

## Files

- `manifest.yaml` declares the trusted ABI+SZA input mode, combined source-balanced sampling, trusted random mirroring, BCE-Dice training, and Line/Centerline auxiliary targets.
- `model.py` defines the PyTorch model and the `build_model` entry point.
- `PROPOSAL.md` records the hypothesis, comparison targets, budget, success criteria, and fallback decision.

## Expected evidence

This is capped representative feasibility evidence only. Primary comparisons are ABI-202, ABI-249, ABI-279/280, ABI-303, and ABI-317. The branch should continue only if it gives finite source-informative evidence that routed C4/detail/cross-scale support improves fixed-threshold recall or connected-line continuity without ABI-292-style clutter broadening.
