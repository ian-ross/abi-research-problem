# ABI-159 Full-Spectral BTD+SZA Coarse-Recall-Bridge ASPP/Detail Decoder BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-154 is the whole-validation-tested full-scale skip ASPP/detail precision/connectivity branch, but its capped selected checkpoint is under-recall relative to ABI-130 and ABI-068. ABI-155/156/158 showed that late logit calibration, feature calibration, and extra Line Target supervision did not recover useful recall without damaging precision or connectivity. ABI-159 keeps ABI-154's trusted input, loss, data, training policy, and centerline auxiliary target, while changing the architecture to inject coarse semantic recall support before final full-scale refinement.

## Hypothesis

ABI-154's all-scale fusion improved positive-area discipline and Contrail Connectivity Metric but remained conservative at the fixed threshold. A compact coarse recall bridge that projects ASPP context, decoder scales, and high-resolution detail to mask resolution before final refinement may expose faint broad-support contrail candidates earlier than the final mask head. Because the bridge is concatenated into learned features rather than used for thresholding or postprocessing, it can improve fixed-threshold recall while preserving ABI-154's precision/connectivity advantages under provider-owned losses and metrics.

## Comparison Target

The primary comparison target is ABI-154 `abi154_fullspectral_btd_sza_fullscale_skip_aspp_detail_decoder_bce_dice_centerline_aux_v1`, Run `run_20260901_071026_32d3ec`: capped filtered Dice 0.3944, MIT/Google filtered Dice 0.3824/0.4260, filtered precision 0.4777, recall 0.3359, connectivity 0.4374, and filtered predicted-positive fraction 0.00255. ABI-154 also has whole-validation failure-bucket diagnostics showing a useful precision/connectivity profile but persistent false negatives.

Secondary references are ABI-130 `run_20260831_121006_7d24be` as the SZA-aware ASPP/detail aggregate/reference branch, ABI-156 `run_20260901_090713_9c7d32` as the best local full-scale skip calibration continuation, ABI-158 `run_20260901_105011_c26d0c` as the negative Line+Centerline auxiliary continuation, and ABI-068 `run_20260828_010836_4ccc77` as the local capped aggregate/source-balance reference. Canonical MCAST 2.1 remains promotion context only.

## Expected Effect

A useful outcome would increase filtered recall versus ABI-154 by at least 0.015 while keeping aggregate filtered Dice within roughly 0.005-0.010 of ABI-154 and retaining materially better precision/connectivity than ABI-158. A stronger outcome would match or improve ABI-154 aggregate filtered Dice while increasing recall or MIT Dice. A negative outcome would show that adding pre-final coarse support merely raises positive area or disrupts full-scale skip calibration without improving Dice/source balance.

## Implementation Sketch

- Reuse ABI-154's normalized full-spectral ABI features, deterministic thermal BTD planes from approved ABI channels, normalized SZA and `cos(SZA)` features, and learned 1x1 spectral projection.
- Keep the compact residual encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail/context stem, full-scale skip aggregation, and line-aware final refinement.
- Add a compact `CoarseRecallBridge` that projects ASPP context, decoder levels, and high-resolution detail to mask resolution and fuses them with GroupNorm/GELU residual blocks.
- Concatenate this recall-support feature with decoder, detail, stem, and full-scale skip features before final projection.
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
6. As family-development evidence, the result is useful if it improves ABI-154 recall, MIT Dice, source balance, aggregate Dice, or ABI-154-relative false-negative behavior while preserving reasonable precision/connectivity and avoiding ABI-158-like degradation.

## Continuation and hard stop

Continue this exact coarse-recall-bridge branch only if ABI-159 is finite, non-degenerate, source-informative, and preserves at least one useful ABI-154-relative diagnostic such as recall, MIT Dice, aggregate Dice, source balance, or late-epoch trajectory without severe precision/connectivity loss. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. If it completes finite but falls materially below ABI-154/156 and ABI-130 without a compensating recall/source-balance gain, stop the branch and broaden further away from full-scale skip ASPP/detail variants.

## Fallback/Next Decision

If this candidate fails from a narrow implementation defect while the coarse-recall-bridge hypothesis remains intact, consider at most one explicit Repair Candidate in a later Autonomy Step. If it is scientifically negative, document the result and broaden to another contract-compliant architecture family, loss/auxiliary/data-policy choice, or preprocessing/front-end inductive bias rather than repeating local decoder additions. If it unexpectedly challenges current references on capped and source-stratified metrics, request separate whole-validation diagnostics before making any full-data or promotion claim.
