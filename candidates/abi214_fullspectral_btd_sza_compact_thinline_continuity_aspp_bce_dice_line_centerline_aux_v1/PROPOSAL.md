# ABI-214 compact full-spectral BTD+SZA thin-line continuity ASPP

## Proposal classification

**Family-development continuation / architecture scout within the compact support-bridge frontier.** ABI-214 is a bounded exploratory Candidate, not a promotion claim and not a late-improving request.

## Hypothesis

Recent ABI-209/211 broad support bridges were too expensive, and their compact repairs ABI-210/212 were feasible but did not recover enough precision/connectivity discipline. ABI-212 in particular completed safely but appeared to trade line continuity for broader support cues. ABI-214 tests whether a compact ASPP decoder can improve the same frontier by removing the broad coarse-support map and using only local signed-detail plus horizontal/vertical/diagonal thin-line continuity agreement as a bounded residual feature cue.

The hypothesis is limited to candidate-local model architecture. It does not change data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, coordinate inputs, training loop behavior, scheduler policy, resource placement, or prediction retention.

## Comparison Target

Primary comparison target: ABI-212 `run_20260904_172606_3f797b`, the resource-safe compact line-preserving coarse-support branch, which reached capped `val/filtered_dice` 0.3875 at epoch 12 with MIT/Google filtered Dice 0.3759/0.4172, precision 0.4170, recall 0.3618, connectivity 0.3235, and filtered predicted-positive fraction 0.003144.

Secondary targets: ABI-210 `run_20260904_152018_ce1309` as the compact spectral-ridge support reference, ABI-207/208 as directional-message-passing recall/precision tradeoff scouts, ABI-201/202 as the stronger cross-scale directional-consensus ASPP reference, and ABI-184 as the precision/connectivity and positive-area-discipline reference.

## Expected Effect

A useful Result should complete finitely under the exploratory cap and show whether removing broad support expansion improves thin-line precision/connectivity without collapsing recall. Desired evidence is higher connectivity and/or precision than ABI-212 while staying near ABI-212 aggregate/source filtered Dice and positive-area fraction, or a cleaner tradeoff than ABI-207/208 that combines bounded recall with better continuity. A negative but informative Result would show that the compact bridge loses too much recall or source balance without coarse support, motivating a broader architecture family or trusted evaluation/calibration frontier rather than another local support bridge.

## Implementation Sketch

Start from the resource-safe ABI-212 compact full-spectral BTD+SZA ASPP decoder: approved `abi_16ch_plus_sza` inputs, normalized GOES ABI channels 1-16, deterministic ABI-channel-derived thermal BTD planes, normalized/cosine Solar Geometry features, learned 1x1 spectral mixture, signed local/mid-scale detail stems, compact residual encoder, ASPP context, full-scale skip fusion, line-aware refinement, and `mask_logits`, `line_logits`, and `centerline_logits` outputs.

Replace ABI-212's `LinePreservingCoarseSupportBridge` with a `ThinLineContinuityBridge`. The new bridge projects signed-detail features, computes depthwise horizontal and vertical context plus diagonal no-wrap shifted context, gates those orientation features by feature-space agreement, and applies only a zero-initialized bounded residual back to the decoder features. It does not predict a foreground-support target, does not threshold or mask features, does not perform morphology, does not implement Artifact Filters, and does not use longitude/latitude or any unapproved inputs.

Keep the manifest choices unchanged from ABI-212: trusted `bce_dice`, trusted `combined_source_balanced`, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, provider-derived Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02, exploratory `max_epochs: 12`, and constant scheduler policy. No `budget_request.yaml` is included.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.02, AdamW, learning rate 0.0003, batch size 4, manifest `max_epochs: 12`, and constant scheduler policy.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, budget approval, effective epoch limit, and prediction retention.
- Candidate code defines model architecture only and contains no data loading, custom losses, custom metrics, Artifact Filters, postprocessing, thresholding, runtime downloads, filesystem persistence, Candidate-owned scheduling, or coordinate features.

## Budget Requested

One sequential representative capped exploratory Run: at most 1,024 training and validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, 12 effective epochs, the 3,600-second exploratory Docker timeout, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant scheduler policy, disabled early stopping, and pinned A100 execution through the Harness. No late-improving budget is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and the Run remains within the trusted exploratory resource envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. The continuation is promising if it improves ABI-212 precision/connectivity or ABI-207/208 continuity tradeoffs while staying close to ABI-212 aggregate/source filtered Dice, or if it reaches a late-improving, non-collapsed trajectory near the exploratory budget ceiling.

## Fallback/Next Decision

If ABI-214 fails validation or smoke because of the new bridge, classify and repair only the candidate-local implementation while preserving the thin-line-continuity hypothesis. If it completes but regresses aggregate/source Dice, recall, and connectivity without improving precision or predicted-positive discipline, do not repeat this compact bridge unchanged and broaden to a different architecture family, trusted loss/data policy, or evaluation/calibration request. If it completes near ABI-212 while improving connectivity or precision, write a Research Note and consider whether late-improving continuation or whole-validation diagnostics are justified by the trajectory and source-stratified metrics.
