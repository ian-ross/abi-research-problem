# ABI-364 full-spectral BTD+SZA line-token detail U-Net

## Hypothesis

Recent capped Runs show a persistent fixed-threshold trade-off. ABI-249-style C4/orientation models are compact and precise but recall-limited; ABI-342/360-style recall support broadens predictions; ABI-362/363 local single-frame head changes did not recover MIT/source balance or connected recall. ABI-340 also showed that a final low-cost line-consensus head on a SegFormer-like branch improved connectivity only by sacrificing too much recall and source Dice.

ABI-364 tests a different in-contract mechanism: inject low-rank row/column line-token support and local strip context inside a compact full-spectral BTD+SZA U-Net decoder before final logits, then use a bounded agreement head to combine region, line-token, and signed-detail evidence. The hypothesis is that continuity support applied before final logit formation can raise connected true-contrail evidence without another candidate-owned threshold, postprocessing step, or local C4 tail-sidecar shuffle.

This is a **family-development continuation / lightweight decoder scout**, not a promotion claim. It is intentionally exploratory rather than late-budget because the exact line-token decoder resource and optimization behavior are not yet characterized.

## Comparison Target

Primary capped-development comparators are ABI-202 (aggregate reference), ABI-249 (compact high-precision C4 comparator), ABI-353/362/363 (recent single-frame C4/detail-tail continuations), ABI-342 (recall bridge), and ABI-340 (low-cost line-consensus modern-backbone result). ABI-364 should be interpreted as capped representative feasibility evidence only unless later trusted diagnostics are justified.

## Expected Effect

A useful result would show at least one mechanism-positive signal: higher connected-line continuity than ABI-363/362 without their MIT/source regression, a better precision/recall/footprint balance than ABI-342, recall closer to ABI-202 while preserving ABI-249-like compactness, or a finite improving trajectory at epoch 12 that justifies a close continuation. The line-token bridge should preferably improve connectivity without entering the very low-recall high-precision state observed in several C4 and SegFormer variants.

Hard-stop evidence would be contract/resource failure, non-finite behavior, prediction collapse, clear wall-clock incompatibility, or a completed trajectory that is below ABI-340/342/353/362/363 across aggregate Dice, both source Dice scores, precision, recall, connectivity, footprint, and learning behavior.

## Implementation Sketch

The model consumes only provider-approved `abi_16ch_plus_sza` tensors. It normalizes ABI channels 1-16, appends approved-channel BTD planes and Solar Geometry Input transforms, and uses a compact residual U-Net with ASPP bottleneck context.

The new `LineTokenDetailBridge` fuses full-resolution decoder features, high-resolution signed-detail features, and upsampled mid-level decoder features. It derives row tokens by averaging features along width, column tokens by averaging along height, and local horizontal/vertical strip features with depthwise convolutions. These are model features only, not morphology, thresholding, or postprocessing. A learned agreement map gates line-token and signed-detail support before a bounded `tanh` delta is added to base region logits. Trusted auxiliary outputs remain `line_logits` and `centerline_logits` for provider-owned Line and Centerline targets.

Candidate code defines model architecture only. It does not implement data loading, target construction, losses, metrics, Artifact Filters, thresholds, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinate inputs, Dataset Source identity, resource placement, or lifecycle behavior.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza`; no longitude or latitude channels.
- Output form: `mask_logits` with trusted auxiliary `line_logits` and `centerline_logits`.
- Trusted loss: `bce_dice` primary with provider-owned weighted-BCE Line and Centerline auxiliary targets.
- Trusted data policy: `combined_source_balanced` sampling and `random_mirroring` augmentation.
- Optimizer/scheduler: AdamW with constant learning rate.
- Harness-owned fixed threshold, metrics, Artifact Filters, capped selection, execution, resource limits, budget approval, and lifecycle.

## Budget Requested

Use the default exploratory budget: 12 epochs, 3,600-second exploratory timeout, batch size 4, and the Harness-owned sample/resource ceilings. No `late_improving` request is included because this exact line-token detail decoder has not yet produced finite late-selecting evidence. If it completes with a finite, still-improving epoch-12 trajectory and a mechanism-positive trade-off, a future close continuation can request the approved late-improving budget.

## Success Criteria

Continue or request diagnostics only if ABI-364 is finite and shows a mechanism-positive signal: connectivity improvement without recall collapse; aggregate/source filtered Dice close to ABI-353/249 while improving recall or footprint; improved MIT/source balance versus ABI-362/363; or a late exploratory trajectory that is improving and non-degenerate. Promotion would require later trusted whole-validation diagnostics and human review.

## Fallback/Next Decision

If ABI-364 fails contract/smoke/resource checks because of candidate code, repair the bug while preserving the hypothesis. If it completes but behaves like another low-recall compact head or broad low-precision recall state, treat this exact row/column line-token bridge as non-frontier and broaden to a different architecture family or trusted policy area. Do not respond by adding Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data selection, temporal lookup, coordinate features, or Dataset Source identity.
