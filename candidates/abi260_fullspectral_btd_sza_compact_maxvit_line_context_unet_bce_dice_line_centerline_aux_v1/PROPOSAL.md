# ABI-260 compact MaxViT line-context U-Net

## Hypothesis

Recent search has concentrated on temporal attention/recurrent variants, C4 recall bridges, and local ASPP/detail mutations. ABI-253 showed that a compact U-NetFormer/line-memory branch can transfer to whole validation but remains recall/connectivity limited and expensive under late36. ABI-260 tests whether a different modern lightweight backbone, a compact MaxViT-style encoder that alternates local window attention with sparse global grid attention, can capture mesoscale cloud context and thin-line support without repeating the line-memory U-NetFormer branch. A lightweight line-context decoder should preserve contrail continuity while avoiding Candidate-owned thresholding, postprocessing, or Artifact Filters.

## Classification

Family scout. This is a materially different modern-backbone scout, not a promotion candidate and not a close continuation of ABI-253.

## Comparison Target

Primary capped comparison targets are ABI-253 (`run_20260911_171333_f0b603`, whole-validation-tested compact line-memory U-NetFormer), ABI-249 (`run_20260911_111909_dd7ef7`, high-precision C4 comparator), ABI-202 (`run_20260904_043143_ee0005`, current whole-validation aggregate frontier), and recent temporal references ABI-223/ABI-255/ABI-259. As a first MaxViT-style scout, success does not require beating ABI-202 immediately; useful evidence includes finite resource behavior, non-collapsed predictions, improved recall/connectivity balance versus other exploratory modern-backbone scouts, and a source-informative trajectory.

## Expected Effect

The expected effect is a better fixed-threshold balance between local detail, broader cloud context, and thin-line continuity than earlier standalone modern-backbone scouts. Local window attention should model short-range contrail texture and cloud edges, sparse grid attention should provide patch-scale context without a heavy full transformer, and the line-context decoder should keep connected line evidence available to the mask and auxiliary heads. A positive scout would reach the high-0.38/low-0.40 capped filtered-Dice neighborhood or show late-improving source-informative behavior while retaining bounded predicted-positive area and nontrivial connectivity.

## Implementation Sketch

The Candidate consumes only provider-owned `abi_16ch_plus_sza` tensors. The front end normalizes ABI channels 1-16, appends approved-channel thermal BTD planes, Solar Geometry Input transforms, and a learned 1x1 channel mixer. A signed-detail stem feeds three encoder stages. Each stage uses MBConv-like depthwise convolution plus local window attention and sparse grid attention over the 256x256 patch hierarchy. The decoder fuses multiscale skips with anisotropic line-context blocks and emits `mask_logits`, `line_logits`, and `centerline_logits` for trusted Line and Centerline auxiliary targets.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza`.
- `data.sampling_policy: combined_source_balanced`.
- `data.augmentation_policy: random_mirroring`.
- `training.loss: bce_dice`, `optimizer: adamw`, and `scheduler.policy: constant_lr`.
- Trusted Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02.
- Batch size 4 and default 12-epoch exploratory budget under Harness-owned resource limits.

Candidate code defines architecture only. It does not implement data loading, split logic, temporal lookup, target derivation, losses, metrics, Artifact Filters, threshold selection, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Budget Requested

Use the default exploratory budget only: 12 epochs, batch size 4, constant learning rate, disabled early stopping under Harness policy. No `late_improving` request is made for this first MaxViT-style scout. A longer budget would require a completed parent Run showing a finite non-collapsed trajectory with best checkpoint at or near the exploratory ceiling.

## Success Criteria

Continue the family only if the Run is finite and resource-safe, avoids all-negative/all-positive collapse, remains source-informative on MIT and Google, and either (a) reaches the high-0.38/low-0.40 capped filtered-Dice neighborhood with a better connectivity or recall tradeoff than exploratory modern-backbone references, or (b) shows a late-improving trajectory that justifies one bounded close continuation. Hard-stop this exact scout if it fails contract/smoke/resource checks, shows non-finite behavior, collapses predictions persistently, or plateaus well below the modern-backbone neighborhood without a distinct secondary strength.

## Fallback/Next Decision

If ABI-260 fails contract, smoke, finite-state, or resource validation due to Candidate code, create at most one narrow repair preserving the MaxViT-style scout hypothesis. If it is finite but clearly weaker than retained comparators, record it as modern-backbone scout evidence and broaden again rather than mutating local auxiliary heads. If it is finite and late-improving, consider one close continuation under the approved late-improving request path in a later Autonomy Step.
