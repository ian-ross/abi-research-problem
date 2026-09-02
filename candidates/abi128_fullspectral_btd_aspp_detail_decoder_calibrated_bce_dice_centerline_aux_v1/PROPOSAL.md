# ABI-128 Full-Spectral BTD ASPP/Detail Decoder Calibrated BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-120 through ABI-127 mapped the compact ASPP/detail decoder family's trusted loss and simple auxiliary-head trade-offs. ABI-121 established the focal-Tversky recall/source-balance operating point, ABI-126 established the BCE-Dice precision/connectivity and Google-Dice operating point, and the ABI-126 whole-validation diagnostic showed that much of ABI-126's missed recall is conservative fixed-threshold calibration rather than a total architectural failure. ABI-127 showed that adding a Line Target auxiliary head to ABI-126 is an unfavorable trade-off. ABI-128 therefore keeps the ABI-126 loss/data policy fixed and changes only the mask-logit head to test in-architecture calibration.

## Hypothesis

Replacing ABI-126's single 1x1 mask head with a calibration-aware foreground-minus-background margin head will recover recall, especially MIT recall, while preserving most of ABI-126's positive-area discipline, precision, and connectivity. A dual-logit margin, broad-context/detail gate, small residual logit, and trainable global logit scale/bias initialized mildly recall-friendly may move the fixed Harness threshold toward the balanced part of ABI-126's diagnostic threshold curve without candidate-owned thresholding or postprocessing.

## Comparison Target

The primary comparison target is ABI-126 `abi126_fullspectral_btd_aspp_detail_decoder_bce_dice_centerline_aux_v1`, Run `run_20260831_085615_d05ab3`: capped best filtered Dice 0.3859, MIT/Google filtered Dice 0.3635/0.4415, filtered precision 0.4746, filtered recall 0.3251, filtered connectivity 0.4517, and filtered predicted-positive fraction 0.00248. Its whole-validation evaluation reached filtered Dice 0.3892, precision 0.4770, recall 0.3288, connectivity 0.4563, Google filtered Dice 0.4319, and MIT filtered Dice 0.3662; the threshold sweep improved filtered Dice to 0.4079 at a lower diagnostic threshold.

Secondary ASPP/detail references are ABI-121 `run_20260831_041559_43da35` for recall/source-balance and ABI-127 `run_20260831_094013_5ba974` for the failed simple Line+Centerline auxiliary recovery attempt. Broader local references are ABI-068 `run_20260828_010836_4ccc77` as the capped aggregate-Dice reference and ABI-066 `run_20260827_230540_bf4ce3` as the precision/connectivity reference. Canonical MCAST 2.1 remains full Working Validation Split promotion context, not a promotion claim for this capped continuation.

## Expected Effect

A useful ABI-128 result should raise ABI-126's filtered recall and MIT filtered Dice while keeping aggregate filtered Dice close to or above ABI-126 and avoiding ABI-121-like positive-area clutter. The intended trade-off is acceptable if precision/connectivity fall modestly but remain materially stronger than ABI-121 and the filtered predicted-positive fraction stays closer to ABI-126 than to ABI-121. It need not beat ABI-068 immediately to be scientifically useful; it tests whether the ASPP/detail BCE-Dice branch can be calibrated inside the model architecture after the diagnostic threshold sweep identified recoverable recall.

## Implementation Sketch

- Reuse ABI-126's compact torch-only full-spectral BTD ASPP/detail encoder-decoder: normalized provider-approved GOES ABI channels 1-16, eight deterministic thermal BTD planes derived only from those channels, a learned 16-channel 1x1 projection, full-resolution detail/context stem, residual encoder, ASPP bottleneck with dilation rates 2/4/8 plus image-level context, bilinear decoder fusions, second high-resolution detail path, and line-aware refinement.
- Replace only the primary `mask_logits` projection with a `CalibrationAwareMaskHead` that learns local refined features, broad smoothed context, a foreground-minus-background dual-logit margin, a context/detail gate, a small residual logit, and trainable scalar logit scale/bias initialized to `1.0` and `0.15` respectively.
- Preserve primary output shape `[1, 256, 256]` and the trusted auxiliary `centerline_logits` output shape `[1, 256, 256]`.
- Preserve trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision with trusted `weighted_bce` weight 0.02, provider-owned `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.
- Request one sequential Run only; no Experiment Batch, candidate-owned thresholding, candidate-owned calibration procedure, or resource scheduling is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, thresholding, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, threshold selection, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data evidence, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it improves ABI-126 filtered recall or MIT filtered Dice while preserving most of ABI-126's precision/connectivity, improves aggregate filtered Dice relative to ABI-126, shows a finite improving trajectory, or clarifies that fixed-threshold calibration cannot be recovered by a mask-head architecture change alone.

## Continuation and hard stop

Continue this ASPP/detail calibration branch only if ABI-128 is finite, non-degenerate, source-informative, and improves at least one ABI-126-relative calibration diagnostic without severe precision/connectivity collapse. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. Low capped Dice alone is not a family-wide elimination proof, but a clear loss of ABI-126's precision/connectivity without meaningful recall recovery would stop this exact calibrated-head branch.

## Fallback/Next Decision

If this candidate fails due to a narrow implementation defect while the ABI-126 calibration hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but does not improve fixed-threshold recall or source balance relative to ABI-126, document the calibration-head result and broaden away from ASPP/detail auxiliary/head tuning toward a different architecture family, data policy, loss policy, augmentation policy, or a bounded diagnostic request. If it unexpectedly challenges ABI-068, request separately authorized focused full-data evidence rather than claiming promotion from capped data.
