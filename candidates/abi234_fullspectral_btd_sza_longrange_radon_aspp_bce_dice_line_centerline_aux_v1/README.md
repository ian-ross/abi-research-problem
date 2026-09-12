# ABI-234 long-range Radon ASPP decoder

Candidate `abi234_fullspectral_btd_sza_longrange_radon_aspp_bce_dice_line_centerline_aux_v1` is a family scout for explicit differentiable long-line accumulation in GOES ABI Contrail Segmentation.

It uses provider-approved `abi_16ch_plus_sza` inputs, approved-channel BTD features, a signed-detail ASPP U-Net scaffold, and trusted Mask/Line/Centerline outputs. The distinguishing module is `DifferentiableRadonLineBridge`, which builds low-resolution horizontal, vertical, diagonal, anti-diagonal, shallow, and steep line-integral support from decoder features using differentiable no-wrap shifts and global row/column means. The support is fused by a bounded learned residual gate inside the model architecture.

The candidate does **not** implement data loading, target construction, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy logic, temporal lookup, coordinates, downloads, training loops, or resource scheduling.

Comparison context: ABI-202 single-frame frontier, ABI-228 temporal local line-accumulation scout, and ABI-233 MoE line-voting continuation.
