# ABI-206 full-spectral BTD+SZA cross-scale directional-consensus ASPP boundary auxiliary probe

ABI-206 is a controlled family-development continuation of the ABI-201/202 cross-scale directional-consensus ASPP branch for GOES ABI Contrail Segmentation. It keeps ABI-202's approved input mode, architecture, BCE-Dice loss, source-balanced sampling policy, and Line plus Centerline auxiliary supervision, and adds one low-weight trusted Boundary Target auxiliary head.

## Architecture

- Provider-approved `abi_16ch_plus_sza` input only: GOES ABI channels 1-16 plus Solar Geometry Input.
- Normalized ABI channels, deterministic ABI-channel-derived thermal BTD planes, normalized/cosine SZA features, and a learned 1x1 spectral mixture.
- Compact base-width-36 residual encoder, ASPP bottleneck, full-scale skip fusion, and the ABI-201/202 `CrossScaleDirectionalConsensusBridge`.
- Final line-aware refinement followed by `mask_logits`, `line_logits`, `boundary_logits`, and `centerline_logits` heads.

## Manifest policy

The manifest selects trusted `bce_dice` primary loss, provider-derived Line, Boundary, and Centerline auxiliary targets with trusted `weighted_bce` weights 0.01, 0.005, and 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, exploratory `max_epochs: 12`, and `constant_lr` scheduling. No late-improving budget is requested.

Candidate code defines model architecture only. It does not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, sampling, augmentation, resource placement, training loops, persistence writes, runtime downloads, or coordinate features. Longitude and latitude source channels are neither requested nor reconstructed.
