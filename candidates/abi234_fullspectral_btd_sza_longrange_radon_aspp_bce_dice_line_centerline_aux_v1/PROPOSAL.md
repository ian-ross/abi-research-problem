# ABI-234 full-spectral BTD+SZA long-range Radon ASPP decoder

## Hypothesis

A low-resolution differentiable Radon-style long-line accumulation bridge can improve thin-contrail continuity and source-balanced overlap beyond local orientation kernels by letting the decoder compare candidate line evidence over row, column, diagonal, and shallow/steep oriented paths. ABI-234 is a **family scout** for explicit long-range differentiable line accumulation. It uses the strong ABI-202 full-spectral BTD+SZA ASPP/detail decoder as a scaffold, but replaces the prior cross-scale directional-consensus bridge with a materially different low-resolution line-integral support module.

## Comparison Target

Primary comparison targets are ABI-202 (`run_20260904_043143_ee0005`) as the current whole-validation-tested single-frame frontier, ABI-228 as the prior temporal local orientation line-accumulation scout, and ABI-233 as the recent MoE local line-voting continuation. Same-budget interpretation should emphasize finite training, non-collapse, filtered Dice, filtered recall, contrail connectivity, and MIT/Google source-stratified behavior rather than requiring this first Radon-style scout to beat ABI-202 immediately.

## Expected Effect

The Radon bridge should add long-range continuity evidence that local strip/diagonal filters missed. Expected positive signs are higher filtered contrail connectivity, improved filtered Dice at similar predicted-positive fraction, and source-informative MIT/Google metrics without excessive dependence on Artifact Filters. A neutral or negative result is still useful if it separates explicit long-line support from earlier local orientation voting failures.

## Implementation Sketch

The model consumes provider-owned `abi_16ch_plus_sza` tensors only. It keeps normalized ABI channels, approved-channel BTD planes, Solar Geometry Input features, the signed-detail high-resolution stem, ASPP encoder/decoder, full-scale skip fusion, and trusted `mask_logits`, `line_logits`, and `centerline_logits` outputs. The architectural change is `DifferentiableRadonLineBridge`: it projects decoder/detail/stem/full-scale features, downsamples to 64x64, forms differentiable line-integral branches using global row/column means plus no-wrap directional shift sums for horizontal, vertical, diagonal, anti-diagonal, shallow, and steep orientations, softly weights orientations from the feature map, upsamples the support, and applies a bounded learned residual gate. It does not threshold, morphologically postprocess, filter artifacts, load data, define losses, or inspect coordinates.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza`.
- `output_form: mask_logits` with trusted Line and Centerline auxiliary targets.
- Trusted primary loss `bce_dice`; auxiliary `weighted_bce` with weights 0.01 and 0.02.
- Provider/Harness-owned `combined_source_balanced` sampling, `all_target_frames` frame selection, and `random_mirroring` augmentation.
- Constant learning rate scheduler, AdamW optimizer, batch size 4, and 12-epoch exploratory budget.
- No Candidate-owned data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, sampling policy implementation, augmentation transforms, coordinates, temporal cache access, downloads, training loops, or resource scheduling.

## Budget Requested

Exploratory/default budget: 12 epochs, batch size 4, constant learning rate 0.0003. No late-improving budget is requested for this first long-range Radon-style scout.

## Success Criteria

For promotion-style evidence, ABI-234 would need to approach or exceed ABI-202 on capped `val/filtered_dice` while maintaining source-balanced MIT/Google behavior and improving or tying connectivity. For family-development evidence, it is enough for the Run to complete finite/noncollapsed training, show source-informative predictions, and either improve connectivity over ABI-228/ABI-233 or reveal a distinct precision/recall/connectivity tradeoff worth a bounded follow-up.

## Fallback/Next Decision

If ABI-234 fails contract or smoke validation, repair only the implementation while preserving this hypothesis. If it completes but collapses or clearly underperforms local line-voting branches without a connectivity gain, stop this exact Radon bridge and broaden to another underexplored family. If it is finite and improves connectivity or source balance but remains below ABI-202, write a Research Note and consider one controlled continuation that adjusts how Radon support is fused, not a longer-budget rerun unless the best checkpoint lands near the epoch ceiling with an improving trajectory.
