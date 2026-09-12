# ABI-239 temporal line-accumulator attention U-Net

ABI-239 is a sequential exploratory family-development continuation of the ABI-223 temporal-attention branch. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and adds a differentiable low-resolution multi-orientation line accumulator before the encoder. The hypothesis is that accumulating long, weak line evidence before downsampling can recover thin-line connectivity without repeating ABI-238 post-decoder directional bridge that traded away recall/connectivity.

The Candidate uses trusted BCE-Dice loss, random mirroring, source-balanced sampling, and trusted Line/Centerline auxiliary targets. Candidate code remains architecture-only and does not implement data loading, temporal lookup, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, coordinates, or resource scheduling.
