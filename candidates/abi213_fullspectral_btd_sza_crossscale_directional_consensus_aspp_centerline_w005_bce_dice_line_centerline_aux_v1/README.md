# ABI-213 full-spectral BTD+SZA cross-scale directional-consensus ASPP centerline-w005

ABI-213 is a controlled family-development continuation of the ABI-201/202 cross-scale directional-consensus ASPP branch for GOES ABI Contrail Segmentation.

## Architecture

The model architecture is copied from ABI-201 unchanged:

- Provider-approved `abi_16ch_plus_sza` input only: GOES ABI channels 1-16 plus Solar Geometry Input.
- Normalized ABI channels, deterministic ABI-channel-derived BTD planes, normalized/cosine SZA features, and a learned 1x1 spectral mixture.
- Signed local/mid-scale detail stem, residual encoder, ASPP bottleneck, full-scale skip fusion, cross-scale directional-consensus bridge, and final line-aware refinement.
- Primary `mask_logits` plus `line_logits` and `centerline_logits` auxiliary outputs.

## Manifest policy

The manifest keeps trusted `bce_dice`, `combined_source_balanced`, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, exploratory max epochs 12, and `constant_lr` scheduling. The only intended policy change from ABI-201/202 is increasing the provider-derived Centerline auxiliary `weighted_bce` weight from 0.02 to 0.05 while keeping the Line auxiliary weight at 0.01.

Candidate code defines model architecture only. It does not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, sampling, augmentation, resource placement, training loops, persistence writes, runtime downloads, or coordinate features. Longitude and latitude source channels are neither requested nor reconstructed.
