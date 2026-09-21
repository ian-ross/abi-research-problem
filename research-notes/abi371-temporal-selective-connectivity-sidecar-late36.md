# ABI-371 temporal selective connectivity sidecar late36

research-figures: []

## Scope

This note records ABI-371, Candidate `abi371_temporal_selective_connectivity_sidecar_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260920_202930_7bf6ec`.

ABI-371 was a mechanism-changing continuation of ABI-350. It kept provider-owned `abi_16ch_plus_sza_temporal` inputs with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, Line and Centerline auxiliary targets, AdamW with constant LR, and batch size 2. The architectural change was a bounded high-resolution selective connectivity sidecar added to the ABI-350 temporal-attention pre-decoder line-support scaffold.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence and should not be treated as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-371 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs, 10,800 s timeout.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: within the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 5,238,270,464 / 5,901,385,728 bytes.
- Training wall time: 4,680.7 s; validation wall time: 3,285.8 s; total Run wall time: 7,968.6 s, within the late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 27.

## Temporal-eligible aggregate metrics

| Metric | ABI-371 selective connectivity sidecar | ABI-350 line support | ABI-370 clDice diagnostic | ABI-369 no mirroring | ABI-324 balanced five-frame C4 | ABI-223 temporal attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 27 | 33 | 27 | 36 | 27 | 36 |
| Filtered Dice | 0.424489 | 0.431103 | 0.417655 | 0.429268 | 0.429430 | 0.419776 |
| MIT filtered Dice | 0.403669 | 0.409536 | 0.400297 | 0.414658 | 0.408188 | 0.398498 |
| Google filtered Dice | 0.480765 | 0.490518 | 0.463287 | 0.467429 | 0.487231 | 0.476764 |
| Filtered precision | 0.465804 | 0.494306 | 0.434434 | 0.454607 | 0.470412 | 0.483764 |
| Filtered recall | 0.389905 | 0.382230 | 0.402124 | 0.406604 | 0.395017 | 0.370738 |
| Filtered connectivity | 0.320953 | 0.358283 | 0.417017 | 0.298437 | 0.397925 | 0.412427 |
| Filtered predicted-positive pixels | 457,714 | 422,831 | 506,144 | 489,073 | 459,172 | 419,056 |

ABI-371 is finite and source-informative, but it is negative/mixed evidence for this exact selective connectivity sidecar. Relative to ABI-350, it gains only +0.0077 recall while losing -0.0066 aggregate filtered Dice, -0.0059 MIT Dice, -0.0098 Google Dice, -0.0285 precision, and -0.0373 connectivity, with +34,883 more filtered-positive pixels. The intended goal was to recover connected-line evidence while preserving ABI-350 compactness; the selected checkpoint does not do so.

Relative to ABI-370, ABI-371 is more compact and higher precision, but it gives back most of ABI-370's connectivity gain. Relative to ABI-369, it has better Google Dice, precision, and connectivity, but lower aggregate Dice, MIT Dice, and recall. Relative to ABI-324 and ABI-223, it remains below the relevant balanced/connectivity comparators. The result therefore moves within the already characterized precision/recall/connectivity triangle rather than breaking it.

Raw versus filtered behavior shows ordinary Artifact Filter behavior rather than filter-created performance. At the selected checkpoint, raw Dice was 0.442656 versus filtered Dice 0.424489, raw recall was 0.421893 versus filtered recall 0.389905, and raw predicted-positive pixels were 495,515 versus 457,714 filtered. Artifact Filters removed 37,801 predicted-positive pixels and lowered the score.

## Interpretation

Classify ABI-371 as finite, resource-safe, mechanistically informative, but non-frontier. The sidecar did not reproduce ABI-370's high-connectivity state and did not preserve ABI-350's compact high-precision aggregate behavior. It also did not surpass ABI-324's balanced temporal C4/detail-consensus evidence or ABI-223's mature temporal-attention connectivity signal.

Do not promote ABI-371. Do not spend another Run on an unchanged ABI-371 selective connectivity sidecar, a sidecar gain tweak, auxiliary-weight shuffle, or simple late-head residual repeat. The recent ABI-350/369/370/371 sequence provides enough bounded evidence that local temporal line-support sidecars and loss/policy swaps tend to move along the compactness/recall/connectivity trade-off rather than breaking it.

Future work should broaden the mechanism. High-value directions include local motion/correlation temporal alignment before decoder fusion, compact anchor plus selective recall verifier, source-robust high-resolution detail support, or line-aware lightweight backbones that explicitly preserve compact precision while improving MIT-positive-tail recall and connected thin-line continuity. Candidate-owned thresholds, calibration, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, and lifecycle changes remain out of scope.

A Post-Run Evaluation is not requested in this note. ABI-371 did not exceed ABI-350 aggregate/precision behavior and did not improve connectivity; capped temporal-eligible metrics are sufficient to classify this exact branch.

## Decision

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this note. ABI-371 is not a new comparator. ABI-350 remains the temporal-eligible capped aggregate/precision comparator, ABI-324 remains the balanced temporal C4/detail-consensus comparator, ABI-223 remains the mature temporal-attention connectivity diagnostic comparator, and ABI-370 remains only a trusted-loss connectivity diagnostic.

## Artifact references

- `run_20260920_202930_7bf6ec/candidate/PROPOSAL.md`
- `run_20260920_202930_7bf6ec/candidate/README.md`
- `run_20260920_202930_7bf6ec/candidate/manifest.yaml`
- `run_20260920_202930_7bf6ec/candidate/budget_request.yaml`
- `run_20260920_202930_7bf6ec/resolved_manifest.yaml`
- `run_20260920_202930_7bf6ec/execution.json`
- `run_20260920_202930_7bf6ec/run_metadata.json`
- `run_20260920_202930_7bf6ec/outputs/model_summary.json`
- `run_20260920_202930_7bf6ec/outputs/best_metrics.json`
- `run_20260920_202930_7bf6ec/outputs/final_metrics.json`
- `run_20260920_202930_7bf6ec/outputs/metrics.jsonl`
- `run_20260920_202930_7bf6ec/outputs/resource_profile.json`
- `run_20260920_202930_7bf6ec/outputs/validation_postprocessing/index.json`
- `run_20260919_013306_9ca44e/outputs/best_metrics.json` and `/history/research-notes/abi350-temporal-attention-predecoder-line-support-late36.md` for ABI-350 context
- `run_20260920_180416_4cefdd/outputs/best_metrics.json` and `/history/research-notes/abi370-temporal-attention-predecoder-line-support-cldice-late36.md` for ABI-370 context
- `run_20260920_155638_988238/outputs/best_metrics.json` and `/history/research-notes/abi369-temporal-attention-predecoder-line-support-no-mirroring-late36.md` for ABI-369 context
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-eligible-failure-bucket-review.md` for ABI-324 context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/reference/EXPERIMENT_INDEX.md` for ABI-223 context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
