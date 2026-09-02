# ABI-080 — Frequency-gated line U-Net with multi-scale logit consensus

## Hypothesis

ABI-068 is the current strongest local whole-validation-tested Candidate by aggregate filtered Dice, but its gain over ABI-066 came with more negative-patch clutter and lower precision/connectivity. A lightweight multi-scale logit-consensus head on the ABI-068 decoder can reduce uncorroborated high-frequency false positives while preserving focal-Tversky recall: local detail, broad context, and oriented ridge branches each emit candidate mask logits, and an in-model soft gate fuses those logits before the trusted Harness threshold and metrics.

Classification: **family-development continuation** within the full-spectral BTD frequency-gated line U-Net family.

## Comparison Target

Primary comparison target: ABI-068 (`run_20260828_010836_4ccc77`), the full-spectral BTD frequency-gated line U-Net with trusted focal-Tversky loss and centerline auxiliary target.

Secondary comparison target: ABI-066 (`run_20260827_230540_bf4ce3`), the precision/connectivity-forward frequency-gated line U-Net with trusted BCE-Dice-clDice and centerline auxiliary target.

## Expected Effect

The consensus head should lower the filtered predicted-positive fraction and improve filtered precision/connectivity relative to ABI-068 while keeping MIT and Google filtered Dice non-catastrophic. It is not expected to be a final promotion claim from capped evidence; it is a bounded test of whether output-side multi-scale agreement is a better false-positive-control mechanism than the earlier late-refiner, suppressor, SZA, axial-neck, or nested-skip attempts.

## Implementation Sketch

Start from ABI-068's approved-channel front end, thermal BTD planes, learned 1x1 channel mixer, frequency-split stem, gated U-Net decoder, and centerline auxiliary output. Replace only the final single-convolution `mask_logits` head with `MultiScaleLogitConsensusHead`:

- a local-detail branch from high-pass full-resolution features;
- a broad-context branch with dilated convolutions;
- an oriented ridge branch using horizontal and vertical asymmetric convolutions;
- a softmax feature gate that blends the three branch logits, plus a small learned context-logit residual.

Candidate code remains architecture-only. It does not implement data loading, sampling, augmentation, loss, auxiliary-target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, external persistence, network access, or pretrained weight loading. It uses only provider-approved `abi_16ch` inputs and never receives longitude or latitude.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`
- Input mode: provider-approved `abi_16ch` only
- Primary output: `mask_logits`
- Auxiliary target: provider-derived `centerline` via `centerline_logits`, trusted `weighted_bce`, weight 0.02
- Trusted primary loss: `focal_tversky`
- Sampling: provider/Harness-owned `combined_source_balanced`
- Frame selection: `all_target_frames`
- Augmentation: trusted `random_mirroring`
- Optimizer: `adamw`
- Scheduler: `constant_lr`

## Budget Requested

Use the current generated Workspace Configuration limits: provider-selected 1,024 records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, constant learning rate 0.0003, disabled early stopping, fixed first-four prediction retention, 25M-parameter smoke ceiling, 3,600-second Docker training timeout, and Harness-owned sequential execution. The architecture adds only lightweight head modules to ABI-068's approximately 12.1M-parameter profile and is expected to remain below the smoke ceiling.

## Success Criteria

A successful capped continuation would satisfy all of:

- finite training and validation with no all-negative or all-positive prediction collapse;
- `val/filtered_dice` close to or above ABI-068, or at least above ABI-066 if precision/connectivity materially improve;
- both MIT and Google filtered Dice remain above 0.33;
- filtered precision or filtered connectivity improves meaningfully versus ABI-068 without driving filtered recall below ABI-066's recall-forward floor;
- filtered predicted-positive fraction trends toward ABI-066/ABI-078 rather than the permissive ABI-077/ABI-079 profile.

## Fallback Next Decision

If ABI-080 reduces clutter but loses too much recall/Dice, treat it as calibration evidence rather than promotion evidence and consider a simpler trusted-loss or auxiliary-weight comparison. If it remains permissive like ABI-079 or degrades both precision and recall, stop this exact consensus-head branch and broaden to a different architecture or training-policy frontier. Do not claim promotion from capped evidence alone.
