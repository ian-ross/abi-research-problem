# ABI-121 Full-Spectral BTD ASPP/Detail Decoder Focal-Tversky Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-120 established finite, resource-feasible, non-collapsed, positive capped scout evidence for the compact ASPP/detail decoder geometry under trusted `bce_dice_cldice` plus low-weight Centerline Target auxiliary supervision. ABI-121 keeps that architecture fixed and changes only the trusted primary loss to `focal_tversky` to test whether recall and source Dice can improve without abandoning the ASPP/detail family.

## Hypothesis

ABI-120 improved the weak DeepLabV3+ BTD clDice centerline-auxiliary comparison target by a large margin and produced a disciplined precision-forward operating point, but it remained behind ABI-068 on aggregate filtered Dice, MIT filtered Dice, recall, and connectivity. In the frequency-gated line U-Net branch, changing `bce_dice_cldice` to trusted `focal_tversky` improved aggregate Dice and recall while retaining source balance. The same loss-policy swap may be useful for the ASPP/detail decoder: broad ASPP context and high-resolution detail fusion should preserve precision/positive-area discipline, while focal-Tversky should reduce the conservative recall bottleneck observed in ABI-120.

## Comparison Target

The primary family comparison target is ABI-120 `abi120_fullspectral_btd_aspp_detail_decoder_cldice_centerline_aux_v1`, Run `run_20260831_033037_bad0bb`: compact ASPP/detail decoder with `bce_dice_cldice` and Centerline Target auxiliary weight 0.02. ABI-120 selected epoch 10 with filtered Dice 0.3667, MIT/Google filtered Dice 0.3485/0.4078, filtered precision 0.4366, filtered recall 0.3161, filtered connectivity 0.3681, and filtered predicted-positive fraction 0.00262.

Secondary capped references are ABI-068 `run_20260828_010836_4ccc77` (frequency-gated line U-Net focal-Tversky aggregate-Dice reference: filtered Dice 0.3964, precision 0.3992, recall 0.3936, connectivity 0.3900), ABI-066 `run_20260827_230540_bf4ce3` (frequency-gated line U-Net clDice precision/connectivity reference), and ABI-052 `run_20260827_131644_b76d09` (DeepLabV3+ BTD clDice centerline-auxiliary target that ABI-120 exceeded). Canonical MCAST 2.1 remains full Working Validation Split promotion context, not a strict gate for this capped continuation.

## Expected Effect

If focal-Tversky is a useful ASPP/detail continuation, ABI-121 should improve ABI-120 recall and aggregate/source filtered Dice while keeping precision, connectivity, and filtered predicted-positive fraction within a useful range. A useful result need not immediately beat ABI-068; it can justify further ASPP/detail development if it narrows the ABI-120-to-ABI-068 recall/Dice gap without collapsing into the low-precision/high-area regime seen in several suppressor/gate variants. A negative result would show that ABI-120's conservative precision-forward behavior was tied to clDice loss and that the ASPP/detail geometry does not tolerate the focal-Tversky recall push under the current capped policy.

## Implementation Sketch

- Reuse ABI-120 architecture unchanged: normalized provider-approved GOES ABI channels 1-16, eight deterministic thermal BTD planes derived only from those channels, learned 16-channel 1x1 projection, full-resolution detail/context stem, residual encoder, ASPP bottleneck with dilation rates 2/4/8 plus image-level context, bilinear decoder fusions, second high-resolution detail path, and line-aware refinement.
- Emit primary `mask_logits` and trusted auxiliary `centerline_logits` from the same refined feature map.
- Change only the manifest-selected trusted primary loss from `bce_dice_cldice` to `focal_tversky`.
- Preserve provider-owned `combined_source_balanced` traversal, trusted `random_mirroring`, provider-derived Centerline Target auxiliary supervision with trusted `weighted_bce` weight 0.02, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.
- Request one sequential Run only; no Experiment Batch or candidate-owned scheduling/resource placement is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `focal_tversky`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data evidence, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it improves ABI-120 filtered Dice or recall, preserves ABI-120 precision/connectivity within a bounded tradeoff, narrows the ABI-120-to-ABI-068 gap, shows a finite improving trajectory, or exposes a clear loss-specific failure mode for the ASPP/detail family.

## Continuation and hard stop

Continue the ASPP/detail family only if ABI-121 is finite, non-degenerate, source-informative, and improves a meaningful family diagnostic relative to ABI-120, such as filtered Dice, MIT behavior, recall/precision balance, source balance, connectivity, predicted-positive stability, or late-epoch trajectory. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. Low capped Dice alone is not promotion evidence and not family-wide elimination proof, but a clear miss on all ABI-120-relative diagnostics would be enough to stop this exact focal-Tversky ASPP/detail continuation.

## Fallback/Next Decision

If this candidate fails due to a narrow implementation defect while the ABI-120-preserving hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but loses ABI-120 precision/connectivity without a compensating recall or Dice gain, document the continuation and broaden to a different contract-compliant frontier rather than repeating the same loss swap. If it unexpectedly challenges ABI-068, request separately authorized focused full-data evidence rather than claiming promotion from capped data.
