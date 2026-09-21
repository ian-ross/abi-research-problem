# ABI-278 temporal-attention line-logit bridge U-Net

## Hypothesis

ABI-274 showed that early temporal line-state injection can raise temporal-eligible recall/source balance into the ABI-223/238 primary-Dice band, but its selected-checkpoint connectivity remains weak. ABI-275/276/277 then showed that adding later temporal suppressor, full-resolution C4 bridge, center-detail, or bidirectional-consistency states to the ABI-274 line-state path does not reliably repair connected thin-line continuity. ABI-278 returns to the cleaner ABI-223 temporal-attention family and tests a narrower architecture-level evidence-sharpening mechanism: preserve the compact temporal-attention U-Net, then add a learned oriented line-evidence bridge that contributes a bounded residual directly to `mask_logits` before the trusted threshold.

Classification: family-development continuation, mechanism-changing relative to ABI-223 and ABI-274/275/276/277.

## Comparison Target

Primary comparison target: ABI-223 (`run_20260908_154531_8c7e2b`) as the temporal-attention connectivity comparator, with filtered Dice 0.419776, precision 0.483764, recall 0.370738, and connectivity 0.412427 on temporal-eligible validation.

Secondary targets: ABI-274 (`run_20260912_180856_79ba22`) as the temporal recall/source-balance comparator, ABI-238 (`run_20260911_004137_f54c45`) as the temporal directional-context comparator, ABI-255 (`run_20260911_210922_27f346`) as the recurrent temporal comparator, ABI-277 (`run_20260912_222529_d1a74a`) as the negative bidirectional-consistency branch, ABI-249 as the high-precision C4 whole-validation comparator, and ABI-202 as the aggregate whole-validation reference. ABI-278 will produce capped temporal-eligible feasibility evidence, not whole-validation promotion evidence.

## Expected Effect

The expected effect is to preserve ABI-223-style temporal-attention precision/connectivity while raising true thin-line evidence that ABI-223 leaves below threshold 0.5. Useful evidence would be finite, source-informative validation with higher recall than ABI-223 at a smaller connectivity penalty than ABI-274, or similar filtered Dice to ABI-223 with improved MIT/source balance. A modest primary-Dice result can still be useful if the line-logit residual reveals whether oriented support should be used as a logit evidence bridge rather than as an encoder/decoder suppressor.

## Implementation Sketch

Start from the provider-stacked `[-1, 0, 1]` ABI+Solar Geometry Input temporal-attention U-Net pattern used by ABI-223: finite per-frame ABI/SZA/BTD feature construction, per-pixel temporal attention over previous/center/next frames, change features, compact U-Net encoder, ASPP bottleneck, and high-resolution decoder. Add `OrientedLineLogitBridge` after the final high-resolution refinement. The bridge applies one shared horizontal line-support filter to the final feature map under four right-angle rotations, unrotates the responses, fuses mean and peak support with the original features, and emits a bounded gated residual added to the region `mask_logits`. Trusted Line and Centerline auxiliary heads read the same bridge features so the auxiliary targets can shape the support branch without defining new losses or labels.

This is differentiable model architecture only. It does not threshold predictions, postprocess masks, compute custom metrics, alter losses, implement Artifact Filters, or inspect raw temporal cache state.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Provider-owned frame selection: `temporal_eligible_center`.
- Allowed temporal frame offsets: `[-1, 0, 1]`.
- Output form: `mask_logits` with trusted auxiliary `line_logits` and `centerline_logits`.
- Trusted sampling policy: `combined_source_balanced`.
- Trusted augmentation policy: `random_mirroring`.
- Trusted primary loss: `bce_dice`.
- Trusted auxiliary loss: `weighted_bce` for Line and Centerline targets.
- Optimizer/scheduler: AdamW with constant learning rate.

Candidate code does not own data loading, temporal lookup, frame repair, sample selection, sampling implementation, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Use the default exploratory budget: 12 epochs, trusted 3,600-second timeout, batch size 2, and Harness-owned resource ceilings. This is a mechanism-changing continuation, not an exact late-improving repeat, so no late36 budget is requested.

## Success Criteria

Success would be finite, non-collapsed, source-informative temporal-eligible validation behavior with at least one of: filtered Dice near ABI-223/274 while improving ABI-223 recall, connectivity clearly above ABI-274/277 at useful recall, MIT filtered Dice/source balance better than ABI-223 without broad negative-patch clutter, or a late exploratory trajectory that justifies one future close continuation. Promotion-level interest would require approaching the ABI-223/238 temporal Dice band while narrowing the recall/connectivity tradeoff.

## Fallback/Next Decision

If ABI-278 regresses below ABI-277 or behaves like another conservative suppressor, do not repeat this logit-bridge branch unchanged and broaden away from temporal suppressor/evidence bridges. If it is finite but noisy with late improvement and non-degenerate predictions, consider a close continuation through the approved late-improving request path. If it reaches ABI-223/274 primary-Dice with improved recall/connectivity balance, consider a temporal-eligible failure-bucket diagnostic request. Repair only for candidate bugs that preserve this hypothesis and comparison target.
