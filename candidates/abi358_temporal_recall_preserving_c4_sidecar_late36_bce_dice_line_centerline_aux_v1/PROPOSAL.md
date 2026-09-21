# ABI-358 temporal recall-preserving C4 sidecar late36

## Hypothesis

ABI-356 showed that multi-scale temporal-change and center-detail skip fusion can recover fixed-threshold recall on the temporal-eligible validation population, but with a broad footprint and weak connected-line continuity. ABI-357 showed that a compact C4 orientation-continuity anchor can improve precision and connectivity versus ABI-356, but it suppresses too much recall. This family-development continuation tests whether decoupling the C4 continuity path from the recall path can preserve ABI-356-like true-positive coverage while retaining some ABI-357 compactness/connectivity benefit.

## Comparison Target

Primary comparison is ABI-356 (`run_20260919_095725_843317`) as the recall-positive parent and ABI-357 (`run_20260919_123025_7cd861`) as the compact C4-anchor parent. Secondary temporal-eligible comparators are ABI-350 (`run_20260919_013306_9ca44e`) for compact line-support filtered Dice/precision, ABI-324/348 for five-frame C4/detail behavior, and ABI-223 for temporal-attention connectivity. This is capped temporal-eligible evidence, not whole Working Validation Split promotion evidence against ABI-202 or ABI-249.

## Expected Effect

The expected outcome is a less broad version of ABI-356: higher precision, fewer predicted-positive pixels, and better connectivity than ABI-356 while losing less recall than ABI-357. A successful result would move toward ABI-350/324 aggregate quality without becoming another conservative compact state. The most useful diagnostic signal would be fixed-threshold filtered recall near or above 0.40 with connectivity improved over ABI-356 and filtered Dice in the ABI-348/350 band.

## Implementation Sketch

Start from the ABI-357 temporal architecture: finite ABI+SZA+BTD per-frame features, lightweight temporal attention, compact U-Net encoder/decoder, ASPP bottleneck, and multi-scale temporal-change/center-detail line-support skip fusion. Replace the final `C4ContinuityAnchor` with `RecallPreservingC4Sidecar`:

- fuse decoder and high-resolution temporal skip support into an additive recall path;
- compute C4 rotation-shared line context from bounded refined features plus weak support;
- feed C4 line context directly to the trusted Line auxiliary output;
- add only a small learned gated C4 residual into mask features;
- avoid using the C4 path as a late compacting veto on recall support.

The model returns `mask_logits`, `line_logits`, and `centerline_logits` with shape `[1, 256, 256]`.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal` with provider-owned channel-stacked frames only.
- `data.frame_selection_policy: temporal_eligible_center` and `data.temporal_frame_offsets: [-1, 0, 1]`.
- `data.sampling_policy: combined_source_balanced` and trusted `random_mirroring` augmentation.
- Trusted `bce_dice` primary loss, AdamW optimizer, constant learning-rate scheduler, and batch size 2.
- Trusted auxiliary targets `line` and `centerline` with `weighted_bce` losses.

The candidate does not implement data loading, temporal lookup, S3/NetCDF access, padding, sample selection, losses, metrics, Artifact Filters, postprocessing, thresholds, target derivation, augmentation, resource scheduling, or coordinate/location features.

## Budget Requested

Request the approved `late_improving` budget for 36 epochs through `budget_request.yaml`. ABI-356 selected its best checkpoint at epoch 36, and ABI-357 also selected its best checkpoint at epoch 36 after converting ABI-356's broad-recall state into a compact state. The proposed mechanism is a close continuation whose behavior is likely late-dependent and oscillatory; an exploratory 12-epoch result would be a valid fallback if the Harness denies the request.

## Success Criteria

Treat this as family-development evidence, not a promotion claim. Success is any of:

- temporal-eligible `val/filtered_dice` at or above ABI-348/324/350's capped band (roughly 0.428 or higher) while keeping filtered recall at least 0.40;
- filtered connectivity materially above ABI-356 while retaining at least most of ABI-356's recall advantage over ABI-350;
- a compactness/precision improvement over ABI-356 without dropping to ABI-357's low-recall state.

Source-stratified MIT and Google metrics must both remain finite and non-collapsed, with no evidence of coordinate, Artifact Filter, or threshold dependence.

## Fallback/Next Decision

If ABI-358 reproduces ABI-357's recall suppression or fails to improve connectivity over ABI-356, stop this exact C4-sidecar branch and broaden to a different temporal alignment/backbone or recall-calibration mechanism. If it improves recall/connectivity trade-offs but remains below ABI-350/324, consider a bounded diagnostic or one mechanism-changing follow-up that moves continuity support earlier in the center-detail/temporal-alignment path. Do not request Candidate-owned thresholds, postprocessing, losses, metrics, data loading, temporal lookup, or Artifact Filters.
