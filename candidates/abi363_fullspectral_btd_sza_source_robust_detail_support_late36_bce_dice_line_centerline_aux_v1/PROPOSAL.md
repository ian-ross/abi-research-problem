# ABI-363 full-spectral BTD+SZA source-robust detail-support late36

## Hypothesis

Recent single-frame and temporal work repeatedly exposed a precision/recall/connectivity trade-off: ABI-249 and several C4 variants are compact and precise but recall-limited, while ABI-342/360-style recall states broaden the prediction footprint and lose precision. ABI-362 showed that another local C4 anchor/sidecar split is not enough; it recovered only a small amount of recall while regressing aggregate/source Dice, precision, and connectivity.

ABI-363 tests a mechanism-changing single-frame continuation: keep the mature full-spectral ABI+Solar Geometry Input, BTD, signed-detail U-Net/ASPP backbone, but replace local C4-head tuning with a source-agnostic multi-scale signed-detail tail-support path and a bounded architecture-internal dual-evidence calibration head. The hypothesis is that faint positive-tail contrail evidence, especially for MIT/source-balance weaknesses, can be raised at the fixed trusted threshold when region evidence, axis line-support evidence, and high-resolution detail residuals agree, without using Dataset Source identity, coordinates, candidate-owned thresholds, or postprocessing.

This is a **family-development continuation**, not a promotion claim. It broadens the mechanism after the exact C4 anchor/sidecar branch underperformed.

## Comparison Target

Primary capped-development comparators are ABI-202 (aggregate reference), ABI-353 (single-frame C4/detail agreement), ABI-342 (recall bridge), ABI-249 (compact high-precision C4 comparator), and ABI-362 (negative decoupled-head result). ABI-363 should be interpreted as capped representative feasibility evidence unless a later trusted whole-validation diagnostic is requested.

## Expected Effect

A useful result would recover some fixed-threshold recall and MIT/source balance while avoiding the broad low-precision footprint seen in recall-heavy variants. Specifically, success can be shown by any of: aggregate filtered Dice near the ABI-353/249 band with higher MIT filtered Dice or recall; better precision/positive-footprint control than ABI-342/362 at comparable recall; improved connected-line continuity without suppressing recall; or a late trajectory that identifies a stable region/detail/line agreement state.

Hard-stop evidence would be contract/resource failure, non-finite behavior, prediction collapse, or a clear regression below ABI-353/249/342/362 across aggregate Dice, both source Dice scores, precision, recall, connectivity, and trajectory behavior.

## Implementation Sketch

The model consumes only provider-approved `abi_16ch_plus_sza` tensors. It normalizes ABI channels 1-16, appends approved-channel BTD planes and Solar Geometry Input transforms, and uses a residual U-Net encoder/decoder with ASPP context and signed-detail high-resolution stems.

The new `SourceRobustDetailSupport` module fuses decoder, stem, and cross-scale skip features, then derives three architecture-internal support streams: axis line-support context from horizontal/vertical depthwise strip convolutions, fine signed-detail residuals, and broader residual contrast. A consensus gate fuses region, line, and tail-detail evidence into refined features. The `DualEvidenceCalibrationHead` predicts a base region logit and adds only a bounded `tanh` support delta through a learned agreement gate. Trusted auxiliary outputs remain `line_logits` and `centerline_logits` for the provider-owned Line and Centerline targets.

Candidate code defines model architecture only. It does not implement data loading, target construction, losses, metrics, Artifact Filters, thresholds, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinate inputs, Dataset Source identity, resource placement, or lifecycle behavior.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza`; no longitude or latitude channels.
- Output form: `mask_logits` with trusted auxiliary `line_logits` and `centerline_logits`.
- Trusted loss: `bce_dice` primary with provider-owned weighted-BCE Line and Centerline auxiliary targets.
- Trusted data policy: `combined_source_balanced` sampling and `random_mirroring` augmentation.
- Optimizer/scheduler: AdamW with constant learning rate.
- Harness-owned fixed threshold, metrics, Artifact Filters, capped selection, execution, resource limits, budget approval, and lifecycle.

## Budget Requested

Request the approved `late_improving` budget: 36 epochs and 10,800 seconds, with exploratory fallback if denied. The request is justified because the relevant single-frame parent branches select late checkpoints: ABI-202 at epoch 34, ABI-353 at epoch 34, ABI-342 at epoch 36, and ABI-362 at epoch 34. The proposed mechanism targets the same late-forming precision/recall/connectivity trade-off while keeping the profiled input, loss, sampling, auxiliaries, optimizer, and batch size.

The manifest keeps ordinary exploratory fields; the candidate-local `budget_request.yaml` asks the Harness to authorize the longer budget.

## Success Criteria

Continue or request diagnostics only if ABI-363 is finite and shows at least one mechanism-positive signal: filtered Dice near or above ABI-353/249; higher fixed-threshold recall than ABI-249 without ABI-342/362-level clutter; improved MIT filtered Dice/source balance; improved connectivity without suppressing recall; or a late trajectory that remains finite and identifies a stable positive-tail support state. Promotion would require later trusted whole-validation diagnostics and human review.

## Fallback/Next Decision

If ABI-363 fails contract/smoke/resource checks because of candidate code, repair the bug while preserving the hypothesis. If it completes but remains below ABI-353/249/342/362 with broad clutter or unstable late behavior, treat this source-agnostic detail-tail support mechanism as non-frontier and broaden to a different architecture family or trusted policy area rather than another local gate-strength/head-weight shuffle. Do not respond by adding Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data selection, temporal lookup, coordinate features, or Dataset Source identity.
