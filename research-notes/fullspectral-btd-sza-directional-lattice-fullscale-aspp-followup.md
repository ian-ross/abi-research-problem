# Full-spectral BTD+SZA directional-lattice full-scale skip ASPP follow-up

research-figures: []

## Scope

This note records ABI-191 after Run `run_20260903_075132_5cff8c` completed.

Source Runs:

- ABI-191 signed-detail full-scale skip ASPP with conservative directional-lattice bridge: `run_20260903_075132_5cff8c`
- ABI-181 signed-detail full-scale skip ASPP late36 aggregate reference: `run_20260902_150611_cbbf35`; whole-validation Evaluation `eval_evalreq_abi181_wholeval_failure_buckets_v1`
- ABI-184 Line plus Centerline late36 precision/connectivity reference: `run_20260902_213856_2c04ac`; whole-validation Evaluation `eval_evalreq_abi184_wholeval_failure_buckets_v1`
- ABI-188 detached line-logit fusion exploratory reference: `run_20260903_031950_88e745`
- ABI-189 detached line-logit fusion late36 reference: `run_20260903_041610_f244a9`
- ABI-190 feature-level line calibration negative reference: `run_20260903_064825_5a446f`
- ABI-068 frequency-gated line U-Net focal-Tversky source-balance comparator: `run_20260828_010836_4ccc77`

ABI-191 was an exploratory family-development continuation of the ABI-181 signed-detail full-scale skip ASPP branch. It retained provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD features derived only from approved ABI channels, Solar Geometry Input, signed local/mid-scale detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, line-aware final refinement, BCE-Dice primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.

The intended research change was adding a zero-initialized bounded multi-orientation directional lattice bridge before final line-aware refinement. The bridge was designed to improve connected thin-line support and MIT-source detail without adding Line Target auxiliary conservatism, detached logit boosting, Candidate-owned thresholding, or Candidate-owned postprocessing.

## Contract and resource observation

ABI-191 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary output `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 10,060,450 parameters, below the 25,000,000-parameter smoke ceiling. The Run used the exploratory budget (`budget_class_effective: exploratory`, `effective_max_epochs: 12`) and completed on the A100 at batch size 4 with 3,300.7 seconds total wall time, 1,818.5 seconds training wall time, 1,480.0 seconds validation wall time, 13.51 training samples per second, 16.61 validation samples per second, 10,720,424,960 bytes peak CUDA allocated, and 12,721,324,032 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 12.

## Best-validation comparison

| Run | Candidate | Best epoch | Filtered Dice | Raw Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260903_075132_5cff8c` | ABI-191 directional lattice | 12 | 0.4041 | 0.4180 | 0.3939 | 0.4297 | 0.4036 | 0.4045 | 0.3554 | 0.00363 |
| `run_20260902_150611_cbbf35` | ABI-181 centerline-only late36 | 22 | 0.4104 | 0.4254 | 0.3962 | 0.4486 | 0.4423 | 0.3828 | 0.3639 | 0.00314 |
| `run_20260902_213856_2c04ac` | ABI-184 line+centerline late36 | 23 | 0.4066 | 0.4227 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.00261 |
| `run_20260903_031950_88e745` | ABI-188 line-logit fusion exploratory | 12 | 0.4013 | 0.4160 | 0.3898 | 0.4317 | 0.4250 | 0.3801 | 0.3903 | 0.00324 |
| `run_20260903_041610_f244a9` | ABI-189 line-logit fusion late36 | 22 | 0.4022 | 0.4157 | 0.3917 | 0.4290 | 0.3964 | 0.4083 | 0.2962 | 0.00373 |
| `run_20260903_064825_5a446f` | ABI-190 feature-level line calibration | 11 | 0.3717 | 0.3849 | 0.3712 | 0.3727 | 0.3656 | 0.3779 | 0.1509 | 0.00375 |
| `run_20260828_010836_4ccc77` | ABI-068 frequency-gated line U-Net focal-Tversky | 12 | 0.3964 | 0.4100 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |

ABI-191 is a useful positive-to-mixed capped exploratory result. It ranks third in the current capped `val/filtered_dice` history behind ABI-181 and ABI-184. Relative to ABI-181, ABI-191 is lower on aggregate filtered Dice by 0.0064, raw Dice by 0.0074, MIT filtered Dice by 0.0023, Google filtered Dice by 0.0190, precision by 0.0388, and connectivity by 0.0085. It improves filtered recall by 0.0217, with a larger filtered predicted-positive fraction.

Relative to ABI-184, ABI-191 is lower on aggregate filtered Dice by 0.0025, Google filtered Dice by 0.0259, precision by 0.0815, and connectivity by 0.1080, but improves MIT filtered Dice by 0.0060 and recall by 0.0546. This is the first recent signed-detail continuation to come close to ABI-184 aggregate Dice without direct Line Target auxiliary supervision, though it does not preserve ABI-184's clean connectivity/precision operating point.

