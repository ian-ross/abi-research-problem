# ABI-162 compact full-spectral BTD+SZA BiFPN line-fusion U-Net

## Hypothesis

ABI-161's bidirectional feature-pyramid line-fusion hypothesis produced finite partial training and useful mid-run validation signals, but failed as a Harness-recorded `resource_failure` when it exhausted the 3,600-second wall-clock budget near epoch 12. ABI-162 is a **family-development continuation** that preserves the BiFPN-style context-fusion hypothesis while reducing high-resolution compute enough to complete under the active budget.

## Comparison Target

Primary comparison targets are ABI-161 (`run_20260901_132157_1d849b`, resource failure with best observed partial filtered Dice 0.3727 at epoch 7 and later source/precision oscillation), ABI-160 (`run_20260901_123418_da6b1e`, filtered Dice 0.3831), ABI-154 (`run_20260901_071026_32d3ec`, filtered Dice 0.3944), ABI-130 (`run_20260831_121006_7d24be`, filtered Dice 0.3953), and ABI-068 (`run_20260828_010836_4ccc77`, filtered Dice 0.3964). The immediate objective is resource-feasible BiFPN-family evidence rather than a promotion claim.

## Expected Effect

The controlled capacity reduction should convert ABI-161 from a timeout into a complete capped Run while retaining its intended high-resolution thin-line and coarse-context fusion behavior. A useful result would complete finitely, avoid prediction collapse, recover ABI-161's early source-balanced Dice trajectory, and ideally approach or improve on ABI-160's filtered Dice or connectivity. Lower peak capacity may reduce ultimate precision, but the scout should test whether BiFPN fusion itself is worth one further continuation under the 12-epoch capped budget.

## Implementation Sketch

The candidate uses provider-approved `abi_16ch_plus_sza` tensors only. `model.py` normalizes ABI channels, builds deterministic thermal BTD planes from approved ABI channels, normalizes Solar Geometry Input, adds a cosine Solar Geometry feature, and retains a smaller learned 1x1 spectral mixture. Relative to ABI-161, it reduces learned front-end channels, encoder base width, and pyramid width; computes the expensive high-resolution line-evidence stem only once; reuses the first encoder features as high-resolution evidence instead of a second full-resolution line stem; simplifies each BiFPN fusion projection; and shortens the final horizontal/vertical line-context kernels. The model returns `mask_logits` plus `centerline_logits` for the provider-derived Centerline auxiliary target.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza`; longitude and latitude are neither requested nor reconstructed.
- Output form: `mask_logits` with provider-derived `centerline_logits` auxiliary output.
- Trusted primary loss: `bce_dice`.
- Trusted auxiliary loss: `weighted_bce` for `centerline` at weight 0.02.
- Trusted sampling traversal: `combined_source_balanced`.
- Trusted augmentation: `random_mirroring`.
- Trusted optimizer/schedule: AdamW, learning rate 0.0003, `constant_lr` scheduler.
- Candidate code defines architecture only and does not implement data loading, target derivation, losses, metrics, thresholding, Artifact Filters, sampling policy, augmentation transforms, resource placement, or lifecycle behavior.

## Budget Requested

Use the active Workspace Configuration ceilings: 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, max 12 epochs, batch size 4, constant learning rate, disabled early stopping, 3,600-second Docker training timeout, 25M-parameter smoke ceiling, four fixed `first_n` predictions, and Harness-owned concurrency one. This unprofiled compact BiFPN continuation should run sequentially.

## Success Criteria

- Static validation passes and smoke testing remains below the 25M-parameter ceiling.
- The Run completes without contract, resource, Harness, non-finite, or persistent all-negative/all-positive prediction-collapse failure.
- Best-validation `val/filtered_dice` is at least close to ABI-160 or clearly improves on the finite ABI-161 partial trajectory while preserving non-catastrophic MIT and Google filtered Dice.
- Filtered recall/connectivity or source balance provides diagnostically useful evidence beyond another local ASPP/detail refinement.
- Raw-to-filtered differences do not indicate primary Artifact Filter dependence.

## Fallback/Next Decision

If ABI-162 also fails for wall-clock resource reasons, stop the BiFPN branch under the current budget rather than requesting a Candidate-owned scheduling workaround. If it completes but remains well below ABI-160 with poor source balance or prediction collapse, do not continue this compact BiFPN path. If it completes and is balanced, improving, or connectivity-positive despite not beating ABI-068/ABI-130/ABI-154, consider one bounded BiFPN-family continuation such as a loss-axis change within trusted allowlists or a small precision-calibration head. No Capability Request is needed for this in-contract continuation.
