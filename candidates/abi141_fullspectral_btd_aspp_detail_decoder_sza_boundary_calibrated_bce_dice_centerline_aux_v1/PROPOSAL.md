# ABI-141 Full-Spectral BTD+SZA ASPP/Detail Decoder Boundary-Calibrated BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-130 established a finite SZA-aware ASPP/detail BCE-Dice branch that nearly tied ABI-068 on aggregate Dice and survived whole-validation diagnostics, but it traded away some ABI-126/ABI-066 connectivity and negative-patch discipline. ABI-141 keeps ABI-130's input, loss, data policy, training policy, and compact ASPP/detail backbone fixed while adding a provider-derived Boundary Target auxiliary output and a neutral-initialized boundary/detail residual mask-logit calibration branch.

## Hypothesis

A low-weight Boundary Target auxiliary head plus a bounded, initially neutral boundary/detail residual can recover part of ABI-126/ABI-066 edge/connectivity and negative-patch discipline without reverting to ABI-126-style MIT under-recall. The boundary branch is architectural supervision only: it emits trusted `boundary_logits` and learns an additive residual from refined feature maps. It does not implement thresholding, Artifact Filters, candidate-owned postprocessing, target derivation, or sampling changes.

## Comparison Target

Primary comparison target: ABI-130 `run_20260831_121006_7d24be`, which reached capped filtered Dice 0.3953 and whole-validation filtered Dice 0.3954 with MIT/Google whole-validation filtered Dice 0.3797/0.4256, precision 0.4436, recall 0.3566, and connectivity 0.3935.

Secondary references: ABI-126 `run_20260831_085615_d05ab3` for ASPP/detail precision/connectivity, ABI-068 `run_20260828_010836_4ccc77` for local aggregate/source-balance reference, ABI-066 `run_20260827_230540_bf4ce3` for connectivity, and ABI-133 `run_20260831_144720_475594` as evidence that a Line auxiliary alone did not improve the SZA ASPP/detail branch. Canonical MCAST 2.1 remains full Working Validation Split promotion context, not a promotion claim for this capped continuation.

## Expected Effect

A useful result would preserve ABI-130's controlled positive area and source-balanced aggregate Dice while increasing filtered connectivity, precision, or negative-patch discipline. The intended gain is modest: keep filtered Dice within about 0.01 of ABI-130 or ABI-068 while improving connectivity toward ABI-126/ABI-066, or clearly show that boundary supervision is another insufficient auxiliary-only lever for this family.

## Implementation Sketch

- Start from the ABI-130 torch-only compact ASPP/detail encoder-decoder over provider-approved `abi_16ch_plus_sza` input.
- Preserve normalized ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized SZA, `cos(SZA)`, full-resolution detail/context stem, residual encoder, ASPP bottleneck, decoder fusions, high-resolution detail path, and line-aware refinement.
- Add a `BoundaryDetailCalibration` module after the final refinement. It forms feature-space fine-detail and broad-context views, predicts trusted `boundary_logits`, and adds a bounded `0.15 * tanh(...)` residual to primary `mask_logits`.
- Initialize the mask residual convolution to zero so the model begins close to ABI-130 rather than imposing candidate-owned postprocessing or a handcrafted threshold shift.
- Emit primary `mask_logits`, provider-derived `centerline_logits`, and provider-derived `boundary_logits`.
- Preserve trusted `bce_dice` primary loss, Centerline Target weighted-BCE auxiliary weight 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.
- Request one sequential Run only; no Experiment Batch or candidate-owned resource scheduling is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits` and `boundary_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `centerline` and `boundary`, auxiliary loss `weighted_bce`, auxiliary weights 0.02 and 0.01, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, primary and auxiliary losses, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data evidence, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains below the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it keeps aggregate filtered Dice close to ABI-130 while improving filtered connectivity/precision, reduces negative-patch clutter, improves MIT filtered Dice or recall without losing Google transfer, or supplies clear evidence that boundary-calibrated detail supervision is not the right continuation for the SZA ASPP/detail branch.

## Continuation and hard stop

Continue this branch only if ABI-141 is finite, non-degenerate, source-informative, and improves a meaningful ABI-130-relative diagnostic such as connectivity, precision, negative-patch discipline, MIT recall/Dice, aggregate Dice, or late-epoch trajectory. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. A finite result materially below ABI-130 on aggregate Dice without a connectivity or failure-bucket gain would be enough to stop this exact boundary-calibrated continuation, but would not eliminate ASPP/detail or SZA-aware architectures broadly.

## Fallback/Next Decision

If this candidate fails because of a narrow implementation defect while the boundary-calibration hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but simply repeats ABI-133-style auxiliary degradation or ABI-136-style calibration loss, document that result and broaden away from ASPP/detail head tweaks toward a different architecture, preprocessing, calibration, or training-policy frontier. If it unexpectedly improves both ABI-130 aggregate Dice and ABI-126/ABI-066 connectivity/precision, request separately authorized whole-validation diagnostics rather than claiming promotion from capped data.
