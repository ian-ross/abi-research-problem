# ABI-045 Full-Spectral DeepLabV3+ Focal-Tversky Continuation v1

## Proposal classification

**Family-development continuation.** This is a controlled follow-up inside the full-spectral DeepLabV3+ family after ABI-044 completed a finite, non-degenerate, source-balanced, still-improving 12-epoch representative scout. It is not a promotion claim or full-data request.

## Hypothesis

The ABI-044 DeepLabV3+ scout improved through epoch 12 but remained recall-limited at the standard threshold (`val/filtered_recall` 0.0959, `val/filtered_precision` 0.1772, `val/filtered_dice` 0.1244). Replacing trusted `bce_dice` with trusted `focal_tversky` while holding architecture, input mode, augmentation, sampling, learning rate, batch size, and epoch budget constant should bias optimization toward missed thin Contrail Mask pixels and may improve filtered Dice or expose whether the family is precision/recall trade-off limited under the current 12-epoch cap.

## Comparison Target

The family comparison target is ABI-044 `abi044_fullspectral_deeplabv3plus_representative_scout_v1`, Run `run_20260813_145951_a64a37`: 12 epochs, 1,024 records per Dataset Source and Leakage-Safe Split, batch size 4, `bce_dice`, aggregate `val/filtered_dice` 0.124435, `val/raw_dice` 0.129035, MIT filtered Dice 0.112489, Google filtered Dice 0.152161, non-degenerate filtered predicted-positive fraction 0.001961, and provider scout assessment `extension_eligible`. Canonical MCAST 2.1 filtered Dice 0.3873 remains promotion context rather than a strict gate for this immature family-development run.

## Expected Effect

Focal-Tversky loss should penalize false negatives more strongly than the ABI-044 BCE-Dice objective and may raise filtered recall and predicted-positive fraction from ABI-044's sparse-positive regime. A successful result need not beat MCAST 2.1; it should clarify whether the DeepLabV3+ family can improve recall without unacceptable precision loss, artifact-filter dependence, source imbalance, or prediction collapse.

## Implementation Sketch

- Reuse the ABI-044 randomly initialized SMP DeepLabV3+ ResNet-18 architecture: output stride 16, 256-channel decoder, atrous rates 12/24/36, no encoder weights, and one `mask_logits` output plane.
- Reuse ABI-044 rounded trusted campaign-context channel normalization constants for approved `abi_16ch` input.
- Preserve provider-owned `combined_source_balanced` traversal and trusted `random_mirroring` augmentation.
- Change only the primary trusted loss from `bce_dice` to `focal_tversky` in `manifest.yaml`.
- Keep AdamW learning rate 0.0003, batch size 4, and max epochs 12 to isolate the loss effect and remain within the observed ABI-043/044 sequential resource envelope.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are excluded.
- Output form: one `[1, 256, 256]` `mask_logits` tensor.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `focal_tversky`, AdamW, constant learning-rate policy, batch size 4, max epochs 12.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, targets, trusted loss implementation, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, losses, metrics, artifact filtering, target transforms, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No Experiment Batch, concurrency, full-data evaluation, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite.
4. Final epochs do not persistently collapse to all-negative or all-positive predictions.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. Relative to ABI-044, the result is diagnostically useful if it improves filtered recall without severe precision collapse, improves or credibly ties filtered Dice, or cleanly demonstrates that focal-Tversky mainly trades precision for recall under this architecture and budget.

## Continuation and hard stop

Continue DeepLabV3+ family development only if this loss variant is finite, non-degenerate, source-informative, or improves a meaningful family diagnostic such as filtered recall, filtered Dice, late-epoch trajectory, or MIT/Google balance. Eliminate or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or a convincing precision/recall deterioration relative to ABI-044. Low capped Dice alone is not promotion evidence and not a family-wide elimination rule.

## Fallback Next Decision

If this candidate fails due to a narrow implementation defect while the hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but confirms the loss trade-off is unhelpful, document the result and consider a separate controlled DeepLabV3+ architecture or channel-mixing continuation. If it unexpectedly exceeds the current capped family best, request separately authorized focused full-data evidence rather than claiming promotion from capped data.
