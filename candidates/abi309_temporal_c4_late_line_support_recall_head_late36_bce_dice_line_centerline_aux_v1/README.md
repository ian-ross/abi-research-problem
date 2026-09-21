# ABI-309 temporal C4 late line-support recall head late36

This Candidate Experiment is a mechanism-changing family-development continuation of the temporal C4 line-state branch for GOES ABI Contrail Segmentation.

## Summary

ABI-306 established a compact high-precision temporal C4 operating point but left fixed-threshold recall and connected-line continuity headroom. ABI-308 showed that stricter center-detail agreement can improve connectivity, but it over-suppressed aggregate/source-balanced evidence. ABI-309 removes the center-detail bridge and instead feeds the already computed temporal C4 line state into the final learned logit calibration head.

The model consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` frame selection. It predicts `mask_logits` plus trusted auxiliary `line_logits` and `centerline_logits`.

## Architecture

The architecture starts from ABI-306:

- finite ABI/Solar Geometry/BTD feature construction for each provider-supplied temporal frame;
- temporal attention fusion and C4 orientation-consensus line-state stem;
- compact U-Net encoder, ASPP bottleneck, decoder, and multi-scale line-state injection;
- high-resolution directional context before the output head.

The changed mechanism is `LateLineSupportRecallHead`:

- it keeps base mask/Line/Centerline logits from shared decoder features;
- it resizes the temporal C4 line state to full resolution and projects it into head channels;
- it learns a support feature from decoder features, line-state features, and their absolute difference;
- it adds a bounded learned support residual to the mask logits only through learned mask/Line/Centerline/support evidence gates.

This is model architecture only. It does not implement data loading, temporal lookup, missing-frame repair, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, training loops, prediction retention, or lifecycle behavior.

## Manifest policy

- Input mode: `abi_16ch_plus_sza_temporal`
- Temporal frame offsets: `[-1, 0, 1]`
- Frame selection: `temporal_eligible_center`
- Sampling: trusted `combined_source_balanced`
- Augmentation: trusted `random_mirroring`
- Loss: trusted `bce_dice`
- Optimizer/scheduler: AdamW with `constant_lr`
- Auxiliary targets: trusted Line and Centerline with weighted BCE
- Batch size: 2

A `late_improving` budget request is included because the direct parent Runs were finite, source-informative, resource-safe late-budget temporal C4 Runs whose useful checkpoints occurred after the exploratory ceiling.
