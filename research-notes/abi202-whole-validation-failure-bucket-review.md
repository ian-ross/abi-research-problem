# ABI-202 whole-validation failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi202_wholeval_failure_buckets_v1` for ABI-202 Run `run_20260904_043143_ee0005`.

The evaluation request asked whether ABI-202's late36 cross-scale directional-consensus ASPP capped-best improvement to 0.4276 `val/filtered_dice` at epoch 34 survived beyond the trusted 1,024-record-per-source representative validation cap, and whether whole-validation failure buckets show a genuinely stronger tradeoff than ABI-181, ABI-184, ABI-192, and ABI-196. This is diagnostic evidence only; promotion remains operator-reviewed.

Primary comparison references:

- ABI-202 cross-scale directional-consensus ASPP late36 Run: `run_20260904_043143_ee0005`, Evaluation `eval_evalreq_abi202_wholeval_failure_buckets_v1`
- ABI-201 exploratory cross-scale directional-consensus parent Run: `run_20260904_032624_7e855a`
- ABI-196 ridge-detail bridge ASPP late36 aggregate reference: `run_20260903_195527_248472`, Evaluation `eval_evalreq_abi196_wholeval_failure_buckets_v1`
- ABI-181 signed-detail full-scale skip ASPP late36 prior aggregate reference: `run_20260902_150611_cbbf35`, Evaluation `eval_evalreq_abi181_wholeval_failure_buckets_v1`
- ABI-184 signed-detail Line plus Centerline precision/connectivity reference: `run_20260902_213856_2c04ac`, Evaluation `eval_evalreq_abi184_wholeval_failure_buckets_v1`
- ABI-192 directional-lattice late36 comparator: `run_20260903_085513_f395ad`, Evaluation `eval_evalreq_abi192_wholeval_failure_buckets_v1`
- Canonical MCAST 1.1 and MCAST 2.1 summaries from `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`

## Whole-validation metrics

At threshold 0.5 on the full 3,088-sample Working Validation Split, ABI-202 reached:

| Metric | ABI-202 whole validation |
| --- | ---: |
| Filtered Dice | 0.4312 |
| MIT filtered Dice | 0.4141 |
| Google filtered Dice | 0.4644 |
| Filtered precision | 0.4431 |
| Filtered recall | 0.4199 |
| Filtered contrail connectivity | 0.4625 |
| Filtered predicted-positive pixels | 672,206 |
| Filtered false-positive pixels | 374,370 |
| Filtered false-negative pixels | 411,527 |

ABI-202's capped selected-checkpoint signal survived whole-validation evaluation and became the strongest aggregate filtered-Dice Result in local whole-validation-tested Research History. The capped best-validation filtered Dice was 0.4276 at epoch 34; whole-validation filtered Dice was 0.4312. MIT filtered Dice rose from 0.4120 capped to 0.4141 whole validation, while Google softened only slightly from 0.4682 capped to 0.4644 whole validation. Precision, recall, connectivity, and predicted-positive area remained source-informative and non-collapsed.

Relative to ABI-196, ABI-202 improves aggregate filtered Dice (0.4312 versus 0.4147), MIT filtered Dice (0.4141 versus 0.4026), Google filtered Dice (0.4644 versus 0.4368), precision (0.4431 versus 0.4379), recall (0.4199 versus 0.3938), connectivity (0.4625 versus 0.3827), and false negatives (411,527 versus 430,003). The cost is a larger whole-split predicted-positive area and more aggregate false-positive pixels (374,370 versus 358,660), although negative-patch false-positive burden improved in the per-sample buckets.

Relative to ABI-181, ABI-202 improves aggregate, MIT, and Google filtered Dice, recall, connectivity, and false negatives. It gives up a small amount of precision (0.4431 versus 0.4466) and predicts more positive pixels. Relative to ABI-184, ABI-202 strongly improves aggregate, MIT, Google, and recall, but ABI-184 remains the high-precision and strictest negative-patch-discipline reference. Relative to ABI-192, ABI-202 improves every primary aggregate/source metric except raw predicted-positive compactness.

