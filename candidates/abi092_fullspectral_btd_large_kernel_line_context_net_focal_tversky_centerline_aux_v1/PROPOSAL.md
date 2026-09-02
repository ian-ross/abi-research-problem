# ABI-092 full-spectral BTD large-kernel line-context net

## Hypothesis

A depthwise large-kernel line-context encoder-decoder can improve the capped precision/connectivity tradeoff of the current full-spectral BTD line-model frontier. Instead of adding another output-side gate to ABI-068, the model gives every resolution separate local, horizontal, vertical, and dilated convolutional context so elongated contrail evidence can be accumulated in the backbone before final mask prediction.

Classification: **family scout**. This is a materially different architecture family from the frequency-gated line U-Net post-refinement branch, so the first Run is evidence for feasibility and operating profile rather than a promotion-grade verdict.

## Comparison Target

Primary comparison targets are:

- ABI-068 / `run_20260828_010836_4ccc77`, the current strongest capped frequency-gated focal-Tversky reference by `val/filtered_dice`.
- ABI-066 / `run_20260827_230540_bf4ce3`, the precision/connectivity-forward frequency-gated `bce_dice_cldice` reference.
- ABI-091 / `run_20260829_231700_96b245`, the recent negative low-learning-rate clDice continuation indicating that another small local frequency-gated tweak is lower priority.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context; this scout uses the representative capped policy and must not be interpreted as a full-data promotion result.

## Expected Effect

The expected effect is a non-collapsed operating point with source-balanced filtered Dice while reducing uncorroborated positive clutter. Relative to ABI-068, success would be either a near tie in aggregate filtered Dice with improved filtered precision/connectivity or a clear reduction in filtered predicted-positive fraction without a source-specific collapse. Relative to ABI-066, success would be a recall/aggregate-Dice improvement that does not sacrifice all of ABI-066's precision/connectivity advantage.

## Implementation Sketch

The candidate keeps the successful full-spectral BTD front end: normalized provider-approved ABI channels 1-16, explicit thermal brightness-temperature-difference planes derived only from those channels, and a learned 1x1 channel mixer. The architecture then uses a compact encoder-decoder built from `LargeKernelLineBlock` modules. Each block mixes depthwise local 3x3 context, long horizontal context, long vertical context, and dilated context, then applies pointwise channel mixing. A low-resolution pyramid context block adds multi-dilation and global pooled scene context without transformer-style memory cost. Decoder stages bilinearly upsample and fuse same-resolution encoder features, and a multi-scale line head combines final, intermediate, and shallow features before producing `mask_logits` and the trusted `centerline_logits` auxiliary output.

The code does not implement data loading, sampling, augmentation transforms, target derivation, loss functions, metrics, thresholds, Artifact Filters, postprocessing, resource placement, network access, runtime weight downloads, or longitude/latitude-derived features.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; candidate receives only ABI channels 1-16.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target via `centerline_logits`, trusted `weighted_bce`, weight 0.02.
- Sampling policy: provider/Harness-owned `combined_source_balanced`.
- Augmentation policy: trusted `random_mirroring`.
- Primary loss: trusted `focal_tversky`.
- Optimizer: `adamw`.
- Scheduler: `constant_lr`.

## Budget Requested

Use the active Workspace Configuration ceilings: provider-selected representative cap of 1,024 train and validation records per Dataset Source/split, batch size 4, 12 epochs, constant learning rate 0.0003, disabled early stopping, Docker training wall-clock timeout of 3,600 seconds, max four fixed `first_n` prediction artifacts, sequential execution under max parallel Runs 1, and the 25M-parameter smoke budget.

## Success Criteria

Minimum feasibility criteria: static contract validation passes, smoke test stays under the 25M-parameter budget, training completes finitely under the wall-clock limit, predictions are non-degenerate, and both MIT and Google capped validation filtered Dice remain above approximately 0.30.

Useful family-continuation criteria: at least one of the following holds without a source-specific collapse: aggregate `val/filtered_dice` is within about 0.02 of ABI-068; filtered precision or Contrail Connectivity improves over ABI-068 at similar recall; filtered predicted-positive fraction is lower than ABI-068 with no larger than about 0.02 aggregate Dice loss; or the trajectory is late-improving enough to justify one bounded continuation. Promotion-like interpretation would require later whole-validation diagnostics and human review, not this capped scout alone.

## Fallback/Next Decision

If the Run fails static validation or smoke due to a candidate bug, create a repair Candidate only if the hypothesis and comparison target can be preserved. If it trains but shows persistent all-negative/all-positive collapse, non-finite behavior, a clear source-specific catastrophe, or filtered Dice far below the 0.30 scout floor, stop this exact large-kernel line-context configuration. If it is finite but below ABI-068 while providing a distinctive precision/connectivity or positive-area benefit, write a Research Note and consider one bounded family-development continuation. If it is simply lower on aggregate Dice and secondary metrics, broaden to another architecture or trusted data/loss policy axis rather than adding more output-side gates.
