# ABI-313 temporal five-frame continuity-protected calibration late36

ABI-313 is a mechanism-changing temporal C4 family-development Candidate for GOES ABI Contrail Segmentation. It follows ABI-311/312: ABI-311 showed useful five-frame persistence/contrast balance, while ABI-312 showed that a blunt positive-only selective-consensus residual raised recall at the cost of filtered Dice and connected-line continuity.

The Candidate uses only provider-owned `abi_16ch_plus_sza_temporal` tensors with `temporal_eligible_center` selection and offsets `[-2, -1, 0, 1, 2]`. It never receives longitude/latitude, Dataset Source identity, scene identifiers, file paths, raw samples, or temporal-cache records.

## Architecture

- ABI-311 five-frame temporal feature builder with per-frame ABI normalization, ABI-channel-derived BTD planes, and Solar Geometry Input features.
- Five-frame persistence/contrast stem with early C4 orientation-consensus line state.
- Compact U-Net encoder/decoder with multi-scale line-state injection and high-resolution directional context.
- New continuity-protected calibration head: a signed, bounded logit correction gated by decoder detail, early temporal C4 line-state support, and learned Line/Centerline auxiliary evidence.
- The calibration head can learn positive or negative corrections; it is intended to avoid ABI-312's broad positive residual while preserving ABI-311's connected-line evidence.

## Contract boundary

Allowed manifest selections are `mask_logits`, `bce_dice`, `adamw`, `constant_lr`, `combined_source_balanced`, `random_mirroring`, Line and Centerline auxiliary targets, batch size 2, and five-frame provider temporal input. Candidate code defines architecture only and does not implement data loading, temporal lookup, missing-frame repair, augmentation, sampling, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, downloads, training loops, resource placement, or lifecycle behavior.

## Budget

The manifest declares the exploratory 12-epoch ceiling. `budget_request.yaml` requests the Harness-owned 36-epoch `late_improving` budget with fallback to exploratory if denied, justified by ABI-311/312 late selected checkpoints and the unchanged profiled five-frame temporal C4 resource envelope.
