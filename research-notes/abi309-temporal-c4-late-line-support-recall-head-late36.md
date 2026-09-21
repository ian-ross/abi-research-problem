# ABI-309 temporal C4 late line-support recall head late36

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-309, Candidate `abi309_temporal_c4_late_line_support_recall_head_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260914_205014_1794f8`.

ABI-309 was a mechanism-changing continuation of the temporal C4 line-state U-Net branch. It kept the provider-owned three-frame temporal input (`abi_16ch_plus_sza_temporal`, offsets `[-1, 0, 1]`, `temporal_eligible_center`), BCE-Dice loss, combined source-balanced sampling, random mirroring, and trusted Line/Centerline auxiliary targets. The changed mechanism was a late line-support recall head that exposes the already learned temporal C4 line state to the final learned logit calibration head rather than using ABI-307/308-style center-detail bridge residuals.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to the full Working Validation Split frontier.

## Execution result

ABI-309 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs; request approved as `late_improving_parent_completed`.
- Direct parents/comparators: ABI-306, `run_20260914_124245_de843c`, and ABI-308, `run_20260914_175746_f48be2`.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,249,305, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 5.68 / 6.02 GiB.
- Total Run wall time: 8,018.5 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 29.

## Best-validation metrics

| Metric | ABI-309 late line-support head | ABI-306 compact C4 dual-evidence | Delta vs ABI-306 | ABI-308 selective center-detail bridge | Delta vs ABI-308 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 29 | 36 | -7 | 31 | -2 |
| Filtered Dice | 0.423544 | 0.422548 | +0.000996 | 0.410731 | +0.012813 |
| Raw Dice | 0.439038 | 0.441449 | -0.002411 | 0.429809 | +0.009229 |
| MIT filtered Dice | 0.402446 | 0.402764 | -0.000318 | 0.392983 | +0.009463 |
| Google filtered Dice | 0.478510 | 0.476152 | +0.002358 | 0.456340 | +0.022170 |
| Filtered precision | 0.401806 | 0.493422 | -0.091616 | 0.483193 | -0.081386 |
| Filtered recall | 0.447768 | 0.369478 | +0.078290 | 0.357168 | +0.090600 |
| Filtered connectivity | 0.316074 | 0.299384 | +0.016690 | 0.367013 | -0.050939 |
| Filtered predicted-positive fraction | 0.005761 | 0.003871 | +0.001890 | 0.003821 | +0.001940 |
| Filtered predicted-positive pixels | 609,361 | 409,457 | +199,904 | 404,195 | +205,166 |

ABI-309 meets the narrow primary success criterion of matching or slightly exceeding ABI-306 on selected filtered Dice while remaining source-informative. It improves Google filtered Dice and strongly raises fixed-threshold recall. This is the clearest positive signal from the late line-state support mechanism: direct line-state exposure to the final head recovered the true-positive evidence that ABI-308's selective center-detail bridge suppressed.

The trade-off is large. ABI-309 buys the Dice/recall improvement by substantially reducing precision and broadening the filtered predicted-positive footprint by about 200k pixels relative to ABI-306. MIT filtered Dice is essentially tied but slightly lower. Connectivity improves modestly over ABI-306 but does not retain ABI-308's high-connectivity state and remains well below the temporal-attention ABI-223 diagnostic comparator's 0.4124 connectivity.

At the selected checkpoint, raw Dice was 0.439038 versus filtered Dice 0.423544, raw recall was 0.483653 versus filtered recall 0.447768, and raw predicted-positive pixels were 657,946 versus 609,361 filtered. Artifact Filters reduce footprint and score; they do not create the Result.

## Final-epoch metrics

The final epoch remains competitive but is not the selected checkpoint:

| Metric | Epoch 36 final | Epoch 29 selected | Direction |
| --- | ---: | ---: | --- |
| Filtered Dice | 0.421576 | 0.423544 | lower |
| MIT filtered Dice | 0.399655 | 0.402446 | lower |
| Google filtered Dice | 0.479247 | 0.478510 | slightly higher |
| Filtered precision | 0.449761 | 0.401806 | higher |
| Filtered recall | 0.396714 | 0.447768 | lower |
| Filtered connectivity | 0.312732 | 0.316074 | lower |
| Filtered predicted-positive pixels | 482,318 | 609,361 | more compact |

