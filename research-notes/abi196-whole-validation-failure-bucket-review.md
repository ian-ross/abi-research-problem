# ABI-196 whole-validation failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi196_wholeval_failure_buckets_v1` for ABI-196 Run `run_20260903_195527_248472`.

The evaluation request asked whether ABI-196's late36 ridge-detail bridge ASPP capped-best improvement to 0.4133 `val/filtered_dice` survived on the full 3,088-sample Working Validation Split, and whether failure buckets show that its high-connectivity, precision-inclined branch is genuinely stronger than ABI-181, ABI-184, and ABI-192 rather than capped-subset noise. This is diagnostic evidence only; promotion remains operator-reviewed.

Primary comparison references:

- ABI-196 ridge-detail bridge ASPP late36 Run: `run_20260903_195527_248472`, Evaluation `eval_evalreq_abi196_wholeval_failure_buckets_v1`
- ABI-195 exploratory ridge-detail bridge parent Run: `run_20260903_135523_8976a0`
- ABI-181 signed-detail full-scale skip ASPP late36 aggregate reference: `run_20260902_150611_cbbf35`, Evaluation `eval_evalreq_abi181_wholeval_failure_buckets_v1`
- ABI-184 signed-detail full-scale skip ASPP Line plus Centerline auxiliary precision/connectivity reference: `run_20260902_213856_2c04ac`, Evaluation `eval_evalreq_abi184_wholeval_failure_buckets_v1`
- ABI-192 directional-lattice late36 recall comparator: `run_20260903_085513_f395ad`, Evaluation `eval_evalreq_abi192_wholeval_failure_buckets_v1`
- Canonical MCAST 1.1 and MCAST 2.1 summaries from `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`

## Whole-validation metrics

At threshold 0.5 on the full 3,088-sample Working Validation Split, ABI-196 reached:

| Metric | ABI-196 whole validation |
| --- | ---: |
| Filtered Dice | 0.4147 |
| MIT filtered Dice | 0.4026 |
| Google filtered Dice | 0.4368 |
| Filtered precision | 0.4379 |
| Filtered recall | 0.3938 |
| Filtered contrail connectivity | 0.3827 |
| Filtered predicted-positive pixels | 638,020 |
| Filtered false-positive pixels | 358,660 |
| Filtered false-negative pixels | 430,003 |

ABI-196's capped selected-checkpoint signal survived whole-validation evaluation and became the strongest aggregate filtered-Dice Result in local whole-validation-tested Research History. The capped best-validation filtered Dice was 0.4133 at epoch 34; whole-validation filtered Dice was 0.4147. MIT filtered Dice rose slightly from 0.4007 capped to 0.4026 whole validation, while Google softened from 0.4442 capped to 0.4368 whole validation. Precision, recall, connectivity, and predicted-positive area remained close to the selected checkpoint's capped operating point.

Relative to ABI-181, ABI-196 improves aggregate filtered Dice (0.4147 versus 0.4124), MIT filtered Dice (0.4026 versus 0.3988), recall (0.3938 versus 0.3832), connectivity (0.3827 versus 0.3676), and false negatives (430,003 versus 437,567). The tradeoff is lower Google filtered Dice (0.4368 versus 0.4395), lower precision (0.4379 versus 0.4466), more predicted-positive pixels (638,020 versus 608,649), and more false positives (358,660 versus 336,853). ABI-196 should therefore replace ABI-181 as the aggregate whole-validation filtered-Dice reference, but not as a cleaner false-positive reference.

Relative to ABI-184, ABI-196 improves aggregate filtered Dice, MIT filtered Dice, recall, and false negatives, but remains much weaker on ABI-184's main strengths: Google filtered Dice, precision, connectivity, predicted-positive discipline, and negative-patch false-positive burden. ABI-184 remains the precision/connectivity and negative-patch-discipline reference.

Relative to ABI-192, ABI-196 improves aggregate filtered Dice, MIT filtered Dice, precision, recall, connectivity, and false negatives, with similar Google filtered Dice. ABI-192 no longer needs to be retained as the main recall comparator among late36 signed-detail variants; ABI-196 provides better recall while also improving precision and connectivity at the fixed threshold.

