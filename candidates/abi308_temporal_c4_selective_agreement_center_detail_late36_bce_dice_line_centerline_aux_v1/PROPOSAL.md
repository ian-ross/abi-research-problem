# ABI-308 temporal C4 selective agreement center-detail late36

## Hypothesis

ABI-306 is the current compact high-precision temporal C4 comparator on the capped temporal-eligible validation population, but it leaves an under-recall and continuity tail. ABI-307 proved that center-frame detail support can raise aggregate recall and connectivity, yet its failure-bucket review showed that the added positives were too broad: positive-patch miss tails worsened, typical positive-patch precision/connectivity fell, and Google Dice regressed.

A more selective center-detail bridge that requires agreement among decoder context, center-frame detail, C4 temporal line state, and orientation-consensus detail should keep ABI-306's compact precision/low clutter while retaining a subset of ABI-307's fixed-threshold connected-recall gain.

Classification: family-development continuation. This is a mechanism-changing continuation of the temporal C4 line-state branch, not an unchanged ABI-306/307 continuation and not a whole-validation promotion claim.

## Comparison Target

Primary comparison target: ABI-306 (`run_20260914_124245_de843c`) on the provider-owned temporal-eligible capped validation population for offsets `[-1, 0, 1]`.

Secondary comparison target: ABI-307 (`run_20260914_151259_e64cba`) to test whether the selective gate avoids the broader positive-patch operating point diagnosed in its temporal-eligible failure-bucket review.

Broader context: ABI-285 as the recall-heavy temporal C4 comparator, ABI-223 as the temporal continuity comparator, and ABI-238 as a compact directional temporal-attention comparator.

## Expected Effect

Expected improvements relative to ABI-307:

- recover precision and Google Dice by reducing broad center-detail residual positives;
- reduce predicted-positive footprint and false-positive pixels without returning to ABI-306's lower-recall operating point;
- improve positive-patch median Dice/connectivity if later diagnostics are requested.

Expected improvements relative to ABI-306:

- retain at least a modest filtered-recall or connectivity gain;
- preserve compact negative-patch behavior and avoid severe MIT/Google source imbalance;
- keep resource use comparable to ABI-306/307.

A successful result need not beat whole-validation ABI-202/249, because this is temporal-eligible capped family-development evidence.

## Implementation Sketch

Start from ABI-307's provider-owned `abi_16ch_plus_sza_temporal` input path, per-frame ABI/SZA/BTD feature builder, temporal attention/C4 orientation line-state stem, compact encoder/ASPP/decoder, line-state scale injectors, high-resolution directional context, and dual-evidence mask/Line/Centerline logit head.

Replace ABI-307's `CenterDetailRecallBridge` with a selective agreement-gated bridge. The bridge still projects only the already computed center-frame candidate-visible features and full-resolution temporal line state, but it adds two selectivity steps before residual injection:

1. an orientation-detail gate over local, horizontal, and vertical center-detail features; and
2. a scalar center/line/decoder agreement gate plus a channel-wise residual gate over decoder features, oriented detail, line-state support, and their absolute differences.

The residual amplitude is reduced from ABI-307's broad 0.55 detail injection to 0.35 and is multiplied by both agreement gates. This is architecture-internal learned feature gating only; it performs no thresholding, morphology, postprocessing, Artifact Filtering, target derivation, custom loss, custom metric, sample selection, data loading, temporal lookup, coordinate use, or resource scheduling.

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

Request the approved `late_improving` budget with `requested_max_epochs: 36` via `budget_request.yaml`, parented to ABI-306 (`run_20260914_124245_de843c`) and ABI-307 (`run_20260914_151259_e64cba`). Both parents were finite, non-collapsed, source-informative, resource-safe, and selected best checkpoints at epoch 36. If the request is denied, run under the exploratory budget and treat that result as valid bounded evidence.

## Success Criteria

Primary success relative to ABI-306/307 temporal-eligible capped evidence:

- `val/filtered_dice` matches or exceeds ABI-306 while avoiding source collapse;
- filtered precision and predicted-positive footprint are closer to ABI-306 than ABI-307;
- filtered recall and/or connectivity remains above ABI-306;
- finite training, non-collapsed predictions, and resource use within trusted limits.

Useful mixed evidence: a modest aggregate Dice regression may still justify diagnostics if the Run clearly combines ABI-306-like compactness with ABI-307-like recall/connectivity. Hard-stop evidence for this exact branch: smoke/contract failure, non-finite training, persistent prediction collapse, severe precision/clutter regression, or no recall/connectivity gain over ABI-306.

## Fallback/Next Decision

If ABI-308 improves the trade-off surface, request temporal-eligible failure-bucket diagnostics to verify positive-patch tail behavior and negative-patch clutter. If it merely suppresses ABI-307 back to ABI-306 without recall/connectivity benefit, stop the center-detail bridge branch and broaden to a different mechanism such as recurrent temporal line-state support or a different temporal attention architecture. Do not request another unchanged ABI-306/307/308 late36 continuation.
