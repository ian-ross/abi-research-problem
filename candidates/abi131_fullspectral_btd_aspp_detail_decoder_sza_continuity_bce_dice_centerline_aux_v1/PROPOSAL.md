# ABI-131 SZA-Aware ASPP/Detail Decoder Continuity Bridge v1

## Proposal classification

**Family-development continuation.** ABI-130 provided valid capped and whole-validation diagnostic evidence that provider-approved Solar Geometry Input improves the ASPP/detail BCE-Dice branch's fixed-threshold recall and MIT behavior relative to ABI-126. ABI-131 keeps ABI-130's input mode, trusted loss, auxiliary target, data policy, and training budget fixed, and changes only the decoder head geometry by adding a neutral, identity-initialized multi-directional continuity bridge.

## Hypothesis

ABI-130's whole-validation review confirmed a useful SZA recall/calibration gain, but it also showed lower connectivity and more negative-patch clutter than ABI-126/ABI-066. A learned continuity bridge after the line-aware refinement block should give the model a trainable way to connect long thin structures and suppress isolated detail responses without candidate-owned postprocessing. Because the bridge is residual and zero-initialized at its final projection, it should start from ABI-130-like behavior and only learn corrections if the trusted loss supports them.

## Comparison Target

The primary comparison target is ABI-130 `abi130_fullspectral_btd_aspp_detail_decoder_sza_bce_dice_centerline_aux_v1`, Run `run_20260831_121006_7d24be`: capped filtered Dice 0.3953, MIT/Google filtered Dice 0.3779/0.4404, filtered precision 0.4415, filtered recall 0.3578, filtered connectivity 0.3851, and filtered predicted-positive fraction 0.00294. Its whole-validation evaluation reported filtered Dice 0.3954, MIT/Google filtered Dice 0.3797/0.4256, precision 0.4436, recall 0.3566, connectivity 0.3935, and increased negative-patch clutter relative to ABI-126.

Secondary references are ABI-126 `run_20260831_085615_d05ab3` as the ASPP/detail high-precision/connectivity comparator, ABI-066 `run_20260827_230540_bf4ce3` as the local connectivity reference, ABI-068 `run_20260828_010836_4ccc77` as the MIT-recall-balanced aggregate reference, and ABI-121 `run_20260831_041559_43da35` as the ASPP/detail recall comparator. Canonical MCAST summaries remain promotion context only; this Candidate requests capped representative evidence, not promotion.

## Expected Effect

A useful result would keep ABI-130's aggregate filtered Dice near the current local reference range while improving filtered connectivity, precision, or negative-patch discipline relative to ABI-130. The ideal trade-off is modestly higher connectivity with no return to ABI-126-style MIT under-recall. A negative result would show that the SZA-aware ASPP/detail branch cannot recover continuity through head geometry alone under trusted BCE-Dice and low-weight centerline supervision.

## Implementation Sketch

- Reuse ABI-130's normalized raw ABI channel features, deterministic thermal BTD planes from provider-approved ABI channels 1-16, normalized SZA and `cos(SZA)` features, learned 1x1 mixer, detail/context stem, compact encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail path, line-aware refinement, primary `mask_logits`, and auxiliary `centerline_logits`.
- Add `MultiDirectionalContinuityBridge` after the existing `LineAwareRefinement` block and before both heads. The bridge builds horizontal, vertical, dilated, high-frequency detail, and broad-context features, fuses them with a residual projection, and returns `inputs + 0.5 * residual`.
- Initialize the bridge's final projection weights and bias to zero so the bridge is identity at initialization. This is a trainable architecture component, not a fixed Artifact Filter, thresholding rule, postprocessor, or target transform.
- Preserve trusted `bce_dice` primary loss, provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.
- Request one sequential Run only; no Experiment Batch, candidate-owned scheduling, candidate-owned resource placement, runtime downloads, pretrained weights, or external persistence are requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data evidence, Post-Run Evaluation, Experiment Batch, or promotion decision is requested in this handoff.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it improves ABI-130 filtered connectivity, precision, aggregate filtered Dice, MIT Dice/recall, or negative-patch discipline while avoiding severe loss of ABI-130's SZA-driven recall improvement.

## Continuation and hard stop

Continue this sub-branch only if ABI-131 is finite, non-degenerate, source-informative, and shows a meaningful ABI-130-relative gain in connectivity, negative-patch discipline, precision/recall balance, MIT behavior, aggregate Dice, or late-epoch trajectory. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. If ABI-131 completes finite but loses ABI-130's recall without improving connectivity or clutter, do not repeat this exact bridge unchanged.

## Fallback/Next Decision

If ABI-131 fails because of a narrow implementation defect while the SZA-continuity hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but cannot improve continuity/clutter over ABI-130, document the result and broaden away from simple ASPP/detail head-geometry tweaks toward a different contract-compliant architecture, calibration, preprocessing, loss, augmentation, or training-policy frontier. If it unexpectedly strengthens the ABI-130 whole-validation-tested pattern, request a separate bounded whole-validation diagnostic before any promotion discussion.
