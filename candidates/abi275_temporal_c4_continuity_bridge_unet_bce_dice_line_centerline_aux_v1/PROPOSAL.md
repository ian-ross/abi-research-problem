# ABI-275 temporal C4 continuity-bridge U-Net

## Hypothesis

ABI-274 validated early temporal line-state attention as a recall/source-balance mechanism on the provider-owned temporal-eligible population, but its failure-bucket review showed the added true-positive evidence was fragmented: filtered Dice tied ABI-223 while recall improved, yet connectivity fell far below ABI-223 and negative-patch clutter broadened. ABI-275 tests whether a compact C4-style continuity bridge can organize ABI-274-style temporal line evidence before the final logits by applying one shared rotated line-support filter at four right-angle orientations, fusing orientation consensus with the carried line state, and gating the residual support into the full-resolution decoder.

Classification: family-development continuation with a mechanism change. This is not an unchanged ABI-273/274 late36 continuation and does not request the late-improving budget on the first altered-architecture scout.

## Comparison Target

Primary comparison target: ABI-274 (`run_20260912_180856_79ba22`) and its temporal-eligible failure-bucket evaluation, because ABI-275 keeps the same temporal input policy, line-state stem, loss, auxiliary targets, and batch size while adding only the C4 continuity bridge.

Secondary temporal-family targets: ABI-223 (`run_20260908_154531_8c7e2b`) as the cleaner temporal-attention connectivity comparator, ABI-255 (`run_20260911_210922_27f346`) as the compact recurrent temporal comparator, and ABI-238 (`run_20260911_004137_f54c45`) as a recent temporal directional-context late36 comparator. ABI-202 remains the aggregate whole-validation reference, and ABI-249 remains the high-precision C4/rotation-aware whole-validation comparator; this run is capped temporal-eligible feasibility evidence, not promotion evidence.

## Expected Effect

The expected effect is higher connected thin-line continuity and cleaner negative-patch behavior than ABI-274 at similar fixed-threshold recall. The shared rotated filter gives a small architecture-level C4 orientation prior without candidate-owned thresholding or postprocessing; the line-state gate should preserve ABI-274's recall/source lift while suppressing unsupported final decoder fragments. A useful exploratory result would improve connectivity over ABI-274 and move toward ABI-223's line-continuity behavior without collapsing recall or expanding predicted-positive area.

## Implementation Sketch

Start from the ABI-274 temporal line-state attention U-Net over provider-stacked `[-1, 0, 1]` ABI+Solar Geometry Input frames. Keep the finite per-frame ABI/SZA/BTD feature builder, temporal attention/change stem, early line-state branch, learned `LineStateInjector` modules at each encoder scale, ASPP context, decoder, and mask/Line/Centerline heads. Add a full-resolution `C4LineContinuityBridge` after the existing high-resolution directional context: it refines decoder features locally, applies one depthwise horizontal line-support kernel to rotations 0/90/180/270 using `torch.rot90`, rotates features back, averages/max-fuses the orientation responses, combines them with the carried temporal line state, and learns a sigmoid residual gate into the decoder feature map. The bridge is differentiable model architecture only.

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
- Exploratory budget: manifest `max_epochs: 12`, batch size 2.

Candidate code does not own data loading, temporal lookup, temporal padding or repair, sample selection, augmentation implementation, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Use the default exploratory budget. The branch changes ABI-274's architecture, so the first run should profile resource behavior and finite learning before any late-improving continuation is considered.

## Success Criteria

Success is finite, non-collapsed, source-informative temporal-eligible validation behavior with at least one of: improved filtered connectivity over ABI-274 without a filtered-recall regression larger than about 0.02; similar or better filtered Dice with lower predicted-positive fraction or higher precision; reduced MIT/Google imbalance; or a final-epoch trajectory suggesting the C4 continuity bridge is promising for a later late-improving continuation. Promotion-level claims require later trusted diagnostics and cannot be made from this capped exploratory run alone.

## Fallback/Next Decision

If ABI-275 improves connectivity while keeping useful recall, consider a late-improving close continuation under the approved budget-request path. If it only lowers recall/precision or broadens clutter without connectivity gain, stop this exact bridge and try a different temporal continuity mechanism, such as a center-frame detail bridge or line-aware recurrent state. Repair only for candidate bugs that preserve this C4 continuity-bridge hypothesis and comparison target.
