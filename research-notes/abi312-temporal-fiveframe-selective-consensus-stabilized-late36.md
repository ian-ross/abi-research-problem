# ABI-312 temporal five-frame selective-consensus stabilized late36

research-figures: []

## Scope

This note records the bounded late-improving Result for ABI-312, Candidate `abi312_temporal_fiveframe_selective_consensus_stabilized_unet_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260915_043533_14234b`.

ABI-312 was a close temporal C4 family-development continuation after ABI-311. It kept the provider-owned five-frame temporal input (`abi_16ch_plus_sza_temporal`, `temporal_eligible_center`, offsets `[-2, -1, 0, 1, 2]`), BCE-Dice loss, combined source-balanced sampling, random mirroring, and trusted Line/Centerline auxiliary targets. The changed mechanism was a selective consensus stabilizer and small recall residual intended to preserve ABI-311's balanced five-frame persistence/contrast evidence while repairing MIT-heavy positive-patch undercoverage and typical connected-line continuity.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to the full Working Validation Split frontier.

## Execution result

ABI-312 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs; request approved as `late_improving_parent_completed`.
- Direct parents/comparators: ABI-311 (`run_20260915_015552_1ac51f`), ABI-306 (`run_20260914_124245_de843c`), and ABI-309 (`run_20260914_205014_1794f8`).
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-2, -1, 0, 1, 2]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,315,375, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 6.93 / 7.29 GiB.
- Total Run wall time: 9,349.6 s, within the 10,800 s late-improving timeout but materially costlier than ABI-311.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 27.

## Best-validation metrics

| Metric | ABI-312 selective consensus | ABI-311 five-frame persistence/contrast | Delta vs ABI-311 | ABI-306 compact C4 dual-evidence | Delta vs ABI-306 | ABI-309 recall head | Delta vs ABI-309 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 27 | 27 | +0 | 36 | -9 | 29 | -2 |
| Filtered Dice | 0.418688 | 0.425000 | -0.006312 | 0.422548 | -0.003860 | 0.423544 | -0.004856 |
| Raw Dice | 0.435450 | 0.442688 | -0.007238 | 0.441449 | -0.005999 | 0.439038 | -0.003588 |
| MIT filtered Dice | 0.397405 | 0.403831 | -0.006426 | 0.402764 | -0.005359 | 0.402446 | -0.005041 |
| Google filtered Dice | 0.472780 | 0.482615 | -0.009836 | 0.476152 | -0.003372 | 0.478510 | -0.005731 |
| Filtered precision | 0.425069 | 0.459703 | -0.034635 | 0.493422 | -0.068353 | 0.401806 | +0.023263 |
| Filtered recall | 0.412496 | 0.395169 | +0.017328 | 0.369478 | +0.043018 | 0.447768 | -0.035272 |
| Filtered connectivity | 0.261236 | 0.366735 | -0.105499 | 0.299384 | -0.038148 | 0.316074 | -0.054838 |
| Filtered predicted-positive fraction | 0.005017 | 0.004444 | +0.000573 | 0.003871 | +0.001146 | 0.005761 | -0.000744 |
| Filtered predicted-positive pixels | 530,639 | 470,049 | +60,590 | 409,457 | +121,182 | 609,361 | -78,722 |

ABI-312 is finite and non-collapsed, but it is a negative/mixed continuation of ABI-311 rather than a local frontier improvement. The selective consensus stabilizer did raise fixed-threshold recall versus ABI-311 (+0.0173), but it did so with a larger footprint, lower precision, lower MIT and Google filtered Dice, and a large connectivity regression. It also falls below ABI-306 and ABI-309 on aggregate filtered Dice, and below ABI-223/ABI-238 temporal-family comparators in the current index.

The specific intended repair did not materialize. ABI-312 does not improve MIT filtered Dice over ABI-311, ABI-306, or ABI-309, and its aggregate connectivity is far below ABI-311's selected checkpoint. The added selective residual appears to have shifted the operating point toward broader recall without preserving the connected-line quality that made ABI-311 valuable.

At the selected checkpoint, raw Dice was 0.435450 versus filtered Dice 0.418688, raw recall was 0.445970 versus filtered recall 0.412496, and raw predicted-positive pixels were 573,234 versus 530,639 filtered. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.255628 | 0.252489 | 0.263572 | 0.320937 | 0.212404 | 0.220641 | 0.003421 |
| 3 | 0.298808 | 0.292895 | 0.310832 | 0.261398 | 0.348712 | 0.172840 | 0.006896 |
| 5 | 0.343890 | 0.326020 | 0.388165 | 0.390825 | 0.307020 | 0.247376 | 0.004061 |
| 8 | 0.375211 | 0.354076 | 0.431196 | 0.483159 | 0.306690 | 0.388822 | 0.003281 |
| 11 | 0.364405 | 0.336104 | 0.436314 | 0.453883 | 0.304397 | 0.318954 | 0.003467 |
| 15 | 0.399094 | 0.374834 | 0.461716 | 0.483232 | 0.339910 | 0.366544 | 0.003636 |
| 19 | 0.374188 | 0.345737 | 0.448237 | 0.479457 | 0.306822 | 0.313181 | 0.003308 |
| 23 | 0.389132 | 0.363371 | 0.454625 | 0.451810 | 0.341726 | 0.281015 | 0.003910 |
| 27 | 0.418688 | 0.397405 | 0.472780 | 0.425069 | 0.412496 | 0.261236 | 0.005017 |
| 29 | 0.408147 | 0.379415 | 0.481335 | 0.498992 | 0.345285 | 0.386205 | 0.003577 |
| 31 | 0.413890 | 0.394143 | 0.462181 | 0.440687 | 0.390165 | 0.239222 | 0.004577 |
| 34 | 0.402314 | 0.382711 | 0.451573 | 0.453522 | 0.361497 | 0.257694 | 0.004121 |
| 36 | 0.406585 | 0.380766 | 0.473497 | 0.508799 | 0.338570 | 0.302871 | 0.003440 |

