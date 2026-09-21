# ABI-335 temporal calibrated dual-evidence line-gate U-Net

research-figures: []

## Scope

This note records ABI-335, Candidate `abi335_temporal_calibrated_dual_evidence_line_gate_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260917_162237_44136f`.

ABI-335 was a mechanism-changing exploratory continuation of the compact three-frame temporal persistence/detail line-gate branch. It consumed provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`. The candidate returned from ABI-334's trusted `focal_tversky` diagnostic to trusted `bce_dice`, and replaced the head with a calibrated dual-evidence line gate intended to raise uncertain center-frame mask logits only when line context, centerline evidence, center-frame detail, and temporal persistence agree, while vetoing support/detail mismatches.

This is capped temporal-eligible feasibility evidence only. It is not whole Working Validation Split promotion evidence and should not be compared as promotion evidence against the full-validation ABI-202/249 frontier.

## Execution result

ABI-335 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted primary loss: `bce_dice`.
- Capped temporal-eligible sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 2,701,828, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 4,493,640,192 / 4,829,741,056 bytes.
- Training wall time: 1,650.2 s; validation wall time: 1,312.0 s; total Run wall time: 2,964.0 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 11.

## Best-validation metrics

| Metric | ABI-335 calibrated dual-evidence | ABI-331 exploratory parent | ABI-332 late parent | ABI-333 orientation bridge | ABI-334 focal-Tversky diagnostic | ABI-324 five-frame detail consensus | ABI-223 temporal-attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 11 | 12 | 36 | 12 | 10 | 27 | 36 |
| Filtered Dice | 0.391377 | 0.391024 | 0.413321 | 0.389367 | 0.379374 | 0.429430 | 0.419776 |
| MIT filtered Dice | 0.374386 | 0.373811 | 0.394660 | 0.374039 | 0.374650 | 0.408188 | 0.398498 |
| Google filtered Dice | 0.434812 | 0.436055 | 0.460548 | 0.428703 | 0.390775 | 0.487231 | 0.476764 |
| Filtered precision | 0.425650 | 0.481788 | 0.466793 | 0.446187 | 0.352172 | 0.470412 | 0.483764 |
| Filtered recall | 0.362212 | 0.329036 | 0.370840 | 0.345384 | 0.411130 | 0.395017 | 0.370738 |
| Filtered connectivity | 0.315623 | 0.361417 | 0.365588 | 0.345629 | 0.242519 | 0.397925 | 0.412427 |
| Filtered predicted-positive pixels | 465,317 | 373,444 | 434,411 | 423,275 | 638,355 | 459,172 | 419,056 |

ABI-335 partially achieved the proposal's intended direction but not enough to become a useful comparator. Relative to ABI-334, it avoided the worst recall-biased broad-footprint signature: filtered precision is about +0.073 higher, connectivity is about +0.073 higher, Google Dice is about +0.044 higher, and the filtered footprint is about 173k pixels smaller. However, this comes with about -0.049 recall relative to ABI-334, so ABI-335 did not preserve the main benefit of the focal-Tversky diagnostic.

Relative to ABI-331, ABI-335 raises filtered recall by about +0.033 and nearly ties aggregate/source Dice, but it loses about -0.056 precision, -0.046 connectivity, and expands the footprint by about 92k pixels. Relative to ABI-333, it is a small aggregate/source Dice and recall improvement, but not a connectivity improvement. Relative to ABI-332, ABI-335 remains behind on aggregate/source Dice, precision, recall, and connectivity despite having a broader footprint. The calibrated dual-evidence head therefore creates an intermediate operating point between clean compact BCE-Dice and broad focal-Tversky behavior, rather than a cleaner recall recovery.

At the selected checkpoint, raw Dice was 0.407786 versus filtered Dice 0.391377, raw recall was 0.390873 versus filtered recall 0.362212, and raw predicted-positive pixels were 501,453 versus 465,317 filtered. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.230451 | 0.242076 | 0.206362 | 0.210755 | 0.254208 | 0.155077 | 0.006235 |
| 2 | 0.296049 | 0.292067 | 0.305469 | 0.298748 | 0.293397 | 0.204112 | 0.005077 |
| 3 | 0.321439 | 0.305705 | 0.360810 | 0.413593 | 0.262869 | 0.275791 | 0.003286 |
| 4 | 0.325068 | 0.302737 | 0.380916 | 0.430634 | 0.261070 | 0.283842 | 0.003134 |
| 5 | 0.333996 | 0.313354 | 0.386466 | 0.455810 | 0.263560 | 0.338569 | 0.002989 |
| 6 | 0.363328 | 0.346825 | 0.406762 | 0.467149 | 0.297263 | 0.363769 | 0.003290 |
| 7 | 0.357194 | 0.338364 | 0.409529 | 0.458362 | 0.292611 | 0.401056 | 0.003300 |
| 8 | 0.378783 | 0.359753 | 0.429918 | 0.479555 | 0.313009 | 0.391003 | 0.003374 |
| 9 | 0.380193 | 0.364600 | 0.420140 | 0.396137 | 0.365482 | 0.312708 | 0.004770 |
| 10 | 0.379224 | 0.359638 | 0.429203 | 0.452645 | 0.326297 | 0.336541 | 0.003727 |
| 11 | 0.391377 | 0.374386 | 0.434812 | 0.425650 | 0.362212 | 0.315623 | 0.004399 |
| 12 | 0.370523 | 0.352429 | 0.417163 | 0.466163 | 0.307446 | 0.327050 | 0.003409 |

The trajectory is finite, source-informative, and non-collapsed, but not a strong late-improving signal. Best Dice occurs at epoch 11, followed by a final-epoch precision/compactness shift that loses recall and aggregate/source Dice. Connectivity peaks earlier at epoch 7 under a compact lower-recall state, then declines at the selected higher-recall checkpoint. This repeats the compact branch's recurring failure mode: high-connectivity states and higher-recall states are not being unified into one stable threshold-0.5 operating point.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3689, 0.4094, 0.5150, and 0.3886. These confirm finite non-collapsed predictions on retained examples, but do not overturn the aggregate evidence that ABI-335 remains sub-frontier and does not solve the branch's connected-recall trade-off.

## Interpretation

Classify ABI-335 as mixed capped temporal-family development evidence for the calibrated dual-evidence line-gate head. It usefully shows that architecture-level calibration can avoid ABI-334's most excessive broad low-precision footprint while recovering more recall than ABI-331. But the improvement over ABI-331/333 is marginal in filtered Dice, and the cost in precision/connectivity is too high. ABI-332 remains the best compact three-frame persistence/detail line-gate comparator, and ABI-324/223 remain stronger temporal comparators for balanced aggregate/source/connectivity evidence.

The central failure mode is no longer simple recall suppression. The branch can move along the precision/recall axis, but its head and support mechanisms have not produced a stable state with ABI-332-level compactness, ABI-334-like recall, and ABI-331/332-like connected-line continuity. Further work in this exact branch should be mechanism-changing rather than an unchanged late36 continuation of ABI-335.

Comparator roles after ABI-335:

- ABI-324 remains the strongest local balanced recent temporal C4 aggregate/source/connectivity comparator.
- ABI-332 remains the best compact three-frame persistence/detail line-gate comparator.
- ABI-335 is an intermediate calibration-head diagnostic, not a new comparator to continue unchanged.
- ABI-334 remains a recall-biased loss-policy diagnostic.
- ABI-333 remains negative-to-mixed evidence for the previous orientation-consensus line bridge.
- ABI-223 remains the temporal-attention connectivity comparator.

ABI-335 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-335 and do not request whole-validation-style evaluation from this capped temporal-eligible Result. A temporal-eligible failure-bucket Evaluation Request is not immediately necessary because the capped aggregate/source/precision/recall/connectivity metrics already show the central failure mode: a modest recall/footprint shift without a connectivity or aggregate advantage over ABI-332, ABI-324, or ABI-223.

Do not spend another Run on an unchanged late36 continuation of ABI-335. If the compact three-frame branch is revisited, the next hypothesis should explicitly target the observed decoupling between high-connectivity compact states and higher-recall states, for example with a mechanism-changing temporal alignment/attention path or a connectivity-preserving support head. Otherwise broaden to another temporal attention, calibration, data-policy, trusted loss, or line-continuity direction.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260917_162237_44136f/candidate/PROPOSAL.md`
- `run_20260917_162237_44136f/candidate/README.md`
- `run_20260917_162237_44136f/candidate/manifest.yaml`
- `run_20260917_162237_44136f/resolved_manifest.yaml`
- `run_20260917_162237_44136f/execution.json`
- `run_20260917_162237_44136f/outputs/model_summary.json`
- `run_20260917_162237_44136f/outputs/best_metrics.json`
- `run_20260917_162237_44136f/outputs/final_metrics.json`
- `run_20260917_162237_44136f/outputs/metrics.jsonl`
- `run_20260917_162237_44136f/outputs/resource_profile.json`
- `run_20260917_162237_44136f/outputs/validation_postprocessing/index.json`
- `run_20260917_162237_44136f/outputs/prediction_samples/samples.json`
- `run_20260917_105650_6a68cc/outputs/best_metrics.json` and `/history/research-notes/abi331-temporal-persistence-detail-line-gate-unet.md` for ABI-331 comparison context
- `run_20260917_115326_f1e460/outputs/best_metrics.json` and `/history/research-notes/abi332-temporal-persistence-detail-line-gate-late36.md` for ABI-332 comparison context
- `run_20260917_142841_02a028/outputs/best_metrics.json` and `/history/research-notes/abi333-temporal-orientation-consensus-line-bridge-unet.md` for ABI-333 comparison context
- `run_20260917_152533_b1841d/outputs/best_metrics.json` and `/history/research-notes/abi334-temporal-persistence-detail-focal-tversky-unet.md` for ABI-334 comparison context
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-fiveframe-detail-consensus-stabilized-line-state-late36.md` for ABI-324 comparison context
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/aggregate_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
