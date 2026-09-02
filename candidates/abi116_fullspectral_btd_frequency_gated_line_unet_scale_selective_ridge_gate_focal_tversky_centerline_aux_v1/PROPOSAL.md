# ABI-116 full-spectral BTD frequency-gated line U-Net scale-selective ridge-gate continuation

## Hypothesis

ABI-068 is the current strongest local whole-validation-tested Candidate by aggregate filtered Dice, but its full-validation diagnostic showed a recall-forward operating point with more negative-patch clutter and lower connectivity than ABI-066. Many broad post-decoder gates, auxiliary-head additions, traversal swaps, and generic recalibration variants failed to improve that tradeoff. A more targeted low-capacity architecture-side feature gate that explicitly selects among local residual scales and anisotropic line averages may recover precision, connectivity, or positive-area discipline without giving up ABI-068's source-balanced Dice.

This is a **family-development continuation** within the full-spectral BTD frequency-gated line U-Net family. It is capped representative evidence only, not a promotion claim.

## Comparison Target

Primary local target: ABI-068, `run_20260828_010836_4ccc77`, because it is the current strongest local whole-validation-tested frequency-gated line U-Net by aggregate filtered Dice and the branch this Candidate modifies.

Secondary local target: ABI-066, `run_20260827_230540_bf4ce3`, because it remains the precision/connectivity-forward reference with lower predicted-positive burden. ABI-099 and ABI-113 are negative context for earlier directional/coherence and patch-anomaly attempts that expanded positive area or damaged connectivity.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context; this Run requests only bounded representative family-development evidence.

## Expected Effect

The scale-selective ridge gate is expected to:

- keep ABI-068-like focal-Tversky recall and source-balanced MIT/Google Dice;
- improve filtered precision, filtered Contrail Connectivity, or filtered predicted-positive fraction relative to ABI-068 by requiring final features to agree with a thin-ridge residual scale;
- avoid ABI-099-like recall-only expansion because the gate mixes multi-scale local residuals with anisotropic line averages in feature space rather than adding a high-capacity post-logit suppressor;
- preserve resource feasibility by adding only a small pre-head module to the already profiled ABI-068 backbone.

## Implementation Sketch

The candidate uses provider-approved `abi_16ch` input only. The base architecture is ABI-068: normalized full-spectral channels, deterministic thermal BTD planes derived only from approved ABI channels, learned 1x1 spectral mixing, a frequency-split stem, U-Net encoder/decoder, multi-dilation bottleneck, and frequency-pyramid line refinement.

The controlled change is a new `ScaleSelectiveRidgeGate` after the final frequency-pyramid fusion. It computes residual detail at several average-pooling scales, learns a soft selection over those scales, forms horizontal and vertical anisotropic line averages, and fuses the original features, selected ridge detail, and a bounded ridge-consistency gate before the existing `mask_logits` and `centerline_logits` heads. It does not implement thresholding, postprocessing, Artifact Filters, metrics, losses, target derivation, sampling, augmentation, training loops, filesystem writes, network calls, pretrained weights, or coordinate-derived inputs.

## Contract Features Used

- Input mode: `abi_16ch`; no longitude, latitude, or reconstructed coordinate inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` emitted as `centerline_logits` with trusted `weighted_bce` weight 0.02.
- Primary loss: trusted `focal_tversky`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, disabled early stopping, and the current 25M-parameter smoke ceiling.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and no extra concurrency or GPU selection.

## Success Criteria

Useful continuation evidence would be any of:

- capped best `val/filtered_dice` within 0.01 of ABI-068 while improving filtered precision by at least 0.015, filtered connectivity by at least 0.03, or reducing filtered predicted-positive fraction below 0.0033;
- matching or exceeding ABI-066 filtered connectivity while keeping aggregate filtered Dice at least 0.37 and both MIT and Google filtered Dice at least 0.35;
- improving ABI-068 aggregate filtered Dice without worsening either Dataset Source filtered Dice below 0.38;
- a finite, non-collapsed, late-improving trajectory with diagnostically distinct precision/connectivity behavior that justifies whole-validation failure-bucket diagnostics.

Hard stop evidence for this exact branch would be smoke failure, non-finite behavior, prediction collapse, aggregate filtered Dice below 0.34 with no late improvement, Google or MIT filtered Dice below 0.32, or an ABI-099-like recall expansion with filtered predicted-positive fraction above 0.006 and connectivity below 0.20.

## Fallback/Next Decision

If ABI-116 recovers precision/connectivity or lower negative-patch burden while retaining ABI-068-like Dice, request bounded whole-validation failure-bucket diagnostics before any promotion interpretation. If it is finite but misses the secondary-metric criteria, retain ABI-068 as the aggregate-Dice reference and ABI-066 as the precision/connectivity reference, and broaden to a different architecture family or trusted policy axis. If it fails validation or smoke testing, classify the failure and repair only if the scale-selective ridge-gate hypothesis and comparison target are preserved.
