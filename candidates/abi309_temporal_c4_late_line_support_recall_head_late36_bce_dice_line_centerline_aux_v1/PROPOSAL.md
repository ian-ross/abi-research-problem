# ABI-309 temporal C4 late line-support recall head late36

## Hypothesis

ABI-306 is the compact high-precision temporal C4 comparator on the capped temporal-eligible validation population, but it still has an under-recall and connected-line continuity tail. ABI-308 showed that stricter center-detail agreement can raise connectivity, but it over-suppressed true contrail evidence and regressed aggregate/source Dice and recall.

A late line-support recall head that exposes the already learned temporal C4 line state directly to the final logit calibration should be less disruptive than a center-detail residual bridge. It should preserve ABI-306's compact precision while raising connected true-positive logits at the fixed Harness threshold through learned mask/Line/Centerline plus line-state agreement.

Classification: family-development continuation. This is a mechanism-changing continuation of the profiled temporal C4 line-state family, not an unchanged late36 continuation and not a whole-validation promotion claim.

## Comparison Target

Primary comparison target: ABI-306 (`run_20260914_124245_de843c`) on the provider-owned temporal-eligible capped validation population for offsets `[-1, 0, 1]`.

Secondary comparison target: ABI-308 (`run_20260914_175746_f48be2`) to test whether late line-state support retains some of ABI-308's connectivity gain without its source-balanced Dice and recall suppression.

Broader context: ABI-307 as the broad center-detail recall bridge, ABI-223 as the temporal connectivity comparator, and ABI-238 as a compact directional temporal-attention comparator.

## Expected Effect

Expected improvements relative to ABI-306:

- modestly improve filtered recall and/or Contrail Connectivity Metric by adding late full-resolution line-state support to the final logits;
- preserve ABI-306-like precision, compact predicted-positive footprint, and low negative-patch clutter better than broad center-detail residuals;
- keep MIT and Google filtered Dice source-informative without source collapse.

Expected improvements relative to ABI-308:

- recover aggregate filtered Dice, MIT Dice, Google Dice, and recall by avoiding the stricter center-detail agreement bottleneck;
- retain some of ABI-308's connectivity advantage through the temporal C4 line state.

A successful result need not beat whole-validation ABI-202/249, because this is temporal-eligible capped family-development evidence.

## Implementation Sketch

Start from ABI-306's provider-owned `abi_16ch_plus_sza_temporal` input path, per-frame ABI/Solar Geometry/BTD feature builder, temporal attention/C4 orientation line-state stem, compact encoder/ASPP/decoder, line-state scale injectors, high-resolution directional context, and trusted Line plus Centerline auxiliary outputs.

Replace ABI-306's final dual-evidence logit head with `LateLineSupportRecallHead`. The new head:

1. computes the same shared decoder representation and base mask/Line/Centerline logits;
2. resizes the temporal C4 line state to full resolution and projects it into head channels;
3. learns a line-support feature from decoder features, projected line state, and their absolute difference;
4. combines a reduced dual-evidence residual with a bounded line-support residual gated by learned mask, Line, Centerline, and support evidence.

This is architecture-internal learned feature/logit calibration only. It performs no thresholding, morphology, postprocessing, Artifact Filtering, target derivation, custom loss, custom metric, sample selection, data loading, temporal lookup, coordinate use, Dataset Source use, downloads, resource scheduling, or prediction retention.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal`
- `data.frame_selection_policy: temporal_eligible_center`
- `data.temporal_frame_offsets: [-1, 0, 1]`
- `data.sampling_policy: combined_source_balanced`
- `data.augmentation_policy: random_mirroring`
- `training.loss: bce_dice`
- `training.optimizer: adamw`
- `training.scheduler.policy: constant_lr`
- trusted Line auxiliary target `line_logits` with weighted BCE
- trusted Centerline auxiliary target `centerline_logits` with weighted BCE

Candidate code only defines model architecture over Harness-supplied tensors.

## Budget Requested

Request the approved `late_improving` budget with `requested_max_epochs: 36` via `budget_request.yaml`, parented to ABI-306 (`run_20260914_124245_de843c`) and ABI-308 (`run_20260914_175746_f48be2`). Both parents were finite, non-collapsed, source-informative, resource-safe, and selected late checkpoints after the 12-epoch exploratory ceiling. If the request is denied, run under the exploratory budget and treat that result as valid bounded evidence.

## Success Criteria

Primary success relative to ABI-306 temporal-eligible capped evidence:

- `val/filtered_dice` matches or exceeds ABI-306 while avoiding source collapse;
- filtered recall and/or connectivity exceeds ABI-306;
- filtered precision and predicted-positive footprint remain closer to ABI-306 than ABI-307's broad-footprint behavior;
- finite training, non-collapsed predictions, and resource use within trusted limits.

Useful mixed evidence: a modest aggregate Dice regression may still justify diagnostics if ABI-309 clearly combines ABI-306-like compactness with ABI-308-like connectivity. Hard-stop evidence for this exact branch: smoke/contract failure, non-finite training, persistent prediction collapse, severe precision/clutter regression, or no recall/connectivity gain over ABI-306 or ABI-308.

## Fallback/Next Decision

If ABI-309 improves the compactness/recall/connectivity trade-off, request temporal-eligible failure-bucket diagnostics to verify positive-patch tail behavior and negative-patch clutter. If it merely reproduces ABI-306 or suppresses recall like ABI-308, stop this late line-support head branch and broaden to a different temporal recurrence/attention mechanism or a non-temporal architecture-level calibration mechanism. Do not request another unchanged ABI-306/308/309 late36 continuation.
