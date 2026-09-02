# ABI-069 full-spectral BTD frequency-gated line U-Net confidence-suppressor focal-Tversky continuation

## Hypothesis

This is a family-development continuation of the frequency-gated line U-Net branch. ABI-068 produced the strongest local whole-validation-tested filtered Dice so far by using trusted focal-Tversky loss, but the ABI-068 failure-bucket review showed higher negative-patch clutter and lower precision/connectivity than ABI-066. Adding a small differentiable confidence-suppressor mask head should preserve ABI-068's recall-forward focal-Tversky behavior while giving the model an architecture-side way to reduce low-confidence broad/speckle predictions.

## Comparison Target

Primary comparison target: ABI-068 (`run_20260828_010836_4ccc77`) because it is the current strongest whole-validation-tested local Candidate by aggregate filtered Dice.

Secondary operating-profile reference: ABI-066 (`run_20260827_230540_bf4ce3`) because it remains the precision/connectivity-forward reference within the same frequency-gated family.

## Expected Effect

Expected useful effect is a modest reduction in filtered predicted-positive fraction and negative-patch clutter relative to ABI-068 without collapsing recall or Dataset Source balance. A successful outcome would keep aggregate filtered Dice near or above ABI-068 while recovering part of ABI-066's precision/connectivity advantage.

## Implementation Sketch

Start from ABI-068's full-spectral BTD front end, frequency-split stem, high/low-frequency gated U-Net decoder, oriented frequency line refiner, focal-Tversky primary loss, random mirroring, and centerline auxiliary target weight 0.02.

Replace the direct 1x1 mask head with `ConfidenceSuppressorHead`, an in-network differentiable head that combines refined decoder features, a local high-frequency detail residual, and broad smoothed context. It predicts direct mask logits plus a learned residual and subtracts a small sigmoid confidence-suppression term initialized near zero. This is model architecture only, not thresholding or postprocessing.

## Contract Features Used

- `input_mode: abi_16ch`; no longitude or latitude inputs.
- Candidate-derived thermal BTD planes use only provider-approved ABI channels 1-16.
- `output_form: mask_logits` with optional trusted `centerline_logits` auxiliary output.
- Trusted primary loss: `focal_tversky`.
- Trusted auxiliary target: `centerline`, output `centerline_logits`, loss `weighted_bce`, weight `0.02`.
- Trusted provider/Harness data policies: `combined_source_balanced`, `all_target_frames`, and `random_mirroring`.
- Harness-owned optimizer, scheduler, metrics, Artifact Filters, sampling, validation, and lifecycle.

## Budget Requested

Run under the active bounded Workspace Configuration: 1,024 provider-selected train and validation records per Dataset Source/split, 12 epochs, batch size 4, constant learning rate 0.0003, disabled early stopping, A100 execution, 3,600-second Docker timeout, and the 25M-parameter smoke ceiling.

## Success Criteria

Treat this as capped family-development evidence, not promotion evidence. Strong continuation evidence would include all of:

- finite training and validation with no non-finite state or prediction collapse;
- best `val/filtered_dice` matching or exceeding ABI-068's capped 0.3964, or remaining within about 0.01 while improving filtered precision/connectivity or reducing predicted-positive burden;
- both MIT and Google filtered Dice above 0.35;
- filtered recall not materially below ABI-068 unless precision/connectivity gains are large enough to justify a follow-up;
- parameter count and resource profile inside current trusted limits.

If capped results are competitive or diagnostically superior, request a whole-validation failure-bucket evaluation before any promotion interpretation.

## Fallback/Next Decision

If the candidate collapses, fails contract/resource checks, or clearly underperforms ABI-068 without precision/connectivity/clutter benefit, do not repeat this exact suppressor head. Either return to ABI-068 as the aggregate-Dice reference and test a different lightweight precision-recovery mechanism, or broaden to a new architecture family if repeated frequency-gated continuations plateau.
