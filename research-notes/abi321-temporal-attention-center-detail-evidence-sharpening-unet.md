# ABI-321 temporal-attention center-detail evidence-sharpening U-Net

research-figures: []

## Scope

This note records ABI-321, Candidate `abi321_temporal_attention_center_detail_evidence_sharpening_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260915_183315_3f1d30`.

ABI-321 was a bounded exploratory temporal-attention/evidence-sharpening continuation after the local shift-bank/C4 refinements ABI-319 and ABI-320. It consumed provider-owned three-frame temporal inputs with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, then combined lightweight temporal attention, zero-offset center-detail features, and a bounded architecture-internal multi-evidence mask-logit residual. The intended target was to recover fixed-threshold recall/source balance relative to ABI-319/320 without Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, temporal lookup, sampling, coordinates, or resource control.

This is capped temporal-eligible feasibility evidence only. It is not whole Working Validation Split promotion evidence and is not directly comparable to the full-validation ABI-202/249 frontier.

## Execution result

ABI-321 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs; no late-improving budget was requested.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,186,127, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 4,339,162,624 / 4,674,551,808 bytes.
- Training wall time: 1,246.6 s; validation wall time: 1,058.2 s; total Run wall time: 2,306.7 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 8.

## Best-validation metrics

| Metric | ABI-321 attention/detail sharpening | ABI-320 center-detail recall gate | ABI-319 shift-bank C4 confidence | ABI-315 shift-bank scout | ABI-223 temporal-attention comparator |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 8 | 9 | 10 | 12 | 36 |
| Filtered Dice | 0.380685 | 0.382100 | 0.405847 | 0.389886 | 0.419800 |
| MIT filtered Dice | 0.367130 | 0.366449 | 0.387897 | 0.377376 | 0.398500 |
| Google filtered Dice | 0.416557 | 0.420464 | 0.451369 | 0.420154 | 0.476800 |
| Filtered precision | 0.455716 | 0.415251 | 0.463906 | 0.412308 | 0.483800 |
| Filtered recall | 0.326867 | 0.353851 | 0.360703 | 0.369776 | 0.370700 |
| Filtered connectivity | 0.338630 | 0.365299 | 0.360704 | 0.266017 | 0.412400 |
| Filtered predicted-positive fraction | 0.003708 | 0.004405 | 0.004020 | 0.004636 | about 0.00396 |

ABI-321 did not achieve the intended recall-protected improvement. Relative to ABI-320 it is essentially tied on MIT Dice but lower on aggregate Dice, Google Dice, recall, and connectivity; its main improvement is higher precision and a smaller filtered footprint. Relative to ABI-319 it loses about 0.025 filtered Dice, 0.021 MIT Dice, 0.035 Google Dice, 0.034 recall, and 0.022 connectivity. Relative to ABI-315 it improves precision and connectivity, but loses aggregate/source Dice and recall. It remains well below the ABI-223 temporal-attention comparator on all target metrics.

At the selected checkpoint, raw Dice was 0.397785 versus filtered Dice 0.380685, raw recall was 0.353026 versus filtered recall 0.326867, and raw predicted-positive fraction was 0.004006 versus filtered predicted-positive fraction 0.003708. Artifact Filters reduce footprint and score; they do not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.232166 | 0.240466 | 0.214831 | 0.228046 | 0.236438 | 0.152603 | 0.005360 |
| 2 | 0.299842 | 0.292191 | 0.318945 | 0.353453 | 0.260353 | 0.226750 | 0.003808 |
| 3 | 0.323284 | 0.314362 | 0.343108 | 0.344843 | 0.304262 | 0.221446 | 0.004561 |
| 4 | 0.321736 | 0.306803 | 0.355639 | 0.372396 | 0.283209 | 0.247871 | 0.003931 |
| 5 | 0.355306 | 0.344297 | 0.381747 | 0.420333 | 0.307704 | 0.317328 | 0.003784 |
| 6 | 0.360970 | 0.345511 | 0.399800 | 0.432189 | 0.309902 | 0.324002 | 0.003707 |
| 7 | 0.349360 | 0.326030 | 0.408449 | 0.479323 | 0.274840 | 0.365955 | 0.002964 |
| 8 | 0.380685 | 0.367130 | 0.416557 | 0.455716 | 0.326867 | 0.338630 | 0.003708 |
| 9 | 0.368922 | 0.369040 | 0.368646 | 0.340423 | 0.402628 | 0.203516 | 0.006114 |
| 10 | 0.363897 | 0.346866 | 0.408381 | 0.467933 | 0.297707 | 0.291270 | 0.003289 |
| 11 | 0.366359 | 0.350773 | 0.405876 | 0.447337 | 0.310205 | 0.272545 | 0.003585 |
| 12 | 0.369274 | 0.351999 | 0.412329 | 0.426432 | 0.325627 | 0.242046 | 0.003948 |

