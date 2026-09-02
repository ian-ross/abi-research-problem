# ABI-120 full-spectral BTD ASPP/detail decoder clDice centerline auxiliary

Family-scout Candidate for GOES ABI Contrail Segmentation. This candidate keeps the successful ABI-052-style normalized full-spectral ABI channels plus deterministic thermal BTD features, but replaces the SMP DeepLabV3+ decoder with a compact torch-only encoder-decoder using an ASPP bottleneck, high-resolution detail/context stem, and learned line-aware refinement.

The hypothesis is that an explicit ASPP context path plus full-resolution detail fusion can improve MIT/source balance and recover thin-line recall/connectivity relative to the DeepLabV3+ BTD clDice family without adding candidate-owned thresholding or Artifact Filters. The model uses only provider-approved ABI channels 1-16 and BTD planes derived from those same channels; it receives no longitude, latitude, Solar Geometry Input, or reconstructed coordinate features.

All data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, and Run lifecycle remain provider/Harness-owned.
