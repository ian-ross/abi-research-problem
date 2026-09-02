# ABI-046 Full-Spectral DeepLabV3+ BTD-Mixer Continuation v1

## Proposal classification

**Family-development continuation.** This is a controlled follow-up inside the full-spectral DeepLabV3+ family after ABI-044 established the best capped DeepLabV3+ filtered Dice to date and ABI-045 showed that focal-Tversky raises recall but over-trades away precision. It is not a promotion claim or full-data request.

## Hypothesis

ABI-044's BCE-Dice DeepLabV3+ was precision-favorable but recall-limited (`val/filtered_dice` 0.124435, precision 0.177194, recall 0.095885), while ABI-045's focal-Tversky variant raised recall to 0.265716 but reduced precision to 0.061961 and aggregate filtered Dice to 0.100489. Adding explicit normalized thermal brightness-temperature-difference (BTD) contrast planes plus a learned 1x1 channel projection to the ABI-044 BCE-Dice architecture should improve thin-ice/cloud discrimination and recover some recall without the severe precision loss seen in ABI-045.

## Comparison Target

The primary family comparison target is ABI-044 `abi044_fullspectral_deeplabv3plus_representative_scout_v1`, Run `run_20260813_145951_a64a37`: 12 epochs, 1,024 records per Dataset Source and Leakage-Safe Split, batch size 4, `abi_16ch`, `bce_dice`, `random_mirroring`, aggregate `val/filtered_dice` 0.124435, MIT filtered Dice 0.112489, Google filtered Dice 0.152161, filtered precision 0.177194, filtered recall 0.095885, and filtered predicted-positive fraction 0.001961. ABI-045 Run `run_20260826_120037_b98df4` is the recall/precision trade-off reference: filtered Dice 0.100489, precision 0.061961, recall 0.265716, MIT filtered Dice 0.128676, Google filtered Dice 0.068367, and filtered predicted-positive fraction 0.015540. Canonical MCAST 2.1 filtered Dice 0.3873 remains promotion context rather than a strict gate for this capped family-development run.

## Expected Effect

The explicit BTD planes should expose physically meaningful thermal contrasts for thin ice clouds while the learned projection lets the model retain flexible channel combinations. With the primary loss returned to trusted BCE-Dice, expected behavior is a less extreme predicted-positive fraction than ABI-045, filtered recall above ABI-044 if the added spectral features are useful, and filtered Dice that credibly improves or ties the ABI-044 family best. A useful negative result would show that this simple spectral front end does not improve the family under the current epoch and record cap.

## Implementation Sketch

- Reuse the ABI-044 SMP DeepLabV3+ ResNet-18 architecture, output stride 16, 256-channel decoder, atrous rates 12/24/36, no encoder weights, and one `mask_logits` output plane.
- Add a narrow candidate-owned front end that receives only provider-approved `abi_16ch` tensors, normalizes raw channels using the same rounded trusted campaign-context constants as ABI-044, computes eight explicit thermal BTD planes from ABI channels 7-16, and concatenates a 16-channel learned 1x1 GELU projection of normalized raw channels.
- Feed the resulting 40-channel tensor into the DeepLabV3+ encoder.
- Preserve provider-owned `combined_source_balanced` traversal, `random_mirroring` augmentation, trusted `bce_dice` loss, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Request one sequential Run only; no Experiment Batch or candidate-owned resource scheduling is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are excluded.
- Output form: one `[1, 256, 256]` `mask_logits` tensor.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, AdamW, constant learning-rate policy, batch size 4, max epochs 12.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, targets, loss implementation, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, losses, metrics, artifact filtering, target transforms, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data evidence, Post-Run Evaluation, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. Relative to ABI-044, the result is diagnostically useful if it improves or credibly ties filtered Dice, improves filtered recall without ABI-045-like precision collapse, or clarifies that explicit BTD features do not help this DeepLabV3+ branch under the active cap.

## Continuation and hard stop

Continue DeepLabV3+ family development only if this channel-front-end variant is finite, non-degenerate, source-informative, or improves a meaningful family diagnostic such as filtered Dice, recall/precision balance, source balance, or late-epoch trajectory. Eliminate or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. Low capped Dice alone is not promotion evidence and not a family-wide elimination rule.

## Fallback/Next Decision

If this candidate fails due to a narrow implementation defect while the hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but does not improve the ABI-044 family best, document the result and consider a separate architecture-family scout or a trusted auxiliary-target continuation. If it unexpectedly exceeds the current capped family best, request separately authorized focused full-data evidence rather than claiming promotion from capped data.
