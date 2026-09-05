# Full-spectral BTD+SZA signed-detail full-scale skip ASPP line-feature calibration follow-up

research-figures: []

## Scope

This note records ABI-190 after Run `run_20260903_064825_5a446f` completed.

Source Runs:

- ABI-190 signed-detail full-scale skip ASPP with conservative feature-level line-context calibration: `run_20260903_064825_5a446f`
- ABI-184 late36 Line plus Centerline auxiliary precision/connectivity reference: `run_20260902_213856_2c04ac`; whole-validation Evaluation `eval_evalreq_abi184_wholeval_failure_buckets_v1`
- ABI-189 detached line-logit fusion late36 negative-to-mixed reference: `run_20260903_041610_f244a9`
- ABI-188 detached line-logit fusion exploratory parent: `run_20260903_031950_88e745`
- ABI-181 signed-detail full-scale skip ASPP late36 aggregate reference: `run_20260902_150611_cbbf35`; whole-validation Evaluation `eval_evalreq_abi181_wholeval_failure_buckets_v1`
- ABI-183 exploratory Line plus Centerline auxiliary parent: `run_20260902_204128_bba815`
- ABI-068 frequency-gated line U-Net focal-Tversky source-balance comparator: `run_20260828_010836_4ccc77`

ABI-190 was an exploratory family-development continuation of the ABI-184 signed-detail full-scale skip ASPP branch. It retained provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD features derived only from approved ABI channels, Solar Geometry Input, signed local/mid-scale detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, line-aware final refinement, BCE-Dice primary loss, provider-derived Line Target auxiliary supervision at weight 0.01, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The intended research change from ABI-184 was adding a zero-initialized bounded feature-level line-context calibration module before the primary mask head, without adding auxiliary logits directly to `mask_logits`.

## Contract and resource observation

ABI-190 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary outputs `line_logits` and `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 10,013,851 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 3,200.0 seconds total wall time, 1,749.4 seconds training wall time, 1,448.4 seconds validation wall time, 14.05 training samples per second, 16.97 validation samples per second, 10,259,532,288 bytes peak CUDA allocated, and 11,817,451,520 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 11.

## Best-validation comparison

| Run | Candidate | Best epoch | Filtered Dice | Raw Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260903_064825_5a446f` | ABI-190 feature-level line calibration | 11 | 0.3717 | 0.3849 | 0.3712 | 0.3727 | 0.3656 | 0.3779 | 0.1509 | 0.00375 |
| `run_20260902_213856_2c04ac` | ABI-184 line+centerline late36 | 23 | 0.4066 | 0.4227 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.00261 |
| `run_20260903_041610_f244a9` | ABI-189 line-logit fusion late36 | 22 | 0.4022 | 0.4157 | 0.3917 | 0.4290 | 0.3964 | 0.4083 | 0.2962 | 0.00373 |
| `run_20260903_031950_88e745` | ABI-188 line-logit fusion exploratory | 12 | 0.4013 | 0.4160 | 0.3898 | 0.4317 | 0.4250 | 0.3801 | 0.3903 | 0.00324 |
| `run_20260902_150611_cbbf35` | ABI-181 centerline-only late36 | 22 | 0.4104 | 0.4254 | 0.3962 | 0.4486 | 0.4423 | 0.3828 | 0.3639 | 0.00314 |
| `run_20260902_204128_bba815` | ABI-183 line+centerline exploratory parent | 12 | 0.3966 | 0.4119 | 0.3805 | 0.4389 | 0.4468 | 0.3565 | 0.4546 | 0.00289 |
| `run_20260828_010836_4ccc77` | ABI-068 frequency-gated line U-Net focal-Tversky | 12 | 0.3964 | 0.4100 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |

ABI-190 did not meet the family-development success criteria. Relative to ABI-184, it improved filtered recall only from 0.3500 to 0.3779, but aggregate filtered Dice fell by 0.0349, MIT filtered Dice by 0.0167, Google filtered Dice by 0.0828, precision by 0.1194, connectivity by 0.3125, and filtered predicted-positive fraction expanded from 0.00261 to 0.00375. The intended feature-level calibration therefore did not preserve ABI-184's clean, connected Line Target operating point.

Relative to ABI-189, ABI-190 is worse on aggregate filtered Dice, both Dataset Sources, precision, recall, connectivity, and raw Dice while carrying nearly the same filtered predicted-positive fraction. Relative to ABI-188, ABI-190 similarly loses aggregate/source Dice, precision, and especially connectivity without gaining recall. Against ABI-181, ABI-190 approaches the recall value but loses the primary capped metric by 0.0388, MIT by 0.0250, Google by 0.0759, precision by 0.0767, and connectivity by 0.2130. Against ABI-068, ABI-190 is below on every listed comparison except a modestly larger predicted-positive fraction. These comparisons remain capped representative evidence, not full-data promotion evidence.

