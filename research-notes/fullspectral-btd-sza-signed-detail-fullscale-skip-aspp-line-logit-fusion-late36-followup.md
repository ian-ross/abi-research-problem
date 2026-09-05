# Full-spectral BTD+SZA signed-detail full-scale skip ASPP line-logit fusion late36 follow-up

research-figures: []

## Scope

This note records ABI-189 after late-improving Run `run_20260903_041610_f244a9` completed.

Source Runs:

- ABI-189 signed-detail full-scale skip ASPP with detached Line/Centerline logit fusion and late36 budget: `run_20260903_041610_f244a9`
- ABI-188 exploratory detached line-logit fusion parent: `run_20260903_031950_88e745`
- ABI-184 late36 Line plus Centerline auxiliary precision/connectivity reference: `run_20260902_213856_2c04ac`; whole-validation Evaluation `eval_evalreq_abi184_wholeval_failure_buckets_v1`
- ABI-181 signed-detail full-scale skip ASPP late36 aggregate reference: `run_20260902_150611_cbbf35`; whole-validation Evaluation `eval_evalreq_abi181_wholeval_failure_buckets_v1`
- ABI-183 exploratory Line plus Centerline auxiliary parent: `run_20260902_204128_bba815`
- ABI-187 focal-Tversky Line plus Centerline negative connectivity reference: `run_20260903_022247_88e0dc`
- ABI-068 frequency-gated line U-Net focal-Tversky source-balance comparator: `run_20260828_010836_4ccc77`

ABI-189 was a close family-development continuation of ABI-188. It retained provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD features derived only from approved ABI channels, Solar Geometry Input, signed local/mid-scale detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, line-aware final refinement, BCE-Dice primary loss, provider-derived Line Target auxiliary supervision at weight 0.01, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The only intended research change from ABI-188 was the Harness-reviewed `late_improving` budget request for 36 effective epochs.

## Contract and resource observation

ABI-189 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary outputs `line_logits` and `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 9,838,851 parameters, below the 25,000,000-parameter smoke ceiling. The late-improving request was approved with `budget_class_effective: late_improving`, `effective_max_epochs: 36`, and parent Run `run_20260903_031950_88e745`. The Run completed on the A100 at batch size 4 with 8,560.4 seconds total wall time, 4,572.3 seconds training wall time, 3,985.9 seconds validation wall time, 16.13 training samples per second, 18.50 validation samples per second, 9,041,055,744 bytes peak CUDA allocated, and 10,506,731,520 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 22.

## Best-validation comparison

| Run | Candidate | Best epoch | Filtered Dice | Raw Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260903_041610_f244a9` | ABI-189 line-logit fusion late36 | 22 | 0.4022 | 0.4157 | 0.3917 | 0.4290 | 0.3964 | 0.4083 | 0.2962 | 0.00373 |
| `run_20260903_031950_88e745` | ABI-188 line-logit fusion exploratory | 12 | 0.4013 | 0.4160 | 0.3898 | 0.4317 | 0.4250 | 0.3801 | 0.3903 | 0.00324 |
| `run_20260902_213856_2c04ac` | ABI-184 line+centerline late36 | 23 | 0.4066 | 0.4227 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.00261 |
| `run_20260902_150611_cbbf35` | ABI-181 centerline-only late36 | 22 | 0.4104 | 0.4254 | 0.3962 | 0.4486 | 0.4423 | 0.3828 | 0.3639 | 0.00314 |
| `run_20260902_204128_bba815` | ABI-183 line+centerline exploratory parent | 12 | 0.3966 | 0.4119 | 0.3805 | 0.4389 | 0.4468 | 0.3565 | 0.4546 | 0.00289 |
| `run_20260903_022247_88e0dc` | ABI-187 focal-Tversky line+centerline | 12 | 0.3897 | 0.4033 | 0.3830 | 0.4068 | 0.3785 | 0.4017 | 0.2197 | 0.00385 |
| `run_20260828_010836_4ccc77` | ABI-068 frequency-gated line U-Net focal-Tversky | 12 | 0.3964 | 0.4100 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |

ABI-189 only marginally improved ABI-188 on the v0 primary capped metric: filtered Dice rose from 0.4013 to 0.4022 and MIT filtered Dice rose from 0.3898 to 0.3917. The cost was material: Google filtered Dice fell from 0.4317 to 0.4290, precision fell from 0.4250 to 0.3964, filtered predicted-positive fraction expanded from 0.00324 to 0.00373, and connectivity fell sharply from 0.3903 to 0.2962. Recall improved from 0.3801 to 0.4083, but the gain resembles an over-softened fixed-threshold operating point more than the desired ABI-184-style connected line representation.

Relative to ABI-184, ABI-189 is worse on aggregate filtered Dice by 0.0043, Google filtered Dice by 0.0265, precision by 0.0887, connectivity by 0.1672, and positive-area discipline, while improving recall by 0.0583 and MIT filtered Dice by 0.0038. Relative to ABI-181, ABI-189 is worse on aggregate filtered Dice by 0.0082, raw Dice by 0.0097, MIT filtered Dice by 0.0045, Google filtered Dice by 0.0196, precision by 0.0460, and connectivity by 0.0677; it improves recall by 0.0254 but with a larger filtered predicted-positive fraction.

