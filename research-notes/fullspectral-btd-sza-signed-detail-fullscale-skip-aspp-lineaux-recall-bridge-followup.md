# Full-spectral BTD+SZA signed-detail full-scale skip ASPP line-aux recall-bridge follow-up

research-figures: []

## Scope

This note records ABI-185 after Run `run_20260903_002344_daa8ef` completed.

Source Runs:

- ABI-185 signed-detail full-scale skip ASPP with Line plus Centerline auxiliary supervision and a shared feature-level recall bridge: `run_20260903_002344_daa8ef`
- ABI-184 late36 Line plus Centerline auxiliary precision/connectivity reference: `run_20260902_213856_2c04ac`; whole-validation Evaluation `eval_evalreq_abi184_wholeval_failure_buckets_v1`
- ABI-183 exploratory Line plus Centerline auxiliary parent: `run_20260902_204128_bba815`
- ABI-181 signed-detail full-scale skip ASPP late36 aggregate reference: `run_20260902_150611_cbbf35`; whole-validation Evaluation `eval_evalreq_abi181_wholeval_failure_buckets_v1`
- ABI-182 signed-detail line-consensus late36 comparator: `run_20260902_175152_51d2d9`
- ABI-173 signed-detail full-scale skip ASPP 12-epoch parent: `run_20260901_234732_bd5917`; whole-validation Evaluation `eval_evalreq_abi173_wholeval_failure_buckets_v1`
- ABI-154 full-scale skip ASPP/detail decoder precision-connectivity reference: `run_20260901_071026_32d3ec`
- ABI-068 frequency-gated line U-Net focal-Tversky source-balance comparator: `run_20260828_010836_4ccc77`

ABI-185 was a close family-development continuation prompted by ABI-184's whole-validation diagnostic. It retained provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD features derived only from approved ABI channels, Solar Geometry Input, signed local/mid-scale detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, line-aware final refinement, BCE-Dice primary loss, provider-derived Line Target auxiliary supervision at weight 0.01, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The intended research change from ABI-184 was adding a bounded `LineSupportedRecallBridge` shared by the mask, line, and centerline heads before logits, without Candidate-owned thresholding or postprocessing.

## Contract and resource observation

