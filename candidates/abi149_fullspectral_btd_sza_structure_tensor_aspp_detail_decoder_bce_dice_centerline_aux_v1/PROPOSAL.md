# ABI-149 Full-Spectral BTD+SZA Structure-Tensor ASPP/Detail Decoder BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-130 remains the strongest SZA-aware ASPP/detail BCE-Dice reference and whole-validation diagnostics confirmed that Solar Geometry Input improves fixed-threshold recall/calibration, but recent ABI-131 through ABI-148 local head, auxiliary, data-policy, ridge, and learning-rate continuations did not improve the precision/connectivity/source-balance tradeoff. ABI-149 keeps ABI-130's trusted input, loss, auxiliary target, and training/data policy fixed while changing the front-end evidence representation to include differentiable structure-tensor line features.

## Hypothesis

A front-end that exposes local line coherence and orientation balance can help the ASPP/detail decoder separate elongated contrail-like evidence from blob-like cloud clutter and negative-patch false positives. Unlike threshold tuning or Artifact Filtering, the structure-tensor planes are ordinary differentiable model features computed only from provider-approved ABI, BTD, and SZA inputs. A useful result would preserve ABI-130's SZA-driven recall/default-threshold calibration while recovering part of ABI-126/ABI-066 connectivity and positive-area discipline.

## Comparison Target

The primary comparison target is ABI-130 `abi130_fullspectral_btd_aspp_detail_decoder_sza_bce_dice_centerline_aux_v1`, Run `run_20260831_121006_7d24be`: capped filtered Dice 0.3953, MIT/Google filtered Dice 0.3779/0.4404, filtered precision 0.4415, filtered recall 0.3578, filtered connectivity 0.3851, and filtered predicted-positive fraction 0.00294. Whole-validation diagnostics reported filtered Dice 0.3954 and confirmed both the SZA recall gain and the remaining clutter/connectivity cost.

Secondary references are ABI-068 `run_20260828_010836_4ccc77` for local capped aggregate Dice and MIT recall/source balance, ABI-126 `run_20260831_085615_d05ab3` for ASPP/detail precision/connectivity, ABI-066 `run_20260827_230540_bf4ce3` for high-connectivity behavior, and ABI-143 `run_20260831_224534_27b73d` for the best recent SZA-aware ridge-family BCE-Dice point. Canonical MCAST 2.1 remains full Working Validation Split promotion context, not a promotion claim for this capped continuation.

## Expected Effect

The expected effect is a modest increase in structure-aware positive-area discipline: filtered precision or connectivity should improve relative to ABI-130 without reverting to ABI-126-style under-recall. It is acceptable if aggregate filtered Dice only near-ties ABI-130 within about 0.005 when it shows a distinctive secondary gain in connectivity, MIT recall/source balance, or lower predicted-positive fraction. A negative result would show that adding explicit structure-tensor evidence behaves like prior detail/ridge front ends and weakens source balance or recall.

## Implementation Sketch

- Reuse the compact torch-only ABI-130 ASPP/detail encoder-decoder: normalized ABI spectral features, deterministic thermal BTD planes from approved ABI channels, normalized SZA and `cos(SZA)` features, learned 1x1 spectral projection, full-resolution detail/context stem, residual encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail path, and line-aware refinement.
- Add a small learned 1x1 evidence projection over the ABI-130 front-end features, then compute fixed Sobel-gradient structure-tensor features with local averaging: line energy, coherence, orientation balance, diagonal correlation, and ridge residual magnitude.
- Concatenate those differentiable structure features with the ABI-130 front-end feature tensor before the existing encoder-decoder. These are internal model features, not postprocessing, thresholding, Artifact Filters, metrics, or target transforms.
- Emit primary `mask_logits` and trusted auxiliary `centerline_logits` from the same refined feature map.
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
6. As family-development evidence, the result is useful if it near-ties ABI-130 aggregate filtered Dice while improving connectivity, precision, predicted-positive discipline, or MIT source balance; improves aggregate filtered Dice over ABI-130; or supplies clear negative evidence about explicit structure-tensor features under SZA-aware BCE-Dice training.

## Continuation and hard stop

Continue only if ABI-149 is finite, non-degenerate, source-informative, and improves a meaningful ABI-130-relative diagnostic: aggregate Dice, connectivity, precision/recall balance, positive-area stability, MIT recall/source balance, or late-epoch trajectory. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. A finite result materially below ABI-130 on aggregate Dice without any compensating precision/connectivity/source-balance gain is enough to stop this exact structure-tensor ASPP/detail branch, but would not eliminate structure-aware preprocessing or SZA-aware modeling globally.

## Fallback/Next Decision

If this candidate fails because of a narrow implementation defect while the structure-tensor hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but structure features trade away ABI-130's Google/calibration advantage or worsen connectivity, document that result and broaden to a different contract-compliant architecture, input/front-end, data-policy, augmentation, or calibration frontier rather than repeating small ASPP/detail local tweaks. If it unexpectedly challenges ABI-068/ABI-130 or MCAST context, request separately authorized whole-validation diagnostics rather than claiming promotion from capped data.
