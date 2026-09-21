# ABI-353 full-spectral BTD+SZA C4 cross-scale detail agreement late36

## Hypothesis

ABI-352 showed that pre-head cross-scale detail agreement in a single-frame C4/orientation U-Net is finite and still improving at the exploratory boundary, but its useful states were misaligned: epoch 10 was compact/high-connectivity with weak recall, while epoch 12 recovered recall and aggregate Dice but lost compactness and continuity. A late-improving continuation may let the same feature-level agreement mechanism align these states, improving fixed-threshold recall and connected-line continuity without adding candidate-owned thresholds, postprocessing, or final-logit calibration rules.

This is a **family-development continuation**, not a promotion candidate. The goal is to fairly test ABI-352's final-epoch-best trajectory before abandoning the pre-head cross-scale detail-agreement branch.

## Comparison Target

Primary targets are ABI-352 (`run_20260919_044205_9523b3`), ABI-249 as the compact high-precision C4 comparator, and ABI-342/343 as recent C4 recall/precision-veto diagnostics. ABI-202 remains the aggregate whole-validation reference, but ABI-353 will provide capped representative evidence only unless later trusted evaluation is requested.

## Expected Effect

Relative to ABI-352, ABI-353 should improve best filtered Dice beyond the epoch-12 exploratory checkpoint and ideally recover some of the compactness/connectivity seen in ABI-352's earlier epochs while preserving its recall gain over ABI-249. A useful result may be a direct metric improvement, a stronger MIT/source-balanced trajectory, or clear late-budget evidence that the mechanism cannot stabilize recall, compactness, and continuity together.

## Implementation Sketch

The candidate preserves ABI-352's architecture and manifest choices. It consumes provider-approved `abi_16ch_plus_sza` tensors only; derives ABI-channel BTD planes inside the model; uses a compact U-Net encoder/decoder, C4 rotation-shared anisotropic line context, and pre-head cross-scale detail-agreement fusion of full-resolution decoder features, signed detail, stem evidence, and coarser decoder context. The primary `mask_logits` and trusted Line/Centerline auxiliary outputs are unchanged.

Candidate code defines model architecture only. It does not implement data loading, target construction, losses, metrics, Artifact Filters, thresholds, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinate inputs, Dataset Source identity, resource placement, or lifecycle behavior.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza`; no longitude or latitude channels.
- Output form: `mask_logits` with trusted auxiliary `line_logits` and `centerline_logits`.
- Trusted loss: `bce_dice` primary with provider-owned weighted-BCE Line and Centerline auxiliary targets.
- Trusted data policy: `combined_source_balanced` sampling, `all_target_frames` frame selection, and `random_mirroring` augmentation.
- Optimizer/scheduler: AdamW with constant learning rate.
- Harness-owned fixed threshold, metrics, Artifact Filters, capped selection, execution, resource limits, budget approval, and lifecycle.

## Budget Requested

Request the approved `late_improving` budget: 36 epochs and 10,800 seconds, with exploratory fallback if denied. The request is justified because ABI-352 was finite, non-collapsed, source-informative, resource-safe, and selected its best checkpoint at the final exploratory epoch 12. Its learning trajectory was still improving by the selection metric and showed distinct useful states before the exploratory ceiling.

The manifest keeps the ordinary exploratory fields; the candidate-local `budget_request.yaml` asks the Harness to authorize the longer budget.

## Success Criteria

Continue or request diagnostics only if ABI-353 is finite and shows at least one of: improved capped filtered Dice over ABI-352, higher fixed-threshold recall without a large precision collapse, improved connected-line continuity, better MIT/source balance, or a late trajectory that identifies a stable compact/connected state. Promotion would require later trusted whole-validation diagnostics and human review.

## Fallback/Next Decision

If ABI-353 fails contract/smoke/resource checks because of candidate code, repair the bug while preserving the hypothesis. If it completes but remains below ABI-249/342/343 with broad clutter or unstable connectivity, treat the late-budget question as answered and broaden to a different mechanism, such as a lightweight backbone with explicit continuity decoding or a source-agnostic MIT-positive-tail support path. Do not respond by adding candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data selection, or coordinate features.