Against canonical MCAST context, ABI-202's filtered Dice 0.4312 is above MCAST 1.1 (0.3842) and MCAST 2.1 (0.3873). Its precision remains below MCAST 1.1 and above MCAST 2.1, its recall is above MCAST 1.1 and below MCAST 2.1, and its connectivity sits below MCAST 1.1 but well above MCAST 2.1. This is comparison context only, not a promotion claim.

## Threshold behavior

The threshold sweep shows that ABI-202 is not dependent on the exact 0.5 threshold and has modest diagnostic headroom at lower thresholds. Filtered Dice improves from 0.4312 at threshold 0.5 to 0.4337 at threshold 0.25, with precision 0.4113 and recall 0.4587. The closest filtered precision/recall balance is threshold 0.40, with Dice 0.4327, precision 0.4320, recall 0.4335, and a 0.0015 absolute precision/recall gap. Raw Dice similarly improves from 0.4458 at threshold 0.5 to 0.4475 at threshold 0.30.

This does not authorize Candidate-owned thresholding, calibration, postprocessing, losses, metrics, or Artifact Filters. The design lesson is that ABI-202 learned a better-calibrated and stronger whole-validation checkpoint than ABI-196, with threshold-sweep upside that is smaller than the main fixed-threshold improvement.

## Failure-bucket observations

Failure buckets explain why ABI-202 is a more balanced aggregate reference while ABI-184 still matters for strict clutter discipline:

1. Negative-patch clutter improved versus most aggregate references. Among 2,003 negative validation patches, ABI-202 produced at least one filtered predicted-positive pixel on 1,013 patches. Median negative-patch false-positive count was 1 pixel. Total negative-patch false-positive pixels were 71,310, with 214 negative patches above 100 filtered false-positive pixels, 9 above 500, and none above 1,000. This is better than ABI-181, ABI-192, and ABI-196 on total negative-patch false positives, but still worse than ABI-184's 53,814 total and 946 any-FP negative patches.
2. Positive-patch severe misses also improved. ABI-202 had 47 positive validation patches with zero filtered predicted-positive pixels, 179 positive patches below 0.1 filtered Dice, 233 below 0.2 filtered Dice, and 240 below 0.2 filtered recall. It is not best on zero-prediction positives, but it improves the low-Dice and low-recall tails versus ABI-181, ABI-184, ABI-192, and ABI-196.
3. Median positive-patch quality is a major strength. ABI-202's median positive-patch filtered Dice was 0.4275, median precision 0.4914, and median recall 0.4597. By Dataset Source, median positive-patch filtered Dice was 0.3951 on MIT and 0.4720 on Google; median precision was 0.4375 on MIT and 0.5477 on Google; median recall was 0.4085 on MIT and 0.5058 on Google. The median Dice and recall exceed the recent whole-validation references and support ABI-202's aggregate improvement as more than capped-subset noise.

Artifact Filters removed 45,161 predicted-positive pixels over the full split, corresponding to 180,644 square kilometers under the evaluation metadata's pixel-area accounting. Raw Dice was 0.4458 versus filtered Dice 0.4312; raw predicted-positive pixels were 717,367 versus 672,206 filtered. Filtering lowered Dice modestly, as in nearby SZA-aware ASPP branches, and does not indicate primary Artifact Filter dependence.

The retained diagnostic sample GeoTIFFs are traceability artifacts selected under the bounded evaluation policy. This note does not reproduce individual scene identifiers, coordinates, raw samples, or images.

## Training trajectory and resource observations

ABI-202 completed 36/36 late-improving epochs with finite losses and non-collapsed, Dataset Source-informative predictions. The Harness approved the candidate-local `late_improving` budget request against parent Run `run_20260904_032624_7e855a`; effective max epochs were 36 and the Docker wall-clock budget was 10,800 seconds.

The best selected checkpoint occurred at epoch 34. The trajectory was volatile but productive: filtered Dice was 0.3889 at epoch 12, 0.4113 at epoch 22, 0.4197 at epoch 32, dipped to 0.3780 at epoch 33, peaked at 0.4276 at epoch 34, dropped to 0.4057 at epoch 35, and finished at 0.4165 at epoch 36. The selected epoch-34 checkpoint therefore captured a real late-budget improvement, while the final epoch remained above the prior ABI-201 exploratory checkpoint and close to ABI-196's whole-validation operating point.

