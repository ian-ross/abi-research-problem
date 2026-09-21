# ABI-311 temporal five-frame C4 persistence-contrast line-state late36

## Hypothesis

A five-frame temporal C4 line-state U-Net can preserve ABI-306's compact high-precision operating point while recovering some of ABI-309's true fixed-threshold recall if the early temporal stem sees both short-baseline (`-1/+1`) and wider-baseline (`-2/+2`) persistence/contrast evidence before C4 orientation consensus. The specific mechanism is not another late line-support head: ABI-311 keeps the ABI-306 dual-evidence mask/Line/Centerline calibration head and moves the change into provider-owned five-frame temporal fusion.

## Comparison Target

Primary comparison target is the temporal-eligible capped temporal C4 frontier: ABI-306 (`run_20260914_124245_de843c`) as compact high-precision comparator, ABI-309 (`run_20260914_205014_1794f8`) as recall-heavy comparator, and ABI-310 (`run_20260914_232554_0320e8`) as the negative/mixed direct line-support interpolation. Secondary context includes ABI-223/238 temporal-attention continuity comparators and prior five-frame scouts ABI-291/304.

## Expected Effect

Compared with ABI-306, ABI-311 is expected to increase filtered recall and connected-line continuity by using wider temporal persistence/contrast features while keeping the filtered predicted-positive footprint materially closer to ABI-306 than ABI-309. Success does not require beating the whole-validation ABI-202 reference because this is temporal-eligible capped feasibility evidence only.

## Implementation Sketch

The Candidate consumes trusted `abi_16ch_plus_sza_temporal` tensors with offsets `[-2, -1, 0, 1, 2]`. Each provider-visible frame is normalized and expanded with ABI-channel-derived BTD planes plus Solar Geometry Input features. A shared frame projector embeds all five frames. The temporal stem computes attention over the five frame embeddings relative to the center frame, builds short-baseline and wide-baseline contrast features (`center - mean(-1,+1)`, `center - mean(-2,+2)`, `+1 - -1`, `+2 - -2`), and injects a bounded persistence residual before the existing C4 orientation-consensus line-state block. The encoder/decoder, multi-scale line-state injectors, high-resolution directional context, and ABI-306 dual-evidence logit head are retained.

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

Request `late_improving` for 36 epochs via `budget_request.yaml`, with fallback to the exploratory budget if denied. The request is justified by late-improving temporal C4 parents ABI-306/309/310 and the resource-safe five-frame ABI-291/304 scouts, including ABI-304's final-epoch best exploratory checkpoint. Candidate manifest `max_epochs` remains 12; the Harness owns any effective budget change.

## Success Criteria

Useful positive evidence: temporal-eligible `val/filtered_dice` at or above ABI-306/309's approximately 0.422-0.424 band, or a clearly useful trade-off with ABI-306-like precision/footprint plus improved filtered recall/connectivity. Diagnostic continuation is also justified if the run is finite, source-informative, best epoch is late, and it improves either MIT filtered Dice or connectivity without ABI-309-scale negative-patch clutter signals.

Hard-stop evidence: smoke/contract/numerical/resource failure, persistent all-negative/all-positive collapse, materially lower aggregate/source filtered Dice with no recall/connectivity improvement, or another broad-footprint low-precision operating point resembling ABI-309 without compensating true connected-line evidence.

## Fallback/Next Decision

If ABI-311 is positive or mixed-positive, request temporal-eligible failure-bucket diagnostics to determine whether wider temporal context reduces positive-patch under-recall and fragmentation without increasing negative-patch heavy-tail false positives. If it regresses or only repeats the known compactness/recall trade-off, do not submit an unchanged continuation; broaden to a different temporal attention/calibration or line-continuity mechanism under the same Candidate boundary.
