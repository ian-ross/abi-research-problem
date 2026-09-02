# ABI-148 full-spectral BTD+SZA ASPP/detail decoder low-LR BCE-Dice continuation

## Hypothesis

ABI-130 established that provider-approved Solar Geometry Input can move the ASPP/detail BCE-Dice branch toward better default-threshold recall and source balance, and its whole-validation diagnostic confirmed that the capped signal survives beyond the representative subset. However, ABI-130's late-epoch trajectory was oscillatory and its gain came with lower precision/connectivity and more negative-patch clutter than ABI-126. Recent SZA-aware BCE-Dice micro-architecture continuations, including ABI-147, did not improve this tradeoff. ABI-148 tests whether lowering the fixed AdamW learning rate from `0.0003` to `0.0002`, with architecture and trusted data/loss policy unchanged from ABI-130, stabilizes the BCE-Dice calibration and recovers some precision/connectivity without reverting to ABI-126-style MIT under-recall.

## Proposal classification

Family-development continuation. This is a controlled training-policy continuation of the SZA-aware ASPP/detail BCE-Dice branch, not a promotion claim from capped evidence. It deliberately broadens away from further stem/ridge/detail micro-architecture edits after ABI-147 by changing only the optimizer learning rate within the existing Harness-owned resource and scheduler limits.

## Comparison Target

Primary comparison target: ABI-130 (`run_20260831_121006_7d24be`), the strongest SZA-aware ASPP/detail BCE-Dice branch and a whole-validation-tested near-tie to ABI-068.

Secondary references:

- ABI-126 (`run_20260831_085615_d05ab3`) for the non-SZA ASPP/detail precision/connectivity operating point.
- ABI-068 (`run_20260828_010836_4ccc77`) as the local capped aggregate filtered-Dice and MIT-recall reference.
- ABI-143 (`run_20260831_224534_27b73d`) as the nearby SZA-aware BCE-Dice ridge branch with more recall but weaker connectivity.
- ABI-147 (`run_20260901_021228_9ca4b9`) as negative evidence against additional SZA-aware ridge-ASPP stem fusion.

## Expected Effect

The lower learning rate should reduce the epoch-to-epoch oscillation seen in ABI-130 while preserving the same SZA-aware raw+BTD evidence path. Useful behavior would be a filtered predicted-positive fraction close to ABI-130, improved filtered precision or connectivity, and no major loss of MIT filtered recall. Because the architecture, input mode, trusted loss, auxiliary target, sampling traversal, and augmentation policy remain unchanged, differences should isolate whether the SZA-aware ASPP/detail branch benefits from a less aggressive fixed update size under the 12-epoch cap.

## Implementation Sketch

- Reuse ABI-130's provider-approved `abi_16ch_plus_sza` input path: normalized ABI channels 1-16, deterministic thermal BTD planes from approved ABI channels, normalized SZA, cosine SZA, and a learned 1x1 mixture.
- Keep the ABI-130 detail/context stem, compact encoder, ASPP bottleneck, decoder skip fusion, high-resolution detail branch, line-aware refinement, primary `mask_logits` head, and provider-derived `centerline_logits` auxiliary head.
- Keep trusted `bce_dice` primary loss, trusted Centerline Target `weighted_bce` auxiliary loss at weight 0.02, trusted combined source-balanced sampling, and trusted random mirroring.
- Change only `training.learning_rate` from `0.0003` to `0.0002` under the allowlisted AdamW optimizer and constant learning-rate scheduler.

## Contract Features Used

Candidate code defines architecture only. It does not implement or modify data loading, Leakage-Safe Split construction, capped-record selection, sampling traversal, augmentation transforms, target derivation, loss functions, metrics, thresholding, Artifact Filters, Baseline Segmenters, prediction retention, training loops, resource placement, retry policy, or Run lifecycle. All BTD and solar-geometry features are computed only from provider-approved ABI+SZA tensors. No longitude, latitude, raw dataset path, external file access, network access, pretrained weight download, custom persistence, candidate-owned calibration threshold, or postprocessing is used.

## Budget Requested

Use the active trusted Workspace Configuration ceilings: 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, constant learning rate, disabled early stopping, four fixed `first_n` retained predictions, 25M parameter smoke ceiling, A100 execution, and sequential Run execution under the Agent-visible concurrency cap of one.

## Success Criteria

ABI-148 is useful if it remains finite and non-collapsed and achieves at least one of:

- matches ABI-130 aggregate filtered Dice within about 0.005 while improving filtered precision or filtered connectivity;
- improves ABI-130 MIT filtered Dice or MIT filtered recall without increasing filtered predicted-positive fraction beyond ABI-143's more permissive ridge branch;
- lands near the ABI-068/ABI-130 capped reference band with a clearer precision/connectivity tradeoff than ABI-143 or ABI-147.

Hard stop conditions for this exact low-learning-rate branch are non-finite training, contract/resource failure, persistent all-negative/all-positive predictions, clear under-training by epoch 12, or aggregate/source metrics materially below ABI-130 without a compensating precision/connectivity or calibration advantage.

## Fallback decision

If ABI-148 under-trains or merely reproduces ABI-130 without a useful precision/connectivity gain, stop this low-learning-rate ASPP/detail branch and broaden further away from SZA-aware BCE-Dice tuning. Reasonable next frontiers would be a different augmentation/data policy, an in-contract calibration-head architecture with a stronger mechanism than ABI-128/ABI-137, or a distinct architecture family focused on source-robust thin-line continuity rather than more SZA-aware detail-stem modifications.
