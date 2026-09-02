# ABI-126 full-spectral BTD ASPP/detail decoder BCE-Dice centerline auxiliary

Family-development continuation for GOES ABI Contrail Segmentation. This candidate preserves the ABI-121 compact torch-only ASPP/detail encoder-decoder architecture, normalized full-spectral ABI channels, deterministic thermal BTD features derived only from approved ABI channels, learned spectral projection, high-resolution detail/context fusion, and low-weight provider-derived Centerline Target auxiliary head.

The controlled change from ABI-121 is the trusted primary loss: `focal_tversky` is replaced by `bce_dice`. ABI-121's capped and whole-validation diagnostics showed strong recall and source balance but persistent low-confidence clutter and weak connectivity, while ABI-120's `bce_dice_cldice` version was more precision-forward but recall-limited. This BCE-Dice middle point tests whether the same ASPP/detail architecture can reduce focal-Tversky positive-area clutter without returning all the way to the clDice branch's conservative recall.

The model uses only provider-approved GOES ABI channels 1-16 and BTD planes derived from those same channels. It receives no longitude, latitude, Solar Geometry Input, or reconstructed coordinate features.

All data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, and Run lifecycle remain provider/Harness-owned.
