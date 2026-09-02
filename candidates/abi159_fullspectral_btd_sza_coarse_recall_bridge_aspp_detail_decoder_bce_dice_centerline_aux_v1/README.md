# ABI-159 full-spectral BTD+SZA coarse-recall-bridge ASPP/detail decoder BCE-Dice centerline auxiliary

Family-development continuation for GOES ABI Contrail Segmentation. This candidate keeps ABI-154's provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD planes, normalized Solar Geometry Input features, trusted BCE-Dice primary loss, combined source-balanced traversal, trusted random mirroring, AdamW learning rate, and low-weight provider-derived Centerline Target auxiliary head.

The controlled architecture change is a compact coarse recall bridge. The bridge projects ASPP context plus decoder levels and high-resolution detail to mask resolution, then fuses them before the final full-scale skip refinement. The hypothesis is that recall evidence should be injected before the last fused representation rather than by late logit bias or extra auxiliary heads, recovering some ABI-154 under-recall while preserving its precision/connectivity discipline.

The model uses only GOES ABI channels 1-16 plus Solar Geometry Input. It derives deterministic thermal BTD planes and normalized SZA features from provider-approved inputs, and it receives no longitude, latitude, reconstructed coordinates, Dataset Source identity, external data, or pretrained weights.

All data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, and Run lifecycle remain provider/Harness-owned.
