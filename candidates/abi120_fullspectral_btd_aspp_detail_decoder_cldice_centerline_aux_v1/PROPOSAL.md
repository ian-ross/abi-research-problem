# ABI-120 Full-Spectral BTD ASPP/Detail Decoder clDice Centerline Auxiliary v1

## Proposal classification

**Family scout.** This is an early probe of a materially different full-spectral BTD segmentation geometry after recent ABI-116/117/119 high-resolution ridge/detail and context-pyramid branches failed to improve the ABI-068 frequency-gated reference. It is not a promotion claim or full-data request.

## Hypothesis

ABI-052 showed that full-spectral BTD features with trusted `bce_dice_cldice` and a low-weight trusted Centerline Target auxiliary head can produce a stable precision/connectivity trade-off in a DeepLabV3+ family, but the branch remained weak on MIT filtered Dice and recall. ABI-068 later became the capped aggregate-Dice reference, while recent post-decoder ridge/detail and FPN context-pyramid variants around that U-Net backbone tended to add positive area or lose connectivity.

A compact ASPP/detail encoder-decoder may provide a different in-contract balance: ASPP and image-level context at the coarsest scale should supply broad cloud/background calibration, while full-resolution raw/detail/context fusion should preserve thin-line evidence that DeepLabV3+ downsampling may miss. Keeping the ABI-052 BTD front end and trusted `bce_dice_cldice` + centerline-auxiliary policy tests whether architecture geometry, rather than another auxiliary-head or post-decoder gate variant, can improve source-balanced thin-contrail segmentation.

## Comparison Target

The primary family comparison target is ABI-052 `abi052_fullspectral_deeplabv3plus_btd_cldice_centerline_aux_w002_v1`, Run `run_20260827_131644_b76d09`: BTD-mixer DeepLabV3+ with `bce_dice_cldice` and Centerline Target auxiliary weight 0.02, best filtered Dice 0.2214, MIT/Google filtered Dice 0.2083/0.2542, filtered precision 0.2619, recall 0.1918, connectivity 0.3391, and predicted-positive fraction 0.00265.

Secondary capped references are ABI-048 `run_20260827_112338_82a3a6` (BTD DeepLabV3+ clDice without auxiliary target), ABI-049 `run_20260827_114945_e5f83e` (high-recall Line Target auxiliary branch), ABI-066 `run_20260827_230540_bf4ce3` (frequency-gated line U-Net precision/connectivity reference), and ABI-068 `run_20260828_010836_4ccc77` (current local aggregate-Dice reference). Canonical MCAST 2.1 remains full Working Validation Split promotion context, not a strict gate for this capped family scout.

## Expected Effect

If the ASPP/detail geometry is useful, it should improve or credibly tie ABI-052 on aggregate filtered Dice while improving at least one of MIT filtered Dice, filtered recall, source balance, connectivity, or predicted-positive stability. It is not expected to beat the mature ABI-068 branch on a first scout. A useful negative result would show that the DeepLab/ASPP-style context axis is not enough to close the MIT/recall gap under trusted `bce_dice_cldice`, and would redirect future work away from this exact custom ASPP/detail formulation.

## Implementation Sketch

- Reuse the ABI-052 front-end pattern: normalize provider-approved GOES ABI channels 1-16, append eight deterministic thermal BTD planes derived only from those channels, and append a learned 16-channel 1x1 GELU projection of normalized ABI channels.
- Replace the SMP DeepLabV3+ decoder with a torch-only residual encoder-decoder: full-resolution detail/context stem, three downsampling residual stages, an ASPP bottleneck with dilation rates 2/4/8 and image-level pooled context, three bilinear decoder fusions, a second high-resolution detail/context path, and a learned line-aware refinement block.
- Emit primary `mask_logits` and trusted auxiliary `centerline_logits` from the same refined feature map.
- Preserve trusted `bce_dice_cldice` as the primary loss and manifest-declared provider-owned Centerline Target auxiliary supervision with trusted `weighted_bce` weight 0.02.
- Preserve provider-owned `combined_source_balanced` traversal, `random_mirroring` augmentation, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.
- Request one sequential Run only; no Experiment Batch or candidate-owned scheduling/resource placement is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice_cldice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, artifact filtering, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data evidence, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-scout evidence, the result is useful if it improves or credibly ties ABI-052, improves MIT filtered Dice or recall without severe precision/connectivity loss, narrows source imbalance, preserves positive-area discipline, shows a finite improving trajectory, or clearly rules out this ASPP/detail geometry under the current trusted policy.

## Continuation and hard stop

Continue this ASPP/detail family only if the scout is finite, non-degenerate, source-informative, and improves a meaningful family diagnostic such as filtered Dice, MIT behavior, recall/precision balance, source balance, connectivity, predicted-positive stability, or late-epoch trajectory. Stop or repair the exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. Low capped Dice alone is not promotion evidence and not family-wide elimination proof, but a clear miss on all listed diagnostics would be enough to stop this exact custom ASPP/detail formulation.

## Fallback/Next Decision

If this candidate fails due to a narrow implementation defect while the hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but does not improve ABI-052 or offer a useful MIT/recall/connectivity trade-off, document the scout and broaden to a different contract-compliant frontier such as source-robust calibration architecture, trusted data-policy comparison, loss/auxiliary policy comparison, or another materially different architecture family rather than repeating post-decoder ridge/detail gates. If it unexpectedly challenges ABI-068, request separately authorized focused full-data evidence rather than claiming promotion from capped data.
