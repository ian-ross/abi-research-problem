# ABI-274 temporal line-state attention U-Net late36

## Hypothesis

ABI-273 showed that moving temporal line evidence upstream into an encoder-injected line state is more useful than ABI-272-style final-head dual evidence: it improved capped temporal-eligible filtered Dice, precision, connectivity, MIT Dice, and Google Dice over ABI-272 while keeping the predicted-positive fraction compact. Its selected checkpoint was the final exploratory epoch and improved over epochs 10 and 11 in aggregate/source Dice, recall, and connectivity. ABI-274 tests whether that exact early-line-state mechanism is being truncated by the 12-epoch exploratory ceiling and can mature under the approved late-improving budget without changing architecture, data policy, loss, augmentation, thresholding, postprocessing, or resource ownership.

Classification: family-development close continuation using the approved `late_improving` budget-request path.

## Comparison Target

Primary comparison target: ABI-273 (`run_20260912_171825_ff0d00`) as the exploratory parent for the exact early-line-state temporal mechanism.

Secondary temporal-family targets: ABI-238 (`run_20260911_004137_f54c45`) as the strongest recent temporal directional-context late36 comparator, ABI-223 (`run_20260908_154531_8c7e2b`) as the temporal-attention comparator, ABI-259 (`run_20260912_012708_f5897e`) and ABI-261 (`run_20260912_031837_f40c59`) as recent temporal line-support comparators, and ABI-272 (`run_20260912_163151_b5c94d`) as the negative final-head dual-evidence comparison. ABI-202 (`run_20260904_043143_ee0005`) remains the aggregate reference, but ABI-274 is capped temporal-eligible feasibility evidence, not a promotion claim.

## Expected Effect

The expected effect is that additional trusted epochs convert ABI-273 final-epoch improvement into a better precision/recall/connectivity balance while preserving source-informative MIT/Google behavior and compact predicted-positive area. Useful evidence would be improved filtered Dice and connectivity over ABI-273, recall moving closer to ABI-223/238 without ABI-271-like precision collapse, and no resource or numerical regression.

## Implementation Sketch

Use the ABI-273 model unchanged except for the Candidate identifier. The model consumes provider-stacked `[-1, 0, 1]` ABI+Solar Geometry Input frames. Its finite per-frame ABI/SZA/BTD feature builder feeds a temporal-attention/change stem, an orientation-aware full-resolution line-state branch, learned `LineStateInjector` gates at each encoder scale, an ASPP decoder, and simple mask/Line/Centerline heads. The manifest remains the same as ABI-273: temporal input, temporal-eligible center selection, source-balanced sampling, random mirroring, BCE-Dice, Line and Centerline auxiliary targets, AdamW, constant learning rate, and batch size 2. The candidate-local `budget_request.yaml` requests the Harness-owned 36-epoch late-improving budget with fallback to exploratory budget if denied.

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
- Budget request: approved `late_improving` request for 36 trusted epochs, fallback `run_exploratory_budget` if denied.

Candidate code does not own data loading, temporal lookup, frame repair, sampling implementation, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

## Budget Requested

Request the approved late-improving budget: 36 epochs and the corresponding trusted timeout through `budget_request.yaml`. The manifest keeps the normal contract fields and does not raise Harness-owned ceilings directly. If the budget request is denied, run the valid exploratory fallback and treat it as bounded evidence.

## Success Criteria

Success for the close continuation would be finite, non-collapsed, source-informative temporal-eligible validation behavior with improved capped filtered Dice over ABI-273 and at least one of: improved connectivity over ABI-273 at a useful recall level, recall approaching ABI-223/238 without precision collapse, materially better MIT/source balance, or a clearer stable trajectory at late epochs. Promotion-level interest would require approaching the ABI-223/238 temporal-family late36 band and narrowing the remaining recall/connectivity gap while preserving compact positive predictions.

## Fallback/Next Decision

If ABI-274 plateaus below ABI-223/238, loses precision through broad positive expansion, or fails to improve connected-line continuity despite the late budget, stop this exact early-line-state injector and broaden away from temporal line-state variants. If it improves materially but remains capped-only evidence, consider a later trusted diagnostic request rather than interpreting capped temporal-eligible validation as whole-validation promotion evidence. If it fails for a candidate bug or contract issue, repair only if the exact ABI-273 hypothesis and comparison target are preserved.
