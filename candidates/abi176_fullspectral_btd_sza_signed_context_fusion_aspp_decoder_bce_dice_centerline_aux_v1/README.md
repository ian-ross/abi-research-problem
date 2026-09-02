# ABI-176 full-spectral BTD+SZA signed context-fusion ASPP decoder BCE-Dice centerline auxiliary v1

ABI-176 is a controlled family-development continuation of ABI-173. It preserves the provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD features derived only from approved ABI channels, normalized/cosine Solar Geometry Input features, signed positive/negative detail stems, compact residual encoder, ASPP context, full-scale skip aggregation, line-aware final refinement, trusted BCE-Dice primary loss, and provider-derived Centerline Target auxiliary supervision.

The controlled architecture change is `SignedContextFusion`: decoder, signed-detail, stem, and full-scale features are projected to a shared width; decoder/stem/full-scale/broad context compute a neutral feature-space gate; the signed-detail path is bounded to a 0.85-1.15 calibration range; horizontal and vertical detail-context branches are fused before the existing line-aware refinement. The hypothesis is that this earlier context-balanced fusion may preserve ABI-173's signed-detail recall while improving precision, connectivity, or predicted-positive discipline.

Contract boundaries:

- Input mode: `abi_16ch_plus_sza`; longitude/latitude and reconstructed coordinates are not used.
- Outputs: primary `mask_logits` and provider-derived `centerline_logits` auxiliary output.
- Trusted policies: `combined_source_balanced`, `random_mirroring`, `bce_dice`, `weighted_bce` centerline auxiliary at weight 0.02, AdamW, learning rate 0.0003, batch size 4, 12 epochs, `constant_lr`.
- Candidate code defines architecture only. It does not implement data loading, target derivation, losses, metrics, augmentation, sampling, thresholding, Artifact Filters, postprocessing, scheduling, GPU placement, training loops, external persistence, runtime downloads, or pretrained weights.
