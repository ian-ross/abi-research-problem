# ABI-313 temporal five-frame continuity-protected calibration late36

## Hypothesis

ABI-311's five-frame persistence/contrast temporal C4 stem is a useful balanced comparator, but its remaining weakness is MIT/positive-patch undercoverage and typical connected-line continuity. ABI-312 tested a selective consensus stabilizer and positive-only recall residual, but it broadened the footprint and regressed connectivity. ABI-313 tests a narrower continuity-protected calibration mechanism: preserve ABI-311's stem/decoder, then apply only a signed, bounded logit correction gated by center-frame decoder detail, early temporal C4 line-state support, and learned Line/Centerline auxiliary evidence.

This is a **family-development continuation**, not a promotion candidate. It is capped temporal-eligible feasibility evidence and is not intended to displace ABI-202 on the full Working Validation Split.

## Comparison Target

Primary comparison targets are ABI-311 (`run_20260915_015552_1ac51f`) as the balanced five-frame temporal C4 comparator and ABI-312 (`run_20260915_043533_14234b`) as the negative/mixed selective-consensus attempt. Secondary targets are ABI-306 (`run_20260914_124245_de843c`) as compact high-precision temporal C4 comparator, ABI-309 (`run_20260914_205014_1794f8`) as recall-heavy comparator, and ABI-223/238 as temporal-attention continuity comparators.

## Expected Effect

Relative to ABI-312, ABI-313 should recover filtered Dice and connected-line continuity by avoiding an always-positive residual. Relative to ABI-311, it should preserve the compact five-frame footprint while modestly improving fixed-threshold recall or MIT positive-patch support. A useful result may be a better precision/recall/connectivity trade-off even if aggregate Dice only ties ABI-311's approximately 0.425 temporal-eligible score.

## Implementation Sketch

The Candidate consumes trusted `abi_16ch_plus_sza_temporal` tensors with offsets `[-2, -1, 0, 1, 2]`. It keeps ABI-311's per-frame ABI/Solar Geometry Input/BTD feature builder, five-frame center-relative temporal attention, short/wide persistence and contrast features, early C4 orientation-consensus line state, multi-scale line-state injection, compact U-Net decoder, and high-resolution directional context.

The changed mechanism is the final calibration head. Instead of ABI-311's dual-evidence residual or ABI-312's positive-only selective recall support, the head projects the early temporal C4 line state into high-resolution directional support, intersects it softly with decoder detail, and uses mask/Line/Centerline logits to gate a bounded signed correction. The correction can add or subtract logit evidence and is intended to bridge connected true-contrail pixels only where learned continuity and auxiliary evidence agree.

The model returns `mask_logits`, `line_logits`, and `centerline_logits` only. It does not implement data loading, temporal lookup, frame repair, custom losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, augmentation, sampling, coordinates, Dataset Source inputs, downloads, training loops, or resource scheduling.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal`
- `data.frame_selection_policy: temporal_eligible_center`
- `data.temporal_frame_offsets: [-2, -1, 0, 1, 2]`
- `data.sampling_policy: combined_source_balanced`
- `data.augmentation_policy: random_mirroring`
- `output_form: mask_logits`
- Trusted auxiliary targets: `line -> line_logits` and `centerline -> centerline_logits` with `weighted_bce`
- Trusted primary loss `bce_dice`, optimizer `adamw`, constant learning rate scheduler, batch size 2

## Budget Requested

Request `late_improving` for 36 epochs via `budget_request.yaml`, with fallback to the exploratory budget if denied. ABI-311 and ABI-312 both selected best checkpoints at epoch 27 under the same five-frame temporal C4 resource envelope, so the default 12-epoch exploratory budget would likely truncate the relevant late operating point. Candidate manifest `max_epochs` remains 12; the Harness owns any effective budget change.

## Success Criteria

Useful positive evidence: temporal-eligible `val/filtered_dice` that ties or exceeds ABI-311's 0.425 band, or a trade-off that preserves ABI-311-like footprint/precision while improving fixed-threshold recall, MIT filtered Dice, or connectivity without ABI-312's connectivity regression or ABI-309-scale false-positive footprint.

Diagnostic continuation evidence: finite, non-collapsed, source-informative learning with a late improving trajectory and a clearly distinct precision/recall/connectivity trade-off from ABI-311/312.

Hard-stop evidence: smoke/contract/numerical/resource failure, persistent prediction collapse, lower aggregate and source filtered Dice with no recall/connectivity gain, or another broad low-precision residual that repeats ABI-312/309 failure modes.

## Fallback/Next Decision

If ABI-313 is positive or mixed-positive, request temporal-eligible failure-bucket diagnostics to test whether it repairs MIT/positive-patch undercoverage without increasing negative-patch heavy-tail clutter. If it regresses or merely repeats ABI-311/312 trade-offs, do not submit an unchanged continuation; broaden away from temporal C4 calibration heads toward a different temporal attention or line-continuity family under the Candidate boundary.
