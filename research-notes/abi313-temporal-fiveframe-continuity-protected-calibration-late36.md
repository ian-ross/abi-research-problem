# ABI-313 temporal five-frame continuity-protected calibration late36

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-313, Candidate `abi313_temporal_fiveframe_continuity_protected_calibration_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260915_072045_06149f`.

ABI-313 was a mechanism-changing continuation of the five-frame temporal C4 branch after ABI-311 and ABI-312. It kept provider-owned `abi_16ch_plus_sza_temporal` input with `temporal_eligible_center` selection, offsets `[-2, -1, 0, 1, 2]`, BCE-Dice loss, combined source-balanced sampling, random mirroring, and trusted Line/Centerline auxiliary targets. The changed mechanism was a continuity-protected signed calibration head intended to avoid ABI-312's broad positive residual while using center-frame detail, early temporal C4 line-state support, and auxiliary evidence to recover connected true-contrail logits.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to the full Working Validation Split frontier.

## Execution result

ABI-313 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs; request approved as `late_improving_parent_completed`.
- Direct parents/comparators: ABI-311 (`run_20260915_015552_1ac51f`), ABI-312 (`run_20260915_043533_14234b`), and ABI-306 (`run_20260914_124245_de843c`). ABI-309 (`run_20260914_205014_1794f8`) remains the recall-heavy comparison point.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-2, -1, 0, 1, 2]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,287,081, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 7.06 / 7.39 GB.
- Total Run wall time: 9,115.2 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 36.

## Best-validation metrics

| Metric | ABI-313 continuity-protected calibration | ABI-311 five-frame persistence/contrast | Delta vs ABI-311 | ABI-312 selective consensus | Delta vs ABI-312 | ABI-306 compact C4 dual-evidence | Delta vs ABI-306 | ABI-309 recall head | Delta vs ABI-309 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 36 | 27 | +9 | 27 | +9 | 36 | +0 | 29 | +7 |
| Filtered Dice | 0.413478 | 0.425000 | -0.011522 | 0.418688 | -0.005210 | 0.422548 | -0.009070 | 0.423544 | -0.010066 |
| Raw Dice | 0.431341 | 0.442688 | -0.011347 | 0.435450 | -0.004109 | 0.441449 | -0.010109 | 0.439038 | -0.007697 |
| MIT filtered Dice | 0.392755 | 0.403831 | -0.011076 | 0.397405 | -0.004649 | 0.402764 | -0.010009 | 0.402446 | -0.009691 |
| Google filtered Dice | 0.468664 | 0.482615 | -0.013951 | 0.472780 | -0.004115 | 0.476152 | -0.007488 | 0.478510 | -0.009846 |
| Filtered precision | 0.470014 | 0.459703 | +0.010311 | 0.425069 | +0.044946 | 0.493422 | -0.023407 | 0.401806 | +0.068208 |
| Filtered recall | 0.369083 | 0.395169 | -0.026086 | 0.412496 | -0.043413 | 0.369478 | -0.000395 | 0.447768 | -0.078685 |
| Filtered connectivity | 0.253086 | 0.366735 | -0.113649 | 0.261236 | -0.008150 | 0.299384 | -0.046298 | 0.316074 | -0.062988 |
| Filtered predicted-positive fraction | 0.004059 | 0.004444 | -0.000384 | 0.005017 | -0.000957 | 0.003871 | +0.000188 | 0.005761 | -0.001701 |
| Filtered predicted-positive pixels | 429,389 | 470,049 | -40,660 | 530,639 | -101,250 | 409,457 | +19,932 | 609,361 | -179,972 |

ABI-313 is finite and source-informative, but it is a negative continuation of the five-frame temporal C4 calibration line. The signed continuity-protected head did make the footprint more compact than ABI-311/312/309 and improved precision versus ABI-311 and ABI-312, but it did not preserve the target recall or connected-line quality. It trails ABI-311, ABI-312, ABI-306, and ABI-309 on aggregate filtered Dice; trails all four on MIT filtered Dice; trails all four on Google filtered Dice; and records the lowest connectivity among these comparators.

The intended repair therefore did not materialize. ABI-313 avoided ABI-312's broad positive residual, but the protection was too conservative or poorly aligned with true line support: recall collapses back to ABI-306's compact-high-precision band while precision remains below ABI-306, and connectivity is worse than even ABI-312.

At the selected checkpoint, raw Dice was 0.431341 versus filtered Dice 0.413478, raw recall was 0.398307 versus filtered recall 0.369083, and raw predicted-positive pixels were 463,058 versus 429,389 filtered. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.203121 | 0.201442 | 0.207704 | 0.426465 | 0.133307 | 0.315106 | 0.001616 |
| 3 | 0.293129 | 0.279778 | 0.324384 | 0.383226 | 0.237332 | 0.176300 | 0.003202 |
| 5 | 0.334949 | 0.319174 | 0.373827 | 0.435068 | 0.272289 | 0.212785 | 0.003235 |
| 8 | 0.386647 | 0.371643 | 0.424335 | 0.419934 | 0.358249 | 0.241008 | 0.004410 |
| 11 | 0.390364 | 0.377246 | 0.422370 | 0.396216 | 0.384682 | 0.240677 | 0.005019 |
| 15 | 0.385032 | 0.369038 | 0.429156 | 0.547039 | 0.297058 | 0.398531 | 0.002807 |
| 19 | 0.382275 | 0.360009 | 0.437653 | 0.428492 | 0.345056 | 0.240665 | 0.004163 |
| 23 | 0.389771 | 0.369523 | 0.439932 | 0.452062 | 0.342567 | 0.216828 | 0.003917 |
| 27 | 0.405148 | 0.384235 | 0.458468 | 0.438831 | 0.376266 | 0.279248 | 0.004433 |
| 31 | 0.373444 | 0.347790 | 0.440606 | 0.509129 | 0.294862 | 0.231847 | 0.002994 |
| 34 | 0.408889 | 0.387399 | 0.464202 | 0.466752 | 0.363790 | 0.248031 | 0.004029 |
| 36 | 0.413478 | 0.392755 | 0.468664 | 0.470014 | 0.369083 | 0.253086 | 0.004059 |

