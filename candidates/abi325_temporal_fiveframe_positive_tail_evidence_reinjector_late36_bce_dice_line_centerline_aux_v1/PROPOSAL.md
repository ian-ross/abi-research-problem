# ABI-325 temporal five-frame positive-tail evidence reinjector late36

## Classification

Family-development continuation in the provider-owned temporal C4 line-state branch. This is a close but mechanism-changing continuation of ABI-324, not a promotion claim and not an unchanged ABI-324 late36 rerun.

## Hypothesis

ABI-324 is the best balanced temporal C4 comparator so far on the temporal-eligible capped population: relative to ABI-311 it improved aggregate/source filtered Dice, precision, compactness, and aggregate connectivity. Its failure-bucket evaluation also showed the remaining failure mode clearly: the gain did not broadly repair complete positive-patch misses, low-recall positive tails, or the MIT positive-patch quality gap.

ABI-325 tests whether this positive-tail undercoverage can be attacked earlier than the output head while preserving ABI-324's reduced negative-patch clutter. Instead of adding another final logit floor, it inserts a full-resolution `PositiveTailEvidenceReinjector` between the decoder directional context and the detail-consensus head. The reinjector learns a shared memory from decoder features, center-frame temporal-stem detail, and early C4 line-state support, then applies a small bounded feature residual only where learned detail-line agreement and background guards support it. This remains model architecture only and does not implement thresholding, morphology, connected-component logic, postprocessing, Artifact Filtering, custom losses, metrics, data loading, temporal lookup, sampling, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Comparison Target

Primary temporal-eligible capped comparisons are ABI-324 as the new balanced temporal C4 aggregate/connectivity comparator, ABI-311 as the previous five-frame persistence/contrast parent, ABI-306 as the compact high-precision temporal C4 comparator, ABI-309 as the recall-heavy clutter diagnostic variant, and ABI-223 as the temporal-attention connectivity comparator. ABI-325 is temporal-eligible capped feasibility evidence only and is not whole Working Validation Split promotion evidence against ABI-202/249.

## Expected Effect

A useful Result should preserve ABI-324's compact footprint and negative-patch clutter improvements while improving one or more of:

- MIT filtered Dice or source balance through higher true-positive evidence;
- aggregate filtered recall without ABI-309-scale predicted-positive broadening;
- filtered connectivity or positive-patch continuity relative to ABI-324/311/306; or
- a stable late36 trajectory showing that feature-level reinjection reduces ABI-324's oscillatory precision/recall/connectivity trade-off.

A negative Result would show that ABI-324's remaining tail cannot be repaired by full-resolution feature reinjection and that future work should broaden away from temporal C4 decoder/head mechanisms toward a materially different temporal alignment/change architecture or other trusted policy direction.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza_temporal` tensors with trusted offsets `[-2, -1, 0, 1, 2]` and `temporal_eligible_center` selection.
- Reuse ABI-324's finite ABI/Solar Geometry Input normalization, approved-channel BTD construction, five-frame persistence/contrast temporal stem, early C4 orientation-consensus line state, compact encoder/decoder, ASPP context, line-state scale injectors, high-resolution directional context, and detail-consensus trusted Line/Centerline auxiliary outputs.
- Add `PositiveTailEvidenceReinjector` before the final head:
  - project full-resolution decoder, center-frame temporal-stem detail, and early line-state features into a shared evidence memory;
  - learn soft agreement features from decoder/detail alignment and decoder/line-state alignment;
  - learn a background guard from decoder-memory disagreement and low-support features;
  - add a bounded residual to decoder features before the existing detail-consensus head, rather than directly thresholding or postprocessing logits.

## Contract Features Used

ABI-325 uses only allowlisted `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` frame selection, allowlisted temporal offsets `[-2, -1, 0, 1, 2]`, trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets with weighted BCE. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling policies, augmentation transforms, thresholds, postprocessing, temporal lookup, frame repair, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Request the approved `late_improving` budget: 36 epochs, 10,800-second late-improving timeout, batch size 2, constant learning rate, and disabled early stopping under the active Workspace Configuration. Parent evidence is ABI-324 (`run_20260916_184108_954ec7`), ABI-311 (`run_20260915_015552_1ac51f`), and ABI-306 (`run_20260914_124245_de843c`), all finite/resource-safe temporal C4 Runs with informative late-selected checkpoints.

## Success Criteria

Continue or diagnose this branch only if ABI-325 completes, remains finite/non-collapsed/source-informative, and shows a useful improvement or differentiated trade-off against ABI-324/311/306/309: especially higher MIT/positive-tail recall without negative-patch clutter broadening, improved connectivity at comparable footprint, or stable late-budget convergence. A future temporal-eligible Evaluation Request would be justified only if capped aggregate/source metrics suggest the feature-level reinjector may have repaired ABI-324's diagnosed positive-tail failure mode.

## Fallback/Next Decision

If the Run fails due to a candidate bug, repair only if the fix preserves this feature-level positive-tail reinjection hypothesis and comparison targets. If resource usage is too high, reduce reinjector width or residual complexity rather than changing Harness-owned resource policy. If it completes but regresses to ABI-309-like clutter, ABI-306-like under-recall, or weak connectivity, stop this exact temporal C4 feature-reinjection branch and broaden to a materially different temporal alignment/change mechanism, modern backbone, or trusted policy direction.
