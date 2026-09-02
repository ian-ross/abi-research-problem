# ABI-058 whole-validation failure-bucket review

research-figures: []

## Scope

This note records the Harness-owned Post-Run Evaluation for ABI-058:

- Candidate: `abi058_fullspectral_btd_hrline_unet_oriented_context_cldice_centerline_aux_v1`
- Parent Run: `run_20260827_171331_c1769a`
- Evaluation Request: `evalreq_abi058_wholeval_failure_buckets_v1`
- Evaluation: `eval_evalreq_abi058_wholeval_failure_buckets_v1`

The diagnostic question was whether ABI-058's small capped oriented-context improvement over ABI-056 and ABI-053 persists on the full 3,088-sample Working Validation Split, and which trusted failure buckets explain its remaining gap. This note treats the result as diagnostic evidence only; promotion remains operator-reviewed.

## Whole-validation aggregate result

At the primary threshold 0.5, ABI-058 completed the whole-validation evaluation with:

| Metric | Value |
| --- | ---: |
| Sample count | 3,088 |
| Filtered Dice | 0.3233 |
| Raw Dice | 0.3332 |
| Filtered IoU | 0.1928 |
| Filtered precision | 0.3159 |
| Filtered recall | 0.3310 |
| Filtered Contrail Connectivity | 0.2262 |
| Filtered predicted-positive pixels | 743,287 |
| Filtered true-positive pixels | 234,801 |
| Filtered false-positive pixels | 508,486 |
| Filtered false-negative pixels | 474,562 |

This preserves a small whole-validation advantage over ABI-056's whole-validation filtered Dice of 0.3198, but the margin is only about +0.0035 Dice. The full-validation score is also close to ABI-058's capped best-validation score of 0.3248, so the oriented-context improvement was not merely a capped-subset artifact. Canonical MCAST 2.1 remains substantially higher at filtered Dice 0.3873, so ABI-058 is not promotion-ready by aggregate overlap.

Relative to ABI-056, ABI-058 improves recall from 0.3094 to 0.3310 and increases true-positive pixels from 219,460 to 234,801. The cost is lower precision, from 0.3310 to 0.3159, and a larger false-positive burden, from 443,567 to 508,486 filtered false-positive pixels. Connectivity is effectively unchanged versus ABI-056: 0.2262 versus 0.2258.

## Dataset Source behavior

| Dataset Source | Filtered Dice | Filtered precision | Filtered recall | Filtered connectivity |
| --- | ---: | ---: | ---: | ---: |
| MIT | 0.3134 | 0.3404 | 0.2903 | 0.2578 |
| Google | 0.3397 | 0.2846 | 0.4212 | 0.2053 |

The model remains non-collapsed on both Dataset Sources. The source pattern is similar to ABI-056 but slightly more recall-oriented: MIT keeps higher precision and connectivity but lower recall, while Google has higher Dice and recall but weak precision. This is not a catastrophic single-source failure; it is a source-asymmetric precision/recall trade-off that still leaves many false positives and missed positives.

## Threshold behavior

The filtered threshold sweep is nearly flat around the operating point:

| Threshold | Filtered Dice | Precision | Recall |
| ---: | ---: | ---: | ---: |
| 0.20 | 0.3223 | 0.2894 | 0.3635 |
| 0.30 | 0.3230 | 0.2995 | 0.3505 |
| 0.35 | 0.3232 | 0.3038 | 0.3452 |
| 0.45 | 0.3234 | 0.3120 | 0.3357 |
| 0.50 | 0.3233 | 0.3159 | 0.3310 |
| 0.80 | 0.3185 | 0.3447 | 0.2961 |

The best filtered Dice in the sweep is 0.3234 at threshold 0.45, only +0.00012 above threshold 0.5. Threshold/calibration adjustment alone is therefore unlikely to produce a meaningful improvement.

## Failure-bucket observations

The per-sample metrics show 1,085 positive validation patches and 2,003 negative validation patches. Among positive patches, the median filtered Dice is 0.3330, and 207/1,085 positive patches have filtered Dice below 0.1. Exact zero-recall positive cases were not present, but the low-Dice positive tail is slightly larger than ABI-056's 190 low-Dice positives.

Among negative patches, 1,685/2,003 have at least some filtered predicted-positive pixels. The negative-patch median filtered predicted-positive count is 52 pixels, while the positive-patch median is 307 pixels. This confirms a broad low-level false-positive tendency rather than collapse to all-positive masks.

Artifact Filters removed 43,710 predicted-positive pixels over the full split, equivalent to 174,840 km² using the evaluation's area convention. Filtering reduced Dice from 0.3332 raw to 0.3233 filtered and recall from 0.3514 raw to 0.3310 filtered. ABI-058 is not rescued by Artifact Filters; filtered scoring exposes the same overlap and false-positive problem while removing some true-positive-adjacent structure.

## Decision

ABI-058 should replace ABI-056 as the local whole-validation-tested reference within the high-resolution BTD line U-Net branch by primary filtered Dice, but only narrowly. The oriented-context branch is stable enough to count as a real family-development gain, yet the gain comes mostly from recall and extra predicted-positive area rather than a connectivity breakthrough or false-positive reduction.

Do not promote ABI-058 against canonical MCAST 2.1. Do not spend a later step on pure threshold tuning for this branch. A useful next hypothesis should broaden the mechanism away from incremental full-resolution decoder refinements: either a different architecture family with stronger negative-patch false-positive control, or a topology/connectivity approach that improves thin-line continuity without increasing broad predicted-positive area. If remaining within this family, the next change should explicitly target false-positive suppression rather than adding another context/refinement branch.

## Artifact references

- `run_20260827_171331_c1769a/outputs/best_metrics.json`
- `run_20260827_171331_c1769a/outputs/final_metrics.json`
- `run_20260827_171331_c1769a/outputs/evaluations/eval_evalreq_abi058_wholeval_failure_buckets_v1/summary.json`
- `run_20260827_171331_c1769a/outputs/evaluations/eval_evalreq_abi058_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_171331_c1769a/outputs/evaluations/eval_evalreq_abi058_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260827_171331_c1769a/outputs/evaluations/eval_evalreq_abi058_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260827_171331_c1769a/outputs/evaluations/eval_evalreq_abi058_wholeval_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260827_153716_1ac9d4/outputs/evaluations/eval_evalreq_abi056_wholeval_failure_buckets_v1/aggregate_metrics.json`
