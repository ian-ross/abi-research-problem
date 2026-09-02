# ABI-066 whole-validation failure-bucket review

research-figures: []

## Scope

This note records the Harness-owned Post-Run Evaluation for ABI-066:

- Candidate: `abi066_fullspectral_btd_frequency_gated_line_unet_cldice_centerline_aux_v1`
- Parent Run: `run_20260827_230540_bf4ce3`
- Evaluation Request: `evalreq_abi066_wholeval_failure_buckets_v1`
- Evaluation: `eval_evalreq_abi066_wholeval_failure_buckets_v1`

The diagnostic question was whether ABI-066's capped frequency-gated line U-Net gains in filtered Dice, precision, connectivity, predicted-positive burden, and both Dataset Source filtered Dice survived on the full 3,088-sample Working Validation Split. This is diagnostic evidence only; promotion remains operator-reviewed.

## Whole-validation aggregate result

At the primary threshold 0.5, ABI-066 completed the whole-validation evaluation with:

| Metric | Value |
| --- | ---: |
| Sample count | 3,088 |
| Filtered Dice | 0.3811 |
| Raw Dice | 0.3952 |
| Filtered IoU | 0.2354 |
| Filtered precision | 0.4434 |
| Filtered recall | 0.3342 |
| Filtered Contrail Connectivity | 0.4766 |
| Filtered predicted-positive pixels | 534,634 |
| Filtered true-positive pixels | 237,067 |
| Filtered false-positive pixels | 297,567 |
| Filtered false-negative pixels | 472,296 |

The whole-validation result preserves ABI-066's capped improvement. Its full Working Validation Split filtered Dice of 0.3811 is only about -0.0014 below the capped representative best-validation score of 0.3825, so the large ABI-066 improvement was not an artifact of the representative validation cap.

ABI-066 becomes the strongest local whole-validation-tested Candidate observed so far by aggregate filtered Dice and by filtered connectivity. It improves over ABI-058's previous local reference filtered Dice of 0.3233 by about +0.0579, while raising precision from 0.3159 to 0.4434, preserving essentially the same recall, and reducing filtered false positives by about 210,919 pixels. Relative to ABI-064, it improves filtered Dice by about +0.0591 and reduces filtered false positives by about 276,384 pixels, while giving back about -0.0130 recall.

Canonical MCAST 2.1 remains slightly higher by primary filtered Dice at 0.3873, about +0.0061 over ABI-066 at threshold 0.5. ABI-066 is therefore not a promotion result, but it is now close to the canonical baseline while having a very different operating profile: much higher precision and connectivity, much lower recall, and lower predicted-positive burden.

## Dataset Source behavior

| Dataset Source | Filtered Dice | Filtered precision | Filtered recall | Filtered connectivity |
| --- | ---: | ---: | ---: | ---: |
| MIT | 0.3639 | 0.4612 | 0.3005 | 0.4631 |
| Google | 0.4130 | 0.4172 | 0.4090 | 0.4856 |

The model is non-collapsed on both Dataset Sources. The full-validation source split preserves the capped source pattern: Google is stronger than MIT, but MIT remains substantially above catastrophic floors and above the local ABI-058/ABI-064 full-validation MIT references. ABI-066 improves over ABI-058 on both sources: MIT filtered Dice rises from 0.3134 to 0.3639, and Google filtered Dice rises from 0.3397 to 0.4130.

Against canonical MCAST 2.1, ABI-066 has a mixed source profile. It exceeds MCAST 2.1 on Google filtered Dice and precision/connectivity-oriented behavior, but remains below MCAST 2.1 on MIT filtered Dice and aggregate recall. This is not promotion evidence; it identifies ABI-066 as a precision/connectivity-forward local reference whose remaining gap is mostly recall and MIT coverage.

## Threshold behavior

The filtered threshold sweep shows ABI-066 is not flat around the primary threshold; lower thresholds recover recall and improve Dice:

