# ABI-347 temporal C4 orientation-bridge compact recall late36

## Hypothesis

Family-development continuation. ABI-346 showed that a bounded recall head can recover true-positive-tail evidence over ABI-306, but temporal-eligible diagnostics showed no aggregate connectivity improvement and a moderate high-tail clutter cost. The hypothesis for ABI-347 is that recall lift routed through an explicit learned multi-orientation bridge will raise uncertain true contrail line segments to the fixed 0.5 threshold only when mask, Line, Centerline, and orientation-continuity evidence agree.

## Comparison Target

Primary comparison target: ABI-346 (`run_20260918_152331_c80150`) on the same provider-owned temporal-eligible validation population for offsets `[-1, 0, 1]`.

Secondary context: ABI-306 as the compact high-precision three-frame temporal C4 comparator, ABI-324 as the balanced temporal C4/detail-consensus connectivity comparator, and ABI-223 as the temporal-attention connectivity comparator. This is capped temporal-eligible feasibility evidence only, not whole Working Validation Split promotion evidence against ABI-202 or ABI-249.

## Expected Effect

Expected favorable pattern: preserve the ABI-346/306 aggregate Dice neighborhood while improving connected-line continuity or reducing negative-patch clutter. Success would look like filtered Dice near ABI-346/306, connectivity above ABI-346/306, fewer high-tail negative predictions than ABI-346, or a better precision/recall/connectivity trade-off than ABI-346.

Expected risk: the orientation bridge may become too conservative and lose the ABI-346 recall lift, or it may behave like another broad residual recall head without compactness/connectivity gains. If so, stop this exact head rather than submitting simple gain tweaks.

## Implementation Sketch

Reuse the ABI-346 temporal feature builder, temporal C4 line-state stem, encoder/decoder, line-state injectors, ASPP context, and high-resolution directional context. Replace the final connected-recall ladder with an orientation-bridge compact-recall head that:

- predicts base mask, Line, and Centerline logits from shared full-resolution features;
- applies a shared anisotropic strip filter across 0/90/180/270-degree rotations to build an architecture-internal orientation bridge;
- learns a bridge-agreement gate from oriented mean/max/dispersion features;
- adds only bounded non-negative uncertainty-band mask-logit support when mask probability, Line probability, Centerline probability, and bridge agreement coexist;
- subtracts a small compactness veto when line/centerline/bridge evidence is weak.

The model still returns only `mask_logits`, `line_logits`, and `centerline_logits` for Harness-owned losses and metrics.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal`
- `data.frame_selection_policy: temporal_eligible_center`
- `data.temporal_frame_offsets: [-1, 0, 1]`
- `data.sampling_policy: combined_source_balanced`
- `data.augmentation_policy: random_mirroring`
- `training.loss: bce_dice`
- `training.optimizer: adamw`
- `training.scheduler.policy: constant_lr`
- `auxiliary_targets`: trusted Line and Centerline targets with weighted BCE
- Candidate-owned code defines architecture only. It does not load data, inspect temporal caches, choose samples, define losses/metrics/thresholds, implement Artifact Filters/postprocessing, use coordinates or Dataset Source identity, download weights, schedule resources, or alter lifecycle behavior.

## Budget Requested

Request the approved `late_improving` budget for 36 epochs using `budget_request.yaml`. Justification: ABI-346 and comparable temporal C4 branches selected informative checkpoints after epoch 12, and the new head is a close mechanism-changing continuation of a resource-profiled family. If the Harness denies the request, run under the exploratory budget and treat the resulting capped evidence as valid.

## Success Criteria

ABI-347 is worth follow-up if it is finite, resource-safe, non-collapsed, source-informative, and shows at least one of:

- filtered Dice near ABI-346/306 with no material loss of source balance;
- connectivity above ABI-346/306 without sacrificing most aggregate/source filtered Dice;
- negative-patch clutter or high-tail predicted-positive burden below ABI-346 at comparable recall;
- a late-improving trajectory that identifies a compact connected-recall state not present in ABI-346.

It does not need to beat mature whole-validation references in this capped temporal-eligible step, but it must improve the ABI-346 trade-off or reveal a diagnostically useful failure mode.

## Fallback/Next Decision

If ABI-347 regresses by broadening predictions, increasing negative-patch clutter, losing recall, or failing to improve connectivity, do not submit another unchanged orientation-bridge compact-recall continuation. Move to a materially different alignment/change mechanism or a non-temporal orientation-recall architecture. If it improves recall/continuity while remaining compact, request a temporal-eligible failure-bucket diagnostic in a later step before making comparator claims. If it fails contract/smoke/numerical checks, classify the failure and create a repair only if the original hypothesis and comparison target can be preserved.
