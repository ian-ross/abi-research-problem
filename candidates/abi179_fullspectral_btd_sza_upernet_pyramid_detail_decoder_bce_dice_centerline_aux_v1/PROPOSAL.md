# ABI-179 Full-Spectral BTD+SZA UPerNet Pyramid/Detail Decoder BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family scout.** Recent ABI-173 through ABI-178 signed-detail/full-scale ASPP continuations completed finitely but did not produce a better aggregate/source/connectivity tradeoff than the capped ABI-068, ABI-130, ABI-154, and ABI-173 references. ABI-179 broadens the architecture frontier from ASPP/full-scale-skip patches to a UPerNet-style pyramid-pooling plus top-down feature-pyramid decoder while retaining the same trusted input, loss, data, and auxiliary-supervision policies.

## Hypothesis

Contrail masks require both broad scene/cloud context and high-resolution thin-line evidence. The strongest recent SZA-aware ASPP/detail candidates alternated between recall-forward and precision/connectivity-forward checkpoints, suggesting that late local refinement may not calibrate context and detail consistently. A UPerNet-style decoder that first forms bottleneck pyramid-pooling context, then propagates it through a top-down feature pyramid and fuses signed high-resolution detail at mask resolution may give the model a cleaner scale hierarchy: broad context suppresses clutter while detail branches preserve thin positive/negative ABI and BTD anomalies.

## Comparison Target

The primary comparison target is ABI-173 `abi173_fullspectral_btd_sza_signed_detail_fullscale_skip_aspp_decoder_bce_dice_centerline_aux_v1`, Run `run_20260901_234732_bd5917`: capped filtered Dice 0.3962, MIT/Google filtered Dice 0.3838/0.4269, filtered precision 0.4238, recall 0.3720, connectivity 0.3203, and filtered predicted-positive fraction 0.00318. Secondary references are ABI-154 `run_20260901_071026_32d3ec` for precision/connectivity, ABI-130 `run_20260831_121006_7d24be` for SZA-aware ASPP/detail aggregate behavior, ABI-068 `run_20260828_010836_4ccc77` for recall/source balance, and ABI-178 `run_20260902_044555_a3f915` as the negative thermal-only signed-detail input-frontier control. Canonical MCAST 2.1 remains promotion context only.

## Expected Effect

A useful scout would complete finitely and non-degenerately while reaching the ABI-130/154/173 aggregate band or showing a diagnostically distinct balance, such as ABI-173-like recall with better connectivity, ABI-154-like precision/connectivity with less recall loss, or improved MIT filtered Dice without a large Google regression. A negative result would be persistent non-finite behavior, prediction collapse, a severe source-specific collapse, or another late-epoch oscillatory regime that falls clearly below the capped reference band without a compensating secondary-metric strength.

## Implementation Sketch

- Use provider-approved `abi_16ch_plus_sza` input only: normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived from approved ABI channels, normalized Solar Geometry Input, cosine SZA, and a learned 1x1 projection over approved inputs.
- Replace the ASPP/full-scale-skip decoder with a compact UPerNet-like structure: residual encoder, bottleneck pyramid pooling at 1/2/4 pooled scales, top-down lateral feature pyramid over encoder scales, and high-resolution signed-detail fusion at the final mask scale.
- Use positive and negative local/mid-scale residual streams only as learned feature inputs, not as target transforms, postprocessing, or Artifact Filters.
- Preserve a line-context feature refiner before the primary and auxiliary output heads, but return only `mask_logits` and provider-declared `centerline_logits`.
- Keep trusted BCE-Dice primary loss, trusted weighted-BCE Centerline Target auxiliary weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant scheduler, disabled early stopping, and one sequential representative capped Run.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, Dataset Source identity, labels, predictions, external data, and pretrained weights are not candidate inputs.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, primary and auxiliary loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data claim, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains below the 25,000,000 smoke ceiling and batch size 4 completes inside the trusted runtime envelope.
3. Losses, logits, gradients, parameters, aggregate/source metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As scout evidence, continue the UPerNet-style family if ABI-179 reaches within roughly 0.01 filtered Dice of ABI-173 or shows a distinct useful secondary-metric tradeoff such as improved connectivity or MIT Dice without severe recall/precision loss.

## Continuation and hard stop

Treat ABI-179 as the first bounded UPerNet-style scout. Continue with at most two focused family-development runs only if it is finite, resource-safe, non-degenerate, source-informative, and either approaches the capped reference band or reveals a clear secondary-metric strength. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. Low score alone is not an elimination reason if the trajectory is improving and non-degenerate, but a flat or collapsing 12-epoch trajectory would be a hard stop for this exact implementation.

## Fallback/Next Decision

If ABI-179 fails from a narrow implementation defect while the UPerNet-style hypothesis remains intact, consider one explicit Repair Candidate in a later Autonomy Step. If it completes finitely but behaves like another local context/detail regression, document the result and broaden away from SZA-aware context/detail decoders toward a different in-contract architecture, training-policy, data-policy, preprocessing, calibration, or evaluation frontier. If it unexpectedly challenges ABI-068/130/154/173 or shows an unusually strong source/connectivity tradeoff, request separate whole-validation diagnostics before making any full-data or promotion claim.