The trajectory is finite, non-collapsed, source-informative, and late-budget-dependent: the best checkpoint occurs at the final epoch, well beyond the 12-epoch exploratory ceiling. However, late improvement does not rescue the mechanism. ABI-313 develops into a compact, moderate-precision operating point whose aggregate Dice and source scores remain below the already characterized temporal C4 comparators. The epoch-15 high-connectivity/high-precision state was not retained, and later epochs improve Dice mostly by broadening from the epoch-31 compact state rather than recovering ABI-311-like connected-line continuity.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3864, 0.1493, 0.6363, and 0.4254. This is consistent with finite non-collapsed predictions and mixed per-sample behavior, including one weak retained sample. It does not establish promotion evidence.

## Interpretation

Classify ABI-313 as valid negative temporal C4 family-development evidence. It answers the immediate ABI-311/312 continuation question: replacing ABI-312's positive-only residual with a signed continuity-protected calibration head reduced footprint and recovered precision, but did not recover aggregate Dice, MIT/source support, fixed-threshold recall, or connected-line continuity. The protection mechanism appears to suppress too much true positive evidence while failing to stabilize line continuity.

Comparator roles after ABI-313:

- ABI-311 remains the balanced five-frame persistence/contrast temporal C4 comparator.
- ABI-306 remains the compact high-precision temporal C4 comparator.
- ABI-309 remains the recall-heavy temporal C4 diagnostic comparator with known footprint cost.
- ABI-312 and ABI-313 are negative/mixed head-calibration attempts, not new frontier targets.
- ABI-223/238 remain important temporal-attention comparators for continuity and broader temporal-family context.

ABI-313 does not justify a temporal-eligible failure-bucket evaluation as the next primary action: the aggregate metrics already show regression on the targeted MIT/source, recall, and connectivity mechanisms, and the footprint reduction is not enough to create a new useful trade-off. A diagnostic would be useful only if the campaign later needs to understand the exact conservative-gate failure mode, not for frontier selection.

## Decision

Do not promote ABI-313 and do not submit an unchanged ABI-313 late36 continuation. Treat it as evidence that continuity-protected temporal C4 calibration heads have now been characterized enough for this local line: ABI-311 remains the best balanced parent, but ABI-312 and ABI-313 did not repair its MIT/positive-patch undercoverage or typical continuity weakness.

The next useful hypothesis should broaden away from temporal C4 calibration-head interpolation. Mechanism-changing options include a different temporal-attention evidence-sharpening design, a line-continuity mechanism that is not another late residual gate, or a return to single-frame C4/orientation priors with recall/connectivity support. Any next work must preserve provider-owned temporal input, trusted losses/metrics/Artifact Filters, coordinate exclusion, and Harness-owned resource policy.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260915_072045_06149f/candidate/PROPOSAL.md`
- `run_20260915_072045_06149f/candidate/README.md`
- `run_20260915_072045_06149f/candidate/manifest.yaml`
- `run_20260915_072045_06149f/candidate/budget_request.yaml`
- `run_20260915_072045_06149f/resolved_manifest.yaml`
- `run_20260915_072045_06149f/execution.json`
- `run_20260915_072045_06149f/outputs/model_summary.json`
- `run_20260915_072045_06149f/outputs/best_metrics.json`
- `run_20260915_072045_06149f/outputs/final_metrics.json`
- `run_20260915_072045_06149f/outputs/metrics.jsonl`
- `run_20260915_072045_06149f/outputs/resource_profile.json`
- `run_20260915_072045_06149f/outputs/validation_postprocessing/index.json`
- `run_20260915_072045_06149f/outputs/prediction_samples/samples.json`
- `run_20260915_015552_1ac51f/outputs/best_metrics.json` and `/history/research-notes/abi311-temporal-fiveframe-c4-persistence-contrast-line-state-late36.md` for ABI-311 parent comparison context
- `/history/research-notes/abi311-temporal-eligible-failure-bucket-review.md` for ABI-311 diagnostic context
- `run_20260915_043533_14234b/outputs/best_metrics.json` and `/history/research-notes/abi312-temporal-fiveframe-selective-consensus-stabilized-late36.md` for ABI-312 comparison context
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md` for ABI-306 comparator context
- `/history/research-notes/abi306-temporal-eligible-failure-bucket-review.md` for ABI-306 diagnostic context
- `run_20260914_205014_1794f8/outputs/best_metrics.json` and `/history/research-notes/abi309-temporal-c4-late-line-support-recall-head-late36.md` for ABI-309 comparator context
- `/history/research-notes/abi309-temporal-eligible-failure-bucket-review.md` for ABI-309 diagnostic context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-attention-fusion-unet-late36.md` for temporal-attention comparator context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 temporal directional-context comparator context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
