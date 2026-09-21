# ABI-322 temporal five-frame C4 clDice-connectivity line-state late36

## Hypothesis

ABI-311's five-frame temporal C4 persistence/contrast line-state architecture already produced the best balanced temporal C4 capped Result, with cleaner negative-patch clutter than ABI-309 and better connectivity/recall than ABI-306. Its remaining weakness is MIT/positive-patch undercoverage and non-uniform typical-patch continuity. ABI-322 tests a trusted loss-policy mechanism: keep the ABI-311 architecture fixed, but train it with the allowlisted `bce_dice_cldice` primary loss so the same five-frame line-state evidence is optimized for thin-line topology rather than adding another late residual head.

## Proposal Type

Family-development continuation / loss-policy scout within the profiled ABI-311 five-frame temporal C4 family. This is not a promotion claim and not whole-validation evidence; it is temporal-eligible capped feasibility evidence.

## Comparison Target

Primary comparison target is ABI-311 (`run_20260915_015552_1ac51f`) plus its temporal-eligible failure-bucket evaluation (`eval_evalreq_abi311_temporal_eligible_failure_buckets_v1`). Secondary comparators are ABI-306 (`run_20260914_124245_de843c`) as compact high-precision temporal C4, ABI-309 (`run_20260914_205014_1794f8`) as recall-heavy temporal C4, ABI-316 (`run_20260915_110252_3a6dca`) as negative decoder-continuity bridge, and ABI-223 (`run_20260908_154531_8c7e2b`) as temporal-attention connectivity comparator.

## Expected Effect

Compared with ABI-311, ABI-322 is expected to preserve a similar prediction footprint while improving connected-line continuity, MIT filtered Dice, or positive-patch undercoverage by optimizing the same mask/line evidence under a trusted topology-aware loss. A useful trade-off would be ABI-311-like aggregate/source Dice with higher connectivity, or ABI-306-like compactness with improved recall/continuity. A bad result would resemble ABI-312/316: lower Dice/source balance and no stable connectivity gain.

## Implementation Sketch

Copy the ABI-311 architecture unchanged except for candidate identifiers. The model consumes trusted five-frame `abi_16ch_plus_sza_temporal` tensors, normalizes ABI channels, derives ABI-channel-only BTD planes, computes center-relative temporal attention over offsets `[-2, -1, 0, 1, 2]`, builds short/wide temporal persistence and contrast features, injects a C4 orientation-consensus line state into encoder scales, decodes through a compact U-Net with high-resolution directional context, and returns `mask_logits`, `line_logits`, and `centerline_logits`.

The manifest changes the trusted primary loss from `bce_dice` to `bce_dice_cldice`. Line and Centerline auxiliaries remain trusted `weighted_bce`. The Candidate does not implement custom losses, clDice code, target transforms, metrics, thresholding, postprocessing, Artifact Filters, temporal lookup, sample selection, coordinates, Dataset Source identity, training loops, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal`
- `data.frame_selection_policy: temporal_eligible_center`
- `data.temporal_frame_offsets: [-2, -1, 0, 1, 2]`
- `data.sampling_policy: combined_source_balanced`
- `data.augmentation_policy: random_mirroring`
- `output_form: mask_logits`
- Trusted auxiliary targets: `line -> line_logits` and `centerline -> centerline_logits` with `weighted_bce`
- Trusted primary loss `bce_dice_cldice`, optimizer `adamw`, constant learning rate scheduler, batch size 2

## Budget Requested

Request `late_improving` for 36 epochs via `budget_request.yaml`, with fallback to the exploratory budget if denied. The request is justified because the directly reused ABI-311 architecture was late-budget-dependent, selected its best checkpoint at epoch 27, and remained finite/resource-safe. This loss-policy continuation should be evaluated at a comparable budget before judging whether clDice can stabilize the ABI-311 connected-line evidence.

## Success Criteria

Useful positive evidence: temporal-eligible `val/filtered_dice` near ABI-311's 0.425 band with improved filtered connectivity, MIT filtered Dice, or low-recall positive-patch behavior; or a compact ABI-306-like footprint with materially improved recall/continuity. Diagnostic continuation could be justified if the Run is finite, source-informative, late-improving, and shows a new precision/recall/connectivity trade-off not already characterized by ABI-306/309/311/316.

Hard-stop evidence: smoke/contract/numerical/resource failure, persistent all-negative/all-positive collapse, broad false-positive footprint without connected true-positive gain, materially lower aggregate/source filtered Dice with no connectivity or positive-tail improvement, or an unstable trajectory that repeats ABI-312/316's degraded continuity pattern.

## Fallback/Next Decision

If ABI-322 is positive or mixed-positive, request temporal-eligible failure-bucket diagnostics to test whether any connectivity gain reduces MIT/positive-patch undercoverage rather than creating negative-patch clutter. If it regresses, do not submit an unchanged clDice continuation; broaden away from temporal C4 calibration/loss variants toward a different temporal-attention or line-continuity mechanism under the same Candidate boundary.
