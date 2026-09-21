# ABI-316 temporal five-frame decoder line-continuity bridge late36

ABI-316 is a mechanism-changing temporal C4 family-development Candidate for GOES ABI Contrail Segmentation. It keeps ABI-311's successful five-frame persistence/contrast temporal stem and tests whether multi-scale decoder-stage line-continuity bridges can repair the remaining MIT/positive-patch undercoverage and typical connected-line weakness without repeating ABI-312/313 late-logit calibration regressions.

The Candidate uses only provider-owned `abi_16ch_plus_sza_temporal` tensors with `temporal_eligible_center` selection and offsets `[-2, -1, 0, 1, 2]`. It never receives longitude/latitude, Dataset Source identity, scene identifiers, file paths, raw samples, or temporal-cache records.

## Architecture

- Per-frame ABI+Solar Geometry Input normalization and ABI-channel-derived thermal BTD features.
- Shared frame projection for all five temporal frames.
- Five-frame attention centered on the zero-offset frame.
- Short-baseline and wide-baseline persistence/contrast features.
- Early C4 orientation-consensus line state.
- Compact U-Net encoder/decoder with line-state injection into encoder scales.
- New decoder-stage line-continuity bridges that resize the early temporal C4 line state into each decoder scale, combine it with decoder detail, and apply gated orientation-aware refinement before logits.
- ABI-311-style dual-evidence mask/Line/Centerline output head.

## Contract boundary

Allowed manifest selections are: `mask_logits`, `bce_dice`, `adamw`, `constant_lr`, `combined_source_balanced`, `random_mirroring`, Line and Centerline auxiliary targets, batch size 2, and five-frame provider temporal input. Candidate code defines architecture only and does not implement data loading, temporal lookup, missing-frame repair, augmentation, sampling, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, downloads, training loops, resource placement, or lifecycle behavior.

## Budget

The manifest declares the exploratory 12-epoch ceiling. `budget_request.yaml` requests the Harness-owned 36-epoch `late_improving` budget with fallback to exploratory if denied, justified by ABI-311's late best checkpoint and the late-forming behavior of ABI-312/313 close continuations under the same five-frame resource envelope.
