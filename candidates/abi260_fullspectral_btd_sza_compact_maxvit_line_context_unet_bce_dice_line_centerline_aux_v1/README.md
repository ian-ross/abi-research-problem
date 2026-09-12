# ABI-260 compact MaxViT line-context U-Net

ABI-260 is a bounded family scout for GOES ABI Contrail Segmentation. It tests a compact MaxViT-style encoder-decoder that alternates local window attention with sparse global grid attention, while retaining full-spectral ABI+Solar Geometry Input features, approved-channel BTD planes, and a lightweight line-context decoder.

The Candidate consumes only provider-owned `abi_16ch_plus_sza` inputs and emits `mask_logits`, `line_logits`, and `centerline_logits`. It selects trusted BCE-Dice loss, trusted Line/Centerline auxiliary targets, source-balanced sampling, random mirroring, batch size 4, constant learning rate, and the default 12-epoch exploratory budget.

This Candidate does not implement data loading, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.