Against canonical MCAST context, ABI-196's filtered Dice 0.4147 is above MCAST 1.1 (0.3842) and MCAST 2.1 (0.3873). ABI-196's precision is below MCAST 1.1 but above MCAST 2.1, its recall is above MCAST 1.1 and below MCAST 2.1, and its connectivity is between MCAST 2.1 and MCAST 1.1. This is comparison context only, not a promotion claim.

## Threshold behavior

The threshold sweep shows meaningful diagnostic headroom at lower thresholds. ABI-196 improves from filtered Dice 0.4147 at threshold 0.5 to 0.4197 at threshold 0.15. At threshold 0.15, filtered precision is 0.3965 and recall is 0.4458. The closest filtered precision/recall balance is threshold 0.30, with Dice 0.4185, precision 0.4187, recall 0.4183, and an extremely small precision/recall gap. Raw Dice similarly improves from 0.4295 at threshold 0.5 to 0.4335 at threshold 0.20.

This does not authorize Candidate-owned thresholding, calibration, postprocessing, losses, metrics, or Artifact Filters. The design lesson is that the ridge-detail bridge learned a reasonably calibrated aggregate checkpoint with modest threshold-sweep upside, not merely a too-conservative high-threshold representation. ABI-184 still has larger best-threshold Dice headroom, but ABI-196 exceeds ABI-181 and ABI-192 on fixed-threshold aggregate Dice and slightly exceeds their best-threshold filtered-Dice diagnostics.

## Failure-bucket observations

Failure buckets explain why ABI-196 improves aggregate Dice while not settling the false-positive-discipline problem:

1. Negative-patch clutter is mixed. Among 2,003 negative validation patches, ABI-196 produced at least one filtered predicted-positive pixel on 1,241 patches. Median negative-patch false-positive count was 9 pixels. Total negative-patch false-positive pixels were 88,298, with 274 negative patches above 100 filtered false-positive pixels, 14 above 500, and none above 1,000. This is better than ABI-192's 100,925 negative-patch false-positive pixels but worse than ABI-181's 77,592 and much worse than ABI-184's 53,814. The aggregate gain is therefore not a clutter-discipline gain.
2. Positive-patch severe misses are competitive but not uniformly best. ABI-196 had 36 positive validation patches with zero filtered predicted-positive pixels, 187 positive patches below 0.1 filtered Dice, 244 below 0.2 filtered Dice, and 255 below 0.2 filtered recall. This improves ABI-184's conservative positive-miss profile and slightly improves ABI-181 on the low-recall tail, but ABI-181 has fewer zero-prediction positives and fewer very-low-Dice positives. ABI-192 has fewer zero-prediction positives but a worse low-recall tail.
3. Median positive-patch quality is a main strength. ABI-196's median positive-patch filtered Dice was 0.4187, median precision 0.4804, and median recall 0.4420. By Dataset Source, median positive-patch filtered Dice was 0.3919 on MIT and 0.4462 on Google; median precision was 0.4532 on MIT and 0.4966 on Google; median recall was 0.4149 on MIT and 0.4694 on Google. The median recall is stronger than ABI-181, ABI-184, and ABI-192, and the MIT median Dice is stronger than the recent aggregate references. This supports ABI-196's aggregate improvement despite its false-positive cost.

Artifact Filters removed 40,331 predicted-positive pixels over the full split, corresponding to 161,324 square kilometers under the evaluation metadata's pixel-area accounting. Raw Dice was 0.4295 versus filtered Dice 0.4147; raw predicted-positive pixels were 678,351 versus 638,020 filtered. Filtering lowered Dice modestly, comparable to nearby SZA-aware ASPP branches, and does not indicate primary Artifact Filter dependence.

The retained diagnostic sample GeoTIFFs are traceability artifacts selected under the bounded evaluation policy. This note does not reproduce individual scene identifiers, coordinates, raw samples, or images.

## Training trajectory and resource observations

ABI-196 completed 36/36 late-improving epochs with finite losses and non-collapsed, source-informative predictions. The Harness approved the candidate-local `late_improving` budget request against parent Run `run_20260903_135523_8976a0`; effective max epochs were 36 and the Docker wall-clock budget was 10,800 seconds.

