# ABI-282 temporal C4 detail-continuity U-Net

## Hypothesis

ABI-274 showed that early temporal line-state evidence can raise fixed-threshold recall and source coverage, but its masks remain fragmented and cluttered. ABI-281 showed that a post-decoder center-frame detail agreement head improves over ABI-278 but still lacks enough line organization to approach ABI-223/274. ABI-282 tests a mechanism-changing temporal-family continuation: keep the compact ABI-223/281 temporal-attention encoder/decoder, but organize the final high-resolution temporal/detail features with a C4 rotation-shared line-context head before logits.

Classification: family-development continuation, mechanism-changing relative to ABI-223, ABI-274, ABI-278, and ABI-281.

## Comparison Target

Primary comparison targets are ABI-223 (`run_20260908_154531_8c7e2b`) as the temporal-attention connectivity comparator and ABI-274 (`run_20260912_180856_79ba22`) as the temporal recall/source-balance comparator. Secondary targets are ABI-281 as the negative center-detail agreement integration, ABI-249/279/280 as C4 whole-validation precision/recall tradeoff comparators, and ABI-202 as the aggregate whole-validation reference. ABI-282 will produce capped temporal-eligible feasibility evidence only, not whole-validation promotion evidence.

## Expected Effect

The expected effect is to preserve more of ABI-274's recall/source lift while improving connected thin-line continuity and avoiding ABI-281's broad low-precision final-epoch instability. Useful evidence would be finite, non-collapsed temporal-eligible validation with filtered Dice moving back toward the ABI-223/274 band, connectivity clearly above ABI-274/281 at useful recall, or improved MIT/source balance without broadening negative-patch clutter.

## Implementation Sketch

Use provider-stacked `[-1, 0, 1]` ABI+Solar Geometry Input temporal tensors. Build finite per-frame ABI/SZA/BTD features from provider-visible channels, fuse previous/center/next frames with lightweight temporal attention and change features, encode/decode with a compact U-Net and ASPP bottleneck, then project center-frame detail features into the final high-resolution decoder width. The new `C4DetailContinuityHead` seeds a fused temporal/detail feature, applies a rotation-shared anisotropic strip-context block over the four C4 rotations, gates line-context evidence against center-frame detail, and emits bounded mask-logit residual/veto terms plus trusted Line and Centerline auxiliary logits.

This is model architecture only. It does not own temporal lookup, data loading, sample selection, augmentation implementation, losses, metrics, Artifact Filters, thresholding, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Provider-owned frame selection: `temporal_eligible_center`.
- Allowed temporal frame offsets: `[-1, 0, 1]`.
- Output form: `mask_logits` with trusted `line_logits` and `centerline_logits` auxiliary outputs.
- Trusted sampling policy: `combined_source_balanced`.
- Trusted augmentation policy: `random_mirroring`.
- Trusted primary loss: `bce_dice`.
- Trusted auxiliary loss: `weighted_bce` for Line and Centerline targets.
- Optimizer/scheduler: AdamW with constant learning rate.

## Budget Requested

Use the default exploratory budget: 12 epochs, trusted 3,600-second timeout, batch size 2, fixed prediction retention, and Harness-owned resource ceilings. No late36 budget is requested because this is a mechanism-changing continuation rather than a close repeat with prior late-improving evidence.

## Success Criteria

Success would be finite, non-collapsed, source-informative temporal-eligible behavior with at least one of: filtered Dice near ABI-223/274 while improving ABI-274 connectivity, recall above ABI-223 with a smaller connectivity/precision penalty than ABI-274, MIT filtered Dice/source balance better than ABI-223, or a late non-degenerate trajectory that justifies one future close continuation through the approved late-improving path. Promotion-level interest would require approaching the ABI-223/238/274 temporal Dice band while narrowing the recall/connectivity/clutter tradeoff.

## Fallback/Next Decision

If ABI-282 regresses to ABI-281-like low Dice or unstable broad clutter, do not repeat this C4 detail-continuity head unchanged. If it is finite but near ABI-274 with improved connectivity or source balance and a late-improving trajectory, consider a close late36 continuation. If it reaches the temporal comparator band with better recall/connectivity balance, request temporal-eligible failure-bucket diagnostics. Repair only for candidate bugs that preserve this hypothesis and comparison target.
