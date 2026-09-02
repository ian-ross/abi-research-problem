# ABI-074 full-spectral BTD Laplacian-pyramid U-Net focal-Tversky centerline-aux scout

## Hypothesis

ABI-068 remains the current strongest local whole-validation-tested Candidate by aggregate filtered Dice, but its focal-Tversky recall-forward operating point has lower precision and Contrail Connectivity and more negative-patch clutter than ABI-066. Follow-up variants that stacked suppressor, residual, soft-evidence, or boundary auxiliary heads onto ABI-068 did not improve the trade-off, and the heavier steerable-ridge scout increased clutter. The next useful step is therefore to broaden away from output-head stacking and late suppressive/gated refiners while staying inside the same provider-owned ABI, loss, sampling, augmentation, target, metric, Artifact Filter, and lifecycle boundaries.

ABI-074 is a **family scout** for a full-spectral BTD Laplacian-pyramid U-Net. The hypothesis is that repeatedly exposing narrow, middle, and broad bandpass feature bands inside the backbone can preserve ABI-068's source-balanced focal-Tversky recall while recovering some ABI-066-style precision/connectivity through architecture-side multi-scale feature separation rather than candidate-owned postprocessing or additional auxiliary-head stacking.

## Comparison Target

Primary local comparison target: ABI-068 (`run_20260828_010836_4ccc77`), the current strongest local whole-validation-tested Candidate by aggregate filtered Dice and the focal-Tversky recall-forward reference.

Secondary operating-profile target: ABI-066 (`run_20260827_230540_bf4ce3`), retained as the precision/connectivity-forward reference, plus recent negative branch evidence from ABI-071, ABI-072, and ABI-073 showing that soft gates, dense ridge context, and boundary-auxiliary stacking did not improve ABI-068. Canonical MCAST 2.1 remains the broader promotion context; this capped scout is not a promotion claim.

## Expected Effect

The candidate should test whether explicit multi-scale bandpass feature fusion is a better broadening direction than adding more late heads or suppressive gates. Expected useful signals include:

- filtered Dice near ABI-068 while improving filtered precision, filtered Contrail Connectivity, or filtered predicted-positive fraction;
- less broad-clutter behavior than ABI-072 because Laplacian bands separate local ridge-like detail from smoother cloud context at each scale instead of densely inserting oriented context everywhere;
- better recall retention than ABI-066 because the trusted focal-Tversky primary loss and centerline auxiliary supervision are preserved;
- non-collapsed source-balanced behavior on both MIT and Google Dataset Sources under the representative cap.

## Implementation Sketch

Use provider-approved `abi_16ch` inputs only. The front end normalizes ABI channels 1-16, appends explicit thermal BTD planes derived only from those ABI channels, and appends a learned 1x1 channel mixture. The backbone is a compact GroupNorm/GELU U-Net. Its new `LaplacianBandBlock` computes smoothed feature maps at multiple kernel sizes and derives narrow, middle, and broad bandpass features (`x - smooth5`, `smooth5 - smooth13`, and `smooth13 - smooth31`). The block learns a soft per-pixel mixture across raw and bandpass branches and projects the mixture back into the residual feature stream. These blocks appear in the stem, encoder, bottleneck, decoder, and full-resolution pyramid-fusion block.

The output heads are direct `mask_logits` and provider-declared `centerline_logits`. No boundary head, confidence suppressor head, candidate-owned thresholding, postprocessing, Artifact Filter, target derivation, data loading, sampling, augmentation, metrics, training loop, data-root access, network access, runtime weight download, or pretrained weights are introduced.

## Contract Features Used

- `research_problem`: `goes_abi_contrail_segmentation`
- `input_mode`: provider-approved `abi_16ch`
- `output_form`: primary `mask_logits` with shape `[1, 256, 256]`
- `auxiliary_targets`: provider-derived `centerline` target emitted as `centerline_logits`, trusted `weighted_bce`, weight `0.02`
- `training.loss`: trusted `focal_tversky`
- `training.optimizer`: `adamw`
- `training.learning_rate`: `0.0003`
- `training.batch_size`: `4`
- `training.max_epochs`: `12`
- `training.scheduler.policy`: trusted `constant_lr`
- `data.sampling_policy`: provider/Harness-owned `combined_source_balanced`
- `data.frame_selection_policy`: provider/Harness-owned `all_target_frames`
- `data.augmentation_policy`: provider/Harness-owned `random_mirroring`

## Budget Requested

One sequential representative capped Run under the active Workspace Configuration: at most 1,024 records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, constant learning rate, disabled early stopping, four fixed `first_n` prediction artifacts, the configured 25M-parameter smoke ceiling, A100 GPU policy, and the configured 3,600-second Docker training timeout. No Experiment Batch, extra concurrency, GPU selection, data-policy change, or full-data promotion evaluation is requested.

## Success Criteria

Treat this as capped family-scout evidence, not full-data promotion evidence. The scout is successful enough for continued bounded development if it:

- completes finite smoke/training/validation without contract, resource, or non-finite failure;
- avoids persistent all-negative or all-positive prediction collapse;
- reaches aggregate best-validation `val/filtered_dice` within roughly 0.02 of ABI-068 while improving at least one of filtered precision, filtered Contrail Connectivity, or filtered predicted-positive fraction;
- keeps filtered recall at least about 0.36 and both MIT and Google filtered Dice above about 0.33; or
- shows a clearly improving late trajectory with a diagnostically different precision/recall/clutter profile even if it does not immediately beat ABI-068.

A stronger success signal would be capped filtered Dice matching or exceeding ABI-068 while moving precision/connectivity or negative-patch-clutter proxies back toward ABI-066.

Hard stop evidence for this exact branch would be contract/smoke failure, non-finite behavior, prediction collapse, aggregate filtered Dice below 0.34 without late improvement, a high-clutter low-connectivity profile like ABI-072, or materially worse source balance with no compensating precision/connectivity evidence.

## Fallback/Next Decision

If ABI-074 meaningfully improves the ABI-068 trade-off, request bounded whole-validation failure-bucket diagnostics before any promotion interpretation. If it is finite but weaker while showing a useful resource or operating-profile signal, consider one bounded family-development continuation that adjusts only architecture capacity or trusted allowlisted loss/auxiliary-weight choices. If it fails validation, smoke, or collapses, classify the failure and repair only if the original Laplacian-pyramid backbone hypothesis is preserved. If it is simply lower-Dice and higher-clutter with no source-balanced benefit, do not repeat this exact configuration unchanged; broaden to a different in-contract architecture or training-policy axis rather than moving provider-owned data policy, losses, evaluation, thresholding, or Artifact Filters into Candidate code.
