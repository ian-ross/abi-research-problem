# ABI-361 temporal shift-aligned detail-consensus line support late36

research-figures: []

## Scope

This note records ABI-361, Candidate `abi361_temporal_shift_aligned_detail_consensus_line_support_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260919_233003_a91c98`.

ABI-361 was a close, mechanism-changing temporal family-development continuation after ABI-350/359/360 on the capped temporal-eligible GOES ABI Contrail Segmentation population. It kept provider-owned `abi_16ch_plus_sza_temporal` inputs with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, Line and Centerline auxiliary targets, AdamW with constant LR, and batch size 2. The architectural question was whether learned local integer-shift alignment of previous/next frame features to the center frame before temporal attention would recover displaced neighbor-frame detail, raising fixed-threshold recall/connectivity without broadening the prediction footprint.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence and should not be treated as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-361 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs, 10,800 s timeout.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,169,382, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated memory: 6,817,038,336 bytes.
- Training wall time: 5,152.0 s; validation wall time: 3,546.0 s; total Run wall time: 8,700.2 s, within the late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 27.

## Temporal-eligible aggregate metrics

| Metric | ABI-361 shift alignment | ABI-350 line support | ABI-359 early C4 alignment | ABI-360 stabilized head | ABI-356 recall parent |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 27 | 33 | 27 | 22 | 36 |
| Filtered Dice | 0.414944 | 0.431103 | 0.426759 | 0.424190 | 0.426056 |
| MIT filtered Dice | 0.388679 | 0.409536 | 0.406428 | 0.408971 | 0.411375 |
| Google filtered Dice | 0.482763 | 0.490518 | 0.481165 | 0.464689 | 0.465688 |
| Filtered precision | 0.456387 | 0.494306 | 0.474933 | 0.420281 | 0.421447 |
| Filtered recall | 0.380401 | 0.382230 | 0.387459 | 0.428173 | 0.430766 |
| Filtered connectivity | 0.298575 | 0.358283 | 0.376348 | 0.342524 | 0.282116 |
| Filtered positive fraction | 0.004309 | 0.003997 | 0.004217 | 0.005267 | 0.005284 |

ABI-361 is finite and source-informative, but it is a clear non-frontier result. The shift-alignment mechanism did not improve the intended precision/recall/connectivity trade-off. Relative to ABI-350 it loses -0.0162 filtered Dice, -0.0209 MIT Dice, -0.0078 Google Dice, -0.0379 precision, -0.0018 recall, and -0.0597 connectivity while predicting a slightly broader filtered-positive footprint. Relative to ABI-359 it loses aggregate Dice, MIT Dice, precision, recall, and connectivity; the only small positive is a +0.0016 Google Dice tie-level improvement.

Compared with ABI-360, ABI-361 is more compact and precise, but that comes by giving up -0.0478 recall and -0.0439 connectivity, so it does not solve the recall/connectivity weakness that motivated the shift-alignment block.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.197746 | 0.194699 | 0.205118 | 0.235497 | 0.170426 | 0.087198 | 0.003741 |
| 5 | 0.310219 | 0.291455 | 0.354779 | 0.341677 | 0.284065 | 0.215204 | 0.004298 |
| 10 | 0.374773 | 0.358194 | 0.418057 | 0.433820 | 0.329874 | 0.321804 | 0.003931 |
| 15 | 0.390089 | 0.366404 | 0.452740 | 0.474799 | 0.331030 | 0.371419 | 0.003604 |
| 20 | 0.388136 | 0.360866 | 0.462060 | 0.520788 | 0.309342 | 0.403781 | 0.003071 |
| 25 | 0.375285 | 0.358887 | 0.416491 | 0.410253 | 0.345810 | 0.212255 | 0.004358 |
| 27 | 0.414944 | 0.388679 | 0.482763 | 0.456387 | 0.380401 | 0.298575 | 0.004309 |
| 30 | 0.393273 | 0.370338 | 0.450056 | 0.462988 | 0.341805 | 0.265042 | 0.003816 |
| 31 | 0.401965 | 0.374903 | 0.470366 | 0.455988 | 0.359387 | 0.292780 | 0.004074 |
| 32 | 0.377261 | 0.349664 | 0.449101 | 0.525435 | 0.294275 | 0.314282 | 0.002895 |
| 33 | 0.369928 | 0.341644 | 0.445676 | 0.490953 | 0.296771 | 0.327647 | 0.003125 |
| 34 | 0.412094 | 0.389252 | 0.471230 | 0.472702 | 0.365261 | 0.305492 | 0.003995 |
| 35 | 0.371529 | 0.345405 | 0.438992 | 0.473927 | 0.305518 | 0.307196 | 0.003333 |
| 36 | 0.311721 | 0.301946 | 0.334162 | 0.321902 | 0.302164 | 0.146685 | 0.004853 |

