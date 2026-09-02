# ABI-152 Proposal: no-augmentation SZA ASPP/detail decoder

## Proposal classification

**Family-development continuation.** ABI-152 is a controlled augmentation-policy continuation of the ABI-130 SZA-aware full-spectral BTD ASPP/detail BCE-Dice branch. It broadens away from additional ad-hoc SZA-aware ASPP/detail front-end tweaks by testing whether the trusted random-mirroring augmentation itself is part of the repeated calibration/connectivity tradeoff observed in recent SZA ASPP/detail variants.

## Hypothesis

ABI-130 reached near-best capped aggregate filtered Dice and strong Google filtered Dice, but subsequent SZA-aware ASPP/detail micro-architecture, front-end, ridge, anomaly, frequency-support, loss, learning-rate, and source-policy continuations did not improve its precision/connectivity/negative-patch tradeoff. Because GOES ABI scan geometry, cloud streak orientation, Solar Geometry Input, and Artifact Filter failure modes are not necessarily mirror-invariant, disabling trusted random mirroring may preserve native-orientation correlations that help the SZA-aware BCE-Dice ASPP/detail branch calibrate positives without candidate-owned preprocessing, thresholding, postprocessing, or metric changes.

The expected effect is not guaranteed improvement. This Run is useful if it shows that random mirroring is harmless for ABI-130, or if native-orientation training recovers ABI-126-like precision/connectivity while retaining a meaningful fraction of ABI-130's SZA-enabled recall and Google Dice.

## Comparison Target

Primary comparison target: ABI-130 `abi130_fullspectral_btd_aspp_detail_decoder_sza_bce_dice_centerline_aux_v1`, Run `run_20260831_121006_7d24be`, capped filtered Dice 0.3953, MIT/Google filtered Dice 0.3779/0.4404, filtered precision 0.4415, recall 0.3578, connectivity 0.3851, and filtered predicted-positive fraction 0.00294.

Secondary references are ABI-126 `run_20260831_085615_d05ab3` for non-SZA ASPP/detail precision/connectivity under random mirroring, ABI-143 `run_20260831_224534_27b73d` for the near-best SZA-aware soft ridge-gate branch, ABI-068 `run_20260828_010836_4ccc77` for the best local capped aggregate filtered Dice, ABI-087 `run_20260829_193824_241e30` as prior no-augmentation evidence in the different frequency-gated focal-Tversky family, and ABI-151 `run_20260901_044007_880e7e` as recent negative evidence against another SZA ASPP/detail front-end tweak.

## Expected Effect

If mirroring is diluting native-orientation or SZA-related calibration cues, ABI-152 should reduce filtered predicted-positive clutter or improve filtered precision/connectivity relative to ABI-130 while avoiding severe MIT/Google source imbalance. If random mirroring is beneficial regularization, ABI-152 should underperform ABI-130, which would be useful negative evidence before spending more steps on this branch. A diagnostically valuable outcome may be a precision/connectivity gain even with modest aggregate Dice loss, or confirmation that no-augmentation is harmful in both frequency-gated and SZA ASPP/detail families.

## Implementation Sketch

- Reuse ABI-130's compact torch-only ASPP/detail encoder-decoder and SZA-aware front end: normalized ABI channels, deterministic thermal BTD planes from approved ABI channels 1-16, normalized SZA and `cos(SZA)`, learned 1x1 spectral/SZA projection, full-resolution detail/context stem, residual encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail path, and line-aware refinement.
- Emit primary `mask_logits` and provider-declared auxiliary `centerline_logits`.
- Change only the manifest augmentation policy from trusted `random_mirroring` to trusted `none`.
- Keep provider-approved `abi_16ch_plus_sza`, trusted `bce_dice` primary loss, Centerline Target auxiliary weighted BCE at 0.02, `combined_source_balanced` traversal, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, Dataset Source identity, and external metadata are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, augmentation policy `none`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation semantics, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, thresholding, postprocessing, prediction retention, resource limits, execution, and lifecycle.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No Experiment Batch, full-data promotion claim, or Post-Run Evaluation is requested by this handoff.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported.
6. As family-development evidence, the result is useful if it ties ABI-130 within about 0.005 filtered Dice, improves ABI-130 filtered precision/connectivity or positive-area discipline without severe source Dice loss, improves aggregate filtered Dice over ABI-130, or cleanly shows that disabling mirroring is harmful for this SZA-aware branch.

## Continuation and Hard Stop

Continue no-augmentation SZA ASPP/detail work only if ABI-152 is finite, non-degenerate, source-informative, and improves a meaningful ABI-130-relative diagnostic: precision, connectivity, predicted-positive discipline, source balance, MIT Dice/recall, or aggregate filtered Dice. Stop this exact no-augmentation branch if it has non-finite behavior, prediction collapse, resource failure, or a finite result materially below ABI-130 without compensating precision/connectivity/source-balance gains.

## Fallback/Next Decision

If ABI-152 improves or near-ties ABI-130 with better calibration/connectivity, request whole-validation diagnostics in a later Autonomy Step before any promotion interpretation. If it underperforms, document the result and broaden to a different architecture family, preprocessing, loss/auxiliary-target choice, or other trusted data-policy frontier rather than repeating further ad-hoc SZA ASPP/detail front-end edits.
