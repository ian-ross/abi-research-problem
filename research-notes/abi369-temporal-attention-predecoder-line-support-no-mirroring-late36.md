# ABI-369 temporal-attention pre-decoder line-support no-mirroring late36

research-figures: []

## Scope

This note records ABI-369, Candidate `abi369_temporal_attention_predecoder_line_support_no_mirroring_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260920_155638_988238`.

ABI-369 was a one-factor data-policy continuation of ABI-350. It kept the ABI-350 temporal-attention pre-decoder line-support U-Net architecture, provider-owned `abi_16ch_plus_sza_temporal` inputs with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, BCE-Dice primary loss, Line and Centerline auxiliary targets, AdamW with constant learning rate, and batch size 2. The controlled change was disabling trusted `random_mirroring` by setting the allowlisted augmentation policy to `none`, testing whether preserving physical GOES scan/illumination orientation helps MIT/source balance, fixed-threshold recall, or connected-line continuity on the current strongest temporal line-support scaffold.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence and should not be treated as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-369 completed without contract, smoke, shape, numerical, resource, or lifecycle failure. The requested late-improving budget was approved.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs, 10,800 s timeout.
- Budget parents: `run_20260919_013306_9ca44e` (ABI-350 mirrored architecture parent) and `run_20260917_201833_57b081` (ABI-337 no-mirroring diagnostic control).
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `none`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,132,228, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 4,244,163,584 / 4,766,826,496 bytes.
- Training wall time: 4,042.1 s; validation wall time: 3,134.2 s; total Run wall time: 7,178.3 s, within the late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 36.

## Temporal-eligible aggregate metrics

| Metric | ABI-369 no mirroring | ABI-350 mirrored parent | Delta vs ABI-350 | ABI-337 no-mirror diagnostic | ABI-359 early C4 alignment | ABI-367 detail tail | ABI-356 recall parent | ABI-223 temporal attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 36 | 33 | +3 | 27 | 27 | 27 | 36 | 36 |
| Filtered Dice | 0.429268 | 0.431103 | -0.001835 | 0.428894 | 0.426759 | 0.420955 | 0.426056 | 0.419776 |
| MIT filtered Dice | 0.414658 | 0.409536 | +0.005122 | 0.411838 | 0.406428 | 0.404132 | 0.411375 | 0.398498 |
| Google filtered Dice | 0.467429 | 0.490518 | -0.023090 | 0.476340 | 0.481165 | 0.465751 | 0.465688 | 0.476764 |
| Filtered precision | 0.454607 | 0.494306 | -0.039699 | 0.466489 | 0.474933 | 0.459504 | 0.421447 | 0.483764 |
| Filtered recall | 0.406604 | 0.382230 | +0.024374 | 0.396906 | 0.387459 | 0.388373 | 0.430766 | 0.370738 |
| Filtered connectivity | 0.298437 | 0.358283 | -0.059846 | 0.365326 | 0.376348 | 0.245025 | 0.282116 | 0.412427 |
| Filtered predicted-positive pixels | 489,073 | 422,831 | +66,242 | 465,248 | 446,099 | 462,166 | 558,903 | 419,056 |

ABI-369 is finite and source-informative, but it is mixed-negative evidence for disabling random mirroring on the ABI-350 architecture. Relative to ABI-350, it improves MIT filtered Dice and fixed-threshold recall, but loses aggregate Dice, Google Dice, precision, and connected-line continuity while broadening the filtered footprint by 66,242 pixels. The result repeats ABI-337's qualitative data-policy pattern: no mirroring can shift the model toward MIT/recall, but it does not improve the targeted connectivity/compactness failure mode.

The high MIT filtered Dice is the main positive signal. ABI-369's MIT Dice is above ABI-350, ABI-337, ABI-359, ABI-367, ABI-356, and ABI-223 on this capped temporal-eligible validation population. However, the source trade-off is unfavorable for a comparator: Google Dice falls far below ABI-350 and below ABI-337/359/223, and the aggregate score remains below ABI-350. ABI-369 is therefore not a new temporal frontier despite being one of the stronger capped temporal-eligible scores.

Raw versus filtered metrics show ordinary Artifact Filter behavior rather than filter-created performance. At the selected checkpoint, raw Dice was 0.447131 versus filtered Dice 0.429268, raw recall was 0.439952 versus filtered recall 0.406604, and raw predicted-positive pixels were 529,254 versus 489,073 filtered. Artifact Filters removed 40,181 predicted-positive pixels and lowered the score.

