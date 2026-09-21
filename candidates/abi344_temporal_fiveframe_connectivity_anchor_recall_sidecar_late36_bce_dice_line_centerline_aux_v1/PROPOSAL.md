# ABI-344 temporal five-frame connectivity-anchor recall sidecar

## Hypothesis

ABI-324 established the strongest local five-frame temporal C4/detail-consensus balance, but its trajectory and later diagnostics show a persistent decoupling: some checkpoints are compact and connected but under-recall, while recall-oriented variants such as ABI-341 reduce positive-tail misses at the cost of broad negative-patch clutter and weak connectivity. ABI-344 tests whether making that separation explicit in the architecture can improve the trade-off: a compact connectivity anchor predicts the main mask from decoder plus temporal C4 line-state evidence, and a learned recall sidecar adds only a bounded non-negative lift where anchor uncertainty, Line/Centerline evidence, center-detail agreement, line-state agreement, and sidecar/anchor agreement all concur.

This is a **family-development continuation** in the profiled five-frame temporal C4 line-state branch. It is not an unchanged late36 continuation of ABI-324, ABI-337, or ABI-341: the final evidence construction changes from a single fused consensus residual/router into a two-state connectivity-anchor plus agreement-gated sidecar.

## Comparison Target

Primary comparison targets are:

- ABI-324 (`run_20260916_184108_954ec7`) as the balanced temporal C4/detail-consensus comparator.
- ABI-337 (`run_20260917_201833_57b081`) as the no-mirroring/recall-shift diagnostic control.
- ABI-341 (`run_20260918_031022_a8f552`) as the positive-tail recall-router diagnostic with unacceptable clutter/connectivity cost.
- ABI-223 (`run_20260908_154531_8c7e2b`) as the temporal-attention connectivity comparator on the temporal-eligible validation population.

## Expected Effect

Expected effects on the capped temporal-eligible validation population:

- Preserve ABI-324-like compactness and connected-line behavior through a compact anchor driven by decoder features and early temporal C4 line-state support.
- Recover some true-positive recall and positive-tail support through a small sidecar lift near uncertain anchor logits.
- Avoid ABI-341-style broad negative-patch clutter by requiring Line, Centerline, detail, line-state, and anchor/sidecar agreement before any positive lift is applied.
- Maintain finite, non-collapsed, source-informative behavior under the same profiled resource envelope as ABI-324/337/341.

## Implementation Sketch

The Candidate reuses the ABI-324 temporal frame feature builder, C4 orientation-consensus line-state stem, single-stream encoder, line-state injection at all scales, ASPP context, decoder, and high-resolution directional context. The changed `ConnectivityAnchorRecallSidecarHead` computes:

1. a compact anchor feature from full-resolution decoder evidence plus resized early C4 line state;
2. a sidecar feature from decoder evidence, center-frame temporal-stem detail, line state, and decoder/detail disagreement;
3. `line_logits` from the anchor feature and `centerline_logits` from the sidecar feature for trusted auxiliary targets;
4. an anchor mask logit and a sidecar candidate mask logit;
5. a bounded positive lift `relu(tanh(sidecar - anchor))` multiplied by anchor uncertainty and learned agreement gates;
6. final `mask_logits = anchor + recall_lift` with logits bounded by existing architecture-internal activation limits.

All logic is model architecture. The Candidate does not implement thresholding, postprocessing, Artifact Filters, custom losses, metrics, data loading, sampling, temporal lookup, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal`
- `data.frame_selection_policy: temporal_eligible_center`
- `data.temporal_frame_offsets: [-2, -1, 0, 1, 2]`
- `output_form: mask_logits`
- Trusted auxiliary targets: `line` -> `line_logits`, `centerline` -> `centerline_logits`
- Trusted sampling policy: `combined_source_balanced`
- Trusted augmentation policy: `random_mirroring`
- Trusted primary loss: `bce_dice`
- Trusted optimizer/scheduler: AdamW with `constant_lr`
- Batch size 2, exploratory manifest `max_epochs: 12`, optional Harness-validated late-improving budget request to 36 epochs

## Budget Requested

Request the approved `late_improving` budget (`requested_max_epochs: 36`) with parent Runs ABI-324, ABI-337, and ABI-341. All three were finite, source-informative, resource-safe five-frame temporal C4 Runs whose selected checkpoints occurred after the exploratory epoch ceiling. If the Harness denies the request, run under the exploratory budget and treat that as the valid bounded result.

## Success Criteria

A useful capped-family result should satisfy several of:

- Filtered Dice at or above ABI-324, or no worse than about 0.003 below ABI-324 while improving recall or positive-tail indicators without damaging connectivity.
- Filtered connectivity near ABI-324 and clearly above ABI-341.
- Filtered recall above ABI-324 or comparable to ABI-337/341 without ABI-341-like broad footprint.
- Filtered precision and predicted-positive pixels closer to ABI-324 than ABI-341.
- MIT and Google filtered Dice source behavior at least comparable to ABI-324/337 without source collapse.
- Finite, non-collapsed learning with no hard resource, smoke, contract, or lifecycle failure.

## Fallback/Next Decision

If ABI-344 still reproduces the same compact-versus-recall oscillation, or if the sidecar lift again raises recall only by broadening negative-patch clutter and lowering connectivity, do not continue this exact temporal C4 sidecar head unchanged. Either request a bounded temporal-eligible failure-bucket evaluation only if the capped result is near-comparator and diagnostically ambiguous, or broaden to a different temporal attention/evidence-sharpening, alignment/change, calibration, or non-temporal C4/orientation-recall mechanism. Do not implement Candidate-owned thresholds, losses, postprocessing, Artifact Filters, data policy, coordinates, or sampling workarounds.
