# ABI-090 full-spectral BTD dual-decoder region/line U-Net

Family-scout Candidate for GOES ABI Contrail Segmentation. This candidate broadens away from ABI-068 post-decoder gating refinements by splitting the decoder itself into a smooth region-context path and a high-frequency line-detail path, then fusing those representations before the primary mask head.

The hypothesis is that maintaining separate region and line decoder streams can preserve ABI-068-like recall while recovering some ABI-066-like precision and connectivity, because broad cloud context and thin-line evidence are not forced through a single decoder representation. The model uses only provider-approved ABI channels 1-16 plus brightness-temperature-difference planes derived from those same channels; it receives no longitude, latitude, or reconstructed coordinate inputs.

All data loading, split logic, sampling, augmentation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned.
