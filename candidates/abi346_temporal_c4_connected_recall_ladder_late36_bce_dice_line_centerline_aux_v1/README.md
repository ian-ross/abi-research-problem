# ABI-346 temporal C4 connected-recall ladder late36 U-Net

ABI-346 is a close, mechanism-changing continuation of ABI-306 for GOES ABI Contrail Segmentation. It keeps ABI-306's provider-owned three-frame temporal C4 line-state U-Net backbone and replaces the final dual-evidence residual head with a connected-recall ladder head.

The scientific target is ABI-306's remaining under-recall tail. ABI-306 became a compact high-precision temporal C4 comparator, but its temporal-eligible diagnostic showed low-threshold recall reserve that cannot be used through Candidate-owned thresholding. ABI-346 tests whether a bounded architecture-level head can raise connected true-contrail evidence to the trusted fixed threshold while preserving compact predictions.

## Contract choices

- `input_mode: abi_16ch_plus_sza_temporal`
- `frame_selection_policy: temporal_eligible_center`
- `temporal_frame_offsets: [-1, 0, 1]`
- `sampling_policy: combined_source_balanced`
- `augmentation_policy: random_mirroring`
- `loss: bce_dice`
- Line and Centerline trusted auxiliary targets with weighted BCE
- AdamW, constant LR, batch size 2, exploratory manifest max 12 epochs
- `budget_request.yaml` requests the approved 36-epoch `late_improving` budget from ABI-306/285 parent evidence

## Architecture summary

The model consumes only the Harness-supplied temporal ABI+Solar Geometry Input tensor. It builds finite per-frame normalized ABI and BTD features, fuses previous/center/next frames through temporal attention and change features, constructs an early C4 orientation-consensus line state, injects that line state through a compact U-Net encoder/decoder, and applies high-resolution directional context.

`ConnectedRecallLadderHead` returns primary `mask_logits` plus trusted auxiliary `line_logits` and `centerline_logits`. It uses:

- a base mask anchor;
- Line/Centerline agreement;
- differentiable horizontal/vertical continuity context;
- a bounded non-negative recall lift in the base-mask uncertainty band;
- a small low-line-evidence clutter veto suppressed near confident base-mask anchors.

This is all architecture-internal logit generation. It is not thresholding, postprocessing, morphology, Artifact Filtering, custom loss/metric logic, temporal lookup, data loading, sample selection, coordinate use, Dataset Source identity use, downloading, resource scheduling, or lifecycle control.

## Expected comparison

Primary comparison is ABI-306 (`run_20260914_124245_de843c`) on the same temporal-eligible capped validation population. A useful result would improve ABI-306 recall or connectivity while preserving most of ABI-306's precision and compact footprint. A broad recall-heavy regression should stop this exact head branch.
