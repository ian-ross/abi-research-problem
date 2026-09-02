# ABI-122 full-spectral BTD ASPP/detail decoder directional-continuity focal-Tversky centerline auxiliary

Family-development continuation for GOES ABI Contrail Segmentation. This candidate preserves ABI-121's compact torch-only ASPP/detail encoder-decoder, normalized full-spectral ABI channels, deterministic thermal BTD features derived only from approved ABI channels, learned spectral projection, high-resolution detail/context fusion, trusted `focal_tversky` primary loss, and low-weight provider-derived Centerline Target auxiliary supervision.

The controlled architectural change is a non-suppressive high-resolution directional-continuity refinement block before the mask and centerline heads. The block adds learned short and long horizontal/vertical line-context branches plus dilated local context as a residual feature update. It is intended to improve the low connectivity observed in ABI-121 while preserving ABI-121's recall and source balance.

The model uses only provider-approved GOES ABI channels 1-16 and BTD planes derived from those same channels. It receives no longitude, latitude, Solar Geometry Input, or reconstructed coordinate features.

All data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, and Run lifecycle remain provider/Harness-owned.
