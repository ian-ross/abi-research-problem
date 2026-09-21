# ABI-316 temporal five-frame decoder line-continuity bridge late36

## Hypothesis

ABI-311's five-frame temporal C4 persistence/contrast stem is the best balanced local temporal C4 comparator, but its temporal-eligible diagnostics show that the gain is not a broad typical positive-patch continuity repair: MIT positive-patch quality and connected-line medians remain weak. ABI-312 and ABI-313 tried to repair this with late logit/head calibration, but both regressed the target aggregate/source/connectivity trade-off. ABI-316 tests a different mechanism: keep ABI-311's five-frame temporal stem and final dual-evidence head, but inject early temporal C4 line-state evidence into decoder representations at multiple scales before logits are formed.

This is a **family-development continuation**, not a promotion candidate. It is capped temporal-eligible feasibility evidence and is not intended to displace ABI-202 on the full Working Validation Split.

## Comparison Target

Primary comparison target is ABI-311 (`run_20260915_015552_1ac51f`) as the balanced five-frame temporal C4 comparator. Secondary targets are ABI-313 (`run_20260915_072045_06149f`) and ABI-312 (`run_20260915_043533_14234b`) as negative/mixed logit-calibration continuations, ABI-306 (`run_20260914_124245_de843c`) as compact high-precision temporal C4 comparator, ABI-309 (`run_20260914_205014_1794f8`) as recall-heavy temporal C4 comparator, and ABI-223/238 as temporal-attention continuity comparators.

## Expected Effect

Relative to ABI-311, ABI-316 should preserve the balanced five-frame footprint while improving typical connected-line support, MIT filtered Dice, or fixed-threshold recall. Relative to ABI-312/313, it should avoid another blunt final-logit residual by refining decoder features before the mask/Line/Centerline heads. A useful result may be a better precision/recall/connectivity trade-off even if aggregate Dice only ties ABI-311's approximately 0.425 temporal-eligible band.

## Implementation Sketch

The Candidate consumes trusted `abi_16ch_plus_sza_temporal` tensors with offsets `[-2, -1, 0, 1, 2]`. It retains ABI-311's per-frame ABI/Solar Geometry Input/BTD feature builder, five-frame attention centered on the zero-offset frame, short/wide persistence and contrast features, early C4 orientation-consensus line state, compact U-Net encoder/decoder, high-resolution directional context, and final dual-evidence mask/Line/Centerline head.

The changed mechanism is a set of decoder-stage line-continuity bridges. After each decoder upsample/fuse stage, the early temporal C4 line state is resized to the decoder scale, projected, combined with decoder features, passed through orientation-aware high-resolution context, and added back through a learned sigmoid gate. This asks the model to form connected decoder features where temporal line-state support and decoder detail agree, rather than adding a late positive logit residual.

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

Request `late_improving` for 36 epochs via `budget_request.yaml`, with fallback to the exploratory budget if denied. ABI-311 selected its best checkpoint at epoch 27, while ABI-312 and ABI-313 were also late-forming close continuations. ABI-316 keeps the same profiled five-frame resource envelope and changes the line-continuity mechanism before logits; the 12-epoch exploratory ceiling would likely truncate the relevant operating point. Candidate manifest `max_epochs` remains 12; the Harness owns any effective budget change.

## Success Criteria

Useful positive evidence: temporal-eligible `val/filtered_dice` that ties or exceeds ABI-311's 0.425 band, or a trade-off that preserves ABI-311-like footprint/precision while improving MIT filtered Dice, fixed-threshold recall, or connected-line continuity without ABI-309-scale false-positive footprint.

Diagnostic continuation evidence: finite, non-collapsed, source-informative learning with a late improving trajectory and a clearly distinct precision/recall/connectivity trade-off from ABI-311/312/313.

Hard-stop evidence: smoke/contract/numerical/resource failure, persistent prediction collapse, lower aggregate and source filtered Dice with no recall/connectivity gain, or another broad low-precision footprint that repeats ABI-309/312 failure modes.

## Fallback/Next Decision

If ABI-316 is positive or mixed-positive, request temporal-eligible failure-bucket diagnostics to test whether decoder-stage continuity bridges improve MIT/positive-patch undercoverage and typical connected-line continuity without increasing negative-patch heavy-tail clutter. If it regresses or merely repeats ABI-311/312/313 trade-offs, do not submit an unchanged continuation; broaden away from temporal C4 decoder/head variants toward a different temporal-attention evidence-sharpening or single-frame C4/orientation recall-support family under the Candidate boundary.
