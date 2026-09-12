# ABI-262 full-spectral BTD+SZA overlap SegFormer line decoder

ABI-262 is a compact SegFormer/MiT-style modern-backbone family scout for GOES ABI Contrail Segmentation. It uses provider-approved `abi_16ch_plus_sza` inputs, derives only ABI-channel BTD/Solar Geometry Input features inside the architecture, and adds a line-aware high-resolution decoder for thin Contrail Mask evidence.

The Candidate is architecture-only. It does not own data loading, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, temporal lookup, coordinates, Dataset Source identity, scheduling, or training loops.

Expected outputs are `mask_logits`, `line_logits`, and `centerline_logits`, each `[1, 256, 256]`.
