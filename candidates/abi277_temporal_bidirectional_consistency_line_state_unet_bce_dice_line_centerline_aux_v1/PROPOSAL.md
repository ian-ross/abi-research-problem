# ABI-277 temporal bidirectional-consistency line-state U-Net

## Hypothesis

ABI-274 showed that early temporal line-state injection can reach the ABI-223/238 temporal filtered-Dice band and improve recall/source balance, but selected-checkpoint connectivity remains weak. ABI-275 and ABI-276 then showed that a post-decoder C4 bridge or center-frame detail injection does not repair that weakness. ABI-277 tests a different integration point: preserve ABI-274's early line state, but add a separate bidirectional temporal-consistency state built from before/after residual agreement and inject it with the line state at every encoder scale.

Classification: family-development continuation, mechanism-changing relative to ABI-274/275/276.

## Comparison Target

Primary comparison target: ABI-274 (`run_20260912_180856_79ba22`) as the temporal line-state recall/source-balance comparator, with filtered Dice 0.419364, recall 0.389545, and connectivity 0.282911 on temporal-eligible validation.

Secondary targets: ABI-276 (`run_20260912_212900_56562e`) as the negative center-detail injection branch, ABI-275 (`run_20260912_203536_240ad8`) as the negative post-decoder C4 bridge branch, ABI-223 (`run_20260908_154531_8c7e2b`) as the temporal-attention connectivity comparator, ABI-238 (`run_20260911_004137_f54c45`) as the temporal directional-context comparator, ABI-255 (`run_20260911_210922_27f346`) as the recurrent temporal comparator, and ABI-202 (`run_20260904_043143_ee0005`) as the aggregate whole-validation reference. ABI-277 is capped temporal-eligible feasibility evidence, not a promotion claim.

## Expected Effect

The expected effect is better selected-checkpoint line organization than ABI-274/276 without ABI-271-style broad positive expansion. Useful evidence would be finite, source-informative training with filtered Dice above ABI-276 and connectivity above ABI-274/276 at a comparable predicted-positive fraction. A small recall or primary-Dice tradeoff could still be diagnostically useful if it demonstrates that bidirectional before/after agreement selectively suppresses clutter while preserving true thin-line support.

## Implementation Sketch

Start from ABI-274/276's provider-stacked `[-1, 0, 1]` ABI+Solar Geometry Input temporal U-Net pattern. Keep the finite per-frame ABI/SZA/BTD feature builder, temporal-attention/change stem, orientation-aware line state, ASPP decoder, BCE-Dice loss, random mirroring, source-balanced sampling, batch size 2, and trusted Line/Centerline auxiliary heads. Replace the center-detail support branch with a `TemporalConsistencyStem` that computes differentiable architecture-internal features from candidate-visible approved tensors: center-minus-previous, next-minus-center, center-minus-neighbor-mean persistence, next-minus-previous motion, absolute before/after agreement, and before/after imbalance. Pass this consistency state through horizontal, vertical, and dilated orientation filters, then gate it with the temporal line state into each encoder scale and concatenate it into the final high-resolution refinement before the shared mask/Line/Centerline heads.

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

Candidate code does not own data loading, temporal lookup, frame repair, sampling implementation, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Use the default exploratory budget: 12 epochs, trusted 3,600-second timeout, batch size 2, and Harness-owned resource ceilings. This is a mechanism-changing continuation, not an exact late-improving repeat, so no late36 budget is requested.

## Success Criteria

Success would be finite, non-collapsed, source-informative temporal-eligible validation behavior with at least one of: improved connectivity over ABI-274 at useful recall, improved filtered Dice over ABI-276 while preserving compact predicted-positive fraction, better MIT/source balance than ABI-275/276, or a final/late exploratory trajectory that justifies one future close continuation. Promotion-level interest would require approaching ABI-223/238 filtered Dice while narrowing ABI-274's connectivity gap.

## Fallback/Next Decision

If ABI-277 regresses below ABI-276 without improving connectivity or source balance, do not repeat this bidirectional-consistency injection unchanged. If it is finite but mid-run/noisy, write a note and broaden to a different architecture-level evidence-sharpening mechanism rather than requesting late36. If it reaches the ABI-274 primary-Dice band with improved connectivity or recall/source balance, consider a temporal-eligible diagnostic request or one close continuation under the approved late-improving request path. Repair only for candidate bugs that preserve this hypothesis and comparison target.
