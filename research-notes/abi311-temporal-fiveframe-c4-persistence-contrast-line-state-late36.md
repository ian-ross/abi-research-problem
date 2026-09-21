# ABI-311 temporal five-frame C4 persistence-contrast line-state late36

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-311, Candidate `abi311_temporal_fiveframe_c4_persistence_contrast_line_state_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260915_015552_1ac51f`.

ABI-311 was a mechanism-changing continuation of the temporal C4 line-state branch. It kept provider-owned temporal input, BCE-Dice loss, combined source-balanced sampling, random mirroring, and trusted Line/Centerline auxiliary targets, but moved the mechanism from another late line-support head to an allowlisted five-frame temporal stem. The stem used offsets `[-2, -1, 0, 1, 2]`, short- and wide-baseline persistence/contrast features, center-relative temporal attention, and early C4 orientation-consensus line state before the compact U-Net decoder and dual-evidence calibration head.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to the full Working Validation Split frontier.

## Execution result

ABI-311 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs; request approved as `late_improving_parent_completed`.
- Direct parents/comparators: ABI-306, `run_20260914_124245_de843c`; ABI-309, `run_20260914_205014_1794f8`; and ABI-310, `run_20260914_232554_0320e8`.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-2, -1, 0, 1, 2]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,245,655, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 5.81 / 6.09 GB.
- Total Run wall time: 8,256.0 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 27.

## Best-validation metrics

| Metric | ABI-311 five-frame persistence-contrast | ABI-306 compact C4 dual-evidence | Delta vs ABI-306 | ABI-309 late line-support recall | Delta vs ABI-309 | ABI-310 agreement-gated support | Delta vs ABI-310 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 27 | 36 | -9 | 29 | -2 | 36 | -9 |
| Filtered Dice | 0.425000 | 0.422548 | +0.002452 | 0.423544 | +0.001456 | 0.417524 | +0.007476 |
| Raw Dice | 0.442688 | 0.441449 | +0.001238 | 0.439038 | +0.003650 | 0.434711 | +0.007977 |
| MIT filtered Dice | 0.403831 | 0.402764 | +0.001067 | 0.402446 | +0.001385 | 0.403431 | +0.000399 |
| Google filtered Dice | 0.482615 | 0.476152 | +0.006463 | 0.478510 | +0.004105 | 0.453585 | +0.029030 |
| Filtered precision | 0.459703 | 0.493422 | -0.033719 | 0.401806 | +0.057897 | 0.438475 | +0.021228 |
| Filtered recall | 0.395169 | 0.369478 | +0.025691 | 0.447768 | -0.052599 | 0.398484 | -0.003316 |
| Filtered connectivity | 0.366735 | 0.299384 | +0.067350 | 0.316074 | +0.050661 | 0.284845 | +0.081890 |
| Filtered predicted-positive fraction | 0.004444 | 0.003871 | +0.000573 | 0.005761 | -0.001317 | 0.004698 | -0.000254 |
| Filtered predicted-positive pixels | 470,049 | 409,457 | +60,592 | 609,361 | -139,312 | 496,940 | -26,891 |

ABI-311 is a positive capped temporal-family Result. It sets a new local temporal-eligible capped best filtered Dice among the recent temporal C4 variants and edges past the ABI-223/238 temporal-attention comparators on aggregate capped filtered Dice. The mechanism gives a useful three-way trade-off: it recovers recall and connectivity relative to ABI-306 while staying much more compact and precise than ABI-309. Compared with ABI-310, it improves aggregate, Google, precision, and connectivity with essentially the same MIT score and only a small recall reduction.

The improvement is still modest in primary Dice and capped to the temporal-eligible validation population. It does not displace ABI-202 as the whole-validation reference. The most important positive signal is not only the +0.0025 Dice over ABI-306; it is the simultaneous connectivity gain (+0.0674), recall gain (+0.0257), and limited footprint increase (+60.6k filtered pixels) against the compact high-precision parent.

At the selected checkpoint, raw Dice was 0.442688 versus filtered Dice 0.425000, raw recall was 0.426816 versus filtered recall 0.395169, and raw predicted-positive pixels were 507,602 versus 470,049 filtered. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.150991 | 0.140485 | 0.181016 | 0.612166 | 0.086116 | 0.489532 | 0.000727 |
| 3 | 0.297985 | 0.277861 | 0.346115 | 0.366849 | 0.250889 | 0.224663 | 0.003535 |
| 5 | 0.294821 | 0.264377 | 0.376064 | 0.573596 | 0.198397 | 0.428726 | 0.001788 |
| 8 | 0.386090 | 0.366091 | 0.435941 | 0.428510 | 0.351313 | 0.320608 | 0.004238 |
| 11 | 0.389500 | 0.371097 | 0.435473 | 0.427019 | 0.358041 | 0.289655 | 0.004335 |
| 15 | 0.352233 | 0.329032 | 0.408046 | 0.423283 | 0.301606 | 0.259811 | 0.003684 |
| 19 | 0.367478 | 0.347785 | 0.417716 | 0.503984 | 0.289158 | 0.284687 | 0.002966 |
| 23 | 0.394063 | 0.376090 | 0.440312 | 0.445488 | 0.353282 | 0.262548 | 0.004100 |
| 27 | 0.425000 | 0.403831 | 0.482615 | 0.459703 | 0.395169 | 0.366735 | 0.004444 |
| 31 | 0.403307 | 0.376315 | 0.473445 | 0.486441 | 0.344442 | 0.374759 | 0.003661 |
| 34 | 0.398134 | 0.374623 | 0.458932 | 0.453933 | 0.354551 | 0.312653 | 0.004038 |
| 36 | 0.423798 | 0.411036 | 0.458580 | 0.422618 | 0.424983 | 0.280892 | 0.005199 |

