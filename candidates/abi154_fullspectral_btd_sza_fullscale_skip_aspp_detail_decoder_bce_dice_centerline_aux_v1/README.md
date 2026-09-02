# ABI-154 full-spectral BTD+SZA full-scale skip ASPP/detail decoder BCE-Dice centerline auxiliary

Family-development continuation for GOES ABI Contrail Segmentation. This candidate keeps ABI-130's provider-approved `abi_16ch_plus_sza` input, trusted BCE-Dice primary loss, combined source-balanced traversal, trusted random mirroring, AdamW learning rate, and low-weight provider-derived Centerline Target auxiliary head.

The controlled architecture change is full-scale skip aggregation. The model projects the stem, all encoder levels, ASPP bottleneck, decoder levels, and high-resolution detail path to mask resolution before the final line-aware refinement. The goal is to recover some of ABI-126/ABI-066 connectivity and positive-area discipline while preserving ABI-130's SZA-aided default-threshold recall and Google performance.

The model uses only GOES ABI channels 1-16 plus Solar Geometry Input. It derives deterministic thermal BTD planes and normalized SZA features from provider-approved inputs, and it receives no longitude, latitude, reconstructed coordinates, Dataset Source identity, external data, or pretrained weights.

All data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, and Run lifecycle remain provider/Harness-owned.
