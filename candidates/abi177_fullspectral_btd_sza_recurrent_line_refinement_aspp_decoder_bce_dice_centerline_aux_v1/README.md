# ABI-177 full-spectral BTD+SZA recurrent line-refinement ASPP decoder BCE-Dice centerline auxiliary v1

ABI-177 is a family-development continuation that broadens away from recent signed-detail/full-scale fusion patches. It preserves provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal brightness-temperature-difference features derived only from approved ABI channels, normalized Solar Geometry Input features, trusted BCE-Dice primary loss, and provider-derived Centerline Target auxiliary supervision.

The controlled architecture change is a separate thermal-anchor support branch plus a recurrent line-refinement head. The thermal anchor uses only normalized thermal ABI channels, approved-channel BTD planes, and Solar Geometry features to produce a compact support map. The final decoder then refines features for three shared recurrent steps using additive horizontal, vertical, diagonal/local, broad-context, and thermal-anchor evidence. This tests whether iterative non-thresholded line propagation can recover ABI-068/130/154/173-like connectivity and recall without adding another suppressive signed-detail gate.

Contract boundaries:

- Input mode: `abi_16ch_plus_sza`; longitude/latitude and reconstructed coordinates are not used.
- Outputs: primary `mask_logits` and provider-derived `centerline_logits` auxiliary output.
- Trusted policies: `combined_source_balanced`, `random_mirroring`, `bce_dice`, `weighted_bce` centerline auxiliary at weight 0.02, AdamW, learning rate 0.0003, batch size 4, 12 epochs, `constant_lr`.
- Candidate code defines architecture only. It does not implement data loading, target derivation, losses, metrics, augmentation, sampling, thresholding, Artifact Filters, postprocessing, scheduling, GPU placement, training loops, external persistence, runtime downloads, or pretrained weights.