The trajectory is finite but unstable. Epoch 20 produces the strongest connectivity state, but only by becoming too compact and recall-poor. Epoch 27 is the best aggregate checkpoint. Epoch 34 nearly recovers the best Dice with slightly higher MIT Dice but still lower Google Dice, recall, and connectivity. The final checkpoint remains non-collapsed but sharply regresses from best epoch by -0.1032 filtered Dice, -0.0866 MIT Dice, -0.1486 Google Dice, -0.1345 precision, -0.0782 recall, and -0.1519 connectivity. This late degradation argues against the shift-alignment block as a stabilizing temporal mechanism in this branch.

## Interpretation

Classify ABI-361 as a finite, resource-safe, negative temporal family-development result. The local shift-alignment idea is contract-safe and computationally feasible, but the capped evidence does not support the hypothesis that learned center alignment improves displaced neighbor-frame detail for fixed-threshold contrail segmentation. It neither matches ABI-350's aggregate/precision band nor ABI-359's connectivity, and it does not provide ABI-356/360-style recall.

Do not promote ABI-361. Do not spend another Run on an unchanged shift-aligned detail-consensus late36 continuation, a larger shift bank, or a simple gate-strength/head-weight shuffle in this same temporal-attention line-support branch. The recent ABI-350/356/358/359/360/361 sequence has repeatedly shown late-budget oscillation among compact precision, recall, and connectivity without a stable joint improvement.

A Post-Run Evaluation is not requested in this Autonomy Step. ABI-361 is below the capped temporal comparators on the intended metrics, so capped temporal-eligible metrics are enough to classify this exact mechanism as non-frontier. If future work continues, broaden the mechanism rather than locally tuning this branch: e.g. a single-frame C4/detail anchor with an architecture-level recall sidecar, a source-robust MIT-tail support path, or a genuinely different lightweight line-continuity decoder. Candidate-owned thresholds, calibration, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sampling, coordinates, Dataset Source identity, downloads, resource scheduling, and lifecycle changes remain out of scope.

## Decision

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260919_233003_a91c98/candidate/PROPOSAL.md`
- `run_20260919_233003_a91c98/candidate/README.md`
- `run_20260919_233003_a91c98/candidate/manifest.yaml`
- `run_20260919_233003_a91c98/candidate/budget_request.yaml`
- `run_20260919_233003_a91c98/resolved_manifest.yaml`
- `run_20260919_233003_a91c98/execution.json`
- `run_20260919_233003_a91c98/run_metadata.json`
- `run_20260919_233003_a91c98/outputs/model_summary.json`
- `run_20260919_233003_a91c98/outputs/best_metrics.json`
- `run_20260919_233003_a91c98/outputs/final_metrics.json`
- `run_20260919_233003_a91c98/outputs/metrics.jsonl`
- `run_20260919_233003_a91c98/outputs/resource_profile.json`
- `run_20260919_233003_a91c98/outputs/validation_postprocessing/index.json`
- `run_20260919_233003_a91c98/outputs/prediction_samples/samples.json`
- `run_20260919_013306_9ca44e/outputs/best_metrics.json` and `/history/research-notes/abi350-temporal-attention-predecoder-line-support-late36.md` for ABI-350 comparator context
- `run_20260919_175950_ac7b89/outputs/best_metrics.json` and `/history/research-notes/abi359-temporal-alignment-c4-center-detail-bridge-late36.md` for ABI-359 parent context
- `run_20260919_210615_da5139/outputs/best_metrics.json` and `/history/research-notes/abi360-temporal-attention-continuity-stabilized-line-support-late36.md` for ABI-360 parent context
- `run_20260919_095725_843317/outputs/best_metrics.json` and `/history/research-notes/abi356-temporal-attention-multiscale-change-line-fusion-late36.md` for ABI-356 recall parent context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
