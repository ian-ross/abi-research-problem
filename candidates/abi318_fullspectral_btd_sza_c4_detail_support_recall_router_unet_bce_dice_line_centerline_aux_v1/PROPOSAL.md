# ABI-318 C4 detail/support recall-router U-Net

## Classification

Family-development continuation in the single-frame full-spectral BTD+Solar Geometry Input C4/orientation-prior line. This is a mechanism-changing exploratory follow-up after ABI-249, ABI-279/280, ABI-303, and ABI-317; it is not a promotion candidate and not an unchanged late36 continuation.

## Hypothesis

ABI-249 remains the compact high-precision C4 comparator, but it under-recovers fixed-threshold recall. ABI-279/280 partially repaired recall/connectivity with C4 recall bridges, while ABI-303 became too conservative and ABI-317 showed that non-C4 directional message passing was resource-heavy and still weak on recall/source balance. The next useful single-frame question is whether C4 orientation evidence can be paired with center-frame signed detail and multi-scale decoder support through a less suppressive architecture-internal router.

ABI-318 tests a C4 detail/support recall router. It keeps a compact C4 steerable line-context U-Net and computes line-context, high-resolution signed-detail, and three cross-scale decoder support streams. Instead of subtracting a veto or requiring strict centerline protection, it adds only a small bounded non-negative recall lift when learned gates find agreement between C4 line context, detail features, and cross-scale support. A learned guard attenuates the lift under disagreement but does not perform Candidate-owned thresholding, morphology, connected-component logic, postprocessing, Artifact Filtering, custom loss, metric computation, data loading, sample selection, coordinate use, or resource scheduling.

## Comparison Target

Primary capped comparisons are ABI-202 as the aggregate single-frame reference, ABI-249 as the compact high-precision C4 comparator, ABI-279/280 as C4 recall-bridge comparators, ABI-303 as the conservative centerline-protected C4 head, and ABI-317 as the non-C4 directional message-passing scout. ABI-318 produces capped representative feasibility evidence only, not whole-validation promotion evidence.

## Expected Effect

A useful Result should complete under the exploratory budget, remain finite and source-informative, and show at least one of:

- higher fixed-threshold recall than ABI-249/303 without ABI-292/302-style precision collapse or a very broad footprint;
- connectivity closer to ABI-202/279 while preserving C4-like precision;
- better MIT/source balance than ABI-317 and ABI-303; or
- a stable late exploratory trajectory indicating that the router is a viable bounded continuation target.

A negative Result would show that this C4/detail/support routed lift is another ineffective recall-calibration surface and should push the campaign away from single-frame C4 residual-head variants.

## Implementation Sketch

- Consume only provider-approved `abi_16ch_plus_sza` tensors.
- Normalize ABI channels 1-16, derive approved-channel thermal BTD planes, include Solar Geometry Input, and learn a small 1x1 channel mixture.
- Use the compact C4 steerable line-context U-Net structure from the ABI-249/303 family: signed-detail stem, encoder/decoder, ASPP bottleneck, full-resolution detail fusion, and Line/Centerline auxiliary outputs.
- Replace ABI-303's centerline-protected head with `C4DetailSupportRecallRouterHead`:
  - build region logits from full-resolution decoder plus C4 line context;
  - build signed-detail, support, centerline, and routed evidence features;
  - compute learned line/detail/support gates from approved model features;
  - compute a learned disagreement guard that attenuates but never subtracts an independent postprocessing veto;
  - add a small bounded non-negative recall lift to the region logits;
  - emit `mask_logits`, `line_logits`, and `centerline_logits` for trusted Harness losses.

## Contract Features Used

ABI-318 uses only allowlisted `abi_16ch_plus_sza` input, trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, BCE-Dice primary loss, AdamW, constant learning rate, batch size 4, 12 exploratory epochs, and trusted Line plus Centerline auxiliary targets with weighted BCE. Candidate source does not implement data loading, target construction, losses, metrics, Artifact Filters, sampling policies, augmentation transforms, thresholds, postprocessing, longitude/latitude, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Default exploratory budget only: capped provider-selected records, 12 epochs, batch size 4, constant learning rate, disabled early stopping, and A100 execution under the active Workspace Configuration. No late-improving budget is requested because this router first needs bounded resource and early scientific evidence.

## Success Criteria

Continue this branch only if ABI-318 completes, remains finite/non-collapsed/source-informative, and improves or usefully differentiates the recall/precision/connectivity trade-off against ABI-249/279/280/303/317. A later late-improving request would require a best checkpoint near epoch 12, non-degenerate predicted-positive fractions, source-informative MIT/Google metrics, and a trajectory suggesting under-training rather than plateau, collapse, or oscillatory trade-off.

## Fallback/Next Decision

If the Run fails due to a candidate bug, repair only if the fix preserves this detail/support recall-router hypothesis and comparison target. If resource usage is too high, reduce head width or support streams rather than changing Harness-owned data/resource policy. If it completes but repeats compact underprediction, broad low-precision recall, weak MIT/source balance, or poor connectivity, stop this exact C4 router branch and broaden to a different temporal-attention, data/loss-policy, or modern-backbone mechanism.
