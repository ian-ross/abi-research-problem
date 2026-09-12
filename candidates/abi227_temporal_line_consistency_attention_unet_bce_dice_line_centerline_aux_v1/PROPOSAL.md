# ABI-227 temporal line-consistency attention U-Net

## Hypothesis

ABI-223 showed that the compact three-frame temporal-attention family can become competitive under the approved late-improving budget, but it still trailed ABI-202 on capped recall, MIT Dice, and Contrail Connectivity. ABI-226 showed that simply widening the temporal window to five frames does not fix line continuity. A three-frame temporal-attention continuation with an architecture-internal, differentiable line-consistency context block should improve temporal-family connectivity and MIT/Google balance by strengthening line-shaped features only when center-frame and temporally attended evidence are coherent.

This is a **family-development continuation** within the temporal-attention family, not a promotion candidate. It is intended to test a specific architectural fix for ABI-223/226 continuity weaknesses before requesting any longer budget.

## Comparison Target

Primary comparison target: ABI-223 (`run_20260908_154531_8c7e2b`), the current capped temporal-family frontier, with best `val/filtered_dice` 0.419776 at epoch 36, filtered recall 0.370738, filtered connectivity 0.412427, MIT filtered Dice 0.398498, and Google filtered Dice 0.476764.

Exploratory-budget comparison targets: ABI-222 (`run_20260908_150315_9aea3f`, best 12-epoch filtered Dice 0.374329, connectivity 0.281396) and ABI-226 (`run_20260910_120441_916a03`, best 12-epoch filtered Dice 0.378604, connectivity 0.224851). ABI-218 remains the matched temporal-eligible single-frame control. ABI-202 remains mature single-frame frontier context only, not the required win condition for this scout.

## Expected Effect

The line-consistency block is expected to increase filtered Contrail Connectivity and source-stratified Dice relative to ABI-222 at the same 12-epoch budget, while avoiding ABI-226's five-frame connectivity regression. A useful result would preserve ABI-222/223's precision-oriented temporal attention while recovering recall through longer learned horizontal, vertical, and dilated line-context features gated by temporal-center agreement.

## Implementation Sketch

Start from the ABI-223 three-frame temporal-attention U-Net over provider-owned `[-1, 0, 1]` ABI+SZA frames. Keep the bounded finite ABI+BTD+SZA frame feature builder, shared frame projector, per-pixel temporal attention, signed/absolute change embedding, compact U-Net/ASPP decoder, and trusted Line/Centerline auxiliary outputs. Add a differentiable `TemporalLineConsistencyBlock` inside the temporal stem after attention/change fusion. The block learns anisotropic depthwise branches `(1x9)`, `(9x1)`, and dilated local context branches, projects their concatenated line context, and applies it as a gated residual using only center-frame embedding, temporal-attended embedding disagreement, and change embedding. This is model architecture logic, not thresholding, morphology, Artifact Filtering, or postprocessing.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal` with provider-owned temporal provisioning.
- `data.frame_selection_policy: temporal_eligible_center`.
- `data.temporal_frame_offsets: [-1, 0, 1]`.
- `data.sampling_policy: combined_source_balanced`.
- `data.augmentation_policy: random_mirroring`.
- `training.loss: bce_dice`, `optimizer: adamw`, `scheduler.policy: constant_lr`.
- Trusted Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02.

The Candidate code defines architecture only. It does not implement data loading, temporal lookup, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Budget Requested

Use the default exploratory budget: 12 epochs, batch size 2, constant learning rate 0.0003, disabled early stopping, and current Harness-owned sample/resource ceilings. No `late_improving` budget is requested for this first line-consistency variant because the added block changes the architecture and should be resource/trajectory-profiled first.

## Success Criteria

Treat ABI-227 as useful temporal-family evidence if it completes finite within resource limits and either exceeds ABI-222's 12-epoch filtered Dice by at least about 0.005, or materially improves filtered connectivity over ABI-222 without collapsing filtered Dice below ABI-219/220/221. Strong continuation evidence would include best epoch at or near 12, noncollapsed predicted-positive fractions, MIT and Google filtered Dice both above ABI-222, and connectivity approaching ABI-223's late36 level. A late-improving continuation would be justified only if the result is finite, source-informative, noncollapsed, and still improving near epoch 12.

## Fallback/Next Decision

If ABI-227 fails contract, smoke, or finite-state validation, create at most one narrow Repair Candidate preserving this line-consistency hypothesis. If it completes but does not beat ABI-222/226 and offers no connectivity or source-balance improvement, stop close temporal-attention stem tweaks and broaden to a materially different underexplored family such as rotation-aware line accumulation, compact modern attention/backbone designs, or spectral/SZA-gated mixture-of-experts. Do not request whole-validation diagnostics or late-improving budget unless capped evidence is strong enough to warrant it.
