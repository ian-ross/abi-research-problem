# ABI-145 Full-Spectral BTD+SZA ASPP/Detail Decoder Focal-Tversky Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-130 showed that the SZA-aware ASPP/detail BCE-Dice branch can nearly match the local capped aggregate-Dice reference while providing strong Google Dice and good precision, but it remained conservative at the fixed threshold, especially on MIT recall. ABI-145 keeps the ABI-130 model architecture, input mode, auxiliary target, optimizer, augmentation, and source-balanced data policy fixed while changing only the trusted primary loss from `bce_dice` to `focal_tversky`.

## Hypothesis

Focal-Tversky's asymmetric recall pressure may recover source-balanced thin-contrail recall in the SZA-aware ASPP/detail branch without losing all of ABI-130's positive-area discipline. ABI-121 showed that focal-Tversky can make the non-SZA ASPP/detail branch more recall-forward, while ABI-130 showed that SZA helps the BCE-Dice branch approach ABI-068-level aggregate Dice with stronger Google performance. Combining the two may improve MIT filtered Dice/recall and aggregate filtered Dice if SZA provides enough calibration to prevent the focal-Tversky branch from becoming overly permissive.

## Comparison Target

The primary comparison target is ABI-130 `abi130_fullspectral_btd_aspp_detail_decoder_sza_bce_dice_centerline_aux_v1`, Run `run_20260831_121006_7d24be`: capped filtered Dice 0.3953, MIT/Google filtered Dice 0.3779/0.4404, filtered precision 0.4415, filtered recall 0.3578, filtered connectivity 0.3851, and filtered predicted-positive fraction 0.00294.

Secondary references are ABI-121 `run_20260831_041559_43da35` as the non-SZA ASPP/detail focal-Tversky reference, ABI-126 `run_20260831_085615_d05ab3` as the non-SZA BCE-Dice ASPP/detail reference, and ABI-068 `run_20260828_010836_4ccc77` as the strongest local capped aggregate-Dice reference. Canonical MCAST 2.1 remains full Working Validation Split promotion context, not a promotion claim for this capped continuation.

## Expected Effect

A useful outcome would raise MIT filtered Dice or recall relative to ABI-130 and remain near ABI-130 aggregate filtered Dice, while keeping Google filtered Dice and precision from collapsing. The expected trade-off is higher predicted-positive fraction and recall with somewhat lower precision; the branch is useful only if that added positive area improves source-balanced overlap rather than recreating diffuse clutter.

## Implementation Sketch

- Reuse ABI-130's torch-only compact ASPP/detail encoder-decoder: normalized ABI channels, deterministic ABI-channel BTD planes, normalized SZA and `cos(SZA)`, learned 1x1 front-end projection, detail/context stem, residual encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail path, line-aware refinement, primary mask head, and centerline auxiliary head.
- Preserve provider-approved `abi_16ch_plus_sza` input; channels 1-16 are GOES ABI channels and the seventeenth candidate channel is Solar Geometry Input.
- Preserve primary `mask_logits` and trusted auxiliary `centerline_logits` outputs.
- Change only the manifest primary loss from `bce_dice` to trusted `focal_tversky`.
- Preserve provider-derived Centerline Target auxiliary supervision with trusted `weighted_bce` weight 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.
- Request one sequential Run only; no Experiment Batch or candidate-owned scheduling/resource placement is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `focal_tversky`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data evidence, Experiment Batch, Post-Run Evaluation, or promotion decision is requested in this handoff.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it improves ABI-130 MIT filtered Dice or recall, improves aggregate filtered Dice, stays within 0.01 aggregate filtered Dice while materially improving recall/source balance, or clearly demonstrates that focal-Tversky over-expands positive area in the SZA-aware ASPP/detail branch.

## Continuation and hard stop

Continue this branch only if ABI-145 is finite, non-degenerate, source-informative, and improves a meaningful ABI-130-relative diagnostic: MIT recall/Dice, aggregate Dice, precision/recall balance, connectivity retention, positive-area stability, or late-epoch trajectory. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. A finite result that loses ABI-130 precision and Google Dice without improving MIT recall or aggregate Dice would stop this exact loss-continuation branch, but would not eliminate ASPP/detail, SZA, BTD front ends, or focal-Tversky globally.

## Fallback/Next Decision

If this candidate fails because of a narrow implementation defect while the controlled loss hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but becomes too recall-heavy, document that focal-Tversky is not the right calibration pressure for the SZA-aware ASPP/detail branch and broaden toward different training policy, front-end, or architecture mechanisms rather than repeating small ASPP/detail head tweaks. If it unexpectedly challenges ABI-068 or canonical MCAST context, request separately authorized whole-validation diagnostics rather than claiming promotion from capped data.
