# ABI-132 Full-Spectral BTD+SZA ASPP/Detail Decoder Region-Line Agreement v1

## Proposal classification

**Family-development continuation.** ABI-130 established useful SZA-aware ASPP/detail evidence: capped filtered Dice 0.3953 and whole-validation filtered Dice 0.3954, with improved default-threshold recall and MIT behavior relative to ABI-126. ABI-131 showed that a simple post-refinement continuity bridge damaged connectivity and did not improve ABI-130. ABI-132 keeps ABI-130's input, trusted loss, auxiliary target, data policy, and main encoder-decoder fixed while changing only the mask head to a bounded region-line agreement residual.

## Hypothesis

ABI-130's whole-validation review showed a real but imperfect trade-off: SZA improved fixed-threshold recall and aggregate Dice, but gave up part of ABI-126/ABI-066's precision and Contrail Connectivity Metric. A zero-initialized, bounded residual head that must combine local detail, broad regional support, and horizontal/vertical line context may let the model suppress unsupported clutter and recover connectivity without reverting to ABI-126-style under-recall. Because the residual is learned inside the model logits, this tests in-contract calibration rather than candidate-owned thresholding, postprocessing, or Artifact Filters.

## Comparison Target

The primary comparison target is ABI-130 `abi130_fullspectral_btd_aspp_detail_decoder_sza_bce_dice_centerline_aux_v1`, Run `run_20260831_121006_7d24be`: capped filtered Dice 0.3953, MIT/Google filtered Dice 0.3779/0.4404, filtered precision 0.4415, filtered recall 0.3578, filtered connectivity 0.3851, and filtered predicted-positive fraction 0.00294. Its whole-validation diagnostic reached filtered Dice 0.3954, precision 0.4436, recall 0.3566, connectivity 0.3935, and confirmed the SZA recall/calibration gain with added clutter/connectivity cost.

Secondary references are ABI-126 `run_20260831_085615_d05ab3` as the ASPP/detail high-precision/connectivity comparator, ABI-066 `run_20260827_230540_bf4ce3` as the line-family connectivity reference, ABI-068 `run_20260828_010836_4ccc77` as the local aggregate-Dice/source-balance reference, and ABI-131 `run_20260831_130730_08040a` as the negative simple-continuity continuation. Canonical MCAST 2.1 remains full Working Validation Split promotion context, not a promotion claim for this capped continuation.

## Expected Effect

A useful result would stay close to ABI-130's aggregate and source Dice while improving filtered precision, filtered connectivity, or filtered predicted-positive discipline. The desired movement is smaller than a new family scout: recover part of the ABI-126/066 precision/connectivity gap without giving back ABI-130's SZA-assisted recall. A negative result would show that additional local agreement capacity either behaves like ABI-131's damaging continuity bridge or merely adds parameters without moving the precision/recall/connectivity trade-off.

## Implementation Sketch

- Reuse ABI-130's compact torch-only ASPP/detail encoder-decoder: normalized approved ABI channels, deterministic thermal BTD planes from ABI channels 1-16, normalized SZA and `cos(SZA)` features, learned 1x1 spectral projection, detail/context stem, residual encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail path, and line-aware refinement.
- Replace the single 1x1 `mask_head` with `RegionLineAgreementHead`.
- The new head keeps a standard learned 1x1 base mask-logit projection from the refined feature map.
- In parallel, it forms local detail from `features - smooth(features)`, broad regional support from a larger average-pooled context, and horizontal/vertical line context using non-wrapping convolutions.
- These feature streams are fused through normal residual conv blocks and projected to a bounded residual logit correction, initialized exactly to zero and added as `base_logits + 0.75 * tanh(residual_logits)`.
- Emit primary `mask_logits` and trusted auxiliary `centerline_logits` from the same refined feature map.
- Preserve trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision with trusted `weighted_bce` weight 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.
- Request one sequential Run only; no Experiment Batch or candidate-owned scheduling/resource placement is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data evidence, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it matches ABI-130 within about 0.01 aggregate filtered Dice while improving filtered precision, filtered connectivity, or filtered predicted-positive discipline, or if it exposes a clear limitation of bounded model-internal agreement heads for SZA-aware ASPP/detail calibration.

## Continuation and hard stop

Continue only if ABI-132 is finite, non-degenerate, source-informative, and improves a meaningful ABI-130-relative diagnostic: precision/connectivity recovery, positive-area stability, source balance, or late-epoch trajectory without destroying recall. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. A finite result materially below ABI-130 and ABI-126 on aggregate Dice without a precision/connectivity gain would be enough to stop this exact head variant, but would not eliminate SZA-aware ASPP/detail architectures broadly.

## Fallback/Next Decision

If this candidate fails because of a narrow implementation defect while the region-line agreement hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but repeats ABI-131's connectivity loss or adds no useful calibration signal, document the negative family-development result and broaden to a different architecture, preprocessing, trusted data-policy, loss/auxiliary-target, or calibration frontier rather than stacking more simple ASPP/detail head tweaks. If it unexpectedly challenges ABI-068 or MCAST context, request separately authorized whole-validation diagnostics rather than claiming promotion from capped data.
