# ABI-303 C4 centerline-protected recall bridge U-Net

## Classification

Family-development continuation in the C4/orientation-prior branch. This is a mechanism-changing exploratory follow-up after ABI-283 and ABI-292, not a promotion candidate and not an unchanged late36 continuation.

## Hypothesis

ABI-249 remains the compact high-precision C4 comparator, ABI-279 showed that bounded C4 line/detail residuals can raise recall/connectivity but cost precision and Google/source balance, and ABI-283 found a cleaner compact high-connectivity state that underpredicted true contrails. ABI-292 then showed that a late soft-band recall calibrator loosened the compact C4 mode without preserving connectivity or precision.

ABI-303 tests whether recall support should be protected by an explicit centerline/detail stream rather than by strict cross-scale consensus or broad uncertain-logit support. The model keeps the resource-profiled C4 steerable line-context U-Net body, but replaces the mask head with a centerline-protected recall bridge: a learned centerline stream receives C4 line context, high-resolution signed detail, and multiscale decoder support; a recall gate adds small bounded centerline/detail/line residuals; a separate precision gate and small disagreement veto keep support compact. The intended mechanism is to recover true thin contrails at the fixed 0.5 threshold while preserving more of ABI-283's compact connected-line evidence than ABI-292 did.

This is ordinary differentiable architecture logic. It is not Candidate-owned thresholding, morphology, postprocessing, a custom loss, a metric, an Artifact Filter, sample selection, or data loading.

## Comparison Target

Primary capped comparisons are ABI-283 cross-scale consensus C4, ABI-292 soft-band C4 recall calibrator, ABI-249 compact C4, ABI-279 C4 dual-evidence recall bridge, and ABI-202 aggregate whole-validation reference. ABI-280 is secondary context for selective consensus trade-offs. ABI-303 will produce capped representative feasibility evidence only, not full-data promotion evidence.

## Expected Effect

A useful ABI-303 result does not need to beat ABI-202. It should complete under the exploratory budget, remain finite and non-collapsed, and show at least one of:

- filtered recall above ABI-283 while losing substantially less precision/connectivity than ABI-292;
- filtered Dice near ABI-249/279/283 with a more balanced precision/recall/connectivity trade-off;
- MIT/source balance improvement over ABI-283's under-recall mode without ABI-280/292-style broad clutter;
- predicted-positive fraction between ABI-283's compact footprint and ABI-279/280's broader recall footprints, with source-informative finite metrics; or
- a late exploratory trajectory that justifies a future late-improving request because the new centerline-protected head is still improving rather than oscillating or collapsing.

A negative but useful result would show that even centerline-protected C4 recall support still moves along the same compact-underprediction versus broad-clutter trade-off, motivating a temporal or non-C4 frontier pivot.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza` tensors.
- Normalize ABI channels 1-16, derive approved-channel thermal BTD planes, include Solar Geometry Input and a small learned 1x1 channel mixture.
- Reuse the compact signed-detail U-Net, ASPP bottleneck, and C4 rotation-shared line-context module from the recent resource-profiled C4 branch.
- Replace the ABI-283/292 final mask head with a centerline-protected recall bridge:
  - `line_context` from C4 steerable orientation context;
  - `region_features`, `detail_features`, and `multiscale_features` from full-resolution and decoder/context support;
  - `centerline_features` from line context, detail features, signed detail, and multiscale support;
  - a precision gate from line/context/multiscale agreement and disagreement;
  - a recall gate from region, line, detail, centerline, and multiscale evidence;
  - bounded residual additions from line, centerline, detail, and multiscale logits; and
  - a smaller learned disagreement veto than ABI-283 to reduce underprediction.
- Emit `mask_logits`, `line_logits`, and `centerline_logits` for trusted Harness losses.

## Contract Features Used

ABI-303 uses only allowlisted `abi_16ch_plus_sza` input, trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 4, 12 exploratory epochs, and trusted Line plus Centerline auxiliary targets with weighted BCE. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling policies, augmentation transforms, thresholds, postprocessing, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Default exploratory budget only: capped provider-selected records, 12 epochs, batch size 4, constant learning rate, disabled early stopping, and A100 execution under the active Workspace Configuration. No late-improving budget is requested because the centerline-protected recall bridge changes the head mechanism and should first demonstrate finite/resource behavior and early scientific value.

## Success Criteria

Continue this branch only if ABI-303 completes, remains finite and source-informative, and improves the C4 recall/precision/connectivity compromise relative to ABI-283/292 or closely approaches ABI-249/279 while preserving a plausible compact footprint. A late-improving continuation would require a best checkpoint near epoch 12, non-degenerate predicted-positive fractions, source-informative MIT/Google metrics, and a trajectory suggesting under-training rather than plateau, collapse, or oscillatory trade-off.

## Fallback/Next Decision

If the Run fails due to a candidate bug, repair only if the fix preserves this centerline-protected C4 recall hypothesis and comparison target. If it is resource-infeasible, reduce head width/branches rather than changing data or Harness-owned policy. If it completes but repeats ABI-283 underprediction or ABI-292 broad low-connectivity recall, stop this exact C4 head design and broaden toward temporal evidence sharpening, non-C4 line-continuity mechanisms, or a different calibration architecture within the contract.
