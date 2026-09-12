# ABI-255 temporal recurrent change-state U-Net late36

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-255, Candidate `abi255_temporal_recurrent_change_state_unet_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260911_210922_27f346`.

ABI-255 was the exact close continuation of ABI-242. It preserved the compact bidirectional ConvGRU-style temporal change-state architecture, provider-owned `abi_16ch_plus_sza_temporal` input with offsets `[-1, 0, 1]`, `frame_selection_policy: temporal_eligible_center`, trusted source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, constant learning rate, batch size 2, and trusted Line/Centerline auxiliary outputs. The only intended change was the approved `late_improving` budget request citing parent Run `run_20260911_055200_52c75f`. Candidate code remained architecture-only and did not implement temporal lookup, cache access, data loading, missing-frame handling, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Execution result

ABI-255 completed the approved late-improving 36-epoch budget without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Budget request: `late_improving`, approved; parent Run `run_20260911_055200_52c75f`.
- Input mode: `abi_16ch_plus_sza_temporal` with provider-owned temporal offsets `[-1, 0, 1]`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,157,779, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.07 / 3.32 GB.
- Training wall time: 2,991.0 s; validation wall time: 3,081.9 s; total Run wall time: 6,074.8 s.

This is valid finite/resource evidence for the recurrent temporal change-state branch. The late36 run remained comfortably inside the 10,800-second budget and used substantially less memory than recent attention-heavy or U-NetFormer late36 runs.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was the final epoch 36, so ABI-255 directly answers the ABI-242 budget-truncation question.

| Metric | ABI-255 best epoch 36 | ABI-242 parent epoch 12 | ABI-240 line-accum late36 | ABI-238 directional attention late36 | ABI-223 attention late36 | ABI-202 single-frame frontier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.417348 | 0.376521 | 0.414892 | 0.420235 | 0.419776 | 0.427570 |
| Raw Dice | 0.435656 | 0.391788 | 0.431959 | 0.438718 | 0.438487 | 0.442746 |
| Filtered precision | 0.468293 | 0.384767 | 0.436241 | 0.488730 | 0.483764 | 0.439467 |
| Filtered recall | 0.376400 | 0.368620 | 0.395534 | 0.368578 | 0.370738 | 0.416301 |
| Filtered connectivity | 0.281116 | 0.201293 | 0.264863 | 0.352239 | 0.412427 | 0.457773 |
| MIT filtered Dice | 0.400833 | 0.367296 | 0.397067 | 0.405383 | 0.398498 | 0.411992 |
| Google filtered Dice | 0.463143 | 0.398964 | 0.460659 | 0.460838 | 0.476764 | 0.468151 |
| Filtered predicted-positive fraction | 0.004155 | 0.004953 | 0.004687 | 0.003899 | 0.003962 | 0.003433 |

Relative to the ABI-242 parent, ABI-255 improves filtered Dice by about +0.0408, raw Dice by +0.0439, precision by +0.0835, connectivity by +0.0798, MIT filtered Dice by +0.0335, and Google filtered Dice by +0.0642 while preserving similar recall. The late-improving request was therefore justified: the recurrent change-state branch was materially truncated by the 12-epoch exploratory budget.

Relative to ABI-240, ABI-255 is slightly higher in filtered Dice, raw Dice, precision, connectivity, MIT Dice, and Google Dice, but lower in recall. Relative to ABI-223 and ABI-238, ABI-255 is a near-frontier temporal result on aggregate filtered Dice while retaining competitive MIT/Google behavior. Its main deficit remains connectivity: it trails ABI-238 by about -0.0711 and ABI-223 by about -0.1313 on filtered connectivity despite comparable overlap. Relative to ABI-202, ABI-255 is lower by about -0.0102 filtered Dice, -0.0399 recall, -0.1767 connectivity, -0.0112 MIT Dice, and -0.0050 Google Dice, while having higher precision.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.217697 | 0.223755 | 0.205672 | 0.203255 | 0.234349 | 0.147578 | 0.005960 |
| 6 | 0.331384 | 0.319709 | 0.359117 | 0.347050 | 0.317072 | 0.283191 | 0.004723 |
| 12 | 0.336681 | 0.342020 | 0.325029 | 0.270534 | 0.445643 | 0.149928 | 0.008516 |
| 18 | 0.380574 | 0.372110 | 0.400525 | 0.340963 | 0.430598 | 0.199287 | 0.006529 |
| 24 | 0.391999 | 0.369188 | 0.452931 | 0.508800 | 0.318812 | 0.327514 | 0.003239 |
| 29 | 0.394888 | 0.376249 | 0.442633 | 0.427492 | 0.366905 | 0.224266 | 0.004437 |
| 30 | 0.396778 | 0.382647 | 0.434386 | 0.457735 | 0.350148 | 0.242846 | 0.003955 |
| 34 | 0.390077 | 0.371143 | 0.438921 | 0.417315 | 0.366177 | 0.211997 | 0.004536 |
| 35 | 0.372830 | 0.352874 | 0.428416 | 0.575818 | 0.275656 | 0.450035 | 0.002475 |
| 36 | 0.417348 | 0.400833 | 0.463143 | 0.468293 | 0.376400 | 0.281116 | 0.004155 |

