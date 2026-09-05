# Full-spectral BTD+SZA signed-detail full-scale skip ASPP line-aux focal-Tversky follow-up

research-figures: []

## Scope

This note records ABI-187 after Run `run_20260903_022247_88e0dc` completed.

Source Runs:

- ABI-187 signed-detail full-scale skip ASPP with trusted focal-Tversky primary loss and Line plus Centerline auxiliary supervision: `run_20260903_022247_88e0dc`
- ABI-184 late36 Line plus Centerline auxiliary BCE-Dice precision/connectivity reference: `run_20260902_213856_2c04ac`; whole-validation Evaluation `eval_evalreq_abi184_wholeval_failure_buckets_v1`
- ABI-183 exploratory Line plus Centerline auxiliary BCE-Dice parent: `run_20260902_204128_bba815`
- ABI-181 signed-detail full-scale skip ASPP late36 aggregate reference: `run_20260902_150611_cbbf35`; whole-validation Evaluation `eval_evalreq_abi181_wholeval_failure_buckets_v1`
- ABI-172 centerline-only focal-Tversky negative reference: `run_20260901_225502_53acd2`
- ABI-068 frequency-gated line U-Net focal-Tversky source-balance comparator: `run_20260828_010836_4ccc77`

ABI-187 was a controlled family-development continuation of the ABI-183/184 signed-detail full-scale skip ASPP branch. It retained provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD features derived only from approved ABI channels, Solar Geometry Input, signed local/mid-scale detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, line-aware final refinement, provider-derived Line Target auxiliary supervision at weight 0.01, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The intended research change from ABI-183/184 was selecting the trusted `focal_tversky` primary loss instead of `bce_dice`.

## Contract and resource observation

ABI-187 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary outputs `line_logits` and `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 9,838,851 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,906.8 seconds total wall time, 1,523.8 seconds training wall time, 1,380.9 seconds validation wall time, 16.13 training samples per second, 17.80 validation samples per second, 9,041,055,744 bytes peak CUDA allocated, and 10,508,828,672 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 12, the final exploratory epoch.

## Best-validation comparison

| Run | Candidate | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260903_022247_88e0dc` | ABI-187 focal-Tversky line+centerline | 12 | 0.3897 | 0.3830 | 0.4068 | 0.3785 | 0.4017 | 0.2197 | 0.00385 |
| `run_20260902_213856_2c04ac` | ABI-184 line+centerline late36 | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.00261 |
| `run_20260902_204128_bba815` | ABI-183 line+centerline exploratory parent | 12 | 0.3966 | 0.3805 | 0.4389 | 0.4468 | 0.3565 | 0.4546 | 0.00289 |
| `run_20260902_150611_cbbf35` | ABI-181 centerline-only late36 | 22 | 0.4104 | 0.3962 | 0.4486 | 0.4423 | 0.3828 | 0.3639 | 0.00314 |
| `run_20260901_225502_53acd2` | ABI-172 centerline-only focal-Tversky | 10 | 0.3578 | 0.3552 | 0.3631 | 0.3185 | 0.4081 | 0.2312 | 0.00464 |
| `run_20260828_010836_4ccc77` | ABI-068 frequency-gated line U-Net focal-Tversky | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |

ABI-187 partially achieved the intended recall-softening effect but failed the precision/connectivity constraint. Relative to ABI-184, filtered recall improved from 0.3500 to 0.4017 and MIT filtered recall improved from 0.3245 to 0.3790, but aggregate filtered Dice fell by 0.0168, Google filtered Dice fell by 0.0487, precision fell by 0.1065, connectivity fell by 0.2437, and filtered predicted-positive fraction expanded from 0.00261 to 0.00385. Relative to ABI-183, ABI-187 has slightly higher MIT filtered Dice and higher recall, but lower aggregate Dice, much lower Google Dice, lower precision, and much lower connectivity.

