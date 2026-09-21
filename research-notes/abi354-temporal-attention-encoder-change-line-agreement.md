# ABI-354 temporal-attention encoder change-line agreement

research-figures: []

## Scope

This note records ABI-354, Candidate `abi354_temporal_attention_encoder_change_line_agreement_unet_bce_dice_line_centerline_aux_v1`, and Run `run_20260919_080945_2ab8be`.

ABI-354 was an exploratory, mechanism-changing follow-up to ABI-350/351 in the temporal-attention family. It kept ABI-350's provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, BCE-Dice loss, Line and Centerline auxiliary targets, AdamW with constant LR, and batch size 2. The architectural change was an encoder-entry temporal change/detail line-agreement bridge, inserted after the temporal stem and before encoder skip features are formed.

This is capped temporal-eligible exploratory evidence only. It is not whole Working Validation Split promotion evidence.

## Execution result

ABI-354 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: exploratory, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,226,812, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 5,634,415,616 / 6,174,015,488 bytes.
- Training wall time: 1,651.2 s; validation wall time: 1,143.6 s; total Run wall time: 2,796.8 s, within the 3,600 s exploratory timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 11.

## Best-validation metrics

| Metric | ABI-354 encoder-entry change-line agreement | ABI-350 line-support late36 | ABI-351 post-decoder continuity bridge | ABI-349 exploratory parent | ABI-324 balanced five-frame C4 | ABI-223 temporal attention | ABI-348 compact five-frame C4 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 11 | 33 | 11 | 12 | 27 | 36 | 36 |
| Filtered Dice | 0.379645 | 0.431103 | 0.389837 | 0.389171 | 0.429430 | 0.419776 | 0.427829 |
| MIT filtered Dice | 0.361755 | 0.409536 | 0.370966 | 0.369849 | 0.408188 | 0.398498 | 0.410244 |
| Google filtered Dice | 0.424959 | 0.490518 | 0.437075 | 0.440561 | 0.487231 | 0.476764 | 0.478363 |
| Filtered precision | 0.450025 | 0.494306 | 0.417607 | 0.478850 | 0.470412 | 0.483764 | 0.477546 |
| Filtered recall | 0.328301 | 0.382230 | 0.365530 | 0.327784 | 0.395017 | 0.370738 | 0.387488 |
| Filtered connectivity | 0.227228 | 0.358283 | 0.271278 | 0.337620 | 0.397925 | 0.412427 | 0.300904 |
| Filtered predicted-positive pixels | 398,909 | 422,831 | 478,622 | 374,305 | 459,172 | 419,056 | 443,691 |

ABI-354 does not improve the intended temporal-attention line-support branch. Relative to ABI-350, it loses -0.0515 filtered Dice, -0.0478 MIT Dice, -0.0656 Google Dice, -0.0443 precision, -0.0539 recall, and -0.1311 connectivity. The smaller footprint does not indicate useful compactness because the lost recall and connected-line evidence are too large.

Relative to ABI-351, ABI-354 is more compact and more precise, but it loses aggregate Dice, both source Dice scores, recall, and connectivity. Relative to ABI-349, ABI-354 is almost tied on recall but lower on aggregate/source Dice and much lower on connectivity while predicting more filtered-positive pixels. The early bridge therefore does not recover the compact connected state that ABI-350 found under late training, and it also does not improve the exploratory parent.

At the selected checkpoint, raw Dice was 0.397403 versus filtered Dice 0.379645; raw recall was 0.354786 versus filtered recall 0.328301; raw predicted-positive pixels were 429,532 versus 398,909 filtered. Artifact Filters removed 30,623 predicted-positive pixels and lowered the score; they did not create the Result.

