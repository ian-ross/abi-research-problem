# ABI-136 Full-Spectral BTD+SZA ASPP/Detail Decoder Coarse Objectness Gate BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-130 established the best SZA-aware ASPP/detail reference and whole-validation diagnostics confirmed that Solar Geometry Input improved default-threshold recall and aggregate Dice relative to ABI-126. ABI-131, ABI-132, ABI-133, and ABI-135 showed that simple continuity, region/line, auxiliary, or traversal tweaks did not recover the desired precision/connectivity balance. ABI-136 keeps ABI-130's input, trusted loss, auxiliary target, and training/data policy fixed while adding a neutral coarse-context objectness gate inside the model architecture.

## Hypothesis

ABI-130's useful signal is a real SZA-driven recall/calibration improvement, but its whole-validation review also found more negative-patch clutter and weaker connectivity than ABI-126/ABI-066. A bounded, neutral-initialized gate that uses low-resolution ASPP context to calibrate high-resolution detail features may suppress cloud-edge or negative-patch clutter before the line-aware refinement while preserving ABI-130's default-threshold recall. Because the gate operates on learned features before the mask head, it is an in-contract calibration mechanism rather than candidate-owned thresholding, postprocessing, Artifact Filtering, or data handling.

## Comparison Target

The primary comparison target is ABI-130 `abi130_fullspectral_btd_aspp_detail_decoder_sza_bce_dice_centerline_aux_v1`, Run `run_20260831_121006_7d24be`: capped filtered Dice 0.3953, MIT/Google filtered Dice 0.3779/0.4404, filtered precision 0.4415, filtered recall 0.3578, filtered connectivity 0.3851, and filtered predicted-positive fraction 0.00294. Its whole-validation diagnostic reached filtered Dice 0.3954, precision 0.4436, recall 0.3566, connectivity 0.3935, and identified negative-patch clutter/connectivity as the main costs of SZA recall recovery.

Secondary references are ABI-068 `run_20260828_010836_4ccc77` as the local capped aggregate-Dice and MIT-recall/source-balance reference, ABI-126 `run_20260831_085615_d05ab3` as the ASPP/detail BCE-Dice precision/connectivity reference, ABI-066 `run_20260827_230540_bf4ce3` as the high-connectivity reference, and ABI-135 `run_20260831_162753_adfc95` as the negative deterministic-shuffle data-policy comparison. Canonical MCAST 2.1 remains full Working Validation Split promotion context, not a promotion claim for this capped continuation.

## Expected Effect

A useful result would retain ABI-130-like aggregate filtered Dice and Google strength while improving one or more of filtered precision, filtered connectivity, negative-patch positive-area discipline, or MIT filtered Dice. The expected effect is not a large recall expansion; success requires a cleaner precision/connectivity trade-off at the fixed Harness threshold. A negative result would show that adding coarse objectness context either behaves like another ineffective ASPP/detail head/refiner tweak or destabilizes ABI-130's useful SZA calibration.

## Implementation Sketch

- Reuse ABI-130's torch-only SZA-aware ASPP/detail encoder-decoder: normalized ABI channels, deterministic thermal BTD planes from approved ABI channels, normalized SZA and cosine-SZA planes, learned 1x1 spectral/SZA projection, detail/context stem, residual encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail path, and final line-aware refinement.
- Add `CoarseObjectnessGate` after the high-resolution decoder/detail fusion and before final line-aware refinement. It upsamples the low-resolution ASPP context, projects it and the fused high-resolution feature map to the same width, predicts a per-feature spatial gate, and applies a bounded multiplier `0.8 + 0.4 * sigmoid(gate_logits)`.
- Initialize the final gate logits weights and bias to zero, so the multiplier starts at 1.0 and the new branch begins as a conservative calibration path rather than a hand-coded suppressor.
- Emit only primary `mask_logits` and trusted auxiliary `centerline_logits` from the refined feature map.
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
6. As family-development evidence, the result is useful if it improves ABI-130 filtered precision, connectivity, predicted-positive discipline, MIT filtered Dice, or aggregate filtered Dice while keeping ABI-130's recall benefit from reverting to ABI-126-like under-segmentation.

## Continuation and hard stop

Continue only if ABI-136 is finite, non-degenerate, source-informative, and improves a meaningful ABI-130-relative diagnostic: precision/connectivity retention, negative-patch or predicted-positive discipline, MIT filtered Dice, aggregate Dice, or a cleaner late-epoch trajectory. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. A finite result that is below ABI-130 on aggregate Dice and below ABI-126/ABI-066 on precision/connectivity, without a compensating recall/source-balance gain, is enough to stop this exact coarse-objectness gate branch.

## Fallback/Next Decision

If this candidate fails because of a narrow implementation defect while the coarse-context calibration hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but behaves like another ineffective ASPP/detail refiner tweak, document that result and broaden away from ASPP/detail local calibration toward a different architecture, loss/data-policy diagnostic, or preprocessing frontier. If it unexpectedly challenges ABI-068 or improves ABI-130's whole-validation-relevant trade-off, request separately authorized whole-validation diagnostics rather than claiming promotion from capped data.
