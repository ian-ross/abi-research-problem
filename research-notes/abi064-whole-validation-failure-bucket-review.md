# ABI-064 whole-validation failure-bucket review

research-figures: []

## Scope

This note records the Harness-owned Post-Run Evaluation for ABI-064:

- Candidate: `abi064_fullspectral_btd_coarse_to_fine_unet_cldice_centerline_aux_v1`
- Parent Run: `run_20260827_212811_0e34e2`
- Evaluation Request: `evalreq_abi064_wholeval_failure_buckets_v1`
- Evaluation: `eval_evalreq_abi064_wholeval_failure_buckets_v1`

The diagnostic question was whether ABI-064's capped best-validation source balance and small filtered-Dice lead over ABI-058 persist on the full 3,088-sample Working Validation Split, and whether its coarse-to-fine soft prior actually improves false-positive control. This is diagnostic evidence only; promotion remains operator-reviewed.

## Whole-validation aggregate result

At the primary threshold 0.5, ABI-064 completed the whole-validation evaluation with:

| Metric | Value |
| --- | ---: |
| Sample count | 3,088 |
| Filtered Dice | 0.3220 |
| Raw Dice | 0.3320 |
| Filtered IoU | 0.1919 |
| Filtered precision | 0.3003 |
| Filtered recall | 0.3472 |
| Filtered Contrail Connectivity | 0.1915 |
| Filtered predicted-positive pixels | 820,229 |
| Filtered true-positive pixels | 246,278 |
| Filtered false-positive pixels | 573,951 |
| Filtered false-negative pixels | 463,085 |

The whole-validation result does not preserve ABI-064's small capped lead over ABI-058. ABI-064's full-validation filtered Dice is 0.3220, about 0.0013 below ABI-058's 0.3233 and 0.0022 above ABI-056's 0.3198. It gains true positives and recall relative to both ABI-056 and ABI-058, but pays for that with the largest filtered false-positive burden among the three whole-validation-tested local references.

Canonical MCAST 2.1 remains substantially higher at filtered Dice 0.3873, so ABI-064 is not promotion-ready by aggregate overlap.

## Dataset Source behavior

| Dataset Source | Filtered Dice | Filtered precision | Filtered recall | Filtered connectivity |
| --- | ---: | ---: | ---: | ---: |
| MIT | 0.3226 | 0.3341 | 0.3120 | 0.2229 |
| Google | 0.3210 | 0.2578 | 0.4253 | 0.1706 |

ABI-064 is non-collapsed on both Dataset Sources and is more source-balanced by filtered Dice than ABI-058. The improvement is concentrated on MIT, where ABI-064 exceeds ABI-058's whole-validation MIT filtered Dice of 0.3134. The cost is a clear Google regression from ABI-058's 0.3397 to 0.3210, with weak Google precision despite high recall. This shifts the coarse-to-fine branch toward a MIT-balanced, recall-heavy profile rather than a uniformly better reference.

## Threshold behavior

The filtered threshold sweep is very flat near the operating point:

| Threshold | Filtered Dice | Precision | Recall |
| ---: | ---: | ---: | ---: |
| 0.30 | 0.3206 | 0.2852 | 0.3661 |
| 0.45 | 0.3218 | 0.2967 | 0.3516 |
| 0.50 | 0.3220 | 0.3003 | 0.3472 |
| 0.60 | 0.3222 | 0.3076 | 0.3381 |
| 0.75 | 0.3217 | 0.3211 | 0.3223 |
| 0.90 | 0.3155 | 0.3477 | 0.2887 |

The best filtered Dice in the sweep is 0.3222 at threshold 0.60, only +0.00016 above threshold 0.5. The precision/recall-equal threshold is 0.75 with filtered Dice 0.3217. Threshold adjustment alone is therefore not a meaningful path to close the MCAST gap or to recover ABI-058's aggregate lead.

## Failure-bucket observations

The per-sample metrics show 1,085 positive validation patches and 2,003 negative validation patches. Among positive patches, the median filtered Dice is 0.3393, and 191/1,085 positive patches have filtered Dice below 0.1. Exact zero-recall positive cases were not present. This low-Dice positive tail is slightly smaller than ABI-058's 207 low-Dice positives and close to ABI-056's 190.

Among negative patches, 1,801/2,003 have at least some filtered predicted-positive pixels. The negative-patch median filtered predicted-positive count is 69 pixels and the 90th percentile is 256 pixels. The positive-patch median filtered predicted-positive count is 337 pixels. This confirms that the coarse soft-prior branch did not solve the broad low-level false-positive problem; it increased recall and true-positive pixels while allowing many small false positives on negative patches.

Artifact Filters removed 48,399 predicted-positive pixels over the full split, equivalent to 193,596 km² using the evaluation's area convention. Filtering reduced Dice from 0.3320 raw to 0.3220 filtered and recall from 0.3692 raw to 0.3472 filtered. ABI-064 is not rescued by Artifact Filters, and the filter removal burden is higher than the comparable whole-validation evaluations for ABI-056 and ABI-058.

## Decision

ABI-064 remains a strong capped-run reference and a useful coarse-to-fine family scout, but it should not replace ABI-058 as the local whole-validation-tested reference by aggregate filtered Dice. Its value is diagnostic: the low-resolution coarse prior improves MIT balance and aggregate recall, but does not deliver the intended false-positive-control improvement and weakens Google aggregate performance and connectivity.

Classify the whole-validation outcome as `bad_research_result` / mixed capped-to-full diagnostic evidence for this exact ABI-064 branch, not as an execution or contract failure. Do not promote ABI-064 against canonical MCAST 2.1, and do not pursue pure threshold tuning for this branch.

After the negative ABI-065 focal-Tversky follow-up and this full-validation diagnostic, further work should broaden away from simple loss substitution or incremental coarse-prior tuning. A useful next hypothesis should target false-positive suppression and thin-line connectivity more directly, or scout a materially different architecture family, while keeping provider-owned inputs, losses, targets, sampling, augmentation, metrics, and Artifact Filters unchanged.

## Artifact references

- `run_20260827_212811_0e34e2/outputs/best_metrics.json`
- `run_20260827_212811_0e34e2/outputs/final_metrics.json`
- `run_20260827_212811_0e34e2/outputs/metrics.jsonl`
- `run_20260827_212811_0e34e2/outputs/resource_profile.json`
- `run_20260827_212811_0e34e2/outputs/model_summary.json`
- `run_20260827_212811_0e34e2/outputs/evaluations/eval_evalreq_abi064_wholeval_failure_buckets_v1/summary.json`
- `run_20260827_212811_0e34e2/outputs/evaluations/eval_evalreq_abi064_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_212811_0e34e2/outputs/evaluations/eval_evalreq_abi064_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260827_212811_0e34e2/outputs/evaluations/eval_evalreq_abi064_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260827_212811_0e34e2/outputs/evaluations/eval_evalreq_abi064_wholeval_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260827_171331_c1769a/outputs/evaluations/eval_evalreq_abi058_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_153716_1ac9d4/outputs/evaluations/eval_evalreq_abi056_wholeval_failure_buckets_v1/aggregate_metrics.json`
