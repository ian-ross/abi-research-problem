# ABI-060 Full-Spectral BTD High-Resolution Line U-Net + Confidence-Gated Refiner + clDice + Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** This is a controlled follow-up within the full-spectral BTD high-resolution line U-Net family after ABI-058 whole-validation diagnostics and the negative ABI-059 false-positive-suppressor result. It is not a promotion claim, not a full-data training request, and not an Experiment Batch candidate.

## Hypothesis

ABI-058 is the current local whole-validation-tested reference in this branch: whole-validation filtered Dice 0.3233, with recall-oriented gains but broad low-level false positives on negative patches. ABI-059 tested subtractive learned suppression, but its capped best filtered Dice fell to 0.3135, precision and predicted-positive fraction did not improve, and filtered connectivity dropped sharply.

ABI-060 tests a materially different false-positive-control mechanism that remains model architecture only. Instead of subtracting a learned suppression term from logits, it uses confidence-gated feature selection: low-resolution context and oriented line features produce soft gates that decide how strongly full-resolution features enter the final mask refinement. The gate bias is initialized mildly open so the model starts near the ABI-058/ABI-059 oriented-context branch while allowing the trusted loss to learn feature selection that rejects diffuse background activations.

## Comparison Target

Primary family comparison targets are:

- ABI-058 `abi058_fullspectral_btd_hrline_unet_oriented_context_cldice_centerline_aux_v1`, Run `run_20260827_171331_c1769a`: capped best filtered Dice 0.3248 and whole-validation filtered Dice 0.3233, with higher recall but broad false positives.
- ABI-056 `abi056_fullspectral_btd_hrline_unet_multiscale_skip_fusion_cldice_centerline_aux_v1`, Run `run_20260827_153716_1ac9d4`: capped best filtered Dice 0.3225 and whole-validation filtered Dice 0.3198, with better precision and fewer false-positive pixels than ABI-058.
- ABI-059 `abi059_fullspectral_btd_hrline_unet_false_positive_suppressor_cldice_centerline_aux_v1`, Run `run_20260827_181006_6a9a1f`: negative capped evidence for subtractive suppression, best filtered Dice 0.3135 and weak connectivity.
- Canonical MCAST 2.1 remains full Working Validation Split promotion context at filtered Dice 0.3873; ABI-060 is representative capped family-development evidence only.

## Expected Effect

If ABI-058's remaining gap is driven by diffuse background activation rather than lack of context alone, confidence-gated feature selection should lower filtered predicted-positive fraction or improve precision while preserving more recall/connectivity than ABI-059's subtractive suppression. A useful positive result would tie or exceed ABI-058 capped filtered Dice while improving precision, predicted-positive burden, connectivity, or source balance. A useful mixed result would identify whether soft gating is a better family mechanism than subtractive suppression even if aggregate Dice remains below ABI-058.

## Implementation Sketch

- Reuse the ABI-058/ABI-059 front end: normalized provider-approved ABI channels 1-16, eight explicit thermal brightness-temperature-difference planes derived only from approved ABI channels, and a learned 16-channel 1x1 GELU projection.
- Keep the high-resolution line U-Net encoder, dilated coarsest context, gated decoder skips, multi-scale skip fusion, and oriented full-resolution context refiner.
- Replace ABI-059's `FalsePositiveSuppressorHead` with `ConfidenceGatedMaskHead`:
  - build an oriented line-feature branch with horizontal/vertical asymmetric convolutions;
  - build a low-resolution context branch and upsample it back to full resolution;
  - predict soft confidence and line gates from concatenated refined, line, and context features;
  - form final mask features from confidence-gated full-resolution features, line-gated oriented features, and context features;
  - produce `mask_logits` and a provider-declared `centerline_logits` auxiliary output from differentiable network layers.
- Keep trusted `bce_dice_cldice`, `centerline` auxiliary target with trusted `weighted_bce` weight 0.02, `combined_source_balanced` traversal, `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler policy, disabled early stopping, and provider-owned capped-record selection.
- Request one sequential Run because the Agent-visible parallel cap is one and this is a controlled but still resource-nonidentical decoder-head branch.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice_cldice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, primary and auxiliary loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, sampling policy, augmentation, target derivation, losses, metrics, artifact filtering, postprocessing, thresholding, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No Experiment Batch, Post-Run Evaluation, full-data training claim, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, checkpoints, and both output heads remain finite.
4. Predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. Relative to ABI-058 and ABI-056, the continuation is extension-positive if it improves or credibly ties capped filtered Dice while lowering predicted-positive fraction, improving precision, preserving recall/source balance, or recovering connectivity relative to ABI-059.

## Continuation and hard stop

Low capped Dice alone should not eliminate the broader high-resolution line U-Net family if ABI-060 remains finite, non-degenerate, source-informative, or diagnostically distinct. Do not repeat this exact confidence-gated head unchanged if it underperforms ABI-058/ABI-056 without useful precision, predicted-positive, connectivity, stability, or source-balance gains. Eliminate or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope.

## Fallback/Next Decision

If ABI-060 fails due to a narrow implementation defect while the hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but does not improve false-positive behavior over ABI-058/ABI-056, document the result and broaden away from high-resolution decoder-head refinements toward a materially different architecture family or a trusted-policy axis. If it reduces false positives while preserving ABI-058-like Dice, request separately authorized whole-validation diagnostics rather than claiming promotion from capped data.
