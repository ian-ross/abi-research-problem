# ABI-070 full-spectral BTD frequency-gated line U-Net centerline-guided focal-Tversky continuation

## Hypothesis

ABI-068 is the strongest local whole-validation-tested Candidate in the frequency-gated line U-Net branch by aggregate filtered Dice, but its recall-forward operating point increased negative-patch clutter and lost some of ABI-066's precision and Contrail Connectivity. ABI-069 tested a differentiable confidence-suppressor head on top of ABI-068, but the subtractive mechanism produced only a tiny predicted-positive-fraction reduction while reducing filtered Dice, recall, and especially connectivity.

This Candidate is a **family-development continuation** within the full-spectral BTD frequency-gated line U-Net family. The hypothesis is that a less suppressive centerline-guided additive residual in the mask head can preserve ABI-068's focal-Tversky recall/source-balanced Dice while recovering some continuity or precision. The residual is initialized at zero and bounded, so the direct ABI-068-style mask-logit path remains the primary path at initialization.

## Comparison Target

Primary target: ABI-068, `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, because it is the current strongest local whole-validation-tested Candidate by primary filtered Dice and the frequency-gated aggregate-Dice reference.

Secondary targets: ABI-066, `run_20260827_230540_bf4ce3`, because it remains the precision/connectivity-forward reference for this family; and ABI-069, `run_20260828_021352_6f4329`, because it showed that overly suppressive architecture-side clutter control can damage line continuity. Canonical MCAST 2.1 remains the promotion context, but this capped Run is family-development evidence rather than a promotion claim.

## Expected Effect

The centerline-guided head is expected to:

- keep ABI-068's focal-Tversky loss, source-balanced sampling, BTD front end, frequency-gated encoder/decoder, and centerline auxiliary weight unchanged;
- provide a small differentiable residual only where the model's supervised centerline branch finds line-like support;
- reduce the chance of ABI-069-style useful-line suppression because the residual is additive/bidirectional and bounded rather than a learned subtractive penalty;
- improve filtered Contrail Connectivity or filtered precision relative to ABI-068 without materially reducing filtered recall;
- remain source-balanced, with no Dataset Source-specific catastrophic regression.

## Implementation Sketch

The model uses provider-approved `abi_16ch` inputs only. The architecture is copied from ABI-068 through the frequency-pyramid fusion stage: normalized full-spectral ABI channels, thermal BTD planes derived only from approved ABI channels, learned 1x1 spectral mixing, high/low spatial-frequency split stem, low-frequency-gated skip fusion, multi-dilation coarse context, full-resolution frequency-pyramid fusion, and oriented high-frequency line refinement.

The controlled change is the final head. Instead of a plain 1x1 mask head, `CenterlineGuidedMaskHead` emits direct `mask_logits`, emits `centerline_logits` for the provider-derived auxiliary target, and adds a bounded residual `0.20 * tanh(residual_logits) * sigmoid(centerline_logits)`. The residual weights are initialized to zero so the model starts close to the ABI-068 head and can learn a modest centerline-supported correction during training. This is ordinary differentiable architecture: it does not threshold, postprocess, apply Artifact Filters, derive targets, inspect coordinates/source metadata, or implement losses/metrics.

## Contract Features Used

- Input mode: `abi_16ch` only; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target emitted as `centerline_logits` with trusted `weighted_bce` at weight 0.02.
- Primary loss: trusted `focal_tversky`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping under the current Workspace Configuration.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch, extra concurrency, GPU selection, data-policy change, or full-data promotion evaluation is requested by this Candidate handoff.

## Success Criteria

Strong continuation evidence would be any of:

- capped best `val/filtered_dice` matching ABI-068 within about 0.01 while improving filtered Contrail Connectivity or filtered precision;
- capped best `val/filtered_dice` exceeding ABI-068 while keeping filtered recall within about 0.02 of ABI-068;
- filtered recall at least 0.37, filtered precision at least 0.40, and both MIT and Google filtered Dice above 0.36;
- a finite, non-collapsed, late-improving trajectory that preserves ABI-068's source balance while improving the ABI-066/ABI-068 precision-recall-connectivity tradeoff.

Hard stop evidence for this exact branch would be smoke failure, non-finite behavior, prediction collapse, aggregate filtered Dice below 0.34 with no late improvement, a clear ABI-069-style connectivity regression, or a source-specific filtered-Dice collapse below 0.30.

## Fallback/Next Decision

If ABI-070 improves the ABI-068 tradeoff, request whole-validation failure-bucket diagnostics before any promotion interpretation. If it remains finite but only ties ABI-068 without secondary-metric improvement, keep ABI-068 as the local reference and broaden to a different precision/control mechanism. If it repeats ABI-069's connectivity loss, stop this head branch. If it fails contract validation or smoke testing, repair only if the centerline-guided residual hypothesis is preserved; otherwise classify the failure and choose a different in-contract family-development path.
