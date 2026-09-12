# ABI-233 full-spectral BTD+SZA MoE line-voting U-Net

ABI-233 is a bounded family-development continuation of ABI-231/ABI-232 for GOES ABI Contrail Segmentation. It keeps the provider-owned single-frame `abi_16ch_plus_sza` input and the spectral/Solar Geometry Input gated MoE U-Net, then adds a differentiable multi-orientation line-voting support module before the prediction heads.

The hypothesis is that explicit learned horizontal, vertical, diagonal, and anti-diagonal line accumulation can recover connectivity lost by ABI-232 while preserving its recall and source-balanced overlap. Candidate code remains architecture-only and relies on trusted Harness/provider ownership for data loading, sampling, augmentation, losses, metrics, Artifact Filters, thresholding, training, and Run lifecycle.

This scout uses the default exploratory budget. It does not request the late-improving budget until same-budget resource/trajectory evidence exists for the architecture change.
