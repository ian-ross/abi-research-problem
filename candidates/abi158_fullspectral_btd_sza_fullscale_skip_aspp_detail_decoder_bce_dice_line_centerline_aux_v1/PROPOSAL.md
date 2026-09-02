# ABI-158 Full-Spectral BTD+SZA Full-Scale Skip ASPP/Detail Decoder BCE-Dice Line+Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-154 is the strongest whole-validation-tested full-scale skip ASPP/detail branch: it preserved high precision and connectivity, but remained more conservative than desired at the fixed threshold. ABI-155/156 calibration tweaks and ABI-157 deterministic-shuffle traversal did not improve that trade-off. ABI-158 keeps ABI-154's trusted input, architecture, loss, data policy, augmentation, optimizer, learning rate, batch size, and epoch budget, and changes only the auxiliary-supervision axis by adding a low-weight provider-derived Line Target head alongside the existing Centerline Target head.

## Hypothesis

The full-scale skip decoder already collects high-resolution line detail, low-resolution cloud context, and intermediate features at mask resolution, but BCE-Dice training with only Centerline Target supervision may under-reward broader line-region evidence needed to lift fixed-threshold recall. A low-weight trusted Line Target auxiliary head should shape the shared refined features toward complete contrail line support while the primary BCE-Dice objective and existing Centerline Target keep the branch from drifting into broad cloud clutter. This may recover recall or connectivity relative to ABI-154 without candidate-owned thresholding, postprocessing, Artifact Filters, data loading, losses, metrics, or target transforms.

## Comparison Target

The primary comparison target is ABI-154 `abi154_fullspectral_btd_sza_fullscale_skip_aspp_detail_decoder_bce_dice_centerline_aux_v1`, Run `run_20260901_071026_32d3ec`: capped filtered Dice 0.3944, MIT/Google filtered Dice 0.3824/0.4260, filtered precision 0.4777, recall 0.3359, connectivity 0.4374, and filtered predicted-positive fraction 0.00255. Its whole-validation failure-bucket review made it the local full-scale skip precision/connectivity reference.

Secondary references are ABI-130 `run_20260831_121006_7d24be` as the SZA-aware ASPP/detail aggregate/reference branch, ABI-068 `run_20260828_010836_4ccc77` as the local capped aggregate/source-balance reference, ABI-126 `run_20260831_085615_d05ab3` as the ASPP/detail high-precision/connectivity comparator, and ABI-133 `run_20260831_144720_475594` as prior evidence for Line+Centerline auxiliary supervision in the non-full-scale ASPP/detail branch. Canonical MCAST 2.1 remains promotion context only.

## Expected Effect

A useful outcome would preserve ABI-154's high precision/connectivity profile while increasing filtered recall, MIT filtered Dice, aggregate filtered Dice, or line connectivity. A stronger outcome would challenge ABI-130/ABI-068 on aggregate capped Dice while retaining ABI-154-like positive-area discipline. A negative outcome would show that Line Target supervision simply adds auxiliary burden or over-expands positive area in the full-scale skip branch, matching prior mixed evidence from ABI-133.

## Implementation Sketch

- Reuse ABI-154's normalized full-spectral raw features, deterministic thermal BTD planes from approved ABI channels, normalized SZA and `cos(SZA)` features, and learned 1x1 spectral projection.
- Keep the compact residual encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail/context stem, full-scale skip fusion, final projection, and line-aware refinement unchanged.
- Add one low-capacity `line_logits` 1x1 auxiliary head from the same refined features that feed `mask_logits` and `centerline_logits`.
- Declare trusted auxiliary targets `line` at weight 0.01 and `centerline` at weight 0.02, both using provider-owned `weighted_bce`.
- Request one sequential Run; no candidate-owned scheduling, GPU placement, postprocessing, thresholding, data loading, loss, target, augmentation, sampling, or metric code is introduced.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
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
6. As family-development evidence, the result is useful if it improves ABI-154 recall, connectivity, aggregate Dice, MIT Dice, or source balance without materially damaging ABI-154 precision, positive-area discipline, or Google filtered Dice.

## Continuation and hard stop

Continue this Line+Centerline full-scale skip branch only if ABI-158 is finite, non-degenerate, source-informative, and preserves at least one useful ABI-154-relative diagnostic such as recall recovery, connectivity, precision, positive-area discipline, source balance, or late-epoch trajectory. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. If it completes finite but falls materially below ABI-154/ABI-130/ABI-068 without a compensating recall/connectivity/source-balance gain, stop the exact auxiliary-supervision variant and broaden away from local full-scale skip repairs.

## Fallback/Next Decision

If this candidate fails from a narrow implementation defect while the auxiliary-supervision hypothesis remains intact, consider at most one explicit Repair Candidate in a later Autonomy Step. If it is scientifically negative, document the result and broaden to another contract-compliant architecture, data-policy, loss/auxiliary, calibration, or preprocessing frontier. If it unexpectedly challenges current references on capped and source-stratified metrics, request separate whole-validation diagnostics before making any full-data or promotion claim.
