# ABI-156 full-spectral BTD+SZA feature-calibrated full-scale skip ASPP/detail decoder BCE-Dice centerline auxiliary

Family-development continuation for GOES ABI Contrail Segmentation. This candidate keeps ABI-154's provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD front end, trusted BCE-Dice primary loss, combined source-balanced traversal, trusted random mirroring, AdamW learning rate, and low-weight provider-derived Centerline Target auxiliary head.

The controlled architecture change is a bounded Solar Geometry Input-conditioned feature calibrator applied to the concatenated decoder, detail, stem, and full-scale skip features before final projection and line-aware refinement. ABI-155's final mask-head calibration did not recover default-threshold recall; ABI-156 tests whether earlier feature-fusion calibration can shift the operating point while preserving ABI-154's precision/connectivity and negative-patch discipline.

The model uses only GOES ABI channels 1-16 plus Solar Geometry Input. It derives deterministic thermal BTD planes and normalized SZA features from provider-approved inputs, and it receives no longitude, latitude, reconstructed coordinates, Dataset Source identity, external data, or pretrained weights.

All data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, and Run lifecycle remain provider/Harness-owned.
