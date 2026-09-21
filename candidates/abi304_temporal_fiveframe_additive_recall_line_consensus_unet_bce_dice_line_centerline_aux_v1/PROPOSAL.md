# ABI-304 temporal five-frame additive recall line-consensus U-Net

## Classification

Family-development continuation. ABI-304 remains inside the trusted temporal-input family, but it changes mechanism relative to ABI-291 and ABI-300: it uses the allowlisted five-frame window for learned additive recall and line-consensus support, not hard persistence, hard agreement, subtractive clutter vetoes, Candidate-owned thresholds, or postprocessing.

## Hypothesis

Recent temporal Runs show two recurring failure modes. ABI-291's five-frame persistence attention was compact/high-precision but under-recalled. ABI-300's three-frame evidence-sharpening head also became conservative and failed to preserve ABI-223/238 temporal-attention precision/connectivity. ABI-296/299 local correlation recovered recall but widened predictions and did not solve connected-line organization.

ABI-304 tests whether five-frame temporal attention can use short-window and long-window temporal differences as feature evidence while preserving a center-frame residual and adding only small bounded positive support from line/detail/scale consensus. The intended mechanism is to recover fixed-threshold recall and MIT/source balance without hard temporal-veto underprediction or broad local-correlation clutter.

This is ordinary differentiable architecture logic over provider-visible temporal tensors. It is not Candidate-owned thresholding, morphology, postprocessing, a custom loss, a metric, an Artifact Filter, sample selection, temporal lookup, or data loading.

## Comparison Target

Primary temporal-eligible comparison targets are ABI-223 (`run_20260908_154531_8c7e2b`), ABI-238 (`run_20260911_004137_f54c45`), and ABI-285 (`run_20260913_100333_a250df`). Immediate mechanism comparisons are ABI-291 five-frame persistence, ABI-296 local temporal correlation, ABI-299 temporal correlation line-continuity, and ABI-300 temporal evidence sharpening.

ABI-304 will produce capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to full Working Validation Split Results.

## Expected Effect

A useful ABI-304 result does not need to beat ABI-223/238/285 immediately. It should complete under the exploratory budget, remain finite and non-collapsed, and show at least one of:

- filtered recall above ABI-300 and ABI-291 without a severe precision/connectivity collapse;
- filtered Dice near ABI-296/299 while showing a smaller footprint or better connectivity trade-off;
- improved source balance, especially MIT temporal-eligible Dice, relative to ABI-300's conservative operating point;
- predicted-positive fraction between ABI-291's compact under-recall mode and ABI-296/299's broad local-correlation footprints; or
- a late, source-informative trajectory that justifies a mechanism-preserving follow-up.

A negative but useful result would show that five-frame additive support still moves along the same temporal precision/recall/connectivity trade-off, motivating a different temporal continuity mechanism or a non-temporal pivot.

## Implementation Sketch

- Consume only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted offsets `[-2, -1, 0, 1, 2]` and trusted `temporal_eligible_center` selection.
- Build per-frame normalized ABI, approved-channel BTD, scaled Solar Geometry, and cos(Solar Geometry) features.
- Use a shared per-frame projection and learned per-pixel attention across five frame embeddings, with a center-frame residual gate.
- Add short/long temporal-difference features (`center - mean(-1,+1)`, `center - mean(-2,+2)`, forward/backward differences, and center-neighbor absolute differences) as architecture-internal features.
- Decode with a compact U-Net/ASPP backbone and high-resolution directional line context.
- Emit `mask_logits`, `line_logits`, and `centerline_logits`. The final mask head adds only bounded learned line/detail/multiscale support; it does not own thresholding or filtering.

## Contract Features Used

ABI-304 uses only allowlisted `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` frame selection, allowlisted temporal offsets `[-2, -1, 0, 1, 2]`, trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, 12 exploratory epochs, and trusted Line plus Centerline auxiliary targets with weighted BCE. Candidate source does not implement temporal lookup, cache reads, missing-neighbor repair, data loading, target construction, losses, metrics, Artifact Filters, sampling policies, augmentation transforms, thresholds, postprocessing, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Default exploratory budget only: capped provider-selected records, 12 epochs, batch size 2, constant learning rate, disabled early stopping, and A100 execution under the active Workspace Configuration. No late-improving budget is requested because the five-frame additive recall head changes the mechanism and should first demonstrate finite/resource behavior and early scientific value.

## Success Criteria

Continue temporal family development if ABI-304 completes, remains finite and source-informative, and improves the recall/precision/connectivity compromise relative to ABI-300/291 or closely approaches ABI-296/299 while preserving a plausible footprint. A late-improving continuation would require a best checkpoint near epoch 12, non-degenerate predicted-positive fractions, source-informative temporal-eligible MIT/Google metrics, and a trajectory suggesting under-training rather than plateau, collapse, or oscillatory trade-off.

## Fallback/Next Decision

If the Run fails due to a candidate bug, repair only if the fix preserves this five-frame additive-recall hypothesis and comparison target. If it is resource-infeasible, reduce head width/branches rather than changing data or Harness-owned policy. If it completes but repeats ABI-291/300 conservative low-recall behavior or ABI-296/299 broad low-connectivity clutter, stop this exact five-frame additive head and broaden toward a different temporal continuity mechanism, a non-C4 line-continuity design, or a different calibration architecture within the contract.