The trajectory is noisy but clearly late-improving. Epoch 12 had high recall but poor precision and connectivity, epoch 24 shifted to a compact high-precision operating point, epoch 35 briefly produced very high precision/connectivity with severe recall loss, and epoch 36 reached the best aggregate source-balanced compromise. Because the selected checkpoint is the final late-budget epoch, the recurrent change-state mechanism may still have unresolved training-time dynamics, but the current approved late36 budget is already the bounded close-continuation answer.

## Interpretation

Classify ABI-255 as successful late-budget family-development evidence for compact recurrent temporal change modeling. It validates that a bidirectional ConvGRU-style state over provider-owned neighboring frames can mature from a mid-tier exploratory result into a near-frontier temporal capped Result without collapse, excessive resource use, or source-specific failure.

The result does not supersede the strongest temporal attention comparators or the ABI-202 single-frame whole-validation frontier. ABI-255's overlap is close to ABI-223/238, and its MIT/Google split is competitive, but the recurrent state has not learned line continuity as effectively as attention/line-accumulation variants. The connectivity deficit is the key scientific finding: recurrent temporal evidence improves classification/coverage but does not by itself preserve thin contrail continuity.

Because ABI-255 is evaluated on the temporal-eligible validation population rather than the full 3,088-sample Working Validation Split, this remains capped temporal-family feasibility evidence. It should not be treated as promotion evidence or as a whole-validation replacement for ABI-202.

## Decision

Do not promote ABI-255 from capped temporal-eligible evidence alone. Do not submit another unchanged late36 continuation of the exact ABI-242/255 recurrent change-state branch; the close-continuation question has been answered positively, but the remaining weakness is mechanism-level connectivity rather than simply insufficient epochs.

Retain ABI-255 as the recurrent temporal comparator alongside ABI-223/238 attention comparators. A future Autonomy Step may reasonably request trusted failure-bucket/threshold diagnostics for ABI-255 to determine whether its lower-confidence temporal evidence and epoch-35 connectivity behavior reflect useful line continuity or over-pruned recall. If proposing another Candidate instead, it should be mechanism-changing: add a line-aware recurrent state, centerline-preserving temporal decoder, or recall-preserving calibration/evidence-raising head over temporal features without Candidate-owned thresholding, postprocessing, losses, metrics, data loading, or temporal selection.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_210922_27f346/candidate/PROPOSAL.md`
- `run_20260911_210922_27f346/candidate/README.md`
- `run_20260911_210922_27f346/candidate/manifest.yaml`
- `run_20260911_210922_27f346/candidate/budget_request.yaml`
- `run_20260911_210922_27f346/resolved_manifest.yaml`
- `run_20260911_210922_27f346/outputs/model_summary.json`
- `run_20260911_210922_27f346/outputs/best_metrics.json`
- `run_20260911_210922_27f346/outputs/final_metrics.json`
- `run_20260911_210922_27f346/outputs/metrics.jsonl`
- `run_20260911_210922_27f346/outputs/resource_profile.json`
- `run_20260911_210922_27f346/outputs/validation_postprocessing/index.json`
- `run_20260911_210922_27f346/outputs/prediction_samples/samples.json`
- `run_20260911_055200_52c75f` for ABI-242 parent context
- `run_20260911_050449_17cdcb` for ABI-241 high-resolution change-skip context
- `run_20260911_031326_43ed12` for ABI-240 temporal line-accumulator late36 context
- `run_20260911_004137_f54c45` for ABI-238 temporal directional-attention late36 context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention late36 comparator context
- `run_20260904_043143_ee0005` for ABI-202 current aggregate whole-validation frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
