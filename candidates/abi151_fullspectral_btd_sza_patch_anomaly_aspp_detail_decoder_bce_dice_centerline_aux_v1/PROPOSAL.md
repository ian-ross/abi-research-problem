# ABI-151 Proposal: patch-anomaly SZA ASPP/detail decoder

## Hypothesis

ABI-151 is a **family-development continuation** of the SZA-aware full-spectral BTD ASPP/detail decoder branch. ABI-130 showed that provider-approved Solar Geometry Input can shift the ABI-126 BCE-Dice ASPP/detail branch toward better default-threshold recall and near-best aggregate Dice, but whole-validation diagnostics also confirmed added negative-patch clutter and lower connectivity versus ABI-126/ABI-066. Recent SZA-aware micro-architecture, ridge, frequency-support, and learning-rate edits did not improve this tradeoff.

The hypothesis is that patch-relative anomaly features computed only from provider-approved ABI channels, approved thermal BTD planes, and Solar Geometry Input can give the ASPP/detail decoder a source-robust local contrast representation. By supplying both absolute normalized spectral state and within-patch standardized deviations, the model may preserve ABI-130's recall benefit while improving negative-patch discipline, connectivity, or source balance without candidate-owned thresholding, postprocessing, loss changes, data access, or Artifact Filters.

## Comparison Target

Primary comparison target: ABI-130 `abi130_fullspectral_btd_aspp_detail_decoder_sza_bce_dice_centerline_aux_v1`, Run `run_20260831_121006_7d24be`, with capped filtered Dice 0.3953 and whole-validation filtered Dice 0.3954. Key capped metrics were MIT/Google filtered Dice 0.3779/0.4404, filtered precision 0.4415, recall 0.3578, connectivity 0.3851, and predicted-positive fraction 0.00294.

Secondary references are ABI-068 `run_20260828_010836_4ccc77` for the best local aggregate whole-validation-tested frequency-gated focal-Tversky profile, ABI-126 `run_20260831_085615_d05ab3` for ASPP/detail precision/connectivity, ABI-066 `run_20260827_230540_bf4ce3` for high-connectivity behavior, and ABI-150 `run_20260901_034937_91779f` as recent negative evidence against explicit structure-tensor features in the same SZA-aware ASPP/detail branch.

## Expected Effect

Patch-relative anomaly planes should emphasize contrail-like thin local departures from patch background brightness and reflectance while retaining absolute ABI/BTD/SZA context needed to avoid turning cloud edges or broad cloud decks into positives. Unlike hard structure-tensor features, the anomaly front end uses smooth mean/variance normalization with bounded clamping and should avoid non-finite gradients. Success would be a near-tie or improvement versus ABI-130 aggregate filtered Dice, or a diagnostically useful improvement in connectivity, precision, predicted-positive discipline, MIT recall/source balance, or late-epoch stability.

## Implementation Sketch

- Use provider-approved `abi_16ch_plus_sza` input only.
- Build a torch-only front end containing normalized ABI channels, deterministic thermal BTD planes derived from approved ABI channels 1-16, normalized SZA and cosine SZA, learned 1x1 spectral projection, and patch-relative anomaly planes.
- Compute anomaly planes by subtracting per-patch spatial means and dividing by per-patch spatial standard deviation with positive epsilon, then clamp to a bounded finite range. These statistics are computed only from the current approved input tensor and do not use Dataset Source identity, coordinates, raw labels, or external state.
- Feed the features into the compact ABI-130-style detail/context stem, residual encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail path, and line-aware refinement.
- Output primary `mask_logits` and provider-declared auxiliary `centerline_logits`.
- Keep trusted `bce_dice` primary loss, Centerline Target auxiliary weighted BCE at 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, Dataset Source identity, and external metadata are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-derived `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, thresholding, postprocessing, prediction retention, resource limits, execution, and lifecycle.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler, disabled early stopping, and the 3,600-second trusted training timeout. No Experiment Batch, full-data promotion claim, or Post-Run Evaluation is requested by this handoff.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count stays below the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Final predictions are finite and do not persistently collapse to all-negative or all-positive masks.
4. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported.
5. As family-development evidence, the result is useful if it ties ABI-130 within about 0.005 filtered Dice while improving connectivity, precision, predicted-positive discipline, source balance, MIT recall, or late-epoch trajectory; improves aggregate filtered Dice over ABI-130; or supplies clear negative evidence about patch-relative anomaly features for this branch.

## Continuation and Hard Stop

Continue this patch-anomaly ASPP/detail line only if ABI-151 is finite, non-degenerate, source-informative, and improves a meaningful ABI-130-relative diagnostic. Stop the exact branch if it has non-finite behavior, prediction collapse, resource failure, or a finite result materially below ABI-130 without compensating precision/connectivity/source-balance gains. A negative finite result should broaden the frontier rather than invite more ad-hoc ASPP/detail tweaks.

## Fallback/Next Decision

If ABI-151 improves or near-ties ABI-130 with better clutter/connectivity/source behavior, request whole-validation diagnostics in a later Autonomy Step before any promotion interpretation. If it underperforms like recent SZA-aware micro-architecture continuations, document the result and broaden to a different architecture, preprocessing, data-policy, augmentation, calibration, or mining frontier within the current contract.
