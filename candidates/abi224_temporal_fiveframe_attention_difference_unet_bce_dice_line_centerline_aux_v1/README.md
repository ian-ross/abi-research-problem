# ABI-224 temporal five-frame attention/difference U-Net

ABI-224 is a sequential exploratory scout for GOES ABI Contrail Segmentation. It broadens the successful ABI-223 temporal-attention branch from three provider-owned frames to the allowlisted five-frame `[-2, -1, 0, 1, 2]` temporal window.

The model consumes only the trusted `abi_16ch_plus_sza_temporal` tensor with `frame_selection_policy: temporal_eligible_center`. For each frame it builds bounded ABI+SZA+BTD features, applies a shared frame projection, learns per-pixel temporal-attention weights relative to the center frame, and fuses the attended embedding with near-neighbor and far-neighbor signed/absolute temporal-difference evidence before a compact U-Net/ASPP decoder. It returns `mask_logits` plus trusted `line_logits` and `centerline_logits` auxiliary outputs.

Contract boundaries: no candidate-owned data loading, temporal lookup, missing-frame fallback, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, training loop, coordinate inputs, Dataset Source identity, downloads, or resource scheduling.
