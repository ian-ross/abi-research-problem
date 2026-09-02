# ABI-138 Full-Spectral BTD+SZA Spectral-Attention ASPP/Detail Decoder BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-130 remains the best SZA-aware ASPP/detail capped reference, while ABI-131 through ABI-137 show that local continuity bridges, agreement heads, auxiliary additions, deterministic-shuffle traversal, coarse objectness gates, and additive logit heads do not improve ABI-130's fixed-threshold trade-off. ABI-138 keeps ABI-130's trusted input, loss, auxiliary target, sampling traversal, augmentation, optimizer, and budget fixed, but moves the calibration intervention upstream into a neutral solar-conditioned spectral-attention front end rather than adding another output-side head.

## Hypothesis

ABI-130's strength appears to come from combining full ABI spectral evidence, thermal brightness-temperature differences, and Solar Geometry Input before an ASPP/detail decoder. The recent negative ABI-131--ABI-137 results suggest that the remaining limitation is not a simple final-head geometry or output-logit adjustment. A neutral, trainable front-end gate conditioned on approved ABI+BTD+SZA features may learn when to emphasize cirrus/window/water-vapor contrasts and learned spectral mixtures for daylight/illumination regimes, improving precision/connectivity or retaining ABI-130-level Google performance without candidate-owned thresholding, postprocessing, Artifact Filters, losses, metrics, data loading, sampling, or target derivation.

## Comparison Target

The primary comparison target is ABI-130 `abi130_fullspectral_btd_aspp_detail_decoder_sza_bce_dice_centerline_aux_v1`, Run `run_20260831_121006_7d24be`: capped filtered Dice 0.3953, MIT/Google filtered Dice 0.3779/0.4404, filtered precision 0.4415, filtered recall 0.3578, filtered connectivity 0.3851, and filtered predicted-positive fraction 0.00294. Its whole-validation diagnostic found filtered Dice 0.3954, precision 0.4436, recall 0.3566, and connectivity 0.3935, with higher threshold-sweep Dice at a lower external threshold.

Secondary references are ABI-068 `run_20260828_010836_4ccc77` as the local capped aggregate-Dice/source-balance reference, ABI-066 `run_20260827_230540_bf4ce3` as the high-connectivity reference, ABI-126 `run_20260831_085615_d05ab3` as the non-SZA ASPP/detail high-precision/connectivity comparator, and ABI-137 `run_20260831_180256_71be83` as the negative output-side adaptive-logit comparator. Canonical MCAST 2.1 remains the full Working Validation Split promotion context.

## Expected Effect

A useful result would keep ABI-130's non-degenerate SZA-aware calibration while improving at least one of filtered Dice, precision/connectivity, source balance, or positive-area discipline. Because the attention is neutral-initialized and front-end-local, the expected effect is modest: retain ABI-130 within about 0.01 aggregate filtered Dice while either raising connectivity/precision, improving MIT Dice, or reducing predicted-positive fraction without collapsing recall. A negative result would show that front-end spectral gating behaves like recent local head changes by damaging Google Dice, connectivity, or calibration.

## Implementation Sketch

- Reuse ABI-130's compact torch-only ASPP/detail encoder-decoder: normalized full ABI channels, deterministic thermal BTD planes from approved ABI channels, normalized SZA and `cos(SZA)`, learned 1x1 spectral/SZA projection, detail/context stem, residual encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail path, line-aware refinement, and simple primary/auxiliary heads.
- Replace only the front-end feature assembly with `NormalizedBTDSZASpectralAttentionFrontEnd`, which concatenates normalized ABI channels, BTD planes, SZA features, and the learned 1x1 mixture, then applies a global pooled channel-attention gate.
- Initialize the final attention projection to zero so the gate starts at exactly `0.75 + 0.5 * sigmoid(0) = 1.0`; the initial network is therefore close to ABI-130, and any spectral reweighting is learned during training.
- Preserve trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision with trusted `weighted_bce` weight 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.
- Request one sequential Run only; no Experiment Batch, custom scheduler, candidate-owned resource placement, threshold selection, external calibration, or Post-Run Evaluation is requested in this handoff.

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
6. As family-development evidence, the result is useful if it retains ABI-130 within about 0.01 aggregate filtered Dice while improving a meaningful diagnostic such as filtered precision, connectivity, MIT filtered Dice, predicted-positive fraction, or source balance; alternatively, a late-improving finite trajectory with clear source-informative behavior may justify one later bounded continuation.

## Continuation and hard stop

Continue this front-end attention branch only if ABI-138 is finite, non-degenerate, source-informative, and improves or preserves a meaningful ABI-130-relative diagnostic: aggregate filtered Dice retention, precision/connectivity recovery, MIT/Google balance, positive-area stability, or a late improving trajectory. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. A finite result materially below ABI-130 while also losing precision/connectivity or inflating positive area would stop this exact spectral-attention front end, but would not eliminate SZA, ASPP/detail decoders, or other front-end calibration mechanisms broadly.

## Fallback/Next Decision

If this experiment fails because of a narrow implementation defect while the spectral-attention hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but behaves like recent negative SZA-aware ASPP/detail variants, document the result and broaden to a distinct architecture, preprocessing, loss, calibration, or data-policy frontier that remains inside provider/Harness-owned boundaries. If it unexpectedly challenges ABI-068/ABI-130 or the MCAST context, request separately authorized whole-validation diagnostics rather than claiming promotion from capped data.
