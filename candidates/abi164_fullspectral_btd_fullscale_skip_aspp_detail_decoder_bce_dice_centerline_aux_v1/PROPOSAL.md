# ABI-164 Full-Spectral BTD Full-Scale Skip ASPP/Detail Decoder BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-154 established a whole-validation-tested SZA-aware full-scale skip ASPP/detail branch with strong precision, connectivity, and positive-area discipline, but it remained slightly behind ABI-130 and ABI-068 on aggregate filtered Dice and under-recalled positive patches at the fixed threshold. ABI-155 through ABI-160 and ABI-162/ABI-163 show that late calibration heads, extra auxiliary supervision, coarse recall bridges, mid-level directional context, and compact BiFPN variants did not produce a better default-threshold balance. ABI-164 changes a different controlled axis: remove Solar Geometry Input from ABI-154 while preserving its full-scale skip architecture and trusted BCE-Dice policy.

## Hypothesis

ABI-154's useful behavior may come primarily from full-scale skip aggregation rather than from SZA conditioning. Removing SZA while retaining normalized full-spectral ABI channels, deterministic thermal BTD planes, learned ABI-only channel mixing, ASPP context, high-resolution detail features, and full-scale skip fusion may recover some ABI-126/ABI-066-style source balance, Google strength, and threshold stability without sacrificing the full-scale branch's precision/connectivity discipline. If SZA was contributing to conservative under-recall or source trade-offs in ABI-154, an ABI-only full-scale skip continuation should move the operating point toward ABI-126/ABI-130 while testing the independent value of the full-scale skip topology.

## Comparison Target

The primary comparison target is ABI-154 `abi154_fullspectral_btd_sza_fullscale_skip_aspp_detail_decoder_bce_dice_centerline_aux_v1`, Run `run_20260901_071026_32d3ec`, with capped filtered Dice 0.3944, MIT/Google filtered Dice 0.3824/0.4260, filtered precision 0.4777, recall 0.3359, connectivity 0.4374, and whole-validation filtered Dice 0.3941.

Secondary references are ABI-130 `run_20260831_121006_7d24be` as the SZA-aware ASPP/detail aggregate reference, ABI-126 `run_20260831_085615_d05ab3` as the non-SZA ASPP/detail precision/connectivity comparator, ABI-068 `run_20260828_010836_4ccc77` as the current local aggregate/source-balance reference, and canonical MCAST 2.1 as promotion context only.

## Expected Effect

A useful outcome would keep aggregate filtered Dice within roughly 0.005-0.010 of ABI-154 while improving at least one of recall, Google filtered Dice, MIT/Google balance, or late-epoch stability and preserving materially better precision/connectivity than recent negative recall-bridge variants. A stronger outcome would exceed ABI-154 or ABI-130 aggregate filtered Dice while retaining filtered connectivity above about 0.40. A negative outcome would show that ABI-154's full-scale skip value depends on SZA-aware features or that removing SZA collapses the precision/connectivity branch toward ABI-126-like limits without compensating source-balance gains.

## Implementation Sketch

- Start from the ABI-154 full-scale skip ASPP/detail decoder implementation.
- Change the provider input mode from `abi_16ch_plus_sza` to `abi_16ch`.
- Normalize only GOES ABI channels 1-16, derive the same deterministic thermal BTD planes from approved ABI channels, and use a learned 1x1 mixer over the normalized ABI channels only.
- Keep the compact residual encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail/context stem, full-scale skip fusion, line-aware final refinement, primary `mask_logits`, and provider-derived `centerline_logits` auxiliary output.
- Request one sequential Run; no candidate-owned scheduling, GPU placement, thresholding, postprocessing, data loading, sampling implementation, augmentation, target derivation, loss, or metric code is introduced.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, Solar Geometry Input, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
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
6. As family-development evidence, the result is useful if it preserves ABI-154-like precision/connectivity while improving recall, Google filtered Dice, source balance, aggregate Dice, or late-epoch stability.

## Continuation and hard stop

Continue this branch only if ABI-164 is finite, non-degenerate, source-informative, and preserves at least one useful ABI-154-relative diagnostic such as precision, connectivity, positive-area discipline, source balance, recall recovery, or late-epoch trajectory. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. If it completes finite but falls materially below ABI-154, ABI-130, and ABI-126 without a compensating source-balance or precision/connectivity gain, stop the exact ABI-only full-scale skip variant and broaden to another architecture/front-end/data-policy frontier.

## Fallback/Next Decision

If this candidate fails from a narrow implementation defect while the ABI-only full-scale skip hypothesis remains intact, consider at most one explicit Repair Candidate in a later Autonomy Step. If it is scientifically negative, document the result and broaden away from local ASPP/detail decoder variants. If it unexpectedly challenges current references on capped and source-stratified metrics, request separate whole-validation diagnostics before making any full-data or promotion claim.
