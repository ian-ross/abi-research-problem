# ABI-331 temporal persistence/detail line-gate U-Net

research-figures: []

## Scope

This note records ABI-331, Candidate `abi331_temporal_persistence_detail_line_gate_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260917_105650_6a68cc`.

ABI-331 was a bounded exploratory temporal-family development scout after the resource-failed ABI-329/330 strip-token line-mixer branch. It consumed provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`. The mechanism used a compact temporal persistence/detail stem and an architecture-internal line/detail residual gate, aiming to recover connected true-positive evidence without the wall-clock cost of strip-token mixing.

This is capped temporal-eligible feasibility evidence only. It is not whole Working Validation Split promotion evidence and is not directly comparable as promotion evidence against the full-validation ABI-202/249 frontier.

## Execution result

ABI-331 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Capped temporal-eligible sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 2,690,739, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 4,322,569,728 / 4,720,689,152 bytes.
- Training wall time: 1,589.4 s; validation wall time: 1,292.2 s; total Run wall time: 2,883.5 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 12.

## Best-validation metrics

| Metric | ABI-331 persistence/detail gate | ABI-321 attention/detail sharpening | Delta vs ABI-321 | ABI-319 shift-bank C4 confidence | ABI-324 five-frame detail consensus | ABI-325 positive-tail | ABI-328 soft-shift align | ABI-223 temporal-attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 12 | 8 | +4 | 10 | 27 | 27 | 36 | 36 |
| Filtered Dice | 0.391024 | 0.380685 | +0.010339 | 0.405847 | 0.429430 | 0.427745 | 0.423805 | 0.419776 |
| MIT filtered Dice | 0.373811 | 0.367130 | +0.006681 | 0.387897 | 0.408188 | 0.412855 | 0.403841 | 0.398498 |
| Google filtered Dice | 0.436055 | 0.416557 | +0.019498 | 0.451369 | 0.487231 | 0.466540 | 0.476913 | 0.476764 |
| Filtered precision | 0.481788 | 0.455716 | +0.026072 | 0.463906 | 0.470412 | 0.425680 | 0.444466 | 0.483764 |
| Filtered recall | 0.329036 | 0.326867 | +0.002169 | 0.360703 | 0.395017 | 0.429830 | 0.404980 | 0.370738 |
| Filtered connectivity | 0.361417 | 0.338630 | +0.022787 | 0.360704 | 0.397925 | 0.327452 | 0.322966 | 0.412427 |
| Filtered predicted-positive pixels | 373,444 | 392,207 | -18,763 | 425,166 | 459,172 | 552,142 | 498,234 | 419,056 |

ABI-331 is a positive scout relative to ABI-321: it improves aggregate Dice, both source Dice scores, precision, recall, connectivity, and compactness. The improvement is not just a broader footprint; ABI-331 predicts fewer filtered-positive pixels than ABI-321 while improving filtered Dice by about +0.010 and connectivity by about +0.023.

Against stronger temporal comparators, ABI-331 is not a frontier Result. It remains below ABI-319 by about -0.0148 filtered Dice and -0.0317 recall, although it is more precise and similarly connected with a smaller footprint. It remains substantially below ABI-324/223 on aggregate/source Dice and connected-line continuity, and below ABI-325/328 on recall. The main favorable signal is that the cheaper persistence/detail mechanism is resource-safe, compact, and cleaner than ABI-321, not that it is immediately competitive with the mature temporal C4 branch.

At the selected checkpoint, raw Dice was 0.408874 versus filtered Dice 0.391024, raw recall was 0.355433 versus filtered recall 0.329036, and raw predicted-positive pixels were 403,871 versus 373,444 filtered. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.241012 | 0.249187 | 0.223146 | 0.224371 | 0.260320 | 0.154442 | 0.005998 |
| 2 | 0.292535 | 0.285617 | 0.310963 | 0.348673 | 0.251968 | 0.265970 | 0.003736 |
| 3 | 0.301188 | 0.283155 | 0.348019 | 0.458636 | 0.224216 | 0.307166 | 0.002527 |
| 4 | 0.326489 | 0.309975 | 0.368594 | 0.400981 | 0.275338 | 0.270636 | 0.003550 |
| 5 | 0.366395 | 0.356284 | 0.390104 | 0.385696 | 0.348933 | 0.247848 | 0.004677 |
| 6 | 0.349638 | 0.334523 | 0.390819 | 0.492740 | 0.270949 | 0.398831 | 0.002843 |
| 7 | 0.366596 | 0.351273 | 0.407840 | 0.492883 | 0.291824 | 0.405503 | 0.003061 |
| 8 | 0.378528 | 0.366051 | 0.410732 | 0.411373 | 0.350541 | 0.288932 | 0.004405 |
| 9 | 0.383487 | 0.373699 | 0.407432 | 0.390828 | 0.376416 | 0.316012 | 0.004979 |
| 10 | 0.359505 | 0.336693 | 0.419022 | 0.464500 | 0.293225 | 0.351525 | 0.003263 |
| 11 | 0.364048 | 0.349321 | 0.401002 | 0.419841 | 0.321344 | 0.285788 | 0.003957 |
| 12 | 0.391024 | 0.373811 | 0.436055 | 0.481788 | 0.329036 | 0.361417 | 0.003531 |

The trajectory is finite, source-informative, and late active. The best checkpoint is the final exploratory epoch, and the final epoch improves aggregate Dice, Google Dice, precision, and compactness after several noisy precision/recall oscillations. Epochs 6-7 briefly reached higher connectivity but under lower recall; epoch 9 reached the highest recall but at lower precision and worse Google Dice. This suggests the mechanism is useful but has an unstable calibration surface under the 12-epoch exploratory budget.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.4220, 0.3978, 0.5970, and 0.4186. This confirms finite non-collapsed predictions on retained examples, but does not overturn the aggregate evidence that ABI-331 is below the stronger temporal C4 and ABI-223 comparators.

## Interpretation

Classify ABI-331 as positive capped temporal-family development evidence for a cheap persistence/detail line-gate mechanism, but not as a promotion candidate. It directly addresses the ABI-329/330 resource failure by avoiding full-resolution strip-token mixing and completes comfortably within the exploratory timeout. Relative to ABI-321, the mechanism gives a cleaner and more connected operating point, with better precision and a smaller filtered footprint.

The remaining failure mode is under-recall and source-gap versus the stronger temporal comparators. ABI-331 appears to keep negative-patch clutter controlled, but it does not yet raise enough true contrail pixels at threshold 0.5. Its final-epoch best checkpoint means the exploratory budget may be truncating the mechanism's learning, but the current Result is still materially below ABI-319/324/223 and should be treated as bounded feasibility evidence only.

Comparator roles after ABI-331:

- ABI-324 remains the strongest local balanced temporal C4 aggregate/source/connectivity comparator.
- ABI-325 remains the broad positive-tail recall diagnostic, not a balanced comparator.
- ABI-328 remains negative-to-mixed evidence for soft-shift alignment as a C4 repair.
- ABI-319 remains a stronger three-frame shift-bank/C4 comparator than ABI-331.
- ABI-321 is now a weaker lightweight temporal-attention/detail-sharpening comparator; ABI-331 supersedes it as the cleaner cheap temporal-gated scout.
- ABI-223 remains the older temporal-attention connectivity comparator.

ABI-331 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-331 and do not request whole-validation-style evaluation from this capped exploratory Result. A temporal-eligible failure-bucket Evaluation Request is not immediately necessary because the capped aggregate/source/connectivity metrics already show the main trade-off: clean compact predictions but insufficient recall versus ABI-319/324/223.

ABI-331 does justify further bounded family development if the next step chooses to continue this branch: the run is resource-safe, finite, non-collapsed, better than ABI-321 across the target metrics, and selected its best checkpoint at the final epoch. A close continuation could request the approved `late_improving` budget or add a specific recall-support mechanism, but it should not simply rerun the unchanged architecture without a budget-request rationale.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260917_105650_6a68cc/candidate/PROPOSAL.md`
- `run_20260917_105650_6a68cc/candidate/README.md`
- `run_20260917_105650_6a68cc/candidate/manifest.yaml`
- `run_20260917_105650_6a68cc/resolved_manifest.yaml`
- `run_20260917_105650_6a68cc/execution.json`
- `run_20260917_105650_6a68cc/outputs/model_summary.json`
- `run_20260917_105650_6a68cc/outputs/best_metrics.json`
- `run_20260917_105650_6a68cc/outputs/final_metrics.json`
- `run_20260917_105650_6a68cc/outputs/metrics.jsonl`
- `run_20260917_105650_6a68cc/outputs/resource_profile.json`
- `run_20260917_105650_6a68cc/outputs/validation_postprocessing/index.json`
- `run_20260917_105650_6a68cc/outputs/prediction_samples/samples.json`
- `run_20260915_183315_3f1d30/outputs/best_metrics.json` and `/history/research-notes/abi321-temporal-attention-center-detail-evidence-sharpening-unet.md` for ABI-321 comparison context
- `run_20260915_162050_163586/outputs/best_metrics.json` and `/history/research-notes/abi319-temporal-shiftbank-c4-alignment-confidence-line-unet.md` for ABI-319 comparison context
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-fiveframe-detail-consensus-stabilized-line-state-late36.md` for ABI-324 comparison context
- `run_20260916_212722_d66d93/outputs/best_metrics.json` and `/history/research-notes/abi325-temporal-fiveframe-positive-tail-evidence-reinjector-late36.md` for ABI-325 comparison context
- `run_20260917_055012_ba7890/outputs/best_metrics.json` and `/history/research-notes/abi328-temporal-fiveframe-softshift-alignment-c4-line-state-late36.md` for ABI-328 comparison context
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/aggregate_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
