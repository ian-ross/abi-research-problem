# ABI-343 C4 precision-veto recall bridge

## Hypothesis

ABI-249 showed that C4/rotation-shared line context can produce compact, high-precision predictions, while ABI-342 showed that the same branch can recover fixed-threshold recall but at excessive precision and footprint cost. ABI-343 tests whether a smaller positive recall residual, gated by anchor uncertainty plus C4 line/detail agreement and paired with a differentiable low-line-evidence clutter veto, can keep much of ABI-342's recall gain while moving precision and predicted-positive footprint back toward ABI-249.

This is a **family-development continuation** in the single-frame C4/orientation-prior branch. It is not an unchanged late36 continuation of ABI-342: the head changes from a direct line-gated signed residual to an uncertainty-band, detail-agreement-limited positive lift with an architecture-internal clutter veto.

## Comparison Target

Primary comparison targets are:

- ABI-249 (`run_20260911_111909_dd7ef7`) as the compact high-precision C4 comparator.
- ABI-342 (`run_20260918_055403_f17232`) as the recall-biased C4 diagnostic.
- ABI-202 (`run_20260904_043143_ee0005`) as the aggregate whole-validation filtered-Dice reference.

## Expected Effect

Expected effects on the capped validation split:

- Increase recall over ABI-249 by adding a bounded residual only near uncertain anchor logits.
- Improve precision and reduce predicted-positive pixels relative to ABI-342 by requiring line/detail agreement and subtracting a small low-line-evidence veto.
- Preserve or improve ABI-249/ABI-342 connectivity through the shared C4 line context and trusted Line/Centerline auxiliary outputs.
- Maintain finite, non-collapsed, source-informative behavior under the same resource envelope as recent C4 late36 Runs.

## Implementation Sketch

The Candidate reuses the ABI-342 full-spectral BTD+SZA front end, signed-detail stem, U-Net encoder/decoder, ASPP context, and C4 steerable line-context block. The changed `C4PrecisionVetoRecallMaskHead` computes:

1. an anchor mask from fused full-resolution features and C4 line context;
2. C4 `line_logits` and `centerline_logits` for trusted auxiliary targets;
3. an anchor-uncertainty gate `exp(-abs(anchor_logits))` so residual support is strongest only around the fixed-threshold decision band;
4. a C4 line-evidence/detail-agreement gate for a small non-negative recall lift;
5. a small differentiable clutter veto where anchor uncertainty is high but line evidence is low.

All logic is model architecture. The Candidate does not implement thresholding, postprocessing, Artifact Filters, custom losses, metrics, data loading, sampling, temporal lookup, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza`
- `output_form: mask_logits`
- Trusted auxiliary targets: `line` -> `line_logits`, `centerline` -> `centerline_logits`
- Trusted sampling policy: `combined_source_balanced`
- Trusted frame-selection policy: `all_target_frames`
- Trusted augmentation policy: `random_mirroring`
- Trusted primary loss: `bce_dice`
- Trusted optimizer/scheduler: AdamW with `constant_lr`
- Batch size 4, exploratory manifest `max_epochs: 12`, optional Harness-validated late-improving budget request to 36 epochs

## Budget Requested

Request the approved `late_improving` budget (`requested_max_epochs: 36`) with parent Runs ABI-249 and ABI-342. ABI-249 selected its best checkpoint at epoch 31 and ABI-342 selected its best checkpoint at epoch 36 with finite, source-informative trajectories. If the Harness denies the request, run under the exploratory budget and treat that as the valid bounded result.

## Success Criteria

A successful capped-family result should satisfy several of:

- Filtered Dice at or above ABI-249, or no worse than about 0.003 below ABI-249 while improving recall/connectivity.
- Filtered recall clearly above ABI-249 and preferably near ABI-342 without ABI-342's large precision drop.
- Filtered precision materially above ABI-342 and predicted-positive pixels closer to ABI-249 than ABI-342.
- MIT filtered Dice and aggregate source behavior at least comparable to ABI-249/ABI-342 without source collapse.
- Finite, non-collapsed learning with no hard resource, smoke, contract, or lifecycle failure.

## Fallback/Next Decision

If ABI-343 still trades too much precision for recall or fails to improve over both ABI-249 and ABI-342 on the intended compact-recall balance, do not continue this exact C4 recall-veto head unchanged. Either request a bounded failure-bucket evaluation only if the capped result is near-comparator and diagnostically ambiguous, or broaden to a different mechanism such as temporal attention/evidence sharpening or a separate line-continuity architecture. Do not implement Candidate-owned thresholds, losses, postprocessing, Artifact Filters, data policy, coordinates, or sampling workarounds.
