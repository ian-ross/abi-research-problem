# ABI-228 temporal center-anchored rotation-aware line accumulation U-Net

## Hypothesis

ABI-223 showed that provider-owned three-frame temporal context can become competitive, but ABI-226/227 showed that wider-window attention and a simple temporal-line consistency gate do not align line continuity with primary filtered Dice. A stronger center-frame anchor plus an architecture-internal rotation-aware line accumulation module should preserve ABI-223's useful temporal support while reducing neighbor-driven false support and improving thin-line continuity at the same exploratory budget.

This is a **family scout** for a materially different temporal/line formulation, not a promotion candidate. It broadens away from another ABI-223 stem tweak by changing how temporal support enters the model and by replacing ad-hoc horizontal/vertical line context with learned multi-orientation feature accumulation.

## Comparison Target

Primary family comparison targets are ABI-222 (`run_20260908_150315_9aea3f`, 12-epoch temporal-attention filtered Dice 0.374329, connectivity 0.281396), ABI-227 (`run_20260910_124920_f1b455`, line-consistency filtered Dice 0.370657, final connectivity 0.378301), and ABI-223 (`run_20260908_154531_8c7e2b`, late36 temporal frontier filtered Dice 0.419776). ABI-218 remains the matched temporal-eligible single-frame control. ABI-202 is mature whole-validation frontier context only.

## Expected Effect

The center-anchored stem should keep the center ABI Patch as the dominant evidence source while allowing learned temporal support and motion/change features to act as residual evidence. The rotation-aware accumulator should improve continuity for thin contrails whose orientation is not well captured by only horizontal/vertical context. A useful scout would improve ABI-222/227 same-budget filtered Dice or connectivity without collapsing precision/recall or either Dataset Source.

## Implementation Sketch

Use provider-owned `abi_16ch_plus_sza_temporal` with offsets `[-1, 0, 1]`. Reuse the finite ABI+BTD+SZA per-frame feature builder from the temporal branch. Project each frame with a shared compact residual block. The temporal stem forms learned neighbor support from the previous and next frame, constructs signed/absolute change features around the center frame, and fuses them as residual support around the center embedding rather than replacing the center embedding with temporal attention.

After center-anchored temporal fusion, add a differentiable `RotationAwareLineAccumulator`: horizontal, vertical, initialized diagonal, and initialized anti-diagonal depthwise line branches produce candidate line evidence; a learned softmax chooses orientation mixture per pixel; and a sigmoid residual gate blends accumulated line support into the feature map. This is model architecture only, not thresholding, morphology, Artifact Filtering, or postprocessing.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal`.
- `data.frame_selection_policy: temporal_eligible_center`.
- `data.temporal_frame_offsets: [-1, 0, 1]`.
- `data.sampling_policy: combined_source_balanced`.
- `data.augmentation_policy: random_mirroring`.
- `training.loss: bce_dice`, `optimizer: adamw`, `scheduler.policy: constant_lr`.
- Trusted Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02.

Candidate code defines architecture only and does not implement data loading, temporal lookup, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Budget Requested

Use the default exploratory budget: 12 epochs, batch size 2, constant learning rate 0.0003, disabled early stopping, and current Harness-owned sample/resource ceilings. No late-improving budget is requested because this is an unprofiled architecture scout.

## Success Criteria

Useful evidence requires finite completion within resource limits, noncollapsed predictions, and source-informative MIT/Google metrics. Continue the branch only if it beats ABI-222 or ABI-227 on same-budget filtered Dice, materially improves filtered connectivity while keeping filtered Dice near the temporal scout band, or shows a clearly late-improving nondegenerate trajectory. A later late-improving request would require best epoch near 12 plus stable precision/recall and source behavior.

## Fallback/Next Decision

If the candidate fails contract, smoke, or finite-state validation, create at most one narrow repair preserving the same center-anchored rotation-aware hypothesis. If it completes but is below ABI-222/226/227 with no continuity or source-balance advantage, treat this exact line-accumulation formulation as negative and broaden to another underexplored family such as compact window attention, spectral/SZA-gated mixture of experts, or a trusted evaluation request for the temporal frontier.
