# ABI-165 Full-Spectral BTD+SZA Soft Ridge-Gate U-Net BCE-Dice Line+Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-143 brought the SZA-aware soft ridge-gate U-Net into the current capped reference band with filtered Dice 0.3947, MIT/Google filtered Dice 0.3815/0.4287, filtered recall 0.3801, and a final-epoch best checkpoint, but it gave up line connectivity relative to ABI-142, ABI-154, ABI-126, and ABI-068. ABI-153 showed that changing the same soft ridge-gate branch to trusted BCE-Dice-clDice did not recover a better operating point. ABI-165 therefore keeps ABI-143's stronger BCE-Dice calibration and tests a narrower trusted auxiliary-supervision axis: add low-weight Line Target supervision alongside Centerline Target.

## Hypothesis

The ABI-143 soft ridge gate may have recovered recall by allowing broader positive support while under-constraining connected line extent. Provider-derived Line Target supervision should encourage continuous thin-line evidence in the same high-resolution ridge features without moving thresholding, skeletonization, postprocessing, losses, or target generation into Candidate code. With a low auxiliary weight, the added line head should act as a training-time shape cue rather than a dominant objective, preserving ABI-143's near-best aggregate/source behavior while improving connectivity or precision/recall balance.

## Comparison Target

The primary comparison target is ABI-143 `abi143_fullspectral_btd_sza_soft_ridge_gate_unet_bce_dice_centerline_aux_v1`, Run `run_20260831_224534_27b73d`, with capped filtered Dice 0.3947, MIT/Google filtered Dice 0.3815/0.4287, filtered precision 0.4105, recall 0.3801, connectivity 0.3010, and filtered predicted-positive fraction 0.00336.

Secondary references are ABI-142 `run_20260831_215104_d4c318` for the ridge-attention predecessor with higher connectivity, ABI-153 `run_20260901_061306_9b10a4` for the clDice loss-axis continuation, ABI-068 `run_20260828_010836_4ccc77` as the current capped aggregate/source-balance reference, ABI-130 `run_20260831_121006_7d24be` as the SZA-aware ASPP/detail aggregate reference, and ABI-154 `run_20260901_071026_32d3ec` as the whole-validation-tested high-connectivity full-scale skip reference.

## Expected Effect

A useful outcome would keep aggregate filtered Dice within roughly 0.005 of ABI-143 while improving filtered connectivity, MIT filtered Dice, source balance, or the precision/recall balance. A stronger outcome would exceed ABI-143 and challenge ABI-068/ABI-130 on aggregate filtered Dice while moving connectivity toward ABI-142/ABI-154 without lowering Google filtered Dice below the current reference band. A negative outcome would show that Line Target supervision over-regularizes the soft ridge branch, lowers recall/precision balance, duplicates the ABI-153 loss-axis failure mode, or adds no measurable connectivity gain.

## Implementation Sketch

- Start from the ABI-143 SZA-aware full-spectral BTD soft ridge-gate U-Net implementation.
- Preserve provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD planes from approved ABI channels, normalized/cosine Solar Geometry features, and the learned 1x1 spectral/SZA mixer.
- Preserve the ridge-attention stem, compact residual encoder, dilated bottleneck context, bilinear decoder fusions, high-resolution ridge branch, neutral-initialized conservative ridge gate, and primary `mask_logits` head.
- Add a separate `line_logits` auxiliary head from the shared refined high-resolution features, while retaining the existing `centerline_logits` auxiliary head.
- Select trusted `bce_dice` primary loss, trusted weighted-BCE Line Target supervision at weight 0.01, and trusted weighted-BCE Centerline Target supervision at weight 0.02.
- Request one sequential representative capped Run; do not add Candidate-owned scheduling, data loading, augmentation, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, runtime downloads, or external persistence.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; GOES ABI channels 1-16 plus Solar Geometry Input are used, and longitude/latitude inputs, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits`, provider-declared auxiliary `[1, 256, 256]` `line_logits`, and provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data claim, Experiment Batch, Post-Run Evaluation, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes inside the trusted runtime envelope.
3. Primary and auxiliary losses, logits, gradients, parameters, metrics, and checkpoint state remain finite.
4. Predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it preserves ABI-143's near-reference aggregate/source behavior while improving filtered connectivity, precision/recall balance, MIT Dice, or line-structure diagnostics.

## Continuation and hard stop

Continue this branch only if ABI-165 is finite, non-degenerate, source-informative, and either improves a meaningful ABI-143-relative diagnostic or remains close enough to the ABI-142/ABI-143 ridge-family band with an interpretable trade-off. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. If it completes finite but materially worsens aggregate Dice without a compensating connectivity or source-balance gain, do not repeat this auxiliary combination unchanged.

## Fallback/Next Decision

If ABI-165 fails from a narrow implementation defect while the Line+Centerline auxiliary hypothesis remains intact, consider at most one explicit Repair Candidate in a later Autonomy Step. If it is scientifically negative, document the result and broaden to a different high-resolution line-continuity, preprocessing, data-policy, or calibration frontier rather than continuing local ASPP/detail/full-scale-skip variants. If it unexpectedly challenges the capped references and improves line-connectivity diagnostics, request separate whole-validation diagnostics before making any full-data or promotion claim.
