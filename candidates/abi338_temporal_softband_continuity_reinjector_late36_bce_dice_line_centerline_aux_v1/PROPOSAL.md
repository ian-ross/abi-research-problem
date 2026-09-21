# ABI-338 temporal soft-band continuity reinjector late36

## Hypothesis

ABI-324/337 show that the five-frame temporal C4/detail-consensus family can produce finite, source-informative predictions near the temporal frontier, but it repeatedly separates compact high-connectivity states from broader higher-recall states. A differentiable soft-band continuity reinjection head can raise uncertain true contrail logits along learned Line/Centerline-supported temporal C4 evidence while preserving ABI-324-like clutter control better than positive-tail or no-mirroring variants.

This is a family-development continuation, not a promotion claim. It is mechanism-changing relative to ABI-324/337 because the mask head adds a second bounded positive residual path gated by soft base-mask uncertainty, detail/line alignment, and Line/Centerline agreement rather than relying only on a single consensus residual.

## Comparison Target

Primary capped temporal-eligible comparisons:

- ABI-324 (`run_20260916_184108_954ec7`): strongest local balanced five-frame temporal C4/detail-consensus comparator, filtered Dice 0.4294 and connectivity 0.3979.
- ABI-337 (`run_20260917_201833_57b081`): no-mirroring control, useful for source/clutter trade-offs but not a new comparator.
- ABI-328 (`run_20260917_055012_ba7890`): soft-shift alignment diagnostic with higher recall than ABI-324 but weaker connectivity.
- ABI-223 (`run_20260908_154531_8c7e2b`): temporal-attention connectivity comparator on the temporal-eligible validation population.

Whole-validation references ABI-202 and ABI-249 remain context only; this Candidate uses capped temporal-eligible evidence and is not a full Working Validation Split promotion comparison.

## Expected Effect

Expected useful signal is not merely higher aggregate Dice. ABI-338 should improve one or more of:

- fixed-threshold filtered recall versus ABI-324 without ABI-325/309-scale negative-patch clutter expansion;
- filtered connectivity versus ABI-337/328 while retaining competitive aggregate filtered Dice;
- MIT filtered Dice or positive-patch low-recall bucket counts without worsening Google negative clutter enough to erase the gain.

The main risk is that the soft-band path behaves like another recall broadener and increases negative-patch clutter. The conflict guard and Line/Centerline/detail gates are intended to keep reinjection tied to learned line evidence rather than a generic foreground boost.

## Implementation Sketch

Start from the profiled ABI-324 five-frame temporal C4/detail-consensus U-Net resource envelope:

- consume provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-2, -1, 0, 1, 2]`;
- build per-frame normalized ABI, trusted Solar Geometry Input, and ABI-channel-derived BTD features inside the architecture;
- use the existing temporal attention/change stem, early C4 orientation line state, compact encoder/decoder, line-state injection, and high-resolution directional context;
- replace `DetailConsensusStabilizedHead` with `SoftBandContinuityReinjectorHead`.

The new head computes base mask, Line, and Centerline logits from the shared full-resolution evidence. It keeps the prior consensus residual at a slightly smaller bound and adds a second continuity residual only where the base mask probability is in a differentiable soft uncertainty band (`4 p (1-p)`), Line and Centerline probabilities agree, and center-detail/temporal-line evidence aligns. This is model architecture only: it does not select thresholds, postprocess predictions, derive targets, change losses, or own Artifact Filters.

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

Justification: ABI-324 and ABI-337 selected best checkpoints at epoch 27, ABI-328 selected at epoch 36, and the family remains finite, non-collapsed, source-informative, and late-budget-dependent. ABI-338 is a close, mechanism-changing continuation in the same profiled resource class rather than a new unprofiled architecture family. If the request is denied, run under the exploratory budget and treat that result as valid capped feasibility evidence.

## Success Criteria

Continue this line only if ABI-338 provides one of the following bounded signals on the temporal-eligible validation population:

- aggregate filtered Dice credibly ties or improves on ABI-324 while improving filtered recall or MIT filtered Dice;
- filtered connectivity improves over ABI-337/328 without a large negative-patch clutter increase;
- failure-bucket diagnostics show fewer low-recall positive samples or less source imbalance with finite non-collapsed predictions.

A promotion-level claim would require later trusted full-data/diagnostic evaluation; this Candidate alone is capped temporal-eligible evidence.

## Fallback/Next Decision

If ABI-338 is worse than ABI-324 on aggregate Dice and does not improve recall/connectivity/source balance, stop the soft-band reinjection branch rather than submitting another unchanged late36 continuation. If it improves recall but expands clutter, prefer an Evaluation Request for temporal-eligible failure buckets before modifying the head. If it is finite and late-improving but ambiguous, a single controlled follow-up may adjust the architecture-internal gates; otherwise broaden away from this temporal C4/detail-consensus family.
