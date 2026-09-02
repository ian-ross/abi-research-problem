# ABI-176 Full-Spectral BTD+SZA Signed Context-Fusion ASPP Decoder BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-173 is now the strongest whole-validation-tested SZA-aware ASPP/detail aggregate branch, but its signed-detail recall recovery came with lower precision, lower connectivity, and materially more negative-patch clutter than ABI-154. ABI-174's late line-consensus calibration recovered only a small amount of connectivity while reducing aggregate overlap, and ABI-175's anti-aliased downsampling became too conservative. ABI-176 keeps the useful signed-detail front end from ABI-173 but moves the next change earlier into feature fusion rather than adding another final-logit or post-refinement patch.

## Hypothesis

ABI-173's signed positive/negative detail streams recover missed thin contrails, but the final fusion treats signed high-resolution detail, decoder output, stem features, and full-scale context as unconstrained peers. This may allow local detail anomalies to become false positives on negative patches before sufficient broader context is incorporated. A neutral context-balanced fusion module should preserve ABI-173's signed-detail recall while modestly improving precision, connectivity, and positive-area discipline by letting decoder/stem/full-scale context calibrate high-resolution signed detail before the existing line-aware refinement.

## Comparison Target

The primary comparison target is ABI-173 `abi173_fullspectral_btd_sza_signed_detail_fullscale_skip_aspp_decoder_bce_dice_centerline_aux_v1`, Run `run_20260901_234732_bd5917`, with capped filtered Dice 0.3962, MIT/Google filtered Dice 0.3838/0.4269, filtered precision 0.4238, recall 0.3720, connectivity 0.3203, and filtered predicted-positive fraction 0.00318. Its whole-validation diagnostic reached filtered Dice 0.3973, MIT/Google filtered Dice 0.3870/0.4161, precision 0.4263, recall 0.3719, connectivity 0.3197, and documented increased negative-patch false-positive burden versus ABI-154.

Secondary references are ABI-154 `run_20260901_071026_32d3ec` as the SZA-aware full-scale skip precision/connectivity branch, ABI-130 `run_20260831_121006_7d24be` as the prior SZA-aware ASPP/detail aggregate branch, ABI-174 `run_20260902_005632_5651ef` as the failed post-refinement line-consensus variant, ABI-175 `run_20260902_015941_3ebc45` as the failed anti-aliased-downsampling variant, and ABI-068 `run_20260828_010836_4ccc77` as the broader capped aggregate/source-balance comparator. Canonical MCAST summaries remain context only.

## Expected Effect

A useful outcome would keep aggregate filtered Dice in the ABI-068/130/154/173 band while reducing ABI-173's false-positive tendency: higher filtered precision or connectivity, lower filtered predicted-positive fraction, and no major recall loss. A strong outcome would keep ABI-173-like recall above about 0.36, recover connectivity toward ABI-130/154, and preserve source-stratified filtered Dice above roughly 0.38 MIT and 0.41 Google. A negative outcome would show the familiar local-fusion failure mode: reduced aggregate/source Dice, degraded connectivity, or excessive positive-area expansion without overlap gain.

## Implementation Sketch

- Reuse ABI-173's approved input and front end: normalized GOES ABI channels 1-16, deterministic thermal BTD planes from approved ABI channels, normalized Solar Geometry Input, cosine SZA feature, and learned 1x1 projection over approved inputs.
- Preserve ABI-173's signed local and mid-scale detail stems, compact residual encoder, ASPP context, decoder, full-scale skip aggregation, line-aware final refinement, primary `mask_logits`, and provider-derived `centerline_logits` auxiliary output.
- Replace the direct `concat(dec0, detail, stem, fullscale)` final projection with a `SignedContextFusion` module. It projects decoder, signed-detail, stem, and full-scale features to a shared width; computes a neutral feature-space gate from decoder/stem/full-scale/broad context; applies only a bounded 0.85-1.15 calibration to signed detail; adds horizontal and vertical detail-context branches; and fuses those features before the existing line-aware refinement.
- Keep trusted `bce_dice` primary loss, trusted `weighted_bce` Centerline Target auxiliary weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant scheduler, disabled early stopping, and one sequential representative capped Run.
- Do not introduce candidate-owned thresholding, Artifact Filters, postprocessing, losses, target derivation, data loading, sampling implementation, augmentation implementation, scheduling, GPU placement, training loops, external persistence, runtime downloads, or pretrained weights.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data claim, Experiment Batch, Post-Run Evaluation, or promotion decision is requested in this handoff.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes inside the trusted runtime envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it preserves most ABI-173 recall while improving at least one of precision, connectivity, predicted-positive discipline, or source balance without falling clearly below the ABI-130/154/173 aggregate band.

## Continuation and hard stop

Continue this signed-detail/context-fusion branch only if it is finite, non-degenerate, source-informative, and demonstrates a better precision/recall/connectivity trade-off than ABI-173 or a diagnostically useful source-specific difference. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. If it completes finite but behaves like another local full-scale skip fusion regression, stop this branch and broaden to a more distinct architecture, data-policy, preprocessing, calibration, or evaluation frontier.

## Fallback/Next Decision

If the candidate fails from a narrow implementation defect while the context-balanced signed-detail hypothesis remains intact, consider at most one explicit Repair Candidate in a later Autonomy Step. If it is scientifically negative, document the result and avoid further local signed-detail/full-scale fusion tweaks unless new diagnostics identify a fixable failure mode. If it challenges ABI-068/130/154/173 or combines ABI-173-like recall with ABI-154-like precision/connectivity, request separate whole-validation diagnostics before making any full-data or promotion claim.
