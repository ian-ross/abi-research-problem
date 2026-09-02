# ABI-151 full-spectral BTD+SZA patch-anomaly ASPP/detail decoder

Candidate Experiment for GOES ABI Contrail Segmentation. ABI-151 is a family-development continuation of the ABI-130 SZA-aware ASPP/detail BCE-Dice branch.

The model receives only provider-approved `abi_16ch_plus_sza`: GOES ABI channels 1-16 plus Solar Geometry Input. It computes normalized raw ABI features, deterministic thermal BTD features from approved ABI channels, normalized SZA/cos(SZA), learned 1x1 spectral features, and bounded patch-relative anomaly features from the current approved input tensor. It does not receive longitude, latitude, reconstructed coordinates, Dataset Source identity, external weights, runtime downloads, thresholding, postprocessing, or Artifact Filters.

Provider/Harness code retains ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, trusted random mirroring, target derivation, losses, metrics, thresholding, Artifact Filters, prediction retention, resource placement, and Run lifecycle. The manifest keeps trusted `bce_dice` primary loss and provider-derived Centerline Target auxiliary supervision at weight 0.02.
