# ABI-152 full-spectral BTD+SZA ASPP/detail decoder no-augmentation continuation

Family-development continuation for GOES ABI Contrail Segmentation. ABI-152 reuses the finite ABI-130 SZA-aware ASPP/detail BCE-Dice architecture and changes only the trusted augmentation policy from `random_mirroring` to `none`.

The model receives only provider-approved `abi_16ch_plus_sza`: GOES ABI channels 1-16 plus Solar Geometry Input. It computes normalized raw ABI features, deterministic thermal BTD features from approved ABI channels, normalized SZA/`cos(SZA)`, and learned 1x1 spectral/SZA mixtures. It does not receive longitude, latitude, reconstructed coordinates, Dataset Source identity, external weights, runtime downloads, thresholding, postprocessing, or Artifact Filters.

Provider/Harness code retains ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, target derivation, trusted loss functions, metrics, thresholding, Artifact Filters, prediction retention, resource placement, and Run lifecycle. The manifest keeps trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, batch size 4, and the current 12-epoch capped representative budget.
