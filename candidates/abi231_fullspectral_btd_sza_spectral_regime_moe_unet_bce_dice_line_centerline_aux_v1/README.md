# ABI-231 full-spectral BTD+SZA spectral-regime MoE U-Net

ABI-231 is a bounded family scout for GOES ABI Contrail Segmentation. It broadens away from the recent temporal/window-attention line by testing a compact single-frame spectral/Solar Geometry Input-regime gated mixture-of-experts U-Net.

The model consumes only provider-approved `abi_16ch_plus_sza` tensors. It normalizes ABI channels, derives brightness-temperature-difference planes from approved ABI channels, adds scaled/cosine Solar Geometry Input features, and learns soft global/per-pixel gates over three convolutional experts. The gated features feed a compact U-Net with ASPP context, a high-resolution signed-detail bridge, and trusted Mask/Line/Centerline output heads.

Candidate code does not load data, access temporal caches, use longitude/latitude, use Dataset Source identity, derive targets, implement losses/metrics/Artifact Filters/thresholding/postprocessing/augmentation/sampling/training loops, download weights, probe arbitrary filesystems, or schedule resources.
