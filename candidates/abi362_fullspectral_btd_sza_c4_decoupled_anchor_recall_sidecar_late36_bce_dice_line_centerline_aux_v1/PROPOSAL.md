# ABI-362 full-spectral BTD+SZA C4 decoupled anchor/recall-sidecar late36

## Hypothesis

ABI-353 showed that pre-head cross-scale C4/detail agreement can recover positive-tail recall, but the whole-validation diagnostic also showed extra negative-patch clutter, weaker Google transfer, and lower connectivity than ABI-249/ABI-202. ABI-342 and ABI-343 showed the same C4-family coupling problem: recall states are too broad, while compact high-connectivity states suppress recall.

ABI-362 tests a close, mechanism-changing continuation: keep the ABI-353 full-spectral BTD+SZA encoder/decoder and pre-head C4/detail agreement, but split the mask head into (1) a compact C4 anchor logit and (2) a bounded architecture-internal recall sidecar. The sidecar contributes only through a smooth uncertainty band around the anchor logit and a learned line/detail agreement gate. This should preserve ABI-249/ABI-353 compactness while recovering some ABI-353/ABI-342 positive-tail recall without Candidate-owned thresholds or postprocessing.

This is a **family-development continuation**, not a promotion candidate. It changes the mechanism from a single fused agreement logit to a decoupled compact anchor plus gated recall residual.

## Comparison Target

Primary capped-development comparators are ABI-249, ABI-353, ABI-342, and ABI-343. ABI-202 remains the aggregate reference for scientific context. ABI-362 should be judged as capped representative feasibility evidence unless a later trusted whole-validation diagnostic is requested.

## Expected Effect

Expected useful signal is not necessarily beating ABI-202 immediately. A successful result would stay near ABI-353/ABI-249 aggregate filtered Dice while improving at least one C4 trade-off: lower filtered predicted-positive footprint and higher precision than ABI-353 at comparable recall; higher recall than ABI-249 with less compactness/connectivity loss than ABI-353; or improved MIT/source balance without widening Google negative-patch clutter.

Hard-stop evidence would be non-finite behavior, contract/resource failure, prediction collapse, or a clear regression below the recent C4 branch on aggregate Dice, source Dice, precision, recall, and connectivity with no late-improving trajectory.

## Implementation Sketch

The model consumes provider-approved `abi_16ch_plus_sza` tensors only. It reuses ABI-353's normalized full-spectral ABI+Solar Geometry Input front end, approved-channel thermal BTD planes, signed-detail/context stem, residual U-Net encoder/decoder, ASPP bottleneck, and pre-head cross-scale C4/detail agreement module.

The new `DecoupledAnchorRecallSidecarHead` predicts an anchor mask logit from compact C4/context features, predicts a bounded `tanh` recall delta from detail and line context, and adds that delta only through a learned agreement gate and the smooth anchor uncertainty band `4*p*(1-p)`. Trusted auxiliary outputs remain `line_logits` from C4 line context and `centerline_logits` from combined anchor/recall features.

Candidate code defines model architecture only. It does not implement data loading, target construction, losses, metrics, Artifact Filters, thresholds, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinate inputs, Dataset Source identity, resource placement, or lifecycle behavior.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza`; no longitude or latitude channels.
- Output form: `mask_logits` with trusted auxiliary `line_logits` and `centerline_logits`.
- Trusted loss: `bce_dice` primary with provider-owned weighted-BCE Line and Centerline auxiliary targets.
- Trusted data policy: `combined_source_balanced` sampling, `all_target_frames` frame selection, and `random_mirroring` augmentation.
- Optimizer/scheduler: AdamW with constant learning rate.
- Harness-owned fixed threshold, metrics, Artifact Filters, capped selection, execution, resource limits, budget approval, and lifecycle.

## Budget Requested

Request the approved `late_improving` budget: 36 epochs and 10,800 seconds, with exploratory fallback if denied. The request is justified because the immediate single-frame C4/detail parents selected late checkpoints: ABI-353 at epoch 34, ABI-342 at epoch 36, and ABI-343 at epoch 32. The proposed head targets the same late-forming precision/recall/connectivity trade-off while keeping the profiled input, loss, sampling, auxiliary targets, optimizer, and batch size.

The manifest keeps the ordinary exploratory fields; the candidate-local `budget_request.yaml` asks the Harness to authorize the longer budget.

## Success Criteria

Continue or request diagnostics only if ABI-362 is finite and shows at least one of: filtered Dice near or above ABI-353/ABI-249, higher fixed-threshold recall than ABI-249 without ABI-353-level clutter, improved precision/compactness over ABI-353 at comparable recall, improved connected-line continuity, better MIT/source balance, or a late trajectory that identifies a stable compact/connected state. Promotion would require later trusted whole-validation diagnostics and human review.

## Fallback/Next Decision

If ABI-362 fails contract/smoke/resource checks because of candidate code, repair the bug while preserving the hypothesis. If it completes but remains below ABI-249/342/343/353 with broad clutter or unstable connectivity, treat this exact decoupled-head question as answered and broaden away from local C4-head tuning, for example toward a different lightweight line-continuity decoder or source-robust positive-tail support path. Do not respond by adding Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data selection, temporal lookup, or coordinate features.
