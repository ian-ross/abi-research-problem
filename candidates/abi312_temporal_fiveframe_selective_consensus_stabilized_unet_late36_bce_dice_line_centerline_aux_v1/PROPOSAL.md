# ABI-312 temporal five-frame selective consensus stabilized U-Net late36

## Hypothesis

ABI-311's five-frame temporal C4 persistence/contrast stem improved aggregate temporal-eligible filtered Dice, Google Dice, connectivity, and negative-patch clutter balance, but its failure-bucket review showed remaining MIT-heavy positive-patch undercoverage and no uniform median positive-patch connectivity repair. A close continuation can preserve ABI-311's balanced operating point while repairing part of the positive-patch tail if the decoder receives a selective consensus stabilizer: center-frame detail, temporal line-state support, and high-resolution orientation context must agree before the model adds a small recall-supporting logit residual.

Classification: family-development continuation, not a whole-validation promotion candidate. Evidence will be capped temporal-eligible feasibility/diagnostic evidence only.

## Comparison Target

Primary comparison target is ABI-311 (`run_20260915_015552_1ac51f`) as the balanced five-frame temporal C4 comparator. ABI-306 (`run_20260914_124245_de843c`) remains the compact high-precision comparator, and ABI-309 (`run_20260914_205014_1794f8`) remains the recall-heavy broad-footprint comparator. Secondary context includes ABI-223 and ABI-238 temporal-attention/continuity comparators.

## Expected Effect

Compared with ABI-311, ABI-312 should improve MIT or aggregate positive-patch undercoverage and typical connected-line continuity while keeping negative-patch clutter and predicted-positive footprint closer to ABI-311/306 than to ABI-309. The intended improvement is not threshold tuning: it should be visible at the trusted fixed 0.5 threshold through `val/filtered_dice`, source-stratified filtered Dice, filtered recall, connectivity, and predicted-positive footprint.

## Implementation Sketch

The Candidate consumes provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-2, -1, 0, 1, 2]`. It retains ABI-311's per-frame ABI/Solar Geometry Input normalization, ABI-channel-derived BTD planes, five-frame temporal attention, short/wide-baseline persistence/contrast features, early C4 orientation-consensus line state, compact encoder/decoder, multi-scale line-state injection, and high-resolution directional context.

ABI-312 changes the late architecture only. A new `SelectiveConsensusStabilizer` projects the early temporal line state to full resolution, combines it with decoder detail, computes orientation-aware support, and gates that support through a learned soft consensus map. A new `SelectiveConsensusRecallHead` keeps the mask/Line/Centerline heads but adds only a small positive bounded logit residual when shared mask features, trusted auxiliary head evidence, and the consensus support agree. This is model architecture, not candidate-owned thresholding or postprocessing.

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

Request `late_improving` for 36 epochs via `budget_request.yaml`, with fallback to the exploratory budget if denied. ABI-311 selected its best checkpoint at epoch 27, and recent temporal C4 parents selected useful late checkpoints, so the hypothesis is specifically about stabilizing a late operating point. Candidate manifest `max_epochs` remains 12; the Harness owns any effective budget change.

## Success Criteria

Useful positive evidence: temporal-eligible `val/filtered_dice` at or above ABI-311's 0.4250 band, or a diagnostically useful trade-off that improves MIT filtered Dice, filtered recall, or connectivity without moving toward ABI-309-scale footprint or negative-patch clutter. A finite source-informative run with late best epoch and lower positive-patch miss/undercoverage counts would justify follow-up diagnostics even if the aggregate Dice gain is modest.

Hard-stop evidence: smoke/contract/numerical/resource failure, persistent all-negative/all-positive collapse, materially lower aggregate/source filtered Dice with no positive-tail or connectivity improvement, or a broad low-precision footprint resembling ABI-309 without compensating true connected-line evidence.

## Fallback/Next Decision

If ABI-312 is positive or mixed-positive, request temporal-eligible failure-bucket diagnostics to test whether the stabilizer reduces positive-patch undercoverage and MIT tail failures without reintroducing negative-patch heavy-tail clutter. If it regresses or only repeats the ABI-311 operating point, do not submit an unchanged late36 continuation; broaden to a different temporal attention or calibration-head mechanism under the Candidate boundary.
