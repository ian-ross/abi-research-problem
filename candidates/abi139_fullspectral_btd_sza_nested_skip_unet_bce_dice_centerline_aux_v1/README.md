# ABI-139 full-spectral BTD+SZA nested-skip U-Net BCE-Dice continuation

Family-development Candidate for GOES ABI Contrail Segmentation. This candidate revisits the resource-feasible ABI-079 nested-skip U-Net after ABI-130 showed that provider-approved Solar Geometry Input plus trusted BCE-Dice can move a conservative ASPP/detail branch toward a useful fixed-threshold operating point. The controlled goal is to test whether the same calibration axis can correct ABI-079's permissive, low-precision nested-skip profile without adding candidate-owned thresholding or postprocessing.

The model uses provider-approved `abi_16ch_plus_sza` input, normalized ABI channels 1-16, thermal brightness-temperature-difference planes derived only from approved ABI channels, normalized SZA/`cos(SZA)` features, and a learned 1x1 spectral/SZA mixer. It emits primary `mask_logits` and a provider-derived `centerline_logits` auxiliary output. It receives no longitude, latitude, Dataset Source identity, or reconstructed coordinate inputs.

All data loading, split logic, sampling, augmentation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned.
