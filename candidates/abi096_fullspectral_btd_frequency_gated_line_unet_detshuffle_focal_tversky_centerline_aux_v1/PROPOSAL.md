# ABI-096 full-spectral BTD frequency-gated line U-Net deterministic-shuffle focal-Tversky continuation

## Hypothesis

ABI-068 is the strongest local whole-validation-tested Candidate by filtered Dice, but its whole-validation diagnostic showed a recall-forward tradeoff: filtered Dice 0.3951 with precision 0.3996, recall 0.3907, connectivity 0.3868, and materially more negative-patch clutter than ABI-066. Many architecture-side suppressors, post-decoder gates, auxiliary-head stacks, and broader thin-line scouts have not improved this operating point. A different in-contract axis is the provider-owned training traversal policy rather than another candidate-owned architectural suppressor.

This is a **family-development continuation** and trusted data-policy probe for the ABI-068 full-spectral BTD frequency-gated line U-Net branch. The hypothesis is that changing only the manifest-selected sampling policy from `combined_source_balanced` to `deterministic_shuffle` will expose the model to a less aggressively source/positive-balanced stream of capped training records during the same 12-epoch budget. That may reduce negative-patch false-positive clutter and recover some ABI-066-like precision/connectivity while retaining enough ABI-068 recall through the trusted `focal_tversky` loss and the provider-derived Centerline Target auxiliary head.

## Comparison Target

Primary comparison target: ABI-068, `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, because it is the current strongest local capped and whole-validation-tested aggregate-Dice reference for this family.

Secondary comparison targets: ABI-066, `run_20260827_230540_bf4ce3`, because it remains the precision/connectivity-forward frequency-gated reference; ABI-085, `run_20260829_181201_01c5e7`, because it tested a training-policy learning-rate change on the same ABI-068 branch; and the ABI-068 whole-validation failure-bucket evaluation, which identified negative-patch clutter as the main remaining weakness. Canonical MCAST 2.1 remains the promotion context, but this Run is representative capped family-development evidence unless a later Harness-owned whole-validation diagnostic is requested.

## Expected Effect

The expected operating-profile shift is lower filtered predicted-positive fraction on negative patches and higher filtered precision/connectivity than ABI-068. Because deterministic traversal may reduce the effective positive/source balancing pressure, some recall loss is expected and acceptable if it is offset by cleaner predictions. A useful result would preserve source-stratified learning on both MIT and Google while moving the branch toward ABI-066 disciplined positive-area profile without returning to ABI-066 recall gap.

A negative result would show that ABI-068 sampling policy is not the main source of clutter, either because deterministic shuffle collapses recall/source balance or because it preserves the same false-positive burden while lowering aggregate Dice.

## Implementation Sketch

The candidate copies the ABI-068 model architecture unchanged: provider-approved `abi_16ch` input only, normalized raw ABI features, explicit thermal brightness-temperature-difference planes derived only from approved ABI channels, learned 1x1 spectral mixing, high/low spatial-frequency split stem, residual encoder/decoder, frequency-pyramid fusion, oriented line refinement, primary `mask_logits`, and provider-derived `centerline_logits`.

The manifest changes only the trusted provider/Harness-owned `data.sampling_policy` from `combined_source_balanced` to `deterministic_shuffle`. It keeps trusted `random_mirroring`, `focal_tversky`, AdamW, learning rate 0.0003, batch size 4, 12 epochs, constant learning-rate scheduler, disabled early stopping, and the Centerline Target auxiliary output with trusted `weighted_bce` weight 0.02. Candidate code does not implement sampling, data loading, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, training loops, filesystem writes, network calls, pretrained weights, or coordinate inputs.

## Contract Features Used

- Input mode: provider-approved `abi_16ch` only; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target emitted as `centerline_logits` with trusted `weighted_bce` weight 0.02.
- Primary loss: trusted `focal_tversky`.
- Data policy: provider-owned `deterministic_shuffle` sampling policy and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping under the active Workspace Configuration.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch, extra concurrency, GPU selection, candidate-owned sampling implementation, or full-data promotion evaluation is requested.

## Success Criteria

Useful continuation evidence would be any of:

- capped best `val/filtered_dice` within 0.015 of ABI-068 while improving filtered precision or connectivity and lowering filtered predicted-positive fraction;
- capped best `val/filtered_dice` within 0.01 of ABI-066 while improving recall over ABI-066 and preserving ABI-066-like precision/connectivity discipline;
- both MIT and Google filtered Dice above 0.35 with finite, non-collapsed predictions and a late-improving or stable trajectory;
- a clear diagnostic operating-profile shift toward lower false-positive burden without Dataset Source-specific collapse.

Hard stop evidence for this exact data-policy branch would be smoke failure, non-finite behavior, persistent all-negative/all-positive prediction collapse, either Dataset Source below about 0.30 filtered Dice, aggregate filtered Dice below 0.34 with no late improvement, or an ABI-082/084-like high-recall low-precision positive-area expansion.

## Fallback/Next Decision

If ABI-096 reduces false-positive burden while preserving ABI-068-like aggregate Dice and source balance, request a bounded whole-validation failure-bucket diagnostic before any promotion interpretation. If it collapses recall or source balance, retain `combined_source_balanced` as the preferred sampling policy for this branch and avoid further deterministic-shuffle repeats. If it is finite but only trades away Dice without a precision/connectivity gain, broaden to another trusted policy axis or materially different backbone rather than moving sampling, thresholding, loss implementation, Artifact Filters, target derivation, or data loading into Candidate code. If it fails contract validation or smoke testing, classify the failure and repair only if the original data-policy hypothesis is preserved.
