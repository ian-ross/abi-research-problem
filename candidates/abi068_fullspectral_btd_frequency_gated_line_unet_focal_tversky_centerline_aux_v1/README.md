# ABI-068 full-spectral BTD frequency-gated line U-Net focal-Tversky continuation

Family-development Candidate for GOES ABI Contrail Segmentation. This candidate keeps the ABI-066 frequency-gated line U-Net architecture unchanged and changes only the trusted primary loss from `bce_dice_cldice` to allowlisted `focal_tversky`. The centerline auxiliary output and trusted weighted-BCE auxiliary loss remain at weight 0.02.

The hypothesis is that focal-Tversky can recover recall and improve the operating point of the frequency-gated branch without surrendering the false-positive suppression and connectivity behavior that made ABI-066 the strongest local capped reference. The model uses only provider-approved ABI channels 1-16 plus derived BTD planes from those same channels; it receives no longitude, latitude, or reconstructed coordinate inputs.

All data loading, split logic, sampling, augmentation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned.
