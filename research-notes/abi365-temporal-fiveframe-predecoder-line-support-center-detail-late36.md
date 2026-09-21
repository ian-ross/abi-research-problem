# ABI-365 temporal five-frame pre-decoder line-support center-detail late36

research-figures: []

## Scope

This note records ABI-365, Candidate `abi365_temporal_fiveframe_predecoder_line_support_center_detail_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260920_081530_7577c1`.

ABI-365 was a mechanism-changing temporal family-development continuation after ABI-350 and the recent ABI-356/359/360/361 temporal line-support sequence. It kept provider-owned `abi_16ch_plus_sza_temporal` inputs with trusted `temporal_eligible_center` selection, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, Line and Centerline auxiliary targets, AdamW with constant LR, and batch size 2. The architectural change was to extend ABI-350's three-frame pre-decoder orientation line-support idea to five trusted offsets `[-2, -1, 0, 1, 2]`, using center-anchored near/far temporal-change evidence before decoder fusion.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence and should not be treated as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-365 completed without contract, smoke, shape, numerical, resource, or lifecycle failure. The requested late-improving budget was approved.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs, 10,800 s timeout.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-2, -1, 0, 1, 2]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,134,724, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 4,877,475,328 / 5,408,555,008 bytes.
- Training wall time: 4,308.6 s; validation wall time: 3,254.3 s; total Run wall time: 7,565.0 s, within the late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 31.

## Temporal-eligible aggregate metrics

| Metric | ABI-365 five-frame pre-decoder line support | ABI-350 three-frame line support | ABI-324 balanced five-frame C4 | ABI-348 compact five-frame C4 | ABI-223 temporal attention | ABI-356 recall parent | ABI-360 stabilized head |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 31 | 33 | 27 | 36 | 36 | 36 | 22 |
| Filtered Dice | 0.407516 | 0.431103 | 0.429430 | 0.427829 | 0.419776 | 0.426056 | 0.424190 |
| MIT filtered Dice | 0.384403 | 0.409536 | 0.408188 | 0.410244 | 0.398498 | 0.411375 | 0.408971 |
| Google filtered Dice | 0.465848 | 0.490518 | 0.487231 | 0.478363 | 0.476764 | 0.465688 | 0.464689 |
| Filtered precision | 0.459703 | 0.494306 | 0.470412 | 0.477546 | 0.483764 | 0.421447 | 0.420281 |
| Filtered recall | 0.365970 | 0.382230 | 0.395017 | 0.387488 | 0.370738 | 0.430766 | 0.428173 |
| Filtered connectivity | 0.297708 | 0.358283 | 0.397925 | 0.300904 | 0.412427 | 0.282116 | 0.342524 |
| Filtered predicted-positive pixels | 435,318 | 422,831 | 459,172 | 443,691 | 419,056 | 558,903 | 557,080 |

ABI-365 is finite and source-informative, but it is negative evidence for this exact five-frame pre-decoder line-support mechanism. Relative to ABI-350, it loses -0.0236 aggregate filtered Dice, -0.0251 MIT Dice, -0.0247 Google Dice, -0.0346 precision, -0.0163 recall, and -0.0606 connectivity while predicting a slightly larger footprint (+12,487 filtered-positive pixels). The move from three frames to five frames did not improve persistence, continuity, source balance, or recall.

Relative to ABI-324, ABI-365 loses -0.0219 aggregate Dice, -0.0238 MIT Dice, -0.0214 Google Dice, -0.0107 precision, -0.0290 recall, and -0.1002 connectivity. It also remains below ABI-223 on aggregate/source Dice, precision, recall, and especially connectivity. Compared with ABI-356/360 recall-biased variants, ABI-365 is more compact and precise but gives up substantial recall and does not recover enough connectivity to be useful.

The only narrow positive is that ABI-365 roughly matches ABI-356/360 on Google Dice while keeping a smaller footprint. That does not support the stated hypothesis because the intended target was connected true-contrail evidence and MIT/source-balanced recall, not another compact-but-under-recalling temporal state.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive pixels |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.217460 | 0.210440 | 0.233573 | 0.284235 | 0.176092 | 0.157390 | 338,766 |
| 6 | 0.328240 | 0.307273 | 0.380025 | 0.400245 | 0.278193 | 0.248838 | 380,065 |
| 12 | 0.374856 | 0.350224 | 0.437267 | 0.483446 | 0.306035 | 0.344293 | 326,418 |
| 20 | 0.382828 | 0.366271 | 0.423116 | 0.425734 | 0.347787 | 0.239842 | 420,987 |
| 27 | 0.346568 | 0.323395 | 0.410332 | 0.599704 | 0.243702 | 0.450822 | 222,208 |
| 28 | 0.404519 | 0.386420 | 0.450002 | 0.431804 | 0.380476 | 0.271435 | 481,813 |
| 29 | 0.404880 | 0.380236 | 0.467349 | 0.442715 | 0.373002 | 0.335866 | 460,707 |
| 30 | 0.382852 | 0.354025 | 0.457934 | 0.509620 | 0.306588 | 0.375208 | 328,963 |
| 31 | 0.407516 | 0.384403 | 0.465848 | 0.459703 | 0.365970 | 0.297708 | 435,318 |
| 32 | 0.406572 | 0.383182 | 0.467734 | 0.507175 | 0.339274 | 0.380340 | 365,789 |
| 34 | 0.406089 | 0.386878 | 0.454621 | 0.461002 | 0.362865 | 0.242344 | 430,408 |
| 36 | 0.403268 | 0.390056 | 0.438492 | 0.354337 | 0.467877 | 0.220251 | 722,028 |

