# ABI-056 whole-validation failure-bucket review

research-figures: []

## Scope

This note records the Harness-owned Post-Run Evaluation for ABI-056:

- Candidate: `abi056_fullspectral_btd_hrline_unet_multiscale_skip_fusion_cldice_centerline_aux_v1`
- Parent Run: `run_20260827_153716_1ac9d4`
- Evaluation Request: `evalreq_abi056_wholeval_failure_buckets_v1`
- Evaluation: `eval_evalreq_abi056_wholeval_failure_buckets_v1`

The diagnostic question was whether ABI-056's capped high-resolution BTD line U-Net multi-scale skip-fusion advantage persists on the full 3,088-sample Working Validation Split, and which trusted failure buckets explain the remaining gap. This note treats the result as diagnostic evidence only; promotion remains operator-reviewed.

## Whole-validation aggregate result

At the primary threshold 0.5, ABI-056 completed the whole-validation evaluation with:

| Metric | Value |
| --- | ---: |
| Sample count | 3,088 |
| Filtered Dice | 0.3198 |
| Raw Dice | 0.3306 |
| Filtered IoU | 0.1903 |
| Filtered precision | 0.3310 |
| Filtered recall | 0.3094 |
| Filtered Contrail Connectivity | 0.2258 |
| Filtered predicted-positive pixels | 663,027 |
| Filtered true-positive pixels | 219,460 |
| Filtered false-positive pixels | 443,567 |
| Filtered false-negative pixels | 489,903 |

This is very close to the capped representative validation evidence from the parent Run: best filtered Dice 0.3225 at epoch 11 and final filtered Dice 0.3221 at epoch 12. The capped ABI-056 advantage over ABI-053 was only about +0.0003 filtered Dice, so this whole-validation result supports ABI-056 stability but does not provide strong evidence for a meaningful architectural improvement over ABI-053.

Canonical MCAST 2.1 remains higher on full Working Validation Split filtered Dice: 0.3873 versus ABI-056's 0.3198. ABI-056 has higher filtered Contrail Connectivity than MCAST 2.1 in the campaign context (0.2258 versus 0.1925), but still much lower connectivity than MCAST 1.1 (0.5421). The main full-validation gap versus the best filtered-Dice baseline is therefore aggregate overlap and recall/precision balance rather than a pure threshold artifact.

## Dataset Source behavior

| Dataset Source | Filtered Dice | Filtered precision | Filtered recall | Filtered connectivity |
| --- | ---: | ---: | ---: | ---: |
| MIT | 0.3092 | 0.3568 | 0.2729 | 0.2575 |
| Google | 0.3377 | 0.2976 | 0.3904 | 0.2048 |

The model remains non-collapsed on both Dataset Sources. The source pattern is asymmetric: MIT has better precision and connectivity but weaker recall, while Google has better Dice and recall but weaker precision. This does not indicate a catastrophic single-source failure, but it does suggest that the high-resolution line U-Net branch is still making many background positives while also missing substantial positive area.

## Threshold behavior

The filtered threshold sweep is nearly flat around the operating point:

| Threshold | Filtered Dice | Precision | Recall |
| ---: | ---: | ---: | ---: |
| 0.20 | 0.3201 | 0.3061 | 0.3354 |
| 0.30 | 0.3203 | 0.3158 | 0.3249 |
| 0.35 | 0.3202 | 0.3198 | 0.3206 |
| 0.50 | 0.3198 | 0.3310 | 0.3094 |
| 0.80 | 0.3157 | 0.3577 | 0.2826 |

The best filtered Dice in the sweep is 0.3203 at threshold 0.30, only +0.00045 above threshold 0.5. Lowering the threshold trades precision for recall but does not materially improve Dice. Threshold/calibration adjustment alone is therefore unlikely to close the gap.

## Failure-bucket observations

The per-sample metrics show 1,085 positive validation patches and 2,003 negative validation patches. Among positive patches, the median filtered Dice is 0.3324 and 190/1,085 positive patches have filtered Dice below 0.1. Exact zero-recall positive cases were not present, but the low tail is substantial. Among negative patches, 1,695/2,003 have at least some filtered predicted-positive pixels, indicating broad low-level false-positive tendency.

Artifact Filters removed 37,391 predicted-positive pixels over the full split, equivalent to 149,564 km² using the evaluation's area convention. Filtering reduced Dice from 0.3306 raw to 0.3198 filtered and recall from 0.3285 raw to 0.3094 filtered. The model is not rescued by Artifact Filters; if anything, filtered scoring exposes the remaining overlap and recall problem. The bounded diagnostic samples include 12 prediction GeoTIFF pairs, with 9 selected for filter hits and 3 for no-filter-hit controls.

## Decision

ABI-056 should remain the current local capped best in the high-resolution BTD line U-Net family, but the full-validation evaluation makes the margin look scientifically small. The multi-scale skip-fusion branch is stable and non-degenerate, not promotion-ready.

Do not spend a later step on pure threshold tuning for this branch under the current evidence. A useful next hypothesis should broaden the connectivity/false-positive mechanism rather than repeating centerline weight, directional refiner, or the same skip-fusion change. Candidate directions include an architecture that separates thin-line proposal from mask refinement, a topology-preserving decoder with explicit high-resolution edge/centerline fusion, or a different family that can reduce negative-patch false positives without suppressing source-balanced recall.

## Artifact references

- `run_20260827_153716_1ac9d4/outputs/best_metrics.json`
- `run_20260827_153716_1ac9d4/outputs/final_metrics.json`
- `run_20260827_153716_1ac9d4/outputs/evaluations/eval_evalreq_abi056_wholeval_failure_buckets_v1/summary.json`
- `run_20260827_153716_1ac9d4/outputs/evaluations/eval_evalreq_abi056_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_153716_1ac9d4/outputs/evaluations/eval_evalreq_abi056_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260827_153716_1ac9d4/outputs/evaluations/eval_evalreq_abi056_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260827_153716_1ac9d4/outputs/evaluations/eval_evalreq_abi056_wholeval_failure_buckets_v1/diagnostic_samples/samples.json`
