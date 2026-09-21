# ABI-270 compact MoE orientation-consensus U-Net

## Classification

Family-development continuation. ABI-270 is a mechanism-changing continuation of the compact spectral/Solar Geometry Input MoE branch after ABI-269. It is not an unchanged late36 continuation: it returns to the exploratory budget and changes the architecture specifically to address ABI-269's weak selected-checkpoint connected-line continuity.

## Hypothesis

ABI-269 showed that compact spectral/SZA regime gating can raise capped Dice and recall, but its selected checkpoint lost connectivity versus ABI-268, ABI-265, ABI-249, and ABI-202. A conservative high-resolution orientation-consensus head on the resource-safe compact MoE body should preserve the useful spectral-regime gating while requiring multiple lightweight orientation branches to agree before line evidence influences the mask logits. This should improve connected thin-line continuity without broad recall boosting, candidate-owned thresholding, postprocessing, losses, metrics, Artifact Filters, data loading, coordinates, Dataset Source identity, or resource scheduling.

## Comparison target

Primary comparisons are ABI-269 (`run_20260912_121857_19f67d`) as the compact MoE late36 parent, ABI-268 (`run_20260912_113911_7a5f94`) as the exploratory compact MoE parent, ABI-265 (`run_20260912_065321_ceab64`) as the selective axial line-memory connectivity comparator, ABI-249 (`run_20260911_111909_dd7ef7`) as the high-precision C4 comparator, and ABI-202 (`run_20260904_043143_ee0005`) as the current whole-validation aggregate reference.

## Expected effect

Compared with ABI-269, ABI-270 is expected to trade some recall or Google-source lift for higher selected-checkpoint connectivity and more stable compact positive fraction. Compared with ABI-268, it should show whether replacing the simple final line head with explicit multi-orientation consensus recovers the connectivity that compact MoE lost during late-budget recall improvement. Because this is a mechanism-changing exploratory continuation, success does not require beating ABI-202 immediately.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`.
- Input mode: `abi_16ch_plus_sza`; no longitude/latitude, Dataset Source identity, scene identity, temporal lookup, or route/location priors.
- Output form: `mask_logits` plus trusted auxiliary `line_logits` and `centerline_logits`.
- Trusted loss/optimizer/scheduler choices: `bce_dice`, AdamW, constant learning rate.
- Trusted data choices: `combined_source_balanced`, `all_target_frames`, `random_mirroring`.
- Harness-owned budget/resource policy: exploratory 12 epochs, batch size 4, fixed GPU/resource policy, provider-owned metrics and Artifact Filters.

## Implementation sketch

- Reuse ABI-268/269's provider-approved ABI+SZA normalization, approved-channel BTD features, compact U-Net encoder/decoder, and downsampled local/dilated/line MoE blocks.
- Replace the final compact line head with a high-resolution orientation-consensus head containing horizontal, vertical, and two learned diagonal/broad directional depthwise branches.
- Average per-branch orientation logits and learn a disagreement-aware gate so orientation evidence is added conservatively, rather than as a broad recall bridge.
- Emit `mask_logits`, `line_logits`, and `centerline_logits` with only a small bounded line-logit contribution to the primary mask logits.

## Constraints

Candidate code remains architecture-only. It must not load data, select samples, derive targets, implement losses/metrics/Artifact Filters/thresholds/postprocessing/augmentation transforms, use longitude/latitude, use Dataset Source identity, discover temporal frames, download resources, write external artifacts, select GPUs, or manage lifecycle behavior.

## Budget

Exploratory/default budget: 12 epochs, batch size 4, constant learning rate, within the 25M parameter and 3,600-second exploratory ceilings. No late-improving budget is requested because the architecture is changed and needs fresh bounded resource/metric evidence.

## Success Criteria

Continue this compact MoE-plus-orientation-consensus branch only if ABI-270 completes within the exploratory wall-clock budget, remains finite and non-collapsed, and shows at least one of: connectivity above ABI-269/268 without a severe Dice collapse, improved precision/connectivity balance versus ABI-269, source-balanced filtered Dice near the compact MoE scout band, or a late improving trajectory that specifically supports a late-improving continuation. Low score alone is not elimination evidence if the connectivity mechanism is improving and source-informative.

## Fallback Next Decision

Hard stop this exact orientation-consensus head if it causes resource failure, smoke/contract failure, non-finite training, persistent prediction collapse, severe Dataset Source-specific collapse, or repeats ABI-266's broad-recall failure mode with low precision and low connectivity. If finite but mixed, use the result to decide between a more selective C4/orientation alignment variant, a temporal evidence-sharpening continuation, or broader frontier search.