The retained fixed `first_n` prediction samples have nonzero per-sample Dice values of 0.4045, 0.2000, 0.6041, and 0.3707. They do not indicate all-negative or all-positive qualitative collapse, but they are only the first four validation samples and should not override aggregate temporal-eligible metrics.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive pixels |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.218187 | 0.222927 | 0.208680 | 0.217437 | 0.218942 | 0.134489 | 550,595 |
| 6 | 0.378906 | 0.368109 | 0.406127 | 0.423858 | 0.342575 | 0.307556 | 441,950 |
| 12 | 0.366859 | 0.352936 | 0.403850 | 0.499669 | 0.289825 | 0.267135 | 317,170 |
| 15 | 0.408846 | 0.393466 | 0.450932 | 0.519608 | 0.337008 | 0.392114 | 354,652 |
| 22 | 0.398211 | 0.386674 | 0.427537 | 0.425664 | 0.374085 | 0.209289 | 480,553 |
| 27 | 0.413419 | 0.398260 | 0.457183 | 0.530778 | 0.338561 | 0.426522 | 348,788 |
| 29 | 0.406582 | 0.392715 | 0.442576 | 0.487218 | 0.348848 | 0.236376 | 391,517 |
| 31 | 0.395572 | 0.376043 | 0.448607 | 0.528300 | 0.316145 | 0.332754 | 327,223 |
| 33 | 0.396521 | 0.377491 | 0.449525 | 0.521484 | 0.319870 | 0.376959 | 335,406 |
| 34 | 0.403432 | 0.385325 | 0.453094 | 0.519333 | 0.329825 | 0.376439 | 347,276 |
| 35 | 0.369268 | 0.353196 | 0.414176 | 0.540528 | 0.280420 | 0.374937 | 283,680 |
| 36 | 0.429268 | 0.414658 | 0.467429 | 0.454607 | 0.406604 | 0.298437 | 489,073 |

The late budget was informative: the selected checkpoint arrived at epoch 36 and was materially different from the epoch-12 exploratory state. The trajectory also illustrates the repeated temporal-family decoupling between compact/high-connectivity states and high-recall states. Epoch 27 had much better precision and connectivity than the selected epoch, with fewer filtered-positive pixels, but it under-recalled and scored lower. Epoch 36 improved aggregate and MIT Dice by broadening the footprint and raising recall, but it sacrificed connectivity and precision.

This trajectory argues against a simple data-policy explanation for ABI-350's remaining errors. Preserving physical orientation by disabling mirroring can move the model between MIT/recall and Google/precision/connectivity operating regions, but it does not combine them at the trusted fixed threshold.

## Interpretation

Classify ABI-369 as a finite, resource-safe, mixed temporal data-policy result. It provides useful evidence that disabling trusted random mirroring is not a clear upgrade for the strongest temporal-attention pre-decoder line-support branch. The controlled change improves MIT filtered Dice and recall, but the aggregate/source/precision/connectivity trade-off is worse than ABI-350. The branch should not be promoted and should not replace ABI-350 as the capped temporal-eligible comparator.

Do not submit another unchanged no-mirroring late36 continuation of ABI-350, an augmentation-only repeat, or a minor width/gate-strength variant. Random mirroring appears to regularize the stronger temporal line-support scaffold toward better Google/source balance and connected-line compactness. If this architecture family continues, it should be mechanism-changing: for example, explicitly separating MIT/Google-like recall evidence from connectivity support without using Dataset Source identity, or adding architecture-level line continuity that preserves the epoch-27 compact/high-connectivity state while recovering the epoch-36 recall. Candidate-owned thresholds, calibration, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, and lifecycle changes remain out of scope.

A Post-Run Evaluation is not requested in this Autonomy Step. ABI-369 is close to ABI-350 in aggregate capped temporal-eligible Dice and raises MIT/recall, but it regresses the intended connectivity/source-balance behavior and prior temporal-eligible diagnostics already characterize the relevant no-mirroring and line-support failure modes. Further diagnostic spend should be reserved for a candidate that clearly changes the comparator frontier or presents an unresolved promotion/failure-bucket question.

## Decision

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260920_155638_988238/candidate/PROPOSAL.md`
- `run_20260920_155638_988238/candidate/README.md`
- `run_20260920_155638_988238/candidate/manifest.yaml`
- `run_20260920_155638_988238/candidate/budget_request.yaml`
- `run_20260920_155638_988238/resolved_manifest.yaml`
- `run_20260920_155638_988238/execution.json`
- `run_20260920_155638_988238/run_metadata.json`
- `run_20260920_155638_988238/outputs/model_summary.json`
- `run_20260920_155638_988238/outputs/best_metrics.json`
- `run_20260920_155638_988238/outputs/final_metrics.json`
- `run_20260920_155638_988238/outputs/metrics.jsonl`
- `run_20260920_155638_988238/outputs/resource_profile.json`
- `run_20260920_155638_988238/outputs/validation_postprocessing/index.json`
- `run_20260920_155638_988238/outputs/prediction_samples/samples.json`
- `run_20260919_013306_9ca44e/outputs/best_metrics.json` and `/history/research-notes/abi350-temporal-attention-predecoder-line-support-late36.md` for ABI-350 mirrored-parent context
- `run_20260917_201833_57b081/outputs/best_metrics.json` and `/history/research-notes/abi337-temporal-fiveframe-detail-consensus-no-mirroring-late36.md` for ABI-337 no-mirroring diagnostic context
- `run_20260919_175950_ac7b89/outputs/best_metrics.json` and `/history/research-notes/abi359-temporal-alignment-c4-center-detail-bridge-late36.md` for ABI-359 early-C4 comparator context
- `run_20260920_112921_1ee9bd/outputs/best_metrics.json` and `/history/research-notes/abi367-temporal-center-detail-tail-support-late36.md` for ABI-367 local temporal-tail comparator context
- `run_20260919_095725_843317/outputs/best_metrics.json` and `/history/research-notes/abi356-temporal-attention-multiscale-change-line-fusion-late36.md` for ABI-356 recall-parent context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/reference/EXPERIMENT_INDEX.md` for ABI-223 temporal-attention comparator context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
