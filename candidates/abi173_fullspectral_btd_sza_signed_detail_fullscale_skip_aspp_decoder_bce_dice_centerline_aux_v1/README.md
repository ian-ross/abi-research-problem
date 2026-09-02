# ABI-173 full-spectral BTD+SZA signed-detail full-scale skip ASPP decoder BCE-Dice centerline auxiliary v1

ABI-173 is a controlled family-development continuation of ABI-154. It preserves the SZA-aware full-spectral BTD full-scale skip ASPP/detail decoder, trusted BCE-Dice primary loss, and provider-derived Centerline Target auxiliary supervision, but replaces the raw/signed-unaware detail stems with signed local and mid-scale detail streams.

The hypothesis is that separating positive and negative high-frequency anomalies before the encoder and high-resolution detail path may recover missed thin contrails without the broad positive-area expansion seen in focal-Tversky and coarse-recall-bridge variants. The comparison target is ABI-154 Run `run_20260901_071026_32d3ec`; secondary references are ABI-130, ABI-156, ABI-168, ABI-171, ABI-172, and ABI-068.

Contract boundaries:

- Input mode: `abi_16ch_plus_sza`; longitude/latitude and reconstructed coordinates are not used.
- Outputs: primary `mask_logits` and provider-derived `centerline_logits` auxiliary output.
- Trusted policies: `combined_source_balanced`, `random_mirroring`, `bce_dice`, `weighted_bce` centerline auxiliary at weight 0.02, AdamW, learning rate 0.0003, batch size 4, 12 epochs, `constant_lr`.
- Candidate code defines architecture only. It does not implement data loading, target derivation, losses, metrics, augmentation, sampling, thresholding, Artifact Filters, postprocessing, scheduling, GPU placement, training loops, external persistence, runtime downloads, or pretrained weights.
