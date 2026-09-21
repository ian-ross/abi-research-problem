# ABI-335 temporal calibrated dual-evidence line-gate U-Net

## Classification

ABI-335 is a **family-development continuation** in the compact temporal persistence/detail architecture family.

## Hypothesis

ABI-332 showed that the compact three-frame persistence/detail line-gate branch benefits from late training and can beat the older ABI-319 three-frame shift-bank/C4 scout, but it remains below ABI-324/326/328 and ABI-223 because connected thin-line support and source-balanced recall are insufficient. ABI-334 isolated a trusted-loss effect: focal-Tversky raises recall, but mainly by broadening predictions, lowering precision, damaging Google source balance, and weakening connectivity.

ABI-335 tests whether the recall support can be made architectural rather than loss-only. It keeps the ABI-331/332 provider-owned temporal inputs and compact encoder, returns to trusted `bce_dice`, and replaces the head with a calibrated dual-evidence line gate. The new head raises uncertain center-frame mask logits only when line context, centerline evidence, center-frame detail, and temporal persistence agree; it also learns a disagreement veto for support/detail mismatches. The intended effect is to recover part of ABI-334's recall without copying its broad low-precision footprint or losing ABI-332's cleaner connected-line behavior.

## Comparison Target

Primary comparisons are:

- ABI-332 as the best compact three-frame persistence/detail line-gate comparator.
- ABI-334 as the recall-biased focal-Tversky diagnostic whose broad footprint ABI-335 tries to avoid.
- ABI-333 as negative-to-mixed evidence for the prior orientation-consensus bridge.
- ABI-324/326/328 as stronger recent temporal C4/five-frame comparators.
- ABI-223 as the temporal-attention connectivity comparator.

This is capped temporal-eligible feasibility evidence only, not whole-validation promotion evidence against ABI-202/249.

## Expected Effect

Relative to ABI-331/333 at exploratory budget, ABI-335 should improve filtered Dice or recall while preserving better precision/connectivity than ABI-334. Relative to ABI-332, a 12-epoch ABI-335 run may not beat the late36 parent immediately, but should show whether architecture-level calibration moves the branch toward higher true-positive evidence without the high-recall/low-connectivity collapse seen under focal-Tversky.

The desired signature is finite non-collapsed predictions, lower filtered-positive footprint than ABI-334, precision materially above ABI-334, connectivity closer to ABI-331/332 than ABI-334, and a source-informative trajectory.

## Implementation Sketch

- Use `input_mode: abi_16ch_plus_sza_temporal` with trusted `data.frame_selection_policy: temporal_eligible_center` and `data.temporal_frame_offsets: [-1, 0, 1]`.
- Reuse ABI-331's per-frame ABI+Solar Geometry feature builder, ABI-channel BTD features, temporal persistence/detail stem, compact U-Net encoder/decoder, and high-resolution directional context.
- Replace the final head with a calibrated dual-evidence head. It computes mask, line, centerline, detail, and temporal-support logits, forms differentiable agreement maps from line/detail/centerline/support probabilities, applies a learned recall gate for uncertain logits, and applies a learned disagreement veto when support/detail evidence conflicts.
- Emit only `mask_logits`, `line_logits`, and `centerline_logits` for trusted Harness losses and metrics.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Trusted frame selection: `data.frame_selection_policy: temporal_eligible_center`.
- Trusted temporal offsets: `[-1, 0, 1]`.
- Trusted sampling policy: `combined_source_balanced`.
- Trusted augmentation policy: `random_mirroring`.
- Trusted primary loss: `bce_dice`.
- Trusted auxiliary targets: Line Target (`line_logits`, weighted BCE 0.01) and Centerline Target (`centerline_logits`, weighted BCE 0.02).
- Trusted optimizer/scheduler: AdamW with constant learning rate 0.0003.
- Candidate code owns only model architecture over provider-supplied tensors.

Candidate code must not own data loading, temporal lookup, S3/NetCDF access, sample selection, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, coordinate inputs, Dataset Source identity, downloads, resource scheduling, training loops, prediction retention, or lifecycle behavior.

## Budget Requested

Default exploratory budget: 12 epochs, batch size 2, provider-selected temporal-eligible capped records, and Harness-owned timeout/resource enforcement. No late-improving budget is requested for this mechanism-changing head scout.

## Success Criteria

ABI-335 is worth further family development if it:

1. completes without contract, numerical, resource, or lifecycle failure;
2. produces finite non-collapsed source-informative predictions;
3. improves over ABI-331 or ABI-333 on filtered Dice, recall/connectivity balance, or predicted-positive compactness;
4. avoids ABI-334's broad low-precision signature while recovering some recall; or
5. shows a late improving trajectory suggesting the calibrated head may merit an approved late-improving continuation.

It does not need to beat ABI-324/223 or the full-validation ABI-202/249 frontier immediately to be scientifically useful.

## Fallback/Next Decision

If ABI-335 fails for a candidate bug or contract issue, submit a narrow repair preserving this hypothesis. If it fails for resource reasons, stop pursuing heavier high-resolution calibration heads in this compact branch and broaden to a cheaper temporal alignment or single-frame calibration direction. If it completes but behaves like ABI-334 with broad low-precision weakly connected predictions, record negative evidence for this calibration head and broaden away from loss/head-only recall recovery.
