# Full-spectral BTD+SZA signed-detail full-scale skip ASPP line-aux mask-sidecar follow-up

research-figures: []

## Scope

This note records ABI-186 after Run `run_20260903_012452_9e35a4` completed.

Source Runs:

- ABI-186 signed-detail full-scale skip ASPP with Line plus Centerline auxiliary supervision and a separate mask-logit sidecar: `run_20260903_012452_9e35a4`
- ABI-185 shared recall-bridge negative reference: `run_20260903_002344_daa8ef`
- ABI-184 late36 Line plus Centerline auxiliary precision/connectivity reference: `run_20260902_213856_2c04ac`; whole-validation Evaluation `eval_evalreq_abi184_wholeval_failure_buckets_v1`
- ABI-183 exploratory Line plus Centerline auxiliary parent: `run_20260902_204128_bba815`
- ABI-181 signed-detail full-scale skip ASPP late36 aggregate reference: `run_20260902_150611_cbbf35`; whole-validation Evaluation `eval_evalreq_abi181_wholeval_failure_buckets_v1`
- ABI-182 signed-detail line-consensus late36 comparator: `run_20260902_175152_51d2d9`
- ABI-173 signed-detail full-scale skip ASPP 12-epoch parent: `run_20260901_234732_bd5917`; whole-validation Evaluation `eval_evalreq_abi173_wholeval_failure_buckets_v1`
- ABI-154 full-scale skip ASPP/detail decoder precision-connectivity reference: `run_20260901_071026_32d3ec`
- ABI-068 frequency-gated line U-Net focal-Tversky source-balance comparator: `run_20260828_010836_4ccc77`

ABI-186 was a close family-development continuation prompted by ABI-184 and ABI-185. It retained provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD features derived only from approved ABI channels, Solar Geometry Input, signed local/mid-scale detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, line-aware final refinement, BCE-Dice primary loss, provider-derived Line Target auxiliary supervision at weight 0.01, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The intended research change from ABI-185 was replacing the shared pre-logit recall bridge with a neutral, low-capacity additive `MaskRecallSidecar` attached only to `mask_logits`, so the Line and Centerline heads would not be perturbed.

## Contract and resource observation

