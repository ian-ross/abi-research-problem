# ABI-154 Full-Spectral BTD+SZA Full-Scale Skip ASPP/Detail Decoder BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-130 is the best whole-validation-tested SZA-aware ASPP/detail BCE-Dice branch: it nearly ties ABI-068 on aggregate filtered Dice and improves ABI-126's fixed-threshold recall, but it gives back some ABI-126/ABI-066 connectivity and negative-patch discipline. Recent local tweaks around loss, simple front ends, output heads, augmentation, and ridge gates did not improve that trade-off. ABI-154 keeps ABI-130's trusted input/loss/data/training policy and tests a controlled decoder-architecture change: full-scale skip aggregation before final refinement.

## Hypothesis

Contrail masks need both fine line evidence and broad cloud-context calibration. ABI-130's ASPP/detail decoder already combines bottleneck context with a high-resolution detail stem, but its final mask features are dominated by the last decoder scale plus local detail. A compact full-scale skip aggregation module may preserve low-resolution scene context, intermediate cloud-edge structure, and high-resolution line detail simultaneously at mask resolution. This should improve connectivity and positive-area discipline relative to ABI-130 without reverting to ABI-126-style MIT under-recall or moving thresholding/postprocessing into candidate code.

## Comparison Target

The primary comparison target is ABI-130 `abi130_fullspectral_btd_aspp_detail_decoder_sza_bce_dice_centerline_aux_v1`, Run `run_20260831_121006_7d24be`: capped filtered Dice 0.3953, MIT/Google filtered Dice 0.3779/0.4404, filtered precision 0.4415, recall 0.3578, connectivity 0.3851, and filtered predicted-positive fraction 0.00294. Its whole-validation diagnostic reached filtered Dice 0.3954 and confirmed the same recall-versus-connectivity trade-off.

Secondary references are ABI-068 `run_20260828_010836_4ccc77` as the local aggregate/source-balance reference, ABI-126 `run_20260831_085615_d05ab3` as the ASPP/detail precision/connectivity reference, ABI-066 `run_20260827_230540_bf4ce3` as the high-connectivity reference, and ABI-143 `run_20260831_224534_27b73d` as a nearby SZA-aware BCE-Dice ridge branch. Canonical MCAST 2.1 remains promotion context only.

## Expected Effect

A useful outcome would keep aggregate filtered Dice within roughly 0.005-0.010 of ABI-130 while increasing filtered connectivity, precision, or lowering filtered predicted-positive fraction. A stronger outcome would improve aggregate filtered Dice or MIT filtered Dice without sacrificing ABI-130's Google strength. A negative outcome would show that extra all-scale decoder fusion adds learned degrees of freedom that disrupt ABI-130's calibrated SZA operating point.

## Implementation Sketch

- Reuse ABI-130's normalized full-spectral raw features, deterministic thermal BTD planes from approved ABI channels, normalized SZA and `cos(SZA)` features, and learned 1x1 spectral projection.
- Keep the compact residual encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail/context stem, and line-aware final refinement.
- Add a compact `FullScaleSkipFusion` module that projects stem, encoder levels, ASPP context, decoder levels, and high-resolution detail features to mask resolution, concatenates them, and fuses them with GroupNorm/GELU residual blocks.
- Feed the fused full-scale feature alongside the original decoder, detail, and stem features before the final line-aware refinement.
- Emit primary `mask_logits` and provider-derived auxiliary `centerline_logits` only.
- Request one sequential Run; no candidate-owned scheduling, GPU placement, postprocessing, thresholding, data loading, loss, target, augmentation, sampling, or metric code is introduced.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
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
6. As family-development evidence, the result is useful if it improves ABI-130 connectivity, precision, positive-area discipline, aggregate Dice, MIT Dice, or source balance without materially damaging ABI-130's Google filtered Dice.

## Continuation and hard stop

Continue this full-scale skip branch only if ABI-154 is finite, non-degenerate, source-informative, and preserves at least one useful ABI-130-relative diagnostic such as connectivity, precision, positive-area discipline, source balance, or late-epoch trajectory. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. If it completes finite but falls materially below ABI-130 and ABI-143 without a compensating connectivity/precision/source-balance gain, stop the exact full-scale skip aggregation variant and broaden away from local ASPP/detail decoder changes.

## Fallback/Next Decision

If this candidate fails from a narrow implementation defect while the full-scale skip hypothesis remains intact, consider at most one explicit Repair Candidate in a later Autonomy Step. If it is scientifically negative, document the result and broaden to another contract-compliant architecture, calibration, data-policy, loss/auxiliary, or preprocessing frontier rather than repeating ad-hoc ASPP/detail decoder additions. If it unexpectedly challenges current references on capped and source-stratified metrics, request separate whole-validation diagnostics before making any full-data or promotion claim.