The trajectory is finite, non-collapsed, source-informative, and late-budget-dependent. The selected epoch 27 is well beyond the 12-epoch exploratory ceiling, validating the late-improving budget for this close-continuation branch. The run does not show monotonic convergence: epoch 27 gives the best aggregate and Google score with balanced precision/recall and strong connectivity, while epoch 36 shifts toward higher recall and MIT Dice at the cost of Google Dice, precision, and connectivity. This supports treating ABI-311 as a useful calibrated temporal mechanism, not as a solved stable operating point.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.4454, 0.1415, 0.5852, and 0.3449. This is consistent with finite non-collapsed predictions and mixed per-sample behavior, including at least one weak retained sample; it does not establish promotion evidence.

## Interpretation

Classify ABI-311 as positive temporal C4 family-development evidence. The five-frame persistence/contrast stem appears more useful than further late head interpolation: it raises the local temporal C4 frontier, improves Google filtered Dice, and substantially improves connected-line continuity relative to ABI-306/309/310 at the selected checkpoint.

The result also clarifies the compact-recall-connectivity trade-off map:

- ABI-306 remains the compact high-precision temporal C4 comparator.
- ABI-309 remains the recall-heavy, broad-footprint temporal C4 diagnostic variant.
- ABI-310 is now a negative/mixed interpolation that did not preserve connectivity.
- ABI-311 is the best capped temporal C4 balance so far, using five-frame persistence/contrast to add recall and connectivity without ABI-309-scale footprint expansion.

Because the best checkpoint was epoch 27 and the final checkpoint moved to a more recall-heavy/lower-connectivity state, any next step should inspect failure buckets and threshold behavior before adding another mechanism. The immediate scientific question is whether ABI-311's apparent connectivity and Google gains correspond to fewer positive-patch fragmentation failures without a hidden increase in negative-patch clutter.

## Decision

Do not promote ABI-311 from capped temporal-eligible evidence alone. Do treat it as the current local temporal C4 family-development comparator for balanced persistence/contrast evidence, while retaining ABI-306 as the compact precision comparator and ABI-309 as the broad recall comparator.

A future Autonomy Step should request temporal-eligible failure-bucket diagnostics for ABI-311, then compare those diagnostics against ABI-306 and ABI-309 before proposing another continuation. If diagnostics confirm improved connected-line continuity without increased negative-patch clutter, a mechanism-changing continuation could focus on stabilizing the epoch-27 operating point late in training. If diagnostics show the gains are mostly source/threshold noise or false-positive heavy tails, broaden away from temporal C4 head/stem variants.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260915_015552_1ac51f/candidate/PROPOSAL.md`
- `run_20260915_015552_1ac51f/candidate/README.md`
- `run_20260915_015552_1ac51f/candidate/manifest.yaml`
- `run_20260915_015552_1ac51f/candidate/budget_request.yaml`
- `run_20260915_015552_1ac51f/resolved_manifest.yaml`
- `run_20260915_015552_1ac51f/execution.json`
- `run_20260915_015552_1ac51f/outputs/model_summary.json`
- `run_20260915_015552_1ac51f/outputs/best_metrics.json`
- `run_20260915_015552_1ac51f/outputs/final_metrics.json`
- `run_20260915_015552_1ac51f/outputs/metrics.jsonl`
- `run_20260915_015552_1ac51f/outputs/resource_profile.json`
- `run_20260915_015552_1ac51f/outputs/validation_postprocessing/index.json`
- `run_20260915_015552_1ac51f/outputs/prediction_samples/samples.json`
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md` for ABI-306 parent comparison context
- `/history/research-notes/abi306-temporal-eligible-failure-bucket-review.md` for ABI-306 diagnostic context
- `run_20260914_205014_1794f8/outputs/best_metrics.json` and `/history/research-notes/abi309-temporal-c4-late-line-support-recall-head-late36.md` for ABI-309 parent comparison context
- `/history/research-notes/abi309-temporal-eligible-failure-bucket-review.md` for ABI-309 diagnostic context
- `run_20260914_232554_0320e8/outputs/best_metrics.json` and `/history/research-notes/abi310-temporal-c4-agreement-gated-line-support-late36.md` for ABI-310 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-attention-fusion-unet-late36.md` for temporal-attention comparator context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 temporal directional-context comparator context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
