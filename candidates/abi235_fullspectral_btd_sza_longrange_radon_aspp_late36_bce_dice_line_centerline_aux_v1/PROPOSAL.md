# ABI-235 full-spectral BTD+SZA long-range Radon ASPP late36

## Hypothesis

A longer trusted training budget can let ABI-234's differentiable low-resolution Radon-style long-line accumulation branch convert its final-epoch improvement into better recall and source-balanced overlap while preserving its compact-positive, high-precision, connected-line signature. This is a **family-development continuation** of the underexplored differentiable Hough/Radon-style line-accumulation direction, not a promotion claim and not another ABI-202 local support-gate tweak.

## Comparison Target

Primary comparison is the parent ABI-234 (`run_20260910_185443_f88be8`, capped best/final epoch 12 `val/filtered_dice` 0.381342, MIT 0.363530, Google 0.425620, filtered precision 0.451640, filtered recall 0.329981, filtered connectivity 0.386193). Broader context is the current single-frame frontier ABI-202 (`run_20260904_043143_ee0005`, capped best `val/filtered_dice` 0.427570; whole-validation filtered Dice 0.4312), temporal-family frontier ABI-223 (`run_20260908_154531_8c7e2b`, capped best `val/filtered_dice` 0.419776), and spectral/SZA-regime MoE late36 ABI-232 (`run_20260910_163616_4f7416`, capped best `val/filtered_dice` 0.400942). ABI-235 is judged mainly on whether the ABI-234 Radon branch benefits from approved late training.

## Expected Effect

The late-improving budget should distinguish an undertrained line-accumulation scout from an intrinsically recall-limited fusion design. A positive result would improve aggregate filtered Dice, MIT filtered Dice, or filtered recall over ABI-234 without collapsing predictions or sacrificing the parent's precision/connectivity strengths. Even if it remains below ABI-202 or ABI-223, improvement over ABI-234 with finite upward trajectory would justify one further recall-preserving Radon-family change; plateau/divergence would stop this exact late36 branch.

## Implementation Sketch

The candidate keeps the ABI-234 architecture unchanged. `model.py` consumes provider-supplied `abi_16ch_plus_sza` tensors only, normalizes ABI channels using fixed bounded profile-derived constants, derives approved-channel brightness-temperature-difference planes, derives scaled/cosine Solar Geometry Input features, and applies a learned 1x1 channel mixer. A compact GroupNorm U-Net with ASPP bottleneck and high-resolution signed-detail bridge is fused with a differentiable low-resolution Radon-style module that accumulates horizontal, vertical, diagonal, anti-diagonal, shallow, and steep oriented support. The model emits `mask_logits`, `line_logits`, and `centerline_logits`.

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

The run is operationally successful if it completes finite smoke/training/validation under resource limits and remains noncollapsed with source-informative MIT and Google filtered metrics. Scientific success versus the parent is an improvement in capped `val/filtered_dice`, MIT filtered Dice, or filtered recall while keeping filtered precision/connectivity within the diagnostically useful range of ABI-234. Strong evidence would narrow the gap to ABI-232/ABI-223 or approach ABI-202 while retaining source balance. A hard failure, non-finite state, persistent all-negative/all-positive predictions, or a convincing late plateau/divergence below ABI-234 would stop this exact late36 Radon branch.

## Fallback/Next Decision

If ABI-235 improves over ABI-234 and remains late-improving, consider one controlled recall-preserving Radon fusion change such as a center-detail bypass or weaker Radon residual gate, or request trusted whole-validation diagnostics if it approaches the current frontier. If ABI-235 is finite but clearly plateaus or regresses, classify this exact late36 Radon continuation as negative and broaden to a materially different modern backbone or calibration/agreement family. If it fails by contract or candidate bug, create a repair only if the original Radon hypothesis and comparison target are preserved. If it fails by resource exhaustion, reduce width or line-support cost rather than implementing candidate-owned scheduling.
