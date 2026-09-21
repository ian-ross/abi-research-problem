# ABI-356 temporal-attention multi-scale change-line fusion late36

## Hypothesis

ABI-355 showed that injecting temporal-change and center-frame detail evidence during multi-scale decoder skip fusion is healthier than the recent encoder-entry or final-output bridge placements: it improved capped filtered Dice, recall, and connectivity over ABI-349/351/354, remained finite and source-informative, and selected its best checkpoint near the 12-epoch exploratory ceiling. A late-improving continuation may stabilize the epoch-8-to-11 state into a more compact, connected fixed-threshold temporal solution without changing thresholds, postprocessing, losses, metrics, data selection, or temporal provisioning.

This is a **family-development continuation**, not a promotion candidate. The goal is to fairly test ABI-355s specific multi-scale change-line fusion mechanism under the approved late-improving budget before either developing it further or moving to a mechanism-changing temporal branch.

## Comparison Target

Primary comparison is ABI-355 (`run_20260919_090506_bad1ff`). Secondary temporal-family comparators are ABI-350 late36 line-support (`run_20260919_013306_9ca44e`), ABI-324 balanced five-frame C4 (`run_20260916_184108_954ec7`), ABI-223 temporal attention (`run_20260908_154531_8c7e2b`), and ABI-348 compact five-frame C4 (`run_20260918_215534_a35ab9`). ABI-202 remains the aggregate whole-validation reference, but ABI-356 will provide capped temporal-eligible evidence only unless a later trusted evaluation is requested.

## Expected Effect

Relative to ABI-355, ABI-356 should either improve best capped temporal-eligible filtered Dice or clarify whether the ABI-355 late oscillation can be resolved into a better recall/connectivity/precision balance. A useful positive result would raise fixed-threshold recall and connected-line continuity without broad predicted-positive expansion or severe MIT/Google imbalance. A useful negative result would show that the multi-scale placement remains unstable or clutter-prone even with the approved longer budget.

## Implementation Sketch

The candidate preserves ABI-355s architecture and manifest choices. It consumes provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]`; splits only the already-provided channel-stacked tensor inside the model; derives finite ABI-channel BTD planes from candidate-visible channels; uses a per-pixel temporal-attention stem, compact U-Net encoder/decoder, ASPP bottleneck, and `MultiScaleTemporalChangeLineFusion` modules at decoder skip scales. The primary `mask_logits` and trusted Line/Centerline auxiliary outputs are unchanged.

Candidate code defines model architecture only. It does not implement data loading, temporal lookup, S3/NetCDF access, cache reads, padding, duplicate-frame fallback, target construction, losses, metrics, Artifact Filters, thresholds, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinate inputs, Dataset Source identity, resource placement, or lifecycle behavior.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`; no longitude or latitude channels.
- Trusted temporal policy: `data.frame_selection_policy: temporal_eligible_center` with `data.temporal_frame_offsets: [-1, 0, 1]`.
- Output form: `mask_logits` with trusted auxiliary `line_logits` and `centerline_logits`.
- Trusted loss: `bce_dice` primary with provider-owned weighted-BCE Line and Centerline auxiliary targets.
- Trusted data policy: `combined_source_balanced` sampling and `random_mirroring` augmentation.
- Optimizer/scheduler: AdamW with constant learning rate.
- Harness-owned fixed threshold, metrics, Artifact Filters, capped record selection, temporal provisioning, execution, resource limits, budget approval, and lifecycle.

## Budget Requested

Request the approved `late_improving` budget: 36 epochs and 10,800 seconds, with exploratory fallback if denied. The request is justified because ABI-355 was finite, non-collapsed, resource-safe, source-informative, improved over related exploratory placement variants, and selected its best checkpoint at epoch 11 with unresolved late oscillation near the exploratory ceiling.

The manifest keeps the ordinary exploratory fields; the candidate-local `budget_request.yaml` asks the Harness to authorize the longer budget.

## Success Criteria

Continue or request bounded diagnostics only if ABI-356 is finite and shows at least one of: improved capped temporal-eligible filtered Dice over ABI-355, higher fixed-threshold recall without a large precision collapse, improved Contrail Connectivity Metric, stronger MIT/source balance, or a late trajectory that identifies a stable compact/connected state. Whole-validation or temporal-eligible failure-bucket diagnostics would require a separate handoff and should be reserved for a result that approaches the established temporal comparator band.

## Fallback/Next Decision

If ABI-356 fails contract/smoke/resource checks because of candidate code, repair the bug while preserving the hypothesis. If it completes but remains below ABI-350/324/223/348 with unstable connectivity, broad clutter, or no meaningful improvement over ABI-355, treat the late-budget question as answered and broaden to a mechanism-changing temporal alignment/change architecture rather than another gate-strength or placement shuffle. Do not respond by adding candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, or coordinate features.
