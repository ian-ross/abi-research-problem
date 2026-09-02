# ABI-143 Full-Spectral BTD+SZA Soft Ridge-Gate U-Net BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-142 was a finite, resource-feasible, non-collapsed ridge-attention family scout whose capped filtered Dice landed within 0.003 of both ABI-068 and ABI-130, but it did not establish a distinctive connectivity or source-balance advantage. ABI-143 spends one bounded continuation on the specific mechanism suggested by ABI-142's note: preserve the SZA+BCE-Dice setup and ridge-aware architecture, but reduce final ridge-gate aggressiveness rather than adding another auxiliary target or candidate-owned postprocessing.

## Hypothesis

ABI-142's encoder-level ridge features were useful enough to reach the current capped reference band, but its final multiplicative ridge gate could suppress or amplify decoded features too strongly for the fixed 0.5 threshold, especially on MIT patches where recall remained weaker. A neutral-initialized conservative ridge gate bounded near identity should keep the same approved-channel ridge/detail evidence while improving calibration stability, MIT recall/Dice, or connectivity without increasing false-positive clutter. Because the gate operates only on learned features before the mask head, it is architecture code rather than thresholding, Artifact Filtering, or postprocessing.

## Comparison Target

Primary comparison targets are ABI-142 `run_20260831_215104_d4c318`, the ridge-attention family scout being continued; ABI-130 `run_20260831_121006_7d24be`, the strongest SZA-aware ASPP/detail BCE-Dice branch; and ABI-068 `run_20260828_010836_4ccc77`, the local capped aggregate/source-balance reference. Secondary references are ABI-126 `run_20260831_085615_d05ab3` and ABI-066 `run_20260827_230540_bf4ce3` for high-precision/connectivity behavior. Canonical MCAST 2.1 remains the full Working Validation Split promotion context, not a promotion claim for this representative capped continuation.

## Expected Effect

A useful result would train finitely and preserve ABI-142's near-reference aggregate Dice while moving the ridge family toward a clearer advantage: higher MIT filtered Dice/recall, stronger filtered connectivity, or a better precision/recall balance at a similar predicted-positive fraction. The exact branch should be considered positive if it ties ABI-142 within about 0.005 aggregate filtered Dice while improving either MIT filtered Dice/recall or filtered connectivity, or if it approaches ABI-068/ABI-130 with a more stable source profile. It need not beat the mature ABI-068 incumbent to be informative, but it should outperform obvious negative head-level tweaks such as ABI-141 or show a distinct trade-off.

## Implementation Sketch

- Use provider-approved `abi_16ch_plus_sza` input only; exclude longitude, latitude, reconstructed coordinates, and Dataset Source identity.
- Normalize ABI channels 1-16 using fixed campaign-profile ranges; derive eight deterministic thermal BTD planes from approved ABI thermal channels; add normalized SZA, `cos(SZA)`, and a learned 1x1 approved-channel mixture.
- Keep ABI-142's compact three-level U-Net with GroupNorm/GELU residual blocks, early `RidgeAttentionStem`, dilated bottleneck context, decoder skip fusion, and high-resolution ridge feature path.
- Change only the final `MultiScaleRidgeRefinement` calibration: replace the broader learned multiplicative range with a neutral-initialized sigmoid gate whose final 1x1 weights/bias start at zero and whose multiplier is bounded to `0.85 + 0.3 * gate`, i.e. 0.85-1.15 and exactly 1.0 at initialization.
- Emit primary `mask_logits` and provider-derived `centerline_logits` only.
- Preserve trusted `bce_dice` primary loss, Centerline Target weighted-BCE auxiliary weight 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.
- Request one sequential Run only; no Experiment Batch or candidate-owned resource scheduling is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, primary and auxiliary losses, metrics, checkpointing, Artifact Filters, thresholding, postprocessing, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data evidence, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains below the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As ridge-family continuation evidence, the branch should tie ABI-142 within about 0.005 aggregate filtered Dice while improving MIT filtered Dice/recall, filtered connectivity, or precision/recall balance; alternatively, it should approach ABI-068/ABI-130 with a clearer source-profile or positive-area advantage.

## Continuation and hard stop

This is the planned bounded follow-up to ABI-142, not an open-ended ridge-attention sweep. Stop this exact soft-gate branch for hard execution failure, persistent non-finite behavior, persistent all-negative or all-positive prediction collapse, clear optimization failure, severe Dataset Source-specific collapse, or resource failure outside the trusted envelope. If it is finite but worse than ABI-142 without a source/connectivity/calibration advantage, document the negative result and broaden away from ridge-gate tuning. If it improves the ridge family or produces a distinctive trade-off, a later Autonomy Step may request whole-validation diagnostics or propose a different in-contract frontier; do not claim promotion from capped evidence.

## Fallback/Next Decision

If this candidate fails because of a narrow implementation defect while the soft-gate hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but underperforms ABI-142 without the planned source/connectivity/calibration signal, write a Research Note and broaden to a different architecture family, input/front-end, loss, augmentation, data-policy, or evaluation frontier. If it unexpectedly improves capped aggregate/source/connectivity behavior versus ABI-142 and remains competitive with ABI-068/ABI-130, request separately authorized whole-validation diagnostics rather than claiming promotion from capped data.
