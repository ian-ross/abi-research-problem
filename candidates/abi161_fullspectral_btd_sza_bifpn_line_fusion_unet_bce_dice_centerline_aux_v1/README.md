# ABI-161 full-spectral BTD+SZA BiFPN line-fusion U-Net

ABI-161 is a family-scout Candidate Experiment for GOES ABI Contrail Segmentation. It broadens away from the recent ASPP/detail/full-scale-skip refinements by using bidirectional feature-pyramid fusion over high-resolution line evidence and coarser cloud context.

## Architecture

- Provider-approved `abi_16ch_plus_sza` input only.
- Normalized GOES ABI channels 1-16, deterministic thermal BTD planes from approved channels, normalized/cosine Solar Geometry features, and a learned 1x1 spectral mixture.
- Compact residual encoder with four scales.
- Learnable positive-weight BiFPN top-down and bottom-up fusion instead of an ASPP bottleneck.
- High-resolution line-evidence stem plus final horizontal/vertical line-fusion feature head.
- Outputs `mask_logits` and provider-derived `centerline_logits`.

## Manifest policy

The manifest selects trusted `bce_dice` primary loss, `weighted_bce` Centerline auxiliary loss at weight 0.02, `combined_source_balanced` traversal, `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max 12 epochs, and `constant_lr` scheduler.

Candidate code does not implement data loading, losses, metrics, Artifact Filters, target derivation, sampling, augmentation, thresholding, resource placement, or Run lifecycle behavior. Longitude and latitude are not inputs.
