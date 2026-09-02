# ABI-113 full-spectral BTD patch-anomaly line U-Net

ABI-113 is a controlled family-development continuation of ABI-068. It keeps the frequency-gated line U-Net, trusted focal-Tversky primary loss, and provider-derived Centerline Target auxiliary supervision, but widens the model-owned front end with patch-relative raw and BTD anomaly planes.

The front end uses only provider-approved GOES ABI channels 1-16. It concatenates fixed normalized raw channels, fixed thermal BTD planes, per-patch z-scored raw-channel anomalies, per-patch z-scored BTD anomalies, and a small learned 1x1 projection of those features. The goal is source/background-adaptive thin-line calibration without candidate-owned data handling, thresholding, Artifact Filters, metrics, losses, augmentation, or postprocessing.

Expected comparison targets are ABI-068 (`run_20260828_010836_4ccc77`) for aggregate filtered Dice/source balance and ABI-066 (`run_20260827_230540_bf4ce3`) for precision/connectivity.