Epoch 36 shifted back toward a more compact/higher-precision operating point, but did not beat the selected filtered Dice. The selected epoch is recall-heavy; the final epoch is closer to ABI-306 compactness but loses much of ABI-309's recall gain.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.236514 | 0.235703 | 0.238327 | 0.259905 | 0.216985 | 0.164118 | 0.004316 |
| 3 | 0.330044 | 0.315111 | 0.363377 | 0.332999 | 0.327142 | 0.178033 | 0.005079 |
| 5 | 0.382216 | 0.362306 | 0.432480 | 0.469403 | 0.322343 | 0.366509 | 0.003550 |
| 8 | 0.321827 | 0.312644 | 0.342936 | 0.359810 | 0.291098 | 0.193723 | 0.004182 |
| 11 | 0.394283 | 0.369060 | 0.459380 | 0.464508 | 0.342503 | 0.379308 | 0.003812 |
| 15 | 0.413740 | 0.400850 | 0.446345 | 0.412966 | 0.414517 | 0.323262 | 0.005189 |
| 19 | 0.364114 | 0.331066 | 0.447631 | 0.489337 | 0.289922 | 0.306847 | 0.003063 |
| 23 | 0.390992 | 0.373048 | 0.434618 | 0.437158 | 0.353644 | 0.228195 | 0.004182 |
| 27 | 0.384215 | 0.357820 | 0.454255 | 0.533529 | 0.300200 | 0.386814 | 0.002909 |
| 29 | 0.423544 | 0.402446 | 0.478510 | 0.401806 | 0.447768 | 0.316074 | 0.005761 |
| 31 | 0.401730 | 0.383068 | 0.446506 | 0.401350 | 0.402111 | 0.243458 | 0.005179 |
| 34 | 0.407132 | 0.381744 | 0.473469 | 0.476056 | 0.355641 | 0.333702 | 0.003862 |
| 36 | 0.421576 | 0.399655 | 0.479247 | 0.449761 | 0.396714 | 0.312732 | 0.004560 |

The trajectory is finite, non-collapsed, source-informative, and late-budget-dependent. The best checkpoint appears well after the 12-epoch exploratory ceiling. It is also oscillatory: epochs 5, 11, 27, and 34 show high-connectivity/high-precision states, while epochs 15 and 29 raise recall and aggregate Dice with broader footprints. This supports the hypothesis that late line-state support can move true contrail logits across the fixed threshold, but also shows the mechanism is not yet a stable compact-connectivity solution.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.4418, 0.0791, 0.5150, and 0.3191. This is consistent with finite non-collapsed predictions and mixed per-sample behavior, including at least one weak retained sample. It does not establish promotion evidence.

## Interpretation

Classify ABI-309 as valid positive/mixed temporal C4 family-development evidence. Relative to ABI-308, it successfully removes the overly suppressive center-detail agreement bottleneck: aggregate filtered Dice, source Dice, raw Dice, and recall all recover strongly. Relative to ABI-306, it produces a small selected filtered-Dice improvement and a large recall gain, but at a major precision and footprint cost. It therefore should not simply replace ABI-306 as the compact high-precision comparator.

The result sharpens the temporal C4 branch lesson:

- ABI-306 remains the compact high-precision temporal C4 reference.
- ABI-307 showed broad center-detail support can add recall and connectivity but broadened predictions.
- ABI-308 showed stricter center-detail agreement can improve connectivity and compactness but over-suppresses true positives.
- ABI-309 shows late temporal line-state support can recover recall and slightly improve selected filtered Dice, but does not preserve ABI-306 precision or ABI-308 connectivity.

This is enough to justify temporal-eligible diagnostics in a future step if the campaign wants failure-bucket evidence for the new recall-heavy operating point. The key diagnostic question would be whether ABI-309's extra 200k filtered predicted-positive pixels are mostly useful positive-patch recovery or negative-patch clutter. Without that evidence, do not treat ABI-309 as a promotion candidate or as whole-validation frontier evidence.

## Decision

Do not promote ABI-309. Treat it as the current recall-support variant within the temporal C4 family, not as a clean replacement for ABI-306's compact high-precision role. Do not request another unchanged ABI-306/307/308/309 late36 continuation.

A future Autonomy Step may request temporal-eligible failure-bucket diagnostics for ABI-309 because it slightly improves selected filtered Dice and substantially improves recall over ABI-306, but this note is the only primary handoff for the current Autonomy Step. If diagnostics show excessive negative-patch clutter, broaden away from late line-support heads toward a mechanism that preserves ABI-306 precision while adding connected recall support.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260914_205014_1794f8/candidate/PROPOSAL.md`
- `run_20260914_205014_1794f8/candidate/README.md`
- `run_20260914_205014_1794f8/candidate/manifest.yaml`
- `run_20260914_205014_1794f8/candidate/budget_request.yaml`
- `run_20260914_205014_1794f8/resolved_manifest.yaml`
- `run_20260914_205014_1794f8/execution.json`
- `run_20260914_205014_1794f8/outputs/model_summary.json`
- `run_20260914_205014_1794f8/outputs/best_metrics.json`
- `run_20260914_205014_1794f8/outputs/final_metrics.json`
- `run_20260914_205014_1794f8/outputs/metrics.jsonl`
- `run_20260914_205014_1794f8/outputs/resource_profile.json`
- `run_20260914_205014_1794f8/outputs/validation_postprocessing/index.json`
- `run_20260914_205014_1794f8/outputs/prediction_samples/samples.json`
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md` for ABI-306 parent comparison context
- `/history/research-notes/abi306-temporal-eligible-failure-bucket-review.md` for ABI-306 diagnostic context
- `run_20260914_175746_f48be2/outputs/best_metrics.json` and `/history/research-notes/abi308-temporal-c4-selective-agreement-center-detail-late36.md` for ABI-308 parent comparison context
- `run_20260914_151259_e64cba/outputs/best_metrics.json` and `/history/research-notes/abi307-temporal-c4-center-detail-recall-bridge-late36.md` for ABI-307 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-attention-fusion-unet-late36.md` for temporal-attention comparator context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
