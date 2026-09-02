# ABI-155 Full-Spectral BTD+SZA Full-Scale Skip ASPP/Detail Decoder Recall-Calibrated BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-154 established a whole-validation-tested SZA-aware ASPP/detail precision/connectivity branch: filtered Dice 0.3941 on the 3,088-sample Working Validation Split, filtered precision 0.4812, filtered recall 0.3338, filtered connectivity 0.4438, and stable capped-to-whole behavior. It nearly tied ABI-130 aggregate Dice while improving precision, connectivity, MIT Dice, and negative-patch false-positive burden, but its main cost was default-threshold under-recall. ABI-155 keeps ABI-154's architecture, input, loss, auxiliary target, sampling, augmentation, optimizer, learning-rate, and budget, changing only the final mask-logit head to test conservative trainable recall calibration.

## Hypothesis

ABI-154's threshold sweep showed latent filtered Dice at lower thresholds, with whole-validation filtered Dice rising from 0.3941 at threshold 0.5 to 0.4107 at threshold 0.05 and a precision/recall balance near threshold 0.10. A low-capacity trainable mask-logit head can move part of that recall into the Harness fixed threshold without candidate-owned thresholding or postprocessing. The head should preserve ABI-154's full-scale skip, detail, SZA, and line-aware features while adding a bounded local residual and gentle learnable bias that can recover positive-patch recall where the existing representation already has local detail, context, and line support.

## Comparison Target

The primary comparison target is ABI-154 `abi154_fullspectral_btd_sza_fullscale_skip_aspp_detail_decoder_bce_dice_centerline_aux_v1`, Run `run_20260901_071026_32d3ec`, with capped filtered Dice 0.3944, MIT/Google filtered Dice 0.3824/0.4260, filtered precision 0.4777, recall 0.3359, connectivity 0.4374, and filtered predicted-positive fraction 0.00255. Its whole-validation evaluation `eval_evalreq_abi154_wholeval_failure_buckets_v1` confirmed filtered Dice 0.3941, precision 0.4812, recall 0.3338, connectivity 0.4438, and improved negative-patch clutter relative to ABI-130 and ABI-068.

Secondary references are ABI-130 `run_20260831_121006_7d24be` as the SZA-aware ASPP/detail aggregate/reference branch, ABI-068 `run_20260828_010836_4ccc77` as the current capped aggregate/source-balance reference, ABI-126 `run_20260831_085615_d05ab3` as the non-SZA ASPP/detail precision/connectivity comparator, and canonical MCAST 2.1 as promotion context only.

## Expected Effect

A useful outcome would raise ABI-154's filtered recall and aggregate/MIT filtered Dice while keeping most of its precision, connectivity, and filtered predicted-positive discipline. The desired profile is not an indiscriminate positive-area expansion: negative-patch clutter and filtered precision should remain closer to ABI-154 than to more permissive failed calibration branches. A negative outcome would reproduce prior additive-head failures, increasing false positives or lowering connectivity without a compensating recall/Dice gain.

## Implementation Sketch

- Start from ABI-154's normalized full-spectral raw features, deterministic thermal BTD planes from approved ABI channels, normalized Solar Geometry Input, `cos(SZA)`, learned 1x1 spectral projection, residual encoder, ASPP context, high-resolution detail stem, full-scale skip fusion, and line-aware final refinement.
- Replace the final single 1x1 mask projection with `RecallCalibratedMaskHead`.
- The new head keeps a direct base mask-logit projection, computes local detail support, smoothed context support, and line support from refined features, then adds only a bounded `0.20 * sigmoid(gate) * tanh(residual)` correction plus a small trainable logit bias initialized to `0.08`.
- The spatial residual projection is zero-initialized so the candidate starts from the ABI-154-style direct head plus a gentle learned calibration offset; training must earn any spatially varying correction.
- Emit primary `mask_logits` and provider-derived auxiliary `centerline_logits` only.
- Do not add thresholding, Artifact Filters, postprocessing, candidate-owned losses, data loading, sampling logic, augmentation transforms, target derivation, training loops, resource scheduling, external persistence, pretrained weights, network access, or runtime downloads.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data claim, Experiment Batch, Capability Request, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains below the 25,000,000 smoke ceiling and batch size 4 completes inside the trusted runtime envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it improves ABI-154 recall, aggregate filtered Dice, MIT filtered Dice, or ABI-130 aggregate/source balance while preserving most of ABI-154's precision/connectivity advantage and without a large filtered predicted-positive expansion.

## Continuation and hard stop

Continue this calibrated full-scale skip branch only if ABI-155 is finite, non-degenerate, source-informative, and improves at least one of recall, aggregate Dice, MIT Dice, or source balance without materially giving back ABI-154's precision/connectivity/negative-patch gains. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. If it completes finite but falls materially below ABI-154 and ABI-130 without a compensating recall or calibration gain, stop the exact recall-calibrated mask-head variant.

## Fallback/Next Decision

If this candidate fails from a narrow implementation defect while the recall-calibrated full-scale skip hypothesis remains intact, consider at most one explicit Repair Candidate in a later Autonomy Step. If it is scientifically negative, document the result and broaden away from local ASPP/detail head calibration toward another contract-compliant architecture, data-policy, loss/auxiliary, or preprocessing/front-end frontier. If it unexpectedly improves capped/source-stratified metrics while preserving ABI-154's precision/connectivity profile, request separate whole-validation diagnostics before making any full-data or promotion claim.