| Threshold | Filtered Dice | Precision | Recall | Predicted-positive pixels |
| ---: | ---: | ---: | ---: | ---: |
| 0.05 | 0.3923 | 0.3861 | 0.3988 | 732,754 |
| 0.30 | 0.3853 | 0.4276 | 0.3506 | 581,600 |
| 0.45 | 0.3823 | 0.4397 | 0.3381 | 545,434 |
| 0.50 | 0.3811 | 0.4434 | 0.3342 | 534,634 |
| 0.60 | 0.3786 | 0.4510 | 0.3261 | 512,948 |
| 0.75 | 0.3732 | 0.4648 | 0.3117 | 475,652 |
| 0.90 | 0.3560 | 0.4915 | 0.2791 | 402,753 |

The best filtered Dice in the sweep is 0.3923 at threshold 0.05, about +0.0112 above threshold 0.5 and above the canonical MCAST 2.1 default-threshold filtered Dice. The precision/recall-equal filtered threshold is also 0.05, with precision 0.3861 and recall 0.3988. This threshold sweep is diagnostic only and does not replace `val/filtered_dice` selection or establish a promotion result, but it strongly suggests ABI-066's remaining gap includes calibration/operating-point behavior rather than only representation quality.

## Failure-bucket observations

The per-sample metrics show 1,085 positive validation patches and 2,003 negative validation patches. Among positive patches, the median filtered Dice is 0.3836. There are 189/1,085 positive patches with filtered Dice below 0.1, and no exact zero-recall positive cases. This low-Dice positive tail is slightly smaller than ABI-058's 207 and ABI-064's 191, while the positive-patch median Dice is higher.

Among negative patches, 960/2,003 have at least some filtered predicted-positive pixels. The negative-patch median filtered predicted-positive count is 0 pixels, the 90th percentile is 100 pixels, and the 99th percentile is 382 pixels. This is the clearest false-positive-control improvement observed in the recent whole-validation-tested local branch: ABI-058 had 1,685 negative patches with predictions and ABI-064 had 1,801. ABI-066 does not eliminate false positives, but the frequency-gated mechanism meaningfully suppresses broad low-level negative-patch clutter while preserving true-positive count close to ABI-058.

Artifact Filters removed 32,927 predicted-positive pixels over the full split, equivalent to 131,708 km² using the evaluation's area convention. Filtering reduced Dice from 0.3952 raw to 0.3811 filtered and recall from 0.3557 raw to 0.3342 filtered. ABI-066 is not rescued by Artifact Filters; the filtered result remains strong despite the filter removing predicted-positive area.

## Decision

Classify ABI-066 as positive full-validation diagnostic evidence for the frequency-gated high/low spatial-feature line U-Net branch. ABI-066 should replace ABI-058 as the local whole-validation-tested Candidate reference for subsequent family-development comparisons. It is not a promotion result because canonical MCAST 2.1 remains slightly higher on primary filtered Dice at the default threshold and retains substantially higher recall.

The next useful hypothesis should remain within the frequency-gated branch rather than abandoning it: test whether an in-contract training-policy continuation, such as trusted `focal_tversky` on the same ABI-066 architecture or a bounded centerline-auxiliary weight adjustment, can recover recall/calibration while preserving the false-positive suppression and connectivity gains. Pure post-hoc threshold selection should not be treated as a Candidate-owned workaround; any calibration/threshold conclusion must remain Harness-owned diagnostic or operator-reviewed policy.

## Artifact references

- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/final_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/metrics.jsonl`
- `run_20260827_230540_bf4ce3/outputs/resource_profile.json`
- `run_20260827_230540_bf4ce3/outputs/model_summary.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/summary.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260827_171331_c1769a/outputs/evaluations/eval_evalreq_abi058_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_212811_0e34e2/outputs/evaluations/eval_evalreq_abi064_wholeval_failure_buckets_v1/aggregate_metrics.json`
