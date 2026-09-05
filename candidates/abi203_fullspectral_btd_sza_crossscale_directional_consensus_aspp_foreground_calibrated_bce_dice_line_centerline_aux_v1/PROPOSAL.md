# ABI-203 full-spectral BTD+SZA foreground-calibrated cross-scale directional-consensus ASPP

## Proposal classification

**Family-development continuation.** ABI-203 is a controlled exploratory architecture continuation of ABI-202. It is not a promotion claim and does not request the late-improving budget for this first modified-head probe.

## Hypothesis

ABI-202 became the current whole-validation aggregate filtered-Dice reference with strong MIT/Google balance, recall, and connectivity, but the full-split failure buckets still showed a larger aggregate false-positive burden than ABI-184's stricter precision/negative-patch discipline. A small bounded learned foreground-calibration residual on the final mask logits may let the cross-scale directional-consensus branch suppress unsupported clutter while preserving ABI-202's recall, Google Dice, connectivity, and median positive-patch quality.

The hypothesis is limited to model architecture. It does not change data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, metrics, Artifact Filters, thresholding, postprocessing, coordinate inputs, scheduler policy, training loop behavior, resource placement, or prediction retention.

## Comparison Target

Primary comparison target: ABI-202 `run_20260904_043143_ee0005`, whose capped selected checkpoint reached `val/filtered_dice` 0.4276 at epoch 34 and whose whole-validation diagnostic reached filtered Dice 0.4312, MIT/Google filtered Dice 0.4141/0.4644, precision 0.4431, recall 0.4199, connectivity 0.4625, and filtered predicted-positive pixels 672,206.

Secondary comparison target: ABI-184 `run_20260902_213856_2c04ac`, retained as the precision/connectivity and negative-patch-discipline reference. ABI-201 is the exploratory architecture parent and ABI-196 remains a prior ridge-detail bridge aggregate reference.

## Expected Effect

A useful result should complete finitely and test whether a lightweight mask-logit calibration head can reduce predicted-positive burden or raise precision without causing the recall/connectivity collapse seen in earlier local head probes. Desired evidence is near-ABI-202 aggregate/source filtered Dice with lower filtered predicted-positive fraction, higher precision, fewer negative-patch false positives if later evaluated, or a cleaner threshold-sweep operating point. A negative but informative result would show that ABI-202's false-positive burden is not improved by post-refinement logit calibration and that future work should move to a different architecture, loss, data-policy, or trusted calibration frontier.

## Implementation Sketch

Start from the validated ABI-202 cross-scale directional-consensus ASPP model and remove only the candidate-local late-budget request. Keep approved `abi_16ch_plus_sza` inputs, normalized ABI channels 1-16, deterministic ABI-channel-derived thermal BTD planes, normalized/cosine Solar Geometry features, learned 1x1 spectral mixture, signed local/mid-scale detail stem, compact residual encoder, ASPP context, full-scale skip fusion, `CrossScaleDirectionalConsensusBridge`, and line-aware refinement.

Replace the plain `nn.Conv2d` mask head with `ForegroundCalibrationMaskHead`. The head computes the ordinary linear mask logits plus a zero-initialized, bounded `0.35 * tanh(...)` residual derived from refined features, bridged features, local detail, and smoothed context. The residual is modulated by a soft learned support value and predicts no target of its own. It applies no threshold, hard mask, morphological operation, Artifact Filter, geolocation prior, custom loss, or postprocessing. `line_logits` and `centerline_logits` remain ordinary auxiliary heads trained only through trusted provider-derived auxiliary targets.

Keep the manifest choices unchanged from ABI-202 except for the absence of `budget_request.yaml`: trusted `bce_dice`, trusted `combined_source_balanced`, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, provider-derived Line plus Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02, exploratory `max_epochs: 12`, and `constant_lr` scheduling.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.02, AdamW, learning rate 0.0003, batch size 4, manifest `max_epochs: 12`, and constant scheduler policy.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, budget approval, effective epoch limit, and prediction retention.
- Candidate code defines model architecture only and contains no data loading, custom losses, custom metrics, Artifact Filters, postprocessing, thresholding, runtime downloads, filesystem persistence, Candidate-owned scheduling, or coordinate features.

## Budget Requested

One sequential representative capped exploratory Run: at most 1,024 training and validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, 12 effective epochs, the 3,600-second exploratory Docker timeout, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant scheduler policy, disabled early stopping, and pinned A100 execution through the Harness. No late-improving budget is requested for this first modified-head probe.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and the Run remains within the trusted exploratory resource envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. The continuation is promising if it stays near ABI-202/ABI-201 family performance while improving precision or reducing filtered predicted-positive fraction, or if it gives a diagnostically useful cleaner precision/recall tradeoff than ABI-202 without severe recall/connectivity loss.

## Fallback/Next Decision

If ABI-203 fails validation or smoke because of the new head, classify and repair the candidate-local implementation while preserving the foreground-calibration hypothesis. If it completes but regresses aggregate/source Dice, recall, or connectivity without reducing predicted-positive burden, do not repeat this head unchanged and broaden to a different architecture, loss, trusted data policy, or evaluation/calibration frontier. If it improves false-positive discipline while remaining close to ABI-202's aggregate/source metrics, write a Research Note and consider whole-validation failure-bucket diagnostics before any promotion claim.
