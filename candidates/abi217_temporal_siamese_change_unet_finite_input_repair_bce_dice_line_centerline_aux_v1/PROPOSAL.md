# ABI-217 Repair Proposal: temporal Siamese change U-Net finite-input repair

## Hypothesis

ABI-216 tested the first real temporal/change segmentation scout after ABI-215 proved provider-owned temporal provisioning. Run `run_20260908_114141_bf7ae7` failed with Harness-recorded `candidate_bug`: `non_finite_training_state` because `output.mask_logits` contained 65,536 non-finite values at train forward outputs in epoch 1 batch 134. The diagnostic counted one full 256 x 256 batch element as NaN while the other batch element remained finite, and the Run had already processed 268 training samples with finite losses and low A100 memory use. This points to a candidate numerical robustness defect around one temporal sample or feature transform, not a Resource Failure or evidence against the temporal/change hypothesis.

ABI-217 is a **Repair Candidate / temporal family-scout repair**. It preserves ABI-216's hypothesis that a compact shared-weight temporal encoder over provider-owned `[-1, 0, 1]` ABI+SZA frames can learn motion/change cues that are not available to the mature single-frame ABI-202 family. The repair only adds bounded finite feature handling to the candidate front end and finite activation bounds; it does not change temporal offsets, data policy, loss, auxiliary targets, sampling, augmentation, training budget, or comparison target.

## Comparison Target

The motivating failed implementation is ABI-216, Candidate `abi216_temporal_siamese_change_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260908_114141_bf7ae7`. ABI-217 should supply the missing finite representative capped temporal-scout Result.

Primary scientific context remains ABI-202 (`run_20260904_043143_ee0005`), the current best whole-validation-tested single-frame candidate. ABI-215 (`run_20260908_111425_74e4ec`) remains only the successful temporal-provisioning canary, not a segmentation-quality baseline. ABI-217 is not required to beat ABI-202 in this first repaired exploratory temporal run; it should demonstrate whether the temporal/change branch can train and produce nondegenerate source-stratified metrics.

## Expected Effect

The expected repair effect is finite training through the batch that failed ABI-216 and then through the 12-epoch exploratory budget. If the ABI-216 failure came from non-finite or extreme approved-channel values in one temporal frame, mapping normalized/BTD/SZA features to bounded neutral finite values before the encoder should prevent all-NaN per-sample logits while retaining the same temporal change architecture. Bounded finite internal activations should reduce outlier amplification without hiding non-finite parameter failures.

Scientifically useful evidence would be finite learning, non-collapsed predicted-positive fractions, MIT/Google source-informative metrics, and capped filtered Dice materially above the ABI-215 canary. Distinctive recall/connectivity behavior versus single-frame scouts would justify bounded temporal family development even if aggregate Dice trails ABI-202.

## Implementation Sketch

- Consume only the trusted 51-channel `abi_16ch_plus_sza_temporal` tensor with offsets `[-1, 0, 1]` and target offset `0`.
- Reshape into three ordered 17-channel frames; do not perform temporal lookup, cache reads, padding, missing-frame fallback, or sample selection.
- Preserve ABI-216's per-frame feature construction: normalized ABI channels 1-16, fixed ABI-channel BTD planes, scaled Solar Geometry Input, and cosine Solar Geometry Input.
- Repair the finite path by applying `torch.nan_to_num` and fixed clamps to derived candidate-visible feature planes: normalized ABI and BTD planes are bounded to `[-6, 6]`, and non-finite Solar Geometry Input is mapped to neutral zenith angle before clamping to `[0, 180]`.
- Preserve the ABI-216 shared-weight per-frame encoder, multi-scale temporal change fusers, ASPP bottleneck, U-Net decoder, and primary/auxiliary heads.
- Bound finite hidden activations in convolutional residual blocks to reduce outlier amplification while allowing Harness checks to catch any non-finite parameter/activation state that still occurs.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Temporal frame offsets: `[-1, 0, 1]`.
- Frame selection policy: `temporal_eligible_center`.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.02, AdamW, learning rate 0.0003, batch size 2, max epochs 12, constant learning-rate scheduler, and disabled early stopping.
- Repair lineage: original proposal/candidate ABI-216; motivating Run `run_20260908_114141_bf7ae7`; failure classification `candidate_bug`; original temporal/change hypothesis and comparison target preserved.
- Provider/Harness owns Leakage-Safe Split, temporal eligibility, temporal cache/provisioning, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, thresholding, postprocessing, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, temporal lookup, S3/NetCDF reads, cache access, frame padding/repair, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, external persistence, coordinates, Dataset Source identity, or route/location priors.

## Budget Requested

Use the exploratory/default Candidate budget: one sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 2, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler, disabled early stopping, and the 3,600-second trusted training timeout. No late-improving budget, Experiment Batch, full-data evidence, Post-Run Evaluation, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. The ABI-216 all-NaN `output.mask_logits` failure does not recur, including beyond epoch 1 batch 134.
3. Parameter count remains within the 25,000,000 smoke ceiling and batch size 2 completes without Resource Failure retry.
4. Predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported.
6. As temporal family-scout evidence, continue development if capped `val/filtered_dice` is materially above ABI-215, roughly reaches early single-frame scout range, shows improving/ambiguous late trajectory with nondegenerate predictions, or exhibits distinctive recall/connectivity/source behavior suggesting temporal information is useful.

## Continuation and Hard Stop

Continue temporal family development only if ABI-217 is finite, resource-safe, non-degenerate, and source-informative. Plausible next steps after a finite result include a compact continuation, a matched single-frame temporal-eligible control, a narrower temporal-difference front end, or a small temporal attention/ConvGRU scout under sequential execution.

Hard-stop this exact implementation if the non-finite output failure recurs despite finite feature handling, if a new persistent non-finite parameter/gradient/output failure appears, if resource use exceeds the trusted envelope, or if the finite result clearly plateaus/diverges with collapsed predictions and poor source behavior. Do not eliminate temporal modeling globally solely because this repaired first scout trails the mature ABI-202 incumbent.

## Fallback Next Decision

If this repair fails numerically again, classify the failure and either stop this exact architecture or propose a smaller/simpler temporal front end that keeps the provider-owned temporal contract. If it completes finite but underperforms, document the trajectory and source behavior before choosing between further temporal family development, a matched temporal-eligible single-frame control, or another underexplored architecture family. If it unexpectedly challenges the current frontier, request separately authorized whole-validation diagnostics rather than claiming promotion from capped evidence.
