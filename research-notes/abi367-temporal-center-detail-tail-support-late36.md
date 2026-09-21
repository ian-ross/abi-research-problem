# ABI-367 temporal center-detail tail support late36

research-figures: []

## Scope

This note records ABI-367, Candidate `abi367_temporal_center_detail_tail_support_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260920_112921_1ee9bd`.

ABI-367 was a temporal family-development continuation of ABI-350. It kept provider-owned `abi_16ch_plus_sza_temporal` inputs with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, Line and Centerline auxiliary targets, AdamW with constant learning rate, and batch size 2. The architectural question was whether an ABI-350-style temporal-attention U-Net with pre-decoder line-support gates could benefit from a bounded source-agnostic center-frame detail tail injected after high-resolution decoder fusion through an architecture-internal line-evidence gate.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence and should not be treated as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-367 completed without contract, smoke, shape, numerical, resource, or lifecycle failure. The requested late-improving budget was approved.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, 36 epochs, 10,800 s timeout.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,197,100, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 5,368,559,616 / 5,949,620,224 bytes.
- Training wall time: 4,747.7 s; validation wall time: 3,264.7 s; total Run wall time: 8,014.6 s, within the late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 27.

## Temporal-eligible aggregate metrics

| Metric | ABI-367 center-detail tail | ABI-350 line support | ABI-359 C4/detail bridge | ABI-356 recall fusion | ABI-365 five-frame line support | ABI-223 temporal attention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 27 | 33 | 27 | 36 | 31 | 36 |
| Filtered Dice | 0.420955 | 0.431103 | 0.426759 | 0.426056 | 0.407516 | 0.419776 |
| MIT filtered Dice | 0.404132 | 0.409536 | 0.406428 | 0.411375 | 0.384403 | 0.398498 |
| Google filtered Dice | 0.465751 | 0.490518 | 0.481165 | 0.465688 | 0.465848 | 0.476764 |
| Filtered precision | 0.459504 | 0.494306 | 0.474933 | 0.421447 | 0.459703 | 0.483764 |
| Filtered recall | 0.388373 | 0.382230 | 0.387459 | 0.430766 | 0.365970 | 0.370738 |
| Filtered connectivity | 0.245025 | 0.358283 | 0.376348 | 0.282116 | 0.297708 | 0.412427 |
| Filtered predicted-positive pixels | 462,166 | 422,831 | 446,099 | 558,903 | 435,318 | 419,056 |

ABI-367 is finite and non-collapsed, but it is negative evidence for this exact center-detail tail support mechanism. Relative to ABI-350, it loses -0.0101 aggregate filtered Dice, -0.0054 MIT Dice, -0.0248 Google Dice, -0.0348 precision, and -0.1133 connectivity while predicting +39,335 more filtered-positive pixels. It does raise recall by +0.0061, but that recall gain is too small to compensate for the precision, source, and connected-line losses.

Relative to ABI-359, ABI-367 is also weaker on the intended continuity/composite evidence target: aggregate Dice is -0.0058 lower, Google Dice is -0.0154 lower, precision is -0.0154 lower, connectivity is -0.1313 lower, and footprint is +16,067 pixels broader, while recall is essentially tied. Relative to ABI-356, ABI-367 is more compact and precise but gives up the recall signal that ABI-356 was meant to represent and still has weaker connectivity.

The useful narrow signal is that ABI-367 improves over ABI-365's five-frame line-support branch on aggregate filtered Dice (+0.0134), MIT Dice (+0.0197), and recall (+0.0224) while keeping similar precision. However, it does this with much worse connectivity (-0.0527) and a broader footprint (+26,848 pixels), so it does not solve the recent temporal-family failure mode. Against ABI-223, ABI-367 slightly improves aggregate/MIT Dice and recall but loses Google Dice, precision, and a large amount of connectivity.

Raw versus filtered metrics show ordinary Artifact Filter behavior rather than filter-created performance. At the selected checkpoint, raw Dice was 0.438769 versus filtered Dice 0.420955, raw recall was 0.420203 versus filtered recall 0.388373, and raw predicted-positive pixels were 500,537 versus 462,166 filtered. Artifact Filters removed 38,371 predicted-positive pixels and lowered the score.

