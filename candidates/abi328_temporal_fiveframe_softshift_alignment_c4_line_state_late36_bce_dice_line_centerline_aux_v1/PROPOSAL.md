# ABI-328 temporal five-frame soft-shift alignment C4 line-state late36

## Classification

Family-development continuation in the provider-owned temporal line-state branch. This is a mechanism-changing continuation after ABI-324/325/326/327; it is not a promotion claim and not an unchanged late36 rerun.

## Hypothesis

ABI-324 remains the best balanced local temporal C4 comparator, while ABI-325/326/327 show that final-head reinjection, selective tail guards, and early change-salience gating do not reliably combine MIT positive-tail recall, compactness, and connected-line continuity. ABI-327 in particular became a high-precision under-recall point, suggesting that merely gating early change features can suppress true temporal support.

ABI-328 tests a different temporal mechanism: before deriving the C4 line state, each non-center temporal frame is softly aligned to the center frame over a small local shift bank with zero-filled shifts. Aligned before/after differences and match confidence then seed the C4 line-state and encoder pyramid. The intended effect is to recover connected true-contrail evidence when neighboring frames are slightly displaced by advection, without broad full-resolution reinjection or Candidate-owned thresholds/postprocessing.

This remains differentiable architecture logic over provider-stacked temporal tensors only. It does not implement temporal lookup, cache access, frame selection, padding/repair of missing frames, data loading, target construction, thresholding, morphology, Artifact Filters, custom losses, metrics, sampling, augmentation, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Comparison Target

Primary capped temporal-eligible comparisons are ABI-324 as the balanced temporal C4 aggregate/connectivity comparator, ABI-327 as the failed early change-salience gate, ABI-326 as the failed selective-tail guard, ABI-325 as the positive-tail/clutter diagnostic, ABI-311 as the five-frame persistence/contrast parent, ABI-306 as compact high-precision temporal C4, ABI-309 as broad recall-heavy temporal C4, and ABI-223 as the temporal-attention connectivity comparator. ABI-328 is temporal-eligible capped feasibility evidence only and is not whole Working Validation Split promotion evidence against ABI-202/249.

## Expected Effect

A useful Result would show that local temporal alignment is a better control point than salience/reinjection gates. Desired evidence includes one or more of:

- filtered Dice or MIT filtered Dice near or above ABI-324 without ABI-325-scale footprint broadening;
- recall or positive-tail recovery versus ABI-324/327 while keeping precision and Google Dice closer to ABI-324 than ABI-325;
- connectivity restored toward ABI-324 or ABI-223, rather than ABI-326/327 weak connected-line behavior;
- predicted-positive pixels closer to ABI-324 than ABI-325/309; or
- a finite late36 trajectory showing source-informative alignment trade-offs that justify later diagnostics.

A negative Result would indicate that the current compact C4 temporal line-state family still cannot exploit five-frame displacement evidence safely, supporting a broader move to materially different temporal attention, modern backbone, or trusted policy directions.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza_temporal` tensors with trusted offsets `[-2, -1, 0, 1, 2]` and `temporal_eligible_center` selection.
- Reuse the finite ABI/Solar Geometry Input normalization, approved-channel BTD features, compact C4 line-state U-Net encoder/decoder, ASPP context, scale-wise line-state injectors, high-resolution directional context, and Line/Centerline auxiliary heads from the profiled temporal branch.
- Replace ABI-327's early change-salience gate with `SoftShiftTemporalAligner`:
  - project each trusted temporal frame to compact features;
  - for each non-center frame, score a shared local shift bank `(0,0), up, down, left, right` against the center feature using zero-filled shifts, not wraparound;
  - form an aligned neighbor as the softmax-weighted shifted feature and expose the maximum shift weight as confidence;
  - derive inner/outer aligned differences and before/after aligned changes;
  - fuse center, attended aligned neighbors, motion, and confidence into the C4 line seed and early encoder input.

## Contract Features Used

ABI-328 uses only allowlisted `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` frame selection, allowlisted offsets `[-2, -1, 0, 1, 2]`, trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets with weighted BCE.

## Budget Requested

Request the approved `late_improving` budget: 36 epochs, 10,800-second late-improving timeout, batch size 2, constant learning rate, and disabled early stopping under the active Workspace Configuration. Parent evidence is ABI-324 (`run_20260916_184108_954ec7`), ABI-327 (`run_20260917_031010_2dd7e6`), and ABI-326 (`run_20260917_002229_d43b7a`): all are finite/resource-profiled five-frame temporal C4 Runs, and their late-selected or late-active trajectories make a 12-epoch cap likely to truncate the comparison.

## Success Criteria

Continue or diagnose this branch only if ABI-328 completes, remains finite/non-collapsed/source-informative, and shows a useful trade-off against ABI-324/325/326/327, especially improving MIT/positive-tail recall or connectivity without broadening predicted-positive footprint and negative-patch clutter toward ABI-325/309. A temporal-eligible Evaluation Request would be justified later only if capped metrics suggest alignment may repair positive tails or connectivity while preserving ABI-324-like compactness.

## Fallback/Next Decision

If the Run fails due to a candidate bug, repair only if the fix preserves this soft-shift temporal-alignment hypothesis and comparison targets. If resource use is too high, reduce the shift bank or alignment width rather than changing Harness-owned resource policy. If it completes but regresses to ABI-325/309-like clutter, ABI-326/327-like low connectivity, or ABI-306-like under-recall, stop this exact soft-shift C4 branch and broaden to a materially different temporal attention/alignment mechanism, modern lightweight backbone, or other contract-compliant frontier.
