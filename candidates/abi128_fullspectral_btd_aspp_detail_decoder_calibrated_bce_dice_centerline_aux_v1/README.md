# ABI-128 full-spectral BTD ASPP/detail decoder calibrated BCE-Dice centerline auxiliary

Family-development continuation for GOES ABI Contrail Segmentation. This candidate keeps ABI-126's compact full-spectral BTD ASPP/detail encoder-decoder, provider-approved ABI channels 1-16, deterministic thermal BTD planes derived only from those channels, high-resolution detail/context fusion, trusted `bce_dice` primary loss, and low-weight provider-derived Centerline Target auxiliary supervision.

The controlled architecture change is a calibration-aware primary mask head. Instead of one 1x1 mask-logit projection, the head learns a foreground-minus-background margin, a broad-context/detail gate, a small residual logit, and a gentle trainable global logit scale/bias initialized to a mildly more recall-friendly operating point. This targets ABI-126's whole-validation diagnosis: good positive-area discipline, precision, connectivity, and Google Dice, but conservative fixed-threshold recall, especially on MIT.

The model uses only provider-approved GOES ABI channels 1-16 and BTD planes derived from those same channels. It receives no longitude, latitude, Solar Geometry Input, or reconstructed coordinate features.

All data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, and Run lifecycle remain provider/Harness-owned.
