# ABI-124: full-spectral BTD frequency-gated line U-Net stem detail-agreement calibration

## Hypothesis

ABI-068 is the current strongest local whole-validation-tested Candidate by aggregate filtered Dice, but its full-validation diagnostics showed more negative-patch clutter and lower precision/connectivity than ABI-066. ABI-123 showed that a blunt patch-level objectness gate worsens precision, connectivity, and Google Dice. A neutral-initialized pixelwise calibration block placed early at the full-resolution stem may recover some precision/connectivity by requiring agreement between local high-frequency detail and smoothed context before false positives propagate through the encoder, without imposing candidate-owned thresholding, postprocessing, loss changes, or Artifact Filters.

This is a **family-development continuation** of the ABI-068 frequency-gated line U-Net branch, not a promotion claim from capped evidence.

## Comparison Target

Primary comparison target: ABI-068 (`run_20260828_010836_4ccc77`), the frequency-gated line U-Net focal-Tversky centerline-auxiliary reference and current strongest local whole-validation-tested Candidate by filtered Dice.

Secondary references: ABI-066 (`run_20260827_230540_bf4ce3`) for precision/connectivity discipline, ABI-121 (`run_20260831_041559_43da35`) for ASPP/detail recall/source-balance behavior, and ABI-123 (`run_20260831_060046_508684`) as the negative result for global patch objectness gating.

## Expected Effect

The stem detail-agreement calibrator should reduce low-confidence negative-patch clutter relative to ABI-068/ABI-123 while preserving ABI-068-like recall and source balance. Because the final agreement projection is zero-initialized and the residual is bounded, the model should start close to ABI-068 and only learn local corrections when detail/context evidence helps. A useful result would show higher filtered precision or connectivity with no substantial collapse in MIT/Google filtered Dice.

## Implementation Sketch

Start from ABI-068. Keep its normalized raw-plus-BTD front end, frequency-split stem, frequency-gated encoder/decoder, pyramid fusion, line refiner, mask head, and centerline auxiliary head. Add one `StemDetailAgreementCalibrator` after the full-resolution stem and before `enc1`.

The calibrator computes local detail as stem features minus a 9x9 smoothed version, computes smoothed context with a 17x17 average pool, projects detail and context with 1x1 Conv/GN/GELU blocks, and concatenates them with the original stem features. A support branch proposes residual features; a separate zero-initialized 1x1 agreement projection produces a bounded `tanh` agreement map. The returned stem features are `inputs + 0.25 * agreement * support`, making the block neutral at initialization and architecture-owned during training.

## Contract Features Used

- `input_mode: abi_16ch`; no longitude or latitude inputs.
- `output_form: mask_logits` plus provider-declared `centerline_logits` auxiliary output.
- Trusted primary loss `focal_tversky`.
- Trusted auxiliary target `centerline` with `weighted_bce` weight 0.02.
- Trusted `combined_source_balanced` sampling traversal and `random_mirroring` augmentation policy.
- AdamW optimizer, learning rate `0.0003`, batch size 4, max epochs 12, and `constant_lr` scheduler under the active Harness bounds.

Candidate code owns only model architecture. It does not implement data loading, split logic, capped-record selection, sampling, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, filesystem writes, network access, pretrained weights, resource placement, or lifecycle behavior.

## Budget Requested

Run one sequential capped representative Candidate under the active Workspace Configuration: up to 1,024 provider-selected train and validation records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, constant learning rate, disabled early stopping, 3,600-second Docker wall-clock budget, A100 execution as configured by the Harness, and the fixed first-four prediction artifact retention policy.

## Success Criteria

Do not require a capped Run to be promotion-grade. Treat ABI-124 as useful family-development evidence if it completes finitely without prediction collapse and satisfies most of:

- aggregate capped `val/filtered_dice` within about 0.01 of ABI-068 or better;
- filtered precision or filtered connectivity improves over ABI-068 without an ABI-123-like positive-area increase;
- both MIT and Google filtered Dice remain non-catastrophic and reasonably source-balanced;
- filtered predicted-positive fraction remains near or below ABI-068's 0.00357 rather than ABI-123's 0.00499;
- learning trajectory is finite and improving or diagnostically informative through the 12-epoch cap.

## Fallback/Next Decision

If ABI-124 regresses like ABI-123, stop this exact stem detail-agreement branch and avoid further blunt gating additions to ABI-068. If it improves precision/connectivity but slightly trails ABI-068 in aggregate Dice, retain it as a calibration/line-quality reference and consider a bounded follow-up that tunes the residual placement or auxiliary mix. If it clearly improves aggregate Dice or preserves ABI-068 Dice while recovering precision/connectivity, request whole-validation failure-bucket analysis before any promotion interpretation.
