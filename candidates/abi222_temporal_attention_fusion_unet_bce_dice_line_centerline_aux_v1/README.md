# ABI-222 temporal-attention fusion U-Net

ABI-222 is a compact temporal-family scout/continuation for GOES ABI Contrail Segmentation. It consumes the trusted `abi_16ch_plus_sza_temporal` input with frame offsets `[-1, 0, 1]` and `frame_selection_policy: temporal_eligible_center`.

The model builds bounded finite ABI+SZA+BTD features for each provider-supplied frame, projects frames with shared weights, computes per-pixel temporal-attention weights relative to the center frame, and fuses the attention-weighted temporal embedding with bounded signed/absolute change features before a compact U-Net/ASPP decoder. It returns `mask_logits` plus trusted `line_logits` and `centerline_logits` auxiliary outputs.

This Candidate is compared primarily to ABI-219/ABI-220 temporal-difference models, ABI-221 ConvGRU temporal-state scout, and the ABI-218 temporal-eligible single-frame control. It is not a promotion candidate against ABI-202.

Contract boundaries: no candidate-owned data loading, temporal lookup, missing-frame fallback, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, training loop, coordinate inputs, Dataset Source identity, downloads, or resource scheduling.
