# Proposal: ABI-287 temporal C4 recall-protected continuity bridge U-Net

## Classification

Family-development continuation in the provider-owned temporal ABI input family. This is an exploratory capped mechanism test, not a promotion claim.

## Hypothesis

ABI-286 showed that adding full-resolution continuity evidence to the ABI-285 temporal C4 line-state family can improve connected-line organization relative to the 12-epoch ABI-284 parent, especially by its final checkpoint, but its agreement bridge was too suppressive and lost too much of ABI-285's stronger recall and source balance. The hypothesis is that a recall-protected continuity bridge--where decoder appearance remains the primary mask path and line-continuity evidence is added only as a bounded residual sidecar plus a small non-negative evidence lift--can recover more fixed-threshold recall while retaining useful continuity support.

## Comparison Target

Primary temporal-family comparison targets:

- ABI-285 (`run_20260913_100333_a250df`) for the late36 temporal C4 recall/source-balance target to preserve.
- ABI-286 (`run_20260913_123056_4152f3`) for the suppressive continuity-bridge failure mode to repair.
- ABI-284 (`run_20260913_091156_167372`) as the immediate 12-epoch temporal C4 parent.
- ABI-223 (`run_20260908_154531_8c7e2b`) and ABI-238 (`run_20260911_004137_f54c45`) for stronger temporal-eligible connected-line comparators.
- ABI-274 (`run_20260912_180856_79ba22`) for temporal line-state recall/source behavior.

ABI-202 remains the whole-validation aggregate reference, but this Candidate should be interpreted on the provider-owned temporal-eligible capped validation population.

## Implementation Sketch

Start from ABI-286's temporal C4 continuity-bridge U-Net using provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`. Keep the per-frame ABI/SZA/BTD feature builder, temporal attention/change stem, early C4 orientation line-state, encoder-scale line-state injection, ASPP bottleneck, high-resolution directional decoder context, and trusted Line/Centerline auxiliary outputs.

Change only the post-decoder bridge and mask head:

- replace ABI-286's agreement bridge with a recall-protected continuity sidecar that projects the early temporal C4 line state to full decoder resolution, computes C4 continuity support, and adds only a modest gated residual to the decoder features;
- keep decoder appearance as the primary `mask_logits` path rather than making line agreement a suppressive bottleneck;
- add a region-preserving head whose line-support branch contributes a small non-negative evidence lift initialized near zero, so learned line support can raise weak connected contrail evidence at the fixed 0.5 threshold without implementing threshold selection or postprocessing;
- continue to emit `line_logits` from the support branch and `centerline_logits` from the region branch for trusted auxiliary targets.

All mechanisms are differentiable architecture logic only. The Candidate does not threshold, skeletonize, connect components morphologically, postprocess predictions, apply Artifact Filters, derive labels, or inspect hidden temporal/cache metadata.

## Contract Features Used

The Candidate uses only provider-advertised `abi_16ch_plus_sza_temporal` tensors. The manifest requests trusted `temporal_eligible_center` frame selection, temporal offsets `[-1, 0, 1]`, source-balanced sampling, random mirroring, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, and trusted Line/Centerline auxiliary targets with weighted BCE. Candidate code does not load data, inspect temporal cache state, download frames, repair or pad temporal neighbors, select samples, implement losses/metrics/augmentation, derive targets, use Dataset Source identity, use longitude/latitude, set thresholds, postprocess predictions, apply Artifact Filters, write external artifacts, choose GPUs, or schedule resources.

## Expected Effect

The intended effect is to keep more of ABI-285's recall/source balance than ABI-286 while retaining or improving ABI-286's continuity gains over ABI-284. The most useful outcome would move closer to ABI-223/238 connected-line behavior without the broad low-precision clutter or recall collapse failure modes observed in recent temporal C4 variants.

## Budget

Use the exploratory/default budget: 12 epochs, batch size 2, constant learning rate, disabled early stopping, and Harness-owned execution/resource limits. Do not request `late_improving` for this first recall-protected mechanism variant.

## Success Criteria

A useful exploratory result should be finite, non-collapsed, resource-safe, and source-informative. It need not beat the mature temporal comparators immediately, but should show at least one of:

- higher filtered Dice, recall, or MIT/source balance than ABI-286 while keeping connectivity at or above ABI-286's best checkpoint;
- a better recall/connectivity tradeoff than ABI-284/286 at the same 12-epoch budget;
- evidence that the non-negative support lift raises true contrail pixels without exploding filtered predicted-positive fraction or negative-patch clutter;
- an improving or ambiguous epoch-12 trajectory that justifies a bounded continuation.

## Fallback Next Decision

Do not repeat this exact recall-protected bridge unchanged if it collapses into broad false-positive clutter, remains below ABI-286 on both recall and connectivity, underpredicts like conservative C4 branches, or has numerical/resource failure. If finite and improving with a better recall/connectivity tradeoff, consider either a late-improving close continuation or temporal-eligible failure-bucket diagnostics in a later Autonomy Step.
