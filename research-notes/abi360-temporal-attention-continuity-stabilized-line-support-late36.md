# ABI-360 temporal-attention continuity-stabilized line support late36

research-figures: []

## Scope

This note records ABI-360, Candidate `abi360_temporal_attention_continuity_stabilized_line_support_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260919_210615_da5139`.

ABI-360 was a close, mechanism-changing temporal family-development continuation after ABI-350/358/359 on the capped temporal-eligible GOES ABI Contrail Segmentation population. It kept provider-owned `abi_16ch_plus_sza_temporal` inputs with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, Line and Centerline auxiliary targets, AdamW with constant LR, and batch size 2. The architectural question was whether a continuity-stabilized evidence head on top of the ABI-350 pre-decoder line-support U-Net could preserve compact fixed-threshold Dice while injecting more stable connected-line evidence than the recent C4/continuity parents.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence and should not be treated as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-360 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs, 10,800 s timeout.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,194,652, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated memory: 5,275,393,024 bytes.
- Training wall time: 4,697.1 s; validation wall time: 3,288.3 s; total Run wall time: 7,987.6 s, within the late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 22.

## Temporal-eligible aggregate metrics

| Metric | ABI-360 stabilized head | ABI-350 line support | ABI-359 early C4 alignment | ABI-358 C4 sidecar | ABI-356 recall parent |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 22 | 33 | 27 | 30 | 36 |
| Filtered Dice | 0.424190 | 0.431103 | 0.426759 | 0.427570 | 0.426056 |
| MIT filtered Dice | 0.408971 | 0.409536 | 0.406428 | 0.405720 | 0.411375 |
| Google filtered Dice | 0.464689 | 0.490518 | 0.481165 | 0.484984 | 0.465688 |
| Filtered precision | 0.420281 | 0.494306 | 0.474933 | 0.485745 | 0.421447 |
| Filtered recall | 0.428173 | 0.382230 | 0.387459 | 0.381839 | 0.430766 |
| Filtered connectivity | 0.342524 | 0.358283 | 0.376348 | 0.290228 | 0.282116 |
| Filtered positive fraction | 0.005267 | 0.003997 | 0.004217 | 0.004064 | 0.005284 |

ABI-360 is finite and recall-positive, but it is not a new temporal frontier. It does not preserve ABI-350/358-style compact precision: compared with ABI-350 it gives up -0.0069 filtered Dice, -0.0740 precision, -0.0158 connectivity, and substantially broadens the predicted-positive footprint, while gaining +0.0459 recall. Compared with ABI-358, it similarly gives up aggregate Dice and precision, but improves recall and connectivity. Compared with ABI-359, it has higher recall but lower aggregate Dice, lower Google Dice, lower precision, and lower connectivity.

The useful signal is that the continuity-stabilized evidence head avoids collapse and finds a source-informative recall operating point: MIT filtered Dice remains close to ABI-350/359/358, and the selected checkpoint nearly matches ABI-356 recall with slightly better connectivity and slightly smaller footprint. The negative signal is that this recall comes through a broad, low-precision state rather than through the intended compact continuity stabilization.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.219702 | 0.224352 | 0.210096 | 0.216384 | 0.223124 | 0.123125 | 0.005331 |
| 5 | 0.332499 | 0.310318 | 0.385939 | 0.400924 | 0.284024 | 0.273194 | 0.003662 |
| 10 | 0.374798 | 0.349101 | 0.439791 | 0.455255 | 0.318508 | 0.314704 | 0.003617 |
| 15 | 0.401873 | 0.383649 | 0.449732 | 0.421727 | 0.383805 | 0.315112 | 0.004705 |
| 20 | 0.393099 | 0.368599 | 0.459166 | 0.496774 | 0.325225 | 0.377697 | 0.003384 |
| 22 | 0.424190 | 0.408971 | 0.464689 | 0.420281 | 0.428173 | 0.342524 | 0.005267 |
| 25 | 0.397388 | 0.374671 | 0.456491 | 0.450655 | 0.355382 | 0.289824 | 0.004077 |
| 30 | 0.396095 | 0.371814 | 0.459596 | 0.524469 | 0.318208 | 0.367396 | 0.003137 |
| 32 | 0.395068 | 0.375992 | 0.442700 | 0.442627 | 0.356737 | 0.212553 | 0.004166 |
| 33 | 0.377653 | 0.357583 | 0.429908 | 0.461735 | 0.319475 | 0.252900 | 0.003577 |
| 34 | 0.404239 | 0.384530 | 0.456299 | 0.461685 | 0.359507 | 0.234577 | 0.004025 |
| 35 | 0.361378 | 0.336394 | 0.430824 | 0.541873 | 0.271082 | 0.381512 | 0.002586 |
| 36 | 0.393171 | 0.371244 | 0.451528 | 0.459684 | 0.343473 | 0.267224 | 0.003863 |

