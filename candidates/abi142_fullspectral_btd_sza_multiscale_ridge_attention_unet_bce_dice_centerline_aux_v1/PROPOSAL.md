# ABI-142 Full-Spectral BTD+SZA Multiscale Ridge-Attention U-Net BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family scout.** Recent SZA-aware ASPP/detail decoder work found a strong capped branch in ABI-130, but subsequent auxiliary and mask-head tweaks (ABI-133, ABI-136, ABI-141) did not improve aggregate Dice, source balance, or connectivity. ABI-142 broadens away from incremental ASPP/detail head modifications to a compact multiscale ridge-attention U-Net that moves line-sensitive evidence into the encoder stem and final feature refinement while retaining the successful SZA+BCE-Dice calibration axis.

## Hypothesis

A U-Net whose earliest features explicitly include multiscale fine-detail, broad-context, horizontal-ridge, and vertical-ridge residual views from approved ABI+BTD+SZA channels can learn more stable thin-contrail evidence than adding auxiliary heads to an already fixed ASPP/detail decoder. The ridge views are differentiable feature inputs to the architecture, not candidate-owned Artifact Filters or postprocessing. Pairing them with trusted BCE-Dice and low-weight Centerline Target supervision should preserve default-threshold calibration while testing whether ridge-aware features recover connectivity or source-robust MIT/Google behavior.

## Comparison Target

Primary comparison targets: ABI-130 `run_20260831_121006_7d24be` as the strongest SZA-aware ASPP/detail BCE-Dice branch, and ABI-068 `run_20260828_010836_4ccc77` as the local capped aggregate/source-balance reference. Secondary references are ABI-126 `run_20260831_085615_d05ab3` and ABI-066 `run_20260827_230540_bf4ce3` for high-precision/connectivity behavior, plus ABI-141 `run_20260831_210158_e9ce5e` as evidence that boundary/detail head-level calibration was insufficient. Canonical MCAST 2.1 remains the full Working Validation Split promotion context, not a promotion claim for this capped scout.

## Expected Effect

A useful scout would train finitely and show whether early ridge-aware feature construction changes the precision/recall/connectivity tradeoff relative to the mature capped references. Because this is a new family scout, immediate promotion-level superiority is not required. Useful evidence includes aggregate filtered Dice within about 0.03-0.04 of ABI-130/ABI-068 with stronger connectivity or predicted-positive discipline, a source-specific improvement such as better MIT Dice/recall without Google collapse, or a clearly different non-degenerate trajectory that identifies ridge-feature calibration as worth one bounded follow-up.

## Implementation Sketch

- Use provider-approved `abi_16ch_plus_sza` input only; exclude longitude, latitude, reconstructed coordinates, and Dataset Source identity.
- Normalize ABI channels 1-16 using fixed campaign-profile ranges; derive eight deterministic thermal BTD planes from approved ABI thermal channels; add normalized SZA, `cos(SZA)`, and a learned 1x1 approved-channel mixture.
- Replace the ASPP/detail stem with `RidgeAttentionStem`, which projects raw features, local high-pass detail, broad cloud context, horizontal strip residuals, and vertical strip residuals before residual fusion.
- Use a compact three-level U-Net encoder/decoder with GroupNorm and GELU for batch-size-4 stability.
- Add `MultiScaleRidgeRefinement` after decoding. It computes local detail plus learned horizontal/vertical strip context and applies a feature-space sigmoid gate bounded around neutral scaling before final residual fusion.
- Emit primary `mask_logits` and provider-derived `centerline_logits` only.
- Preserve trusted `bce_dice` primary loss, Centerline Target weighted-BCE auxiliary weight 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.
- Request one sequential Run only; no Experiment Batch or candidate-owned resource scheduling is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, primary and auxiliary losses, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data evidence, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains below the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As scout evidence, continue only if ABI-142 is finite, source-informative, and shows a meaningful difference from recent ASPP/detail tweaks: near-reference aggregate filtered Dice, improved filtered connectivity, improved MIT or Google source behavior, better precision/recall balance, or a late improving trajectory that justifies one bounded family-development follow-up.

## Continuation and hard stop

Allow at most one or two later family-development follow-ups if ABI-142 is finite, non-degenerate, resource-feasible, and either approaches ABI-130/ABI-068 within about 0.03-0.04 aggregate filtered Dice or shows a distinctive connectivity/source-balance/positive-area advantage. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent all-negative or all-positive prediction collapse, clear optimization failure, severe Dataset Source-specific collapse, or resource failure outside the trusted envelope. A finite result materially below ABI-130/ABI-068 without a diagnostic strength would stop this exact ridge-attention scout, but would not eliminate all deterministic-feature or SZA-aware architecture work.

## Fallback/Next Decision

If this candidate fails because of a narrow implementation defect while the ridge-attention hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but underperforms without connectivity or source-balance gains, document that result and broaden to a different in-contract architecture, input/front-end, loss, augmentation, data-policy, or evaluation frontier. If it unexpectedly improves capped aggregate/source/connectivity behavior versus ABI-130 or ABI-068, request separately authorized whole-validation diagnostics rather than claiming promotion from capped data.
