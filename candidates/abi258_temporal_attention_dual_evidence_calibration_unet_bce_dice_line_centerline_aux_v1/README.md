# ABI-258 temporal attention dual-evidence calibration U-Net

Candidate Experiment for GOES ABI Contrail Segmentation.

ABI-258 is a temporal-attention family-development continuation after ABI-223, ABI-254, ABI-255, and ABI-257. It keeps provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]` and ABI-223's compact temporal-attention fusion U-Net, then replaces the simple final mask head with a bounded dual recall/precision evidence-calibration head.

The Candidate uses only contract-owned features: source-balanced sampling, temporal-eligible frame selection, trusted random mirroring, BCE-Dice primary loss, AdamW with constant learning rate, and trusted Line/Centerline auxiliary targets. Candidate code defines model architecture only and does not implement data loading, temporal lookup, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, coordinates, or resource scheduling.
