# ABI-180 Full-Spectral BTD+SZA UPerNet Directional Line-Context BCE-Dice Line+Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-179 was the first bounded UPerNet-style pyramid/detail scout. It completed finitely, remained resource-safe, improved through epoch 12, and reached the capped reference band, but it was connectivity-weak and slightly MIT-weak relative to ABI-068, ABI-130, ABI-154, and ABI-173. ABI-180 keeps the ABI-179 UPerNet pyramid/detail hierarchy and changes only the continuity-focused refinement and auxiliary supervision within approved candidate boundaries.

## Hypothesis

ABI-179 suggests that UPerNet-style pyramid pooling and top-down feature fusion can calibrate broad context and Google-like positives efficiently, but its final high-resolution refiner did not preserve enough thin-line continuity. A non-suppressive additive directional line-context stage that propagates feature evidence along horizontal, vertical, and diagonal orientations should strengthen continuity and MIT retention without discarding ABI-179's precision/Google behavior. Adding a low-weight provider-derived Line Target auxiliary head alongside the existing Centerline Target should make the new directional support easier to learn while keeping mask training governed by the trusted BCE-Dice primary loss.

## Comparison Target

The primary comparison target is ABI-179 `abi179_fullspectral_btd_sza_upernet_pyramid_detail_decoder_bce_dice_centerline_aux_v1`, Run `run_20260902_054206_a6b406`: capped filtered Dice 0.3939, MIT/Google filtered Dice 0.3774/0.4354, filtered precision 0.4520, recall 0.3490, connectivity 0.2895, and filtered predicted-positive fraction 0.00280. Secondary capped references are ABI-173 `run_20260901_234732_bd5917` for SZA-aware signed-detail aggregate behavior, ABI-154 `run_20260901_071026_32d3ec` for precision/connectivity, ABI-130 `run_20260831_121006_7d24be` for SZA-aware ASPP/detail aggregate behavior, and ABI-068 `run_20260828_010836_4ccc77` as the broader current capped aggregate/source-balance comparator. Canonical MCAST 2.1 remains promotion context only.

## Expected Effect

A useful continuation would preserve ABI-179's finite/resource-safe UPerNet behavior while improving filtered connectivity and/or MIT filtered Dice, ideally without losing more than a small amount of aggregate filtered Dice, Google filtered Dice, or precision. A clear negative result would be persistent non-finite behavior, all-negative/all-positive prediction collapse, a severe source-specific collapse, or aggregate filtered Dice falling clearly outside the recent capped SZA-aware reference band without compensating connectivity or MIT-source strength.

## Implementation Sketch

- Use provider-approved `abi_16ch_plus_sza` input only: normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived from approved ABI channels, normalized Solar Geometry Input, cosine SZA, and a learned 1x1 projection over approved inputs.
- Retain ABI-179's compact residual encoder, bottleneck pyramid pooling, top-down feature pyramid, and high-resolution signed-detail fusion.
- Replace the final gated horizontal/vertical line refiner with an additive directional line-context refiner using fixed feature-space directional averages along horizontal, vertical, and both diagonal orientations, learned projections, broad context, and a bounded additive residual. This is model architecture only, not thresholding, postprocessing, an Artifact Filter, or target derivation.
- Return primary `mask_logits` plus provider-declared `line_logits` and `centerline_logits` auxiliary outputs.
- Keep trusted BCE-Dice primary loss, trusted weighted-BCE Line Target auxiliary weight 0.01, trusted weighted-BCE Centerline Target auxiliary weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant scheduler, disabled early stopping, and one sequential representative capped Run.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, Dataset Source identity, labels, predictions, external data, and pretrained weights are not candidate inputs.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `line_logits` and `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, primary and auxiliary loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data claim, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains below the 25,000,000 smoke ceiling and batch size 4 completes inside the trusted runtime envelope.
3. Losses, logits, gradients, parameters, aggregate/source metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As UPerNet family-development evidence, prefer continuation only if ABI-180 improves ABI-179 connectivity or MIT filtered Dice while staying near the ABI-179/130/154/173 aggregate band, or reveals a distinct source/calibration tradeoff useful for deciding whether UPerNet-style context/detail decoders deserve further work.

## Continuation and hard stop

Treat ABI-180 as one of the at-most-two focused UPerNet continuations allowed after the ABI-179 scout. Continue the UPerNet branch only if it remains finite, resource-safe, non-degenerate, source-informative, and directly improves the scout's weak connectivity/MIT signal or reveals an actionable secondary-metric tradeoff. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. Low score alone is not an elimination reason if the trajectory is improving and diagnostically distinct, but another connectivity-weak aggregate regression would argue for broadening away from UPerNet/SZA-aware context-detail decoders.

## Fallback/Next Decision

If ABI-180 fails from a narrow implementation defect while the continuity-refined UPerNet hypothesis remains intact, consider one explicit Repair Candidate in a later Autonomy Step. If it completes finitely but remains connectivity-weak or loses the capped aggregate/source band, document the result and broaden toward a different in-contract architecture, data-policy, preprocessing, calibration, or evaluation frontier. If it unexpectedly improves the ABI-179/173/154 tradeoff or challenges ABI-068, request separate whole-validation diagnostics before making any full-data or promotion claim.