## Late-improving trajectory

ABI-189 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was:

`0.2018, 0.2672, 0.2735, 0.3061, 0.3436, 0.3602, 0.3789, 0.3258, 0.3704, 0.3540, 0.3762, 0.3905, 0.3709, 0.3718, 0.3853, 0.3864, 0.3766, 0.3756, 0.3749, 0.3690, 0.3877, 0.4022, 0.3930, 0.3747, 0.3569, 0.3959, 0.3864, 0.3850, 0.3958, 0.3681, 0.3810, 0.4008, 0.3794, 0.3960, 0.3807, 0.3887`.

The best checkpoint was epoch 22. Later epochs remained finite but did not surpass it; final epoch 36 declined to filtered Dice 0.3887, raw Dice 0.4032, MIT/Google filtered Dice 0.3748/0.4234, precision 0.4136, recall 0.3665, connectivity 0.3035, and filtered predicted-positive fraction 0.00321. The late budget therefore confirmed that ABI-188's epoch-12 jump was not the exact ceiling, but it did not convert the detached auxiliary-logit fusion mechanism into an ABI-181/184-level aggregate or connectivity point.

At the selected epoch 22 checkpoint, raw Dice was 0.4157 versus filtered Dice 0.4022, raw recall 0.4370 versus filtered recall 0.4083, and raw predicted-positive fraction 0.00400 versus filtered predicted-positive fraction 0.00373. Source-stratified filtered Dice was 0.3917 for MIT and 0.4290 for Google. MIT had filtered precision 0.4008, recall 0.3830, connectivity 0.3026, and predicted-positive fraction 0.00516; Google had filtered precision 0.3865, recall 0.4821, connectivity 0.2897, and predicted-positive fraction 0.00230. Raw-to-filtered differences are modest enough that this does not indicate primary Artifact Filter dependence, but the low filtered connectivity indicates the mask-logit residual weakened the intended line structure.

The fixed first-four retained prediction samples include three near-zero per-sample Dice cases and one empty/negative perfect case under the `first_n` retention policy. They are traceability samples and should not be treated as representative qualitative evidence for the validation distribution.

## Interpretation

Classify ABI-189 as a completed, finite, non-collapsed, scientifically useful negative-to-mixed capped late-improving continuation. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The narrow late36 hypothesis is mostly unsupported. The longer budget slightly improved ABI-188's capped aggregate and MIT filtered Dice and recovered recall, but failed the main continuation criterion of retaining useful line connectivity. The best checkpoint fell below ABI-181 and ABI-184 on the primary capped metric and below ABI-068 on connectivity. Compared with ABI-184's whole-validation-tested precision/connectivity reference, detached auxiliary-logit fusion appears to soften the mask too aggressively: it buys recall through a larger, less connected positive mask rather than combining ABI-184's direct line supervision with ABI-181-level overlap.

The result does not eliminate the broader signed-detail full-scale skip ASPP family or the direct Line Target auxiliary idea. It does support stopping this exact detached auxiliary-logit-fusion branch after one exploratory and one approved late-improving continuation. The branch has now shown its likely tradeoff: modest recall/MIT gains with precision, Google, positive-area, and especially connectivity losses.

## Decision

Do not promote ABI-189 and do not reinterpret this capped representative result as full-data evidence. Retain ABI-181 as the current whole-validation-tested aggregate filtered-Dice reference. Retain ABI-184 as the whole-validation-tested precision/connectivity and negative-patch-discipline reference in the signed-detail full-scale skip ASPP family.

Do not repeat ABI-189 unchanged and do not request a whole-validation Evaluation for it unless a later review specifically needs diagnostic evidence about this negative tradeoff. The next in-contract hypothesis should move away from additive detached auxiliary-logit boosting and toward a mechanism that preserves ABI-184's direct line-supervised connectivity while improving recall/calibration, such as feature-level line-context calibration, a less permissive learned mask refinement path, or a new high-resolution line-aware architecture under provider-approved inputs, trusted BCE-Dice or focal-Tversky loss, and Harness-owned data/loss/metric/Artifact Filter boundaries. No new Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260903_041610_f244a9/outputs/best_metrics.json`
- `run_20260903_041610_f244a9/outputs/final_metrics.json`
- `run_20260903_041610_f244a9/outputs/metrics.jsonl`
- `run_20260903_041610_f244a9/outputs/resource_profile.json`
- `run_20260903_041610_f244a9/outputs/model_summary.json`
- `run_20260903_041610_f244a9/outputs/prediction_samples/samples.json`
- `run_20260903_041610_f244a9/outputs/validation_postprocessing/index.json`
- `run_20260903_041610_f244a9/resolved_manifest.yaml`
- `run_20260903_041610_f244a9/candidate/budget_request.yaml`
- `run_20260903_031950_88e745/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_150611_cbbf35/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_204128_bba815/outputs/best_metrics.json`
- `run_20260903_022247_88e0dc/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
