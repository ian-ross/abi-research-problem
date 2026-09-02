# ABI-093 Repair Proposal: stable full-spectral BTD large-kernel line-context net

## Hypothesis

A numerically stabilized repair of ABI-092 can still test the same large-kernel line-context family-scout hypothesis: axial horizontal, vertical, local, and dilated convolutional context throughout the encoder-decoder may accumulate elongated contrail evidence before final mask prediction, improving the capped precision/connectivity tradeoff without candidate-owned thresholding or Artifact Filters.

Proposal class: **family scout repair**. ABI-092 (`run_20260830_001308_e99407`) failed during training with Harness-recorded `candidate_bug` / `non_finite_training_state`: `gradient.front_end.learned_mixer.0.weight` contained 256 NaN values at epoch 2 batch 212. ABI-093 preserves the comparison target, input mode, full-spectral BTD front end, centerline auxiliary target, focal-Tversky loss, source-balanced sampling, trusted augmentation, and large-kernel line-context architecture family, while reducing residual amplification and the AdamW learning rate to obtain finite evidence for the same scout question.

## Comparison Target

Primary comparison targets remain:

- ABI-068 / `run_20260828_010836_4ccc77`, the strongest capped frequency-gated focal-Tversky reference by `val/filtered_dice`.
- ABI-066 / `run_20260827_230540_bf4ce3`, the precision/connectivity-forward frequency-gated `bce_dice_cldice` reference.
- ABI-092 / `run_20260830_001308_e99407`, the failed large-kernel line-context scout whose non-finite training state this repair addresses.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-093 uses the representative capped policy and must not be interpreted as a full-data promotion result.

## Expected Effect

The expected first effect is finite, non-degenerate training for the ABI-092 large-kernel line-context hypothesis. Residual-scaled pointwise and line-context branches should reduce the activation/gradient amplification that likely propagated NaN gradients into the learned channel mixer. Clamping normalized raw and BTD feature planes to a bounded finite range should make the front end less sensitive to rare finite outliers while still using only provider-approved ABI channels 1-16 and BTDs derived from those channels. Lowering the constant learning rate to 0.0001 further reduces update size without changing the trusted optimizer, scheduler, loss, data, or metric ownership.

If the repair trains finitely, useful scientific evidence would be either a non-collapsed operating point near the ABI-068/066 band or a distinctive large-kernel profile: improved filtered precision/connectivity or lower filtered predicted-positive fraction without source-specific collapse.

## Implementation Sketch

The model keeps ABI-092's normalized full-spectral BTD front end over `abi_16ch`, explicit thermal BTD planes, learned 1x1 channel mixer, compact large-kernel encoder-decoder, low-resolution pyramid context, multi-scale line head, primary `mask_logits`, and provider-derived `centerline_logits` auxiliary output.

The repair changes only numerical stabilization inside the model and one allowlisted manifest choice:

- bounded normalized raw and BTD feature values with `torch.clamp(..., -8, 8)` inside the model front end;
- residual scale 0.2 on `LargeKernelLineBlock` branch fusion;
- residual scale 0.2 on pointwise feed-forward channel mixing;
- AdamW learning rate 0.0001 under the trusted constant-LR scheduler.

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

## Budget Requested

One sequential representative capped Run under the active Workspace Configuration: 1,024 provider-selected train and validation records per Dataset Source/split, batch size 4, 12 epochs, constant learning rate 0.0001, disabled early stopping, Docker training wall-clock timeout of 3,600 seconds, max four fixed `first_n` prediction artifacts, pinned A100 execution, and the 25M-parameter smoke budget.

## Success Criteria

Minimum repair criteria: static contract validation passes, smoke test stays under the 25M-parameter budget, training completes finitely under the wall-clock limit, predictions are non-degenerate, and both MIT and Google capped validation filtered Dice remain above approximately 0.30.

Useful family-continuation criteria: at least one of the following holds without a source-specific collapse: aggregate `val/filtered_dice` is within about 0.03 of ABI-068 after the stabilization change; filtered precision or Contrail Connectivity improves over ABI-068 at similar recall; filtered predicted-positive fraction is lower than ABI-068 with no larger than about 0.03 aggregate Dice loss; or the trajectory is late-improving enough to justify one bounded continuation. Promotion-like interpretation would require later whole-validation diagnostics and human review, not this capped scout repair alone.

## Fallback/Next Decision

If ABI-093 still fails static validation, smoke, or finite-state checks, stop this exact large-kernel line-context implementation and broaden to a different architecture or trusted policy axis rather than retrying or increasing Candidate-owned resource use. If it trains but shows persistent all-negative/all-positive collapse, non-finite behavior, a clear source-specific catastrophe, or filtered Dice far below the 0.30 scout floor, do not repeat this exact branch. If it is finite but below ABI-068 while providing a distinctive precision/connectivity or positive-area benefit, write a Research Note and consider one bounded family-development continuation. If it is simply lower on aggregate Dice and secondary metrics, broaden the frontier rather than adding more output-side gates.
