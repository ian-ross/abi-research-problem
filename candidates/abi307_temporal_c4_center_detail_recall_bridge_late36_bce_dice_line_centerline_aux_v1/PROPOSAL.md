# ABI-307 temporal C4 center-detail recall bridge late36

## Hypothesis

ABI-306 repaired ABI-285's temporal C4 line-state clutter/precision problem, but the temporal-eligible failure-bucket review showed that the gain came with a positive-patch under-recall tail and connectivity still below ABI-223/238. A compact center-frame detail recall bridge, gated by ABI-306's temporal C4 line state and decoder context, should raise true contrail evidence at the fixed 0.5 threshold without reopening the broad negative-patch clutter footprint.

Classification: family-development continuation. This is a mechanism-changing continuation of the temporal C4 line-state branch, not an unchanged ABI-306 continuation and not a whole-validation promotion claim.

## Comparison Target

Primary comparison target: ABI-306 (`run_20260914_124245_de843c`) on the provider-owned temporal-eligible capped validation population for offsets `[-1, 0, 1]`.

Secondary context: ABI-285 as the recall-heavy temporal C4 parent, ABI-223/238 as temporal continuity comparators, and ABI-255 as compact recurrent temporal context.

## Expected Effect

Expected improvements relative to ABI-306:

- increase filtered recall, especially MIT positive-patch recall, by using center-frame detail evidence before the final logit head;
- preserve most of ABI-306's compact precision and lower negative-patch clutter by requiring agreement between decoder features, center-detail features, and the C4 temporal line state;
- improve or at least not further degrade filtered connectivity versus ABI-306.

A successful result need not beat whole-validation ABI-202/249, because this is temporal-eligible capped family-development evidence.

## Implementation Sketch

Start from ABI-306's provider-owned `abi_16ch_plus_sza_temporal` input path, temporal feature builder, C4 orientation line-state stem, compact encoder/ASPP/decoder, line-state scale injectors, high-resolution directional context, and dual-evidence mask/Line/Centerline logit head.

Add a new architecture-internal `CenterDetailRecallBridge` after high-resolution directional decoder refinement and before the logit head. The bridge projects the already computed center-frame ABI/SZA/BTD features, applies local and horizontal/vertical detail filters, aligns the early temporal C4 line state to full resolution, and adds a bounded gated residual to decoder features. The gate uses only candidate-visible tensors: decoder features, center-frame features derived from provider-approved channels, and the temporal line-state features. It performs no thresholding, morphology, postprocessing, Artifact Filtering, target derivation, custom loss, custom metric, sampling, data loading, temporal lookup, coordinate use, or resource scheduling.

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

Request the approved `late_improving` budget with `requested_max_epochs: 36` via `budget_request.yaml`, parented to ABI-306 (`run_20260914_124245_de843c`). ABI-306 was finite, non-collapsed, source-informative, resource-safe, and selected its best checkpoint at epoch 36; ABI-307 is a close mechanism-changing continuation with a comparable resource profile. If the request is denied, run under the exploratory budget and treat that result as the valid bounded evidence.

## Success Criteria

Primary success relative to ABI-306 temporal-eligible capped evidence:

- higher `val/filtered_dice` with no source collapse;
- filtered recall improves without a large precision collapse or predicted-positive footprint expansion;
- filtered connectivity improves or remains competitive with ABI-306;
- predictions remain finite, non-collapsed, and within trusted resource bounds.

Useful mixed evidence: a clear recall or connectivity gain with modest Dice regression may still justify one diagnostic/evaluation follow-up if negative-patch clutter remains controlled.

Hard-stop evidence for this exact branch: smoke/contract failure, non-finite training, persistent prediction collapse, severe precision/clutter regression, or a clear plateau/divergence that shows the center-detail bridge only expands false positives.

## Fallback/Next Decision

If ABI-307 improves recall/connectivity while preserving compact precision, consider temporal-eligible failure-bucket diagnostics to verify whether MIT positive-patch misses and connected-line fragmentation improved. If it regresses by expanding clutter or losing source balance, stop this exact center-detail bridge and broaden to a different mechanism such as orientation-consensus continuity logits or recurrent temporal line-state support. Do not request another unchanged ABI-306/307 late36 continuation.
