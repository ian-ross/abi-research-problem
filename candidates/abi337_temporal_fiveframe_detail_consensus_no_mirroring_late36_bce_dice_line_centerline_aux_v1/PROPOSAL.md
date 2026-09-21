# ABI-337 temporal five-frame detail-consensus no-mirroring late36

## Hypothesis

Random mirroring may be washing out physically meaningful GOES scan/illumination and temporal-advection orientation cues for the current best balanced temporal C4/detail-consensus branch. Disabling trusted mirroring while keeping ABI-324 architecture and all other training choices fixed may improve MIT-positive undercoverage and connected thin-line continuity at the fixed 0.5 threshold without adding Candidate-owned thresholds, postprocessing, data loading, losses, metrics, or Artifact Filters.

Classification: family-development data-policy continuation.

## Comparison Target

Primary comparison is ABI-324 (`run_20260916_184108_954ec7`), the strongest balanced recent five-frame temporal C4/detail-consensus comparator on the temporal-eligible validation population. Secondary context includes ABI-311 (`run_20260915_015552_1ac51f`) as the parent C4 line-state comparator, ABI-306 as compact high-precision temporal C4, ABI-309 as recall-heavy temporal C4, and ABI-223 as the temporal-attention connectivity comparator.

## Expected Effect

If mirrored samples are harming physically oriented line evidence, ABI-337 should preserve or improve ABI-324 temporal-eligible filtered Dice, MIT filtered Dice, positive-patch recall, and connectivity while keeping negative-patch clutter and filtered predicted-positive pixels close to ABI-324. If random mirroring is instead regularizing useful orientation invariance, ABI-337 may overfit orientation-specific clutter, lower Google/source balance, or reduce threshold stability.

## Implementation Sketch

Copy the ABI-324 model architecture unchanged: provider-owned five-frame `abi_16ch_plus_sza_temporal` input, per-frame ABI/Solar Geometry normalization and BTD features, temporal C4 persistence/contrast line-state stem, line-state injection into the encoder scales, ASPP bottleneck, high-resolution directional context, and detail-consensus stabilized mask/Line/Centerline heads. The only controlled change is the manifest-selected trusted `data.augmentation_policy: none` instead of `random_mirroring`.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal`
- `data.frame_selection_policy: temporal_eligible_center`
- `data.temporal_frame_offsets: [-2, -1, 0, 1, 2]`
- `data.sampling_policy: combined_source_balanced`
- `data.augmentation_policy: none`
- trusted primary loss `bce_dice`
- trusted Line and Centerline auxiliary targets with `weighted_bce`
- AdamW, constant LR, batch size 2, exploratory manifest max 12 epochs
- candidate-local `budget_request.yaml` for the approved `late_improving` 36-epoch close-continuation budget

No longitude/latitude, Dataset Source identity, candidate-side data loading, temporal lookup, padding, S3/NetCDF access, target derivation, augmentation implementation, custom loss, custom metric, Artifact Filter, thresholding, postprocessing, resource scheduling, or training loop is introduced.

## Budget Requested

Request the `late_improving` budget for 36 epochs. The request is justified by ABI-324 selecting its best checkpoint at epoch 27 and by ABI-311/ABI-324 evidence that this exact temporal C4/detail-consensus family is not fairly characterized at 12 epochs. If the Harness denies the request, run under the exploratory fallback and interpret the result as bounded exploratory evidence only.

## Success Criteria

ABI-337 is useful if it improves ABI-324 on temporal-eligible filtered Dice or MIT filtered Dice without materially increasing filtered predicted-positive pixels or negative-patch clutter, or if it preserves ABI-324-like Dice while improving connectivity/positive-patch undercoverage. A clean success would also maintain finite, source-informative, non-collapsed predictions and remain within the established resource profile.

## Fallback/Next Decision

If ABI-337 regresses aggregate/source Dice or expands clutter, treat no-mirroring as a negative data-policy control and keep ABI-324 as the balanced temporal C4 comparator. Do not repeat unchanged no-mirroring continuations. If ABI-337 is positive or mixed with a clear MIT/connectivity gain, request a temporal-eligible failure-bucket review to determine whether the improvement comes from positive-patch undercoverage, negative-patch clutter reduction, source balance, or threshold behavior.
