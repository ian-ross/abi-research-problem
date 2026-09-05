# ABI-201 full-spectral BTD+SZA cross-scale directional-consensus ASPP

ABI-201 is an exploratory family-development/broadened line-continuity Candidate Experiment for GOES ABI Contrail Segmentation. It moves away from the recent ridge-detail local bridge edits by testing whether high-resolution decoder features should pass through a cross-scale directional-consensus feature bridge before final mask prediction.

## Architecture

- Provider-approved `abi_16ch_plus_sza` input only: GOES ABI channels 1-16 plus Solar Geometry Input.
- Normalized ABI channels, deterministic ABI-channel-derived BTD planes, normalized/cosine SZA features, and a learned 1x1 spectral mixture.
- Compact base-width-36 residual encoder, ASPP bottleneck, and full-scale skip fusion adapted from the finite signed-detail ASPP lineage to keep the unprofiled bridge within the exploratory resource envelope.
- New architecture-internal `CrossScaleDirectionalConsensusBridge` that fuses decoder, signed-detail, stem, and full-scale context features with horizontal, vertical, diagonal, and broad context views. The bridge uses a zero-initialized bounded residual so training starts near the parent decoder, and it predicts no target and applies no thresholding or filtering.
- Final line-aware refinement followed by `mask_logits`, `line_logits`, and `centerline_logits` heads.

## Manifest policy

The manifest selects trusted `bce_dice` primary loss, provider-derived Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, 12 exploratory epochs, and `constant_lr` scheduling.

Candidate code defines model architecture only. It does not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, sampling, augmentation, resource placement, training loops, persistence writes, runtime downloads, or coordinate features. Longitude and latitude source channels are neither requested nor reconstructed.
