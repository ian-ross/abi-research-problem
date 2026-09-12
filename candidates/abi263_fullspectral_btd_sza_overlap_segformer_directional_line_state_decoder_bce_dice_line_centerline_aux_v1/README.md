# ABI-263 full-spectral BTD+SZA overlap SegFormer directional line-state decoder

ABI-263 is a SegFormer-family continuation after ABI-262 for GOES ABI Contrail Segmentation. It keeps provider-approved `abi_16ch_plus_sza` inputs and the compact overlap-attention encoder, then adds a high-resolution directional line-state decoder intended to improve thin-line connectivity without candidate-owned thresholding or postprocessing.

The Candidate is architecture-only. It does not own data loading, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, temporal lookup, coordinates, Dataset Source identity, scheduling, or training loops.

Expected outputs are `mask_logits`, `line_logits`, and `centerline_logits`, each `[1, 256, 256]`.
