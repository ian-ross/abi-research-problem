# ABI-068 whole-validation failure-bucket review

research-figures: []

## Scope

This note records the Harness-owned Post-Run Evaluation for ABI-068:

- Candidate: `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`
- Parent Run: `run_20260828_010836_4ccc77`
- Evaluation Request: `evalreq_abi068_wholeval_failure_buckets_v1`
- Evaluation: `eval_evalreq_abi068_wholeval_failure_buckets_v1`

The diagnostic question was whether ABI-068's capped frequency-gated line U-Net focal-Tversky gains in aggregate filtered Dice, filtered recall, MIT filtered Dice, and source balance survived on the full 3,088-sample Working Validation Split, and whether the recall gain introduced unacceptable false-positive clutter, connectivity loss, or Google-source regression relative to ABI-066. This is diagnostic evidence only; promotion remains operator-reviewed.

## Whole-validation aggregate result

At the primary threshold 0.5, ABI-068 completed the whole-validation evaluation with:

| Metric | Value |
| --- | ---: |
| Sample count | 3,088 |
| Filtered Dice | 0.3951 |
| Raw Dice | 0.4084 |
| Filtered IoU | 0.2462 |
| Filtered precision | 0.3996 |
| Filtered recall | 0.3907 |
| Filtered Contrail Connectivity | 0.3868 |
| Filtered predicted-positive pixels | 693,688 |
| Filtered true-positive pixels | 277,183 |
| Filtered false-positive pixels | 416,505 |
| Filtered false-negative pixels | 432,180 |

The whole-validation result preserves ABI-068's capped representative score: full-split filtered Dice is 0.3951 versus the capped best-validation filtered Dice of 0.3964, a difference of about -0.0013. MIT filtered Dice slightly improves from the capped 0.3886 to full-split 0.3908, while Google filtered Dice falls from 0.4161 capped to 0.4032 full-split but remains strong.

ABI-068 becomes the strongest local whole-validation-tested Candidate observed so far by aggregate filtered Dice. Relative to ABI-066, it improves filtered Dice from 0.3811 to 0.3951 and recall from 0.3342 to 0.3907, but it gives back precision from 0.4434 to 0.3996 and connectivity from 0.4766 to 0.3868. It also increases filtered predicted-positive pixels from 534,634 to 693,688, so the gain is a recall-forward operating-profile shift, not a pure false-positive-control improvement.

Canonical MCAST 2.1 remains the promotion context. ABI-068 exceeds MCAST 2.1's campaign-context default-threshold filtered Dice of 0.3873 on this full Working Validation Split diagnostic, but it still has lower filtered recall than MCAST 2.1 and promotion remains a human decision rather than an autonomy-step conclusion.

## Dataset Source behavior

| Dataset Source | Filtered Dice | Filtered precision | Filtered recall | Filtered connectivity |
| --- | ---: | ---: | ---: | ---: |
| MIT | 0.3908 | 0.4191 | 0.3661 | 0.4084 |
| Google | 0.4032 | 0.3683 | 0.4455 | 0.3724 |

The model is non-collapsed on both Dataset Sources. ABI-068 improves over ABI-066 on MIT filtered Dice by about +0.0269 and remains above ABI-066's aggregate MIT catastrophic-floor concerns. Google filtered Dice remains high at 0.4032, but it is about -0.0098 below ABI-066's 0.4130. The source profile is more balanced than ABI-066 by Dice, but it trades away ABI-066's stronger Google score and connectivity.

Against canonical MCAST 2.1, ABI-068 has a mixed source profile: it exceeds MCAST 2.1 on Google filtered Dice and aggregate precision/connectivity, but remains below MCAST 2.1 on MIT filtered Dice and aggregate recall. This supports continued family development but not an autonomous promotion claim.

## Threshold behavior

The filtered threshold sweep is unusually flat near the primary threshold:

| Threshold | Filtered Dice | Precision | Recall | Predicted-positive pixels |
| ---: | ---: | ---: | ---: | ---: |
| 0.05 | 0.3947 | 0.3789 | 0.4119 | 771,215 |
| 0.30 | 0.3953 | 0.3940 | 0.3965 | 713,923 |
| 0.35 | 0.3952 | 0.3955 | 0.3950 | 708,478 |
| 0.45 | 0.3952 | 0.3982 | 0.3921 | 698,436 |
| 0.50 | 0.3951 | 0.3996 | 0.3907 | 693,688 |
| 0.60 | 0.3950 | 0.4022 | 0.3881 | 684,431 |
| 0.75 | 0.3948 | 0.4067 | 0.3836 | 669,064 |
| 0.90 | 0.3943 | 0.4137 | 0.3767 | 645,873 |

The best filtered Dice in the sweep is 0.3953 at threshold 0.20, only about +0.0002 above threshold 0.5. The precision/recall-equal filtered threshold is 0.35, with precision 0.3955 and recall 0.3950. Unlike ABI-066, ABI-068 does not show a large diagnostic gain from lowering the threshold; its full-validation result appears comparatively stable around the primary operating point.

## Failure-bucket observations

The per-sample metrics show 1,085 positive validation patches and 2,003 negative validation patches. Among positive patches, the median filtered Dice is 0.3924. There are 184/1,085 positive patches with filtered Dice below 0.1, and no exact zero-recall positive cases. This improves the low-Dice positive tail relative to ABI-066's 189 such patches while raising aggregate true-positive pixels by about 40,116.

Among negative patches, 1,219/2,003 have at least some filtered predicted-positive pixels. The negative-patch median filtered predicted-positive count is 9 pixels, the 90th percentile is 137 pixels, and the 99th percentile is 463 pixels. This is materially more negative-patch clutter than ABI-066, which had 960 negative patches with any filtered prediction and lower high-percentile false-positive counts. The clutter is still far below older broad-clutter branches such as ABI-064, but ABI-068 should be treated as a recall-forward branch rather than ABI-066's precision/connectivity-forward replacement in all respects.

Artifact Filters removed 44,358 predicted-positive pixels over the full split, equivalent to 177,432 km² using the evaluation's area convention. Filtering reduced Dice from 0.4084 raw to 0.3951 filtered and recall from 0.4167 raw to 0.3907 filtered. ABI-068 is not rescued by Artifact Filters; the filtered score remains strong despite filter removal.

## Decision

Classify ABI-068 as positive full-validation diagnostic evidence for the frequency-gated high/low spatial-feature line U-Net branch and as the current strongest local whole-validation-tested Candidate by primary filtered Dice. It should replace ABI-066 as the local aggregate-Dice reference, while ABI-066 remains the precision/connectivity-forward reference.

Do not promote ABI-068 from this note alone. The next useful hypothesis should preserve ABI-068's focal-Tversky recall and source-balanced Dice while recovering some of ABI-066's precision/connectivity and lower negative-patch clutter. A bounded in-contract continuation could target this with architecture-side false-positive suppression or confidence gating that does not move thresholding, Artifact Filters, data loading, sampling, losses, metrics, or target derivation into Candidate code.

## Artifact references

- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/final_metrics.json`
- `run_20260828_010836_4ccc77/outputs/metrics.jsonl`
- `run_20260828_010836_4ccc77/outputs/resource_profile.json`
- `run_20260828_010836_4ccc77/outputs/model_summary.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/summary.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260827_212811_0e34e2/outputs/evaluations/eval_evalreq_abi064_wholeval_failure_buckets_v1/aggregate_metrics.json`
