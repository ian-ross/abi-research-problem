# ABI-357 temporal C4 orientation-continuity anchor late36

## Hypothesis

ABI-356 recovered useful fixed-threshold recall from multi-scale temporal change/detail fusion, but its selected late36 checkpoint broadened the positive footprint and left connected-line continuity below ABI-350/324/223. ABI-350 showed that compact temporal line support can be high-precision after late training, while ABI-353/249-style C4 rotation-shared context remains the strongest compact orientation prior. A close mechanism-changing continuation that preserves ABI-356's recall-positive temporal fusion but adds a compact C4 rotation-shared orientation-continuity anchor before the logits may raise connectivity and precision without losing the recovered recall.

This is a **family-development continuation**, not a promotion candidate. It is intended to test a specific mechanism change inside the profiled temporal-attention line-support family.

## Comparison Target

Primary comparison target is ABI-356 (`run_20260919_095725_843317`) because ABI-357 directly modifies its multi-scale temporal change/detail fusion with a C4 continuity anchor. Secondary temporal-eligible comparators are ABI-350 (`run_20260919_013306_9ca44e`), ABI-324 (`run_20260916_184108_954ec7`), ABI-348 (`run_20260918_215534_a35ab9`), ABI-346 (`run_20260918_152331_c80150`), and ABI-223 (`run_20260908_154531_8c7e2b`). ABI-202 and ABI-249 remain whole-validation references, but this Run will be capped temporal-eligible evidence unless a later trusted evaluation is requested.

## Expected Effect

Relative to ABI-356, ABI-357 should reduce the broad positive footprint, improve filtered precision and Contrail Connectivity Metric, and preserve much of ABI-356's fixed-threshold recall. A strong result would approach ABI-350/324 aggregate temporal-eligible Dice while improving ABI-356 connectivity and retaining better recall than ABI-350. A useful negative result would show that adding a compact C4 anchor either suppresses the recovered recall or fails to constrain clutter/continuity, indicating that this temporal-attention fusion branch needs a different continuity mechanism.

## Implementation Sketch

The candidate consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` selection. The model splits the already-provided channel-stacked tensor into previous/center/next frames, builds finite normalized ABI, Solar Geometry Input, and ABI-channel-derived BTD features, and uses the ABI-356 temporal-attention stem, compact U-Net encoder/decoder, ASPP context, and multi-scale temporal-change line-fusion skip modules.

The mechanism change is a differentiable high-resolution `C4ContinuityAnchor`: it reuses one horizontal strip-context block over four rotated views, learns soft orientation weights, combines weighted/mean/max orientation context with signed detail, and gates that compact C4 line context against the decoder and high-resolution skip-support features before the final mask and auxiliary heads. This is architecture-internal feature fusion only; it is not thresholding, morphology, postprocessing, or an Artifact Filter.

Candidate code does not implement data loading, temporal lookup, S3/NetCDF access, cache reads, padding, duplicate-frame fallback, target construction, losses, metrics, Artifact Filters, thresholds, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinate inputs, Dataset Source identity, resource placement, or lifecycle behavior.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`; no longitude or latitude channels.
- Trusted temporal policy: `data.frame_selection_policy: temporal_eligible_center` with `data.temporal_frame_offsets: [-1, 0, 1]`.
- Output form: `mask_logits` with trusted auxiliary `line_logits` and `centerline_logits`.
- Trusted primary loss: `bce_dice`.
- Trusted auxiliary losses: provider-owned weighted-BCE Line and Centerline targets.
- Trusted data policy: `combined_source_balanced` sampling and `random_mirroring` augmentation.
- Optimizer/scheduler: AdamW with constant learning rate.
- Harness-owned fixed threshold, validation metric, Artifact Filters, capped record selection, temporal provisioning, execution, resource limits, budget approval, and lifecycle.

## Budget Requested

Request the approved `late_improving` budget: 36 epochs and 10,800 seconds, with exploratory fallback if denied. The request is justified because ABI-356 selected its best checkpoint at the final late36 epoch with finite source-informative recall recovery, and ABI-350 selected a compact temporal line-support state only near epoch 33. ABI-357 is a close continuation using the same temporal input policy, batch size 2, and profiled model family, but with a mechanism-changing C4 continuity anchor intended to stabilize the late recall/precision/connectivity oscillation.

The manifest keeps the ordinary exploratory fields; `budget_request.yaml` asks the Harness to authorize the longer budget.

## Success Criteria

Treat ABI-357 as positive family-development evidence if it completes finite and shows at least one of: higher filtered Dice than ABI-356, materially improved Contrail Connectivity Metric over ABI-356 while retaining most of its recall, improved precision/compactness without reverting to ABI-350-level under-recall, fewer predicted-positive pixels without a source-specific collapse, or a late trajectory that identifies a stable compact connected-line state. A temporal-eligible failure-bucket evaluation would be justified only if the result approaches or exceeds ABI-350/324/348 temporal comparator band or shows a novel recall/connectivity trade-off worth diagnosing.

## Fallback/Next Decision

If ABI-357 fails contract, smoke, shape, or finite-state checks due to candidate code, submit a Repair Candidate that preserves this hypothesis and comparison target. If it completes but loses ABI-356's recall without improving connectivity/precision, or remains below ABI-350/324/223/348 with broad clutter or unstable line continuity, stop this exact anchor branch and broaden to a different continuity mechanism rather than another gate-strength or placement shuffle. Do not respond by adding candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, resource scheduling, or lifecycle changes.
