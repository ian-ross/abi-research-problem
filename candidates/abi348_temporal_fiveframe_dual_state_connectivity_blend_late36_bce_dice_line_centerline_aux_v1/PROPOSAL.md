# ABI-348 temporal five-frame dual-state connectivity blend late36

## Classification

Family-development continuation in the provider-owned five-frame temporal C4/detail-consensus branch. This is a close but mechanism-changing continuation of ABI-324/337/344, not a promotion claim and not an unchanged late36 rerun.

## Hypothesis

ABI-324 remains the balanced five-frame temporal C4/detail-consensus comparator: strong aggregate temporal-eligible filtered Dice, reasonable fixed-threshold recall, compact footprint, and better connectivity than most temporal C4 variants. Recent recall-repair attempts (ABI-325, ABI-341, ABI-344) show a consistent failure mode: positive-tail and MIT recall can be improved, but additive residual/sidecar heads broaden predictions, raise negative-patch clutter, and weaken connected-line continuity. ABI-337 also showed that data-policy orientation preservation alone does not solve the compact-connectivity versus recall decoupling.

ABI-348 tests a different final evidence construction. Instead of adding a recall residual to ABI-324-style logits, it predicts two architecture-internal states: a compact connected anchor and a recall candidate. A learned convex blend lets the recall candidate replace the anchor only where decoder/detail/temporal-line evidence, Line logits, and Centerline logits agree and a learned disagreement guard remains low. The hypothesis is that a blend can preserve ABI-324-like compactness/connectivity better than additive sidecars while recovering some positive-tail recall.

This remains model architecture only. It does not implement thresholding, morphology, connected-component logic, postprocessing, Artifact Filtering, custom losses, metrics, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Comparison Target

Primary temporal-eligible capped comparisons are ABI-324 as the balanced five-frame temporal C4/detail-consensus comparator, ABI-337 as the no-mirroring control, ABI-344 and ABI-325 as broad recall-sidecar/positive-tail diagnostics, ABI-306 as the compact high-precision temporal C4 comparator, and ABI-223 as the temporal-attention connectivity comparator. ABI-348 is temporal-eligible capped feasibility evidence only and is not whole Working Validation Split promotion evidence against ABI-202/249.

## Expected Effect

A useful Result would improve the ABI-324/337 positive-tail or MIT undercoverage trade-off without repeating ABI-344's broad-footprint connectivity loss. Success signals include one or more of:

- aggregate filtered Dice within the ABI-324/337 band while improving recall or MIT filtered Dice;
- filtered connectivity closer to ABI-324 than ABI-344/325 at comparable or smaller footprint;
- fewer predicted-positive pixels than ABI-344/325 at similar recall; or
- a late36 trajectory showing that blended compact/recall states are more stable than the oscillatory additive sidecar states.

A negative Result would show that final-state blending is not enough to decouple the temporal C4 family's compact-connectivity and recall modes, supporting a broader move to a materially different temporal alignment/attention or non-temporal architecture mechanism.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza_temporal` tensors with trusted offsets `[-2, -1, 0, 1, 2]` and `temporal_eligible_center` selection.
- Reuse ABI-324's finite ABI/Solar Geometry Input normalization, approved-channel BTD construction, five-frame temporal stem, C4 orientation-consensus line state, compact encoder/decoder, ASPP context, line-state scale injectors, and high-resolution directional context.
- Replace ABI-324's additive `DetailConsensusStabilizedHead` with `DualStateConnectivityBlendHead`:
  - build decoder, center-detail, and temporal-line support features;
  - emit Line and Centerline auxiliary logits from the compact anchor state;
  - predict compact anchor logits and a bounded recall-candidate lift;
  - compute a learned blend gate from anchor/recall probabilities, Line/Centerline evidence, and detail/line alignment;
  - compute a learned disagreement guard from anchor-recall, anchor-Line, anchor-Centerline, detail, and line disagreements;
  - return a guarded convex blend of anchor and recall logits rather than an additive residual.

## Contract Features Used

ABI-348 uses only allowlisted `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` frame selection, allowlisted temporal offsets `[-2, -1, 0, 1, 2]`, trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets with weighted BCE. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling policies, augmentation transforms, thresholds, postprocessing, temporal lookup, frame repair, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Request the approved `late_improving` budget: 36 epochs, 10,800-second late-improving timeout, batch size 2, constant learning rate, and disabled early stopping under the active Workspace Configuration. Parent evidence is ABI-324 (`run_20260916_184108_954ec7`), ABI-337 (`run_20260917_201833_57b081`), and ABI-344 (`run_20260918_105020_e806bb`), all finite/resource-safe five-frame temporal Runs with informative selected checkpoints well beyond the exploratory ceiling.

## Success Criteria

Continue or diagnose this branch only if ABI-348 completes, remains finite/non-collapsed/source-informative, and shows a useful differentiated trade-off against ABI-324/337/344: especially ABI-324-like compactness/connectivity with higher recall or MIT Dice, or ABI-344-like positive-tail recovery with materially lower footprint and better connectivity. A temporal-eligible Evaluation Request would be justified only if capped metrics suggest such a near-frontier trade-off.

## Fallback/Next Decision

If the Run fails due to a candidate bug, repair only if the fix preserves the dual-state blend hypothesis and comparison targets. If resource usage is too high, reduce head width/gate complexity rather than changing Harness-owned resource policy. If it completes but repeats ABI-344-like clutter, ABI-337-like source/connectivity regression, or ABI-306-like under-recall, stop this exact final-head branch and broaden to a materially different temporal alignment/change, temporal attention, modern backbone, or trusted policy direction.
