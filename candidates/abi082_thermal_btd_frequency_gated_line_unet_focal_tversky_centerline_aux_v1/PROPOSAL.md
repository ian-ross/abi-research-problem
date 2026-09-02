# ABI-082 Thermal BTD frequency-gated line U-Net

## Hypothesis

ABI-068 remains the strongest capped frequency-gated line U-Net reference by aggregate filtered Dice, while ABI-066 remains the precision/connectivity-forward reference. Recent attempts to alter auxiliary heads, late refiners, SZA input, and output-side consensus did not improve the trade-off. This family-development continuation changes the provider-approved input mode rather than adding another head: use only ABI thermal channels 7-16 plus thermal brightness-temperature-difference planes. Removing reflective channels may reduce illumination/source-specific clutter while preserving ice-cloud and split-window evidence relevant to contrails.

Classification: **family-development continuation** on the input/preprocessing axis of the full-spectral BTD frequency-gated line U-Net branch.

## Comparison Target

Primary comparison is ABI-068 (`run_20260828_010836_4ccc77`), which uses the same frequency-gated architecture pattern, trusted focal-Tversky loss, centerline auxiliary weight 0.02, and combined source-balanced sampling with full ABI channel input. Secondary references are ABI-066 (`run_20260827_230540_bf4ce3`) for precision/connectivity-forward behavior and ABI-081 (`run_20260829_143707_7c7d44`) for the recent no-auxiliary result.

## Expected Effect

Expected useful outcomes are either:

- a thermal-only operating point that remains non-degenerate and source-balanced while recovering some ABI-066-like precision, connectivity, or lower predicted-positive burden without a large aggregate Dice loss; or
- clear evidence that reflective channels are necessary for the current frequency-gated branch's capped performance, motivating broader architecture or policy exploration instead of more thermal-only variants.

This is capped representative family-development evidence, not full-data promotion evidence.

## Implementation Sketch

Start from ABI-068's contract-compliant frequency-gated line U-Net: learned channel mixing, explicit BTD planes, frequency-split stem, residual encoder/decoder, frequency-pyramid fusion, oriented line refiner, primary `mask_logits`, and provider-derived `centerline_logits`. The controlled change is to request `abi_thermal_10ch` input and normalize only ABI channels 7-16. Recompute the same thermal BTD concepts using zero-based indices within the 10-channel thermal tensor. Keep the trusted focal-Tversky primary loss and centerline auxiliary head unchanged.

## Contract Features Used

- `input_mode: abi_thermal_10ch` with no longitude/latitude inputs and no reconstructed coordinates.
- Harness/provider-owned combined source-balanced sampling and all-target-frame selection.
- Trusted `random_mirroring` augmentation.
- Trusted primary loss `focal_tversky`.
- Provider-derived `centerline` auxiliary target with trusted `weighted_bce` loss at weight 0.02.
- Constant learning-rate scheduler, AdamW optimizer, batch size 4, and 12 epochs within current Workspace Configuration limits.
- Candidate source defines only model architecture and validates the Harness-supplied input/output specs.

## Budget Requested

Use the active bounded representative policy: 1,024 train and validation records per Dataset Source and Leakage-Safe Split, batch size 4, 12 epochs, constant learning rate 0.0003, fixed first-four prediction retention, A100 GPU placement, 25M-parameter smoke ceiling, and 3,600-second Docker training timeout. The model removes six raw input channels from ABI-068 and keeps comparable downstream width, so expected resource use should remain within the ABI-068/081 envelope.

## Success Criteria

Treat the Run as useful family-development evidence if it completes finite and non-collapsed, both Dataset Sources achieve filtered Dice at least 0.33, and the operating point is diagnostically different from ABI-068. Strong continuation evidence requires at least one of:

- aggregate filtered Dice within 0.02 of ABI-068 while improving filtered precision, filtered connectivity, or filtered predicted-positive fraction;
- filtered Dice exceeding ABI-081 while avoiding material MIT or Google source imbalance;
- a late improving trajectory that suggests thermal-only evidence is viable under the current capped budget.

Promotion interpretation would require later whole-validation diagnostics and human review; this capped Run alone must not be promoted.

## Fallback/Next Decision

If ABI-082 collapses, falls materially below ABI-081 without compensating secondary-metric gains, or shows a clear source-specific failure, stop this exact thermal-only frequency-gated branch. If it approaches ABI-068 while improving precision/connectivity or positive-area control, request whole-validation diagnostics before promotion interpretation. If it is only neutral, broaden to a materially different architecture family or trusted policy axis rather than repeating thermal-only input unchanged.
