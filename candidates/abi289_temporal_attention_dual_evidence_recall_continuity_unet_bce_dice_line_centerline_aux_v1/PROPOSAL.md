# Proposal: ABI-289 temporal attention dual-evidence recall/continuity U-Net

## Classification

Family-development continuation in the provider-owned temporal ABI input family. This is an exploratory capped mechanism test, not a promotion claim.

## Hypothesis

Recent temporal work has exposed two failure modes. ABI-288 showed that switching the resource-profiled ABI-238 temporal-attention directional-context architecture to the trusted `bce_dice_cldice` primary loss did not improve connected-line continuity and materially reduced precision/source-stratified Dice. ABI-286/287 showed that feature-level C4 continuity bridges can also fail to align fixed-threshold recall with connected-line support.

The hypothesis is that a late dual-evidence geometry can do better: preserve a center-detail recall path as the primary mask evidence, keep directional continuity evidence in a separate line-support path, and merge them only as a small bounded non-negative logit lift. This should allow weak connected contrail evidence to rise at the fixed 0.5 threshold without making continuity a suppressive feature bottleneck or relying on Candidate-owned thresholds/postprocessing.

## Comparison Target

Primary temporal-family comparison targets:

- ABI-238 (`run_20260911_004137_f54c45`) as the same backbone's temporal-attention directional-context comparator.
- ABI-223 (`run_20260908_154531_8c7e2b`) as the mature temporal-attention comparator with strong temporal-eligible connectivity.
- ABI-288 (`run_20260913_143121_ebfc60`) as the negative trusted-loss variant on ABI-238's architecture.
- ABI-286 (`run_20260913_123056_4152f3`) and ABI-287 (`run_20260913_133037_6bd482`) as recent continuity-bridge failure modes.
- ABI-285 (`run_20260913_100333_a250df`) for the temporal C4 late36 recall/source-balance target.

ABI-202 remains the whole-validation aggregate reference, but this Candidate should be interpreted on the provider-owned temporal-eligible capped validation population.

## Implementation Sketch

Start from ABI-238's temporal-attention directional-context U-Net over provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`. Keep the per-frame ABI/SZA/BTD feature builder, temporal attention/change stem, single-stream encoder, ASPP bottleneck, decoder, and high-resolution directional context.

Change the full-resolution head geometry:

- add a center-detail recall path that processes the center frame's ABI/SZA/BTD features and fuses them with decoder features for primary `mask_logits`;
- keep a separate directional continuity path over decoder features and use it for `line_logits`;
- compute an agreement representation from recall features, continuity features, and their absolute difference;
- add only a small bounded non-negative agreement lift to the primary mask logits, initialized near zero, so the learned support can raise weak line evidence without threshold selection, morphology, or postprocessing;
- emit `centerline_logits` from the recall path and `line_logits` from the continuity path for trusted auxiliary targets.

All mechanisms are differentiable architecture logic only. The Candidate does not threshold, skeletonize, connect components morphologically, postprocess predictions, apply Artifact Filters, derive labels, or inspect hidden temporal/cache metadata.

## Contract Features Used

The Candidate uses only provider-advertised `abi_16ch_plus_sza_temporal` tensors. The manifest requests trusted `temporal_eligible_center` frame selection, temporal offsets `[-1, 0, 1]`, source-balanced sampling, random mirroring, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, and trusted Line/Centerline auxiliary targets with weighted BCE. Candidate code does not load data, inspect temporal cache state, download frames, repair or pad temporal neighbors, select samples, implement losses/metrics/augmentation, derive targets, use Dataset Source identity, use longitude/latitude, set thresholds, postprocess predictions, apply Artifact Filters, write external artifacts, choose GPUs, or schedule resources.

## Expected Effect

The intended effect is to retain more of ABI-238/223 precision and source balance than ABI-288 while improving the recall/connectivity alignment targeted by ABI-286/287. A useful result would avoid broad negative-patch clutter, keep filtered predicted-positive fraction near the temporal comparator band, and show either better connectivity at comparable recall or better recall at comparable connectivity.

## Budget

Use the exploratory/default budget: 12 epochs, batch size 2, constant learning rate, disabled early stopping, and Harness-owned execution/resource limits. Do not request `late_improving` for this first dual-evidence variant.

## Success Criteria

A useful exploratory result should be finite, non-collapsed, resource-safe, and source-informative. It need not beat the mature temporal comparators immediately, but should show at least one of:

- better filtered Dice, precision, or connectivity than ABI-288 while keeping recall near or above ABI-238/223;
- a better recall/connectivity tradeoff than ABI-286/287 without expanding filtered predicted-positive fraction into broad clutter;
- MIT and Google filtered Dice both remaining source-informative and not catastrophically imbalanced;
- an improving or ambiguous epoch-12 trajectory that justifies a bounded continuation.

## Fallback Next Decision

Do not repeat this exact dual-evidence head unchanged if it collapses into broad false-positive clutter, underpredicts like conservative C4 branches, remains below ABI-288 on both precision and connectivity, or has numerical/resource failure. If finite and improving with a better recall/connectivity tradeoff, consider either temporal-eligible failure-bucket diagnostics or a late-improving close continuation in a later Autonomy Step.
