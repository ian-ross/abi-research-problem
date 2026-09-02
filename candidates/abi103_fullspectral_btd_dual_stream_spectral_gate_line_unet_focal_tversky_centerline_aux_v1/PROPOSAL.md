# ABI-103 full-spectral BTD dual-stream spectral-gate line U-Net scout

## Hypothesis

Recent capped work shows that ABI-068 remains the strongest aggregate-Dice frequency-gated line U-Net reference, while ABI-066 remains the precision/connectivity reference. Several local continuations that changed sampling, learning rate, output bias, auxiliary structure, or small gating mechanisms failed to improve the tradeoff, and recent ConvNeXt/large-kernel stability repairs showed that deterministic raw+BTD features alone are not sufficient.

ABI-103 is a **family scout** for a dual-stream spectral-gate line U-Net. Instead of immediately mixing all approved ABI channels plus BTD planes into one feature tensor, it lets reflective channels, thermal channels, and thermal BTD planes specialize in separate stems, then learns bounded cross-stream gates before U-Net encoding and line-aware multi-scale fusion. The hypothesis is that separating visible/near-IR cloud texture from thermal ice-cloud evidence before fusion can improve source-robust threshold discipline and thin-line continuity without candidate-owned thresholding, postprocessing, or Artifact Filters.

## Comparison Target

Primary local target: ABI-068, `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, because it is the current capped aggregate-Dice reference and a whole-validation-tested frequency-gated branch.

Secondary local target: ABI-066, `run_20260827_230540_bf4ce3`, because it retains the strongest precision/connectivity profile in the same full-spectral BTD line-sensitive search area. ABI-085, ABI-097, ABI-100, and ABI-102 are negative context for small learning-rate, bias, deterministic-shuffle, and modern-block repairs. Canonical MCAST 2.1 remains the full Working Validation Split promotion context; this scout requests only capped representative evidence.

## Expected Effect

The dual-stream spectral-gate design is expected to:

- reduce false-positive clutter by requiring agreement between thermal/BTD ice-cloud evidence and reflective cloud texture when both are informative;
- preserve ABI-068-like recall through focal-Tversky and full-resolution line-aware fusion;
- improve source balance by avoiding a single early learned mixer that can overfit one Dataset Source's spectral statistics;
- remain diagnostically distinct from ABI-068/066 by testing spectral specialization rather than another small decoder gate, sampling, or initialization change;
- complete within the existing frequency-gated U-Net resource envelope using a compact base width and no pretrained weights.

## Implementation Sketch

The candidate uses provider-approved `abi_16ch` input only. Candidate code normalizes the 16 approved ABI channels using bounded constants from the dataset profile and constructs deterministic thermal BTD planes from approved ABI channels only. A reflective stem consumes ABI channels 1-6, a thermal stem consumes ABI channels 7-16, and a BTD stem consumes selected thermal differences. Cross-stream sigmoid gates modulate reflective and thermal features before fusion. The fused tensor enters a compact residual U-Net with low-frequency-gated skip fusion, a dilated bottleneck, and a line-consensus refinement block that combines horizontal, vertical, local-detail, and broad-context features at full resolution. It emits primary `mask_logits` and provider-derived `centerline_logits`.

The manifest uses trusted `focal_tversky`, trusted `random_mirroring`, provider-owned `combined_source_balanced` traversal, AdamW learning rate 0.0003, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and a trusted provider-derived `centerline` auxiliary target with `weighted_bce` weight 0.02. No candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, threshold selection, Artifact Filters, postprocessing, filesystem writes, network calls, pretrained weights, or training loop logic are introduced. The model does not receive longitude, latitude, or reconstructed coordinate inputs.

## Contract Features Used

- Input mode: `abi_16ch` only; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target emitted as `centerline_logits` with trusted `weighted_bce` at weight 0.02.
- Primary loss: trusted `focal_tversky`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping under the current Workspace Configuration.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch, extra concurrency, GPU selection, data-policy change, or full-data promotion evaluation is requested.

## Success Criteria

Strong scout evidence would be any of:

- capped best `val/filtered_dice` within 0.015 of ABI-068 while improving filtered precision, connectivity, or predicted-positive discipline;
- capped best `val/filtered_dice` matching or exceeding ABI-066 with better MIT/Google balance than ABI-066;
- both MIT and Google filtered Dice above 0.35 with non-collapsed predictions and a late-improving trajectory;
- a distinctive secondary-metric strength, such as ABI-066-like connectivity with ABI-068-like recall, that justifies bounded family development.

Hard stop evidence for this exact scout would be smoke failure, non-finite behavior, persistent all-negative/all-positive prediction collapse, aggregate filtered Dice below 0.30 with no late improvement, either Dataset Source below 0.25 filtered Dice, or a low-precision/high-positive-area regime resembling the negative ConvNeXt repair without any compensating recall/connectivity strength.

## Fallback/Next Decision

If ABI-103 approaches ABI-068 while improving precision/connectivity/source balance, request bounded whole-validation diagnostics or a tightly controlled family continuation. If it is finite but mixed, compare its stream-specific failure mode to ABI-066/068 before deciding whether a second dual-stream follow-up is justified. If it fails contract validation or smoke testing, classify the failure and repair only if the original spectral-specialization hypothesis is preserved. If it is clearly negative by the hard-stop criteria, broaden to another in-contract architecture or trusted policy axis rather than moving provider-owned thresholding, Artifact Filters, data loading, sampling, augmentation, target derivation, losses, metrics, resource placement, or lifecycle behavior into Candidate code.
