# ABI-232 full-spectral BTD+SZA spectral-regime MoE U-Net late36

## Hypothesis

A longer trusted training budget can let ABI-231's compact spectral/Solar Geometry Input-regime gated mixture-of-experts U-Net convert its final-epoch improvement and high-connectivity/low-positive-fraction behavior into better recall and source-balanced overlap. This is a **family-development continuation** of the underexplored spectral/SZA-state mixture-of-experts direction, not a promotion claim and not a same-family tweak to ABI-202 or the temporal window-attention branch.

## Comparison Target

Primary comparison is the parent ABI-231 (`run_20260910_155936_362435`, capped best `val/filtered_dice` 0.371985 at epoch 12, MIT 0.355799, Google 0.413787, filtered connectivity 0.398515). Broader context is the current single-frame frontier ABI-202 (`run_20260904_043143_ee0005`, capped best `val/filtered_dice` 0.427570; whole-validation filtered Dice 0.4312) and the temporal-family late36 frontier ABI-223 (`run_20260908_154531_8c7e2b`, capped best `val/filtered_dice` 0.419776). Same-budget recent scouts ABI-226 through ABI-231 remain comparison context for family allocation, but ABI-232 is judged mainly on whether the ABI-231 MoE branch benefits from approved late training.

## Expected Effect

The late-improving budget should determine whether ABI-231's soft spectral/SZA regime routing was undertrained rather than intrinsically recall-limited. A positive result would improve aggregate filtered Dice, MIT filtered Dice, or filtered recall over ABI-231 while preserving noncollapsed source behavior and the parent's useful connectivity/compact-positive-area signature. Even if it does not beat ABI-202 or ABI-223, it can justify bounded MoE family development if it shows a finite upward trajectory, stronger source balance, or diagnostically distinct precision/connectivity tradeoffs.

## Implementation Sketch

The candidate keeps the ABI-231 architecture unchanged. `model.py` consumes provider-supplied `abi_16ch_plus_sza` tensors only, normalizes ABI channels using fixed bounded profile-derived constants, derives approved-channel brightness-temperature-difference planes, derives scaled/cosine Solar Geometry Input features, and applies a learned 1x1 channel mixer. A three-expert stem processes the resulting features with different receptive fields while global pooled ABI/SZA-derived context plus a per-pixel 1x1 gate produce soft expert weights. The fused features feed a compact GroupNorm U-Net with ASPP bottleneck, high-resolution signed-detail bridge, and mask/Line/Centerline output heads.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza`; no longitude/latitude, temporal cache access, Dataset Source identity, scene identity, or route/location priors.
- Output form: primary `mask_logits` plus trusted auxiliary `line_logits` and `centerline_logits`.
- Data policy: provider-owned `combined_source_balanced` sampling, `all_target_frames`, and trusted `random_mirroring` augmentation.
- Training policy: trusted `bce_dice` loss, AdamW optimizer, constant learning rate, batch size 4, manifest `max_epochs: 12`, and separate Harness-validated `late_improving` budget request for 36 effective epochs.
- Auxiliary targets: provider-derived Line Target and Centerline Target with `weighted_bce` losses at 0.01 and 0.02.
- Candidate code is architecture-only and does not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, filesystem probing, or resource scheduling.

## Budget Requested

Request the approved `late_improving` budget via `budget_request.yaml`: up to 36 effective epochs, configured 10,800-second wall-clock budget, batch size 4, constant learning rate, disabled early stopping, configured 1,024-record cap per Dataset Source/split, four fixed `first_n` prediction artifacts, and sequential execution under the Harness-owned concurrency cap. If the request is denied, fall back to the exploratory budget and treat that bounded Run as the valid result.

## Success Criteria

The run is operationally successful if it completes finite smoke/training/validation under resource limits and remains noncollapsed with source-informative MIT and Google filtered metrics. Scientific success versus the parent is an improvement in capped `val/filtered_dice`, MIT filtered Dice, or filtered recall without losing the high-connectivity/compact-positive-fraction signature. Strong evidence would approach the ABI-223 temporal late36 frontier or narrow the gap to ABI-202 while retaining source balance. A hard failure, non-finite state, persistent all-negative/all-positive predictions, or a convincing late plateau/divergence below ABI-231 would stop this exact late36 MoE branch.

## Fallback/Next Decision

If ABI-232 improves over ABI-231 and remains late-improving, consider a focused MoE continuation that explicitly targets MIT recall or, if close to ABI-223/ABI-202, a trusted whole-validation diagnostic request. If ABI-232 is finite but clearly plateaus or regresses, classify this exact late36 MoE branch as a negative result and broaden to a materially different differentiable Hough/Radon-style line-voting scout. If it fails by contract or candidate bug, create a repair only if the original MoE hypothesis and comparison target are preserved. If it fails by resource exhaustion, reduce width or expert count rather than implementing candidate-owned scheduling.
