# ABI-146 Full-Spectral BTD+SZA Frequency-Support ASPP/Detail Decoder BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-130 established the strongest whole-validation-tested ASPP/detail SZA-calibrated branch: full-validation filtered Dice 0.3954 with improved recall versus ABI-126, but lower connectivity and more negative-patch clutter than ABI-126/ABI-066. Several small SZA-aware ASPP/detail head, auxiliary, traversal, gate, attention, and loss changes did not improve on ABI-130. ABI-146 keeps ABI-130's trusted input/loss/data/training policy fixed and changes only the architecture by adding a non-suppressive frequency-support feature residual before the output heads.

## Hypothesis

A bounded additive frequency-support path can recover some line continuity and negative-patch discipline that ABI-130 lost relative to ABI-126/ABI-066 while preserving ABI-130's default-threshold SZA recall gain. The expected useful mechanism is not a candidate-owned threshold, postprocessor, Artifact Filter, loss, target transform, or sampling change. It is a feature-space bridge that exposes high-frequency detail, low-frequency cloud context, horizontal/vertical ribbon context, and dilated local context to the final heads without multiplicatively suppressing the mask evidence.

## Comparison Target

The primary comparison target is ABI-130 `abi130_fullspectral_btd_aspp_detail_decoder_sza_bce_dice_centerline_aux_v1`, Run `run_20260831_121006_7d24be`: capped filtered Dice 0.3953, MIT/Google filtered Dice 0.3779/0.4404, filtered precision 0.4415, filtered recall 0.3578, filtered connectivity 0.3851, and filtered predicted-positive fraction 0.00294. Its whole-validation diagnostic `eval_evalreq_abi130_wholeval_failure_buckets_v1` confirmed filtered Dice 0.3954, precision 0.4436, recall 0.3566, connectivity 0.3935, and a real but bounded clutter increase relative to ABI-126.

Secondary references are ABI-126 `run_20260831_085615_d05ab3` as the ASPP/detail high-precision/connectivity comparator, ABI-066 `run_20260827_230540_bf4ce3` as the high-connectivity BCE-Dice-clDice reference, ABI-068 `run_20260828_010836_4ccc77` as the local capped aggregate/source-balance reference, and ABI-143 `run_20260831_224534_27b73d` as the closest SZA-aware ridge-family BCE-Dice continuation. Canonical MCAST summaries remain full Working Validation Split context, not promotion authority for this capped candidate.

## Expected Effect

A useful result would keep ABI-130-like aggregate filtered Dice while improving filtered connectivity, precision, or negative-patch discipline, or would improve MIT recall/source balance without the Google-Dice and connectivity loss observed in ABI-145. Because the residual is additive and bounded in feature space rather than a final multiplicative gate, it should avoid the recall suppression seen in ABI-144. A negative result would show that frequency/detail support around the ASPP/detail branch behaves like prior local head/gate changes and fails to improve the ABI-130 trade-off.

## Implementation Sketch

- Reuse ABI-130's provider-approved `abi_16ch_plus_sza` front end: normalized ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized SZA, `cos(SZA)`, and a learned 1x1 channel mixer.
- Reuse the compact ASPP/detail encoder-decoder: high-resolution detail/context stem, residual encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail fusion, and line-aware refinement.
- Add `FrequencySupportFusion` after line-aware refinement. It derives high-frequency residual features (`x - smooth9(x)`), low-frequency context (`smooth25(x)`), horizontal and vertical 21-pixel ribbon context, and a dilation-3 local context branch from the decoded feature map.
- Fuse those views through Conv/GroupNorm/GELU residual blocks and add `0.15 * tanh(delta)` back to the refined features before the primary and auxiliary heads. This is bounded feature fusion, not thresholding, postprocessing, or Artifact Filtering.
- Emit primary `mask_logits` and trusted auxiliary `centerline_logits` from the fused feature map.
- Preserve trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision with trusted `weighted_bce` weight 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.
- Request one sequential Run only; no Experiment Batch or candidate-owned scheduling/resource placement is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data evidence, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it improves ABI-130 filtered connectivity, precision, negative-patch discipline, MIT recall, or aggregate/source-stratified filtered Dice without a large recall or Google-Dice regression.

## Continuation and hard stop

Continue this branch only if ABI-146 is finite, non-degenerate, source-informative, and improves at least one ABI-130-relative diagnostic without creating a severe compensating loss: connectivity, precision, clutter discipline, MIT recall, aggregate filtered Dice, source balance, or late-epoch trajectory. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. A finite result clearly below ABI-130/ABI-143 on aggregate Dice with no compensating connectivity, precision, recall, or source-balance improvement is enough to stop this exact frequency-support continuation, but it would not eliminate SZA-aware ASPP/detail or line-context modeling broadly.

## Fallback/Next Decision

If this candidate fails because of a narrow implementation defect while the bounded frequency-support hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but behaves like prior local head/gate variants, document the negative result and broaden away from SZA-aware ASPP/detail micro-architecture changes toward a different architecture, training-policy, loss, data-policy, preprocessing, calibration, or diagnostic frontier. If it unexpectedly challenges ABI-068/ABI-130 or the MCAST context, request separately authorized whole-validation diagnostics rather than claiming promotion from capped evidence.
