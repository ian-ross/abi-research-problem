# ABI-174 full-spectral BTD+SZA signed-detail line-consensus full-scale skip ASPP decoder BCE-Dice centerline auxiliary v1

ABI-174 is a controlled family-development continuation of ABI-173. It preserves ABI-173's provider-approved `abi_16ch_plus_sza` input, normalized ABI/BTD/SZA front end, signed local and mid-scale detail streams, compact residual encoder, ASPP context, full-scale skip fusion, trusted BCE-Dice primary loss, and provider-derived Centerline Target auxiliary supervision.

The controlled architecture change is a conservative line-consensus calibration block after the existing line-aware refinement. The block learns short and wide horizontal/vertical line-context features, fuses them into a consensus feature, and applies a gently initialized feature-space support gate before the final mask and centerline heads. This is intended to keep ABI-173's signed-detail recall gains while reducing negative-patch clutter and recovering some of ABI-154's connectivity/positive-area discipline.

Contract boundaries:

- Input mode: `abi_16ch_plus_sza`; longitude/latitude and reconstructed coordinates are not used.
- Outputs: primary `mask_logits` and provider-derived `centerline_logits` auxiliary output.
- Trusted policies: `combined_source_balanced`, `random_mirroring`, `bce_dice`, `weighted_bce` centerline auxiliary at weight 0.02, AdamW, learning rate 0.0003, batch size 4, 12 epochs, `constant_lr`.
- Candidate code defines architecture only. It does not implement data loading, target derivation, losses, metrics, augmentation, sampling, thresholding, Artifact Filters, postprocessing, scheduling, GPU placement, training loops, external persistence, runtime downloads, or pretrained weights.
