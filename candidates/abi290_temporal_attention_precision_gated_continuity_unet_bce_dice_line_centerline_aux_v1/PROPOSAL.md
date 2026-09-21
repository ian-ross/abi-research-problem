# Proposal: ABI-290 temporal attention precision-gated continuity U-Net

## Classification

Family-development continuation in the provider-owned temporal ABI input family. This is an exploratory capped mechanism test, not a promotion claim.

## Hypothesis

ABI-289 showed that the ABI-238-style temporal-attention backbone can raise fixed-threshold recall when center-detail and continuity evidence are merged as a late non-negative lift, but the lift was too permissive: precision, source Dice, connected-line organization, and negative-patch cleanliness all regressed versus ABI-238/223 and ABI-285. ABI-286/287 also showed that suppressive C4 continuity sidecars can trade away too much recall.

The hypothesis is that the same temporal-attention recall/continuity separation can be made cleaner if the continuity lift is explicitly precision-gated by learned agreement between center-detail recall features and directional continuity features, with a tiny learned clutter veto initialized inactive. This should preserve ABI-289's recall lesson while preventing broad low-agreement mask expansion, without Candidate-owned thresholds, morphology, postprocessing, metrics, losses, Artifact Filters, temporal lookup, sample selection, or coordinates.

## Comparison Target

Primary temporal-family comparison targets:

- ABI-289 (`run_20260913_194511_b462e0`) as the immediate dual-evidence recall/continuity parent that raised recall but broadened clutter.
- ABI-238 (`run_20260911_004137_f54c45`) as the same-backbone temporal-attention directional-context comparator.
- ABI-223 (`run_20260908_154531_8c7e2b`) as the mature temporal-attention line-continuity comparator.
- ABI-285 (`run_20260913_100333_a250df`) as the current capped temporal-eligible aggregate filtered-Dice and recall comparator.
- ABI-286/287 (`run_20260913_123056_4152f3`, `run_20260913_133037_6bd482`) as recent continuity-bridge failure modes.

ABI-202 remains the whole-validation aggregate reference, but this Candidate should be interpreted only on the provider-owned temporal-eligible capped validation population.

## Implementation Sketch

Start from ABI-289's temporal-attention U-Net over provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`. Keep the per-frame ABI/SZA/BTD feature builder, temporal attention/change stem, single-stream encoder, ASPP bottleneck, decoder, center-detail recall path, separate high-resolution directional continuity path, trusted `line_logits`, and trusted `centerline_logits`.

Change only the late head geometry:

- compute agreement features from recall features, continuity features, and their absolute difference;
- predict the primary region logits from the center-detail recall path;
- predict a non-negative continuity lift, but multiply it by a learned precision gate from the agreement features, initialized conservative;
- add a very small learned clutter-veto residual from the same agreement features, initialized nearly inactive, so the model can suppress low-agreement line-like clutter through differentiable architecture logic rather than thresholding or postprocessing;
- keep line auxiliary logits on the continuity path and centerline auxiliary logits on the recall path.

All mechanisms are model architecture only. The Candidate does not threshold, skeletonize, connect components morphologically, postprocess predictions, apply Artifact Filters, derive labels, inspect hidden temporal/cache metadata, or select examples.

## Contract Features Used

The Candidate uses only provider-advertised `abi_16ch_plus_sza_temporal` tensors. The manifest requests trusted `temporal_eligible_center` frame selection, temporal offsets `[-1, 0, 1]`, source-balanced sampling, random mirroring, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, and trusted Line/Centerline auxiliary targets with weighted BCE. Candidate code does not load data, inspect temporal cache state, download frames, repair or pad temporal neighbors, select samples, implement losses/metrics/augmentation, derive targets, use Dataset Source identity, use longitude/latitude, set thresholds, postprocess predictions, apply Artifact Filters, write external artifacts, choose GPUs, or schedule resources.

## Expected Effect

The intended effect is to keep ABI-289's recall-positive behavior while recovering precision, source balance, and connected-line organization closer to ABI-238/223/285. A useful result would reduce ABI-289's filtered predicted-positive footprint and false-positive tendency while maintaining recall above the ABI-238/223 band or improving connectivity at comparable footprint.

## Budget

Use the exploratory/default budget: 12 epochs, batch size 2, constant learning rate, disabled early stopping, and Harness-owned execution/resource limits. Do not request `late_improving` for this first precision-gated continuity variant.

## Success Criteria

A useful exploratory result should be finite, non-collapsed, resource-safe, and source-informative. It need not beat the mature temporal comparators immediately, but should show at least one of:

- higher filtered precision, source Dice, or connectivity than ABI-289 while preserving much of ABI-289's recall lift;
- a better recall/connectivity tradeoff than ABI-286/287 without broadening filtered predicted-positive fraction beyond ABI-289;
- filtered Dice approaching the ABI-238/223/285 temporal comparator band with both MIT and Google remaining source-informative;
- an improving or ambiguous late trajectory that justifies a bounded continuation.

## Fallback Next Decision

Do not repeat this exact precision-gated head unchanged if it still expands clutter like ABI-289, suppresses recall like conservative C4 branches, remains below ABI-286/287 on both aggregate Dice and connectivity, or has numerical/resource failure. If finite and improving with better cleanliness and recall/connectivity alignment, consider a later temporal-eligible failure-bucket diagnostic or a late-improving close continuation in a future Autonomy Step.
