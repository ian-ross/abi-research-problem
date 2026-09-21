# ABI-334 temporal persistence/detail focal-Tversky U-Net

research-figures: []

## Scope

This note records ABI-334, Candidate `abi334_temporal_persistence_detail_focal_tversky_unet_line_centerline_aux_v1`, Run `run_20260917_152533_b1841d`.

ABI-334 was a one-factor trusted loss-policy continuation of the ABI-331/332 compact three-frame temporal persistence/detail line-gate branch. It consumed provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`. The architecture was intentionally kept ABI-331-compatible while changing the manifest-selected trusted primary loss from `bce_dice` to `focal_tversky` to test whether the compact branch's under-recall was loss-objective limited.

This is capped temporal-eligible feasibility evidence only. It is not whole Working Validation Split promotion evidence and should not be compared as promotion evidence against the full-validation ABI-202/249 frontier.

## Execution result

ABI-334 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted primary loss: `focal_tversky`.
- Capped temporal-eligible sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 2,690,739, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 4,322,569,728 / 4,720,689,152 bytes.
- Training wall time: 1,597.0 s; validation wall time: 1,263.2 s; total Run wall time: 2,861.9 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 10.

## Best-validation metrics

| Metric | ABI-334 focal-Tversky | ABI-331 BCE-Dice parent | ABI-332 BCE-Dice late36 | ABI-333 orientation bridge | ABI-324 five-frame detail consensus | ABI-223 temporal-attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 10 | 12 | 36 | 12 | 27 | 36 |
| Filtered Dice | 0.379374 | 0.391024 | 0.413321 | 0.389367 | 0.429430 | 0.419776 |
| MIT filtered Dice | 0.374650 | 0.373811 | 0.394660 | 0.374039 | 0.408188 | 0.398498 |
| Google filtered Dice | 0.390775 | 0.436055 | 0.460548 | 0.428703 | 0.487231 | 0.476764 |
| Filtered precision | 0.352172 | 0.481788 | 0.466793 | 0.446187 | 0.470412 | 0.483764 |
| Filtered recall | 0.411130 | 0.329036 | 0.370840 | 0.345384 | 0.395017 | 0.370738 |
| Filtered connectivity | 0.242519 | 0.361417 | 0.365588 | 0.345629 | 0.397925 | 0.412427 |
| Filtered predicted-positive pixels | 638,355 | 373,444 | 434,411 | 423,275 | 459,172 | 419,056 |

ABI-334 answers the loss-policy diagnostic clearly: trusted focal-Tversky does unlock recall for this compact branch, but mainly by broadening low-precision predictions and weakening connected-line continuity. Relative to ABI-331, it raises filtered recall by about +0.082 and nearly ties MIT Dice, but lowers aggregate filtered Dice by about -0.0117, Google Dice by about -0.0453, precision by about -0.130, and connectivity by about -0.119 while expanding filtered positives by about 265k pixels. This is not a clean recall recovery.

Relative to ABI-332, ABI-334 has higher recall but worse aggregate/source Dice, precision, connectivity, and footprint. The late36 BCE-Dice parent remains the better compact persistence/detail comparator. ABI-334 is also below ABI-333 on aggregate Dice, Google Dice, precision, and connectivity despite higher recall, and it remains far below ABI-324 and ABI-223 on connected-line evidence.

At the selected checkpoint, raw Dice was 0.392762 versus filtered Dice 0.379374, raw recall was 0.444275 versus filtered recall 0.411130, and raw predicted-positive pixels were 690,249 versus 638,355 filtered. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.198556 | 0.222473 | 0.158232 | 0.136170 | 0.366439 | 0.129581 | 0.013912 |
| 2 | 0.287728 | 0.292624 | 0.277302 | 0.281112 | 0.294663 | 0.197855 | 0.005419 |
| 3 | 0.309790 | 0.315788 | 0.297464 | 0.267952 | 0.367112 | 0.186160 | 0.007083 |
| 4 | 0.323659 | 0.318507 | 0.335008 | 0.332374 | 0.315390 | 0.234657 | 0.004905 |
| 5 | 0.350689 | 0.352959 | 0.345692 | 0.331339 | 0.372439 | 0.260785 | 0.005811 |
| 6 | 0.343540 | 0.354690 | 0.319741 | 0.286996 | 0.427833 | 0.215756 | 0.007706 |
| 7 | 0.358776 | 0.350384 | 0.381027 | 0.430333 | 0.307623 | 0.384808 | 0.003695 |
| 8 | 0.347666 | 0.352301 | 0.336732 | 0.272936 | 0.478746 | 0.204250 | 0.009068 |
| 9 | 0.332531 | 0.341146 | 0.314771 | 0.266562 | 0.441889 | 0.171855 | 0.008570 |
| 10 | 0.379374 | 0.374650 | 0.390775 | 0.352172 | 0.411130 | 0.242519 | 0.006035 |
| 11 | 0.364773 | 0.364978 | 0.364296 | 0.309673 | 0.443725 | 0.230856 | 0.007407 |
| 12 | 0.314825 | 0.326642 | 0.290520 | 0.238849 | 0.461683 | 0.154227 | 0.009993 |

The trajectory is finite and non-collapsed, but it is not a late-improving signal. Best Dice occurs at epoch 10, while epochs 11-12 continue trading precision and connectivity for recall and a much broader footprint. The final epoch reaches high recall but drops to 0.314825 filtered Dice, 0.238849 precision, 0.154227 connectivity, and 1,056,962 filtered-positive pixels. This late degradation argues against requesting a late-improving focal-Tversky continuation of the unchanged branch.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.2499, 0.2094, 0.4321, and 0.2556. These examples confirm finite predictions, but their weak scores are consistent with the aggregate evidence that focal-Tversky broadened the operating point without delivering a cleaner connected true-positive mask.

## Interpretation

Classify ABI-334 as negative-to-mixed capped temporal-family development evidence for applying trusted `focal_tversky` to the exact compact persistence/detail line-gate architecture. It is scientifically useful because it isolates a loss-policy question: the branch can access more recall under focal-Tversky, but that recall is too expensive in precision, Google source balance, footprint, and connectivity.

ABI-334 does not supersede ABI-331 as the cleaner exploratory compact branch and does not supersede ABI-332 as the compact branch's best late-budget comparator. It also does not revive ABI-333's orientation-consensus path. The remaining failure mode is not simply that BCE-Dice was suppressing recall; focal-Tversky exposes recall but destabilizes threshold-0.5 compactness and thin-line continuity.

Comparator roles after ABI-334:

- ABI-324 remains the strongest local balanced recent temporal C4 aggregate/source/connectivity comparator.
- ABI-332 remains the best compact three-frame persistence/detail line-gate comparator.
- ABI-331 remains the cleaner exploratory compact parent.
- ABI-334 is a recall-biased loss-policy diagnostic, not a comparator to continue unchanged.
- ABI-223 remains the temporal-attention connectivity comparator.

ABI-334 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-334 and do not request whole-validation-style evaluation from this capped temporal-eligible Result. A temporal-eligible failure-bucket Evaluation Request is not immediately necessary because the capped aggregate/source/precision/recall/connectivity metrics already show the central failure mode: recall gained through broad, low-precision, weakly connected predictions.

Do not spend another Run on an unchanged late36 focal-Tversky continuation of ABI-334. Future compact temporal work should be mechanism-changing rather than loss-only: for example, a calibrated evidence-sharpening head that preserves compactness, a better temporal alignment/attention path, or a connectivity-preserving support mechanism that avoids the high-recall/low-connectivity collapse seen here. Alternatively, broaden away from this compact branch to another temporal attention, data-policy, or line-continuity direction.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260917_152533_b1841d/candidate/PROPOSAL.md`
- `run_20260917_152533_b1841d/candidate/README.md`
- `run_20260917_152533_b1841d/candidate/manifest.yaml`
- `run_20260917_152533_b1841d/resolved_manifest.yaml`
- `run_20260917_152533_b1841d/execution.json`
- `run_20260917_152533_b1841d/outputs/model_summary.json`
- `run_20260917_152533_b1841d/outputs/best_metrics.json`
- `run_20260917_152533_b1841d/outputs/final_metrics.json`
- `run_20260917_152533_b1841d/outputs/metrics.jsonl`
- `run_20260917_152533_b1841d/outputs/resource_profile.json`
- `run_20260917_152533_b1841d/outputs/validation_postprocessing/index.json`
- `run_20260917_152533_b1841d/outputs/prediction_samples/samples.json`
- `run_20260917_105650_6a68cc/outputs/best_metrics.json` and `/history/research-notes/abi331-temporal-persistence-detail-line-gate-unet.md` for ABI-331 comparison context
- `run_20260917_115326_f1e460/outputs/best_metrics.json` and `/history/research-notes/abi332-temporal-persistence-detail-line-gate-late36.md` for ABI-332 comparison context
- `run_20260917_142841_02a028/outputs/best_metrics.json` and `/history/research-notes/abi333-temporal-orientation-consensus-line-bridge-unet.md` for ABI-333 comparison context
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-fiveframe-detail-consensus-stabilized-line-state-late36.md` for ABI-324 comparison context
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/aggregate_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
