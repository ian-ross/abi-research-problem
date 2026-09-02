# ABI-126 Full-Spectral BTD ASPP/Detail Decoder BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-120 and ABI-121 established that the compact ASPP/detail decoder family is finite and source-informative under trusted capped evidence. ABI-121's focal-Tversky follow-up produced near-top capped filtered Dice and its whole-validation diagnostic survived in aggregate, but the failure buckets showed widespread negative-patch clutter and weak line connectivity. ABI-126 keeps the ABI-121 architecture fixed and changes only the trusted primary loss to `bce_dice` to test a middle calibration point between the recall-heavy focal-Tversky branch and the conservative `bce_dice_cldice` branch.

## Hypothesis

Replacing ABI-121's trusted `focal_tversky` loss with trusted `bce_dice` will reduce low-confidence false positives and filtered predicted-positive fraction while preserving more recall than ABI-120's `bce_dice_cldice` branch. The ASPP/detail architecture already provides broad cloud context and high-resolution detail fusion, so BCE-Dice may supply a less recall-biased objective that improves precision/connectivity enough to make the ASPP/detail family more useful as a balanced non-frequency-gated comparator.

## Comparison Target

The primary comparison target is ABI-121 `abi121_fullspectral_btd_aspp_detail_decoder_focal_tversky_centerline_aux_v1`, Run `run_20260831_041559_43da35`: capped best filtered Dice 0.3884, MIT/Google filtered Dice 0.3835/0.4005, filtered precision 0.3526, filtered recall 0.4323, filtered connectivity 0.2315, and filtered predicted-positive fraction 0.00444. Its whole-validation failure-bucket review found similar aggregate Dice but substantial negative-patch clutter and low connectivity.

The secondary family comparison target is ABI-120 `run_20260831_033037_bad0bb`: the same ASPP/detail architecture with trusted `bce_dice_cldice`, capped filtered Dice 0.3667, precision 0.4366, recall 0.3161, connectivity 0.3681, and filtered predicted-positive fraction 0.00262. Broader references are ABI-068 `run_20260828_010836_4ccc77` as the local aggregate-Dice frequency-gated reference and ABI-066 `run_20260827_230540_bf4ce3` as the precision/connectivity reference. Canonical MCAST 2.1 remains full Working Validation Split promotion context, not a promotion gate for this capped continuation.

## Expected Effect

A useful ABI-126 result should sit between ABI-120 and ABI-121: higher precision and connectivity than ABI-121, lower filtered predicted-positive fraction and negative-patch clutter risk than ABI-121, and higher recall and aggregate/source Dice than ABI-120. It need not immediately beat ABI-068 to be informative; the purpose is to determine whether ASPP/detail's recall-versus-clutter trade-off is loss-calibratable using the existing trusted loss allowlist. A negative result would show that BCE-Dice neither preserves ABI-121's recall nor recovers ABI-120's precision/connectivity, pushing the campaign away from ASPP/detail loss tuning.

## Implementation Sketch

- Reuse ABI-121 architecture unchanged: normalized provider-approved GOES ABI channels 1-16, eight deterministic thermal BTD planes derived only from those channels, learned 16-channel 1x1 projection, full-resolution detail/context stem, residual encoder, ASPP bottleneck with dilation rates 2/4/8 plus image-level context, bilinear decoder fusions, second high-resolution detail path, and line-aware refinement.
- Emit primary `mask_logits` and trusted auxiliary `centerline_logits` from the same refined feature map.
- Change only the manifest-selected trusted primary loss from `focal_tversky` to `bce_dice`.
- Preserve provider-owned `combined_source_balanced` traversal, trusted `random_mirroring`, provider-derived Centerline Target auxiliary supervision with trusted `weighted_bce` weight 0.02, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.
- Request one sequential Run only; no Experiment Batch or candidate-owned scheduling/resource placement is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are excluded.
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
6. As family-development evidence, the result is useful if it improves ABI-121 precision/connectivity or positive-area discipline without losing most of ABI-121's recall, improves ABI-120 recall or aggregate/source Dice without collapsing precision, shows a finite improving trajectory, or exposes a clear loss-specific limit for the ASPP/detail family.

## Continuation and hard stop

Continue the ASPP/detail family only if ABI-126 is finite, non-degenerate, source-informative, and improves a meaningful family diagnostic relative to ABI-120 or ABI-121, such as precision/recall balance, source balance, connectivity, predicted-positive stability, or late-epoch trajectory. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. Low capped Dice alone is not promotion evidence and not family-wide elimination proof, but a clear miss on both ABI-120 and ABI-121-relative diagnostics would be enough to stop this exact BCE-Dice ASPP/detail continuation.

## Fallback/Next Decision

If this candidate fails due to a narrow implementation defect while the ABI-121-preserving architecture hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but neither improves ABI-121's clutter/connectivity trade-off nor preserves ABI-120-level recall/Dice, document the loss-policy result and broaden to a different contract-compliant frontier rather than repeating ASPP/detail loss swaps. If it unexpectedly challenges ABI-068, request separately authorized focused full-data evidence rather than claiming promotion from capped data.
