# ABI-327 temporal five-frame change-salience C4 line-state late36

## Classification

Family-development continuation in the provider-owned temporal C4 line-state branch. This is a close but mechanism-changing continuation after ABI-324/325/326 diagnostics, not a promotion claim and not an unchanged late36 rerun.

## Hypothesis

ABI-324 remains the best balanced temporal C4 comparator after temporal-eligible diagnostics: it reduced negative-patch clutter and improved aggregate/source Dice versus ABI-311, but it did not broadly repair MIT positive-patch undercoverage. ABI-325 showed that useful positive-tail evidence exists in decoder/detail/line-state features, but broad reinjection increased clutter and hurt connectivity. ABI-326 then showed that a simple selective tail guard can recover some compactness but gives up too much recall and still does not restore connected-line behavior.

ABI-327 tests a different timing for the repair. Instead of another final-head residual or full-resolution tail reinjection/guard, it moves temporal support earlier into the five-frame stem. The model derives learned temporal-change salience from center-vs-inner-neighbor motion, center-vs-outer-neighbor motion, before/after temporal slope, and the center-vs-attended temporal gap. That salience gates the early C4 orientation line state before the encoder pyramid, so true changing/persistent thin-line evidence can shape all decoder scales while background disagreement is still controlled by ABI-324's detail-consensus head. This remains differentiable architecture logic only and does not implement temporal lookup, thresholding, morphology, postprocessing, Artifact Filters, custom losses, metrics, data loading, sampling, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Comparison Target

Primary temporal-eligible capped comparisons are ABI-324 as the balanced temporal C4 aggregate/connectivity comparator, ABI-326 as the failed selective-tail guard, ABI-325 as the positive-tail repair but clutter diagnostic, ABI-311 as the five-frame persistence/contrast parent, ABI-306 as compact high-precision temporal C4, ABI-309 as broad recall-heavy temporal C4, and ABI-223 as temporal-attention connectivity comparator. ABI-327 is temporal-eligible capped feasibility evidence only and is not whole Working Validation Split promotion evidence against ABI-202/249.

## Expected Effect

A useful Result should show that earlier change-salience gating is a better control point than ABI-325/326 final-tail mechanisms. Desired evidence includes one or more of:

- filtered Dice or MIT filtered Dice at or above ABI-324 without ABI-325-scale predicted-positive broadening;
- fixed-threshold recall or positive-tail behavior improved versus ABI-324 while precision/Google Dice remain closer to ABI-324 than ABI-325;
- connectivity restored toward ABI-324/223 rather than ABI-326's weak connected-line state;
- smaller negative-patch clutter than ABI-325 if a temporal-eligible failure-bucket Evaluation is later justified; or
- a finite late36 trajectory showing stable source-informative trade-offs rather than the oscillating final-head residual behavior of ABI-325/326.

A negative Result would indicate that the current five-frame temporal C4 family cannot selectively exploit temporal-change salience without either under-recalling or weakening connectivity, supporting a broader move to different temporal attention/alignment, modern backbone, or trusted policy directions.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza_temporal` tensors with trusted offsets `[-2, -1, 0, 1, 2]` and `temporal_eligible_center` selection.
- Reuse ABI-324 finite ABI/Solar Geometry Input normalization, approved-channel BTD construction, five-frame persistence/contrast temporal attention, early C4 orientation-consensus line state, compact encoder/decoder, ASPP context, line-state scale injectors, high-resolution directional context, and detail-consensus mask/Line/Centerline head.
- Add an early change-salience path inside `TemporalLineStateStem`:
  - build frame embeddings for all five trusted temporal offsets;
  - compute differentiable center-vs-inner and center-vs-outer motion features, before/after temporal slope, and center-vs-attended temporal gap;
  - project those features into a bounded salience state;
  - gate salience using appearance and persistence/contrast change embeddings;
  - use the gated salience as one input to the C4 line seed and as an attenuated support term in the early line state.

## Contract Features Used

ABI-327 uses only allowlisted `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` frame selection, allowlisted offsets `[-2, -1, 0, 1, 2]`, trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets with weighted BCE. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling policies, augmentation transforms, thresholds, postprocessing, temporal lookup, frame repair, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Request the approved `late_improving` budget: 36 epochs, 10,800-second late-improving timeout, batch size 2, constant learning rate, and disabled early stopping under the active Workspace Configuration. Parent evidence is ABI-324 (`run_20260916_184108_954ec7`), ABI-311 (`run_20260915_015552_1ac51f`), and ABI-326 (`run_20260917_002229_d43b7a`): all finite/resource-safe five-frame temporal C4 Runs with late-selected or late-relevant checkpoints and the exact undercoverage/clutter/connectivity failure sequence motivating this early-salience continuation.

## Success Criteria

Continue or diagnose this branch only if ABI-327 completes, remains finite/non-collapsed/source-informative, and shows a useful trade-off against ABI-324/325/326: especially improving MIT/positive-tail recall or connectivity without broadening the predicted-positive footprint and negative-patch clutter toward ABI-325. A future temporal-eligible Evaluation Request would be justified if capped aggregate/source metrics suggest change-salience gating may repair positive tails or connectivity while preserving ABI-324 compactness.

## Fallback/Next Decision

If the Run fails due to a candidate bug, repair only if the fix preserves this early change-salience C4 line-state hypothesis and comparison targets. If resource usage is too high, reduce salience/gate width rather than changing Harness-owned resource policy. If it completes but regresses to ABI-325/309-like clutter, ABI-326-like low connectivity, or ABI-306-like under-recall, stop this exact temporal C4 salience-gating branch and broaden to a materially different temporal attention/alignment mechanism, modern lightweight backbone, or other contract-compliant frontier.
