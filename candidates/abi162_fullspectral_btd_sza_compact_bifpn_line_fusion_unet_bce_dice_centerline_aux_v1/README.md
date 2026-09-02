# ABI-162 compact full-spectral BTD+SZA BiFPN line-fusion U-Net

ABI-162 is a resource-feasibility continuation of the ABI-161 BiFPN line-fusion family scout. ABI-161 trained finitely but exhausted the Harness wall-clock budget near epoch 12, so this candidate preserves the bidirectional pyramid/context-fusion hypothesis with reduced high-resolution compute.

## Architecture

- Provider-approved `abi_16ch_plus_sza` input only.
- Normalized GOES ABI channels 1-16, deterministic thermal BTD planes from approved channels, normalized/cosine Solar Geometry features, and a smaller learned 1x1 spectral mixture.
- Single high-resolution line-evidence stem followed by a compact four-scale residual encoder.
- Learnable positive-weight top-down/bottom-up feature-pyramid fusion with narrower projection channels.
- Reused first-scale encoder features for high-resolution evidence instead of ABI-161's duplicate full-resolution line stem.
- Shorter horizontal/vertical line-context final head.
- Outputs `mask_logits` and provider-derived `centerline_logits`.

## Manifest policy

The manifest selects trusted `bce_dice` primary loss, `weighted_bce` Centerline auxiliary loss at weight 0.02, `combined_source_balanced` traversal, `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max 12 epochs, and `constant_lr` scheduler.

Candidate code does not implement data loading, losses, metrics, Artifact Filters, target derivation, sampling, augmentation, thresholding, resource placement, or Run lifecycle behavior. Longitude and latitude are not inputs.
