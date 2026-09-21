# ABI-319 temporal shift-bank C4 alignment-confidence line U-Net

## Classification

Family-development continuation in the temporal line-continuity/evidence-sharpening branch. This is a mechanism-changing exploratory follow-up after ABI-315's shift-bank alignment scout and ABI-311's five-frame temporal C4 comparator; it is not a promotion candidate and not an unchanged late36 continuation.

## Hypothesis

ABI-315 showed that differentiable small-displacement temporal alignment is executable and can briefly create high-connectivity states, but the selected checkpoint did not stabilize connected thin-line evidence or beat temporal C4 comparators. ABI-311 remains the best balanced temporal C4 comparator, with cleaner negative-patch clutter and better aggregate/connectivity than ABI-306/309, but its temporal-eligible diagnostic still shows MIT-heavy positive-patch undercoverage.

ABI-319 tests whether the missing coupling is alignment confidence plus orientation consensus. It keeps ABI-315's provider-owned three-frame shift-bank alignment and center-frame detail path, then adds an alignment-confidence-gated C4 orientation line-state before the encoder and head. The line state is used only where the learned shift-bank has confident previous/next support, so it should stabilize the early connectivity signal while protecting center-frame evidence when temporal alignment is ambiguous. The candidate does not implement Candidate-owned thresholding, morphology, connected-component logic, postprocessing, Artifact Filtering, custom losses, metrics, data loading, sample selection, coordinate use, temporal lookup, or resource scheduling.

## Comparison Target

Primary capped temporal-eligible comparisons are ABI-315 as the shift-bank scout, ABI-311 as the balanced five-frame temporal C4 comparator, ABI-306 as the compact high-precision temporal C4 comparator, ABI-309 as the recall-heavy temporal C4 comparator, and ABI-223/238 as temporal-attention continuity comparators. ABI-319 produces capped temporal-eligible feasibility evidence only, not full Working Validation Split promotion evidence.

## Expected Effect

A useful Result should complete under the exploratory budget, remain finite and source-informative, and show at least one of:

- higher connectivity than ABI-315 while preserving or improving its final-epoch filtered Dice;
- recall closer to ABI-311/309 without the broad ABI-309 false-positive footprint;
- better MIT filtered Dice or smaller source gap than ABI-315; or
- a stable late exploratory trajectory that justifies considering a mechanism-preserving late-improving continuation.

A negative Result would show that local shift-bank alignment plus confidence-gated C4 line consensus still fails to convert temporal support into fixed-threshold connected Contrail Masks, pushing the campaign away from this shift-bank family.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza_temporal` tensors with trusted temporal-eligible center selection and offsets `[-1, 0, 1]`.
- Normalize ABI channels 1-16 per frame, derive approved-channel BTD planes, and include per-frame Solar Geometry Input.
- Encode previous, center, and next frames with a shared stem; align previous/next features to the center frame through ABI-315's no-wrap nine-shift differentiable shift bank.
- Return both fused aligned temporal features and the learned shift-confidence map.
- Build a C4 orientation-consensus line state from aligned temporal features and center-frame detail, then multiply it by alignment confidence before adding it to the encoder seed and full-resolution head support.
- Emit `mask_logits`, `line_logits`, and `centerline_logits`; the Line and Centerline auxiliary targets remain trusted Harness/provider targets.

## Contract Features Used

ABI-319 uses only allowlisted `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` frame selection with allowlisted `[-1, 0, 1]` offsets, trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, 12 exploratory epochs, and trusted Line plus Centerline auxiliary targets with weighted BCE. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling policies, augmentation transforms, thresholds, postprocessing, longitude/latitude, Dataset Source identity, downloads, temporal provisioning, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Default exploratory budget only: capped provider-selected temporal-eligible records, 12 epochs, batch size 2, constant learning rate, disabled early stopping, and A100 execution under the active Workspace Configuration. No late-improving budget is requested because this mechanism-changing shift-bank/C4 coupling first needs bounded resource and early scientific evidence.

## Success Criteria

Continue this branch only if ABI-319 completes, remains finite/non-collapsed/source-informative, and improves or usefully differentiates ABI-315's recall/connectivity/source-balance trade-off without excessive predicted-positive expansion. A later late-improving request would require a best checkpoint near epoch 12, non-degenerate predicted-positive fractions, source-informative MIT/Google metrics, and a trajectory suggesting under-training rather than plateau, collapse, or oscillation.

## Fallback/Next Decision

If the Run fails due to a candidate bug, repair only if the fix preserves this alignment-confidence-gated C4 line-state hypothesis and comparison target. If resource usage is too high, reduce width or C4/head support streams rather than changing Harness-owned data/resource policy. If it completes but repeats ABI-315's weak connectivity, source imbalance, or broad low-precision footprint, do not submit an unchanged continuation; broaden to a different temporal-attention evidence-sharpening design, loss/data policy via trusted allowlists, or a materially different line-continuity family.
