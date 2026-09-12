# ABI-236 full-spectral BTD+SZA recall-bypass Radon ASPP decoder

ABI-236 is a controlled Radon-family continuation after ABI-235. It keeps the provider-owned `abi_16ch_plus_sza` input, ABI-channel-derived BTD/Solar Geometry Input front end, signed-detail ASPP U-Net scaffold, full-scale skip fusion, trusted BCE-Dice loss, and Line/Centerline auxiliary outputs. The architectural change weakens the long-range differentiable Radon residual and adds a learned high-resolution detail bypass so faint local contrail evidence can survive alongside line-integral support.

Candidate code remains architecture-only. It does not implement data loading, sampling, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, coordinate inputs, temporal cache access, downloads, training loops, or resource scheduling.
