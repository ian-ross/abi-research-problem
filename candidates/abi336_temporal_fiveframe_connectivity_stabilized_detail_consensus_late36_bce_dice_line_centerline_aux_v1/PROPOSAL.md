# ABI-336 temporal five-frame connectivity-stabilized detail consensus late36

## Classification

Family-development continuation in the provider-owned five-frame temporal C4 line-state branch. ABI-336 is a close but mechanism-changing continuation of ABI-324, not a promotion claim and not an unchanged late36 rerun of ABI-324/325/326/328.

## Hypothesis

ABI-324 is the strongest balanced recent temporal C4 Result on the capped temporal-eligible validation population: it improved ABI-311 aggregate/source Dice, precision, footprint, and connectivity. Its trajectory still showed the central unresolved failure mode. Epoch 27 was the best balanced checkpoint, while epoch 30 had higher precision/connectivity but lower recall and Dice; subsequent ABI-325/326/328 variants moved recall/footprint but did not preserve ABI-324-like connected compactness.

ABI-336 tests whether the final architecture-internal evidence construction can explicitly couple recall support to learned directional continuity. The head adds a bounded positive residual only where decoder mask evidence, center-frame temporal detail, trusted Line/Centerline logits, temporal line-state support, and learned directional continuity all agree. It also applies a small learned isolation veto against decoder-positive but line-discontinuous evidence. This remains ordinary differentiable model architecture over provider-supplied tensors; it is not thresholding, morphology, connected-component analysis, postprocessing, an Artifact Filter, a custom loss, a metric, data loading, temporal lookup, sample selection, coordinates, or resource control.

## Comparison Target

Primary capped temporal-eligible comparisons are ABI-324 as the balanced detail-consensus temporal C4 comparator, ABI-325 as the positive-tail recall diagnostic, ABI-328 as the soft-shift alignment diagnostic, ABI-311 as the five-frame C4 parent, ABI-306 as the compact high-precision temporal C4 comparator, ABI-309 as the broad recall-heavy temporal C4 diagnostic, and ABI-223 as the temporal-attention connectivity comparator. ABI-336 is temporal-eligible capped feasibility evidence only and is not whole Working Validation Split promotion evidence against ABI-202/249.

## Expected Effect

A useful Result should preserve ABI-324's compact/source-balanced operating point while improving one or more of:

- filtered connectivity or positive-patch continuity at comparable filtered predicted-positive footprint;
- MIT filtered Dice or fixed-threshold recall without ABI-325/309-scale precision loss or negative-patch clutter broadening;
- aggregate filtered Dice relative to ABI-324/311, or a differentiated tie with better connectivity; or
- late-budget trajectory evidence that high-connectivity compact states and higher-recall states are less decoupled than in ABI-324/328.

A negative Result would show that final-head continuity gating is insufficient and that further temporal C4 head work should stop unless driven by new diagnostics or a materially different temporal alignment/change mechanism.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza_temporal` tensors with trusted offsets `[-2, -1, 0, 1, 2]` and `temporal_eligible_center` selection.
- Reuse ABI-324's finite ABI/Solar Geometry Input normalization, approved-channel BTD construction, five-frame persistence/contrast temporal stem, early C4 orientation-consensus line state, compact encoder/decoder, ASPP context, scale line-state injectors, and high-resolution directional context.
- Replace ABI-324's `DetailConsensusStabilizedHead` with `ConnectivityStabilizedDetailConsensusHead`:
  - project decoder, center-detail, and early line-state features into a shared evidence space;
  - build a learned directional continuity feature using depthwise horizontal/vertical strip filters plus dilated diagonal convolutions;
  - emit trusted primary `mask_logits` plus trusted `line_logits` and `centerline_logits` auxiliary outputs;
  - add a bounded recall residual only under learned mask/Line/Centerline/detail/line-state/continuity agreement; and
  - subtract a small bounded isolation veto for decoder-positive but line-discontinuous clutter.

## Contract Features Used

ABI-336 uses only allowlisted `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` frame selection, allowlisted temporal offsets `[-2, -1, 0, 1, 2]`, trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets with weighted BCE. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling policies, augmentation transforms, thresholds, postprocessing, temporal lookup, frame repair, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Request the approved `late_improving` budget: 36 epochs, 10,800-second late-improving timeout, batch size 2, constant learning rate, and disabled early stopping under the active Workspace Configuration. Parent evidence is ABI-324 (`run_20260916_184108_954ec7`), ABI-325 (`run_20260916_212722_d66d93`), and ABI-328 (`run_20260917_055012_ba7890`). These are finite/resource-safe five-frame temporal C4 Runs whose selected or diagnostic behavior depended on late-epoch evidence and directly motivate the connectivity/recall coupling tested here.

## Success Criteria

Continue or diagnose this branch only if ABI-336 completes, remains finite/non-collapsed/source-informative, and shows a useful improvement or differentiated trade-off against ABI-324/325/328: especially higher connectivity at comparable footprint, improved MIT/positive-tail recall without broad clutter, or an aggregate/source Dice tie with better connected-line evidence. A future temporal-eligible Evaluation Request would be justified only if capped aggregate/source/connectivity metrics suggest that the mechanism may have preserved ABI-324 compactness while repairing positive-tail undercoverage.

## Fallback/Next Decision

If the Run fails due to a candidate bug, repair only if the fix preserves this connectivity-stabilized detail-consensus hypothesis and comparison targets. If resource usage is too high, reduce only the final head's directional-continuity width or veto complexity rather than changing Harness-owned resource policy. If it completes but regresses to ABI-325/309-like clutter, ABI-306-like under-recall, or weak connectivity, stop this exact temporal C4 final-head branch and broaden to a materially different temporal attention/alignment/change mechanism, modern lightweight backbone, trusted policy direction, or failure-bucket-driven evaluation.
