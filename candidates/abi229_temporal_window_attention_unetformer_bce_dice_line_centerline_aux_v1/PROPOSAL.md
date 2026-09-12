# ABI-229 temporal window-attention U-NetFormer

## Hypothesis

ABI-223 showed that provider-owned three-frame temporal context can become competitive with mature single-frame candidates after enough training, but ABI-226/227/228 did not improve the 12-epoch temporal scout band by adding wider temporal offsets or local line-specific gates. A compact UNetFormer-style temporal model with local window self-attention should capture patch-local cloud/contrail context and motion-consistent thin-line evidence more flexibly than convolution-only temporal stems, without moving sampling, temporal lookup, losses, metrics, or postprocessing into Candidate code.

This is a **family scout** for a modern lightweight segmentation backbone direction, not a promotion candidate. It broadens from the recent temporal line-module variants by replacing much of the convolutional encoder/context mixing with local window self-attention while retaining the same provider-owned three-frame input contract for comparability.

## Comparison Target

Primary family comparison targets are ABI-222 (`run_20260908_150315_9aea3f`, 12-epoch temporal-attention filtered Dice 0.374329, connectivity 0.281396), ABI-226 (`run_20260910_120441_916a03`, five-frame temporal-attention filtered Dice 0.378604), ABI-227 (`run_20260910_124920_f1b455`, line-consistency filtered Dice 0.370657), and ABI-228 (`run_20260910_133212_0380e1`, rotation line-accumulation filtered Dice 0.368554). ABI-223 (`run_20260908_154531_8c7e2b`, late36 filtered Dice 0.419776) is the temporal-family frontier; ABI-202 remains mature whole-validation frontier context only.

## Expected Effect

Local window attention should let each pixel exchange evidence with nearby cloud/line texture over fixed 8x8 neighborhoods at multiple scales, improving discrimination of persistent contrails from static geography, scan-like artifacts, and cloud edges while preserving thin-line recall. A useful scout would improve the same-budget temporal band on filtered Dice or show a connectivity/source-balance advantage that justifies bounded family development.

## Implementation Sketch

Use provider-owned `abi_16ch_plus_sza_temporal` with offsets `[-1, 0, 1]`. Reuse finite ABI normalization, thermal BTD features, and Solar Geometry Input transforms from prior temporal candidates. A center-anchored temporal stem projects the previous, center, and next frames, learns per-pixel temporal support, and builds signed/absolute change features from candidate-visible channels only.

Feed the fused temporal feature map to a compact hierarchical U-NetFormer: convolutional residual blocks provide stable local features; non-shifted 8x8 window self-attention blocks at the stem, encoder stages, bottleneck, and selected decoder stages provide lightweight spatial token mixing; a small atrous/context block remains at the bottleneck for multi-scale support. The model returns `mask_logits`, `line_logits`, and `centerline_logits`. Window attention is differentiable architecture logic only, not thresholding, morphology, Artifact Filtering, or postprocessing.

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

Useful evidence requires finite completion within resource limits, noncollapsed predictions, and source-informative MIT/Google metrics. Continue the branch only if it beats ABI-222/226/227/228 on same-budget filtered Dice, materially improves filtered connectivity or source balance while keeping filtered Dice near the temporal scout band, or shows a clearly late-improving nondegenerate trajectory. A later late-improving request would require best epoch near 12 plus stable precision/recall and source behavior.

## Fallback/Next Decision

If the candidate fails contract, smoke, finite-state, or resource validation, create at most one narrow repair preserving the temporal window-attention hypothesis. If it completes below the temporal scout band without connectivity, source-balance, or trajectory advantages, treat this exact compact window-attention formulation as negative and broaden to another underexplored family such as spectral/SZA-gated mixture-of-experts or a more explicit long-range differentiable Hough/Radon-style voting mechanism.
