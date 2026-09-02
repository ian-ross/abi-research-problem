# ABI-067 full-spectral BTD frequency-gated line U-Net centerline-weight continuation

Family-development continuation of ABI-066 for GOES ABI Contrail Segmentation. The model architecture is intentionally unchanged from the frequency-gated line U-Net: provider-approved ABI channels 1-16 are normalized, thermal BTD planes are derived only from those channels, and an internal high/low spatial-frequency split gates thin-line evidence against smooth cloud/background context.

The controlled change is manifest-only: retain trusted `bce_dice_cldice` but lower the provider-derived `centerline` auxiliary `weighted_bce` loss weight from 0.02 to 0.01. This tests whether ABI-066s whole-validation low-recall/calibration gap can be eased without losing its false-positive suppression and connectivity gains.

All data loading, sampling, augmentation, loss computation, target derivation, metrics, thresholding, and Artifact Filters remain provider/Harness-owned.
