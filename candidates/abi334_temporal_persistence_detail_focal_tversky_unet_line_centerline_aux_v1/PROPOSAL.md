# ABI-334 temporal persistence/detail focal-Tversky U-Net

## Classification

ABI-334 is a **family-development continuation** in the compact three-frame temporal persistence/detail line-gate branch. It is a trusted loss-policy diagnostic after ABI-331/332, not a promotion claim and not an unchanged late36 rerun.

## Hypothesis

ABI-331 showed that the compact temporal persistence/detail gate is resource-safe, cleaner than the lightweight ABI-321 attention/detail scout, and useful enough to justify bounded development. ABI-332 then showed the same branch was late-budget active and improved materially by epoch 36, but its remaining failure mode was still under-recall and insufficient connected thin-line support versus ABI-324/223.

ABI-334 tests a narrower question: whether trusted `focal_tversky` optimization can move this compact, high-precision branch toward better fixed-threshold recall and MIT/positive-patch coverage without changing Candidate-owned thresholds, losses, metrics, postprocessing, Artifact Filters, sampling, or data loading. The architecture is intentionally ABI-331-compatible so the comparison isolates the trusted primary loss choice.

## Comparison Target

Primary comparisons are ABI-331 as the exploratory `bce_dice` compact parent, ABI-332 as the late36 `bce_dice` compact comparator, ABI-333 as negative evidence for the exact orientation-consensus bridge, ABI-324 as the stronger five-frame temporal C4 balance comparator, and ABI-223 as the temporal-attention connectivity comparator. This run is temporal-eligible capped feasibility evidence only, not whole Working Validation Split promotion evidence against ABI-202/249.

## Expected Effect

A useful Result would raise filtered recall, MIT filtered Dice, or positive-patch coverage proxies relative to ABI-331 while avoiding ABI-309/325-style broad clutter and preserving finite source-informative predictions. Because focal-Tversky may trade precision for recall, success does not require beating ABI-332 or ABI-324 immediately; it should show whether the compact branch has a cleaner recall-accessible operating region under a trusted loss policy.

A negative Result would show that changing the allowlisted primary loss is insufficient and that future compact temporal work should use a genuinely new alignment, attention, data-policy, or line-continuity mechanism rather than another loss-only continuation.

## Implementation Sketch

- Use provider-approved `abi_16ch_plus_sza_temporal` input with trusted `data.frame_selection_policy: temporal_eligible_center` and offsets `[-1, 0, 1]`.
- Keep the ABI-331 architecture: approved-channel ABI normalization, ABI-channel BTD features, Solar Geometry Input features, temporal persistence/detail stem, compact U-Net encoder/decoder, ASPP context, and guarded line/detail head emitting `mask_logits`, `line_logits`, and `centerline_logits`.
- Change only the manifest-selected trusted primary loss from `bce_dice` to `focal_tversky` while keeping the trusted Line and Centerline weighted-BCE auxiliary targets.
- Do not implement any custom loss, threshold, calibration search, morphology, connected components, Artifact Filter, temporal lookup, data loading, sample selection, coordinate input, training loop, or resource scheduling in Candidate code.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Trusted frame selection: `data.frame_selection_policy: temporal_eligible_center`.
- Trusted temporal offsets: `[-1, 0, 1]`.
- Trusted sampling policy: `combined_source_balanced`.
- Trusted augmentation policy: `random_mirroring`.
- Trusted primary loss: `focal_tversky`.
- Trusted auxiliary targets: Line Target (`line_logits`, weighted BCE 0.01) and Centerline Target (`centerline_logits`, weighted BCE 0.02).
- Trusted optimizer/scheduler: AdamW with constant learning rate 0.0003.
- Candidate code owns only model architecture over provider-supplied tensors.

Candidate code must not own data loading, temporal lookup, S3/NetCDF access, sample selection, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, coordinate inputs, Dataset Source identity, downloads, resource scheduling, training loops, prediction retention, or lifecycle behavior.

## Budget Requested

Default exploratory budget: 12 epochs, batch size 2, provider-selected temporal-eligible capped records, and Harness-owned timeout/resource enforcement. No late-improving budget is requested for this first trusted focal-Tversky diagnostic on the compact branch. If the run is finite, non-collapsed, and best at the final exploratory epoch with a useful recall/source trajectory, a later close continuation may separately request the approved late-improving budget.

## Success Criteria

ABI-334 is worth further family development if it:

1. completes without contract, numerical, resource, or lifecycle failure;
2. produces finite non-collapsed source-informative predictions;
3. improves ABI-331's filtered recall, MIT filtered Dice, or source-balanced positive evidence without a disproportionate predicted-positive footprint increase; or
4. shows a late improving trajectory that makes a future `late_improving` focal-Tversky continuation scientifically justified.

It does not need to beat ABI-324/223/202 immediately to be scientifically useful as a trusted loss-policy diagnostic.

## Fallback/Next Decision

If ABI-334 fails for a candidate bug or contract issue, submit a narrow repair only if the fix preserves the one-factor trusted focal-Tversky comparison. If it fails for resource reasons, stop this exact loss-policy diagnostic and return to a cheaper or non-temporal direction. If it completes but simply broadens predictions with weak Dice/connectivity or clear precision collapse, record it as negative evidence for focal-Tversky on the compact persistence/detail branch and broaden away from loss-only compact temporal continuations.
