# ABI-137 Full-Spectral BTD+SZA ASPP/Detail Decoder Adaptive-Logit BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-130 established a finite SZA-aware ASPP/detail BCE-Dice branch whose capped and whole-validation filtered Dice nearly tied ABI-068 while improving ABI-126's default-threshold recall. ABI-131, ABI-132, ABI-133, ABI-135, and ABI-136 show that simple continuity bridges, agreement heads, auxiliary additions, traversal changes, and coarse multiplicative objectness gates do not recover a better trade-off. ABI-137 keeps ABI-130's trusted input/loss/data policy fixed and tests a narrower architecture-level calibration mechanism motivated by ABI-130's whole-validation threshold sweep.

## Hypothesis

ABI-130's full-validation diagnostic improved filtered Dice from 0.3954 at the fixed 0.5 threshold to 0.4041 at threshold 0.15, indicating that useful contrail evidence is present but not ideally calibrated for the Harness default threshold. A bounded additive logit-calibration head may move some of that latent recall into the trained logits while avoiding the recall damage of ABI-136's multiplicative coarse gate. By learning a local foreground-minus-background margin plus a small patch-context bias from approved ABI+SZA features, ABI-137 should improve fixed-threshold recall or aggregate Dice relative to ABI-130 without candidate-owned threshold selection or postprocessing.

## Comparison Target

The primary comparison target is ABI-130 `abi130_fullspectral_btd_aspp_detail_decoder_sza_bce_dice_centerline_aux_v1`, Run `run_20260831_121006_7d24be`: capped filtered Dice 0.3953, MIT/Google filtered Dice 0.3779/0.4404, filtered precision 0.4415, filtered recall 0.3578, filtered connectivity 0.3851, and filtered predicted-positive fraction 0.00294. Its whole-validation review reported filtered Dice 0.3954, precision 0.4436, recall 0.3566, connectivity 0.3935, and threshold-sweep filtered Dice 0.4041 at threshold 0.15.

Secondary references are ABI-068 `run_20260828_010836_4ccc77` as the local aggregate-Dice/source-balance reference, ABI-066 `run_20260827_230540_bf4ce3` as the high-connectivity reference, ABI-126 `run_20260831_085615_d05ab3` as the ASPP/detail precision/connectivity comparator, and ABI-136 `run_20260831_171408_56b121` as the negative multiplicative-gate comparator. Canonical MCAST 2.1 remains the full Working Validation Split promotion context.

## Expected Effect

A useful result would recover part of ABI-130's threshold-sweep recall upside at the fixed Harness threshold while keeping positive area and precision controlled. The intended trade-off is a small increase in filtered predicted-positive fraction and recall with aggregate filtered Dice at least close to ABI-130; it is not intended to become a broad recall-heavy branch like ABI-135. A negative result would show that additive logit calibration either behaves like another simple head tweak, increasing clutter or damaging connectivity, or fails to improve over ABI-130 despite the threshold-sweep signal.

## Implementation Sketch

- Reuse ABI-130's compact torch-only ASPP/detail encoder-decoder: normalized ABI spectral features, deterministic thermal BTD planes from approved ABI channels, normalized SZA and `cos(SZA)` features, learned 1x1 spectral/SZA projection, detail/context stem, residual encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail path, and line-aware refinement.
- Replace the final single-convolution mask head with an `AdaptiveLogitCalibrationHead` that predicts a local foreground-minus-background margin, a small local residual, and a bounded patch-context additive bias.
- Initialize the context-bias path to a mild positive offset, then let training update it. This changes the trainable architecture producing `mask_logits`; it does not set a validation threshold, inspect validation labels, postprocess predictions, or implement calibration outside the model.
- Preserve the trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision with trusted `weighted_bce` weight 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.
- Request one sequential Run only; no Experiment Batch, custom scheduler, or candidate-owned resource placement is requested.

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
6. As family-development evidence, the result is useful if it improves fixed-threshold recall or aggregate filtered Dice relative to ABI-130 while keeping filtered precision/connectivity and predicted-positive fraction close enough to show that the threshold-sweep signal can be shifted into the model rather than only into external threshold diagnostics.

## Continuation and hard stop

Continue only if ABI-137 is finite, non-degenerate, source-informative, and improves a meaningful ABI-130-relative diagnostic: aggregate filtered Dice, MIT recall/Dice, fixed-threshold recall with acceptable precision loss, connectivity retention, positive-area stability, or a late improving trajectory. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. A finite result below ABI-130 on aggregate Dice while also losing precision/connectivity or inflating positive area would be enough to stop this exact adaptive-logit head, but would not eliminate ASPP/detail, Solar Geometry Input, or other calibration architectures broadly.

## Fallback/Next Decision

If this experiment fails because of a narrow implementation defect while the adaptive-logit calibration hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but behaves like the recent negative SZA-aware ASPP/detail head/gate variants, document the result and broaden away from ASPP/detail local head changes toward a distinct architecture, preprocessing, loss, calibration, or data-policy frontier that remains inside provider/Harness-owned boundaries. If it unexpectedly challenges ABI-068/ABI-130 or the MCAST context, request separately authorized whole-validation diagnostics rather than claiming promotion from capped data.
