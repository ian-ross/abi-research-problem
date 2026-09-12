# ABI-235 full-spectral BTD+SZA long-range Radon ASPP late36

ABI-235 is a late-improving family-development continuation of ABI-234 for GOES ABI Contrail Segmentation. It preserves the ABI-234 single-frame full-spectral BTD+Solar Geometry Input ASPP/detail decoder with low-resolution differentiable Radon-style long-line accumulation and requests the approved `late_improving` budget because ABI-234 completed finite, noncollapsed, source-informative training and selected its best checkpoint at epoch 12.

The model consumes only provider-approved `abi_16ch_plus_sza` tensors. It normalizes ABI channels, derives brightness-temperature-difference planes from approved ABI channels, adds scaled/cosine Solar Geometry Input features, applies a learned 1x1 mixer, and fuses compact U-Net/detail features with differentiable oriented long-line support before trusted Mask/Line/Centerline output heads.

Candidate code does not load data, access temporal caches, use longitude/latitude, use Dataset Source identity, derive targets, implement losses/metrics/Artifact Filters/thresholding/postprocessing/augmentation/sampling/training loops, download weights, probe arbitrary filesystems, or schedule resources.
