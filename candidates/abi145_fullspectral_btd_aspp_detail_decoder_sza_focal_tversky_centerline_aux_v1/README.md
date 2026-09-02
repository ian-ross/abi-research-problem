# ABI-145 full-spectral BTD+SZA ASPP/detail decoder focal-Tversky centerline auxiliary

Family-development continuation for GOES ABI Contrail Segmentation. This candidate preserves ABI-130's SZA-aware full-spectral BTD ASPP/detail encoder-decoder, combined source-balanced traversal, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, and low-weight provider-derived Centerline Target auxiliary head.

The controlled change is the trusted primary loss: `training.loss` changes from `bce_dice` to `focal_tversky`. The model uses provider-approved GOES ABI channels 1-16 plus Solar Geometry Input, with deterministic thermal BTD features derived only from approved ABI channels, normalized SZA, and `cos(SZA)` illumination features. It receives no longitude, latitude, reconstructed coordinate features, Dataset Source identity, or candidate-owned postprocessing.

The hypothesis is that focal-Tversky's recall pressure can recover MIT/source-balanced recall from the precise ABI-130 branch while SZA and the ASPP/detail decoder retain enough positive-area discipline and Google performance to stay competitive with ABI-068 and ABI-130.

All data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, and Run lifecycle remain provider/Harness-owned.