ABI-187 is better than the ABI-172 centerline-only focal-Tversky negative reference on aggregate/source Dice and precision, so Line plus Centerline supervision did constrain the worst focal-Tversky clutter mode. However, ABI-187 remains weaker than ABI-068 on aggregate/MIT/Google filtered Dice, precision, connectivity, and positive-area discipline, despite modestly higher recall. Against ABI-181, ABI-187 has slightly higher recall but loses aggregate/source Dice, precision, connectivity, and positive-area discipline. These comparisons remain capped representative evidence, not full-data promotion evidence.

## Exploratory trajectory

ABI-187 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was:

`0.1756, 0.2146, 0.2596, 0.3163, 0.3519, 0.3336, 0.3503, 0.3530, 0.3749, 0.3572, 0.2944, 0.3897`.

The final epoch was the selected checkpoint. At epoch 12, raw Dice was 0.4033, filtered Dice was 0.3897, filtered precision was 0.3785, filtered recall was 0.4017, filtered connectivity was 0.2197, and filtered predicted-positive fraction was 0.00385. Source-stratified filtered Dice was 0.3830 for MIT and 0.4068 for Google. MIT had filtered precision 0.3870, recall 0.3790, connectivity 0.2492, and predicted-positive fraction 0.00529; Google had filtered precision 0.3597, recall 0.4681, connectivity 0.1901, and predicted-positive fraction 0.00240.

Raw-to-filtered differences were modest: raw Dice 0.4033 versus filtered Dice 0.3897, raw recall 0.4306 versus filtered recall 0.4017, and raw predicted-positive fraction 0.00411 versus filtered predicted-positive fraction 0.00385. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples are traceability samples under the `first_n` retention policy and should not be treated as representative qualitative evidence for the validation distribution.

The epoch-12 best checkpoint is late-improving/ambiguous in a generic sense, but the branch-specific evidence does not justify an immediate late36 continuation. The final jump recovered the Run from an epoch-11 dip, yet the selected checkpoint still sits below ABI-183/184 on aggregate Dice and far below them on the line-connectivity property this branch was meant to retain.

## Interpretation

Classify ABI-187 as a completed, finite, non-collapsed, scientifically mixed-to-negative capped exploratory continuation. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The controlled focal-Tversky loss switch shows that explicit Line plus Centerline supervision can prevent the severe ABI-172-style low-precision expansion, but it does not preserve the ABI-183/184 connected-line operating point. The main failure is not fixed-threshold recall: recall improved versus ABI-184/183 and is competitive with ABI-068. The failure is that the recall gain came with too much loss of precision, Google overlap, and especially connectivity. That tradeoff is not useful for the signed-detail full-scale skip ASPP lineage because ABI-181 and ABI-184 already bracket stronger aggregate-overlap and precision/connectivity references.

## Decision

Do not promote ABI-187 and do not reinterpret this capped representative result as full-data evidence. Retain ABI-181 as the whole-validation-tested aggregate filtered-Dice reference. Retain ABI-184 as the whole-validation-tested precision/connectivity and negative-patch-discipline reference in the signed-detail full-scale skip ASPP family.

Do not repeat ABI-187 unchanged at the exploratory budget and do not request an immediate late36 continuation of this exact focal-Tversky Line plus Centerline branch. Do not make ABI-187 the next whole-validation Evaluation Request, because the capped result already loses the core connectivity property and is not competitive with ABI-181/184 on primary/source Dice. A reasonable next in-contract direction is to move away from primary-loss-only recall expansion and test a calibration or architecture mechanism that preserves ABI-184-like connected line evidence while softening only the mask-logit operating point, or to broaden to a different high-resolution line-aware family/data-policy probe. No new Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260903_022247_88e0dc/outputs/best_metrics.json`
- `run_20260903_022247_88e0dc/outputs/final_metrics.json`
- `run_20260903_022247_88e0dc/outputs/metrics.jsonl`
- `run_20260903_022247_88e0dc/outputs/resource_profile.json`
- `run_20260903_022247_88e0dc/outputs/model_summary.json`
- `run_20260903_022247_88e0dc/outputs/prediction_samples/samples.json`
- `run_20260903_022247_88e0dc/outputs/validation_postprocessing/index.json`
- `run_20260903_022247_88e0dc/resolved_manifest.yaml`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_204128_bba815/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_225502_53acd2/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
