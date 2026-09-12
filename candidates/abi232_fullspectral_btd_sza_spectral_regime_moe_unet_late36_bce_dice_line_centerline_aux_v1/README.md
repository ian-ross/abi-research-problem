# ABI-232 full-spectral BTD+SZA spectral-regime MoE U-Net late36

ABI-232 is a late-improving family-development continuation of ABI-231 for GOES ABI Contrail Segmentation. It preserves the ABI-231 compact single-frame spectral/Solar Geometry Input-regime gated mixture-of-experts U-Net and requests the approved `late_improving` budget because ABI-231 completed finite, noncollapsed, source-informative training and selected its best checkpoint at epoch 12.

The model consumes only provider-approved `abi_16ch_plus_sza` tensors. It normalizes ABI channels, derives brightness-temperature-difference planes from approved ABI channels, adds scaled/cosine Solar Geometry Input features, and learns soft global/per-pixel gates over three convolutional experts. The gated features feed a compact U-Net with ASPP context, a high-resolution signed-detail bridge, and trusted Mask/Line/Centerline output heads.

Candidate code does not load data, access temporal caches, use longitude/latitude, use Dataset Source identity, derive targets, implement losses/metrics/Artifact Filters/thresholding/postprocessing/augmentation/sampling/training loops, download weights, probe arbitrary filesystems, or schedule resources.
