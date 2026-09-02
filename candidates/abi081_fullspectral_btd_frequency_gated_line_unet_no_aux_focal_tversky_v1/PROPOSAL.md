# ABI-081 Full-spectral BTD frequency-gated line U-Net without auxiliary supervision

## Hypothesis

ABI-068 remains the strongest local frequency-gated line U-Net by capped aggregate filtered Dice and whole-validation diagnostic strength, but repeated output-side refiners, gates, extra auxiliary heads, SZA input, and consensus heads have not recovered a better precision/recall/connectivity trade-off. This family-development continuation tests whether the provider-derived centerline auxiliary head itself is constraining the focal-Tversky operating point. Removing auxiliary supervision may let the primary mask objective calibrate width and support directly, possibly preserving ABI-068's recall while reducing skeleton-biased errors or noisy auxiliary-gradient interaction.

Classification: **family-development continuation** within the full-spectral BTD frequency-gated line U-Net family.

## Comparison Target

Primary comparison is ABI-068 (`run_20260828_010836_4ccc77`), the same frequency-gated architecture with trusted focal-Tversky loss and centerline auxiliary weight 0.02. Secondary references are ABI-066 (`run_20260827_230540_bf4ce3`) as the precision/connectivity-forward branch and ABI-078 (`run_20260828_094949_ad2af0`) as the cleaner BCE-Dice operating-point branch.

## Expected Effect

Expected useful outcomes are either:

- a simpler focal-Tversky model that remains source-balanced and non-degenerate while approaching ABI-068 filtered Dice with improved precision, connectivity, or lower filtered predicted-positive fraction; or
- decisive evidence that the centerline auxiliary head is necessary for this branch's capped performance, allowing future work to stop no-auxiliary variants and broaden elsewhere.

This is not expected to be promotion-grade evidence by itself because it remains capped representative evidence.

## Implementation Sketch

Start from ABI-068's contract-compliant model architecture: provider-approved `abi_16ch` input, normalized raw ABI channels, ABI-channel-derived thermal BTD planes, learned 1x1 channel mixing, frequency-split stem, residual U-Net encoder/decoder, frequency-pyramid fusion, and oriented line refiner. Remove only the `centerline_logits` output head and the manifest `auxiliary_targets` entry. Return exactly the primary `mask_logits` output requested by the Harness.

## Contract Features Used

- `input_mode: abi_16ch` with no longitude/latitude inputs and no reconstructed coordinates.
- Harness/provider-owned combined source-balanced sampling and all-target-frame selection.
- Trusted `random_mirroring` augmentation.
- Trusted primary loss `focal_tversky`.
- No auxiliary targets requested.
- Constant learning rate scheduler, AdamW optimizer, batch size 4, and 12 epochs within current Workspace Configuration limits.
- Candidate source defines only model architecture and validates the Harness-supplied input/output specs.

## Budget Requested

Use the active bounded representative policy: 1,024 train and validation records per Dataset Source and Leakage-Safe Split, batch size 4, 12 epochs, constant learning rate 0.0003, fixed first-four prediction retention, A100 GPU placement, 25M-parameter smoke ceiling, and 3,600-second Docker training timeout. ABI-068-style resource use is already profiled, and this variant removes one 1x1 auxiliary head, so expected resource profile is no higher than ABI-068.

## Success Criteria

Treat the Run as useful family-development evidence if it completes finite and non-collapsed, both Dataset Sources achieve filtered Dice at least 0.33, and the operating point is diagnostically different from ABI-068. Strong continuation evidence requires at least one of:

- aggregate filtered Dice within 0.015 of ABI-068 while improving filtered precision, filtered connectivity, or filtered predicted-positive fraction;
- aggregate filtered Dice exceeding ABI-078 while avoiding a material MIT or Google source collapse;
- a late improving trajectory showing no hard plateau or divergence and a clear reason to revisit auxiliary supervision.

Promotion interpretation would require later whole-validation diagnostics and human review; this capped Run alone must not be promoted.

## Fallback/Next Decision

If the no-auxiliary model collapses, falls materially below ABI-078 without compensating secondary-metric gains, or shows clear optimization instability, stop this exact no-auxiliary focal-Tversky branch. If it ties ABI-068 on aggregate Dice or improves precision/connectivity enough to clarify the operating-point trade-off, request whole-validation failure-bucket diagnostics before promotion interpretation. If it is merely neutral, broaden away from auxiliary/refiner changes toward a materially different thin-line architecture or trusted training-policy capability request.
