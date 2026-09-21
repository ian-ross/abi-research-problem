# ABI-355 temporal-attention multi-scale change-line fusion

research-figures: []

## Scope

This note records ABI-355, Candidate `abi355_temporal_attention_multiscale_change_line_fusion_unet_bce_dice_line_centerline_aux_v1`, and Run `run_20260919_090506_bad1ff`.

ABI-355 was an exploratory family-development continuation in the temporal-attention branch. It kept provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, trusted source-balanced sampling, trusted random mirroring, BCE-Dice loss, Line and Centerline auxiliary targets, AdamW with constant LR, and batch size 2. The mechanism change was to inject temporal-change and center-frame detail evidence during multi-scale decoder skip fusion rather than at the temporal stem, encoder entry, or final decoder output.

This is capped temporal-eligible exploratory evidence only. It is not whole Working Validation Split promotion evidence.

## Execution result

ABI-355 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: exploratory, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,615,732, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 4,915,849,728 / 5,435,817,984 bytes.
- Training wall time: 1,577.0 s; validation wall time: 1,067.1 s; total Run wall time: 2,646.1 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 11.

## Best-validation metrics

| Metric | ABI-355 multi-scale change-line fusion | ABI-350 line-support late36 | ABI-351 post-decoder continuity bridge | ABI-349 exploratory parent | ABI-324 balanced five-frame C4 | ABI-223 temporal attention | ABI-348 compact five-frame C4 | ABI-354 encoder-entry change bridge |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 11 | 33 | 11 | 12 | 27 | 36 | 36 | 11 |
| Filtered Dice | 0.393153 | 0.431103 | 0.389837 | 0.389171 | 0.429430 | 0.419776 | 0.427829 | 0.379645 |
| MIT filtered Dice | 0.375355 | 0.409536 | 0.370966 | 0.369849 | 0.408188 | 0.398498 | 0.410244 | 0.361755 |
| Google filtered Dice | 0.438306 | 0.490518 | 0.437075 | 0.440561 | 0.487231 | 0.476764 | 0.478363 | 0.424959 |
| Filtered precision | 0.426347 | 0.494306 | 0.417607 | 0.478850 | 0.470412 | 0.483764 | 0.477546 | 0.450025 |
| Filtered recall | 0.364754 | 0.382230 | 0.365530 | 0.327784 | 0.395017 | 0.370738 | 0.387488 | 0.328301 |
| Filtered connectivity | 0.312086 | 0.358283 | 0.271278 | 0.337620 | 0.397925 | 0.412427 | 0.300904 | 0.227228 |
| Filtered predicted-positive pixels | 467,816 | 422,831 | 478,622 | 374,305 | 459,172 | 419,056 | 443,691 | 398,909 |

ABI-355 is a modest but real improvement over the recent exploratory temporal-attention placement tests. Relative to ABI-354, it gains +0.0135 filtered Dice, +0.0136 MIT Dice, +0.0133 Google Dice, +0.0365 recall, and +0.0849 connectivity, at the cost of lower precision and a larger filtered-positive footprint. Relative to ABI-351, it gains small aggregate/source Dice, precision, and connectivity while keeping a similar recall level and a slightly smaller footprint. Relative to ABI-349, it raises aggregate Dice, MIT Dice, and recall, but loses Google Dice, precision, and connectivity and predicts many more positives.

ABI-355 remains well below the stronger late-budget temporal and C4 comparators. ABI-350, ABI-324, ABI-223, and ABI-348 all have higher aggregate/source Dice bands or stronger recall/connectivity balance. The multi-scale fusion placement is therefore useful family-development evidence, not a promotion candidate.

At the selected checkpoint, raw Dice was 0.409651 versus filtered Dice 0.393153; raw recall was 0.393909 versus filtered recall 0.364754; raw predicted-positive pixels were 504,786 versus 467,816 filtered. Artifact Filters removed 36,970 predicted-positive pixels and lowered the primary score, so the Result is not being created by postprocessing.

The retained fixed first-four validation samples had sample Dice values 0.2608, 0.6526, 0.5272, and 0.3112. These are traceability artifacts only and do not override aggregate validation metrics.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.232087 | 0.234566 | 0.226776 | 0.233967 | 0.230238 | 0.153803 | 0.005087 |
| 2 | 0.239544 | 0.236077 | 0.247949 | 0.356886 | 0.180272 | 0.195672 | 0.002611 |
| 3 | 0.310049 | 0.293159 | 0.349747 | 0.372574 | 0.265493 | 0.247078 | 0.003684 |
| 4 | 0.320631 | 0.297906 | 0.379476 | 0.464321 | 0.244857 | 0.352853 | 0.002726 |
| 5 | 0.338210 | 0.324764 | 0.369966 | 0.360341 | 0.318640 | 0.214699 | 0.004571 |
| 6 | 0.361562 | 0.352760 | 0.382931 | 0.394990 | 0.333350 | 0.215014 | 0.004363 |
| 7 | 0.312735 | 0.290177 | 0.372065 | 0.528390 | 0.222091 | 0.330368 | 0.002173 |
| 8 | 0.388312 | 0.377100 | 0.416614 | 0.416520 | 0.363683 | 0.239499 | 0.004514 |
| 9 | 0.381485 | 0.376552 | 0.393285 | 0.360535 | 0.405020 | 0.258755 | 0.005807 |
| 10 | 0.390058 | 0.376154 | 0.423963 | 0.419908 | 0.364171 | 0.267945 | 0.004483 |
| 11 | 0.393153 | 0.375355 | 0.438306 | 0.426347 | 0.364754 | 0.312086 | 0.004423 |
| 12 | 0.359450 | 0.335208 | 0.420613 | 0.471986 | 0.290246 | 0.335234 | 0.003179 |

