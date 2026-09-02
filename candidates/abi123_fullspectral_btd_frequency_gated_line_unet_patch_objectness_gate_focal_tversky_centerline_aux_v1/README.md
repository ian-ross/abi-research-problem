# ABI-123 patch-objectness gated frequency-gated line U-Net

Family-development continuation of ABI-068. This candidate keeps the full-spectral raw+BTD frequency-gated line U-Net with trusted focal-Tversky loss and Centerline Target auxiliary supervision, then replaces the mask head with a neutral-initialized patch objectness gate intended to reduce negative-patch clutter in-contract.

The model receives only provider-approved `abi_16ch` tensors and derives BTD planes only from ABI channels 1-16. It does not own data loading, sampling, augmentation implementation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or lifecycle behavior.
