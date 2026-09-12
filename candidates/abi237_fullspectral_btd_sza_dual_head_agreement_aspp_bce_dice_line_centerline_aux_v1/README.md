# ABI-237 full-spectral BTD+SZA dual-head agreement ASPP

ABI-237 is a bounded scout for GOES ABI Contrail Segmentation. It consumes provider-owned `abi_16ch_plus_sza` tensors and tests whether an internal recall/precision dual-head agreement fusion can improve calibration-like behavior while preserving the trusted single-output `mask_logits` contract.

The Candidate uses only architecture code plus allowlisted manifest settings. It does not own data loading, target creation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, coordinates, Dataset Source identity, downloads, or scheduling.
