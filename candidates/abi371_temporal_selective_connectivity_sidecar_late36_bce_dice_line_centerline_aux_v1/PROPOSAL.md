# ABI-371 temporal selective connectivity sidecar late36

## Classification

Family-development continuation. ABI-371 is a mechanism-changing close continuation of ABI-350/ABI-370 within the provider-owned temporal-attention line-support family, not a full-data promotion claim.

## Hypothesis

ABI-350 established a compact high-precision temporal-attention pre-decoder line-support anchor on the temporal-eligible capped population, but its connectivity lagged ABI-223. ABI-370 showed that trusted `bce_dice_cldice` can raise connected-line continuity, but at the cost of broader predictions, lower precision, and worse aggregate/source Dice. ABI-371 tests whether an architecture-level selective connectivity sidecar can inject high-resolution line continuity into `mask_logits` only where decoder detail and supported skip features agree, preserving ABI-350's compactness while recovering part of ABI-370's connectivity gain.

## Comparison target

Primary comparison target: ABI-350 (`run_20260919_013306_9ca44e`) on the same trusted temporal-eligible capped setting. Secondary diagnostic comparators are ABI-370 (`run_20260920_180416_4cefdd`) for high-connectivity/low-precision behavior, ABI-369 (`run_20260920_155638_988238`) for augmentation sensitivity, and ABI-223 (`run_20260908_154531_8c7e2b`) as the mature temporal-attention diagnostic comparator.

## Expected effect

Expected success is not required to beat the whole-validation ABI-202 Result. Useful evidence would be:

- filtered Dice within about 0.005 of ABI-350 or better on the temporal-eligible capped population;
- filtered connectivity above ABI-350 and closer to ABI-223/ABI-370;
- no ABI-370-like footprint expansion, with filtered predicted-positive pixels remaining closer to ABI-350 than ABI-370;
- source-informative MIT and Google metrics without all-negative or all-positive collapse.

A clear regression in filtered Dice, precision, source balance, or compactness without connectivity gain would eliminate this exact sidecar design.

## Implementation sketch

Start from the ABI-350 temporal-attention U-Net scaffold:

- provider-owned `abi_16ch_plus_sza_temporal` input with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`;
- finite ABI/Solar Geometry Input normalization and ABI-channel-derived thermal BTD features;
- per-pixel temporal attention over previous, center, and next frames;
- U-Net encoder, ASPP bottleneck, and pre-decoder `PreDecoderLineSupportGate` modules on skip scales 2, 1, and 0;
- trusted `mask_logits`, `line_logits`, and `centerline_logits` outputs.

The mechanism change is a `SelectiveConnectivitySidecar` after final decoder refinement. It computes high-resolution orientation-line support from refined features, builds detail evidence from refined decoder, decoder-detail, and supported-skip features, predicts a soft selectivity gate, and adds a bounded `0.40 * gate * tanh(delta)` residual to the base mask logits. The residual is differentiable model logic, not thresholding, morphology, postprocessing, or an Artifact Filter.

## Contract Features Used

Candidate code defines only architecture over provider-advertised tensors. It does not implement data loading, temporal lookup, S3/NetCDF access, patch-cache reads, padding, missing-neighbor fallback, coordinates, Dataset Source identity, target derivation, loss definitions, metrics, Artifact Filters, thresholds, postprocessing, augmentation transforms, sampling policies, training loops, resource scheduling, downloads, persistence, or lifecycle behavior.

The manifest uses only trusted/allowlisted policies: `combined_source_balanced` sampling, `random_mirroring` augmentation, `bce_dice` primary loss, Line and Centerline `weighted_bce` auxiliary targets, AdamW, constant learning rate, batch size 2, and the default exploratory max epoch field. A candidate-local budget request asks the Harness for the approved late-improving 36-epoch budget with exploratory fallback if denied.

## Budget Requested

Request the approved `late_improving` budget. The request is justified because ABI-350, the close parent scaffold, selected its best checkpoint at epoch 33, ABI-369 selected at epoch 36, and ABI-370 selected at epoch 27; all are finite, resource-safe, non-collapsed, source-informative, and show that the temporal line-support family's useful behavior emerges beyond the 12-epoch exploratory ceiling. If the Harness denies the request, run under the exploratory budget and treat that bounded result as valid.

## Success Criteria

Continue this sidecar direction only if ABI-371 improves connectivity versus ABI-350 while preserving most of ABI-350's aggregate/source Dice and compact predicted-positive footprint. It is especially useful if filtered Dice is within about 0.005 of ABI-350 or better, filtered connectivity moves toward ABI-223/ABI-370, filtered predicted-positive pixels remain closer to ABI-350 than ABI-370, and MIT/Google source metrics remain nondegenerate and source-informative.

## Fallback Next Decision

If ABI-371 reproduces ABI-370's broad low-precision operating point or damages both Dice and connectivity, do not repeat the same sidecar. Broaden to a different architecture mechanism, such as an ABI-249-style C4/orientation prior with recall support, a source-balance-focused calibration head, or a modern lightweight backbone with explicit line-continuity evidence.
