# ABI-214 compact full-spectral BTD+SZA thin-line continuity ASPP

ABI-214 is a bounded exploratory continuation after ABI-212. It keeps the resource-safe compact full-spectral BTD+SZA ASPP decoder and replaces broad coarse-support fusion with a lightweight `ThinLineContinuityBridge`.

## Architecture

- Provider-approved `abi_16ch_plus_sza` input only: GOES ABI channels 1-16 plus Solar Geometry Input.
- Normalized ABI channels, deterministic ABI-channel-derived thermal BTD planes, normalized/cosine SZA features, and learned 1x1 spectral mixture.
- Compact base-width-28 residual encoder, ASPP bottleneck, full-scale skip fusion, signed-detail stems, and line-aware refinement.
- `ThinLineContinuityBridge` uses signed-detail features plus horizontal, vertical, and diagonal orientation context as a zero-initialized bounded residual. It does not predict support masks, threshold outputs, apply morphology, or implement Artifact Filters.
- Outputs are `mask_logits`, `line_logits`, and `centerline_logits` for provider-owned primary and auxiliary losses.

## Manifest policy

The manifest selects trusted `bce_dice` primary loss, provider-derived Line and Centerline auxiliary targets with trusted `weighted_bce` weights 0.01 and 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, exploratory `max_epochs: 12`, and `constant_lr` scheduling.

Candidate code defines model architecture only. It does not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, sampling, augmentation, resource placement, training loops, persistence writes, runtime downloads, or coordinate features. Longitude and latitude source channels are neither requested nor reconstructed.
