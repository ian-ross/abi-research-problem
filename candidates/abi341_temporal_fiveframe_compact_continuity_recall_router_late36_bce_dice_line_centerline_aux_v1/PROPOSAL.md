# ABI-341 temporal five-frame compact continuity recall router late36

## Hypothesis

ABI-324/337/338 show a persistent five-frame temporal C4/detail-consensus trade-off: compact connected checkpoints control clutter but under-recover some true contrail pixels, while broader recall states lose connectivity or add negative-patch clutter. A compact-state-protected recall router can preserve a connected compact anchor while adding a bounded positive recall lift only where continuous Line, Centerline, center-detail, and temporal line-state evidence agree.

This is a family-development continuation, not a promotion claim. It is mechanism-changing relative to ABI-338 because it separates a small signed compact continuity anchor from the positive recall lift instead of using one soft-band continuity reinjection branch.

## Comparison Target

Primary capped temporal-eligible comparisons:

- ABI-324 (`run_20260916_184108_954ec7`): strongest local balanced five-frame temporal C4/detail-consensus comparator, filtered Dice 0.4294 and connectivity 0.3979.
- ABI-337 (`run_20260917_201833_57b081`): no-mirroring control with slightly higher recall/MIT but lower connectivity and more clutter.
- ABI-338 (`run_20260917_230319_ed1362`): soft-band continuity reinjector with higher connectivity than ABI-337 but lower aggregate Dice than ABI-324.
- ABI-223 (`run_20260908_154531_8c7e2b`): temporal-attention connectivity comparator on the temporal-eligible validation population.

Whole-validation references ABI-202 and ABI-249 remain context only; this Candidate uses capped temporal-eligible evidence and is not a full Working Validation Split promotion comparison.

## Expected Effect

Useful evidence would be one or more of:

- maintain ABI-324/337-level aggregate filtered Dice while improving the recall/connectivity balance;
- improve filtered connectivity over ABI-337 and ABI-338 without ABI-325-like footprint expansion;
- retain ABI-337's MIT/recall benefit while reducing its negative-patch clutter.

The main risk is another over-gated compact state with insufficient recall. The positive lift is therefore tied to a continuous soft uncertainty band around the base logit, while the compact anchor is small and signed rather than a hard suppressor.

## Implementation Sketch

Start from the profiled five-frame temporal C4/detail-consensus U-Net resource envelope:

- consume provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-2, -1, 0, 1, 2]`;
- build per-frame normalized ABI, trusted Solar Geometry Input, and ABI-channel-derived BTD features inside the architecture;
- keep the temporal attention/change stem, early C4 orientation line state, compact encoder/decoder, line-state injection, and high-resolution directional context;
- replace the prior soft-band reinjection head with `CompactContinuityRecallRouterHead`.

The new head computes base mask, Line, and Centerline logits from shared full-resolution evidence. A compact residual is small, signed, and gated by base/Line/Centerline/detail/line-state agreement. A separate non-negative recall lift is bounded and only applied in the differentiable soft uncertainty band (`4 p (1-p)`) under the same learned evidence agreement and conflict guard. This is architecture-only; it does not select thresholds, postprocess predictions, derive targets, change losses, or own Artifact Filters.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Data policy: provider-owned `temporal_eligible_center` selection with `temporal_frame_offsets: [-2, -1, 0, 1, 2]`.
- Sampling policy: `combined_source_balanced`.
- Augmentation policy: trusted `random_mirroring`.
- Output form: `mask_logits`.
- Auxiliary targets: trusted `line_logits` and `centerline_logits` with `weighted_bce` weights 0.01 and 0.02.
- Primary loss: trusted `bce_dice`.
- Optimizer/scheduler: AdamW with constant learning rate 0.0003.
- Candidate code defines only PyTorch architecture and `build_model`; it does not implement data loading, temporal lookup, frame repair, losses, metrics, sampling, augmentation, Artifact Filters, thresholds, postprocessing, coordinate inputs, downloads, resource scheduling, training loops, evaluation, or ledger writes.

## Budget Requested

Request the Harness-owned `late_improving` budget for up to 36 epochs via `budget_request.yaml`.

Justification: ABI-324, ABI-337, and ABI-338 selected best checkpoints at epochs 27, 27, and 36, and the family remains finite, non-collapsed, source-informative, and late-budget-dependent. ABI-341 is a close, mechanism-changing continuation in the same profiled resource class. If the request is denied, run under the exploratory budget and treat that result as valid capped feasibility evidence.

## Success Criteria

Continue this line only if ABI-341 provides one of the following bounded signals on the temporal-eligible validation population:

- aggregate filtered Dice credibly ties ABI-324 while improving filtered recall, connectivity, or MIT filtered Dice;
- filtered connectivity improves over ABI-337/338 without a large negative-patch clutter increase;
- failure-bucket diagnostics show fewer low-recall positives or less source imbalance with finite non-collapsed predictions.

A promotion-level claim would require later trusted full-data/diagnostic evaluation; this Candidate alone is capped temporal-eligible evidence.

## Fallback/Next Decision

If ABI-341 is worse than ABI-324 on aggregate Dice and does not improve recall/connectivity/source balance, stop this compact-continuity recall-router branch rather than submitting another unchanged late36 continuation. If it improves recall but expands clutter, prefer a temporal-eligible failure-bucket Evaluation Request before modifying the head. If it is finite and late-improving but ambiguous, a single controlled follow-up may adjust the architecture-internal gates; otherwise broaden away from this temporal C4/detail-consensus family.
