# ABI-173 Full-Spectral BTD+SZA Signed-Detail Full-Scale Skip ASPP Decoder BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-154 is the SZA-aware full-scale skip ASPP/detail precision/connectivity branch: it nearly matched ABI-130's capped aggregate Dice while improving precision, connectivity, positive-area discipline, and MIT Dice, but it remained under-recall at the fixed threshold. ABI-155/156 showed that final-head or feature-fusion calibration is not sufficient, ABI-158/171/172 showed that simple auxiliary-weight/loss swaps lose too much precision or connectivity, and ABI-159 showed that a coarse recall bridge expands positives without connected overlap. ABI-173 keeps the ABI-154 family and trusted BCE-Dice policy but changes the high-resolution feature extraction mechanism rather than adding another final-logit calibration patch.

## Hypothesis

Thin contrails can appear as either positive or negative local anomalies depending on ABI channel, BTD plane, background cloud, and Solar Geometry Input. ABI-154's signed-unaware detail stem projects raw local residuals directly, which may force the first learned projection to separate opposite-polarity line evidence while also handling broad cloud context. Splitting local and mid-scale residuals into positive and negative streams before the encoder and high-resolution detail path should make thin-line evidence easier to preserve while the existing full-scale skip fusion and BCE-Dice objective retain ABI-154-like positive-area discipline. The expected useful behavior is modest recall recovery without the precision/connectivity collapse seen in focal-Tversky and coarse-support continuations.

## Comparison Target

The primary comparison target is ABI-154 `abi154_fullspectral_btd_sza_fullscale_skip_aspp_detail_decoder_bce_dice_centerline_aux_v1`, Run `run_20260901_071026_32d3ec`: capped filtered Dice 0.3944, MIT/Google filtered Dice 0.3824/0.4260, filtered precision 0.4777, recall 0.3359, connectivity 0.4374, and filtered predicted-positive fraction 0.00255.

Secondary references are ABI-130 `run_20260831_121006_7d24be` as the SZA-aware ASPP/detail aggregate branch, ABI-156 `run_20260901_090713_9c7d32` as the strongest local feature-calibration continuation, ABI-168 `run_20260901_192929_0da8c3` as a sparse early-oriented ASPP/detail comparison, ABI-171/172 as negative centerline-weight and focal-Tversky full-scale skip continuations, and ABI-068 `run_20260828_010836_4ccc77` as the capped aggregate/source-balance reference. Canonical MCAST 2.1 remains promotion context only.

## Expected Effect

A useful outcome would raise filtered recall by roughly 0.01-0.02 over ABI-154 while keeping aggregate filtered Dice within the ABI-130/154/068 band, preserving MIT and Google filtered Dice above about 0.37 and 0.41 respectively, and keeping filtered precision/connectivity closer to ABI-154 than to ABI-159/172. A stronger outcome would improve MIT recall or aggregate Dice while retaining ABI-154's filtered connectivity and low predicted-positive fraction. A negative outcome would look like another local recall-expansion failure: lower aggregate/source Dice, degraded connectivity, or a large positive-fraction increase without overlap improvement.

## Implementation Sketch

- Reuse ABI-154's approved-channel front end: normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized Solar Geometry Input, cosine SZA feature, and learned 1x1 projection over approved inputs.
- Replace the two raw/detail/broad stems with `SignedDetailContextStem`: raw projection, positive and negative local residual projections at a 7-pixel smoothing scale, positive and negative mid-scale residual projections at a 15-pixel smoothing scale, and a broad 31-pixel context projection.
- Preserve the compact residual encoder, ASPP context, decoder, full-scale skip fusion, line-aware final refinement, primary `mask_logits`, and provider-derived `centerline_logits` auxiliary output.
- Keep trusted `bce_dice` primary loss, trusted `weighted_bce` Centerline Target auxiliary weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant scheduler, disabled early stopping, and one sequential representative capped Run.
- Do not introduce candidate-owned thresholding, Artifact Filters, postprocessing, losses, target derivation, data loading, sampling implementation, augmentation implementation, scheduling, GPU placement, training loops, external persistence, runtime downloads, or pretrained weights.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data claim, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes inside the trusted runtime envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it recovers some ABI-154 recall or MIT overlap while preserving materially more precision/connectivity and positive-area discipline than the negative ABI-159/172 branches.

## Continuation and hard stop

Continue the signed-detail branch only if ABI-173 is finite, non-degenerate, source-informative, and shows a useful recall or source-balance improvement without severe precision/connectivity loss. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. If it completes finite but behaves like another local full-scale skip recall-expansion regression, stop this branch and broaden to a more distinct architecture, data-policy, preprocessing, calibration, or evaluation frontier.

## Fallback/Next Decision

If this candidate fails from a narrow implementation defect while the signed-detail stem hypothesis remains intact, consider at most one explicit Repair Candidate in a later Autonomy Step. If it is scientifically negative, document the result and avoid additional local full-scale skip stem tweaks unless new diagnostics explain why they should avoid the repeated precision/recall/connectivity tradeoff. If it unexpectedly challenges ABI-068/130/154 or combines ABI-154-like precision/connectivity with better recall, request separate whole-validation diagnostics before making any full-data or promotion claim.