The retained fixed first-four validation samples had sample Dice values 0.3907, 0.1633, 0.4041, and 0.3069. These are only traceability artifacts and do not override aggregate validation metrics.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Precision | Recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.218299 | 0.217356 | 0.220246 | 0.220677 | 0.215972 | 0.136671 | 0.005059 |
| 2 | 0.263151 | 0.251565 | 0.289698 | 0.328962 | 0.219282 | 0.207250 | 0.003446 |
| 3 | 0.294054 | 0.271050 | 0.354661 | 0.507451 | 0.207004 | 0.395775 | 0.002109 |
| 4 | 0.264487 | 0.245514 | 0.309084 | 0.369282 | 0.206021 | 0.150467 | 0.002884 |
| 5 | 0.344021 | 0.328548 | 0.380808 | 0.386979 | 0.309648 | 0.179235 | 0.004137 |
| 6 | 0.358225 | 0.341527 | 0.399927 | 0.439867 | 0.302146 | 0.260233 | 0.003551 |
| 7 | 0.300833 | 0.278363 | 0.360573 | 0.570503 | 0.204275 | 0.361610 | 0.001851 |
| 8 | 0.364302 | 0.357867 | 0.379202 | 0.347429 | 0.382898 | 0.166109 | 0.005697 |
| 9 | 0.363461 | 0.358251 | 0.375214 | 0.322653 | 0.416086 | 0.197252 | 0.006667 |
| 10 | 0.373099 | 0.353462 | 0.422147 | 0.470600 | 0.309066 | 0.254210 | 0.003395 |
| 11 | 0.379645 | 0.361755 | 0.424959 | 0.450025 | 0.328301 | 0.227228 | 0.003771 |
| 12 | 0.372604 | 0.353244 | 0.420029 | 0.416360 | 0.337171 | 0.209914 | 0.004186 |

The trajectory is finite and non-collapsed, but it is not a convincing late-improving candidate. The selected epoch is near the end, yet the peak remains below ABI-349/351 and far below ABI-350/324/223/348. The transient high-connectivity states at epochs 3 and 7 are coupled to very low recall and low aggregate Dice, while the higher-recall states at epochs 8-9 have poor precision and weak connectivity. This repeats the temporal-family instability problem rather than solving it.

## Interpretation

Classify ABI-354 as negative exploratory evidence for this exact encoder-entry change-line agreement bridge.

The run is technically healthy, so no repair Candidate is needed. Scientifically, the early bridge does not satisfy its success criteria: it does not raise MIT positive-tail evidence, does not improve connected-line continuity, does not stay near the ABI-350/324 temporal comparator band, and does not avoid the precision/recall/connectivity decoupling seen in ABI-351. The mechanism appears to perturb the temporal stem before useful skip features form rather than providing stable center-frame line evidence to the encoder-decoder.

A temporal-eligible failure-bucket evaluation is not warranted for ABI-354 because the capped aggregate and source metrics are already below ABI-349/351 and well below the temporal comparators; the question can be answered without another primary handoff. A late36 continuation is also not justified: the best checkpoint is late but weak, and the final epoch regresses rather than showing an unresolved upward trend.

ABI-354 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-354, do not request a Post-Run Evaluation, and do not submit a late36 continuation of this encoder-entry change-line agreement variant. Stop this exact early-bridge mechanism.

Future work should be mechanism-changing rather than another simple placement/gate variant of ABI-350. Defensible directions include a temporal alignment/change module inside multi-scale fusion, a center-frame detail path supervised before skip fusion without perturbing the temporal stem, or a broader architecture family with explicit line-continuity decoding and source-balanced recall support.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260919_080945_2ab8be/candidate/PROPOSAL.md`
- `run_20260919_080945_2ab8be/candidate/README.md`
- `run_20260919_080945_2ab8be/candidate/manifest.yaml`
- `run_20260919_080945_2ab8be/resolved_manifest.yaml`
- `run_20260919_080945_2ab8be/execution.json`
- `run_20260919_080945_2ab8be/run_metadata.json`
- `run_20260919_080945_2ab8be/outputs/model_summary.json`
- `run_20260919_080945_2ab8be/outputs/best_metrics.json`
- `run_20260919_080945_2ab8be/outputs/final_metrics.json`
- `run_20260919_080945_2ab8be/outputs/metrics.jsonl`
- `run_20260919_080945_2ab8be/outputs/resource_profile.json`
- `run_20260919_080945_2ab8be/outputs/validation_postprocessing/index.json`
- `run_20260919_080945_2ab8be/outputs/prediction_samples/samples.json`
- `run_20260919_013306_9ca44e/outputs/best_metrics.json` and `/history/research-notes/abi350-temporal-attention-predecoder-line-support-late36.md`
- `run_20260919_034932_017f6a/outputs/best_metrics.json` and `/history/research-notes/abi351-temporal-attention-predecoder-continuity-bridge.md`
- `run_20260919_004607_f785f8/outputs/best_metrics.json` and `/history/research-notes/abi349-temporal-attention-predecoder-line-support-unet.md`
- `run_20260916_184108_954ec7/outputs/best_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json`
- `run_20260918_215534_a35ab9/outputs/best_metrics.json`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
