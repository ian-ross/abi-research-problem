# ABI-352 full-spectral BTD+SZA C4 cross-scale detail agreement U-Net

## Hypothesis

A single-frame ABI-249-style C4/orientation anchor can recover more fixed-threshold true contrail pixels without ABI-342/343-style broad final-logit residuals if cross-scale decoder evidence, high-resolution center detail, and C4 line context are fused before the final mask head. The specific mechanism is a pre-head cross-scale detail-agreement block that combines full-resolution decoder features, high-resolution signed detail, the stem, and upsampled decoder features from two coarser scales, then uses a learned line/detail agreement gate to inject C4 line context into features rather than adding a candidate-owned threshold or postprocessing rule.

This is a family-development continuation of the single-frame C4/orientation family, not a promotion claim. It is exploratory capped evidence intended to test a mechanism-changing alternative after temporal C4 final-head blends and temporal post-decoder bridges repeatedly decoupled aggregate Dice from connected-line continuity.

## Comparison Target

Primary comparison targets are ABI-249, the compact high-precision single-frame C4/orientation whole-validation comparator, and the recent single-frame C4 recall variants ABI-342/343. Secondary context comes from ABI-202 as the aggregate whole-validation reference and from capped temporal-eligible comparators ABI-350, ABI-324, and ABI-223 for the recall/connectivity tension.

## Expected Effect

Relative to ABI-249, ABI-352 should trade only a small amount of precision for higher recall and better connected thin-line continuity by raising true contrail evidence before the final logits. Relative to ABI-342/343, it should avoid a broad predicted-positive footprint because the support path is feature-level and requires cross-scale detail/line agreement before the mask head. A useful exploratory result would show finite non-collapsed learning, MIT/Google source-informative metrics, and either improved recall/connectivity over ABI-249-like C4 behavior or a clear failure mode that distinguishes pre-head cross-scale detail agreement from final-head residual variants.

## Implementation Sketch

The model consumes provider-approved `abi_16ch_plus_sza` tensors only. It reuses a normalized ABI+Solar Geometry Input front end with ABI-channel-derived BTD planes, a compact U-Net encoder/decoder, and C4 rotation-shared anisotropic line context. The new block fuses full-resolution decoder features, high-resolution signed-detail features, stem features, and projected/upsampled decoder features from two coarser scales. It computes C4 line context on the fused representation and learns a differentiable agreement gate from fused features, line context, and signed detail. The agreed line/detail features are refined before the primary mask, Line, and Centerline heads.

Candidate code defines architecture only. It does not implement data loading, target construction, losses, metrics, Artifact Filters, thresholds, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinate inputs, Dataset Source identity, resource placement, or lifecycle behavior.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza`; no longitude or latitude channels.
- Output form: `mask_logits` with trusted auxiliary `line_logits` and `centerline_logits`.
- Trusted loss: `bce_dice` primary with provider-owned weighted-BCE Line and Centerline auxiliary targets.
- Trusted data policy: `combined_source_balanced` sampling, `all_target_frames` frame selection, and `random_mirroring` augmentation.
- Optimizer/scheduler: AdamW with constant learning rate.
- Harness-owned fixed threshold, metrics, Artifact Filters, capped selection, execution, and lifecycle.

## Budget Requested

Exploratory budget only: 12 epochs, batch size 4, constant learning rate, under the 25M-parameter smoke ceiling. No `late_improving` budget is requested for this first mechanism-changing cross-scale detail-agreement probe.

## Success Criteria

Continue this branch only if the Run is finite and non-collapsed and shows at least one of the following against ABI-249/ABI-342/343-style C4 behavior on the capped validation evidence: higher fixed-threshold recall without a large precision collapse, improved connected-line continuity, better MIT/source balance, reduced complete-miss/low-recall behavior if a diagnostic is later requested, or a late-improving trajectory that plausibly justifies a close-continuation `late_improving` request. Promotion would require later trusted whole-validation diagnostics and human review; this Run alone is capped exploratory evidence.

## Fallback/Next Decision

If ABI-352 collapses, fails contract/smoke/resource checks, or clearly widens clutter without recall/connectivity value, do not repair unless the failure is a candidate bug. If it is finite but inferior, treat it as negative evidence for this pre-head cross-scale detail-agreement mechanism and broaden to a different family such as a modern lightweight backbone with an explicit continuity decoder or a source-agnostic MIT-positive-tail mechanism. Do not respond by adding candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data selection, or coordinate features.
