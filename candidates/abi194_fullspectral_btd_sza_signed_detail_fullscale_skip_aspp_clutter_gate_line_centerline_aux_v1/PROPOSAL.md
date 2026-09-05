# ABI-194 full-spectral BTD+SZA signed-detail full-scale skip ASPP clutter-gate line+centerline auxiliary

## Hypothesis

ABI-181 remains the whole-validation aggregate filtered-Dice reference, while ABI-184 remains the precision/connectivity and negative-patch-discipline reference. ABI-192 showed that recall-oriented directional context can improve positive-patch median recall but worsens negative-patch clutter, and ABI-193 showed that adding a Boundary Target auxiliary head does not improve the signed-detail ASPP operating point. This family-development continuation tests whether an architecture-only learned clutter gate, trained only through trusted mask and provider-derived line/centerline losses, can reduce broad-context false positives while retaining the signed-detail full-scale skip ASPP overlap strengths.

## Comparison Target

Primary comparison target: ABI-181 Run `run_20260902_150611_cbbf35` / `eval_evalreq_abi181_wholeval_failure_buckets_v1` for aggregate whole-validation filtered Dice.

Secondary comparison targets: ABI-184 Run `run_20260902_213856_2c04ac` / `eval_evalreq_abi184_wholeval_failure_buckets_v1` for precision, connectivity, and negative-patch discipline; ABI-192 Run `run_20260903_085513_f395ad` / `eval_evalreq_abi192_wholeval_failure_buckets_v1` for recall and source balance; ABI-193 Run `run_20260903_115807_8c4be1` for the most recent auxiliary-policy negative control.

## Expected Effect

The learned clutter gate should contrast local signed detail and line-support features with broad smoothed context at mask resolution. If the hypothesis is correct, the capped exploratory run should preserve ABI-181/184-like filtered Dice while improving at least one of filtered precision, filtered predicted-positive fraction, MIT filtered Dice, or filtered contrail connectivity relative to ABI-193. A useful result may be a changed precision/recall operating point rather than an immediate new incumbent.

## Implementation Sketch

Start from the validated ABI-183/184 signed-detail full-scale skip ASPP lineage with approved `abi_16ch_plus_sza` inputs, normalized raw channels, deterministic ABI-channel-derived BTD planes, SZA scaling/cosine, signed local/mid-scale detail stem, residual encoder, ASPP context, full-scale skip fusion, and final line-aware refinement. Add `NegativeClutterGateRefinement` after the final line-aware refinement. The new module computes learned feature gates from the decoder features, local signed-detail residuals, and broad smoothed context, then applies a bounded residual feature calibration before the primary and auxiliary heads.

The candidate returns exactly `mask_logits`, `line_logits`, and `centerline_logits`. It does not implement thresholding, postprocessing, target derivation, custom losses, metrics, Artifact Filters, data loading, sampling, augmentation transforms, runtime downloads, filesystem persistence, or coordinate features.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`
- Input mode: `abi_16ch_plus_sza` only; longitude and latitude are not inputs and are not reconstructed.
- Output form: `mask_logits`
- Trusted auxiliary targets: `line` via `line_logits` at weight 0.01 and `centerline` via `centerline_logits` at weight 0.02
- Trusted primary loss: `bce_dice`
- Trusted sampling policy: `combined_source_balanced`
- Trusted augmentation policy: `random_mirroring`
- Optimizer/scheduler: AdamW with constant learning rate 0.0003
- Batch size and epoch settings remain at or below the active Workspace Configuration ceilings.

## Budget Requested

Exploratory/default budget only: 12 epochs, batch size 4, constant learning rate, disabled early stopping, and Harness-owned capped record selection. No `late_improving` budget is requested because this is a new architecture change and has not yet shown late-improving trajectory evidence.

## Success Criteria

Promotion-level success would require a finite, non-collapsed run that credibly ties or improves on ABI-181 capped filtered Dice while preserving source balance and not regressing precision/connectivity versus ABI-184. Family-development success is weaker: finite resource behavior under the 25M parameter ceiling, capped `val/filtered_dice` within roughly 0.01-0.02 of ABI-181/184/192, and at least one useful secondary tradeoff such as lower filtered predicted-positive fraction than ABI-192, better precision/connectivity than ABI-193, or improved MIT filtered Dice without collapse. If the best checkpoint occurs at epoch 11-12 with an improving or ambiguous non-collapsed trajectory, a later close-continuation budget request may be considered in a subsequent step.

## Fallback/Next Decision

If ABI-194 fails static validation or smoke testing because of a candidate bug, create a repair candidate preserving this hypothesis and comparison target. If it completes but is clearly below ABI-193 without a distinctive precision/connectivity/source-balance tradeoff, stop this exact clutter-gate branch and broaden to a different architecture/front-end or trusted data/loss policy. If it is finite and improves negative-clutter or connectivity but remains epoch-limited, consider a separate late-improving continuation request in a later Autonomy Step. If it materially improves capped metrics, request whole-validation failure-bucket evaluation before making any promotion claim.
