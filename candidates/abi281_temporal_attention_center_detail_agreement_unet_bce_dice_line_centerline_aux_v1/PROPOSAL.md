# ABI-281 temporal-attention center-detail agreement U-Net

## Hypothesis

ABI-223 remains the temporal-family connectivity comparator, while ABI-274 showed that temporal line-state injection can raise fixed-threshold recall but fragments continuity and adds clutter. ABI-278 then showed that a final oriented line-logit bridge does not recover ABI-223 connectivity or ABI-274 recall. ABI-281 tests a different evidence-sharpening mechanism: preserve ABI-223's compact temporal-attention encoder/decoder, then add a center-frame detail agreement head that compares high-resolution temporal decoder features with provider-visible center-frame ABI/SZA/BTD detail before logits.

Classification: family-development continuation, mechanism-changing relative to ABI-223, ABI-274, and ABI-278.

## Comparison Target

Primary comparison target: ABI-223 (`run_20260908_154531_8c7e2b`) as the temporal-attention connectivity comparator, with temporal-eligible filtered Dice 0.419776, precision 0.483764, recall 0.370738, and connectivity 0.412427.

Secondary targets: ABI-274 (`run_20260912_180856_79ba22`) as the temporal recall/source-balance comparator, ABI-278 (`run_20260912_232028_0c31f7`) as the negative line-logit bridge test, ABI-255 as the recurrent temporal comparator, ABI-249 as the high-precision C4 whole-validation comparator, and ABI-202 as the aggregate whole-validation reference. ABI-281 will produce capped temporal-eligible feasibility evidence, not whole-validation promotion evidence.

## Expected Effect

The expected effect is to raise true center-frame contrail logits at the trusted 0.5 threshold while keeping the cleaner ABI-223 temporal-attention organization. Useful evidence would be finite, non-collapsed, source-informative validation with higher recall than ABI-223 at a smaller connectivity/precision penalty than ABI-274, or similar filtered Dice to ABI-223 with better MIT/source balance. The branch is valuable if it distinguishes whether center-frame detail agreement is a better recall-support location than ABI-278's final oriented logit bridge.

## Implementation Sketch

Start from the provider-stacked `[-1, 0, 1]` ABI+Solar Geometry Input temporal-attention U-Net pattern used by ABI-223: finite per-frame ABI/SZA/BTD feature construction, per-pixel temporal attention over previous/center/next frames, change features, compact U-Net encoder, ASPP bottleneck, and high-resolution decoder. Add `CenterDetailAgreementHead` after the final refinement. The head projects the already constructed center-frame ABI/SZA/BTD features, computes an agreement gate from temporal-refined features, center-detail features, and their absolute difference, fuses the features, and emits a bounded agreement-conditioned residual on `mask_logits`. Line and Centerline auxiliary heads read the same fused features.

This is differentiable model architecture only. It does not threshold predictions, postprocess masks, compute custom metrics, alter losses, implement Artifact Filters, inspect raw temporal cache state, or use coordinates.

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

Success would be finite, non-collapsed, source-informative temporal-eligible validation behavior with at least one of: filtered Dice near ABI-223/274 while improving ABI-223 recall, connectivity clearly above ABI-274/278 at useful recall, MIT filtered Dice/source balance better than ABI-223 without broad negative-patch clutter, or a late exploratory trajectory that justifies one future close continuation through the approved late-improving path. Promotion-level interest would require approaching the ABI-223/238 temporal Dice band while narrowing the recall/connectivity tradeoff.

## Fallback/Next Decision

If ABI-281 regresses below ABI-278 or behaves like another conservative under-coverage head, do not repeat this exact center-detail agreement branch unchanged and broaden to a different temporal evidence-sharpening or non-temporal calibration mechanism. If it is finite but noisy with a final-epoch best and non-degenerate predictions, consider one close continuation through the approved late-improving request path. If it reaches ABI-223/274 primary-Dice with improved recall/connectivity balance, consider a temporal-eligible failure-bucket diagnostic request. Repair only for candidate bugs that preserve this hypothesis and comparison target.