Relative to ABI-188 and ABI-189, ABI-191 improves aggregate filtered Dice and MIT filtered Dice while avoiding ABI-190's collapse in connectivity. It does not exceed ABI-188 connectivity, and it trails ABI-188 slightly on Google Dice and precision. Against ABI-068, ABI-191 improves aggregate filtered Dice, MIT and Google filtered Dice, precision, and recall, but remains below ABI-068 on connectivity by 0.0346. These comparisons remain capped representative evidence, not full-data promotion evidence.

## Exploratory trajectory

ABI-191 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was:

`0.2027, 0.2710, 0.3062, 0.3161, 0.3374, 0.3644, 0.3082, 0.3676, 0.3779, 0.3477, 0.3567, 0.4041`.

The selected checkpoint was the final exploratory epoch. The final jump from epoch 11 to epoch 12 combined higher filtered Dice, balanced precision/recall, and recovered connectivity: epoch 12 reached filtered Dice 0.4041, precision 0.4036, recall 0.4045, connectivity 0.3554, and filtered predicted-positive fraction 0.00363. This is a late-improving, non-collapsed trajectory rather than a clear plateau.

At epoch 12, raw Dice was 0.4180 versus filtered Dice 0.4041, raw recall 0.4324 versus filtered recall 0.4045, and raw predicted-positive fraction 0.00391 versus filtered predicted-positive fraction 0.00363. Source-stratified filtered Dice was 0.3939 for MIT and 0.4297 for Google. MIT had filtered precision 0.4099, recall 0.3791, connectivity 0.3426, and predicted-positive fraction 0.00502. Google had filtered precision 0.3895, recall 0.4790, connectivity 0.3682, and predicted-positive fraction 0.00225. Raw-to-filtered differences are modest enough that this does not indicate primary Artifact Filter dependence.

The fixed first-four retained prediction samples include one empty/negative perfect case and three near-zero per-sample Dice cases under the Harness `first_n` retention policy. They are traceability samples and should not be treated as representative qualitative evidence for the validation distribution.

## Interpretation

Classify ABI-191 as a completed, finite, non-collapsed, scientifically useful positive-to-mixed capped exploratory continuation. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The directional-lattice bridge partially supports the hypothesis. It did not produce ABI-184-level line connectivity or precision, and it did not displace ABI-181 on the v0 primary capped metric. However, it did recover ABI-181-like recall while staying within about 0.01 aggregate filtered Dice of ABI-181, improved MIT filtered Dice relative to ABI-184/188/189, and achieved the current third-best capped filtered Dice with the best checkpoint at epoch 12. The result suggests the zero-initialized directional feature-propagation mechanism is a better continuation path than ABI-190-style local line-feature calibration and less damaging than detached logit fusion, but still has an unresolved connectivity/precision tradeoff.

Because the best checkpoint is at the exploratory ceiling and the trajectory is noisy but improving late, ABI-191 is eligible for a controlled `late_improving` continuation under the now-addressed extended-budget policy. The resource profile is close to the exploratory timeout but consistent with a 36-epoch budget class if the Harness grants the longer wall-clock ceiling; Candidate code must not implement any budget workaround.

## Decision

Do not promote ABI-191 and do not reinterpret this capped representative result as full-data evidence. Retain ABI-181 as the current whole-validation-tested aggregate filtered-Dice reference and ABI-184 as the whole-validation-tested precision/connectivity reference. Treat ABI-191 as the best current Centerline-only architecture continuation after ABI-181 and as a plausible late-budget follow-up target.

Do not request whole-validation diagnostics for ABI-191 yet; capped evidence is promising but not clearly stronger than ABI-181 or ABI-184. A reasonable next in-contract hypothesis is a late36 close-continuation of ABI-191 that changes only the Harness budget request, with parent Run `run_20260903_075132_5cff8c`, to test whether the epoch-12 directional-lattice jump stabilizes into ABI-181-level aggregate overlap with better MIT/source balance. If the longer budget is denied, the exploratory result remains valid. If a late36 ABI-191 continuation loses connectivity or plateaus below ABI-181/184, stop this directional-lattice branch and broaden to a different high-resolution line-aware architecture or trusted data/loss/auxiliary policy probe. No new Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260903_075132_5cff8c/outputs/best_metrics.json`
- `run_20260903_075132_5cff8c/outputs/final_metrics.json`
- `run_20260903_075132_5cff8c/outputs/metrics.jsonl`
- `run_20260903_075132_5cff8c/outputs/resource_profile.json`
- `run_20260903_075132_5cff8c/outputs/model_summary.json`
- `run_20260903_075132_5cff8c/outputs/prediction_samples/samples.json`
- `run_20260903_075132_5cff8c/outputs/validation_postprocessing/index.json`
- `run_20260903_075132_5cff8c/resolved_manifest.yaml`
- `run_20260903_075132_5cff8c/candidate/PROPOSAL.md`
- `run_20260902_150611_cbbf35/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260903_031950_88e745/outputs/best_metrics.json`
- `run_20260903_041610_f244a9/outputs/best_metrics.json`
- `run_20260903_064825_5a446f/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
