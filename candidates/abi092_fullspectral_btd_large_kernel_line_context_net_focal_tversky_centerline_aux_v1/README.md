# ABI-092 full-spectral BTD large-kernel line-context net

Family-scout Candidate for GOES ABI Contrail Segmentation. This candidate broadens away from ABI-068-style frequency-gated U-Net refinements by using a depthwise large-kernel encoder-decoder: horizontal, vertical, local, and dilated context branches are inserted throughout the backbone to give thin contrails long spatial support without high-capacity transformer memory or output-side postprocessing.

The hypothesis is that large-kernel line context can preserve ABI-068-like recall while improving precision/connectivity or positive-area discipline, because broad cloud regions and elongated line structures receive separate convolutional evidence before feature fusion. The model uses only provider-approved ABI channels 1-16 plus brightness-temperature-difference planes derived from those same channels; it receives no longitude, latitude, or reconstructed coordinate inputs.

All data loading, split logic, sampling, augmentation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned.