ABI-186 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary outputs `line_logits` and `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 9,861,453 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,919.0 seconds total wall time, 1,569.2 seconds training wall time, 1,347.8 seconds validation wall time, 15.66 training samples per second, 18.23 validation samples per second, 9,156,214,784 bytes peak CUDA allocated, and 10,680,795,136 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 12, the final exploratory epoch.

## Best-validation comparison

| Run | Candidate | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260903_012452_9e35a4` | ABI-186 mask sidecar | 12 | 0.3779 | 0.3641 | 0.4131 | 0.4645 | 0.3185 | 0.3642 | 0.00248 |
| `run_20260903_002344_daa8ef` | ABI-185 shared recall bridge | 12 | 0.3927 | 0.3810 | 0.4228 | 0.4511 | 0.3477 | 0.3433 | 0.00279 |
| `run_20260902_213856_2c04ac` | ABI-184 line+centerline late36 | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.00261 |
| `run_20260902_204128_bba815` | ABI-183 line+centerline exploratory parent | 12 | 0.3966 | 0.3805 | 0.4389 | 0.4468 | 0.3565 | 0.4546 | 0.00289 |
| `run_20260902_150611_cbbf35` | ABI-181 centerline-only late36 | 22 | 0.4104 | 0.3962 | 0.4486 | 0.4423 | 0.3828 | 0.3639 | 0.00314 |
| `run_20260902_175152_51d2d9` | ABI-182 line-consensus late36 | 32 | 0.4035 | 0.3898 | 0.4362 | 0.4010 | 0.4061 | 0.3365 | 0.00367 |
| `run_20260901_234732_bd5917` | ABI-173 signed-detail full-scale skip ASPP | 12 | 0.3962 | 0.3838 | 0.4269 | 0.4238 | 0.3720 | 0.3203 | 0.00318 |
| `run_20260901_071026_32d3ec` | ABI-154 full-scale skip ASPP/detail decoder | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260828_010836_4ccc77` | ABI-068 frequency-gated line U-Net focal-Tversky | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |

ABI-186 did not meet the intended mask-sidecar success criteria. Relative to ABI-185, it improved precision by 0.0134, connectivity by 0.0208, and reduced filtered predicted-positive fraction from 0.00279 to 0.00248, but this came with materially lower aggregate filtered Dice (-0.0148), MIT filtered Dice (-0.0168), Google filtered Dice (-0.0097), and recall (-0.0291). Relative to ABI-184, ABI-186 is worse on aggregate/source Dice, precision, recall, and connectivity; the slightly smaller positive fraction is not useful because it reflects a more conservative, lower-recall mask rather than better calibrated overlap. Relative to ABI-183, ABI-186 also loses aggregate/source Dice, recall, and especially connectivity, despite modestly higher precision.

Against the broader local references, ABI-186 is not competitive with ABI-181 on aggregate/source Dice or recall, not competitive with ABI-184/ABI-154 on the precision/connectivity tradeoff, and not competitive with ABI-068 or ABI-182 on recall/source balance. These comparisons remain capped representative evidence, not full-data promotion evidence.

## Exploratory trajectory

ABI-186 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was:

`0.2101, 0.2475, 0.3095, 0.2849, 0.3362, 0.3552, 0.3471, 0.3479, 0.3635, 0.3477, 0.3459, 0.3779`.

The final epoch was the selected checkpoint. At epoch 12, raw Dice was 0.3934, filtered Dice was 0.3779, filtered precision was 0.4645, filtered recall was 0.3185, filtered connectivity was 0.3642, and filtered predicted-positive fraction was 0.00248. Source-stratified filtered Dice was 0.3641 for MIT and 0.4131 for Google. MIT had filtered precision 0.4731, recall 0.2959, connectivity 0.3457, and predicted-positive fraction 0.00338; Google had filtered precision 0.4462, recall 0.3846, connectivity 0.3827, and predicted-positive fraction 0.00159.

Raw-to-filtered differences were modest: raw Dice 0.3934 versus filtered Dice 0.3779, raw recall 0.3405 versus filtered recall 0.3185, and raw predicted-positive fraction 0.00265 versus filtered predicted-positive fraction 0.00248. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples include two empty/negative perfect cases and two near-zero per-sample Dice cases under the `first_n` retention policy; they are traceability samples and should not be treated as representative qualitative evidence for the validation distribution.

The epoch-12 best checkpoint is generic late-improving evidence, but it is not compelling branch-development evidence by itself. The final jump only recovers ABI-186 to a result that remains below ABI-185 and ABI-183 on the primary/source Dice and recall metrics, and far below ABI-184 on the line-connectivity property the sidecar was meant to preserve.

## Interpretation

Classify ABI-186 as a completed, finite, non-collapsed but scientifically negative capped exploratory continuation. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The separate mask-only sidecar hypothesis is not supported at the 12-epoch budget. It avoided ABI-185's shared-feature perturbation in a narrow sense by slightly improving connectivity and precision over ABI-185, but it did not solve the core failure mode: fixed-threshold recall and source overlap worsened, especially on MIT. More importantly, it failed to preserve ABI-184-like connectivity or ABI-183-like aggregate/source overlap. The sidecar appears to make the branch more conservative rather than recall-preserving.

Because ABI-186's selected checkpoint is at the final exploratory epoch, a late36 continuation could be argued under the generic budget rule. However, the branch-specific scientific signal is weaker than ABI-184's prior extension case: the mechanism moved recall in the wrong direction, lost substantial connectivity relative to ABI-184/183, and trails even the negative ABI-185 bridge on aggregate/source Dice. An immediate late36 repeat of the exact mask-sidecar branch is therefore lower priority than a broader in-contract alternative.

## Decision

Do not promote ABI-186 and do not reinterpret this capped representative result as full-data evidence. Retain ABI-181 as the current whole-validation-tested aggregate filtered-Dice reference. Retain ABI-184 as the current whole-validation-tested precision/connectivity and negative-patch-discipline reference in the signed-detail full-scale skip ASPP family.

Do not repeat ABI-186 unchanged at the exploratory budget. Do not make ABI-186 the next whole-validation Evaluation Request, because its capped metrics are not competitive with ABI-181 or ABI-184 and do not answer a promotion-relevant uncertainty. Deprioritize an immediate late36 continuation of the exact mask-sidecar branch despite the epoch-12 best checkpoint, because the intended recall-preserving calibration effect was not observed.

A reasonable next in-contract direction is to broaden away from additive recall bridges/sidecars and test a less suppressive calibration route: for example, a loss-policy probe around the ABI-184/183 line-supervised branch, a data-policy probe aimed at MIT recall, or a different line-aware architecture family that preserves high-resolution detail without hardening the fixed-threshold mask. Any continuation should keep provider-owned data, sampling, loss, metric, target, Artifact Filter, thresholding, resource, and lifecycle boundaries, and must not use coordinates or Candidate-owned postprocessing. No new Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260903_012452_9e35a4/outputs/best_metrics.json`
- `run_20260903_012452_9e35a4/outputs/final_metrics.json`
- `run_20260903_012452_9e35a4/outputs/metrics.jsonl`
- `run_20260903_012452_9e35a4/outputs/resource_profile.json`
- `run_20260903_012452_9e35a4/outputs/model_summary.json`
- `run_20260903_012452_9e35a4/outputs/prediction_samples/samples.json`
- `run_20260903_012452_9e35a4/outputs/validation_postprocessing/index.json`
- `run_20260903_012452_9e35a4/resolved_manifest.yaml`
- `run_20260903_002344_daa8ef/outputs/best_metrics.json`
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
