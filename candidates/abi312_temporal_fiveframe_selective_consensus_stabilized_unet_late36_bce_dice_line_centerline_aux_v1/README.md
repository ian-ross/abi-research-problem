# ABI-312 temporal five-frame selective consensus stabilized U-Net late36

ABI-312 is a close temporal C4 family-development Candidate for GOES ABI Contrail Segmentation. It starts from ABI-311's finite five-frame persistence/contrast line-state model and adds a selective consensus stabilizer intended to repair MIT-heavy positive-patch undercoverage and typical connected-line continuity without repeating ABI-309's broad low-precision footprint.

The Candidate uses only provider-owned `abi_16ch_plus_sza_temporal` tensors with `temporal_eligible_center` selection and offsets `[-2, -1, 0, 1, 2]`. It never receives longitude/latitude, Dataset Source identity, scene identifiers, file paths, raw samples, or temporal-cache records.

## Architecture

- Per-frame ABI+Solar Geometry Input normalization and ABI-channel-derived thermal BTD features.
- Shared frame projection for all five temporal frames.
- Five-frame attention centered on the zero-offset frame.
- Short-baseline and wide-baseline persistence/contrast features.
- Early C4 orientation-consensus line state, injected into each encoder scale.
- Compact U-Net decoder with high-resolution directional context.
- New selective consensus stabilizer combining decoder detail, projected temporal line state, and orientation-aware support.
- New selective consensus recall head that adds only a small bounded positive residual when mask, Line, Centerline, and temporal-orientation support agree.

## Contract boundary

Allowed manifest selections are: `mask_logits`, `bce_dice`, `adamw`, `constant_lr`, `combined_source_balanced`, `random_mirroring`, Line and Centerline auxiliary targets, batch size 2, and five-frame provider temporal input. Candidate code defines architecture only and does not implement data loading, temporal lookup, missing-frame repair, augmentation, sampling, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, downloads, training loops, resource placement, or lifecycle behavior.

## Budget

The manifest declares the exploratory 12-epoch ceiling. `budget_request.yaml` requests the Harness-owned 36-epoch `late_improving` budget with fallback to exploratory if denied, justified by ABI-311's epoch-27 best checkpoint and the late-improving behavior of recent temporal C4 parents.
