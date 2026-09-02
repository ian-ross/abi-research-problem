# ABI-095 Repair Proposal: ultra-stable large-kernel line-context net

## Hypothesis

ABI-094 failed late in training with a Harness-recorded `candidate_bug`: `non_finite_training_state` in `gradient.front_end.learned_mixer.0.weight` at epoch 12. The large-kernel line-context family still lacks a clean finite scout because ABI-092 and ABI-094 both reached non-finite gradients and ABI-093 was a syntax-only smoke failure. ABI-095 tests whether the same full-spectral BTD large-kernel line-context hypothesis can be made finite by removing the observed learned front-end instability point and lowering update magnitude, while preserving the axial/local/dilated large-kernel encoder-decoder design.

Proposal class: **repair candidate / family scout repair**. This is not a promotion claim. It is a bounded stability repair intended to obtain interpretable representative capped evidence for the large-kernel line-context architecture family.

## Comparison Target

Primary comparison targets remain:

- ABI-068 / `run_20260828_010836_4ccc77`, the strongest capped frequency-gated focal-Tversky reference by `val/filtered_dice`.
- ABI-066 / `run_20260827_230540_bf4ce3`, the precision/connectivity-forward frequency-gated `bce_dice_cldice` reference.
- ABI-092 / `run_20260830_001308_e99407`, the original large-kernel line-context scout that failed with non-finite front-end gradients.
- ABI-094 / `run_20260830_002805_1d4d0f`, the syntax-repaired/stabilized large-kernel branch that still failed with non-finite front-end gradients at epoch 12.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-095 uses the representative capped policy and must not be interpreted as a full-data promotion result.

## Expected Effect

Removing the learned front-end mixer should eliminate the exact parameter group named in the ABI-092/ABI-094 non-finite gradient failures while retaining deterministic normalized ABI channels and physically motivated thermal BTD planes. Reducing base width, residual contribution scales, activation ranges, and learning rate should further reduce gradient amplification through the depthwise large-kernel branches.

If the repair works, the first expected outcome is finite completion and non-degenerate validation predictions. Scientifically useful evidence would be a large-kernel operating point near the ABI-068/066 band or a distinctive secondary profile: higher filtered precision/connectivity or a lower filtered predicted-positive fraction without Dataset Source collapse.

## Implementation Sketch

The model keeps ABI-094's provider-approved `abi_16ch` input, explicit BTD planes derived only from approved ABI channels, residual horizontal/vertical/local/dilated large-kernel stages, pyramid context, multi-scale line head, primary `mask_logits`, and provider-derived `centerline_logits` auxiliary output.

The stability changes are restricted to Candidate-owned architecture/training-policy choices:

- Replace the learned 1x1 front-end mixer with deterministic bounded normalized raw ABI channels plus bounded BTD planes.
- Reduce base width from 48 to 40 to lower activation and parameter pressure while preserving the same encoder-decoder topology.
- Reduce residual contribution scale in large-kernel blocks and pointwise feed-forward blocks to 0.1.
- Clamp normalized/BTD features and intermediate activations to bounded ranges as part of the model architecture.
- Lower AdamW learning rate from 0.0001 to 0.00005 under the trusted constant-LR scheduler.

The candidate does not implement data loading, split logic, sampling policy, augmentation transforms, target derivation, losses, metrics, thresholds, Artifact Filters, postprocessing, resource placement, filesystem probes, network access, runtime weight downloads, or longitude/latitude-derived features.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; candidate receives only ABI channels 1-16.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target via `centerline_logits`, trusted `weighted_bce`, weight 0.02.
- Sampling policy: provider/Harness-owned `combined_source_balanced`.
- Augmentation policy: trusted `random_mirroring`.
- Primary loss: trusted `focal_tversky`.
- Optimizer: `adamw`.
- Scheduler: `constant_lr`.
- Repair lineage: ABI-094 non-finite training failure classified as `candidate_bug`.

## Budget Requested

One sequential representative capped Run under the active Workspace Configuration: 1,024 provider-selected train and validation records per Dataset Source/split, batch size 4, 12 epochs, constant learning rate 0.00005, disabled early stopping, Docker training wall-clock timeout of 3,600 seconds, max four fixed `first_n` prediction artifacts, pinned A100 execution, and the 25M-parameter smoke budget.

## Success Criteria

Minimum repair criteria: static contract validation passes, syntax compilation passes, smoke test stays under the 25M-parameter budget, training completes finitely under the wall-clock limit, predictions are non-degenerate, and both MIT and Google capped validation filtered Dice remain above approximately 0.30.

Useful family-continuation criteria: at least one of the following holds without source-specific collapse: aggregate `val/filtered_dice` is within about 0.03 of ABI-068; filtered precision or Contrail Connectivity improves over ABI-068 at similar recall; filtered predicted-positive fraction is lower than ABI-068 with no larger than about 0.03 aggregate Dice loss; or the trajectory is finite and late-improving enough to justify one further bounded large-kernel continuation. Promotion-like interpretation would require later whole-validation diagnostics and human review, not this capped repair alone.

## Fallback/Next Decision

If ABI-095 still fails static validation, smoke, finite-state checks, or the 3,600-second timeout, stop this exact large-kernel line-context implementation and broaden to a different architecture or trusted policy axis rather than retrying or increasing Candidate-owned resource use. If it trains but shows persistent all-negative/all-positive collapse, a clear source-specific catastrophe, or filtered Dice far below the 0.30 scout floor, do not repeat this exact branch. If it is finite but below ABI-068 while providing distinctive precision/connectivity or positive-area evidence, write a Research Note and consider one bounded family-development continuation. If it is simply lower on aggregate Dice and secondary metrics, broaden the frontier.