The trajectory is finite, source-informative, and late-budget-dependent, with the best aggregate checkpoint again at epoch 27. It is also unstable: precision/recall/connectivity trade-offs move substantially after epoch 27, and the final epoch improves precision while losing recall and aggregate Dice. Unlike ABI-311, the late checkpoint does not define a better balanced operating point; it confirms that the selective consensus residual creates a volatile trade-off rather than stabilizing ABI-311's epoch-27 behavior.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.4702, approximately 0.0000, 0.3800, and 0.4141. This is consistent with finite non-collapsed predictions but includes a complete or near-complete miss in the fixed sample set. It does not establish promotion evidence.

## Interpretation

Classify ABI-312 as valid negative/mixed temporal C4 family-development evidence. The run answers the immediate ABI-311 continuation question: this selective consensus stabilizer and recall residual did not preserve the five-frame persistence/contrast branch's useful balance. It added recall, but at the cost of lower filtered Dice on both sources and a pronounced connected-line continuity regression.

Comparator roles after ABI-312 remain unchanged:

- ABI-311 remains the best balanced five-frame persistence/contrast temporal C4 comparator on capped temporal-eligible evidence.
- ABI-306 remains the compact high-precision temporal C4 comparator.
- ABI-309 remains the recall-heavy temporal C4 diagnostic variant with known footprint cost.
- ABI-223 remains the stronger temporal-attention continuity comparator because its connectivity remains much higher.
- ABI-312 should not become a new frontier target or parent for an unchanged continuation.

The result does not justify a temporal-eligible failure-bucket evaluation as the next primary action: the aggregate metrics already show regression on the targeted MIT/source-balance and connectivity mechanisms. A future diagnostic would be useful only if the campaign later needs to understand ABI-312's specific complete-miss pattern, not for frontier selection.

## Decision

Do not promote ABI-312 and do not submit an unchanged ABI-312 late36 continuation. Treat it as evidence that the current selective consensus residual is too blunt: it raises some fixed-threshold positives but disrupts the connectivity/source balance achieved by ABI-311.

The next useful hypothesis should be mechanism-changing rather than another ABI-311/312 head interpolation. Options include returning to ABI-311 as the balanced temporal comparator and testing a different continuity-preserving calibration design, or broadening away from temporal C4 residual heads toward a different temporal attention/line-continuity mechanism. Any continuation must preserve provider-owned temporal input, trusted losses/metrics/Artifact Filters, coordinate exclusion, and Harness-owned resource policy.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260915_043533_14234b/candidate/PROPOSAL.md`
- `run_20260915_043533_14234b/candidate/README.md`
- `run_20260915_043533_14234b/candidate/manifest.yaml`
- `run_20260915_043533_14234b/candidate/budget_request.yaml`
- `run_20260915_043533_14234b/resolved_manifest.yaml`
- `run_20260915_043533_14234b/execution.json`
- `run_20260915_043533_14234b/outputs/model_summary.json`
- `run_20260915_043533_14234b/outputs/best_metrics.json`
- `run_20260915_043533_14234b/outputs/final_metrics.json`
- `run_20260915_043533_14234b/outputs/metrics.jsonl`
- `run_20260915_043533_14234b/outputs/resource_profile.json`
- `run_20260915_043533_14234b/outputs/validation_postprocessing/index.json`
- `run_20260915_043533_14234b/outputs/prediction_samples/samples.json`
- `run_20260915_015552_1ac51f/outputs/best_metrics.json` and `/history/research-notes/abi311-temporal-fiveframe-c4-persistence-contrast-line-state-late36.md` for ABI-311 parent comparison context
- `/history/research-notes/abi311-temporal-eligible-failure-bucket-review.md` for ABI-311 diagnostic context
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md` for ABI-306 comparator context
- `run_20260914_205014_1794f8/outputs/best_metrics.json` and `/history/research-notes/abi309-temporal-c4-late-line-support-recall-head-late36.md` for ABI-309 comparator context
- `run_20260914_232554_0320e8/outputs/best_metrics.json` and `/history/research-notes/abi310-temporal-c4-agreement-gated-line-support-late36.md` for ABI-310 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-attention-fusion-unet-late36.md` for temporal-attention comparator context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 temporal directional-context comparator context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
