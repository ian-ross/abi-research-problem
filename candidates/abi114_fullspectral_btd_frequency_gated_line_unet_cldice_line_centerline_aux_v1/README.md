# ABI-114 full-spectral BTD frequency-gated line U-Net clDice line+centerline auxiliary continuation

Family-development Candidate for GOES ABI Contrail Segmentation. This candidate keeps the ABI-108 frequency-gated line U-Net architecture and its two trusted auxiliary outputs, but changes the trusted primary loss from `focal_tversky` to allowlisted `bce_dice_cldice`.

The hypothesis is that ABI-066's BCE-Dice-clDice precision/connectivity-forward operating point can benefit from the extra provider-derived Line Target supervision that ABI-108 tested under focal-Tversky. The intended effect is to recover some ABI-066-like connectivity and positive-area discipline while improving recall or Google/MIT balance relative to ABI-066, without candidate-owned losses, targets, thresholding, postprocessing, sampling, data loading, augmentation, metrics, Artifact Filters, resource placement, or lifecycle behavior.

The model uses only provider-approved GOES ABI channels 1-16 plus deterministic BTD planes derived from those channels. It receives no longitude, latitude, reconstructed coordinate inputs, external files, pretrained weights, or network resources.
