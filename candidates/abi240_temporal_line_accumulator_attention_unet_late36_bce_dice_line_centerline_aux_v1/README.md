# ABI-240 temporal line-accumulator attention U-Net late36

ABI-240 is a late-improving close-continuation of ABI-239. It keeps the same temporal/Radon-hybrid architecture, provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]`, `temporal_eligible_center` frame selection, source-balanced sampling, trusted random mirroring, BCE-Dice loss, batch size 2, and trusted Line/Centerline auxiliary targets.

The hypothesis is that ABI-239's final-epoch exploratory improvement can continue under the approved `late_improving` budget and determine whether pre-encoder differentiable line accumulation can approach the ABI-223 temporal frontier without losing source-informative recall.

Candidate code remains architecture-only and does not implement data loading, temporal lookup, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, coordinates, Dataset Source identity, or resource scheduling.
