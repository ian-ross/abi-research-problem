# ABI-218 Proposal: temporal-eligible single-frame control U-Net

## Hypothesis

ABI-218 is a **family-development continuation / matched control** for the temporal branch opened by ABI-215 through ABI-217. ABI-217 proved that a real provider-owned `[-1, 0, 1]` temporal Siamese/change model can train finitely on temporal-eligible centers, but its capped best `val/filtered_dice` of 0.3491 does not reveal whether the limiting factor is temporal-eligibility/sample composition, the compact U-Net/ASPP center-frame backbone, or the extra temporal residual streams.

The hypothesis is that a single-frame `abi_16ch_plus_sza` model trained on the same trusted `temporal_eligible_center` population, with the same source-balanced traversal, loss, auxiliary targets, learning rate, epoch budget, and batch size as ABI-217, will provide the missing control. If the control approaches or exceeds ABI-217, the first temporal fusion design likely added optimization burden without enough useful motion/change signal. If ABI-217 remains clearly stronger than the control, temporal residual streams are probably contributing information even though the first implementation trails the mature ABI-202 frontier.

## Comparison Target

The primary comparison target is ABI-217, Candidate `abi217_temporal_siamese_change_unet_finite_input_repair_bce_dice_line_centerline_aux_v1`, Run `run_20260908_114854_409a12`. ABI-217 completed a 12-epoch exploratory temporal Run with best epoch 11 filtered Dice 0.3491, MIT filtered Dice 0.3338, Google filtered Dice 0.3875, filtered recall 0.3178, filtered precision 0.3873, and noncollapsed predicted-positive fractions.

Secondary context is ABI-202 (`run_20260904_043143_ee0005`), the current best whole-validation-tested single-frame frontier. ABI-218 is not a promotion candidate and is not required to beat ABI-202; its value is to isolate temporal-eligible single-frame behavior before further temporal architecture development.

## Expected Effect

ABI-218 should train more simply than ABI-217 because it removes three-frame shared encoding and multi-scale temporal residual fusers while preserving the center-frame feature builder and decoder width. The expected outcome is a finite, resource-safe, nondegenerate single-frame control on the temporal-eligible center subset.

The diagnostic interpretation is the key effect:

- If ABI-218 substantially underperforms ABI-217 with comparable trajectory and source coverage, continue temporal/change modeling because the residual streams likely added useful signal.
- If ABI-218 matches or beats ABI-217, prioritize either a simpler temporal-difference front end or other underexplored families rather than expanding the current temporal Siamese design.
- If ABI-218 is unexpectedly much weaker than ordinary single-frame scouts, inspect whether temporal-eligible center selection changes the task distribution before interpreting temporal-model quality.

## Implementation Sketch

- Consume only provider-owned `abi_16ch_plus_sza` tensors; do not request temporal tensors for the model.
- Select the trusted `temporal_eligible_center` frame-selection policy in the manifest to match ABI-217's center population without candidate-side filtering.
- Reuse ABI-217's finite center-frame feature construction: normalized ABI channels 1-16, fixed approved-channel BTD planes, scaled Solar Geometry Input, and cosine Solar Geometry Input, with `torch.nan_to_num` and bounded finite feature ranges.
- Use one compact residual U-Net encoder/decoder with base width 24 and an ASPP bottleneck, mirroring the ABI-217 per-frame encoder and decoder width but without previous/next frames or temporal change fusers.
- Emit primary `mask_logits` plus trusted Line and Centerline auxiliary logits.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`.
- Frame selection policy: `temporal_eligible_center`.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.02, AdamW, learning rate 0.0003, batch size 2, max epochs 12, constant learning-rate scheduler, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, temporal eligibility, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, thresholding, postprocessing, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, temporal lookup, S3/NetCDF reads, cache access, frame padding/repair, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, external persistence, coordinates, Dataset Source identity, or route/location priors.

## Budget Requested

Use the exploratory/default Candidate budget: one sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 2, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler, disabled early stopping, and the 3,600-second trusted training timeout. No late-improving budget, Experiment Batch, full-data evidence, Post-Run Evaluation, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. The Run reports the effective `temporal_eligible_center` frame-selection policy while exposing only `abi_16ch_plus_sza` model inputs.
3. Parameter count remains within the 25,000,000 smoke ceiling and batch size 2 completes without Resource Failure retry.
4. Predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported.
6. As matched-control evidence, the Result is useful if it cleanly separates ABI-217's temporal architecture effect from temporal-eligible sample/data-policy effects, even if it trails mature single-frame candidates.

## Continuation and Hard Stop

Continue temporal-family development if ABI-217 clearly outperforms this control with finite, source-informative, nondegenerate behavior, or if the control shows that temporal-eligible centers remain a viable source-balanced subset for stronger temporal designs. Prefer a simpler temporal-difference front end if the control matches or beats ABI-217. Hard-stop this exact control branch if it fails contract validation, becomes non-finite, suffers a resource failure despite its compact single-frame design, or collapses persistently enough that it cannot answer the matched-control question.

Do not eliminate temporal modeling globally solely because ABI-218 or ABI-217 trails the mature ABI-202 incumbent; this is an early diagnostic branch.

## Fallback Next Decision

If ABI-218 fails, classify the failure and repair only if the matched-control question remains blocked by a narrow candidate bug. If it completes, write a Research Note comparing ABI-218 to ABI-217 before choosing between a simpler temporal-difference scout, a richer temporal attention/ConvGRU scout, or a broader non-temporal underexplored architecture family.
