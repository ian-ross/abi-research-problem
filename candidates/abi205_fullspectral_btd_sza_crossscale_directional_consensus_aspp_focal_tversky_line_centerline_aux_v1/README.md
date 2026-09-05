# ABI-205 full-spectral BTD+SZA cross-scale directional-consensus ASPP focal-Tversky probe

ABI-205 is a controlled family-development continuation of ABI-201/202 for GOES ABI Contrail Segmentation. It keeps the same architecture as the strong cross-scale directional-consensus ASPP branch and changes only the trusted primary loss from `bce_dice` to allowlisted `focal_tversky`.

## Architecture

- Provider-approved `abi_16ch_plus_sza` input only: GOES ABI channels 1-16 plus Solar Geometry Input.
- Normalized ABI channels, deterministic ABI-channel-derived thermal BTD planes, normalized/cosine SZA features, and a learned 1x1 spectral mixture.
- Compact base-width-36 residual encoder, ASPP bottleneck, full-scale skip fusion, and architecture-internal `CrossScaleDirectionalConsensusBridge` copied from ABI-201/202.
- Final line-aware refinement followed by `mask_logits`, `line_logits`, and `centerline_logits` heads.

## Manifest policy

The manifest selects trusted `focal_tversky` primary loss, provider-derived Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, 12 exploratory epochs, and `constant_lr` scheduling.

Candidate code defines model architecture only. It does not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, sampling, augmentation, resource placement, training loops, persistence writes, runtime downloads, or coordinate features. Longitude and latitude source channels are neither requested nor reconstructed.