## Exploratory trajectory

ABI-190 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was:

`0.2238, 0.2800, 0.3005, 0.3201, 0.3264, 0.3284, 0.3150, 0.3646, 0.3702, 0.3298, 0.3717, 0.3201`.

The selected epoch 11 checkpoint is near the final exploratory epoch, but the trajectory is oscillatory rather than convincingly late-improving: epoch 12 regressed to filtered Dice 0.3201, precision 0.2659, recall 0.4018, connectivity 0.1418, and filtered predicted-positive fraction 0.00548. This final-epoch behavior looks like unstable positive-area expansion, not a useful extension-eligible plateau.

At the selected epoch 11 checkpoint, raw Dice was 0.3849 versus filtered Dice 0.3717, raw recall 0.4042 versus filtered recall 0.3779, and raw predicted-positive fraction 0.00399 versus filtered predicted-positive fraction 0.00375. Source-stratified filtered Dice was nearly source-balanced but low: 0.3712 for MIT and 0.3727 for Google. MIT had filtered precision 0.3959, recall 0.3494, connectivity 0.1688, and predicted-positive fraction 0.00477. Google had filtered precision 0.3126, recall 0.4614, connectivity 0.1329, and predicted-positive fraction 0.00273. Raw-to-filtered differences are modest enough that this does not indicate primary Artifact Filter dependence, but the very low connectivity and weak Google precision indicate that the calibration module fragmented or softened the mask representation.

The fixed first-four retained prediction samples all have near-zero per-sample Dice under the `first_n` retention policy. They are traceability samples and should not be treated as representative qualitative evidence for the validation distribution.

## Interpretation

Classify ABI-190 as a completed, finite, non-collapsed, scientifically negative capped exploratory continuation. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch; the failure class is `bad_research_result` for this exact feature-level line-calibration hypothesis.

The hypothesis that a conservative feature-space calibration path could recover recall while preserving ABI-184-style connectivity is unsupported. The module delivered a small recall lift over ABI-184, but the cost was larger than both detached logit-fusion branches on the metrics the design was meant to protect. In particular, ABI-190's filtered connectivity 0.1509 is far below ABI-184, ABI-183, ABI-188, ABI-189, ABI-181, and ABI-068. The source-balanced Dice values are not catastrophically single-source, but they are uniformly weak enough that this is not a candidate for whole-validation diagnostics.

The result does not eliminate the broader signed-detail full-scale skip ASPP family or the direct Line plus Centerline auxiliary idea. It does support stopping this exact feature-level line-calibration branch: both logit-level and feature-level attempts to soften ABI-184's conservative fixed-threshold operating point have now degraded line connectivity instead of preserving it.

## Decision

Do not promote ABI-190 and do not reinterpret this capped representative result as full-data evidence. Retain ABI-181 as the current whole-validation-tested aggregate filtered-Dice reference. Retain ABI-184 as the whole-validation-tested precision/connectivity and negative-patch-discipline reference in the signed-detail full-scale skip ASPP family.

Do not repeat ABI-190 unchanged, do not request a late36 continuation despite the epoch-11 selected checkpoint, and do not request a whole-validation Evaluation for it. The next in-contract hypothesis should move away from local calibration modules around ABI-184 and broaden to a different high-resolution line-aware architecture or data/loss-policy probe that can recover recall without collapsing the connectivity advantage, while continuing to use provider-approved inputs, trusted losses and auxiliary targets, Harness-owned sampling/loss/metric/Artifact Filter boundaries, and no Candidate-owned thresholding or postprocessing. No new Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260903_064825_5a446f/outputs/best_metrics.json`
- `run_20260903_064825_5a446f/outputs/final_metrics.json`
- `run_20260903_064825_5a446f/outputs/metrics.jsonl`
- `run_20260903_064825_5a446f/outputs/resource_profile.json`
- `run_20260903_064825_5a446f/outputs/model_summary.json`
- `run_20260903_064825_5a446f/outputs/prediction_samples/samples.json`
- `run_20260903_064825_5a446f/outputs/validation_postprocessing/index.json`
- `run_20260903_064825_5a446f/resolved_manifest.yaml`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260903_041610_f244a9/outputs/best_metrics.json`
- `run_20260903_031950_88e745/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_204128_bba815/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
