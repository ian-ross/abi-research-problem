# ABI-066 full-spectral BTD frequency-gated line U-Net

Family-scout Candidate for GOES ABI Contrail Segmentation. The model uses only provider-approved ABI channels 1-16, explicit thermal BTD planes from those channels, and a learned spectral mixer. Its distinctive mechanism is an internal high/low spatial-frequency split: local residual detail emphasizes thin line evidence, while smoothed context gates skip and decoder features to test whether small false positives on negative ABI Patches can be reduced without losing centerline-supervised contrail continuity.

All data loading, sampling, augmentation, loss computation, target derivation, metrics, thresholding, and Artifact Filters remain provider/Harness-owned.
