# ABI-144 Full-Spectral BTD+SZA Additive Ridge-Residual U-Net BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-143 showed that softening ABI-142's ridge gate improved aggregate filtered Dice and MIT recall, but it lost substantial connectivity and Google precision. ABI-144 spends one bounded continuation on the mechanism-specific question left by that note: can ridge-aware SZA+BCE-Dice modeling keep the MIT recall benefit without a multiplicative feature gate that suppresses or amplifies decoded features?

## Hypothesis

A multiplicative ridge gate can improve calibration but may also attenuate line structure, explaining ABI-143's lower filtered connectivity versus ABI-142 and ABI-130. Replacing the multiplicative gate with a neutral-initialized additive ridge residual should preserve the decoded feature identity at initialization, add only bounded learned ridge/detail corrections, and avoid direct feature suppression. This should improve or preserve filtered connectivity and precision relative to ABI-143 while retaining more MIT recall than ABI-142.

## Comparison Target

Primary targets are ABI-143 `run_20260831_224534_27b73d`, the immediate soft ridge-gate predecessor; ABI-142 `run_20260831_215104_d4c318`, the ridge-attention SZA+BCE-Dice scout; ABI-130 `run_20260831_121006_7d24be`, the strongest SZA-aware ASPP/detail BCE-Dice reference; and ABI-068 `run_20260828_010836_4ccc77`, the local capped aggregate/source-balance reference. Canonical MCAST 2.1 remains full Working Validation Split promotion context, not a promotion claim for this representative capped continuation.

## Expected Effect

A useful result should train finitely, avoid prediction collapse, and land in the same capped reference band as ABI-142/ABI-143. The branch is positive if it ties ABI-143 within about 0.005 aggregate filtered Dice while improving filtered connectivity or precision, or if it ties ABI-142 while improving MIT filtered Dice/recall. It need not beat ABI-068 immediately, but it should clarify whether additive ridge refinement is preferable to multiplicative ridge gating.

## Implementation Sketch

- Use provider-approved `abi_16ch_plus_sza` input only; exclude longitude, latitude, reconstructed coordinates, and Dataset Source identity.
- Normalize ABI channels 1-16 using fixed campaign-profile ranges; derive eight deterministic BTD planes from approved ABI channels; add normalized SZA, `cos(SZA)`, and a learned 1x1 approved-channel mixture.
- Keep the compact ridge-attention U-Net structure from ABI-143: early `RidgeAttentionStem`, three downsampling encoder stages, dilated bottleneck context, decoder skip fusion, high-resolution ridge path, GroupNorm/GELU residual blocks, and Centerline Target auxiliary output.
- Change only the final ridge calibration mechanism: replace the neutral multiplicative `0.85 + 0.3 * sigmoid(...)` feature gate with a neutral additive residual `0.1 * tanh(...)`; initialize the final residual projection weights and bias to zero so the path starts as identity.
- Emit only primary `mask_logits` and provider-declared `centerline_logits`.
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
6. As ridge-family continuation evidence, the branch should tie ABI-143 within about 0.005 aggregate filtered Dice while improving filtered connectivity/precision, or tie ABI-142 while improving MIT filtered Dice/recall.

## Continuation and hard stop

Stop this exact additive-residual branch for hard execution failure, persistent non-finite behavior, persistent all-negative or all-positive prediction collapse, clear optimization failure, severe Dataset Source-specific collapse, or resource failure outside the trusted envelope. If it is finite but worse than ABI-142 and ABI-143 without the planned source/connectivity/calibration signal, document the negative result and broaden away from ridge-gate/refinement tuning. If it improves the ridge family or produces a distinctive trade-off, a later Autonomy Step may request whole-validation diagnostics or propose a different in-contract frontier; do not claim promotion from capped evidence.

## Fallback/Next Decision

If this candidate fails because of a narrow implementation defect while the additive ridge-residual hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but underperforms ABI-142/ABI-143 without the planned signal, write a Research Note and broaden to a different architecture family, input/front-end, loss, augmentation, data-policy, or evaluation frontier. If it unexpectedly improves capped aggregate/source/connectivity behavior versus ABI-142/ABI-143 and remains competitive with ABI-068/ABI-130, request separately authorized whole-validation diagnostics rather than claiming promotion from capped data.
