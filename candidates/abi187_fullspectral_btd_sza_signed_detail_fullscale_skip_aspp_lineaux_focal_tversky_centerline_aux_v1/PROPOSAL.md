# ABI-187 Full-Spectral BTD+SZA Signed-Detail Full-Scale Skip ASPP Line-Aux Focal-Tversky Centerline Auxiliary v1

## Hypothesis

ABI-184 established a strong precision/connectivity operating point for the signed-detail full-scale skip ASPP branch with trusted Line plus Centerline auxiliary supervision, but whole-validation diagnostics showed a fixed-threshold recall and MIT-positive-patch deficit. A controlled switch from trusted `bce_dice` to trusted `focal_tversky` may recover recall if the direct Line Target head and signed-detail full-scale skip architecture constrain the otherwise clutter-prone focal-Tversky expansion seen in the centerline-only ABI-172 branch.

## Comparison Target

Primary comparison is ABI-184 (`run_20260902_213856_2c04ac`) as the whole-validation-tested precision/connectivity reference and ABI-183 (`run_20260902_204128_bba815`) as the matched 12-epoch Line plus Centerline auxiliary parent. Secondary comparisons are ABI-181 (`run_20260902_150611_cbbf35`) as the current whole-validation aggregate filtered-Dice reference, ABI-172 (`run_20260901_225502_53acd2`) as the centerline-only focal-Tversky negative reference, and ABI-068 (`run_20260828_010836_4ccc77`) as a focal-Tversky line-family source-balance comparator.

## Expected Effect

The desired effect is higher filtered recall and MIT filtered Dice than ABI-184/183 while retaining materially better precision and connectivity than ABI-172. A useful result would show that focal-Tversky can be paired with explicit Line plus Centerline supervision to soften ABI-184 conservative mask logits without converting the branch into high-positive-area clutter.

## Implementation Sketch

Reuse the ABI-183/ABI-184 PyTorch model: normalized GOES ABI channels 1-16 plus Solar Geometry Input, deterministic thermal BTD planes computed only from provider-approved ABI channels, signed local/mid-scale detail streams, compact residual encoder, ASPP context, decoder, full-scale skip fusion, line-aware refinement, and `mask_logits`, `line_logits`, and `centerline_logits` heads. Keep auxiliary target declarations and weights unchanged. Change only `training.loss` in `manifest.yaml` from `bce_dice` to `focal_tversky`.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`
- Input mode: `abi_16ch_plus_sza`; longitude and latitude are not candidate inputs
- Output form: `mask_logits`
- Trusted auxiliary targets: `line` -> `line_logits` with `weighted_bce` weight 0.01; `centerline` -> `centerline_logits` with `weighted_bce` weight 0.02
- Trusted primary loss: `focal_tversky`
- Trusted data policy: `combined_source_balanced` sampling, `all_target_frames` frame selection, `random_mirroring` augmentation
- Training: AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning rate, disabled early stopping by workspace policy

Candidate code does not implement or redefine provider/Harness-owned data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, primary or auxiliary losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

## Budget Requested

Exploratory/default budget: 12 epochs, batch size 4, 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, constant learning rate, and the configured Docker training timeout. No late-improving budget is requested for this first focal-Tversky Line plus Centerline branch.

## Success Criteria

This is a family-development continuation, not an immediate promotion candidate. Useful evidence would include finite non-collapsed training, resource usage below the 25M-parameter smoke ceiling and timeout, aggregate filtered Dice near the ABI-183/184 band, filtered recall at least meaningfully above ABI-184, MIT filtered Dice or MIT filtered recall improved versus ABI-184/183, and connectivity/precision not collapsing toward the ABI-172 focal-Tversky failure mode. A particularly strong result would approach or exceed ABI-181 aggregate filtered Dice while preserving a connectivity advantage over ABI-181.

## Fallback/Next Decision

If the Run is non-finite, collapses, or repeats ABI-172-style low-precision/low-connectivity positive-area expansion, stop this exact focal-Tversky Line plus Centerline branch and return to BCE-Dice calibration or a broader architecture/data-policy frontier. If it improves recall but loses too much connectivity, use it as diagnostic evidence rather than promotion evidence. If it is finite, source-balanced, non-collapsed, and still improving at epoch 12 with competitive precision/connectivity, consider a later late-improving continuation under the approved budget-request path.