ABI-185 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary outputs `line_logits` and `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 9,982,092 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 3,153.4 seconds total wall time, 1,734.3 seconds training wall time, 1,417.0 seconds validation wall time, 14.17 training samples per second, 17.34 validation samples per second, 10,510,822,400 bytes peak CUDA allocated, and 12,320,768,000 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 12, the final exploratory epoch.

## Best-validation comparison

| Run | Candidate | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260903_002344_daa8ef` | ABI-185 recall bridge | 12 | 0.3927 | 0.3810 | 0.4228 | 0.4511 | 0.3477 | 0.3433 | 0.00279 |
| `run_20260902_213856_2c04ac` | ABI-184 line+centerline late36 | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.00261 |
| `run_20260902_204128_bba815` | ABI-183 line+centerline exploratory parent | 12 | 0.3966 | 0.3805 | 0.4389 | 0.4468 | 0.3565 | 0.4546 | 0.00289 |
| `run_20260902_150611_cbbf35` | ABI-181 centerline-only late36 | 22 | 0.4104 | 0.3962 | 0.4486 | 0.4423 | 0.3828 | 0.3639 | 0.00314 |
| `run_20260902_175152_51d2d9` | ABI-182 line-consensus late36 | 32 | 0.4035 | 0.3898 | 0.4362 | 0.4010 | 0.4061 | 0.3365 | 0.00367 |
| `run_20260901_234732_bd5917` | ABI-173 signed-detail full-scale skip ASPP | 12 | 0.3962 | 0.3838 | 0.4269 | 0.4238 | 0.3720 | 0.3203 | 0.00318 |
| `run_20260901_071026_32d3ec` | ABI-154 full-scale skip ASPP/detail decoder | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260828_010836_4ccc77` | ABI-068 frequency-gated line U-Net focal-Tversky | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |

ABI-185 did not accomplish the intended recall-bridge effect. Relative to ABI-184, it reduced aggregate filtered Dice by 0.0139, MIT filtered Dice by 0.0070, Google filtered Dice by 0.0327, precision by 0.0339, recall by 0.0023, and connectivity by 0.1200. The only improvement over ABI-184 was a slightly larger filtered predicted-positive fraction, which is not useful because it did not translate into recall or source-overlap gains.

Relative to ABI-183, ABI-185 is also not a clear improvement: it raises MIT filtered Dice by only 0.0004 and precision by 0.0042, while lowering aggregate filtered Dice by 0.0039, Google filtered Dice by 0.0161, recall by 0.0089, and connectivity by 0.1112. Relative to ABI-181, ABI-185 has much lower aggregate/MIT/Google filtered Dice and recall; its precision is only modestly higher while its connectivity is lower. Relative to ABI-154, ABI-185 trades a little recall for materially worse precision/connectivity, so it does not replace ABI-154 as a precision/connectivity reference. These comparisons remain capped representative evidence, not full-data promotion evidence.

## Exploratory trajectory

ABI-185 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was:

`0.1876, 0.3005, 0.2464, 0.3227, 0.3271, 0.3382, 0.3206, 0.3564, 0.3601, 0.3555, 0.3594, 0.3927`.

The final epoch was the selected checkpoint, with a late jump from 0.3594 at epoch 11 to 0.3927 at epoch 12. At the selected checkpoint, raw Dice was 0.4080, filtered Dice was 0.3927, filtered precision was 0.4511, filtered recall was 0.3477, filtered connectivity was 0.3433, and filtered predicted-positive fraction was 0.00279. Source-stratified filtered Dice was 0.3810 for MIT and 0.4228 for Google. MIT had filtered precision 0.4586, recall 0.3258, connectivity 0.3613, and predicted-positive fraction 0.00384; Google had filtered precision 0.4346, recall 0.4116, connectivity 0.3254, and predicted-positive fraction 0.00175.

Raw-to-filtered differences were modest: raw Dice 0.4080 versus filtered Dice 0.3927, raw recall 0.3716 versus filtered recall 0.3477, and raw predicted-positive fraction 0.00298 versus filtered predicted-positive fraction 0.00279. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples include three empty/negative perfect cases and one near-zero per-sample Dice case under the `first_n` retention policy; they are traceability samples and should not be treated as representative qualitative evidence for the validation distribution.

## Interpretation

Classify ABI-185 as a completed, finite, non-collapsed but scientifically negative capped exploratory continuation. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The shared recall-bridge hypothesis is not supported at the 12-epoch budget. The bridge did not recover ABI-184's fixed-threshold recall weakness and it substantially damaged the main feature that made ABI-184 valuable: line connectivity. The result suggests that adding a shared pre-logit residual bridge can disturb the line-supervised representation rather than calibrate it toward higher recall. Because ABI-185 also trails ABI-183, the negative signal is not merely that a 12-epoch run failed to match a 36-epoch run.

The final-epoch best checkpoint creates some late-improving evidence under the generic budget policy, but the branch-specific evidence is weak: the late jump only recovers ABI-185 to below ABI-183/ABI-184 on aggregate, Google, recall, and connectivity, and the intended recall-preserving objective was not moving in the right direction. A late36 repeat of the exact recall-bridge branch is therefore lower priority than broader in-contract alternatives that do not perturb the line-connected representation so directly.

## Decision

Do not promote ABI-185 and do not reinterpret this capped representative result as full-data evidence. Retain ABI-181 as the current whole-validation-tested aggregate filtered-Dice reference. Retain ABI-184 as the current whole-validation-tested precision/connectivity and negative-patch-discipline reference in the signed-detail full-scale skip ASPP family.

Do not repeat ABI-185 unchanged at the exploratory budget. Do not make ABI-185 the next whole-validation Evaluation Request, because its capped result is not competitive with ABI-181 or ABI-184 and does not answer a promotion-relevant uncertainty. Deprioritize an immediate late36 continuation of the exact recall-bridge branch despite the epoch-12 best checkpoint, because the mechanism degraded connectivity and did not improve recall versus ABI-184.

A reasonable next in-contract direction is to broaden from shared residual recall bridges to a less disruptive calibration mechanism: for example, a close continuation around ABI-184 that preserves the line-connected decoder path while using a separate low-capacity recall sidecar, loss-policy change, data-policy probe, or architecture-family scout to improve MIT positive-patch recall without Candidate-owned thresholding, postprocessing, losses, sampling, augmentation, Artifact Filters, or coordinates. No new Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260903_002344_daa8ef/outputs/best_metrics.json`
- `run_20260903_002344_daa8ef/outputs/final_metrics.json`
- `run_20260903_002344_daa8ef/outputs/metrics.jsonl`
- `run_20260903_002344_daa8ef/outputs/resource_profile.json`
- `run_20260903_002344_daa8ef/outputs/model_summary.json`
- `run_20260903_002344_daa8ef/outputs/prediction_samples/samples.json`
- `run_20260903_002344_daa8ef/outputs/validation_postprocessing/index.json`
- `run_20260903_002344_daa8ef/resolved_manifest.yaml`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_204128_bba815/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_175152_51d2d9/outputs/best_metrics.json`
- `run_20260901_234732_bd5917/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
