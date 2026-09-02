# ABI-089 full-spectral BTD context-detail agreement U-Net

Family-development Candidate for GOES ABI Contrail Segmentation. This candidate continues from ABI-068's full-spectral BTD frequency-gated line U-Net but replaces the final frequency-pyramid fusion block with a parallel context/detail agreement fusion module before the existing oriented line refiner.

The hypothesis is that separating full-resolution high-frequency line evidence from smoothed decoder context, then allowing the two streams to exchange learned residual corrections, may preserve ABI-068's recall/source-balanced Dice while recovering some of ABI-066's precision and connectivity. The model uses only provider-approved ABI channels 1-16 plus brightness-temperature-difference planes derived from those same channels; it receives no longitude, latitude, or reconstructed coordinate inputs.

All data loading, split logic, sampling, augmentation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned.
