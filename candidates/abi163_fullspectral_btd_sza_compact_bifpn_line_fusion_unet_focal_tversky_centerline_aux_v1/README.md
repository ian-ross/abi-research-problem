# ABI-163 compact full-spectral BTD+SZA BiFPN line-fusion U-Net with focal-Tversky

ABI-163 is a controlled family-development continuation of ABI-162. It keeps the compact resource-feasible BiFPN line-fusion architecture and changes only the trusted primary loss from `bce_dice` to `focal_tversky` to test recall recovery.

## Architecture

- Provider-approved `abi_16ch_plus_sza` input only.
- Normalized GOES ABI channels 1-16, deterministic thermal BTD planes from approved channels, normalized/cosine Solar Geometry features, and a small learned 1x1 spectral mixture.
- Single high-resolution line-evidence stem followed by a compact four-scale residual encoder.
- Learnable positive-weight top-down/bottom-up feature-pyramid fusion with narrow projection channels.
- Reused first-scale encoder features for high-resolution evidence.
- Compact horizontal/vertical line-context final head.
- Outputs `mask_logits` and provider-derived `centerline_logits`.

## Manifest policy

The manifest selects trusted `focal_tversky` primary loss, `weighted_bce` Centerline auxiliary loss at weight 0.02, `combined_source_balanced` traversal, `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max 12 epochs, and `constant_lr` scheduler.

Candidate code does not implement data loading, losses, metrics, Artifact Filters, target derivation, sampling, augmentation, thresholding, resource placement, or Run lifecycle behavior. Longitude and latitude are not inputs.
