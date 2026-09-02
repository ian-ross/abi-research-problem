# ABI-170 Full-Spectral BTD+SZA Compact BiFPN Multiscale Line-Head BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-162 established that a compact full-spectral BTD+SZA BiFPN line-fusion U-Net is resource-feasible and still improving at epoch 12, but its fixed-threshold result was under-recalled and had weaker connectivity than ABI-068, ABI-130, and ABI-154. ABI-163 showed that changing the same compact BiFPN topology to focal-Tversky recovers recall only by over-expanding predicted positives, damaging precision, Google Dice, and connectivity. ABI-170 therefore stays inside the compact BiFPN family and changes one architecture factor: the final line-context head.

## Hypothesis

The compact BiFPN branch may need a stronger but still lightweight line-continuity head rather than a loss-axis change. ABI-162's final head used one short horizontal/vertical context scale. Adding a bounded multiscale horizontal/vertical feature-space support path after BiFPN fusion should help bridge thin contrail gaps and raise connectivity while keeping BCE-Dice calibration, source-balanced traversal, and the compact resource profile that avoided ABI-161's timeout. Because the added support is feature-space and residual, not thresholding or postprocessing, it remains candidate-owned architecture rather than provider-owned Artifact Filter behavior.

## Comparison Target

The primary comparison target is ABI-162 `abi162_fullspectral_btd_sza_compact_bifpn_line_fusion_unet_bce_dice_centerline_aux_v1`, Run `run_20260901_142708_a2f6c9`: capped filtered Dice 0.3738, MIT/Google filtered Dice 0.3576/0.4133, filtered precision 0.4242, recall 0.3342, connectivity 0.3256, and filtered predicted-positive fraction 0.00285.

Secondary references are ABI-163 `run_20260901_150632_dc4961` for the focal-Tversky over-recall failure mode, ABI-154 `run_20260901_071026_32d3ec` as the whole-validation-tested precision/connectivity SZA-aware ASPP/detail reference, ABI-130 `run_20260831_121006_7d24be` as the SZA-aware ASPP/detail aggregate reference, and ABI-068 `run_20260828_010836_4ccc77` as the current capped aggregate/source-balance reference. Canonical MCAST 2.1 remains promotion context only.

## Expected Effect

A useful outcome would improve ABI-162 filtered connectivity by at least about 0.03 while keeping aggregate filtered Dice near ABI-162 and not moving toward ABI-163-like overprediction. A stronger outcome would also recover MIT filtered Dice or recall while preserving Google Dice above roughly 0.40 and filtered predicted-positive fraction below roughly 0.0035. A negative outcome would show that adding more line-context capacity to the compact BiFPN head either fails to improve connectivity or trades it for clutter without approaching ABI-068/130/154.

## Implementation Sketch

- Reuse ABI-162's provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels, deterministic thermal BTD planes from approved ABI channels, normalized/cosine Solar Geometry Input features, and compact learned 1x1 spectral mixture.
- Keep the compact residual encoder, positive normalized BiFPN top-down/bottom-up fusion, high-resolution encoder feature reuse, BCE-Dice primary loss, and Centerline Target auxiliary output.
- Replace ABI-162's short `CompactLineHead` with a `MultiScaleLineContinuityHead` using short 9-pixel and long 17-pixel horizontal/vertical feature convolutions, local detail, broad context, and a sigmoid feature-space support gate.
- Add the gated line support residually into fused features before the final projection; emit only `mask_logits` and `centerline_logits`.
- Request one sequential representative capped Run; do not add candidate-owned data loading, target derivation, loss, metric, threshold, Artifact Filter, postprocessing, scheduling, GPU placement, runtime downloads, or external persistence.

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
6. As family-development evidence, the result is useful if it improves ABI-162 connectivity or MIT recall/Dice without causing ABI-163-like positive-area expansion or materially worsening ABI-162 Google Dice.

## Continuation and hard stop

Continue the compact BiFPN family only if ABI-170 is finite, non-degenerate, resource-safe, and shows either a connectivity improvement over ABI-162, a cleaner recall/precision balance than ABI-163, or a still-improving trajectory that narrows the gap to ABI-068/130/154. Stop this exact multiscale line-head branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, resource timeout, severe source-specific collapse, or a completed result that remains below ABI-162 without a compensating connectivity, recall, precision, source-balance, or trajectory signal.

## Fallback/Next Decision

If the candidate fails from a narrow implementation defect while the multiscale line-head hypothesis remains intact, consider one explicit Repair Candidate in a later Autonomy Step. If it completes but is scientifically negative, document the result and broaden away from compact BiFPN line-head tuning toward a different architecture, preprocessing, loss, calibration, or data-policy frontier. If it unexpectedly challenges the current capped references or gives a uniquely strong connectivity/negative-patch result, request a separate whole-validation diagnostic before making any full-data or promotion claim.
