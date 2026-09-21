# ABI-276 temporal line-state center-detail U-Net

## Hypothesis

ABI-274 showed that early temporal line-state injection can reach the ABI-223/238 temporal filtered-Dice band and improve recall/source balance, but its selected-checkpoint connectivity remains weak. ABI-275 then showed that appending a full-resolution C4 continuity bridge after the decoder does not repair that weakness. ABI-276 tests a different integration point: preserve ABI-274's early temporal line-state mechanism while injecting center-frame high-resolution detail evidence at every encoder scale and into the final refinement, so temporal support is anchored to center-frame thin structures before logits are formed.

Classification: family-development continuation, mechanism-changing relative to ABI-274/275.

## Comparison Target

Primary comparison target: ABI-274 (`run_20260912_180856_79ba22`) as the strongest recent temporal line-state comparator and recall/source-balance temporal diagnostic Result.

Secondary targets: ABI-275 (`run_20260912_203536_240ad8`) as the negative post-decoder C4 bridge test, ABI-254 (`run_20260911_202724_fee837`) as the earlier center-detail bridge over temporal attention, ABI-223 (`run_20260908_154531_8c7e2b`) as the temporal-attention connectivity comparator, ABI-238 (`run_20260911_004137_f54c45`) as the temporal directional-context comparator, ABI-255 (`run_20260911_210922_27f346`) as the recurrent temporal comparator, and ABI-202 (`run_20260904_043143_ee0005`) as the aggregate whole-validation reference. ABI-276 is capped temporal-eligible feasibility evidence, not a promotion claim.

## Expected Effect

The expected effect is better fixed-threshold connected-line organization than ABI-274/275 without ABI-271-style broad positive expansion. Useful evidence would be finite, source-informative training with filtered Dice near the temporal comparator band and improved connectivity or precision at a comparable recall and filtered predicted-positive fraction. A small primary-Dice loss could still be diagnostically useful if connectivity improves clearly while recall remains competitive.

## Implementation Sketch

Start from ABI-274's provider-stacked `[-1, 0, 1]` ABI+Solar Geometry Input temporal architecture. Keep the finite per-frame ABI/SZA/BTD feature builder, temporal-attention/change stem, orientation-aware line state, ASPP decoder, BCE-Dice loss, random mirroring, source-balanced sampling, batch size 2, and trusted Line/Centerline auxiliary heads. Add a center-frame detail stem that computes local center-frame residuals from approved normalized ABI/SZA/BTD features, forms a compact orientation-aware detail state, and gates that state together with the temporal line state into each encoder scale. Also concatenate the full-resolution detail state into the final refinement before the shared mask/Line/Centerline heads.

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

Success would be finite, non-collapsed, source-informative temporal-eligible validation behavior with at least one of: improved connectivity over ABI-274 at useful recall, improved filtered Dice over ABI-275 while preserving compact predicted-positive fraction, better MIT/source balance than ABI-254/275, or a final/late exploratory trajectory that justifies one future close continuation. Promotion-level interest would require approaching ABI-223/238 filtered Dice while narrowing ABI-274's connectivity gap.

## Fallback/Next Decision

If ABI-276 regresses below ABI-274 without improving connectivity or source balance, do not repeat this center-detail injection unchanged. If it is finite but mid-run/noisy, write a note and broaden to a different architecture-level evidence-sharpening mechanism rather than requesting late36. If it is best-at-final with improved connectivity or recall/source balance, consider one close continuation under the approved late-improving request path. Repair only for candidate bugs that preserve this hypothesis and comparison target.
