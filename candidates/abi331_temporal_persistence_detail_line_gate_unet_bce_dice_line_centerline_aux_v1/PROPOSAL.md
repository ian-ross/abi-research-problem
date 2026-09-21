# ABI-331 temporal persistence/detail line-gate U-Net

## Classification

ABI-331 is a **family-development continuation / mechanism-changing scout** in the temporal architecture family.

## Hypothesis

Recent temporal work shows two complementary failure modes. ABI-324 remains the best balanced local temporal C4 comparator, while ABI-325 can reduce positive-patch low-recall tails but broadens negative-patch clutter and loses connectivity. ABI-329/330 showed that strip-token line mixing can be finite and partially promising, but that exact hierarchy is resource-infeasible under the exploratory wall-clock budget.

ABI-331 tests whether a cheaper temporal persistence/detail mechanism can recover some connected true-positive support without full-resolution strip-token cost. The model uses only provider-stacked `[-1, 0, 1]` ABI+Solar Geometry frames. It builds center-frame spectral/BTD/Solar Geometry features, neighbor mean support, center-vs-neighbor temporal-difference features, and signed center-detail features. A guarded head adds a small positive mask-logit residual only when line, centerline, center-detail, and temporal-persistence evidence agree, with a small support-aware clutter veto when temporal support is weak.

## Comparison Target

Primary local comparison is the completed temporal family, especially:

- ABI-324 as the balanced five-frame temporal C4 aggregate/connectivity comparator.
- ABI-325 as the positive-tail recall diagnostic that became too broad.
- ABI-328 as negative-to-mixed soft-shift evidence.
- ABI-321 as a prior lightweight temporal-attention/detail sharpening scout.
- ABI-329/330 as resource-failed strip-token line-mixer evidence.
- ABI-223 as the older temporal-attention connectivity comparator.

This exploratory run is temporal-eligible capped feasibility evidence, not whole-validation promotion evidence against ABI-202/249.

## Expected Effect

Relative to ABI-321, ABI-331 should be more explicit about temporal persistence and negative-patch clutter control: it should avoid relying only on learned temporal attention and should condition the recall residual on agreement between temporal support and center-frame line/detail evidence. Relative to ABI-329/330, it should be much cheaper because it uses local temporal-difference blocks and a single high-resolution directional context head rather than multi-scale strip-token mixing.

The intended signature is finite, non-collapsed predictions with improved recall/connectivity balance over the lightweight temporal-attention scouts, while staying comfortably within the 3,600-second exploratory timeout.

## Implementation Sketch

- `input_mode: abi_16ch_plus_sza_temporal` with trusted `data.frame_selection_policy: temporal_eligible_center` and `data.temporal_frame_offsets: [-1, 0, 1]`.
- Per-frame feature builder uses only ABI channels 1-16 plus Solar Geometry Input; it normalizes approved channels, derives ABI-channel BTD planes, and excludes longitude/latitude.
- A compact temporal persistence stem combines center embedding, neighbor mean embedding, center-vs-neighbor differences, before/after absolute differences, and a transient guard.
- A U-Net encoder/decoder with ASPP context remains bounded and narrower than ABI-321 (`base=22`).
- A guarded line/detail head emits `mask_logits`, `line_logits`, and `centerline_logits`; the positive residual is architecture-internal and does not implement thresholding, morphology, postprocessing, metrics, losses, or Artifact Filters.

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

Default exploratory budget: 12 epochs, batch size 2, provider-selected temporal-eligible capped records, and Harness-owned timeout/resource enforcement. No late-improving budget is requested for this first mechanism-changing run.

## Success Criteria

ABI-331 is worth further family development if it:

1. completes without contract, numerical, resource, or lifecycle failure;
2. produces finite non-collapsed source-informative predictions;
3. improves over ABI-321 or nearby lightweight temporal scouts on a meaningful combination of filtered Dice, MIT filtered Dice, recall, connectivity, and predicted-positive compactness; or
4. shows a late improving trajectory suggesting that the temporal persistence/detail mechanism is under-trained rather than intrinsically weak.

It does not need to beat ABI-324/223/202 immediately to be scientifically useful as a mechanism-changing scout.

## Fallback/Next Decision

If ABI-331 fails for a candidate bug or contract issue, submit a narrow repair preserving this hypothesis. If it fails for resource reasons, do not narrow the same hierarchy repeatedly; classify it with ABI-329/330-style resource evidence and move to an even cheaper or non-temporal direction. If it completes but is lower than ABI-321 without a useful recall/connectivity/resource signal, record it as negative evidence for this exact persistence/detail line-gate mechanism and broaden away from lightweight gated temporal heads.