The trajectory is finite but unstable. Epoch 22 is the best balanced point and is recall-heavy. Later high-precision/high-connectivity states appear at epochs 30 and 35, but they suppress recall too much and lose aggregate Dice. The final checkpoint remains non-collapsed but regresses from the selected checkpoint by -0.0310 filtered Dice, -0.0377 MIT Dice, -0.0132 Google Dice, -0.0847 recall, and -0.0753 connectivity. This pattern suggests the head can move among recall, precision, and continuity states, but it does not stabilize a joint high-Dice/high-connectivity operating point.

## Interpretation

Classify ABI-360 as a finite, resource-safe, mixed but non-frontier temporal family-development result. The mechanism partly supports recall: it recovers ABI-356-like recall while maintaining better connectivity than ABI-356/358. However, the intended compact continuity stabilization is not supported. ABI-360 remains below ABI-350, ABI-358, and ABI-359 on aggregate filtered Dice; below ABI-350/359 on connectivity; and substantially below ABI-350/358/359 on precision.

Do not promote ABI-360. Do not spend another Run on an unchanged continuity-stabilized evidence-head late36 continuation or a simple gate-strength/head-weight shuffle. The exact branch has now shown the same late-budget oscillation seen in ABI-350/358/359, but with a weaker best fixed-threshold trade-off.

A Post-Run Evaluation is not requested in this Autonomy Step. ABI-360 did not exceed the ABI-350 aggregate/precision frontier and did not improve connectivity over ABI-359, so capped temporal-eligible metrics are enough to classify this exact head as non-frontier. If future temporal work continues, it should broaden the mechanism rather than locally tune this head: for example, a different temporal alignment/backbone, a source-agnostic MIT-positive-tail support path, or a single-frame C4/detail mechanism that raises fixed-threshold true-positive logits without broadening negative-patch clutter. Candidate-owned thresholds, calibration, postprocessing, losses, metrics, data loading, temporal lookup, sampling, coordinates, Dataset Source identity, downloads, resource scheduling, and lifecycle changes remain out of scope.

## Decision

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260919_210615_da5139/candidate/PROPOSAL.md`
- `run_20260919_210615_da5139/candidate/README.md`
- `run_20260919_210615_da5139/candidate/manifest.yaml`
- `run_20260919_210615_da5139/candidate/budget_request.yaml`
- `run_20260919_210615_da5139/resolved_manifest.yaml`
- `run_20260919_210615_da5139/execution.json`
- `run_20260919_210615_da5139/run_metadata.json`
- `run_20260919_210615_da5139/outputs/model_summary.json`
- `run_20260919_210615_da5139/outputs/best_metrics.json`
- `run_20260919_210615_da5139/outputs/final_metrics.json`
- `run_20260919_210615_da5139/outputs/metrics.jsonl`
- `run_20260919_210615_da5139/outputs/resource_profile.json`
- `run_20260919_210615_da5139/outputs/validation_postprocessing/index.json`
- `run_20260919_210615_da5139/outputs/prediction_samples/samples.json`
- `run_20260919_013306_9ca44e/outputs/best_metrics.json` and `/history/research-notes/abi350-temporal-attention-predecoder-line-support-late36.md` for ABI-350 comparator context
- `run_20260919_175950_ac7b89/outputs/best_metrics.json` and `/history/research-notes/abi359-temporal-alignment-c4-center-detail-bridge-late36.md` for ABI-359 parent context
- `run_20260919_151507_2ec383/outputs/best_metrics.json` and `/history/research-notes/abi358-temporal-recall-preserving-c4-sidecar-late36.md` for ABI-358 parent context
- `run_20260919_095725_843317/outputs/best_metrics.json` and `/history/research-notes/abi356-temporal-attention-multiscale-change-line-fusion-late36.md` for ABI-356 recall parent context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
