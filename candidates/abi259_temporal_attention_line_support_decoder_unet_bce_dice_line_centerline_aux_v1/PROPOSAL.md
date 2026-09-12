# ABI-259 temporal-attention line-support decoder U-Net

## Hypothesis

ABI-223 showed that provider-owned three-frame temporal attention can improve over the matched temporal-eligible single-frame control, but diagnostics found conservative fixed-threshold evidence and remaining positive-patch under-coverage. ABI-258's final-head calibration repair recovered some recall but lost precision/connectivity, so the next useful temporal step should preserve line evidence through the decoder rather than only alter the last head. ABI-259 is a family-development continuation that keeps ABI-223's temporal-attention stem and adds learned center-frame detail support plus oriented line-support blocks at decoder scales, aiming to raise connected contrail logits at the trusted 0.5 threshold without Candidate-owned thresholding or postprocessing.

## Comparison Target

The primary temporal-family comparison target is ABI-223 (`run_20260908_154531_8c7e2b`), the strongest temporal-attention comparator on the temporal-eligible population: late36 capped/diagnostic filtered Dice 0.4198, MIT 0.3985, Google 0.4768, precision 0.4838, recall 0.3707, and connectivity 0.4124. Recent mechanism-changing comparators include ABI-255 (`run_20260911_210922_27f346`, recurrent late36 filtered Dice 0.4173 but connectivity 0.2811), ABI-257 (`run_20260911_235337_128345`, oriented recurrent best 0.3751), and ABI-258 (`run_20260912_004429_1eee45`, dual-evidence calibration best 0.3882). ABI-202 remains the mature whole-validation frontier context, not the primary requirement for this exploratory family-development step.

## Expected Effect

The expected effect is better preservation of thin-line continuity and center-frame detail in the temporal decoder. Useful evidence would be a finite non-collapsed run that closes the gap to ABI-223 while improving at least one of fixed-threshold recall, MIT Dice, or connectivity without causing ABI-258-style precision loss or excess predicted-positive area. Because this is a new decoder mechanism, failure to beat ABI-202 would not by itself eliminate the branch; hard failure, non-finite behavior, persistent collapse, or a clearly worse ABI-223/255 comparison would be enough to stop this exact mechanism.

## Implementation Sketch

Start from ABI-223's provider-owned `[-1, 0, 1]` ABI+SZA temporal input path: bounded finite ABI/SZA/BTD per-frame features, shared frame projection, center-relative temporal attention, signed/absolute change features, and compact U-Net/ASPP decoding. Modify the decoder architecture by adding learnable anisotropic line-support blocks with horizontal, vertical, and dilated diagonal convolutional context after each upsample/skip fusion. Add a center-frame detail projection from the center ABI/SZA/BTD features into the final full-resolution refinement. The mask head fuses refined decoder features, final line-support features, and bounded learned line/centerline evidence logits; auxiliary Line and Centerline outputs remain trusted Harness targets.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal` with provider-owned temporal provisioning.
- `data.frame_selection_policy: temporal_eligible_center`.
- `data.temporal_frame_offsets: [-1, 0, 1]`.
- `data.sampling_policy: combined_source_balanced`.
- `data.augmentation_policy: random_mirroring`.
- `training.loss: bce_dice`, `optimizer: adamw`, and `scheduler.policy: constant_lr`.
- Trusted Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02.

Candidate code defines architecture only. It does not implement data loading, temporal lookup, cache access, missing-frame handling, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Budget Requested

Use the default exploratory budget: 12 epochs under the current Harness-owned sample, timeout, batch-size, scheduler, early-stopping, GPU, and artifact-retention limits. Keep batch size 2 because this is a materially changed temporal decoder and should run sequentially until resource behavior is observed. Do not request a late-improving budget until a completed exploratory Run shows finite late-improving or ambiguous trajectory evidence.

## Success Criteria

ABI-259 is useful if it completes finitely within resource limits and produces source-informative non-collapsed predictions. Strong evidence would be `val/filtered_dice` within about 0.01 of ABI-223 exploratory/late temporal frontier while improving either filtered recall, MIT filtered Dice, or filtered connectivity relative to recent temporal mechanism candidates, without dropping filtered precision below about 0.42 or inflating filtered predicted-positive fraction well above ABI-258's high-recall checkpoints. A best epoch near 12 with improving or ambiguous trajectory would justify considering a late36 continuation.

## Fallback/Next Decision

If ABI-259 fails contract, smoke, finite-state, or resource validation due to Candidate code, create at most one narrow repair preserving this line-support decoder hypothesis. If it completes but is clearly below ABI-223/255 with no secondary-metric strength, stop this exact decoder mechanism and broaden to another underexplored family such as differentiable line accumulation, compact motion/change streams, or non-temporal rotation-aware line networks. If it is finite and late-improving, consider a late-improving budget request; if it is near-frontier and source-informative, consider a trusted temporal-eligible failure-bucket Evaluation Request in a later Autonomy Step.
