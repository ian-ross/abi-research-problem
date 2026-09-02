# ABI-163 compact full-spectral BTD+SZA BiFPN line-fusion U-Net with focal-Tversky

## Hypothesis

ABI-163 is a **family-development continuation** of the ABI-162 compact BiFPN line-fusion branch. ABI-162 completed within the active budget and kept a clean improving trajectory through epoch 12, but its fixed-threshold operating point was precision-skewed and recall/connectivity remained below ABI-068, ABI-130, ABI-154, and ABI-160. Changing only the trusted primary loss from BCE-Dice to focal-Tversky should test whether the resource-feasible compact BiFPN architecture can recover thin-contrail recall while preserving its Google-side precision and non-degenerate behavior.

## Comparison Target

The primary family comparison target is ABI-162 (`run_20260901_142708_a2f6c9`): filtered Dice 0.3738, MIT filtered Dice 0.3576, Google filtered Dice 0.4133, filtered precision 0.4242, filtered recall 0.3342, filtered connectivity 0.3256, and final-epoch best trajectory under the capped 12-epoch budget. Secondary references are ABI-161 (`run_20260901_132157_1d849b`, full BiFPN resource failure with partial finite evidence), ABI-160 (`run_20260901_123418_da6b1e`, filtered Dice 0.3831), ABI-154 (`run_20260901_071026_32d3ec`, filtered Dice 0.3944), ABI-130 (`run_20260831_121006_7d24be`, filtered Dice 0.3953), and ABI-068 (`run_20260828_010836_4ccc77`, filtered Dice 0.3964). This is not a promotion claim; it is a bounded loss-axis continuation for a resource-feasible but immature branch.

## Expected Effect

Focal-Tversky should put more optimization pressure on missed positive contrail pixels than BCE-Dice, potentially increasing filtered recall and predicted-positive fraction on both Dataset Sources. A useful result would improve ABI-162's recall and aggregate/source filtered Dice without causing all-positive clutter or severe precision collapse. Because ABI-162 already completed under budget, the architecture/resource profile should remain comparable; the scientific question is whether BiFPN line fusion was under-recalled primarily because of the BCE-Dice loss axis rather than the compact feature topology.

## Implementation Sketch

`model.py` is intentionally inherited from ABI-162. The candidate uses provider-approved `abi_16ch_plus_sza` tensors only, normalizes GOES ABI channels 1-16, constructs deterministic thermal BTD planes from approved ABI channels, normalizes Solar Geometry Input and adds a cosine solar-geometry feature, and includes a small learned 1x1 spectral mixer. The architecture keeps the compact high-resolution line-evidence stem, four-scale residual encoder, positive normalized top-down/bottom-up BiFPN fusion, reused first-scale high-resolution evidence, and final horizontal/vertical line-context head. It returns `mask_logits` plus `centerline_logits` for the provider-derived Centerline auxiliary target. The manifest changes only `training.loss` from `bce_dice` to `focal_tversky` relative to ABI-162.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza`; longitude and latitude are neither requested nor reconstructed.
- Output form: `mask_logits` with provider-derived `centerline_logits` auxiliary output.
- Trusted primary loss: `focal_tversky`.
- Trusted auxiliary loss: `weighted_bce` for `centerline` at weight 0.02.
- Trusted sampling traversal: `combined_source_balanced`.
- Trusted augmentation: `random_mirroring`.
- Trusted optimizer/schedule: AdamW, learning rate 0.0003, `constant_lr` scheduler.
- Candidate code defines architecture only and does not implement data loading, target derivation, losses, metrics, thresholding, Artifact Filters, sampling policy, augmentation transforms, resource placement, or lifecycle behavior.

## Budget Requested

Use the active Workspace Configuration ceilings: 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, max 12 epochs, batch size 4, constant learning rate, disabled early stopping, 3,600-second Docker training timeout, 25M-parameter smoke ceiling, four fixed `first_n` predictions, and Harness-owned concurrency one. This ABI-162-derived branch should run sequentially.

## Success Criteria

- Static validation passes and smoke testing remains below the 25M-parameter ceiling.
- The Run completes without contract, resource, Harness, non-finite, or persistent all-negative/all-positive prediction-collapse failure.
- Relative to ABI-162, filtered recall and aggregate filtered Dice improve without catastrophic precision loss or Dataset Source-specific collapse.
- A diagnostically useful outcome can include recall recovery, source-balance improvement, a stronger final-epoch trajectory, or connectivity evidence, even if it does not beat the mature ABI-068/ABI-130/ABI-154 references.
- Raw-to-filtered differences do not indicate primary Artifact Filter dependence.

## Fallback/Next Decision

If ABI-163 fails for wall-clock resource reasons despite the unchanged compact architecture, stop this BiFPN branch under the current budget rather than attempting Candidate-owned scheduling. If focal-Tversky causes prediction collapse or a large precision/clutter regression, do not repeat this loss branch. If it improves ABI-162 recall/source balance but remains below the leading references, consider at most one further compact BiFPN continuation focused on lightweight non-suppressive line-continuity calibration; otherwise broaden to a different architecture or data/loss policy. No Capability Request is needed for this in-contract continuation.
