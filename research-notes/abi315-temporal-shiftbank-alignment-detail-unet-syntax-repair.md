# ABI-315 temporal shift-bank alignment detail U-Net syntax repair

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-315, Candidate `abi315_temporal_shiftbank_alignment_detail_unet_syntax_repair_v1`, Run `run_20260915_100642_28e66d`.

ABI-315 was a repair Candidate for ABI-314 after `run_20260915_100315_94315b` smoke-failed with a candidate-owned syntax error: an unmatched `}` after the `ShiftBankEvidenceHead` docstring. The repair preserved ABI-314's temporal shift-bank alignment hypothesis, architecture, manifest policy, comparison target, and exploratory budget. It changed only the syntax defect so the intended model could be imported and evaluated.

The mechanism under test is differentiable small-displacement temporal feature alignment: previous and next frame features are scored over a nine-shift bank against center-frame keys, softmax-aligned, then fused with center-frame detail and directional line context. The candidate consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`; all temporal provisioning, sampling, losses, metrics, Artifact Filters, thresholding, postprocessing, and execution remain Harness/provider owned.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to the full Working Validation Split frontier.

## Execution result

ABI-315 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `exploratory`, 12 epochs.
- Repair parent: ABI-314 (`run_20260915_100315_94315b`), smoke-failed as `candidate_bug` before scientific evaluation.
- Comparison targets: ABI-311 balanced five-frame temporal C4 comparator, ABI-309 recall-heavy temporal C4 comparator, ABI-306 compact high-precision temporal C4 comparator, ABI-312/313 recent five-frame calibration attempts, and ABI-296/299 local-correlation branch references.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 5,746,951, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 6.79 / 7.30 GB.
- Total Run wall time: 2,863.0 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 12.

## Best-validation metrics

| Metric | ABI-315 shift-bank alignment | ABI-311 five-frame C4 | Delta vs ABI-311 | ABI-309 recall head | Delta vs ABI-309 | ABI-306 compact C4 | Delta vs ABI-306 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 12 | 27 | -15 | 29 | -17 | 36 | -24 |
| Filtered Dice | 0.389886 | 0.425000 | -0.035114 | 0.423544 | -0.033658 | 0.422548 | -0.032663 |
| MIT filtered Dice | 0.377376 | 0.403831 | -0.026455 | 0.402446 | -0.025070 | 0.402764 | -0.025388 |
| Google filtered Dice | 0.420154 | 0.482615 | -0.062461 | 0.478510 | -0.058356 | 0.476152 | -0.055998 |
| Filtered precision | 0.412308 | 0.459703 | -0.047395 | 0.401806 | +0.010502 | 0.493422 | -0.081114 |
| Filtered recall | 0.369776 | 0.395169 | -0.025393 | 0.447768 | -0.077992 | 0.369478 | +0.000298 |
| Filtered connectivity | 0.266017 | 0.366735 | -0.100717 | 0.316074 | -0.050057 | 0.299384 | -0.033367 |
| Filtered predicted-positive fraction | 0.004636 | 0.004444 | +0.000192 | 0.005761 | -0.001125 | 0.003871 | +0.000765 |
| Filtered predicted-positive pixels | 490,405 | 470,049 | +20,356 | 609,361 | -118,956 | 409,457 | +80,948 |

ABI-315 is finite and source-informative, but it does not reach the current temporal-eligible frontier. The shift-bank alignment scout lands in a moderate-recall, moderate-footprint regime: recall is essentially tied with ABI-306, but precision is much lower; footprint is smaller than ABI-309, but recall is also much lower; connectivity is substantially weaker than ABI-311 and ABI-309. Google filtered Dice is the clearest deficit versus recent temporal C4 comparators.

At the selected checkpoint, raw Dice was 0.405949 versus filtered Dice 0.389886, raw recall was 0.399494 versus filtered recall 0.369776, and raw predicted-positive pixels were 529,421 versus 490,405 filtered. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.271342 | 0.276577 | 0.259795 | 0.256083 | 0.288534 | 0.193886 | 0.005825 |
| 2 | 0.300080 | 0.299047 | 0.302434 | 0.325358 | 0.278447 | 0.227561 | 0.004424 |
| 3 | 0.311526 | 0.304206 | 0.327392 | 0.330223 | 0.294833 | 0.194138 | 0.004616 |
| 4 | 0.334080 | 0.318657 | 0.371795 | 0.430513 | 0.272942 | 0.301153 | 0.003277 |
| 5 | 0.341152 | 0.334721 | 0.355203 | 0.364948 | 0.320269 | 0.228519 | 0.004537 |
| 6 | 0.313729 | 0.300963 | 0.344669 | 0.440072 | 0.243749 | 0.297940 | 0.002863 |
| 7 | 0.329099 | 0.309892 | 0.379934 | 0.548352 | 0.235097 | 0.415477 | 0.002216 |
| 8 | 0.375628 | 0.362065 | 0.410232 | 0.450562 | 0.322065 | 0.297305 | 0.003695 |
| 9 | 0.378117 | 0.370334 | 0.397488 | 0.392495 | 0.364754 | 0.296626 | 0.004804 |
| 10 | 0.371643 | 0.355425 | 0.413234 | 0.470247 | 0.307223 | 0.277032 | 0.003377 |
| 11 | 0.367697 | 0.349464 | 0.415365 | 0.483414 | 0.296680 | 0.376077 | 0.003173 |
| 12 | 0.389886 | 0.377376 | 0.420154 | 0.412308 | 0.369776 | 0.266017 | 0.004636 |

The trajectory is finite, non-collapsed, and still improving at the exploratory ceiling: the best filtered Dice occurs at epoch 12. However, the path is noisy and does not yet show a distinct advantage over better-characterized late-budget temporal comparators. The best connectivity spike at epoch 7 did not coincide with strong Dice or recall and was not retained. The final improvement is mainly a recall/footprint expansion from epochs 10-11 rather than stable connected-line sharpening.

This trajectory could technically meet a minimal late-improving-budget criterion because the best checkpoint is at the final exploratory epoch. Scientifically, an unchanged ABI-315 late36 continuation is not the strongest next use of budget: the branch starts far below ABI-311/309/306, has weak connectivity, and does not yet demonstrate that shift-bank alignment improves the targeted temporal trade-off. A later continuation should require a mechanism change that stabilizes the early connectivity signal while preserving recall.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.4707, 0.1986, 0.5508, and 0.4145. This is consistent with finite non-collapsed predictions and mixed per-sample behavior, including one weak retained sample. It does not establish promotion evidence.

## Interpretation

Classify ABI-315 as a successful syntax repair and valid but negative temporal shift-bank scout. It proves the repaired architecture is executable within the active resource policy, but the current alignment mechanism does not improve the main fixed-threshold temporal trade-offs. It is lower than ABI-311, ABI-309, and ABI-306 on aggregate filtered Dice, MIT filtered Dice, Google filtered Dice, and connected-line continuity. Its only favorable comparison is slightly higher recall than ABI-306 at the cost of much lower precision and a larger prediction footprint.

The likely failure mode is that local shift-bank matching supplies some extra temporal evidence but does not learn a stable line-continuity prior. The model can expand predictions late in training, yet aligned features do not convert into connected thin-line support. Because temporal C4 late-budget variants already occupy stronger balanced, compact, and recall-heavy points, this exact branch should not be promoted.

Comparator roles after ABI-315:

- ABI-311 remains the balanced five-frame temporal C4 comparator.
- ABI-309 remains the recall-heavy temporal C4 comparator with known footprint cost.
- ABI-306 remains the compact high-precision temporal C4 comparator and current strong temporal-eligible Result.
- ABI-315 is a resource-feasible shift-bank alignment scout, not a new frontier target.
- ABI-314 should be treated only as the repaired smoke-failure parent, not as scientific evidence.

ABI-315 does not warrant an immediate temporal-eligible failure-bucket evaluation. The capped aggregate metrics already show that it misses the targeted recall/connectivity/source-balance improvements; diagnostics would be useful only if a future mechanism-changing shift-bank continuation needs to understand why the early connectivity spike disappears.

## Decision

Do not promote ABI-315 and do not submit an unchanged late36 continuation of ABI-315. Treat it as evidence that naive small-displacement temporal feature alignment is feasible but insufficient. Future work in this neighborhood should change the mechanism, for example by coupling alignment to an explicit orientation/line-state consensus or by using learned alignment confidence to protect center-frame evidence rather than merely fusing shifted previous/next features.

The next useful hypothesis should broaden away from this exact shift-bank scout toward a mechanism-changing temporal line-continuity design, temporal attention evidence sharpening, or single-frame C4/orientation recall support. Any next work must preserve provider-owned temporal input, trusted losses/metrics/Artifact Filters, coordinate exclusion, and Harness-owned resource policy.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260915_100642_28e66d/candidate/PROPOSAL.md`
- `run_20260915_100642_28e66d/candidate/README.md`
- `run_20260915_100642_28e66d/candidate/manifest.yaml`
- `run_20260915_100642_28e66d/resolved_manifest.yaml`
- `run_20260915_100642_28e66d/execution.json`
- `run_20260915_100642_28e66d/outputs/model_summary.json`
- `run_20260915_100642_28e66d/outputs/best_metrics.json`
- `run_20260915_100642_28e66d/outputs/final_metrics.json`
- `run_20260915_100642_28e66d/outputs/metrics.jsonl`
- `run_20260915_100642_28e66d/outputs/resource_profile.json`
- `run_20260915_100642_28e66d/outputs/validation_postprocessing/index.json`
- `run_20260915_100642_28e66d/outputs/prediction_samples/samples.json`
- `run_20260915_100315_94315b/outputs/logs/smoke_test.log` for the ABI-314 syntax failure repaired by ABI-315
- `run_20260915_015552_1ac51f/outputs/best_metrics.json` and `/history/research-notes/abi311-temporal-fiveframe-c4-persistence-contrast-line-state-late36.md` for ABI-311 comparison context
- `run_20260914_205014_1794f8/outputs/best_metrics.json` and `/history/research-notes/abi309-temporal-c4-late-line-support-recall-head-late36.md` for ABI-309 comparison context
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md` for ABI-306 comparison context
- `run_20260915_043533_14234b/outputs/best_metrics.json` and `/history/research-notes/abi312-temporal-fiveframe-selective-consensus-stabilized-late36.md` for ABI-312 comparison context
- `run_20260915_072045_06149f/outputs/best_metrics.json` and `/history/research-notes/abi313-temporal-fiveframe-continuity-protected-calibration-late36.md` for ABI-313 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
