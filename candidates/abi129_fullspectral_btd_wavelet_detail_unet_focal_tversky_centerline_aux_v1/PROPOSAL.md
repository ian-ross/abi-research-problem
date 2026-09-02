# ABI-129 Full-Spectral BTD Wavelet-Detail U-Net Focal-Tversky Centerline Auxiliary v1

## Proposal classification

**Family scout.** ABI-120 through ABI-128 mapped the compact ASPP/detail decoder's loss, auxiliary, and mask-head tuning behavior. ABI-128 weakened the case for another simple ASPP/detail BCE-Dice head or auxiliary tweak. ABI-129 therefore broadens to a different contract-compliant thin-line architecture: a wavelet-detail U-Net that preserves multiscale high-frequency evidence while using low-frequency context to gate decoder skips.

## Hypothesis

Fixed multiscale detail summaries in the encoder can preserve thin contrail evidence that ordinary pooling discards, while context-gated decoder skips can avoid the recall-heavy clutter seen in several high-resolution or patch-anomaly variants. Under trusted focal-Tversky loss and low-weight Centerline Target auxiliary supervision, this should recover ABI-068-like MIT recall/source balance without sacrificing as much precision/connectivity as the permissive HRNet, nested-skip, or patch-anomaly scouts.

## Comparison Target

Primary comparison target: ABI-068 `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, the current local capped aggregate-Dice reference with filtered Dice 0.3964, MIT/Google filtered Dice 0.3886/0.4161, precision 0.3992, recall 0.3936, connectivity 0.3900, and filtered predicted-positive fraction 0.00357.

Secondary references are ABI-066 `run_20260827_230540_bf4ce3` for precision/connectivity, ABI-126 `run_20260831_085615_d05ab3` for ASPP/detail BCE-Dice precision/connectivity and Google-Dice behavior, ABI-121 `run_20260831_041559_43da35` for ASPP/detail recall/source balance, and negative high-resolution/detail scouts ABI-079, ABI-084, and ABI-113. Canonical MCAST 2.1 remains full Working Validation Split promotion context; this proposal requests capped representative evidence only.

## Expected Effect

A useful scout need not beat ABI-068 immediately. It should be finite and non-collapsed, keep both Dataset Sources informative, and show whether wavelet-style detail preservation can improve the precision/recall/connectivity trade-off relative to earlier detail-heavy scouts. The desired operating point is aggregate filtered Dice within roughly 0.02 of ABI-068 or a clear secondary strength such as MIT filtered Dice near ABI-068, connectivity above 0.40, precision above 0.40, or a cleaner positive-area fraction than other recall-forward scouts.

## Implementation Sketch

- Normalize provider-approved GOES ABI channels 1-16 using fixed profile-scale constants and concatenate eight deterministic thermal BTD planes derived only from those approved channels plus a learned 1x1 projection.
- Use a compact U-Net with fixed wavelet-detail downsampling blocks. Each downsampling stage forms a low-frequency average-pooled stream and a high-frequency residual-magnitude stream before learned fusion.
- Decode with bilinear upsampling and context-gated skip fusion so high-resolution detail is available but moderated by smooth cloud context.
- Use a multiscale wavelet/detail line head with horizontal and vertical asymmetric convolutions, local detail, and broad smoothed context before producing `mask_logits` and `centerline_logits`.
- Preserve trusted `focal_tversky` primary loss, provider-derived Centerline Target auxiliary supervision (`weighted_bce`, weight 0.02), `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted representative cap.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, reconstructed coordinates, and Solar Geometry Input are excluded.
- Outputs: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `focal_tversky`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, and constant learning-rate scheduler.
- Provider/Harness owns data loading, Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, thresholding, Artifact Filters, resource limits, execution lifecycle, and prediction retention.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler, disabled early stopping, and the 3,600-second trusted training timeout. No Experiment Batch, Post-Run Evaluation, full-data run, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic execution failure.
6. As family-scout evidence, continue only if the result is source-informative and either approaches ABI-068 aggregate/MIT Dice, improves a secondary precision/connectivity/positive-area diagnostic over recent detail-heavy scouts, or shows a clearly improving trajectory worth one bounded follow-up.

## Continuation and hard stop

Continue the wavelet-detail family only if ABI-129 is finite, non-degenerate, resource-feasible, and shows either competitive source-balanced Dice or a distinct secondary-metric advantage over previous high-resolution/detail scouts. Stop this exact branch for hard execution failure, non-finite behavior, persistent prediction collapse, severe source-specific collapse, clear optimization failure, resource failure, or a low-precision high-positive-area result resembling ABI-079/084/113 without compensating connectivity or source-balance evidence.

## Fallback/Next Decision

If ABI-129 fails due to a narrow implementation defect while the wavelet-detail hypothesis remains intact, prepare at most one repair in a later Autonomy Step. If it completes finite but repeats the recall-heavy clutter pattern, document the result and broaden again rather than stacking more local gates. If it unexpectedly challenges ABI-068 or combines ABI-068-like Dice with ABI-066-like connectivity, request separate focused diagnostics rather than claiming promotion from capped evidence.
