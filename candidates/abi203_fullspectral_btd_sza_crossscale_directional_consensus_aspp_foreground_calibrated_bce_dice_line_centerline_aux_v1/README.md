# ABI-203 full-spectral BTD+SZA foreground-calibrated cross-scale directional-consensus ASPP

ABI-203 is an exploratory family-development continuation of ABI-202 for GOES ABI Contrail Segmentation. It keeps the ABI-202 cross-scale directional-consensus ASPP architecture and trusted training/data policy, then replaces the plain mask head with a bounded learned foreground-calibration mask head intended to improve false-positive discipline without moving Artifact Filters, thresholding, or postprocessing into candidate code.

## Architecture

- Provider-approved `abi_16ch_plus_sza` input only: GOES ABI channels 1-16 plus Solar Geometry Input.
- Normalized ABI channels, deterministic ABI-channel-derived thermal BTD planes, normalized/cosine SZA features, and a learned 1x1 spectral mixture.
- Compact base-width-36 residual encoder, ASPP bottleneck, full-scale skip fusion, `CrossScaleDirectionalConsensusBridge`, and line-aware refinement inherited from ABI-202.
- New `ForegroundCalibrationMaskHead`: ordinary linear mask logits plus a zero-initialized bounded learned residual from refined, bridged, local-detail, and smoothed-context features. It predicts no separate target and applies no threshold or filtering.
- Ordinary `line_logits` and `centerline_logits` auxiliary heads.

## Manifest policy

The manifest selects trusted `bce_dice` primary loss, provider-derived Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, exploratory `max_epochs: 12`, and `constant_lr` scheduling.

No `budget_request.yaml` is included. The first ABI-203 Run should use the default exploratory budget.

Candidate code defines model architecture only. It does not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, sampling, augmentation, resource placement, training loops, persistence writes, runtime downloads, or coordinate features. Longitude and latitude source channels are neither requested nor reconstructed.
