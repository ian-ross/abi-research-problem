# ABI-326 temporal five-frame selective tail consensus guard late36

## Classification

Family-development continuation in the provider-owned temporal C4 line-state branch. This is a close but mechanism-changing continuation after ABI-324/325 diagnostics, not a promotion claim and not an unchanged late36 rerun.

## Hypothesis

ABI-324 remains the best balanced temporal C4 comparator: it improved ABI-311 aggregate/source Dice, precision, compactness, and aggregate connectivity while reducing negative-patch clutter. ABI-325 then answered a narrower diagnostic question: feature-level reinjection from decoder, center-frame detail, and temporal C4 line-state evidence genuinely reduced positive-patch low-recall tails and improved MIT positive behavior, but it was too blunt. The cost was a broader footprint, more negative-patch clutter, lower precision, lower Google Dice, and worse aggregate connectivity.

ABI-326 tests whether ABI-325's useful tail evidence can be kept only when it is more selective. It replaces the broad `PositiveTailEvidenceReinjector` with a `SelectiveTailConsensusGuard` before the existing detail-consensus head. The guard projects the same decoder, center-detail, and early C4 line-state features into shared memory, but applies a smaller bounded residual only when decoder/detail, decoder/line-state, and decoder/memory align above a neutral feature baseline and learned background guards do not flag disagreement. This remains model architecture only and does not implement thresholding, morphology, connected-component logic, postprocessing, Artifact Filtering, custom losses, metrics, data loading, temporal lookup, sampling, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Comparison Target

Primary temporal-eligible capped comparisons are ABI-324 as the balanced temporal C4 aggregate/connectivity comparator, ABI-325 as the positive-tail repair but clutter diagnostic variant, ABI-311 as the previous five-frame persistence/contrast parent, ABI-306 as the compact high-precision temporal C4 comparator, ABI-309 as the recall-heavy broad-footprint diagnostic, and ABI-223 as the temporal-attention connectivity comparator. ABI-326 is temporal-eligible capped feasibility evidence only and is not whole Working Validation Split promotion evidence against ABI-202/249.

## Expected Effect

A useful Result should recover part of ABI-325's positive-tail/MIT recall gain while moving back toward ABI-324's compact operating point. Desired evidence includes one or more of:

- MIT filtered Dice or positive-tail recall above ABI-324 without ABI-325-scale negative-patch clutter;
- filtered predicted-positive pixels closer to ABI-324 than ABI-325 at comparable aggregate Dice;
- filtered precision and Google Dice materially recovered versus ABI-325;
- filtered connectivity closer to ABI-324/223 while preserving some of ABI-325's low-recall-tail repair; or
- a stable late36 trajectory showing that selective feature agreement is a better control knob than broad residual reinjection.

A negative Result would show that the temporal C4 detail/line-state tail evidence cannot be made selective enough within this branch, supporting a broader move toward different temporal alignment/change, attention, or policy mechanisms.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza_temporal` tensors with trusted offsets `[-2, -1, 0, 1, 2]` and `temporal_eligible_center` selection.
- Reuse ABI-324/325 finite ABI/Solar Geometry Input normalization, approved-channel BTD construction, five-frame persistence/contrast temporal stem, early C4 orientation-consensus line state, compact encoder/decoder, ASPP context, line-state scale injectors, high-resolution directional context, and detail-consensus trusted Line/Centerline auxiliary outputs.
- Replace ABI-325's broad reinjector with `SelectiveTailConsensusGuard`:
  - project full-resolution decoder, center-frame temporal-stem detail, and early line-state features into shared memory;
  - compute differentiable feature-agreement signals for decoder/detail, decoder/line-state, and decoder/memory support;
  - require support above a neutral feature-alignment baseline and learned low-disagreement guards before any residual is applied;
  - reduce residual amplitude relative to ABI-325 so the block supports tails without repainting broad negative patches.

## Contract Features Used

ABI-326 uses only allowlisted `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` frame selection, allowlisted temporal offsets `[-2, -1, 0, 1, 2]`, trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets with weighted BCE. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling policies, augmentation transforms, thresholds, postprocessing, temporal lookup, frame repair, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Request the approved `late_improving` budget: 36 epochs, 10,800-second late-improving timeout, batch size 2, constant learning rate, and disabled early stopping under the active Workspace Configuration. Parent evidence is ABI-325 (`run_20260916_212722_d66d93`), ABI-324 (`run_20260916_184108_954ec7`), and ABI-311 (`run_20260915_015552_1ac51f`): all finite/resource-safe temporal C4 Runs with informative late-selected checkpoints and the exact failure-mode sequence motivating this selective continuation.

## Success Criteria

Continue or diagnose this branch only if ABI-326 completes, remains finite/non-collapsed/source-informative, and shows a useful trade-off against ABI-324/325: especially retaining ABI-325 positive-tail or MIT recall gains while reducing negative-patch clutter, improving precision/Google balance, or restoring connectivity toward ABI-324/223. A future temporal-eligible Evaluation Request would be justified if capped aggregate/source metrics suggest the selective guard may have kept ABI-325's tail repair with lower clutter.

## Fallback/Next Decision

If the Run fails due to a candidate bug, repair only if the fix preserves this selective tail consensus hypothesis and comparison targets. If resource usage is too high, reduce guard width or residual complexity rather than changing Harness-owned resource policy. If it completes but still regresses to ABI-325/309-like clutter, ABI-306-like under-recall, or weak connectivity, stop this exact temporal C4 feature-reinjection branch and broaden to a materially different temporal alignment/change mechanism, modern backbone, trusted data/loss/augmentation policy request, or other contract-compliant frontier.
