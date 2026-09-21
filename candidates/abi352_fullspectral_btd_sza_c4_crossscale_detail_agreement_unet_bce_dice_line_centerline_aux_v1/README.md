# ABI-352 full-spectral BTD+SZA C4 cross-scale detail agreement U-Net

ABI-352 is an exploratory family-development continuation of the single-frame C4/orientation branch. It starts from the ABI-249-style full-spectral BTD+Solar Geometry Input compact C4 U-Net, but replaces direct final-logit recall bridges with a pre-head cross-scale detail-agreement block.

The hypothesis is that full-resolution decoder features, high-resolution signed detail, stem evidence, and coarser decoder context can agree with C4 line context before the final mask head to improve fixed-threshold recall and connected-line continuity without candidate-owned thresholding or postprocessing.

This Candidate uses only provider-approved `abi_16ch_plus_sza` tensors, trusted source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, AdamW constant learning rate, and trusted Line/Centerline auxiliary targets. It requests the default exploratory budget only.

Candidate code defines model architecture only. It does not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, filesystem probes, coordinate inputs, Dataset Source identity, resource placement, or lifecycle behavior.
