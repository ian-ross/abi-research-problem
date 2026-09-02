# ABI-166 full-spectral BTD+SZA oriented line-bank ASPP/detail decoder

## Hypothesis

Family-development continuation. Recent local full-scale skip and soft ridge-gate follow-ups show that extra auxiliary heads, late calibration gates, and coarse recall bridges can raise recall slightly but often damage precision and Contrail Connectivity. A full-resolution oriented line-bank refinement that explicitly fuses horizontal, vertical, and diagonal feature context may recover continuous thin-line evidence while preserving the calibrated BCE-Dice operating point of the SZA-aware ASPP/detail decoder.

## Comparison Target

Primary comparison targets are ABI-154 (`run_20260901_071026_32d3ec`) for high precision/connectivity in the full-scale skip ASPP/detail branch, ABI-130 (`run_20260831_121006_7d24be`) for the SZA-aware ASPP/detail aggregate reference, ABI-068 (`run_20260828_010836_4ccc77`) as the current capped filtered-Dice/source-balance reference, and ABI-165 (`run_20260901_163629_b45b2d`) as the latest negative auxiliary/gating continuation.

## Expected Effect

The oriented line-bank should improve or preserve filtered connectivity and source-stratified Dice by giving the final feature map non-wrapping multi-orientation line context before mask prediction. Desired behavior is not merely more predicted-positive area: useful evidence would keep precision near ABI-154/130 while improving recall or connectivity relative to recent local follow-ups.

## Implementation Sketch

Start from the ABI-154 full-spectral BTD+SZA full-scale skip ASPP/detail decoder. Keep the normalized ABI, thermal BTD, Solar Geometry Input, learned 1x1 front-end features, detail/context stem, encoder, ASPP context, decoder, and full-scale skip fusion. Replace the prior horizontal/vertical-only line-aware refinement with an oriented line-bank refinement that combines local high-frequency detail, learned horizontal and vertical context convolutions, fixed diagonal and anti-diagonal feature averages, a neutral multiplicative feature gate, and a residual projection before the `mask_logits` and `centerline_logits` heads.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza`; no longitude or latitude inputs.
- `output_form: mask_logits` plus provider-derived `centerline_logits` auxiliary output.
- Trusted primary loss `bce_dice` and trusted auxiliary loss `weighted_bce` for `centerline` at weight 0.02.
- Provider/Harness-owned `combined_source_balanced` sampling traversal and `random_mirroring` augmentation.
- Candidate code owns architecture only; it does not implement data loading, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, sampling, augmentation, resource placement, network access, or pretrained weights.

## Budget Requested

Use the active bounded representative policy: 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, max 12 epochs, batch size 4, constant learning rate 0.0003, AdamW, disabled early stopping, A100 placement owned by the Harness, 3,600-second training timeout, and the configured first-four prediction retention policy.

## Success Criteria

Treat this as capped family-development evidence, not promotion-grade full-data evidence. Useful continuation evidence would include a finite non-collapsed Run with aggregate `val/filtered_dice` within roughly 0.005-0.010 of ABI-154/ABI-130 or a clear secondary-metric gain, no Dataset Source catastrophic failure, MIT and Google filtered Dice both in the current leading band, filtered connectivity at or above ABI-154's high-connectivity reference, and no large raw-to-filtered dependence. A result that is lower on aggregate Dice but materially improves connectivity/source balance without excessive predicted-positive fraction may justify one follow-up; a broad positive-area recall shift with precision/connectivity loss would not.

## Fallback/Next Decision

If ABI-166 fails by non-finite behavior, prediction collapse, resource timeout, or a contract issue, classify the failure before repair. If it completes finitely but repeats the recent pattern of modest recall gain with precision/connectivity loss, do not repeat this exact oriented-line-bank branch; broaden to another architecture family or request trusted operating-point diagnostics for the capped leaders rather than adding more local gates or auxiliary heads.
