# ABI-156 Full-Spectral BTD+SZA Feature-Calibrated Full-Scale Skip ASPP/Detail Decoder BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-154 established full-scale skip aggregation as a valid precision/connectivity branch inside the SZA-aware ASPP/detail family, while ABI-155 showed that a simple final mask-head calibration patch did not recover default-threshold recall and reduced connectivity. ABI-156 preserves ABI-154's input, loss, data policy, training policy, and full-scale skip structure, and changes only where calibration is applied: before final feature projection rather than after mask logits are formed.

## Hypothesis

ABI-154's whole-validation diagnostic showed latent lower-threshold Dice and a conservative fixed-threshold operating point. ABI-155 attempted to shift that behavior at the final head and failed, suggesting that late logit-only calibration is too weak or too disconnected from the multi-scale evidence. A bounded Solar Geometry Input-conditioned feature-fusion calibrator applied to the concatenated decoder, detail, stem, and full-scale skip features may recover some default-threshold recall while preserving ABI-154's high precision, connectivity, and negative-patch discipline. Conditioning on the provider-approved Solar Geometry Input is expected to help daylight/illumination-dependent reflective-channel evidence without introducing coordinates or Dataset Source identity.

## Comparison Target

The primary comparison target is ABI-154 `abi154_fullspectral_btd_sza_fullscale_skip_aspp_detail_decoder_bce_dice_centerline_aux_v1`, Run `run_20260901_071026_32d3ec`: capped filtered Dice 0.3944, MIT/Google filtered Dice 0.3824/0.4260, filtered precision 0.4777, recall 0.3359, connectivity 0.4374, and filtered predicted-positive fraction 0.00255. Its whole-validation diagnostic reached filtered Dice 0.3941 and confirmed a real precision/connectivity shift with conservative recall.

Secondary references are ABI-155 `run_20260901_081321_b38989` as the failed final-head recall-calibration continuation, ABI-130 `run_20260831_121006_7d24be` as the SZA-aware ASPP/detail aggregate/reference branch, ABI-068 `run_20260828_010836_4ccc77` as the local aggregate/source-balance reference, and ABI-126 `run_20260831_085615_d05ab3` as the non-SZA ASPP/detail precision/connectivity comparator. Canonical MCAST 2.1 remains promotion context only.

## Expected Effect

A useful outcome would improve ABI-154 recall or aggregate/MIT filtered Dice without materially damaging its precision, connectivity, and low predicted-positive fraction. A stronger outcome would close the gap to ABI-130's aggregate/default-threshold Dice while retaining ABI-154's cleaner positive-area discipline and connectivity. A negative outcome would show that SZA-conditioned feature-fusion calibration is another local full-scale-skip branch that cannot recover recall without losing the precision/connectivity advantage.

## Implementation Sketch

- Reuse ABI-154's normalized full-spectral raw features, deterministic thermal BTD planes from approved ABI channels, normalized SZA and `cos(SZA)` features, learned 1x1 spectral projection, compact residual encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail/context stem, full-scale skip aggregation, and line-aware final refinement.
- Add a low-capacity `FeatureFusionCalibrator` after concatenating decoder, high-resolution detail, stem, and full-scale skip features and before the existing final projection.
- The calibrator receives the fused feature tensor plus normalized SZA and `cos(SZA)`, predicts a bounded per-feature multiplicative residual with `tanh`, and initializes its final convolution to zero so the starting function is neutral relative to ABI-154.
- Emit primary `mask_logits` and provider-derived auxiliary `centerline_logits` only.
- Request one sequential Run; no candidate-owned scheduling, GPU placement, postprocessing, thresholding, data loading, loss, target, augmentation, sampling, or metric code is introduced.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data claim, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes inside the trusted runtime envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it improves ABI-154 recall, aggregate filtered Dice, MIT filtered Dice, source balance, or ABI-130 distance while preserving ABI-154-like precision, connectivity, or positive-area discipline.

## Continuation and hard stop

Continue this feature-calibrated full-scale skip branch only if ABI-156 is finite, non-degenerate, source-informative, and preserves at least one useful ABI-154-relative diagnostic such as recall recovery, filtered Dice, connectivity, precision, positive-area discipline, source balance, or late-epoch improvement. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. If it completes finite but repeats ABI-155's weaker recall/connectivity profile or materially trails ABI-154 without a compensating diagnostic gain, stop this exact feature-calibration variant and broaden to another contract-compliant architecture, data-policy, loss/auxiliary, or preprocessing frontier.

## Fallback/Next Decision

If this candidate fails from a narrow implementation defect while the feature-fusion calibration hypothesis remains intact, consider at most one explicit Repair Candidate in a later Autonomy Step. If it is scientifically negative, document the result and broaden beyond local calibration of the full-scale skip ASPP/detail branch. If it unexpectedly improves capped and source-stratified metrics, request separate whole-validation diagnostics before making any full-data or promotion claim.
