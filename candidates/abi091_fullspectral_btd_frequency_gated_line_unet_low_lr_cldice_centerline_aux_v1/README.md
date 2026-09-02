# ABI-091 full-spectral BTD frequency-gated line U-Net low-LR clDice continuation

Family-development Candidate for GOES ABI Contrail Segmentation. This keeps the ABI-066 frequency-gated high/low spatial-feature architecture, trusted `bce_dice_cldice` primary loss, and provider-derived `centerline` auxiliary target at weight 0.02, but lowers the AdamW learning rate from 0.0003 to 0.0001.

The hypothesis is that the precision/connectivity-forward ABI-066 operating point may benefit from the same conservative trusted training-policy axis tested in ABI-085, without switching to focal-Tversky's higher-recall/higher-burden behavior. Candidate code uses only provider-approved ABI channels 1-16 and ABI-channel-derived BTD planes. All data loading, sampling, augmentation, loss computation, target derivation, metrics, thresholding, Artifact Filters, resource placement, and lifecycle behavior remain provider/Harness-owned.
