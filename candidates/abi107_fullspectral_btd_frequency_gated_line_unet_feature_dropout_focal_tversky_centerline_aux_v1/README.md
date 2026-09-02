# ABI-107 feature-dropout regularized frequency-gated line U-Net

This Candidate is a family-development continuation of ABI-068. It keeps the full-spectral ABI plus deterministic thermal BTD frequency-gated line U-Net, trusted `focal_tversky` primary loss, trusted Centerline Target auxiliary head, combined source-balanced traversal, and random mirroring. The only architecture change is low-probability `Dropout2d` on intermediate feature tensors to test whether reducing feature co-adaptation can improve precision/connectivity or positive-area discipline without moving thresholding, Artifact Filters, losses, targets, sampling, or augmentation into Candidate code.

The model uses only provider-approved `abi_16ch` inputs and emits `mask_logits` plus `centerline_logits`.
