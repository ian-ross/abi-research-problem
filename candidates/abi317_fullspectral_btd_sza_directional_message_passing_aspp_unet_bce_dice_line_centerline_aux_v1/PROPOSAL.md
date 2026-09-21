# ABI-317 directional message-passing ASPP U-Net

## Classification

Family-development continuation in the single-frame full-spectral BTD+Solar Geometry Input line-continuity branch. This is a mechanism-changing exploratory follow-up after ABI-202/249/279/302/303, not a promotion candidate and not an unchanged late36 continuation.

## Hypothesis

Recent temporal C4 decoder/head-calibration continuations did not stabilize typical connected-line recovery, and ABI-303 showed that another late C4 protected-recall head mainly returned to compact underprediction. ABI-202 remains the aggregate reference, while ABI-249 remains the compact high-precision C4 comparator.

ABI-317 tests a non-C4, architecture-internal directional message-passing bridge: decoder/detail evidence is propagated along horizontal, vertical, and diagonal line directions over multiple distances, then gated by cross-scale agreement with stem/full-scale features and local signed detail. The intended mechanism is to improve connected thin-line continuity and MIT/positive-patch support without broadening into recall-head clutter or moving thresholding/postprocessing into Candidate code.

This is ordinary differentiable model architecture. It is not Candidate-owned thresholding, morphology, connected-component logic, postprocessing, a custom loss, a metric, an Artifact Filter, sample selection, or data loading.

## Comparison Target

Primary capped comparisons are ABI-202 cross-scale directional-consensus ASPP, ABI-249 compact C4 steerable line context, ABI-279/280 C4 recall-bridge variants, ABI-302 trusted clDice loss-policy continuation, and ABI-303 centerline-protected C4 bridge. ABI-317 will produce capped representative feasibility evidence only, not whole-validation promotion evidence.

## Expected Effect

A useful result should complete under the exploratory budget, remain finite/non-collapsed/source-informative, and show at least one of:

- connectivity or recall closer to ABI-202/279 than ABI-249 without ABI-302-style precision collapse;
- filtered Dice near the single-frame C4/ASPP comparators with better MIT/source balance or connected-line evidence;
- a predicted-positive fraction between compact C4 underprediction and broad recall-head footprints; or
- a late exploratory trajectory that justifies a future late-improving request for this mechanism.

A negative result would show that shift-based directional line propagation is another unstable precision/recall surface, motivating a broader family pivot.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza` tensors.
- Normalize ABI channels 1-16, derive approved-channel thermal BTD planes, include Solar Geometry Input, and learn a small 1x1 channel mixture.
- Use an ABI-202-style signed-detail U-Net encoder/decoder with ASPP context and full-scale skip fusion.
- Replace the final cross-scale consensus bridge with a `DirectionalMessagePassingContinuityBridge`:
  - build a decoder/detail seed from full-resolution decoder, high-resolution signed detail, and broad context;
  - aggregate seed features in four signed directions using no-wrap shifts at distances 1, 2, 4, 8, and 16 pixels;
  - learn orientation weighting, cross-scale gates, and detail-protection gates;
  - fuse decoder, detail, stem, full-scale, gated line messages, and line-agreement features through residual blocks;
  - add only a bounded learned residual before the standard line-aware refinement.
- Emit `mask_logits`, `line_logits`, and `centerline_logits` for trusted Harness losses.

## Contract Features Used

ABI-317 uses only allowlisted `abi_16ch_plus_sza` input, trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 4, 12 exploratory epochs, and trusted Line plus Centerline auxiliary targets with weighted BCE. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling policies, augmentation transforms, thresholds, postprocessing, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Default exploratory budget only: capped provider-selected records, 12 epochs, batch size 4, constant learning rate, disabled early stopping, and A100 execution under the active Workspace Configuration. No late-improving budget is requested because this message-passing bridge first needs bounded resource and early scientific evidence.

## Success Criteria

Continue this branch only if ABI-317 completes, remains finite and source-informative, and improves or usefully differentiates the recall/precision/connectivity trade-off against ABI-202/249/279/302/303. A late-improving continuation would require a best checkpoint near epoch 12, non-degenerate predicted-positive fractions, source-informative MIT/Google metrics, and a trajectory suggesting under-training rather than plateau, collapse, or oscillatory trade-off.

## Fallback/Next Decision

If the Run fails due to a candidate bug, repair only if the fix preserves this directional message-passing hypothesis and comparison target. If resource usage is too high, reduce bridge width or distances rather than changing Harness-owned data/resource policy. If it completes but merely repeats compact underprediction or broad low-precision recall, stop this exact message-passing bridge and broaden to a different architecture family or trusted policy direction.
