# ABI-310 temporal C4 agreement-gated line-support late36

## Hypothesis

ABI-309 showed that exposing the temporal C4 line state to the final logit head can recover real fixed-threshold true positives over ABI-306, but the recall gain was too blunt: negative-patch false-positive burden and predicted-positive footprint rose sharply while connectivity remained below ABI-223/238. ABI-310 tests whether an agreement-gated line-support calibration head can retain part of ABI-309's positive-patch recall recovery while preserving more of ABI-306's compact high-precision behavior.

Classification: family-development continuation. This is a mechanism-changing continuation of the profiled temporal C4 line-state family, not an unchanged ABI-306/307/308/309 late36 continuation and not a whole-validation promotion claim.

## Comparison Target

Primary comparison target: ABI-306 (`run_20260914_124245_de843c`) on the provider-owned temporal-eligible capped validation population for offsets `[-1, 0, 1]`, because ABI-306 remains the compact high-precision temporal C4 comparator.

Secondary comparison target: ABI-309 (`run_20260914_205014_1794f8`), because ABI-309 is the recall-support temporal C4 variant whose added true positives came with excessive footprint and clutter.

Broader context: ABI-223 as temporal continuity comparator, ABI-238 as compact directional temporal-attention comparator, ABI-307 as broad center-detail support evidence, and ABI-308 as high-connectivity/over-suppression evidence.

## Expected Effect

Expected improvements relative to ABI-309:

- reduce filtered predicted-positive footprint and negative-patch false-positive burden by requiring learned agreement between base mask evidence, auxiliary line/centerline evidence, and the resized temporal C4 line state;
- improve filtered precision while retaining some of ABI-309's recall gain over ABI-306;
- keep source-stratified filtered Dice viable on both MIT and Google without source collapse.

Expected improvements relative to ABI-306:

- improve filtered recall and/or positive-patch miss-tail behavior through selective line-state support;
- preserve ABI-306-like compactness better than ABI-309's broad recall-heavy operating point;
- modestly improve or at least not materially degrade connectivity.

A successful Result need not beat whole-validation ABI-202/249, because this is temporal-eligible capped family-development evidence only.

## Implementation Sketch

Start from ABI-309's provider-owned `abi_16ch_plus_sza_temporal` input path, per-frame ABI/Solar Geometry/BTD feature builder, temporal attention/C4 orientation line-state stem, compact encoder/ASPP/decoder, line-state scale injectors, high-resolution directional context, and trusted Line plus Centerline auxiliary outputs.

Replace ABI-309's `LateLineSupportRecallHead` with `AgreementGatedLineSupportHead`. The new head:

1. computes a shared decoder representation and base mask/Line/Centerline logits;
2. resizes and projects the temporal C4 line state to full resolution;
3. forms learned agreement features from decoder features, line-state features, their product, and their absolute difference;
4. applies a smaller positive support residual gated by base-mask, Line, Centerline, support, and auxiliary-agreement probabilities;
5. adds a learned unsupported-evidence suppression term where decoder and line-state features disagree and support evidence is weak.

All operations are differentiable architecture-internal feature/logit calibration. The Candidate performs no thresholding, morphology, postprocessing, Artifact Filtering, target derivation, custom loss, custom metric, sample selection, data loading, temporal lookup, coordinate use, Dataset Source use, downloads, resource scheduling, or prediction retention.

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

Request the approved `late_improving` budget with `requested_max_epochs: 36` via `budget_request.yaml`, parented to ABI-306 (`run_20260914_124245_de843c`) and ABI-309 (`run_20260914_205014_1794f8`). Both parents were finite, non-collapsed, source-informative, resource-safe, and selected late checkpoints after the 12-epoch exploratory ceiling. If the request is denied, run under the exploratory budget and treat that result as valid bounded evidence.

## Success Criteria

Primary success relative to ABI-309 and ABI-306 temporal-eligible capped evidence:

- filtered Dice is within the ABI-306/309 temporal C4 comparator band while avoiding source collapse;
- filtered precision and predicted-positive footprint move materially back toward ABI-306 compared with ABI-309;
- filtered recall remains meaningfully above ABI-306 or positive-patch under-recall tails improve in later diagnostics;
- connectivity does not materially regress below ABI-306;
- finite training, non-collapsed predictions, and resource use remain within trusted limits.

Useful mixed evidence: a small filtered-Dice regression may still justify diagnostics if ABI-310 clearly improves the precision/recall/footprint trade-off and source balance. Hard-stop evidence for this exact head: smoke/contract failure, non-finite training, persistent prediction collapse, severe recall collapse, or reproducing ABI-309's clutter without precision recovery.

## Fallback/Next Decision

If ABI-310 improves the compactness/recall trade-off, request temporal-eligible failure-bucket diagnostics to verify positive-patch tail behavior and negative-patch heavy-tail clutter. If it simply suppresses recall like ABI-308 or stays broad/cluttered like ABI-309, stop this agreement-gated line-support head branch and broaden to a different temporal attention/calibration mechanism rather than submitting another unchanged late36 continuation.
