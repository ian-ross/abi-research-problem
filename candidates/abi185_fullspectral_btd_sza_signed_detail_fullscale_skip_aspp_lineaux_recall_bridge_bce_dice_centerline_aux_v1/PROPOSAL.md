# ABI-185 Full-Spectral BTD+SZA Signed-Detail Full-Scale Skip ASPP Line-Aux Recall-Bridge BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-185 is a controlled architecture/calibration continuation from ABI-184 and ABI-181 in the signed-detail full-scale skip ASPP family. It is not a promotion claim and not an unchanged epoch extension. It tests an in-contract mechanism for combining ABI-184's line-supervised precision/connectivity with better fixed-threshold recall.

## Hypothesis

ABI-184's whole-validation evaluation showed that direct low-weight Line Target supervision produces a clean and connected operating point: whole-validation filtered precision 0.4893, connectivity 0.4763, and fewer negative-patch false positives than ABI-181. The weakness was under-recall, with whole-validation recall 0.3517 versus ABI-181's 0.3832 and more zero/low-recall positive patches, especially on MIT. A bounded feature-level recall bridge shared by the mask, line, and centerline heads should let trusted BCE-Dice and auxiliary supervision learn a less conservative fixed-threshold representation while preserving the line-connected structure that made ABI-184 useful.

This deliberately avoids another simple additive/bias logit-head repeat after ABI-155's negative result. The bridge acts before logits and is trained through all three trusted heads, but it performs no thresholding, postprocessing, Artifact Filtering, custom loss, target derivation, or sampling behavior.

## Comparison Target

Primary comparison target: ABI-184 `run_20260902_213856_2c04ac`, the late36 Line plus Centerline auxiliary branch. Capped best-validation metrics were filtered Dice 0.4066, MIT/Google filtered Dice 0.3879/0.4555, precision 0.4850, recall 0.3500, connectivity 0.4634, and filtered predicted-positive fraction 0.00261. Whole-validation metrics were filtered Dice 0.4093, MIT/Google filtered Dice 0.3898/0.4476, precision 0.4893, recall 0.3517, and connectivity 0.4763.

Aggregate comparison target: ABI-181 `run_20260902_150611_cbbf35`, the current whole-validation aggregate filtered-Dice reference. Whole-validation metrics were filtered Dice 0.4124, MIT/Google filtered Dice 0.3988/0.4395, precision 0.4466, recall 0.3832, and connectivity 0.3676. Secondary context includes ABI-183 `run_20260902_204128_bba815`, ABI-173 `run_20260901_234732_bd5917`, ABI-154 `run_20260901_071026_32d3ec`, ABI-068 `run_20260828_010836_4ccc77`, and canonical MCAST summaries.

## Expected Effect

A positive outcome would improve ABI-184's capped filtered recall and MIT filtered Dice without giving up most of its precision/connectivity advantage. The strongest useful outcome would approach ABI-181 aggregate and MIT filtered Dice while remaining materially above ABI-181 on connectivity and avoiding a large expansion in filtered predicted-positive fraction. A negative but informative outcome would show that ABI-184's direct line-supervised representation cannot be recall-calibrated by a shared feature bridge under BCE-Dice, steering future work toward loss/data-policy changes or a different architecture family rather than another line-auxiliary head tweak.

## Implementation Sketch

- Reuse the ABI-184 signed-detail full-scale skip ASPP decoder: normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized/cosine Solar Geometry Input features, learned spectral projection, signed local/mid-scale detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, and line-aware final refinement.
- Add `LineSupportedRecallBridge`, a bounded feature-level residual block after final refinement and before logits. It combines local high-frequency detail, horizontal/vertical line context, and smoothed context, then applies a trainable residual with scale clamped to `[0.0, 0.30]`.
- Feed the bridged features into `mask_logits`, `line_logits`, and `centerline_logits` so provider-derived Line and Centerline auxiliary targets supervise the same features that feed the mask head.
- Keep trusted manifest choices unchanged from ABI-184 except for no longer requesting late36: `abi_16ch_plus_sza`, `bce_dice`, `combined_source_balanced`, `random_mirroring`, Line Target auxiliary `weighted_bce` weight 0.01, Centerline Target auxiliary `weighted_bce` weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Do not implement Candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, scheduler policy, GPU placement, runtime downloads, pretrained weights, coordinate inputs, or external persistence.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` auxiliary outputs `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `line` with `weighted_bce` weight 0.01, auxiliary target `centerline` with `weighted_bce` weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.

## Budget Requested

One sequential exploratory representative capped Run: at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, maximum 12 epochs, 3,600-second Docker training wall-clock budget, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant scheduler policy, disabled early stopping, and Harness-owned GPU placement. No late-improving budget is requested for this first recall-bridge variant.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 remains inside the trusted resource envelope.
3. Primary and auxiliary losses, logits, gradients, parameters, metrics, and checkpoint state remain finite.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw/filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. Family-development success is met if ABI-185 improves ABI-184's recall and/or MIT filtered Dice while retaining materially higher connectivity than ABI-181 and without severe precision or predicted-positive-area regression. A final-epoch best checkpoint with finite, non-collapsed behavior would support a later late-improving budget request; capped results alone are not promotion evidence.

## Fallback/Next Decision

If ABI-185 improves recall/MIT Dice while preserving the ABI-184 connectivity/precision advantage, consider a later late-improving continuation only if the exploratory trajectory is still improving at epoch 12, or a whole-validation Evaluation Request if capped metrics look competitive. If it improves recall only by expanding false positives and losing connectivity, retain ABI-184 as the precision/connectivity reference and ABI-181 as the aggregate reference. If it plateaus below ABI-184 or repeats ABI-155's under-recall pattern, stop this exact recall-bridge branch and broaden to a different in-contract mechanism or architecture family. If it fails by contract, shape, numerical, resource, or lifecycle criteria, classify the failure before proposing any repair.