The late trajectory is finite but unstable. Epoch 27 reaches high connectivity (0.4508), but only in a very compact, low-recall state with weak aggregate Dice. Epoch 32 has better connectivity than the selected checkpoint, but gives up recall and aggregate Dice. The final epoch broadens sharply into a high-recall, low-precision, low-connectivity state. The five-frame near/far temporal evidence therefore separates into incompatible operating points instead of stabilizing the desired joint Dice/recall/connectivity solution.

## Interpretation

Classify ABI-365 as a finite, resource-safe, negative temporal family-development result. The five-frame input/resource class is feasible, and the candidate respected the provider-owned temporal boundary, but the architectural hypothesis is not supported. Extending ABI-350's pre-decoder line-support mechanism from three frames to five frames did not preserve ABI-350's compact aggregate strength, did not improve ABI-324/223-style connected-line continuity, and did not deliver ABI-356/360-style recall.

Do not promote ABI-365. Do not spend another Run on an unchanged five-frame pre-decoder line-support late36 continuation, simple gate-strength tuning, or another near/far residual shuffle on this scaffold. The recent ABI-350/356/359/360/361/365 sequence has enough bounded evidence that local temporal line-support variants oscillate among compact precision, broad recall, and transient connectivity without stable joint improvement.

A Post-Run Evaluation is not requested in this Autonomy Step. ABI-365 is below the temporal-eligible capped comparators on the intended aggregate, source-balance, recall, and connectivity metrics, so capped metrics are enough to classify this exact mechanism as non-frontier. If temporal work continues, it should broaden the mechanism rather than locally tuning this branch: for example, a genuinely different temporal backbone, a source-robust MIT-positive-tail path, architecture-level calibration/dual-evidence heads that preserve recall at threshold 0.5, or a single-frame C4/detail anchor with explicit recall support. Candidate-owned thresholds, calibration, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sampling, coordinates, Dataset Source identity, downloads, resource scheduling, and lifecycle changes remain out of scope.

## Decision

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260920_081530_7577c1/candidate/PROPOSAL.md`
- `run_20260920_081530_7577c1/candidate/README.md`
- `run_20260920_081530_7577c1/candidate/manifest.yaml`
- `run_20260920_081530_7577c1/candidate/budget_request.yaml`
- `run_20260920_081530_7577c1/resolved_manifest.yaml`
- `run_20260920_081530_7577c1/execution.json`
- `run_20260920_081530_7577c1/run_metadata.json`
- `run_20260920_081530_7577c1/outputs/model_summary.json`
- `run_20260920_081530_7577c1/outputs/best_metrics.json`
- `run_20260920_081530_7577c1/outputs/final_metrics.json`
- `run_20260920_081530_7577c1/outputs/metrics.jsonl`
- `run_20260920_081530_7577c1/outputs/resource_profile.json`
- `run_20260920_081530_7577c1/outputs/validation_postprocessing/index.json`
- `run_20260920_081530_7577c1/outputs/prediction_samples/samples.json`
- `run_20260919_013306_9ca44e/outputs/best_metrics.json` and `/history/research-notes/abi350-temporal-attention-predecoder-line-support-late36.md` for ABI-350 comparator context
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-eligible-failure-bucket-review.md` for ABI-324 comparator context
- `run_20260918_215534_a35ab9/outputs/best_metrics.json` and `/history/research-notes/abi348-temporal-fiveframe-dual-state-connectivity-blend-late36.md` for ABI-348 comparator context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/reference/EXPERIMENT_INDEX.md` for ABI-223 comparator context
- `run_20260919_095725_843317/outputs/best_metrics.json` and `/history/research-notes/abi356-temporal-attention-multiscale-change-line-fusion-late36.md` for ABI-356 comparator context
- `run_20260919_210615_da5139/outputs/best_metrics.json` and `/history/research-notes/abi360-temporal-attention-continuity-stabilized-line-support-late36.md` for ABI-360 comparator context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