The retained fixed `first_n` prediction samples have nonzero per-sample Dice values of 0.4053, 0.2222, 0.5652, and 0.4012. They do not indicate all-negative or all-positive qualitative collapse, but they are only the first four validation samples and should not override the aggregate temporal-eligible metrics.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive pixels |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.209840 | 0.203243 | 0.226652 | 0.331850 | 0.153429 | 0.182519 | 252,816 |
| 6 | 0.372336 | 0.359355 | 0.405548 | 0.364389 | 0.380637 | 0.237414 | 571,195 |
| 12 | 0.392463 | 0.375208 | 0.437180 | 0.453606 | 0.345845 | 0.298893 | 416,908 |
| 18 | 0.382023 | 0.366332 | 0.421049 | 0.395402 | 0.369520 | 0.251109 | 511,019 |
| 24 | 0.411130 | 0.387054 | 0.476931 | 0.502490 | 0.347880 | 0.329096 | 378,565 |
| 27 | 0.420955 | 0.404132 | 0.465751 | 0.459504 | 0.388373 | 0.245025 | 462,166 |
| 28 | 0.384510 | 0.360801 | 0.446517 | 0.493096 | 0.315117 | 0.273045 | 349,445 |
| 29 | 0.395213 | 0.372665 | 0.455015 | 0.467819 | 0.342116 | 0.285011 | 399,883 |
| 30 | 0.409562 | 0.386331 | 0.470631 | 0.483762 | 0.355096 | 0.388769 | 401,377 |
| 31 | 0.410487 | 0.389762 | 0.464786 | 0.445338 | 0.380694 | 0.248945 | 467,438 |
| 32 | 0.405108 | 0.380286 | 0.466625 | 0.449848 | 0.368463 | 0.251355 | 447,885 |
| 34 | 0.418394 | 0.399514 | 0.469161 | 0.473377 | 0.374855 | 0.256973 | 433,006 |
| 36 | 0.405443 | 0.385355 | 0.458602 | 0.471907 | 0.355389 | 0.248679 | 411,799 |

The late budget was useful as evidence because the best checkpoint arrived after the exploratory epoch-12 boundary and epochs 24, 27, 30, 31, and 34 remain competitive. The trajectory is nevertheless not the desired convergence pattern. Epoch 24 is compact/high-precision with better Google Dice but low recall. Epoch 27 is the selected aggregate checkpoint but has poor connectivity. Epoch 30 temporarily recovers connectivity to 0.3888, but loses aggregate Dice, MIT Dice, and recall. The final epoch remains finite and reasonably compact, but regresses from the selected checkpoint.

This repeats the recent temporal-line-support pattern: compact precision, recall, and connected-line continuity appear in different epochs rather than combining into a stable selected state.

## Interpretation

Classify ABI-367 as a finite, resource-safe, negative temporal family-development result. The center-frame detail tail is contract-safe and computationally feasible, and it partially recovers ABI-365's MIT/recall weakness. However, it does not improve the strongest direct temporal parent ABI-350, does not preserve ABI-359/223-style connected-line continuity, and does not combine ABI-356-like recall with a compact high-precision footprint.

Do not promote ABI-367. Do not spend another Run on an unchanged late36 continuation, gate-strength tuning, auxiliary-weight shuffle, or minor residual-tail variant of this center-detail tail scaffold. The recent ABI-350/356/359/360/361/365/366/367 sequence now has enough bounded evidence that local temporal line-support/detail-tail variants tend to oscillate among precision, recall, and connectivity instead of producing a stable joint improvement.

A Post-Run Evaluation is not requested in this Autonomy Step. ABI-367 is below the strongest temporal-eligible capped comparators on aggregate/source Dice or connectivity, and capped metrics are sufficient to classify this exact mechanism as non-frontier. If temporal work continues, it should broaden the mechanism rather than locally tune this branch: for example, a genuinely different temporal backbone, a stronger architecture-level evidence-sharpening path tied to ABI-223-style attention, or a single-frame C4/detail recall-support mechanism that explicitly addresses fixed-threshold recall without sacrificing connected-line continuity. Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, and lifecycle changes remain out of scope.

## Decision

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260920_112921_1ee9bd/candidate/PROPOSAL.md`
- `run_20260920_112921_1ee9bd/candidate/README.md`
- `run_20260920_112921_1ee9bd/candidate/manifest.yaml`
- `run_20260920_112921_1ee9bd/candidate/budget_request.yaml`
- `run_20260920_112921_1ee9bd/resolved_manifest.yaml`
- `run_20260920_112921_1ee9bd/execution.json`
- `run_20260920_112921_1ee9bd/run_metadata.json`
- `run_20260920_112921_1ee9bd/outputs/model_summary.json`
- `run_20260920_112921_1ee9bd/outputs/best_metrics.json`
- `run_20260920_112921_1ee9bd/outputs/final_metrics.json`
- `run_20260920_112921_1ee9bd/outputs/metrics.jsonl`
- `run_20260920_112921_1ee9bd/outputs/resource_profile.json`
- `run_20260920_112921_1ee9bd/outputs/validation_postprocessing/index.json`
- `run_20260920_112921_1ee9bd/outputs/prediction_samples/samples.json`
- `run_20260919_013306_9ca44e/outputs/best_metrics.json` and `/history/research-notes/abi350-temporal-attention-predecoder-line-support-late36.md` for ABI-350 comparator context
- `run_20260919_175950_ac7b89/outputs/best_metrics.json` and `/history/research-notes/abi359-temporal-alignment-c4-center-detail-bridge-late36.md` for ABI-359 comparator context
- `run_20260919_095725_843317/outputs/best_metrics.json` and `/history/research-notes/abi356-temporal-attention-multiscale-change-line-fusion-late36.md` for ABI-356 comparator context
- `run_20260920_081530_7577c1/outputs/best_metrics.json` and `/history/research-notes/abi365-temporal-fiveframe-predecoder-line-support-center-detail-late36.md` for ABI-365 comparator context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/reference/EXPERIMENT_INDEX.md` for ABI-223 temporal-attention comparator context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