The Run stayed inside the active Workspace Configuration: late-improving budget, batch size 4, constant learning rate, disabled early stopping, provider-owned source-balanced capped selection, trusted random mirroring, and A100 execution. The resolved manifest uses approved `abi_16ch_plus_sza` input mode; forbidden longitude and latitude source channels are excluded; outputs are `mask_logits`, `line_logits`, and `centerline_logits`; and the model summary reports 8,172,287 parameters under the 25,000,000-parameter ceiling.

Resource profiling completed successfully with about 10.45 GB peak allocated CUDA memory, about 11.89 GB peak reserved CUDA memory, and about 9,984 seconds total run wall time, within the 10,800-second late-improving timeout. No contract, resource, numerical, or lifecycle failure is indicated in the Harness-observed artifacts.

## Interpretation

Classify ABI-202's whole-validation evaluation as valid, finite, non-collapsed diagnostic evidence for the late-improving cross-scale directional-consensus ASPP branch. The longer budget was useful: the parent ABI-201 finished its exploratory run as a promising but sub-frontier precision/connectivity tradeoff, while ABI-202 produced a selected checkpoint that exceeded ABI-196 on whole-validation aggregate filtered Dice and improved both Dataset Sources, recall, connectivity, and median positive-patch quality.

ABI-202 should replace ABI-196 as the current whole-validation-tested aggregate filtered-Dice reference in local Research History. ABI-184 should remain the precision/connectivity and strictest negative-patch-discipline reference, because ABI-202's aggregate gain still carries more aggregate false positives and lower precision than ABI-184. ABI-196 remains useful mainly as the prior aggregate ridge-detail bridge comparator, not as the current best aggregate reference.

The exact ABI-202 architecture is sufficiently characterized for the current budget. The selected checkpoint is strong; the final epochs show volatility rather than a clean monotone truncation; and the whole-validation failure buckets point to a comparatively balanced operating point rather than an unchanged need for another epoch-extension repeat.

## Decision

Do not promote ABI-202 or reinterpret this whole-validation diagnostic as deployment evidence. Retain ABI-202 as the current whole-validation aggregate filtered-Dice reference; retain ABI-184 as the precision/connectivity and negative-patch-discipline reference; retain ABI-196 and ABI-181 as prior aggregate references for regression context.

Do not repeat ABI-202 unchanged and do not request another longer budget for the same exact branch. A reasonable next in-contract hypothesis is a controlled architecture continuation that starts from ABI-202's cross-scale directional-consensus bridge and targets the remaining aggregate false-positive burden without sacrificing its improved recall, Google Dice, connectivity, and median positive-patch quality. Examples within the current contract include a conservative foreground-logit calibration branch, a lighter clutter-suppression residual that does not move Artifact Filters into candidate code, or a focused auxiliary/loss-policy probe using only trusted allowlisted targets and losses. Candidate code must continue to use approved ABI channel inputs only and must not implement thresholding, data loading, losses, metrics, Artifact Filters, sampling behavior, or coordinate features.

No Capability Request or Campaign Report is required from this diagnostic result.

## Artifact references

- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/summary.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260904_043143_ee0005/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/final_metrics.json`
- `run_20260904_043143_ee0005/outputs/metrics.jsonl`
- `run_20260904_043143_ee0005/outputs/resource_profile.json`
- `run_20260904_043143_ee0005/outputs/model_summary.json`
- `run_20260904_043143_ee0005/resolved_manifest.yaml`
- `run_20260904_043143_ee0005/candidate/budget_request.yaml`
- `run_20260904_032624_7e855a/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260903_085513_f395ad/outputs/evaluations/eval_evalreq_abi192_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260903_085513_f395ad/outputs/evaluations/eval_evalreq_abi192_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260903_085513_f395ad/outputs/evaluations/eval_evalreq_abi192_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260903_195527_248472/outputs/evaluations/eval_evalreq_abi196_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260903_195527_248472/outputs/evaluations/eval_evalreq_abi196_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260903_195527_248472/outputs/evaluations/eval_evalreq_abi196_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
