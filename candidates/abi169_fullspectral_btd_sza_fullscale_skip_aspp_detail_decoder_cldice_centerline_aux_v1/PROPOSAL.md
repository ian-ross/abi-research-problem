# ABI-169 Full-Spectral BTD+SZA Full-Scale Skip ASPP/Detail Decoder clDice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-154 showed that the SZA-aware full-scale skip ASPP/detail decoder can run within the active resource envelope and produced the strongest precision/connectivity profile in the recent ASPP/detail branch, but it under-recalled relative to ABI-068 and ABI-130. ABI-169 keeps ABI-154's architecture, input, data traversal, augmentation, auxiliary target, optimizer, learning rate, batch size, and epoch budget, changing only the trusted primary loss from `bce_dice` to `bce_dice_cldice`.

## Hypothesis

The full-scale skip ASPP/detail decoder already preserves high-resolution detail, intermediate cloud-edge structure, and low-resolution context at mask resolution. Its main deficit is recall/source balance rather than Artifact Filter dependence. A trusted BCE-Dice-clDice objective may bias the same feature geometry toward connected thin-line masks, testing whether the ABI-154 connectivity strength can be retained or improved while recovering some missed contrail extent without candidate-owned thresholding or postprocessing.

## Comparison Target

The primary comparison target is ABI-154 `abi154_fullspectral_btd_sza_fullscale_skip_aspp_detail_decoder_bce_dice_centerline_aux_v1`, Run `run_20260901_071026_32d3ec`: capped filtered Dice 0.3944, MIT/Google filtered Dice 0.3824/0.4260, filtered precision 0.4777, filtered recall 0.3359, filtered connectivity 0.4374, and filtered predicted-positive fraction 0.00255.

Secondary references are ABI-068 `run_20260828_010836_4ccc77` as the current capped aggregate/source-balance leader, ABI-130 `run_20260831_121006_7d24be` as the SZA-aware ASPP/detail recall/reference branch, ABI-143 `run_20260831_224534_27b73d` as a strong SZA-aware ridge branch, and ABI-168 `run_20260901_192929_0da8c3` as a recent negative oriented-context repair. Canonical MCAST 2.1 remains promotion context only.

## Expected Effect

A useful outcome would keep aggregate filtered Dice within roughly 0.005-0.010 of ABI-154 while improving filtered recall, MIT filtered Dice, or filtered connectivity. A stronger outcome would challenge ABI-068 on aggregate filtered Dice while retaining ABI-154-like precision and connectivity. A negative outcome would show that clDice pressure disrupts the calibrated high-precision full-scale skip operating point under the current 12-epoch constant-LR budget.

## Implementation Sketch

- Reuse ABI-154's normalized full-spectral ABI features, deterministic thermal BTD planes from approved ABI channels, normalized SZA and `cos(SZA)` features, and learned 1x1 spectral projection.
- Reuse the residual encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail/context stem, full-scale skip aggregation, and line-aware final refinement.
- Emit only primary `mask_logits` and provider-derived auxiliary `centerline_logits`.
- Change the manifest primary loss to trusted `bce_dice_cldice`; retain trusted centerline auxiliary `weighted_bce` at weight 0.02.
- Request one sequential Run; no candidate-owned scheduling, GPU placement, postprocessing, thresholding, data loading, loss, target, augmentation, sampling, or metric code is introduced.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice_cldice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data claim, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes inside the trusted runtime envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it improves ABI-154 recall, MIT Dice, connectivity, or aggregate Dice without a severe precision/source-balance loss.

## Continuation and hard stop

Continue this loss branch only if ABI-169 is finite, non-degenerate, source-informative, and preserves at least one useful ABI-154-relative diagnostic such as connectivity, precision, positive-area discipline, source balance, or late-epoch trajectory. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. If it completes finite but falls materially below ABI-154 and ABI-068 without a compensating recall/connectivity/source-balance gain, stop the exact full-scale skip clDice branch and broaden away from local ASPP/detail loss changes.

## Fallback/Next Decision

If this candidate fails from a narrow implementation defect while the loss-comparison hypothesis remains intact, consider at most one explicit Repair Candidate in a later Autonomy Step. If it is scientifically negative, document the result and broaden to another contract-compliant architecture, data-policy, calibration, or preprocessing frontier. If it unexpectedly challenges current references on capped and source-stratified metrics, request separate whole-validation diagnostics before making any full-data or promotion claim.