The trajectory is finite, source-informative, and non-collapsed. The branch improves sharply by epoch 8, then oscillates between recall-heavy and precision-heavy states. The best checkpoint at epoch 11 has the strongest aggregate Dice and a better connectivity/recall compromise than ABI-351/354, but epoch 12 regresses substantially in aggregate Dice and recall. This is late and ambiguous rather than cleanly converged.

The main scientific signal is placement-specific: injecting change/detail evidence in decoder skip fusion is healthier than ABI-354's encoder-entry bridge and ABI-351's final continuity bridge, but it still does not achieve ABI-350's late-budget compact precision/recall state or ABI-223's stronger temporal connectivity.

## Interpretation

Classify ABI-355 as positive-but-limited exploratory evidence for multi-scale temporal change-line fusion.

No repair Candidate is needed because the run is technically healthy. A temporal-eligible failure-bucket evaluation is not warranted now: ABI-355 does not reach the temporal comparator band, and its capped metrics already answer the immediate placement question. It is also not a promotion candidate and should not be compared as whole-validation evidence.

A single late-improving continuation is scientifically defensible but not mandatory. The case for late36 is that ABI-355 improves over ABI-349/351/354 exploratory variants, is source-balanced and non-collapsed, and selects best near the epoch ceiling with unresolved oscillation. The case against late36 is that epoch 12 regresses and the score remains far below ABI-350/324/223/348. If continued, the late36 question should be narrow: whether the epoch-8-to-11 state stabilizes into a compact high-recall/connected-line solution, not whether this branch is already frontier evidence.

ABI-355 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-355 and do not request a Post-Run Evaluation from this exploratory run. Mark the exact multi-scale fusion placement as the best of the recent ABI-349/351/354 exploratory placement tests, but still below established temporal and C4 comparators.

A next Autonomy Step may either submit one late36 close-continuation of ABI-355, with `run_20260919_090506_bad1ff` as the budget-request parent, or broaden away from simple temporal-attention placement changes toward a mechanism-changing temporal alignment/change module. Do not spend Runs on another exploratory-only gate-strength or placement shuffle around the same ABI-350 scaffold.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260919_090506_bad1ff/candidate/PROPOSAL.md`
- `run_20260919_090506_bad1ff/candidate/README.md`
- `run_20260919_090506_bad1ff/candidate/manifest.yaml`
- `run_20260919_090506_bad1ff/resolved_manifest.yaml`
- `run_20260919_090506_bad1ff/execution.json`
- `run_20260919_090506_bad1ff/run_metadata.json`
- `run_20260919_090506_bad1ff/outputs/model_summary.json`
- `run_20260919_090506_bad1ff/outputs/best_metrics.json`
- `run_20260919_090506_bad1ff/outputs/final_metrics.json`
- `run_20260919_090506_bad1ff/outputs/metrics.jsonl`
- `run_20260919_090506_bad1ff/outputs/resource_profile.json`
- `run_20260919_090506_bad1ff/outputs/validation_postprocessing/index.json`
- `run_20260919_090506_bad1ff/outputs/prediction_samples/samples.json`
- `run_20260919_013306_9ca44e/outputs/best_metrics.json` and `/history/research-notes/abi350-temporal-attention-predecoder-line-support-late36.md`
- `run_20260919_034932_017f6a/outputs/best_metrics.json` and `/history/research-notes/abi351-temporal-attention-predecoder-continuity-bridge.md`
- `run_20260919_004607_f785f8/outputs/best_metrics.json` and `/history/research-notes/abi349-temporal-attention-predecoder-line-support-unet.md`
- `run_20260916_184108_954ec7/outputs/best_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json`
- `run_20260918_215534_a35ab9/outputs/best_metrics.json` and `/history/research-notes/abi348-temporal-fiveframe-dual-state-connectivity-blend-late36.md`
- `run_20260919_080945_2ab8be/outputs/best_metrics.json` and `/history/research-notes/abi354-temporal-attention-encoder-change-line-agreement.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
