# ABI-302 cross-scale directional-consensus ASPP with trusted clDice loss

ABI-302 is a one-factor training-policy continuation of the ABI-202 full-spectral BTD+SZA cross-scale directional-consensus ASPP architecture. It keeps the proven provider-approved `abi_16ch_plus_sza` model body, Line and Centerline auxiliary outputs, source-balanced sampling, random mirroring, AdamW, constant learning rate, and batch size 4, but changes the trusted primary loss from `bce_dice` to `bce_dice_cldice`.

The hypothesis is that provider-owned clDice connectivity pressure may improve connected thin-line continuity and fixed-threshold recall/source balance on the current aggregate-reference architecture without moving losses, metrics, thresholding, postprocessing, Artifact Filters, data loading, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle control into Candidate code.

Comparison targets are ABI-202 as the same-architecture BCE-Dice aggregate reference, ABI-249 as the compact high-precision C4 comparator, ABI-279 as the C4 recall/connectivity bridge diagnostic, ABI-184 as a precision/connectivity reference, and ABI-196 as a prior late36 aggregate comparator. The late-improving budget request is based on ABI-202 selecting epoch 34 and is Harness-validated; if denied, the exploratory fallback remains valid bounded evidence.
