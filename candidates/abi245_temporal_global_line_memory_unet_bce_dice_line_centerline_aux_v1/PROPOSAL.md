# ABI-245 temporal global line-memory U-Net

## Hypothesis

A full-resolution differentiable line-memory module can improve the temporal attention branch's thin-line continuity without depending on fixed local windows or candidate-owned postprocessing. ABI-244 showed that shifted windows improved overlap/recall over ABI-229 but did not recover connectivity; ABI-238 showed that temporal attention plus high-resolution directional context can approach the temporal frontier but still trails ABI-202/223 on connectedness. Broadcasting learned row, column, and coarse scene context over the high-resolution decoder features should let faint linear evidence be reinforced across long extents while retaining the center-anchored temporal-attention stem.

Classification: **family-development continuation** within the provider-owned temporal attention/line-continuity family. It is not a promotion candidate; it is a sequential bounded scout of a materially different continuity mechanism after shifted windows and recurrent line-state variants were connectivity-weak.

## Comparison Target

Primary comparison targets are ABI-244 (`run_20260911_072719_ade068`) for shifted-window local attention, ABI-238 (`run_20260911_004137_f54c45`) for temporal attention plus directional context, ABI-240 (`run_20260911_031326_43ed12`) for temporal line accumulation, ABI-223 (`run_20260908_154531_8c7e2b`) for the temporal late36 frontier, and ABI-202 (`run_20260904_043143_ee0005`) as the mature single-frame frontier context.

## Expected Effect

Expected benefits are higher filtered contrail connectivity than ABI-244/240 with filtered Dice remaining source-informative. The desired signature is not simply more predicted-positive area: filtered recall should improve or remain near ABI-244 without a large precision collapse, MIT and Google filtered Dice should both remain non-catastrophic, and filtered predicted-positive fraction should stay in the recent temporal-frontier range.

## Implementation Sketch

Start from the validated ABI-238 temporal-attention directional-context U-Net. Keep the provider-owned `[-1, 0, 1]` ABI+SZA tensor, finite per-frame ABI/SZA/BTD feature builder, center-anchored temporal attention/change stem, compact U-Net encoder/decoder, ASPP bottleneck, high-resolution directional context, and trusted Line/Centerline auxiliary heads. Add a `GlobalLineMemory` block after the high-resolution directional context. It computes differentiable row-wise, column-wise, and coarse pooled feature memories from candidate-visible decoder activations, broadcasts them back to 256x256, and uses a learned sigmoid gate to add memory evidence residually. No thresholds, morphology, Artifact Filters, or prediction postprocessing are implemented in Candidate code.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal`
- `data.frame_selection_policy: temporal_eligible_center`
- `data.temporal_frame_offsets: [-1, 0, 1]`
- `data.sampling_policy: combined_source_balanced`
- `data.augmentation_policy: random_mirroring`
- `training.loss: bce_dice`
- `training.optimizer: adamw`
- `training.scheduler.policy: constant_lr`
- `training.batch_size: 2`
- trusted Line and Centerline auxiliary targets with `weighted_bce`

Candidate code does not implement data loading, temporal lookup, cache reads, missing-frame fallback, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Budget Requested

Request the default exploratory budget: 12 epochs, batch size 2, constant learning rate 0.0003, and no `late_improving` budget request. This changes the continuity mechanism and should first produce sequential resource and trajectory evidence before any longer continuation is considered.

## Success Criteria

A strong result would exceed ABI-244's filtered Dice (0.392808) and connectivity (0.290859), or recover at least ABI-238-like connectivity (0.352239) while retaining noncollapsed source-informative MIT/Google filtered Dice. A particularly promising result would approach ABI-223/238 temporal late36 capped Dice without sacrificing precision. Continuation can also be justified if the best checkpoint is at epoch 12 with finite noncollapsed predictions and a clearly improving or ambiguous trajectory.

## Fallback/Next Decision

If static validation or smoke fails because of Candidate code, create a repair Candidate preserving this hypothesis. If it completes but collapses, becomes non-finite, or clearly underperforms ABI-244 on both filtered Dice and connectivity, stop this exact global-memory branch. If it is finite and improves either ABI-244 connectivity or primary metric without a predicted-positive blow-up, consider a late-improving continuation only if the approved criteria are met, or a tighter follow-up that couples the global memory more directly to line/centerline auxiliary features.
