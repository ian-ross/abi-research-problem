# ABI-332 temporal persistence/detail line-gate late36

## Classification

ABI-332 is a **family-development continuation** in the temporal architecture family. It is a late-improving continuation of ABI-331, not a promotion candidate and not a new architecture family.

## Hypothesis

ABI-331 showed that a cheap three-frame temporal persistence/detail line-gate can be resource-safe and cleaner than the prior lightweight temporal-attention/detail scout ABI-321. It improved over ABI-321 on aggregate filtered Dice, both source Dice scores, precision, recall, connectivity, and predicted-positive compactness, while avoiding the wall-clock failure mode of ABI-329/330 strip-token line mixing.

The unresolved question is whether ABI-331 was under-trained by the 12-epoch exploratory budget. Its selected checkpoint was epoch 12, with late aggregate/Google/precision improvement after noisy precision-recall oscillation. ABI-332 keeps the architecture unchanged and requests the approved late-improving budget to test the training-trajectory hypothesis under Harness-owned limits.

## Comparison Target

Primary local comparisons are:

- ABI-331, the direct exploratory parent and main family baseline.
- ABI-321, the weaker lightweight temporal-attention/detail sharpening comparator that ABI-331 superseded.
- ABI-319, a stronger three-frame shift-bank/C4 comparator.
- ABI-324, the strongest recent balanced five-frame temporal C4 aggregate/connectivity comparator.
- ABI-223, the older temporal-attention connectivity comparator.

This remains capped temporal-eligible feasibility evidence. It is not whole Working Validation Split promotion evidence against ABI-202/249.

## Expected Effect

If ABI-331 was budget-truncated, ABI-332 should improve filtered Dice and recall/connectivity balance after epoch 12 without the broad-footprint behavior seen in ABI-325. The desired signature is a finite, source-informative trajectory that raises true-positive temporal support at threshold 0.5 while preserving the compact filtered-positive footprint and negative-patch control observed in ABI-331.

A negative result would be a plateau, divergence, loss of compactness, or failure to close the gap to ABI-319/324/223 despite the longer budget.

## Implementation Sketch

- Reuse the ABI-331 architecture: provider-stacked `[-1, 0, 1]` ABI+Solar Geometry frames, per-frame ABI/BTD/Solar Geometry features, center-vs-neighbor temporal persistence/detail stem, compact U-Net decoder with ASPP context, and guarded line/detail logit head.
- Keep `input_mode: abi_16ch_plus_sza_temporal`, trusted `data.frame_selection_policy: temporal_eligible_center`, and trusted `data.temporal_frame_offsets: [-1, 0, 1]`.
- Keep BCE-Dice, Line and Centerline auxiliary targets, combined source-balanced sampling, random mirroring, AdamW, constant learning rate, and batch size 2.
- Add only a candidate-local `budget_request.yaml` requesting the approved `late_improving` 36-epoch budget from ABI-331 trajectory evidence.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Trusted frame selection: `data.frame_selection_policy: temporal_eligible_center`.
- Trusted temporal offsets: `[-1, 0, 1]`.
- Trusted sampling policy: `combined_source_balanced`.
- Trusted augmentation policy: `random_mirroring`.
- Trusted primary loss: `bce_dice`.
- Trusted auxiliary targets: Line Target (`line_logits`, weighted BCE 0.01) and Centerline Target (`centerline_logits`, weighted BCE 0.02).
- Trusted optimizer/scheduler: AdamW with constant learning rate 0.0003.
- Candidate-local budget request: `late_improving`, requested 36 epochs, fallback to exploratory budget if denied.

Candidate code must not own data loading, temporal lookup, S3/NetCDF access, sample selection, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, coordinate inputs, Dataset Source identity, downloads, resource scheduling, training loops, prediction retention, or lifecycle behavior.

## Budget Requested

Request the approved `late_improving` budget: 36 epochs and the Harness-owned late timeout, with batch size 2 and provider-selected temporal-eligible capped records. If the request is denied, run under the default exploratory budget and treat that bounded result as valid.

## Success Criteria

ABI-332 is useful if it:

1. completes without contract, numerical, resource, or lifecycle failure;
2. produces finite non-collapsed source-informative predictions;
3. improves meaningfully over ABI-331 in filtered Dice, MIT/Google balance, recall, connectivity, or predicted-positive compactness;
4. approaches ABI-319 or ABI-223 on aggregate/source/connectivity while remaining much cheaper than failed strip-token variants; or
5. shows a clear plateau/failure mode that justifies stopping this exact compact persistence/detail branch.

It does not need to beat ABI-324 or ABI-202 to be scientifically useful, but it should improve over ABI-331 to justify further continuation.

## Fallback/Next Decision

If ABI-332 fails for a candidate bug or contract issue, submit a narrow repair only if the hypothesis and comparison target remain intact. If it fails for resource reasons under the late budget, stop this exact continuation rather than requesting Candidate-owned scheduling. If it completes but does not improve over ABI-331 or remains materially below ABI-319/324/223 without a new secondary strength, record negative evidence and broaden to a different temporal attention/alignment, calibration, loss, or data-policy direction.
