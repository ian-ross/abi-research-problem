# ABI-324 temporal five-frame detail-consensus stabilized line-state late36

## Classification

Family-development continuation in the provider-owned temporal C4 line-state branch. This is a close but mechanism-changing continuation of ABI-311, not a promotion claim and not an unchanged ABI-306/309/311 late36 rerun.

## Hypothesis

ABI-311's five-frame persistence/contrast temporal C4 stem is the best balanced temporal C4 comparator so far: it improves aggregate temporal-eligible filtered Dice and connectivity versus ABI-306 while avoiding ABI-309's heavy negative-patch clutter. Its temporal-eligible diagnostics still show the unresolved failure mode: MIT and positive-patch undercoverage, with typical positive-patch connectivity not clearly improved over compact comparators.

ABI-324 tests whether the ABI-311 operating point can be stabilized toward connected recall by changing the final architecture-internal evidence construction. Instead of another late broad line-support head or output-only logit floor, the head fuses full-resolution decoder evidence, center-frame temporal-stem detail, and early C4 line-state support. It adds only a bounded non-negative residual where learned mask, Line, Centerline, center-detail, and temporal line-state agreement gates all support the pixel, while a learned conflict guard attenuates disagreement. This remains model architecture only and does not implement thresholding, morphology, connected-component logic, postprocessing, Artifact Filtering, custom losses, metrics, data loading, temporal lookup, sampling, coordinates, or resource scheduling.

## Comparison Target

Primary temporal-eligible capped comparisons are ABI-311 as the balanced five-frame persistence/contrast temporal C4 comparator, ABI-306 as the compact high-precision temporal C4 comparator, ABI-309 as the recall-heavy temporal C4 diagnostic variant, and ABI-223 as the temporal-attention connectivity comparator. ABI-324 is temporal-eligible capped feasibility evidence only and is not whole Working Validation Split promotion evidence against ABI-202/249.

## Expected Effect

A useful Result should preserve ABI-311's low negative-patch clutter profile while improving one or more of:

- MIT filtered Dice or MIT positive-patch undercoverage proxy metrics through higher fixed-threshold recall;
- aggregate filtered recall without ABI-309-scale false-positive footprint broadening;
- filtered connectivity or positive-patch continuity relative to ABI-311/306; or
- a stable late36 trajectory showing that center-detail plus temporal-consensus residuals reduce ABI-311's oscillatory precision/recall trade-off.

A negative Result would show that ABI-311-style evidence cannot be improved by final evidence stabilization alone and that future temporal work should broaden away from temporal C4 head variants.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza_temporal` tensors with trusted offsets `[-2, -1, 0, 1, 2]` and `temporal_eligible_center` selection.
- Reuse ABI-311's finite ABI/Solar Geometry Input normalization, approved-channel BTD construction, five-frame persistence/contrast temporal stem, early C4 orientation-consensus line state, compact encoder/decoder, ASPP context, and line-state scale injectors.
- Replace ABI-311's `DualEvidenceRecallCalibratedHead` with `DetailConsensusStabilizedHead`:
  - project full-resolution decoder, temporal-stem detail, and early line-state features into a shared evidence space;
  - emit trusted primary `mask_logits` plus trusted `line_logits` and `centerline_logits` auxiliary outputs;
  - compute learned agreement gates from mask/Line/Centerline logits, decoder-detail alignment, and decoder-line-state alignment;
  - compute a learned conflict guard from disagreement features;
  - add a small bounded non-negative residual to `mask_logits` only where the learned agreement gates survive the guard.

## Contract Features Used

ABI-324 uses only allowlisted `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` frame selection, allowlisted temporal offsets `[-2, -1, 0, 1, 2]`, trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets with weighted BCE. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling policies, augmentation transforms, thresholds, postprocessing, temporal lookup, frame repair, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Request the approved `late_improving` budget: 36 epochs, 10,800-second late-improving timeout, batch size 2, constant learning rate, and disabled early stopping under the active Workspace Configuration. Parent evidence is ABI-311 (`run_20260915_015552_1ac51f`), ABI-306 (`run_20260914_124245_de843c`), and ABI-309 (`run_20260914_205014_1794f8`), all finite/resource-safe temporal C4 Runs whose informative checkpoints occurred well beyond the exploratory budget.

## Success Criteria

Continue or diagnose this branch only if ABI-324 completes, remains finite/non-collapsed/source-informative, and shows a useful improvement or differentiated trade-off against ABI-311/306/309: especially higher MIT/positive-tail recall without negative-patch clutter broadening, improved connectivity at comparable footprint, or stable late-budget convergence. A future temporal-eligible Evaluation Request would be justified only if capped aggregate/source metrics suggest that the mechanism may have repaired ABI-311's diagnosed MIT/positive-patch tail.

## Fallback/Next Decision

If the Run fails due to a candidate bug, repair only if the fix preserves this center-detail/temporal-consensus stabilization hypothesis and comparison targets. If resource usage is too high, reduce head width or residual-gate complexity rather than changing Harness-owned resource policy. If it completes but regresses to ABI-309-like clutter, ABI-306-like under-recall, or weak connectivity, stop this exact temporal C4 head-stabilization branch and broaden to a materially different temporal alignment/change mechanism, modern backbone, or trusted policy direction.
