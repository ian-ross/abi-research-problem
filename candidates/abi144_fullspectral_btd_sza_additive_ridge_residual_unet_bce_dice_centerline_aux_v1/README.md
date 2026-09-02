# ABI-144 Full-Spectral BTD+SZA Additive Ridge-Residual U-Net BCE-Dice Centerline Auxiliary v1

ABI-144 is a bounded family-development continuation of ABI-143/ABI-142. It keeps provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features derived only from ABI channels 1-16, trusted `bce_dice` loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, and constant learning rate.

The architecture remains a compact U-Net with multiscale ridge-aware stem features and final ridge refinement. The controlled change from ABI-143 is to remove the multiplicative ridge gate and replace it with a neutral-initialized additive ridge residual path: the residual 1x1 projection starts at zero and is bounded by `0.1 * tanh(...)`, so the refinement is identity at initialization and cannot directly suppress decoded features. This tests whether ridge evidence can recover ABI-143's MIT-recall benefit while preserving more of ABI-142/ABI-130 connectivity and precision.

Outputs:

- `mask_logits`: primary Contrail Mask logits.
- `centerline_logits`: provider-derived Centerline Target auxiliary output, `weighted_bce` weight 0.02.

The experiment does not implement data loading, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, network access, or resource scheduling.
