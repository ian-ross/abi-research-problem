# ABI-221 Proposal: temporal ConvGRU state U-Net

## Hypothesis

ABI-221 is a **family scout / family-development continuation** within the young temporal branch. ABI-219 showed that explicit temporal-difference features beat the matched temporal-eligible single-frame control (filtered Dice 0.3676 versus ABI-218's 0.3456), while ABI-220's change-confidence gate only marginally improved primary Dice and did not stabilize recall/connectivity. This suggests provider-owned neighboring frames contain useful signal, but further simple difference-stem/gate tuning is unlikely to add much evidence.

The hypothesis is that a compact recurrent temporal state can learn persistence, short-term advection, and before/after consistency more flexibly than hand-combined center-minus-neighbor features. A small bidirectional ConvGRU over bounded per-frame ABI+SZA+BTD features should let the model retain thin-line temporal evidence while a center-frame path protects against overusing transient cloud edges or static geography.

## Comparison Target

The primary comparison target is ABI-220, Candidate `abi220_temporal_change_confidence_gate_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260908_134203_8bbb6f`: best epoch 11 filtered Dice 0.368730, raw Dice 0.384987, filtered precision 0.417944, filtered recall 0.329885, connectivity 0.278802, MIT filtered Dice 0.350694, Google filtered Dice 0.415136, and 3.07M parameters.

Secondary temporal-family context:

- ABI-219 temporal-difference front-end, Run `run_20260908_130608_80d612`: best filtered Dice 0.367589, recall 0.335468, connectivity 0.288750.
- ABI-218 matched temporal-eligible single-frame control, Run `run_20260908_123030_05ad37`: best filtered Dice 0.345570, recall 0.300125, connectivity 0.231399.
- ABI-217 temporal Siamese/change model, Run `run_20260908_114854_409a12`: best filtered Dice 0.349086, recall 0.317751, connectivity 0.265915.

ABI-202 (`run_20260904_043143_ee0005`) remains the current best whole-validation-tested frontier. ABI-221 is not a promotion candidate and is not expected to beat ABI-202 immediately; it tests whether learned temporal state gives a stronger temporal-family direction than explicit difference gates.

## Expected Effect

Compared with ABI-220, ABI-221 should remain resource-comparable while replacing hand-weighted temporal residual confidence with learned recurrent state. Useful signals would include matching or exceeding ABI-219/220 filtered Dice, improving recall/connectivity stability, or showing a different MIT/Google tradeoff that clarifies whether temporal context helps one Dataset Source more than the other.

Expected useful outcomes include:

- filtered Dice, filtered recall, or Contrail Connectivity Metric improvement over ABI-219/220;
- a clearer benefit over ABI-218's matched single-frame control;
- source-informative, noncollapsed behavior on both MIT and Google;
- resource use within the existing temporal branch profile and below the exploratory envelope.

## Implementation Sketch

- Consume only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and reshape the channel-stacked tensor into previous, center, and next ABI+SZA frames.
- For each frame, construct bounded architecture features from ABI channels 1-16, approved-channel thermal BTD planes, scaled Solar Geometry Input, and cosine Solar Geometry Input.
- Use a shared compact projection for each frame's bounded features.
- Run a small bidirectional ConvGRU across the three projected frames to learn forward and reverse temporal state from the provider-supplied window.
- Project average absolute center-neighbor change as an explicit change summary, but avoid ABI-219/220's larger hand-combined signed-difference stack.
- Fuse center-frame embedding, forward/reverse ConvGRU states, and change summary with a learned spatial/channel gate, then feed one compact residual U-Net/ASPP encoder-decoder with base width 24.
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
6. Scientific success is evidence that learned recurrent temporal state improves or usefully trades off against ABI-219/220 on filtered Dice, recall, connectivity, source balance, or temporal-family stability while staying resource-comparable.

## Continuation and Hard Stop

Continue recurrent temporal modeling if ABI-221 is finite, source-informative, noncollapsed, and improves or closely matches ABI-219/220 while showing better recall/connectivity or a diagnostically useful Dataset Source tradeoff. Consider a late-improving budget only after Harness-valid evidence satisfies the approved late-improving criteria; ABI-220 itself did not justify it because final-epoch behavior still dropped.

Hard-stop this exact ConvGRU state design if it fails contract validation, becomes non-finite, suffers Resource Failure despite the compact design, persistently collapses, or clearly underperforms ABI-219/220 and ABI-218 without a useful secondary-metric tradeoff. Do not eliminate temporal modeling globally solely because ABI-221 trails ABI-202; this remains early bounded temporal-family development.

## Fallback Next Decision

If ABI-221 fails narrowly, classify and repair only if the recurrent temporal-state hypothesis remains blocked by a candidate bug. If it completes but does not improve over ABI-219/220, broaden to a lightweight temporal-attention or five-frame temporal-difference scout rather than continuing small stem/gate mutations.
