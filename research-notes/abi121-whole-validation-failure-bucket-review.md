# ABI-121 whole-validation failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi121_wholeval_failure_buckets_v1` for ABI-121 Run `run_20260831_041559_43da35`.

The evaluation request asked whether ABI-121's capped ASPP/detail decoder focal-Tversky gains in source balance, MIT recovery, and recall survived on the full 3,088-sample Working Validation Split, and whether the lower capped precision/connectivity looked like an acceptable recall trade-off or a full-validation false-positive/fragmentation failure mode. This is diagnostic evidence only; promotion remains operator-reviewed.

Primary comparison references:

- ABI-121 ASPP/detail decoder focal-Tversky centerline-auxiliary Run: `run_20260831_041559_43da35`
- ABI-122 directional-continuity ASPP/detail follow-up: `run_20260831_045937_fa4e34`
- ABI-068 frequency-gated line U-Net focal-Tversky reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- Canonical MCAST 2.1 summary in `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`

## Whole-validation metrics

At threshold 0.5 on the full 3,088-sample Working Validation Split, ABI-121 reached:

| Metric | ABI-121 whole validation |
| --- | ---: |
| Filtered Dice | 0.3891 |
| MIT filtered Dice | 0.3905 |
| Google filtered Dice | 0.3866 |
| Filtered precision | 0.3527 |
| Filtered recall | 0.4339 |
| Filtered contrail connectivity | 0.2337 |
| Filtered predicted-positive pixels | 872,669 |
| Filtered false-positive pixels | 564,866 |
| Filtered false-negative pixels | 401,560 |

The capped representative result was not a subset fluke in aggregate: whole-validation filtered Dice 0.3891 closely matches the capped best-validation filtered Dice 0.3884, and MIT/Google source Dice remain balanced rather than catastrophically splitting. MIT Dice improved from the capped value 0.3835 to 0.3905 on whole validation; Google moved from 0.4005 capped to 0.3866 whole validation.

Relative to canonical MCAST 2.1 full-validation context, ABI-121 is close in aggregate filtered Dice (0.3891 vs 0.3873) and has slightly higher filtered precision and connectivity, but slightly lower filtered recall. The source split is different: ABI-121 is below MCAST 2.1 on MIT filtered Dice (0.3905 vs 0.4161) and above it on Google filtered Dice (0.3866 vs 0.3437). Do not treat this as a promotion claim; it is one diagnostic result and MCAST comparison/promotion decisions remain operator-reviewed.

Relative to the stronger local whole-validation references, ABI-121 does not replace ABI-068 as the aggregate-Dice/line-quality reference. ABI-068 whole-validation filtered Dice is 0.3951 with precision 0.3996 and connectivity 0.3868; ABI-121 trades lower Dice, precision, and connectivity for higher recall. ABI-121 does exceed ABI-066 aggregate Dice and recall, but remains far below ABI-066 on precision/connectivity and below ABI-066 on Google Dice.

## Threshold behavior

The threshold sweep did not reveal a hidden calibration fix. Filtered Dice increased only from 0.3891 at threshold 0.5 to 0.3923 at threshold 0.95. At that best filtered-Dice threshold, precision rose to 0.3799 while recall fell to 0.4055. Raw Dice similarly peaked at threshold 0.95 with 0.4052.

This means ABI-121's main issue is not simply the fixed threshold. Candidate code still must not implement thresholding or postprocessing, and the useful design lesson is architectural/calibration pressure toward fewer low-confidence false positives while preserving the focal-Tversky recall branch.

## Failure-bucket observations

The full-validation per-sample metrics show three overlapping failure modes:

1. Negative-patch clutter is widespread. Among 2,003 negative validation patches, 1,715 had at least one filtered predicted-positive pixel. The median negative-patch false-positive count was 51 pixels; 603 negative patches exceeded 100 filtered false-positive pixels, 34 exceeded 500, and 5 exceeded 1,000.
2. Positive patches often have false positives exceeding true positives. Across 1,085 positive patches, 726 had filtered false-positive pixels greater than filtered true-positive pixels. Median positive-patch Dice was 0.4034, with 153 positive patches below 0.1 Dice and 199 below 0.2 recall.
3. Source behavior is balanced in aggregate but not clean. Positive-patch median filtered Dice was 0.4194 on Google and 0.3878 on MIT. Google retained stronger recall, while MIT carried more total false-positive pixels. The aggregate source balance therefore comes from different error mixes rather than uniformly clean segmentation.

Artifact Filters removed 56,069 pixels over 952 samples and no scanline hits were recorded. Raw Dice was 0.4012 versus filtered Dice 0.3891; the filter removed some true positives as well as false positives. This is not an Artifact Filter-dependence result. The dominant concern is ABI-121's intrinsic positive-area discipline and low connectivity before and after filtering.

The evaluation retained 12 diagnostic sample pairs under `diagnostic_samples/`; nine were selected because Artifact Filters hit the sample and three because no filter hit. This note intentionally does not reproduce individual scene identifiers, coordinates, or images.

## Interpretation

Classify ABI-121's whole-validation result as valid and non-collapsed diagnostic support for the ASPP/detail focal-Tversky branch, not as a promotion-ready replacement for the current local references. The capped aggregate signal survived on the full Working Validation Split, so ABI-121 remains the best observed non-frequency-gated ASPP/detail result and a credible recall/source-balance comparator.

However, the failure-bucket review confirms the capped concern: ABI-121's focal-Tversky recall comes with substantial low-confidence clutter and weak line connectivity. The problem is not severe Artifact Filter dependence or a single threshold-calibration miss. It is a precision/connectivity trade-off that must be addressed inside the in-contract model architecture or allowlisted training choices, without candidate-owned losses, sampling, metrics, thresholding, postprocessing, or Artifact Filters.

ABI-122 already tested one additive directional-continuity refinement and regressed, so do not keep stacking post-decoder line-context residuals on ABI-121 unchanged.

## Decision

Do not promote ABI-121. Retain ABI-068 as the local whole-validation aggregate-Dice and connectivity reference, ABI-066 as the precision/connectivity reference, and ABI-121 as the non-frequency-gated ASPP/detail recall/source-balance reference.

A useful next hypothesis should broaden away from ABI-121-style post-decoder continuity additions. Prefer an in-contract architecture that targets false-positive calibration and line evidence earlier in the feature hierarchy, or a different preprocessing/front-end/data-policy frontier that can reduce negative-patch clutter without sacrificing MIT/Google balance. Do not request another ABI-121 whole-validation diagnostic unchanged.

## Artifact references

- `run_20260831_041559_43da35/outputs/evaluations/eval_evalreq_abi121_wholeval_failure_buckets_v1/summary.json`
- `run_20260831_041559_43da35/outputs/evaluations/eval_evalreq_abi121_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_041559_43da35/outputs/evaluations/eval_evalreq_abi121_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260831_041559_43da35/outputs/evaluations/eval_evalreq_abi121_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260831_041559_43da35/outputs/evaluations/eval_evalreq_abi121_wholeval_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260831_041559_43da35/outputs/best_metrics.json`
- `run_20260831_045937_fa4e34/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
