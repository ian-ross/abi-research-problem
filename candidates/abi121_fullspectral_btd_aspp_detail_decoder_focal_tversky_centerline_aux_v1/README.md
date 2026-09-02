# ABI-121 full-spectral BTD ASPP/detail decoder focal-Tversky centerline auxiliary

Family-development continuation for GOES ABI Contrail Segmentation. This candidate preserves the ABI-120 compact torch-only ASPP/detail encoder-decoder architecture, normalized full-spectral ABI channels, deterministic thermal BTD features derived only from approved ABI channels, learned spectral projection, high-resolution detail/context fusion, and low-weight provider-derived Centerline Target auxiliary head.

The controlled change from ABI-120 is the trusted primary loss: `bce_dice_cldice` is replaced by `focal_tversky`. The hypothesis is that the ASPP/detail geometry already delivered a strong precision-forward, source-balanced clDice scout relative to the DeepLabV3+ BTD clDice branch; focal-Tversky may recover recall and aggregate/source Dice while preserving enough of the architecture's positive-area discipline.

The model uses only provider-approved GOES ABI channels 1-16 and BTD planes derived from those same channels. It receives no longitude, latitude, Solar Geometry Input, or reconstructed coordinate features.

All data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, and Run lifecycle remain provider/Harness-owned.
