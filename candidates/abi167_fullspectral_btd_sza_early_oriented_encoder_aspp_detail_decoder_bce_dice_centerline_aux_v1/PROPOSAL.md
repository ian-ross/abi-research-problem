# ABI-167 full-spectral BTD+SZA early-oriented encoder ASPP/detail decoder

## Hypothesis

Family-development continuation. ABI-166 showed that adding an oriented line bank only at the final full-resolution refinement stage did not preserve ABI-154's high-connectivity behavior and reduced precision/source Dice. The failure suggests that orientation evidence may need to shape intermediate features before bottleneck/context aggregation and skip fusion. ABI-167 tests whether lightweight, neutral additive horizontal/vertical/diagonal context blocks inserted throughout the stem, encoder, and decoder can improve thin-line continuity and source balance while retaining the calibrated BCE-Dice operating point.

## Comparison Target

Primary comparison targets are ABI-068 (`run_20260828_010836_4ccc77`) as the current capped filtered-Dice/source-balance reference, ABI-130 (`run_20260831_121006_7d24be`) as the SZA-aware ASPP/detail BCE-Dice reference, ABI-154 (`run_20260901_071026_32d3ec`) as the high-precision/high-connectivity full-scale skip ASPP/detail reference, and ABI-166 (`run_20260901_173120_9c74ab`) as the late-oriented-line-bank predecessor.

## Expected Effect

Early multi-scale oriented context should let the encoder and decoder represent elongated ABI/BTD/SZA line evidence before the final mask head, rather than trying to repair continuity after context/detail fusion. Useful behavior would include filtered connectivity closer to ABI-154, aggregate filtered Dice in the ABI-068/130/154 leader band, and no shift toward broad positive-area overprediction. A failure that repeats ABI-166's lower Dice and lower connectivity would argue against this oriented-context placement within the ASPP/detail branch.

## Implementation Sketch

Start from the ABI-154 full-spectral BTD+SZA full-scale skip ASPP/detail decoder. Keep the normalized ABI, deterministic thermal BTD planes, normalized and cosine Solar Geometry Input, learned 1x1 front-end mixture, detail/context stem, ASPP bottleneck, decoder, full-scale skip fusion, and BCE-Dice/Centerline-auxiliary training policy. Add `EarlyOrientedContextBlock` modules after the initial stem/enc0 stage, each encoder downsample, and each decoder fusion. Each block computes a local residual feature, depthwise horizontal and vertical context, fixed diagonal and anti-diagonal no-wrap averages, projects the concatenated evidence, and adds a small learnable bounded residual back to the scale feature. The final head remains the ABI-154-style local/horizontal/vertical refinement rather than the ABI-166 late diagonal line bank, so the controlled change is early/multi-scale placement of oriented context.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza`; no longitude or latitude inputs.
- `output_form: mask_logits` plus provider-derived `centerline_logits` auxiliary output.
- Trusted primary loss `bce_dice` and trusted auxiliary loss `weighted_bce` for `centerline` at weight 0.02.
- Provider/Harness-owned `combined_source_balanced` sampling traversal and `random_mirroring` augmentation.
- Candidate code owns architecture only; it does not implement data loading, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, sampling, augmentation, resource placement, network access, or pretrained weights.

## Budget Requested

Use the active bounded representative policy: 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, max 12 epochs, batch size 4, constant learning rate 0.0003, AdamW, disabled early stopping, A100 placement owned by the Harness, 3,600-second training timeout, and the configured first-four prediction retention policy.

## Success Criteria

Treat this as capped family-development evidence, not promotion-grade full-data evidence. Useful continuation evidence would be a finite non-collapsed Run with aggregate `val/filtered_dice` within roughly 0.005-0.010 of ABI-068/130/154, filtered connectivity at or above ABI-130 and moving toward ABI-154, MIT and Google filtered Dice both in the current leading band, modest raw-to-filtered dependence, and no excessive predicted-positive fraction. Even without beating ABI-068, a clear connectivity or MIT-source gain with similar Dice could justify one follow-up; low Dice with continuing improvement is diagnostic but not promotion evidence.

## Fallback/Next Decision

If ABI-167 fails by non-finite behavior, prediction collapse, resource timeout, or a contract issue, classify the failure before repair. If it completes finitely but reproduces ABI-166's lower-connectivity/lower-Dice pattern, do not keep adding local oriented gates to the same ASPP/detail branch; broaden to another architecture family or request trusted whole-validation/operating-point diagnostics for the capped leaders.
