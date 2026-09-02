# ABI-133 Full-Spectral BTD+SZA ASPP/Detail Decoder BCE-Dice Line+Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-130 established that provider-approved Solar Geometry Input can move the ASPP/detail BCE-Dice branch toward better default-threshold recall and near-best whole-validation filtered Dice. ABI-131 and ABI-132 showed that simple extra continuity/agreement mask-head geometry did not recover connectivity. ABI-133 keeps ABI-130's architecture, input mode, loss, and data/training policy fixed while changing only the trusted auxiliary-target set: it adds Line Target supervision beside the existing Centerline Target.

## Hypothesis

Low-weight provider-derived Line Target auxiliary supervision will make the SZA-aware ASPP/detail BCE-Dice branch preserve more continuous thin-line evidence while retaining ABI-130's useful recall calibration. Because ABI-130's whole-validation review confirmed improved recall but lower precision/connectivity than ABI-126, and ABI-127 showed the same Line+Centerline auxiliary idea is feasible in the non-SZA ASPP/detail branch, this controlled auxiliary-target continuation tests whether SZA plus line supervision can recover connectivity without candidate-owned thresholding, postprocessing, or Artifact Filters.

## Comparison Target

The primary comparison target is ABI-130 `abi130_fullspectral_btd_aspp_detail_decoder_sza_bce_dice_centerline_aux_v1`, Run `run_20260831_121006_7d24be`, with capped filtered Dice 0.3953, MIT/Google filtered Dice 0.3779/0.4404, filtered precision 0.4415, filtered recall 0.3578, filtered connectivity 0.3851, and filtered predicted-positive fraction 0.00294. Its whole-validation diagnostic reached filtered Dice 0.3954, precision 0.4436, recall 0.3566, and connectivity 0.3935.

Secondary references are ABI-126 `run_20260831_085615_d05ab3` as the ASPP/detail high-precision/connectivity comparator, ABI-127 `run_20260831_094013_5ba974` as the non-SZA Line+Centerline auxiliary comparator, ABI-068 `run_20260828_010836_4ccc77` as the local capped aggregate-Dice reference, and ABI-066 `run_20260827_230540_bf4ce3` as the high-connectivity line-family reference. Canonical MCAST 2.1 remains full Working Validation Split promotion context, not a promotion claim for this capped continuation.

## Expected Effect

A useful result would preserve ABI-130-level aggregate filtered Dice and source balance while improving filtered connectivity or reducing false-positive clutter/positive-area over-expansion. The expected trade-off is a small auxiliary-loss regularization effect: line supervision may slightly constrain recall, but it should not return to ABI-126-style MIT under-recall or repeat ABI-131/ABI-132 connectivity degradation. A negative result would show that adding Line Target supervision to the SZA-aware ASPP/detail branch damages ABI-130's recall calibration or fails to improve connectivity.

## Implementation Sketch

- Reuse ABI-130's compact torch-only ASPP/detail encoder-decoder: normalized raw ABI channels, deterministic thermal BTD planes from approved ABI channels, normalized SZA and `cos(SZA)` illumination features, learned 1x1 spectral/SZA projection, full-resolution detail/context stem, residual encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail path, and line-aware refinement.
- Keep provider-approved `input_mode: abi_16ch_plus_sza`; the first 16 channels are GOES ABI channels 1-16 and the seventeenth channel is Solar Geometry Input.
- Add a `line_logits` 1x1 auxiliary head from the same refined feature map used by `mask_logits` and `centerline_logits`.
- Preserve trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision with trusted `weighted_bce` weight 0.02, and add provider-derived Line Target auxiliary supervision with trusted `weighted_bce` weight 0.02.
- Preserve `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.
- Request one sequential Run only; no Experiment Batch or candidate-owned scheduling/resource placement is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits` and `line_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `centerline` and `line`, auxiliary loss `weighted_bce`, auxiliary weights 0.02 and 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
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
6. As family-development evidence, the result is useful if it improves ABI-130 filtered connectivity or negative-patch/positive-area discipline while keeping aggregate filtered Dice within about 0.01 of ABI-130, or if it reveals that Line Target supervision conflicts with SZA-enabled recall calibration.

## Continuation and hard stop

Continue this branch only if ABI-133 is finite, non-degenerate, source-informative, and improves a meaningful ABI-130-relative diagnostic: connectivity, precision, predicted-positive discipline, MIT/Google balance, or aggregate Dice with comparable recall. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. A finite result that trails ABI-130 on aggregate Dice, recall, and connectivity would stop the exact Line+Centerline SZA auxiliary variant, but would not eliminate Solar Geometry Input, ASPP/detail architectures, or trusted auxiliary targets broadly.

## Fallback/Next Decision

If this candidate fails because of a narrow implementation defect while the auxiliary-target hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but fails to improve connectivity or positive-area discipline over ABI-130, document that result and broaden toward a different in-contract calibration, preprocessing, loss, augmentation, or architecture frontier rather than repeating simple SZA-aware ASPP/detail head tweaks. If it unexpectedly challenges ABI-068, ABI-130, or MCAST context, request separately authorized whole-validation diagnostics rather than claiming promotion from capped data.
