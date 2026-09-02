# ABI-101 full-spectral BTD ConvNeXt U-Net focal-Tversky centerline-auxiliary scout

Family-scout Candidate for GOES ABI Contrail Segmentation. This candidate broadens away from the frequency-gated line U-Net's hand-built high/low-frequency gates by testing a compact ConvNeXt-style encoder-decoder: normalized ABI channels and ABI-channel-derived thermal BTD planes feed depthwise large-kernel residual blocks with learned per-channel scaling, U-Net skip fusion, and a shallow high-resolution prediction refiner.

The hypothesis is that stable depthwise large-kernel context can improve source-robust line continuity and threshold discipline without the positive-area expansion seen in recent additive/gated refiners. The model uses only provider-approved ABI channels 1-16 plus derived BTD planes from those same channels; it receives no longitude, latitude, or reconstructed coordinate inputs.

All data loading, split logic, sampling, augmentation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned.
