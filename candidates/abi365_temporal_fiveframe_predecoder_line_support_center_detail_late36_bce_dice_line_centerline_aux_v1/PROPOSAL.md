# ABI-365 temporal five-frame pre-decoder line-support center-detail late36

## Hypothesis

Recent temporal Runs show a three-way tension: ABI-350's three-frame temporal-attention pre-decoder line support gives the strongest local capped temporal-eligible aggregate Dice but remains below ABI-223/324 on connected-line continuity; ABI-348/324 five-frame C4 variants provide useful compactness/balance but their final-head blends decouple fixed-threshold Dice from connected-line evidence; ABI-356/360 broad recall states recover positives by widening the footprint.

ABI-365 tests a mechanism-changing but close temporal-family continuation: keep ABI-350's successful pre-decoder orientation line-support idea, but move to provider-owned five-frame offsets `[-2, -1, 0, 1, 2]` and build center-anchored near/far temporal-change evidence before decoder fusion. The hypothesis is that five-frame persistence can raise true continuous contrail evidence in encoder/skip features before final logits, improving connectivity and MIT/source-balanced recall without another final-head residual, Candidate-owned threshold, postprocessing, or data-policy workaround.

This is a **family-development continuation**, not a promotion claim. It is bounded temporal-eligible capped evidence unless later trusted diagnostics are justified.

## Comparison Target

Primary temporal-eligible capped comparators are ABI-350 (three-frame temporal-attention pre-decoder line support), ABI-324 (balanced five-frame C4/detail-consensus comparator), ABI-348 (compact five-frame C4 dual-state blend), ABI-223 (temporal-attention connectivity comparator), and ABI-356/360 (recall-heavy temporal attention diagnostics). Whole-validation roles remain ABI-202 as aggregate reference and ABI-249 as compact high-precision C4 comparator, but ABI-365 should not be interpreted as whole-validation promotion evidence.

## Expected Effect

A useful result would preserve ABI-350-like compact aggregate performance while improving one or more of: filtered connectivity toward ABI-223/324, positive-tail recall without ABI-356/360-style footprint broadening, MIT filtered Dice/source balance, or negative-patch high-tail clutter relative to broad recall sidecars. Because ABI-350 selected epoch 33 and five-frame parents are late-budget dependent, a late-improving budget is requested.

Hard-stop evidence would be contract/resource failure, non-finite behavior, prediction collapse, clear wall-clock incompatibility, or a completed trajectory that is below ABI-350/324/348/223 across aggregate Dice, both source Dice scores, precision, recall, connectivity, footprint, and learning behavior.

## Implementation Sketch

The model consumes only provider-advertised `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-2, -1, 0, 1, 2]`. Candidate code reshapes the channel-stacked tensor into five frames but does not locate, load, pad, duplicate, or repair temporal data.

For each frame it normalizes ABI channels 1-16, appends approved-channel BTD planes and Solar Geometry Input transforms, then projects each frame through a shared compact residual stem. A center-anchored temporal-attention stem forms per-pixel five-frame attention weights and near/far change features (`center - near_mean`, `center - far_mean`, neighbor differences, and absolute center-neighbor residuals). A compact encoder/ASPP decoder follows. Orientation-aware line-support blocks are injected into encoder skips before decoder fusion, so continuity evidence is present before final mask logits rather than as a post-hoc residual. Trusted auxiliary outputs remain `line_logits` and `centerline_logits`.

Candidate code defines architecture only. It does not implement data loading, target construction, losses, metrics, Artifact Filters, thresholds, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinate inputs, Dataset Source identity, resource placement, or lifecycle behavior.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`; no longitude or latitude channels.
- Data policy: trusted `temporal_eligible_center` frame selection with allowlisted offsets `[-2, -1, 0, 1, 2]`, `combined_source_balanced` sampling, and `random_mirroring` augmentation.
- Output form: `mask_logits` with trusted auxiliary `line_logits` and `centerline_logits`.
- Trusted loss: `bce_dice` primary with provider-owned weighted-BCE Line and Centerline auxiliaries.
- Optimizer/scheduler: AdamW with constant learning rate and batch size 2.
- Harness-owned fixed threshold, metrics, Artifact Filters, capped selection, execution, resource limits, budget approval, and lifecycle.

## Budget Requested

Request the approved `late_improving` budget for 36 epochs with fallback to exploratory if denied. The request is tied to parent evidence: ABI-350 selected epoch 33 after a much weaker exploratory-boundary checkpoint; ABI-348 selected epoch 36; ABI-324 selected epoch 27; ABI-223 selected epoch 36. The five-frame input/resource class has prior bounded resource evidence, and this candidate remains compact with the same batch size 2 temporal policy.

## Success Criteria

Continue or request diagnostics only if ABI-365 is finite and shows a mechanism-positive signal: connectivity closer to ABI-223/324 while maintaining ABI-350-like aggregate/source Dice; improved MIT/source-balanced recall without broadening footprint into ABI-356/360 territory; lower negative-patch high-tail clutter than broad recall sidecars; or a late trajectory that is improving and non-degenerate. Promotion would require later trusted whole-validation/temporal diagnostics and human review.

## Fallback/Next Decision

If ABI-365 fails contract/smoke/resource checks because of candidate code, repair the bug while preserving the hypothesis. If it completes but behaves like another low-recall compact state or broad low-precision recall state, treat this exact five-frame pre-decoder line-support variant as non-frontier and broaden to a different temporal alignment/backbone, single-frame C4/detail mechanism, or trusted policy/loss direction tied to a specific failure mode. Do not respond by adding Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data selection, temporal lookup, coordinate features, or Dataset Source identity.