The trajectory is finite and source-informative, but it does not support an unchanged late-improving continuation. The selected checkpoint occurs at epoch 8, not at the budget boundary. Epoch 9 briefly reaches high recall, but only by expanding the footprint and sharply lowering precision/connectivity and Google Dice. Epochs 10-12 do not recover the selected aggregate score, and connectivity degrades markedly by the final epoch. This looks like the same unstable precision/recall/connectivity calibration surface seen in nearby temporal head variants, not evidence that the exploratory budget simply truncated learning.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3680, 0.5391, 0.3858, and 0.4401. This confirms finite non-collapsed predictions with mixed retained-sample behavior, but it is not promotion evidence.

## Interpretation

Classify ABI-321 as a valid, resource-feasible, scientifically useful but negative temporal-attention evidence-sharpening scout. It successfully broadened away from the exact shift-bank/C4 head design and used a much smaller parameter/memory footprint than ABI-319/320, but the mechanism did not raise enough true contrail logits at threshold 0.5. The model tends toward a compact, moderately precise operating point; when recall increases, connectivity and source balance deteriorate.

The main lesson is that simply adding center-detail sharpening to a lightweight temporal-attention stem is not enough to recover the recall/source-balance gap. ABI-321 does not repair ABI-320's failure mode and remains materially below ABI-319, ABI-311, and ABI-223. It is also weaker than ABI-315 on aggregate/source Dice despite better connectivity, so the result does not justify replacing the recent shift-bank/C4 evidence path with this exact temporal-attention sharpening head.

## Decision

Do not promote ABI-321. Do not request a temporal-eligible failure-bucket evaluation for this capped exploratory Result: the aggregate/source/trajectory evidence already shows that the target recall and connected-line improvements were not achieved. Do not request an unchanged late36 continuation because the best checkpoint is mid-run and final metrics remain lower.

Record ABI-321 as bounded negative evidence for this exact lightweight temporal-attention center-detail evidence-sharpening design. Future work should be mechanism-changing rather than another direct gated-head refinement: either revisit ABI-223-style temporal attention with a stronger recall-protecting evidence path, return to ABI-249-style single-frame C4/orientation support plus center-detail recall, or explore a different line-continuity mechanism that stabilizes connected predictions without Candidate-owned thresholding or postprocessing.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260915_183315_3f1d30/candidate/PROPOSAL.md`
- `run_20260915_183315_3f1d30/candidate/README.md`
- `run_20260915_183315_3f1d30/candidate/manifest.yaml`
- `run_20260915_183315_3f1d30/resolved_manifest.yaml`
- `run_20260915_183315_3f1d30/execution.json`
- `run_20260915_183315_3f1d30/outputs/model_summary.json`
- `run_20260915_183315_3f1d30/outputs/best_metrics.json`
- `run_20260915_183315_3f1d30/outputs/final_metrics.json`
- `run_20260915_183315_3f1d30/outputs/metrics.jsonl`
- `run_20260915_183315_3f1d30/outputs/resource_profile.json`
- `run_20260915_183315_3f1d30/outputs/validation_postprocessing/index.json`
- `run_20260915_183315_3f1d30/outputs/prediction_samples/samples.json`
- `run_20260915_172705_4d6463/outputs/best_metrics.json` and `/history/research-notes/abi320-temporal-shiftbank-c4-center-detail-recall-gate-unet.md` for ABI-320 comparison context
- `run_20260915_162050_163586/outputs/best_metrics.json` and `/history/research-notes/abi319-temporal-shiftbank-c4-alignment-confidence-line-unet.md` for ABI-319 comparison context
- `run_20260915_100642_28e66d/outputs/best_metrics.json` and `/history/research-notes/abi315-temporal-shiftbank-alignment-detail-unet-syntax-repair.md` for ABI-315 comparison context
- `run_20260915_015552_1ac51f/outputs/best_metrics.json` and `/history/research-notes/abi311-temporal-fiveframe-c4-persistence-contrast-line-state-late36.md` for ABI-311 comparison context
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/aggregate_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
