# ABI-231 full-spectral BTD+SZA spectral-regime MoE U-Net

## Hypothesis

A compact spectral/Solar Geometry Input-regime gated mixture-of-experts U-Net can improve source-balanced GOES ABI Contrail Segmentation by letting the model softly switch among approved-channel feature experts for reflective/thermal/illumination regimes, without using Dataset Source identity, scene identity, longitude/latitude, route/location priors, or candidate-owned postprocessing. This is a **family scout** for the underexplored spectral/SZA-state mixture-of-experts direction, not a same-family tweak to ABI-202 or the temporal window-attention branch.

## Comparison Target

Primary comparison is the current capped single-frame frontier ABI-202 (`run_20260904_043143_ee0005`, capped best `val/filtered_dice` 0.4276; whole-validation filtered Dice 0.4312) and the recent temporal-family capped frontier ABI-223 (`run_20260908_154531_8c7e2b`, capped best `val/filtered_dice` 0.4198). Scout allocation should also compare against recent finite temporal scouts ABI-226 through ABI-230 to decide whether broadening away from temporal attention is productive.

## Expected Effect

The learned MoE gate should improve threshold-stable precision/recall and Dataset Source balance by routing approved ABI+SZA/BTD features through different local/context experts when spectral contrast or illumination changes. Success may appear as a noncollapsed finite trajectory, improved Google or MIT source behavior relative to generic single-path scouts, better filtered precision at a similar predicted-positive fraction, or a primary-metric result close enough to warrant bounded family development. It is not required to beat ABI-202 on this first scout to remain scientifically useful.

## Implementation Sketch

The candidate consumes provider-supplied `abi_16ch_plus_sza` tensors only. `model.py` normalizes ABI channels using fixed bounded profile-derived constants, derives approved-channel brightness-temperature-difference planes, derives scaled/cosine Solar Geometry Input features, and applies a learned 1x1 channel mixer. A three-expert stem processes the resulting features with different receptive fields while global pooled ABI/SZA-derived context plus a per-pixel 1x1 gate produce soft expert weights. The fused features feed a compact GroupNorm U-Net with ASPP bottleneck, high-resolution signed-detail bridge, and mask/Line/Centerline output heads.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza`; no longitude/latitude or temporal cache access.
- Output form: primary `mask_logits` plus trusted auxiliary `line_logits` and `centerline_logits`.
- Data policy: provider-owned `combined_source_balanced` sampling, `all_target_frames`, and trusted `random_mirroring` augmentation.
- Training policy: trusted `bce_dice` loss, AdamW optimizer, constant learning rate, batch size 4, and 12 exploratory epochs.
- Auxiliary targets: provider-derived Line Target and Centerline Target with `weighted_bce` losses at 0.01 and 0.02.
- Candidate code is architecture-only and does not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, filesystem probing, or resource scheduling.

## Budget Requested

Use the default exploratory budget: 12 epochs, batch size 4, constant learning rate, disabled early stopping, configured 1,024-record cap per Dataset Source/split, configured 3,600-second wall-clock budget, and sequential execution under the Harness-owned concurrency cap. No `late_improving` budget is requested for this first MoE scout.

## Success Criteria

Treat the run as successful if it completes finite smoke/training/validation under resource limits and remains noncollapsed with source-informative MIT and Google filtered metrics. Strong positive evidence would be capped `val/filtered_dice` near or above 0.39 with no source collapse, or a distinctive precision/recall/source balance that suggests MoE-specific follow-up even if the aggregate metric trails ABI-202. A late finite trajectory with best checkpoint at epoch 12 may justify a later close-continuation budget request; a hard failure, non-finite state, persistent all-negative/all-positive predictions, or clear plateau/regression far below recent scouts would stop this exact branch.

## Fallback/Next Decision

If ABI-231 is finite but modest, compare its failure mode against ABI-223 and ABI-230 before deciding whether to develop MoE gates, request whole-validation diagnostics, or broaden again to a materially different long-range differentiable Hough/Radon-style voting module. If it fails by contract or candidate bug, create a repair only if the original MoE hypothesis and comparison target are preserved. If it fails by resource exhaustion, reduce width or expert count rather than implementing candidate-owned scheduling.
