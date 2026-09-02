# ABI-143 Full-Spectral BTD+SZA Soft Ridge-Gate U-Net BCE-Dice Centerline Auxiliary v1

ABI-143 is a bounded family-development continuation of ABI-142. It keeps provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features derived only from ABI channels 1-16, trusted `bce_dice` loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, and constant learning rate.

The architecture remains a compact U-Net with multiscale ridge-aware stem features and a final ridge refinement path. The controlled change from ABI-142 is the final feature-space ridge gate: the gate is now neutral-initialized and conservatively bounded to a 0.85-1.15 multiplier instead of the broader 0.65-1.35 range. This tests whether ABI-142's near-reference SZA+BCE-Dice behavior can retain ridge/detail evidence while reducing over-aggressive feature suppression or amplification.

Outputs:

- `mask_logits`: primary Contrail Mask logits.
- `centerline_logits`: provider-derived Centerline Target auxiliary output, `weighted_bce` weight 0.02.

The experiment tests a specific in-contract calibration mechanism for the ridge-attention family. It does not implement data loading, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, network access, or resource scheduling.
