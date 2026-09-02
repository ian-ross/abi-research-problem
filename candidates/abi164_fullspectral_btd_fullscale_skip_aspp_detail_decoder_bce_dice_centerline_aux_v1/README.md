# ABI-164 full-spectral BTD full-scale skip ASPP/detail decoder BCE-Dice centerline auxiliary

Family-development continuation for GOES ABI Contrail Segmentation. This candidate starts from the ABI-154 full-scale skip ASPP/detail decoder but removes provider-approved Solar Geometry Input, using only the ABI 1-16 tensor plus deterministic thermal brightness-temperature-difference planes derived from those approved ABI channels.

The controlled input/front-end change tests whether ABI-154's whole-validation precision/connectivity gain came from full-scale skip aggregation rather than SZA-conditioned calibration. The goal is to preserve ABI-154-style precision, connectivity, and positive-area discipline while reducing the Google/recall/source-balance trade-off seen in the SZA-aware branch.

The manifest keeps trusted BCE-Dice loss, combined source-balanced traversal, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, 12 epochs, constant learning rate, and a provider-derived Centerline Target auxiliary output with trusted weighted BCE weight 0.02.

The model receives no longitude, latitude, reconstructed coordinates, Dataset Source identity, external data, pretrained weights, or candidate-owned thresholds/postprocessing. Provider/Harness code remains responsible for data loading, Leakage-Safe Split, capped-record selection, sampling, augmentation, target derivation, losses, metrics, Artifact Filters, prediction retention, resource placement, and Run lifecycle.
