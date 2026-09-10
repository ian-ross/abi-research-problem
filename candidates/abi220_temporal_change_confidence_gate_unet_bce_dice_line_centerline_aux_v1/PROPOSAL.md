# ABI-220 Proposal: temporal change-confidence gated U-Net

## Hypothesis

ABI-220 is a **family-development continuation** of the temporal-difference branch. ABI-219 showed the first clear temporal benefit over the matched temporal-eligible single-frame control: best filtered Dice 0.3676 versus ABI-218's 0.3456, with better recall and connectivity at nearly the same resource scale. Its later epochs oscillated between recall-oriented checkpoints and higher-precision/higher-connectivity lower-recall checkpoints, suggesting that temporal-change evidence is useful but its contribution to the mask logits is not yet stable.

The hypothesis is that preserving ABI-219's explicit center-minus-neighbor, next-minus-previous, and absolute-change features while replacing the simple all-feature multiplicative stem gate with a lightweight learned change-confidence residual path will stabilize how temporal evidence enters the decoder. A spatial and channel confidence gate should let the model add temporal-change residuals only where the provider-owned neighboring frames support a persistent or moving thin line, while keeping a center-frame baseline path available for static cloud/background discrimination.

## Comparison Target

The primary comparison target is ABI-219, Candidate `abi219_temporal_difference_frontend_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260908_130608_80d612`: best epoch 8 filtered Dice 0.367589, raw Dice 0.383372, filtered precision 0.406513, filtered recall 0.335468, connectivity 0.288750, MIT filtered Dice 0.352675, Google filtered Dice 0.403426, and 3.06M parameters.

Secondary temporal-family context:

- ABI-218 matched single-frame control, Run `run_20260908_123030_05ad37`: best filtered Dice 0.345570, recall 0.300125, connectivity 0.231399.
- ABI-217 temporal Siamese/change model, Run `run_20260908_114854_409a12`: best filtered Dice 0.349086, recall 0.317751, connectivity 0.265915.

ABI-202 (`run_20260904_043143_ee0005`) remains the current best whole-validation-tested frontier. ABI-220 is not a promotion candidate and is not expected to beat ABI-202 immediately; it tests whether temporal-difference stabilization can improve the young temporal branch enough to justify continued allocation.

## Expected Effect

Compared with ABI-219, ABI-220 should keep the same provider-owned temporal evidence and compact single-decoder resource profile, but improve the precision/recall stability of the temporal contribution. Useful signals would include matching or exceeding ABI-219's best filtered Dice while retaining more of the epoch-8 recall and more of the epoch-10/12 connectivity, or reducing the post-peak drop seen in ABI-219.

Expected useful outcomes include:

- filtered Dice, filtered recall, or Contrail Connectivity Metric improvement over ABI-219;
- source-informative behavior on both MIT and Google without prediction collapse;
- resource use close to ABI-219 and below the exploratory envelope.

## Implementation Sketch

- Consume only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and reshape the channel-stacked tensor into previous, center, and next ABI+SZA frames.
- For each frame, construct bounded architecture features from ABI channels 1-16, approved-channel thermal BTD planes, scaled Solar Geometry Input, and cosine Solar Geometry Input.
- Preserve ABI-219's four temporal feature groups: center-frame features, center-minus-neighbor-mean features, next-minus-previous features, and average absolute center-neighbor change.
- Replace ABI-219's simple whole-stack stem gate with a center-frame projection plus signed-change and absolute-change residual projections.
- Learn both a spatial confidence gate and a channel confidence gate from the complete temporal-difference stack; use them to add a bounded temporal-change residual to the center-frame stem.
- Add a small residual calibration block after the gated change fusion, then feed one compact residual U-Net/ASPP encoder-decoder with base width 24.
- Emit primary `mask_logits` plus trusted Line and Centerline auxiliary logits.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Frame selection policy: `temporal_eligible_center`.
- Temporal frame offsets: `[-1, 0, 1]`, an allowlisted provider-owned temporal window.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.02, AdamW, learning rate 0.0003, batch size 2, max epochs 12, constant learning-rate scheduler, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, temporal eligibility, temporal cache/provenance validation, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, thresholding, postprocessing, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, temporal lookup, S3/NetCDF reads, cache access, frame padding/repair, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, external persistence, coordinates, Dataset Source identity, or route/location priors.

## Budget Requested

Use the exploratory/default Candidate budget: one sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 2, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler, disabled early stopping, and the 3,600-second trusted exploratory training timeout. No late-improving budget, Experiment Batch, full-data evidence, Post-Run Evaluation, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. The Run reports `abi_16ch_plus_sza_temporal`, effective `temporal_eligible_center` frame selection, and provider-owned offsets `[-1, 0, 1]`.
3. Parameter count remains below the 25,000,000 smoke ceiling and batch size 2 completes without Resource Failure retry.
4. Predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw/filtered metrics plus predicted-positive fractions are reported.
6. Scientific success is evidence that change-confidence gating improves on ABI-219's filtered Dice, filtered recall, connectivity, source balance, or post-peak stability while staying resource-comparable. A finite but lower score is still useful if it shows that ABI-219's simple temporal-difference stem was already the better allocation.

## Continuation and Hard Stop

Continue this temporal-change gating branch if ABI-220 is finite, source-informative, noncollapsed, and improves or closely matches ABI-219 while showing better recall/connectivity stability. Consider a late-improving budget only after Harness-valid evidence satisfies the approved late-improving criteria; ABI-219 did not justify it because it peaked before the final exploratory epoch.

Hard-stop this exact change-confidence gate if it fails contract validation, becomes non-finite, suffers Resource Failure despite the compact single-stream design, persistently collapses, or clearly underperforms ABI-219 without a useful secondary-metric tradeoff. Do not eliminate temporal modeling globally solely because ABI-220 trails ABI-202; this remains early bounded temporal-family development.

## Fallback Next Decision

If ABI-220 fails narrowly, classify and repair only if the temporal-change-confidence hypothesis remains blocked by a candidate bug. If it completes but does not improve over ABI-219, stop simple temporal-difference stem tuning and broaden within temporal modeling to a compact ConvGRU, temporal attention, or five-frame temporal-difference scout under the provider-owned temporal input contract.
