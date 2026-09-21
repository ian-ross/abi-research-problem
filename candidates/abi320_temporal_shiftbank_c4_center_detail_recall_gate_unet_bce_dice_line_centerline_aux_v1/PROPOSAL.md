# ABI-320 temporal shift-bank C4 center-detail recall-gate U-Net

## Classification

Family-development continuation in the temporal line-continuity/evidence-sharpening branch. This is a mechanism-changing exploratory follow-up after ABI-319; it is not a promotion candidate and not an unchanged late36 continuation.

## Hypothesis

ABI-319 showed that coupling local shift-bank temporal alignment to alignment-confidence-gated C4 orientation consensus can clean up ABI-315's predictions: precision and connectivity improved while the predicted-positive footprint shrank. The remaining failure was recall: ABI-319 still trailed ABI-311 and ABI-309 on fixed-threshold true-contrail recovery.

ABI-320 tests whether the missing mechanism is a recall-protected center-detail evidence head rather than another shift-bank alignment change. It preserves ABI-319's provider-owned three-frame temporal input, no-wrap local alignment, and C4 cleanliness, then adds a small architecture-internal logit lift only when full-resolution center detail, aligned temporal support, and C4 line-state evidence agree. A learned clutter/disagreement gate reduces the lift where the region prediction, support prediction, and center-detail support diverge. The intent is to recover some ABI-311/309 recall while preserving ABI-319's compactness and connectivity.

The candidate does not implement Candidate-owned thresholds, morphology, connected-component logic, postprocessing, Artifact Filtering, custom losses, metrics, data loading, sample selection, coordinate use, temporal lookup, or resource scheduling.

## Comparison Target

Primary capped temporal-eligible comparisons are ABI-319 as the clean shift-bank/C4 parent, ABI-315 as the original shift-bank scout, ABI-311 as the balanced five-frame temporal C4 comparator, ABI-309 as the recall-heavy temporal C4 comparator, and ABI-306 as the compact high-precision temporal C4 comparator. ABI-320 produces capped temporal-eligible feasibility evidence only, not full Working Validation Split promotion evidence.

## Expected Effect

A useful Result should complete under the exploratory budget, remain finite and source-informative, and show at least one of:

- higher filtered recall than ABI-319 without losing most of ABI-319's precision/connectivity gain over ABI-315;
- filtered Dice closer to ABI-311 than ABI-319 while retaining a materially smaller footprint than ABI-309;
- improved MIT filtered Dice or smaller source gap relative to ABI-319; or
- a final-epoch or late-exploratory trajectory that justifies considering a late-improving continuation.

A negative Result would show that recall-protected center-detail logit support still cannot convert clean shift-bank/C4 temporal evidence into fixed-threshold true-positive recovery.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza_temporal` tensors with trusted temporal-eligible center selection and offsets `[-1, 0, 1]`.
- Normalize ABI channels 1-16 per frame, derive approved-channel BTD planes, and include per-frame Solar Geometry Input.
- Encode previous, center, and next frames with a shared stem; align previous/next features to the center frame through the no-wrap nine-shift differentiable shift bank.
- Build alignment-confidence-gated C4 orientation line state from aligned temporal features and center detail.
- Decode a compact U-Net feature pyramid and project temporal, decoder, center-detail, and C4 supports into the head.
- Replace ABI-319's head with a center-detail recall gate: line/C4 agreement and center-detail/support agreement provide bounded positive logit support, while disagreement and clutter gates provide bounded veto terms.
- Emit `mask_logits`, `line_logits`, and `centerline_logits`; Line and Centerline auxiliary targets remain trusted Harness/provider targets.

## Contract Features Used

ABI-320 uses only allowlisted `abi_16ch_plus_sza_temporal` input, trusted `temporal_eligible_center` frame selection with allowlisted `[-1, 0, 1]` offsets, trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, 12 exploratory epochs, and trusted Line plus Centerline auxiliary targets with weighted BCE. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling policies, augmentation transforms, thresholds, postprocessing, longitude/latitude, Dataset Source identity, downloads, temporal provisioning, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Default exploratory budget only: capped provider-selected temporal-eligible records, 12 epochs, batch size 2, constant learning rate, disabled early stopping, and A100 execution under the active Workspace Configuration. No late-improving budget is requested because this head-level mechanism first needs bounded resource and early scientific evidence.

## Success Criteria

Continue this branch only if ABI-320 completes, remains finite/non-collapsed/source-informative, and improves or usefully differentiates ABI-319's recall/connectivity/source-balance trade-off without broad predicted-positive expansion. A later late-improving request would require a best checkpoint near epoch 12, non-degenerate predicted-positive fractions, source-informative MIT/Google metrics, and a trajectory suggesting under-training rather than plateau, collapse, or oscillation.

## Fallback/Next Decision

If the Run fails due to a candidate bug, repair only if the fix preserves this center-detail recall-gate hypothesis and comparison target. If resource usage is too high, reduce head or decoder width rather than changing Harness-owned data/resource policy. If it completes but repeats ABI-319's under-recall or oscillating calibration, do not submit an unchanged continuation; broaden away from direct shift-bank/C4 head refinements toward a materially different temporal-attention or line-continuity mechanism.
