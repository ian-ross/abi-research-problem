# ABI-295 compact early evidence-calibrated detail U-Net syntax repair

## Classification

Repair Candidate for ABI-294 after `run_20260914_000407_7232d1` smoke-failed with Harness-recorded `candidate_bug`: an `IndentationError` on `model.py` line 278. ABI-295 preserves ABI-294's hypothesis, comparison target, manifest policy, and architecture, changing only the Python indentation defect that prevented smoke import.

## Hypothesis

Recent C4/recall-calibrator work repeatedly traded compact high-precision connected predictions against broader recall. ABI-293 proposed that early feature-level evidence calibration might recover true contrail logits more cleanly than late uncertain-logit support, but the implementation was too slow to produce capped Result evidence. ABI-294 compacted that mechanism to test whether calibrated encoder skips with bounded detail, line-context, and reliability features can complete under the exploratory budget. ABI-295 keeps that same hypothesis and repairs the syntax defect so the compact mechanism can be evaluated.

## Comparison Target

Primary comparisons are ABI-293 for resource feasibility and ABI-292/ABI-283 for the recent single-frame C4/calibration precision-recall trade-off. Secondary comparisons are ABI-249 as the compact high-precision C4 comparator, ABI-279/280 as recall-bridge comparators, and ABI-202 as the aggregate whole-validation reference.

## Expected Effect

Expected success is first resource feasibility: static validation, smoke, and a completed finite 12-epoch capped Run within the exploratory wall-clock budget. Scientific success would be capped filtered Dice and source-stratified behavior closer to ABI-283/249 than ABI-292 while preserving or improving recall relative to compact C4 states without broad low-connectivity clutter. A useful mixed result would show whether early skip calibration changes the precision/recall/connectivity trade-off once implemented at a safe cost.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza` tensors.
- Build normalized ABI, ABI-channel-derived thermal BTD planes, Solar Geometry Input features, and a smaller learned 1x1 channel mixer.
- Use a compact U-Net with base width 32 rather than ABI-293's width 40.
- Keep bounded evidence-calibration blocks on encoder skips, but reduce separable line-context kernels from 15 to 11 pixels.
- Remove ABI-293's duplicate full-resolution `highres_cal` block; retain the high-resolution detail stem and fuse it with the decoder before the calibrated evidence head.
- Repair ABI-294's accidental over-indentation of `self.final_project` without altering the intended architecture.
- Emit trusted `mask_logits`, `line_logits`, and `centerline_logits` outputs for Harness-owned primary and auxiliary losses.

## Contract Features Used

ABI-295 uses only allowlisted `abi_16ch_plus_sza` input, `combined_source_balanced` sampling, `all_target_frames` frame selection, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 4, 12 exploratory epochs, and trusted Line plus Centerline auxiliary targets with weighted BCE. The manifest declares repair lineage to ABI-294's candidate-bug smoke failure. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling, augmentation transforms, thresholds, postprocessing, coordinates, resource scheduling, or training lifecycle behavior.

## Budget Requested

Default exploratory budget only: capped provider-selected samples, 12 epochs, batch size 4, constant learning rate, disabled early stopping, and trusted A100 execution under the active Workspace Configuration. No late-improving budget is requested.

## Success Criteria

Continue this compact early-calibration branch only if the Run completes, remains finite and non-collapsed, and gives source-informative metrics with a trade-off better than ABI-292: higher filtered Dice and connectivity at similar or better recall, or a compact precision/connectivity state that materially improves recall relative to ABI-283/249. Best epoch near epoch 12 is not sufficient for late36 unless the trajectory is improving and the metric trade-off is competitive.

## Fallback/Next Decision

If ABI-295 smoke-fails again with a candidate bug, classify the exact defect before deciding whether a second repair is worthwhile. If it runs but still times out or approaches the wall-clock limit without useful metrics, stop this exact early-calibration design as resource-infeasible under the exploratory policy and broaden to a lighter architecture family or a non-C4/non-calibration mechanism. If it completes but repeats ABI-292's broad low-connectivity clutter or compact underprediction, do not submit an unchanged continuation; pivot to a different mechanism such as temporal evidence sharpening or a simpler dual-evidence calibration head.
