# ABI-161 full-spectral BTD+SZA BiFPN line-fusion U-Net

## Hypothesis

A bidirectional feature-pyramid line-fusion U-Net can recover a more source-balanced fixed-threshold operating point than recent local ASPP/detail decoder refinements by repeatedly mixing high-resolution thin-line evidence with coarser cloud context before the final mask head. This is a **family scout** for a BiFPN-style context-fusion branch, not a promotion claim against mature capped references.

## Comparison Target

Primary capped references are ABI-068 (`run_20260828_010836_4ccc77`, filtered Dice 0.3964), ABI-130 (`run_20260831_121006_7d24be`, filtered Dice 0.3953), ABI-154 (`run_20260901_071026_32d3ec`, filtered Dice 0.3944), and the recent negative/mixed SZA-aware ASPP/detail continuations ABI-155 through ABI-160. ABI-160 showed that another local mid-level directional residual improved ABI-159 but remained below the useful band and source-unstable, so ABI-161 broadens away from ASPP bottleneck and full-scale-skip refinements.

## Expected Effect

The expected useful outcome is not immediate promotion. The scout should stay finite and non-collapsed, keep aggregate filtered Dice within roughly 0.010-0.015 of ABI-130/ABI-154 or clearly improve over ABI-160, and avoid a catastrophic MIT/Google imbalance. A successful trajectory would show improved filtered recall or connectivity versus ABI-160 while retaining precision near the ABI-130/ABI-154 band. Even if the aggregate score remains below ABI-068, a balanced, improving trajectory would justify one bounded BiFPN-family continuation.

## Implementation Sketch

The candidate uses provider-approved `abi_16ch_plus_sza` tensors only. `model.py` constructs normalized ABI channels, deterministic thermal BTD planes from approved ABI channels, normalized Solar Geometry Input, a cosine Solar Geometry feature, and a learned 1x1 spectral mixture. A compact convolutional encoder produces four spatial scales. Instead of an ASPP bottleneck or full-scale skip aggregator, the model projects all scales to a common feature width and applies learnable positive weighted top-down and bottom-up feature-pyramid fusion. A high-resolution line-evidence stem and final horizontal/vertical line-fusion head refine feature-space logits. The model returns `mask_logits` plus `centerline_logits` for a provider-derived auxiliary target.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza`; longitude and latitude are neither requested nor reconstructed.
- Output form: `mask_logits` with provider-derived `centerline_logits` auxiliary output.
- Trusted primary loss: `bce_dice`.
- Trusted auxiliary loss: `weighted_bce` for `centerline` at weight 0.02.
- Trusted sampling traversal: `combined_source_balanced`.
- Trusted augmentation: `random_mirroring`.
- Trusted optimizer/schedule: AdamW, learning rate 0.0003, `constant_lr` scheduler.
- Candidate code defines architecture only and does not implement data loading, target derivation, losses, metrics, thresholding, Artifact Filters, sampling policy, augmentation transforms, resource placement, or lifecycle behavior.

## Budget Requested

Use the active Workspace Configuration ceilings: 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, max 12 epochs, batch size 4, constant learning rate, disabled early stopping, 3,600-second Docker training timeout, 25M-parameter smoke ceiling, and Harness-owned concurrency one. This unprofiled BiFPN architecture should run sequentially.

## Success Criteria

- Static validation passes and smoke training remains finite under the parameter ceiling.
- The Run completes without contract, resource, Harness, non-finite, or persistent all-negative/all-positive prediction-collapse failure.
- Best-validation `val/filtered_dice` improves meaningfully over ABI-160 or remains close enough to ABI-130/ABI-154 while improving filtered recall/connectivity or source balance.
- MIT and Google filtered Dice remain non-catastrophic, and raw-to-filtered differences do not indicate primary Artifact Filter dependence.
- Learning trajectory is still improving or diagnostically distinct enough to justify one bounded BiFPN-family continuation.

## Fallback/Next Decision

If ABI-161 fails static validation or smoke for a candidate bug, create at most one repair preserving this hypothesis. If it trains finitely but is clearly worse than ABI-160 with poor source balance or prediction collapse, do not continue this exact BiFPN branch. If it is finite, non-collapsed, and diagnostically balanced or improving, consider one controlled continuation that adjusts line-fusion capacity or primary loss within trusted allowlists. If the entire local SZA/full-spectral line-fusion frontier remains negative, broaden to a materially different architecture family or write a Research Note proposing non-architecture next axes.
