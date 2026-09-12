# ABI-238 temporal-attention directional-context U-Net late36

ABI-238 is a bounded family-development continuation of ABI-223 for GOES ABI Contrail Segmentation.

It preserves ABI-223's provider-owned `abi_16ch_plus_sza_temporal` input with offsets `[-1, 0, 1]`, `temporal_eligible_center` frame policy, source-balanced sampling, trusted random mirroring, BCE-Dice loss, AdamW constant learning rate, batch size 2, and trusted Line/Centerline auxiliary outputs. Candidate code only defines the PyTorch architecture.

The one architecture change is a small full-resolution directional-context bridge after the final decoder refinement. The bridge applies residual horizontal, vertical, and dilated diagonal/local context branches with a learned gate before the `mask_logits`, `line_logits`, and `centerline_logits` heads. The hypothesis is that this can recover thin-line recall and connectivity that ABI-223 still lacked relative to ABI-202 while preserving ABI-223's temporal precision and source-informative behavior.

A candidate-local `budget_request.yaml` requests the approved `late_improving` 36-epoch budget using ABI-223 (`run_20260908_154531_8c7e2b`) as parent evidence; fallback is the exploratory budget if denied.

## Contract boundary

This Candidate does not implement data loading, temporal lookup, temporal padding/repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinate inputs, Dataset Source identity, or resource scheduling.
