# ABI-247 five-frame center-anchored persistence-attention U-Net

ABI-247 is an exploratory temporal Candidate for GOES ABI Contrail Segmentation. It broadens from ABI-223's successful three-frame temporal-attention U-Net to the provider-owned five-frame window `[-2, -1, 0, 1, 2]`, while explicitly anchoring fusion to the zero-offset target frame.

The architecture keeps ABI-223's finite ABI+SZA+BTD per-frame feature builder, compact U-Net encoder/ASPP/decoder, simple `mask_logits` head, and trusted Line/Centerline auxiliary outputs. The new stem projects all five frames with shared weights, computes center-referenced temporal attention with a small center-bias prior, derives near/far mean and temporal-difference features, and gates the attended features back toward the center-frame embedding before decoding.

This Candidate requests only the default exploratory budget. Contract boundaries: no candidate-owned data loading, temporal lookup, cache reads, missing-frame fallback, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, training loop, coordinate inputs, Dataset Source identity, downloads, or resource scheduling.
