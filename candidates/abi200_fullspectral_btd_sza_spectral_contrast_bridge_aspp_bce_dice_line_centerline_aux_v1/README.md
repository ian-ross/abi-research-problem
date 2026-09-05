# ABI-200 full-spectral BTD+SZA spectral-contrast bridge ASPP

ABI-200 is a bounded exploratory architecture/front-end continuation after ABI-196 through ABI-199. It keeps provider-approved `abi_16ch_plus_sza` inputs, ABI-channel-derived BTD features, trusted `bce_dice`, trusted Line and Centerline auxiliary targets, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW at 0.0003, batch size 4, and the 12-epoch exploratory budget.

The architecture starts from the finite signed-detail full-scale skip ASPP lineage but replaces the ridge-detail bridge with `SpectralContrastDetailBridge`. The bridge fuses decoder/stem/detail features with the existing front-end BTD plus SZA contrast slice through a bounded zero-initialized residual before ordinary line-aware refinement and mask/line/centerline heads.

Candidate code defines model architecture only. It does not use longitude/latitude inputs, data loading, custom losses, custom metrics, target transforms, augmentation transforms, thresholding, postprocessing, Artifact Filters, sampling implementation, runtime downloads, filesystem persistence, or Candidate-owned scheduling.

Primary comparison target: ABI-196 `run_20260903_195527_248472`. Secondary references: ABI-184, ABI-195, ABI-197, ABI-198, ABI-199, ABI-181, and ABI-192.