The best selected checkpoint occurred at epoch 34. The late trajectory was informative but volatile: filtered Dice was 0.3834 at epoch 12, 0.4069 at epoch 22, 0.4063 at epoch 33, peaked at 0.4133 at epoch 34, dropped to 0.3683 at epoch 35, and partially recovered to 0.4002 at epoch 36. The final epoch shifted toward a much more conservative high-precision/high-connectivity operating point (precision 0.4896, connectivity 0.4852, recall 0.3385), while the selected epoch-34 checkpoint produced the best aggregate Dice and was the model used for whole-validation diagnostics.

The Run stayed inside the active Workspace Configuration: late-improving budget, batch size 4, constant learning rate, disabled early stopping, provider-owned source-balanced capped selection, and A100 execution. Resource profiling completed successfully with about 10.9 GB peak allocated CUDA memory and about 10,011 seconds total run wall time, within the 10,800-second late-improving timeout. No contract, resource, numerical, or lifecycle failure is indicated in the Harness-observed artifacts.

## Interpretation

Classify ABI-196's whole-validation evaluation as valid, finite, non-collapsed diagnostic evidence for the late-improving ridge-detail bridge ASPP branch. The longer budget was useful: the parent ABI-195 finished its exploratory run below the main references, but the late36 continuation produced a selected checkpoint that exceeded ABI-181 on whole-validation aggregate filtered Dice and improved the MIT/source-balance side of the frontier.

ABI-196 should replace ABI-181 as the current whole-validation-tested aggregate filtered-Dice reference in local Research History. It should not replace ABI-184 as the precision/connectivity or negative-patch-discipline reference, and it should not be treated as a promotion decision. The remaining weakness is a familiar one: the branch gains recall and median positive-patch quality while paying with too many false positives on negative patches and slightly weaker Google Dice than ABI-181/184.

The exact ABI-196 architecture is sufficiently characterized for the current budget: the selected checkpoint is strong, the final two epochs show volatility rather than a clean monotone truncation, and the whole-validation failure buckets point to architecture/calibration tradeoffs rather than an unchanged epoch-extension question.

## Decision

Do not promote ABI-196 or reinterpret this whole-validation diagnostic as deployment evidence. Retain ABI-196 as the current whole-validation aggregate filtered-Dice reference; retain ABI-184 as the precision/connectivity and negative-patch-discipline reference; retain ABI-181 as the prior aggregate reference and a cleaner false-positive comparator.

Do not repeat ABI-196 unchanged and do not request another longer budget for the same exact branch. A reasonable next in-contract hypothesis is a controlled architecture continuation that starts from ABI-196's ridge-detail bridge but targets negative-patch false-positive burden without sacrificing its improved MIT/median-positive recall. Examples within the current contract include a conservative foreground-logit calibration/residual gate, a cleaner line-consistency side branch, or a loss-policy probe against the same ridge-detail architecture using the trusted allowlist. Candidate code must continue to use approved ABI channel inputs only and must not implement thresholding, data loading, losses, metrics, Artifact Filters, or sampling behavior.

No Capability Request or Campaign Report is required from this diagnostic result.

## Artifact references

- `run_20260903_195527_248472/outputs/evaluations/eval_evalreq_abi196_wholeval_failure_buckets_v1/summary.json`
- `run_20260903_195527_248472/outputs/evaluations/eval_evalreq_abi196_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260903_195527_248472/outputs/evaluations/eval_evalreq_abi196_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260903_195527_248472/outputs/evaluations/eval_evalreq_abi196_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260903_195527_248472/outputs/evaluations/eval_evalreq_abi196_wholeval_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260903_195527_248472/outputs/best_metrics.json`
- `run_20260903_195527_248472/outputs/final_metrics.json`
- `run_20260903_195527_248472/outputs/metrics.jsonl`
- `run_20260903_195527_248472/outputs/resource_profile.json`
- `run_20260903_195527_248472/outputs/model_summary.json`
- `run_20260903_195527_248472/resolved_manifest.yaml`
- `run_20260903_195527_248472/candidate/budget_request.yaml`
- `run_20260903_135523_8976a0/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260903_085513_f395ad/outputs/evaluations/eval_evalreq_abi192_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260903_085513_f395ad/outputs/evaluations/eval_evalreq_abi192_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260903_085513_f395ad/outputs/evaluations/eval_evalreq_abi192_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
