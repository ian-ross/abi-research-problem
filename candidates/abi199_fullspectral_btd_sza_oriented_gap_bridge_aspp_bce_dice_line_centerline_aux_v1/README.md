# ABI-199 full-spectral BTD+SZA oriented gap bridge ASPP

ABI-199 is a bounded exploratory architecture continuation after ABI-196/197/198. It keeps provider-approved `abi_16ch_plus_sza` inputs, ABI-channel-derived BTD features, trusted `bce_dice`, trusted Line and Centerline auxiliary targets, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW at 0.0003, batch size 4, and the 12-epoch exploratory budget.

The architecture starts from the ABI-196 signed-detail full-scale skip ASPP lineage but replaces local mask-head calibration with an ungated `OrientedGapBridge` and `OrientedLineRefinement`. These modules fuse decoder, stem, full-scale, and high-resolution detail features with long horizontal/vertical and dilated gap-spanning context before ordinary mask/line/centerline heads.

Candidate code defines model architecture only. It does not use longitude/latitude inputs, data loading, custom losses, custom metrics, target transforms, augmentation transforms, thresholding, postprocessing, Artifact Filters, sampling implementation, runtime downloads, filesystem persistence, or Candidate-owned scheduling.

Primary comparison target: ABI-196 `run_20260903_195527_248472`. Secondary references: ABI-184, ABI-195, ABI-197, and ABI-198.
