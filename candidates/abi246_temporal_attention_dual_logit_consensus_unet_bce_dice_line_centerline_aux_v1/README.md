# ABI-246 temporal-attention dual-logit consensus U-Net

ABI-246 is an exploratory family-development continuation of ABI-223 for GOES ABI Contrail Segmentation. It keeps ABI-223's provider-owned `abi_16ch_plus_sza_temporal` input with offsets `[-1, 0, 1]`, `frame_selection_policy: temporal_eligible_center`, temporal-attention encoder/decoder, BCE-Dice loss, random mirroring, source-balanced sampling, and trusted Line/Centerline auxiliary outputs.

The only intended architecture change is the final mask head. Instead of a single 1x1 mask projection, ABI-246 uses a dual-logit consensus head with a conservative local branch, a recall-oriented dilated branch, an internal agreement signal, and a learned final fusion that emits exactly one `mask_logits` tensor. The internal logits are model features only; they are not extra losses, thresholds, postprocessing, or Artifact Filters.

This Candidate requests only the default exploratory budget. Contract boundaries: no candidate-owned data loading, temporal lookup, missing-frame fallback, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, training loop, coordinate inputs, Dataset Source identity, downloads, or resource scheduling.
