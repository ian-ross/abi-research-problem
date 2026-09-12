# ABI-268 compact spectral-regime MoE line U-Net

## Classification

Family-development continuation. ABI-268 continues the underexplored spectral/SZA-regime mixture-of-experts direction from ABI-267, but it is not a Repair Candidate for a candidate bug. ABI-267 failed with a Harness-recorded `resource_failure` before producing scientific metrics, so this proposal is a resource-aware compact continuation that preserves the MoE hypothesis while changing the architecture enough to fit the exploratory wall-clock budget.

## Hypothesis

ABI-267's full-resolution MoE blocks were too expensive, but the scientific idea remains plausible: local spectral/SZA regimes may need different feature transformations for thin contrails, clouds, and surface/scan artifacts. A compact U-Net that gates only a small number of mid/low-resolution local, dilated, and line-oriented experts from provider-approved ABI+SZA features may recover finite capped-validation evidence for the MoE family without using coordinates, Dataset Source identity, candidate-owned thresholding, postprocessing, losses, metrics, Artifact Filters, data loading, or sampling logic.

## Comparison target

Primary comparison targets are ABI-267 (`run_20260912_103414_825633`) for resource feasibility, ABI-265 (`run_20260912_065321_ceab64`) as the recent line-memory capped continuation, ABI-249 (`run_20260911_111909_dd7ef7`) as the high-precision C4 comparator, and ABI-202 (`run_20260904_043143_ee0005`) as the current whole-validation aggregate frontier. Because ABI-268 is the first resource-safe MoE attempt after a timeout, continuation decisions should first consider completion, finite non-collapsed predictions, source balance, and scout-band metrics rather than requiring an immediate frontier win.

## Expected effect

Compared with ABI-267, ABI-268 should reduce training/validation wall time by narrowing channels, removing high-resolution MoE blocks from the stem/head, and limiting expert mixtures to encoder/bottleneck plus one low-resolution decoder stage. If the MoE hypothesis is useful, the selected checkpoint should show finite MIT and Google filtered Dice, non-degenerate predicted-positive fractions, and either scout-band aggregate filtered Dice or a diagnostically useful precision/recall/connectivity/source-balance pattern.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`.
- Input mode: `abi_16ch_plus_sza`; no longitude/latitude, Dataset Source identity, scene identity, or route/location priors.
- Output form: `mask_logits` plus trusted auxiliary `line_logits` and `centerline_logits`.
- Trusted loss/optimizer/scheduler choices: `bce_dice`, AdamW, constant learning rate.
- Trusted data choices: `combined_source_balanced`, `all_target_frames`, `random_mirroring`.
- Harness-owned budget/resource policy: exploratory 12 epochs, batch size 4, fixed GPU/resource policy, provider-owned metrics and Artifact Filters.

## Implementation sketch

- Normalize ABI channels using fixed snapshot-scale constants; derive BTD planes only from approved ABI channels; include scaled SZA and cosine SZA.
- Use a compact U-Net with channel widths reduced versus ABI-267.
- Use `CompactRegimeMoEBlock` only at downsampled encoder/bottleneck scales and the first decoder stage. Each block softmax-gates three bounded experts: local depthwise separable convolution, dilated context, and horizontal/vertical line context.
- Keep high-resolution processing cheap with a detail stem and ordinary residual blocks, then emit `mask_logits`, `line_logits`, and `centerline_logits` from a lightweight line head.
- Select only trusted manifest options: source-balanced sampling, random mirroring, BCE-Dice primary loss, AdamW constant learning rate, batch size 4, and 12 exploratory epochs.

## Constraints

Candidate code remains architecture-only. It must not load data, select samples, derive targets, implement losses/metrics/Artifact Filters/thresholds/postprocessing/augmentation transforms, use longitude/latitude, use Dataset Source identity, discover temporal frames, download resources, write external artifacts, select GPUs, or manage lifecycle behavior.

## Budget

Exploratory/default budget: 12 epochs, batch size 4, constant learning rate, within the 25M parameter and 3,600-second exploratory ceilings. No late-improving budget is requested because ABI-267 did not complete and ABI-268 first needs resource-safe scout evidence.

## Success Criteria

Continue the MoE family if ABI-268 completes within the exploratory wall-clock budget, remains finite and non-collapsed, and shows one of: capped filtered Dice in the modern broad-scout band, useful MIT/Google source balance, improved precision/recall calibration relative to nearby broad scouts, useful connectivity, or a clearly improving trajectory suggesting one mechanism-changing continuation.

## Fallback Next Decision

Hard stop the compact MoE branch if ABI-268 again hits resource limits, has smoke/contract failure, non-finite training, persistent all-negative/all-positive collapse, severe source-specific collapse, or a clearly plateaued result far below comparable broad scouts without compensating diagnostic value. If it is finite but mixed, use one focused continuation only if diagnostics identify a specific MoE mechanism to preserve; otherwise broaden to another underexplored family.
