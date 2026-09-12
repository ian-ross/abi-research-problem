# ABI-230 five-frame temporal window-attention U-NetFormer

## Hypothesis

ABI-229 showed that compact local window attention improves the same-budget three-frame temporal-attention band, especially connectivity, while ABI-226 showed that the refreshed provider-owned temporal cache can train five-frame inputs and that a wider temporal window can slightly improve 12-epoch filtered Dice over ABI-222. Combining ABI-229's UNetFormer-style local window attention with ABI-226's allowlisted five-frame temporal window should better use near/far persistence and change evidence without weakening center-frame anchoring.

This is a **family-development continuation** of the temporal/window-attention family, not a promotion candidate. It is a controlled follow-up that changes the temporal window from `[-1, 0, 1]` to `[-2, -1, 0, 1, 2]` and expands the temporal stem's change features accordingly while keeping the lightweight window-attention encoder/decoder, loss, auxiliary targets, sampling, augmentation, learning rate, and exploratory budget aligned with ABI-229.

## Comparison Target

Primary comparison targets are ABI-229 (`run_20260910_141659_818da0`, three-frame window-attention filtered Dice 0.376958, connectivity 0.313635) and ABI-226 (`run_20260910_120441_916a03`, five-frame convolutional temporal-attention filtered Dice 0.378604, connectivity 0.224851). ABI-222 (`run_20260908_150315_9aea3f`, 12-epoch three-frame attention filtered Dice 0.374329), ABI-223 (`run_20260908_154531_8c7e2b`, late36 temporal frontier filtered Dice 0.419776), and ABI-202 (`run_20260904_043143_ee0005`, whole-validation frontier context) are secondary context.

## Expected Effect

The five-frame window should expose longer-lived contrail persistence and symmetric near/far change cues, while local self-attention should preserve ABI-229's ability to exchange thin-line evidence within patch-local cloud texture. A useful result would exceed ABI-229's filtered Dice or maintain similar filtered Dice with better connectivity/source balance, and should improve ABI-226's weak connectivity by replacing its convolution-only encoder/context path with local window attention.

## Implementation Sketch

Use provider-owned `abi_16ch_plus_sza_temporal` with offsets `[-2, -1, 0, 1, 2]` and `frame_selection_policy: temporal_eligible_center`. Each candidate-visible frame is normalized independently, augmented with ABI-channel-derived thermal BTD planes and Solar Geometry Input transforms, and projected through a shared per-frame front end. A center-anchored temporal stem computes learned per-pixel support over all five frames and near/far signed and absolute change features from provider-supplied channels only.

The fused stem feeds the compact ABI-229-style U-NetFormer: residual convolution blocks for stable local features, non-shifted 8x8 window self-attention in the stem, encoder stages, bottleneck, and selected decoder stages, and a small atrous/context bottleneck. The model returns `mask_logits`, `line_logits`, and `centerline_logits` only. Window attention and temporal fusion are differentiable architecture logic, not thresholding, morphology, Artifact Filtering, postprocessing, temporal lookup, or sample selection.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal`.
- `data.frame_selection_policy: temporal_eligible_center`.
- `data.temporal_frame_offsets: [-2, -1, 0, 1, 2]`.
- `data.sampling_policy: combined_source_balanced`.
- `data.augmentation_policy: random_mirroring`.
- `training.loss: bce_dice`, `optimizer: adamw`, `scheduler.policy: constant_lr`.
- Trusted Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02.

Candidate code defines architecture only and does not implement data loading, temporal lookup, cache access, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Budget Requested

Use the default exploratory budget: 12 epochs, batch size 2, constant learning rate 0.0003, disabled early stopping, current Harness-owned 1,024-per-source sample ceiling, 3,600-second exploratory timeout, A100 execution policy, and 25M-parameter smoke ceiling. No `late_improving` budget is requested because this is a new five-frame/window-attention combination whose trajectory is unknown.

## Success Criteria

Useful evidence requires finite completion within resource limits, noncollapsed predictions, and source-informative MIT/Google metrics. Continue the branch if it beats ABI-229 and ABI-226 on same-budget filtered Dice, materially improves ABI-229/226 connectivity or source balance while staying near the temporal scout band, or shows a clearly late-improving nondegenerate trajectory near epoch 12. A later late-improving request would require best epoch near the exploratory ceiling plus stable precision/recall, positive-fraction, and MIT/Google behavior.

## Fallback/Next Decision

If the candidate fails contract, smoke, finite-state, or resource validation, create at most one narrow repair preserving this five-frame window-attention hypothesis. If it completes below ABI-229/226 without connectivity, source-balance, or trajectory advantages, treat this exact combination as negative and broaden away from temporal window-attention toward another underexplored in-contract family such as spectral/SZA-gated mixture-of-experts or a materially different long-range differentiable Hough/Radon-style voting module.
