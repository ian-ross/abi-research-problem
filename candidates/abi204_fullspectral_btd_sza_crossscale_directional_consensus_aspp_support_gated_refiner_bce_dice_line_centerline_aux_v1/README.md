# ABI-204 full-spectral BTD+SZA support-gated cross-scale directional-consensus ASPP

ABI-204 is a controlled exploratory family-development continuation of ABI-202 after ABI-203 showed that post-refinement mask-logit calibration was not a useful clutter-control mechanism.

It keeps provider-approved `abi_16ch_plus_sza` inputs, ABI-channel-derived BTD features, trusted `bce_dice`, trusted Line and Centerline auxiliary targets, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW at 0.0003, batch size 4, constant scheduling, and the 12-epoch exploratory budget.

The architecture-only change replaces ABI-202's ordinary final line-aware refinement with a support-gated line refiner that acts on feature maps before the mask, line, and centerline heads. Candidate code does not implement data loading, losses, metrics, target derivation, Artifact Filters, thresholding, postprocessing, coordinate features, training loops, runtime downloads, or resource scheduling.
