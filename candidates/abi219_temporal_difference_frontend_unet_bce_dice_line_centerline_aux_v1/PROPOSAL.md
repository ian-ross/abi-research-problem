# ABI-219 Proposal: compact temporal-difference front-end U-Net

## Hypothesis

ABI-219 is a **family-development continuation** of the temporal branch opened by ABI-215 through ABI-218. ABI-217 showed that a real three-frame Siamese/change model can train finitely on provider-owned `[-1, 0, 1]` temporal inputs, but ABI-218 showed that a cheaper single-frame control on the same `temporal_eligible_center` population nearly matched it: best filtered Dice 0.3456 versus ABI-217's 0.3491. The first temporal design therefore added only a small recall/connectivity edge for substantial resource cost.

The hypothesis is that temporal information may still help if it is presented as explicit, bounded center-minus-neighbor ABI/SZA/BTD change evidence at the front end rather than through three full frame encoders and multi-scale residual fusers. A lighter temporal-difference front end should preserve the useful temporal contrast signal while behaving closer to ABI-218's simpler optimization/resource profile.

## Comparison Target

The primary comparison targets are the matched temporal pair:

- ABI-217, Candidate `abi217_temporal_siamese_change_unet_finite_input_repair_bce_dice_line_centerline_aux_v1`, Run `run_20260908_114854_409a12`: best epoch 11 filtered Dice 0.3491, filtered precision 0.3873, filtered recall 0.3178, connectivity 0.2659, MIT filtered Dice 0.3338, Google filtered Dice 0.3875, and 4.33M parameters.
- ABI-218, Candidate `abi218_temporal_eligible_singleframe_control_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260908_123030_05ad37`: best epoch 11 filtered Dice 0.3456, filtered precision 0.4072, filtered recall 0.3001, connectivity 0.2314, MIT filtered Dice 0.3304, Google filtered Dice 0.3852, and 3.05M parameters.

Secondary context is ABI-202 (`run_20260904_043143_ee0005`), the current best whole-validation-tested frontier. ABI-219 is not a promotion candidate and is not required to beat ABI-202; it tests whether an early temporal mechanism can exceed the matched single-frame control clearly enough to justify further temporal-family allocation.

## Expected Effect

ABI-219 should be cheaper and easier to optimize than ABI-217 because it uses a single encoder/decoder after an explicit temporal-difference stem instead of encoding previous, center, and next frames independently at all scales. Compared with ABI-218, it should add signed and absolute temporal evidence that may improve recall and Contrail Connectivity Metric for persistent or advecting thin lines without requiring Dataset Source identity, coordinates, or candidate-owned temporal sampling.

Expected useful outcomes include:

- a filtered-Dice, recall, or connectivity improvement over ABI-218 larger than the small ABI-217-minus-ABI-218 difference;
- a resource profile closer to ABI-218 than ABI-217;
- finite, source-informative, noncollapsed learning on both MIT and Google.

## Implementation Sketch

- Consume only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and reshape the channel-stacked tensor into previous, center, and next ABI+SZA frames.
- For each frame, construct finite architecture features from ABI channels 1-16, approved-channel thermal BTD planes, scaled Solar Geometry Input, and cosine Solar Geometry Input.
- Concatenate center-frame features, `center - mean(previous, next)` features, `next - previous` features, and average absolute center-neighbor change features.
- Project this explicit temporal-difference feature stack with a compact 1x1 temporal stem and small learned change gate.
- Feed the projected features into one residual U-Net/ASPP encoder-decoder with base width 24, not three full frame encoders.
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
6. Scientific success is evidence that the explicit temporal-difference front end beats ABI-218's matched single-frame control by more than ABI-217's marginal advantage, especially on filtered recall or Contrail Connectivity Metric, while using materially less resource than ABI-217. A finite but lower score is still useful if it identifies that early temporal gains do not justify the added mechanism.

## Continuation and Hard Stop

Continue this temporal-difference branch if ABI-219 is finite, source-informative, noncollapsed, and clearly improves over ABI-218 on filtered Dice, recall, or connectivity, or if its trajectory is still improving near epoch 12 and suggests optimization rather than architecture exhaustion. Consider a late-improving budget only after Harness-valid evidence satisfies the approved late-improving criteria.

Hard-stop this exact branch if it fails contract validation, becomes non-finite, suffers Resource Failure despite the compact single-stream design, or persistently collapses such that it cannot evaluate temporal-difference value. Do not eliminate temporal modeling globally solely because ABI-219 trails ABI-202; this remains early bounded temporal-family development.

## Fallback Next Decision

If ABI-219 fails narrowly, classify and repair only if the temporal-difference hypothesis remains blocked by a candidate bug. If it completes but does not improve over ABI-218, deprioritize simple temporal-difference front ends and consider either a more selective temporal attention/ConvGRU scout with careful resource profiling or a broader non-temporal underexplored family such as rotation-aware line accumulation or lightweight window-attention segmentation.
