# ABI-311 temporal five-frame C4 persistence-contrast line-state late36

ABI-311 is a mechanism-changing temporal C4 family-development Candidate for GOES ABI Contrail Segmentation. It tests whether the allowlisted five-frame temporal window `[-2, -1, 0, 1, 2]` can provide more selective persistence/contrast evidence before C4 line-state fusion, avoiding another late line-support head tweak after ABI-309/310.

The Candidate uses only provider-owned `abi_16ch_plus_sza_temporal` tensors with `temporal_eligible_center` selection. It never receives longitude/latitude, Dataset Source identity, scene identifiers, file paths, raw samples, or temporal-cache records.

## Architecture

- Per-frame ABI+Solar Geometry Input normalization and ABI-channel-derived thermal BTD features.
- Shared frame projection for all five temporal frames.
- Five-frame attention centered on the zero-offset frame.
- Short-baseline and wide-baseline persistence/contrast features: center-minus-inner-neighbors, center-minus-outer-neighbors, inner temporal difference, and outer temporal difference.
- Early C4 orientation-consensus line state, injected into each encoder scale.
- Compact U-Net decoder with high-resolution directional context.
- ABI-306-style dual-evidence mask/Line/Centerline calibration head.

## Contract boundary

Allowed manifest selections are: `mask_logits`, `bce_dice`, `adamw`, `constant_lr`, `combined_source_balanced`, `random_mirroring`, Line and Centerline auxiliary targets, batch size 2, and five-frame provider temporal input. Candidate code defines architecture only and does not implement data loading, temporal lookup, missing-frame repair, augmentation, sampling, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, downloads, training loops, resource placement, or lifecycle behavior.

## Budget

The manifest declares the exploratory 12-epoch ceiling. `budget_request.yaml` requests the Harness-owned 36-epoch `late_improving` budget with fallback to exploratory if denied, justified by late-improving temporal C4 parents and resource-safe five-frame scouts.
