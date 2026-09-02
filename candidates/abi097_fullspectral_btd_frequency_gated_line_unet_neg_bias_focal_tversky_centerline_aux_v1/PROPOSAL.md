# ABI-097 full-spectral BTD frequency-gated line U-Net negative-bias focal-Tversky continuation

## Hypothesis

ABI-068 remains the strongest local whole-validation-tested Candidate by filtered Dice, but its full Working Validation Split diagnostic showed a recall-forward operating profile with materially more negative-patch clutter than ABI-066. Multiple add-on suppressors, auxiliary-head stacks, data-policy changes, and heavier architecture scouts have either reduced recall/source balance or failed to recover ABI-066-like precision and connectivity.

This is a **family-development continuation** for the ABI-068 full-spectral BTD frequency-gated line U-Net branch. The hypothesis is that part of ABI-068's false-positive burden may come from optimization/calibration dynamics around a neutral output-logit initialization under focal-Tversky. A gentle negative output-bias prior should make early broad positive regions less attractive while preserving the same learned spectral, BTD, high/low-frequency, and oriented-line feature path. Because the bias remains trainable and the loss/threshold are trusted Harness choices, this tests an architecture-initialization axis rather than candidate-owned thresholding or postprocessing.

## Comparison Target

Primary comparison target: ABI-068, `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, because it is the current strongest local capped and whole-validation-tested aggregate-Dice reference for this family.

Secondary comparison targets: ABI-066, `run_20260827_230540_bf4ce3`, because it remains the precision/connectivity-forward frequency-gated reference; ABI-078, `run_20260828_094949_ad2af0`, because it is the conservative BCE-Dice operating-point reference; ABI-085, `run_20260829_181201_01c5e7`, because it tested a lower-learning-rate calibration-like axis; and ABI-096, `run_20260830_021504_c112f8`, because deterministic shuffle improved precision/connectivity but sacrificed too much recall and Dice. Canonical MCAST 2.1 remains the promotion context, but this Run is representative capped family-development evidence unless a later Harness-owned whole-validation diagnostic is requested.

## Expected Effect

The expected effect is a smaller filtered predicted-positive fraction and improved filtered precision/connectivity relative to ABI-068, without the recall/source-balance loss seen in ABI-096. A useful result would keep ABI-068's source-balanced focal-Tversky learning while nudging the selected threshold-0.5 operating point toward ABI-066's cleaner positive-area discipline.

A negative result would show that output-logit initialization is not a useful lever: either the trainable bias is quickly overwritten and metrics remain ABI-068-like, or the conservative prior suppresses recall/MIT performance enough to repeat the ABI-096 tradeoff.

## Implementation Sketch

The candidate copies the ABI-068 model architecture: provider-approved `abi_16ch` input only, normalized raw ABI features, explicit thermal brightness-temperature-difference planes derived only from approved ABI channels, learned 1x1 spectral mixing, high/low spatial-frequency split stem, residual encoder/decoder, frequency-pyramid fusion, oriented line refinement, primary `mask_logits`, and provider-derived `centerline_logits`.

The controlled implementation change is in model initialization only: set the primary `mask_head` bias to `-0.75` and the `centerline_head` bias to `-1.25`. The weights and biases remain trainable. The manifest keeps trusted `combined_source_balanced` sampling, trusted `random_mirroring`, `focal_tversky`, AdamW, learning rate 0.0003, batch size 4, 12 epochs, constant learning-rate scheduler, disabled early stopping, and the Centerline Target auxiliary output with trusted `weighted_bce` weight 0.02. Candidate code does not implement sampling, data loading, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, training loops, filesystem writes, network calls, pretrained weights, or coordinate inputs.

## Contract Features Used

- Input mode: provider-approved `abi_16ch` only; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target emitted as `centerline_logits` with trusted `weighted_bce` weight 0.02.
- Primary loss: trusted `focal_tversky`.
- Data policy: provider-owned `combined_source_balanced` sampling policy and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping under the active Workspace Configuration.
- Architecture-owned initialization: trainable output-head biases initialized to mild negative values; no candidate-owned thresholding or postprocessing.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch, extra concurrency, GPU selection, candidate-owned sampling implementation, or full-data promotion evaluation is requested.

## Success Criteria

Useful continuation evidence would be any of:

- capped best `val/filtered_dice` within 0.01 of ABI-068 while improving filtered precision or connectivity and lowering filtered predicted-positive fraction;
- capped best `val/filtered_dice` above ABI-066 while retaining higher recall than ABI-066 and reducing the ABI-068 positive-area burden;
- both MIT and Google filtered Dice above 0.36 with finite, non-collapsed predictions and a stable or late-improving trajectory;
- a clear diagnostic shift toward lower negative-patch clutter without the recall/source-balance degradation observed in ABI-096.

Hard stop evidence for this exact initialization branch would be smoke failure, non-finite behavior, persistent all-negative/all-positive prediction collapse, either Dataset Source below about 0.32 filtered Dice, aggregate filtered Dice below 0.35 with no late improvement, or a high-recall low-precision positive-area expansion that repeats the recent failed suppressor/gate pattern.

## Fallback/Next Decision

If ABI-097 preserves ABI-068-like aggregate Dice while improving precision/connectivity or lowering predicted-positive burden, request a bounded whole-validation failure-bucket diagnostic before any promotion interpretation. If it suppresses recall or source balance, do not continue negative-bias tuning unchanged; return to ABI-068/066 as the family references and broaden to a materially different architecture or trusted policy axis. If it is finite but effectively indistinguishable from ABI-068, treat initialization as a weak lever and avoid additional bias-only repeats. If it fails contract validation or smoke testing, classify the failure and repair only if the original initialization hypothesis is preserved.
