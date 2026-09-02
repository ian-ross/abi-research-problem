# ABI-169 full-spectral BTD+SZA full-scale skip ASPP/detail decoder clDice centerline auxiliary

Family-development continuation for GOES ABI Contrail Segmentation. This candidate keeps ABI-154's provider-approved `abi_16ch_plus_sza` input, full-scale skip ASPP/detail decoder architecture, combined source-balanced traversal, trusted random mirroring, AdamW learning rate, batch size, epoch budget, and low-weight provider-derived Centerline Target auxiliary head.

The controlled manifest change is the trusted primary loss: ABI-169 uses `bce_dice_cldice` instead of ABI-154's `bce_dice`. The goal is to test whether the full-scale skip architecture's strong precision/connectivity operating point can gain thin-line recall or MIT/source balance from a continuity-aware trusted loss without candidate-owned thresholding or postprocessing.

The model uses only GOES ABI channels 1-16 plus Solar Geometry Input. It derives deterministic thermal BTD planes and normalized SZA features from provider-approved inputs, and it receives no longitude, latitude, reconstructed coordinates, Dataset Source identity, external data, or pretrained weights.

All data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, and Run lifecycle remain provider/Harness-owned.
