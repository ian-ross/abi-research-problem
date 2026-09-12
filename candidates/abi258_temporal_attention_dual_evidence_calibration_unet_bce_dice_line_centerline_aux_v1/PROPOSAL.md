# ABI-258 temporal attention dual-evidence calibration U-Net

## Hypothesis

ABI-223 remains the strongest temporal-attention comparator and its temporal-eligible diagnostic showed substantial lower-threshold recall headroom without Artifact Filter dependence. ABI-254 showed that simply adding a center-detail evidence bridge is useful at exploratory scale but unstable and below ABI-223, while ABI-257 showed that moving oriented line evidence into a recurrent stem regresses both overlap and continuity. ABI-258 tests a narrower architecture-level calibration mechanism: keep ABI-223's finite temporal-attention fusion and replace only the final mask head with a bounded dual recall/precision evidence head that can raise true contrail logits at threshold 0.5 without candidate-owned thresholding, losses, metrics, or postprocessing.

This is a **family-development continuation** within temporal-attention modeling, not a promotion claim.

## Comparison Target

Primary comparison target: ABI-223 (`run_20260908_154531_8c7e2b`), the late36 temporal-attention fusion U-Net with temporal-eligible filtered Dice 0.4198, precision 0.4838, recall 0.3707, connectivity 0.4124, MIT filtered Dice 0.3985, and Google filtered Dice 0.4768.

Secondary temporal context: ABI-254 center-detail evidence bridge (`run_20260911_202724_fee837`), ABI-255 recurrent change-state late36 (`run_20260911_210922_27f346`), ABI-257 oriented recurrent line-state (`run_20260911_235337_128345`), and ABI-202 as the mature aggregate whole-validation frontier context.

## Expected Effect

The expected effect is improved fixed-threshold recall and positive-patch coverage relative to an exploratory temporal-attention head while preserving ABI-223-style precision discipline and temporal connectivity. The dual evidence head gives the decoder separate recall-oriented and precision-oriented feature branches, then learns a per-pixel agreement gate and bounded residual contribution to the primary mask logits. A useful result would raise recall or filtered Dice over ABI-254/222 and approach ABI-223 without the coverage instability seen in ABI-254 or the continuity loss seen in ABI-257.

## Implementation Sketch

Start from the ABI-223 compact temporal-attention fusion U-Net over provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`. Retain the trusted ABI/SZA normalization, ABI-channel-derived BTD features, per-frame projection, center-anchored temporal attention, explicit before/after change features, compact U-Net/ASPP decoder, BCE-Dice primary loss, source-balanced sampling, random mirroring, batch size 2, and trusted Line plus Centerline auxiliary outputs.

Replace the simple one-layer mask head with `DualEvidenceCalibrationHead`: a shared decoder refinement, a recall-oriented branch, a precision-oriented branch, a learned per-pixel agreement gate, and a bounded learned residual added to base mask logits. The residual is differentiable model logic only; it does not inspect targets, choose thresholds, morphologically filter outputs, alter Artifact Filters, implement losses/metrics, select samples, access coordinates, or read temporal cache paths.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal` with provider-owned temporal provisioning.
- `data.frame_selection_policy: temporal_eligible_center` and `data.temporal_frame_offsets: [-1, 0, 1]`.
- `data.sampling_policy: combined_source_balanced` and trusted `random_mirroring` augmentation.
- Trusted primary loss `bce_dice`, AdamW optimizer, and constant learning-rate scheduler.
- Trusted Line and Centerline auxiliary targets using `weighted_bce` weights 0.01 and 0.02.

Candidate code defines architecture only. It does not implement data loading, temporal lookup, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, longitude/latitude features, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Budget Requested

Use the default exploratory budget: 12 epochs, batch size 2, constant learning rate, disabled early stopping, provider-owned capped temporal-eligible selection, and the configured A100 execution policy. Do not request late36 for this mechanism-changing head. If the trajectory is finite, source-informative, and late-improving at epoch 12, a later step can decide whether an approved late-improving close continuation is justified.

## Success Criteria

Treat ABI-258 as useful temporal-family evidence if it completes finitely, avoids prediction collapse, remains source-informative on MIT and Google, and improves at least one of filtered recall, filtered Dice, MIT filtered Dice, or connectivity over ABI-254/222 without a severe precision collapse or positive-fraction blow-up. Near-ABI-223 filtered Dice with improved recall or cleaner positive-patch coverage would justify continued temporal calibration work. Promotion would require later trusted diagnostics and operator review; capped temporal-eligible evidence alone is not promotion evidence.

## Fallback/Next Decision

If ABI-258 fails contract, smoke, shape, numerical, or resource validation, repair only if the dual-evidence calibration hypothesis is preserved. If it completes but repeats ABI-254's oscillatory high-precision/low-recall pruning or ABI-257's connectivity/overlap regression, stop this exact head. If it is finite and late-improving near the exploratory ceiling, consider a later approved late36 close-continuation. If temporal attention remains below ABI-223 after this mechanism-changing head, broaden away from local temporal-head tuning toward another underexplored architecture family.
