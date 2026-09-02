# ABI-126 whole-validation failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi126_wholeval_failure_buckets_v1` for ABI-126 Run `run_20260831_085615_d05ab3`.

The evaluation request asked whether ABI-126's capped ASPP/detail decoder BCE-Dice gains in Google filtered Dice, filtered precision, connectivity, and positive-area discipline survive on the full 3,088-sample Working Validation Split, and whether its lower MIT recall is a manageable calibration trade-off or a full-validation under-segmentation failure mode. This is diagnostic evidence only; promotion remains operator-reviewed.

Primary comparison references:

- ABI-126 ASPP/detail decoder BCE-Dice Centerline-auxiliary Run: `run_20260831_085615_d05ab3`
- ABI-121 ASPP/detail decoder focal-Tversky Centerline-auxiliary whole-validation comparator: `run_20260831_041559_43da35`, Evaluation `eval_evalreq_abi121_wholeval_failure_buckets_v1`
- ABI-068 frequency-gated line U-Net focal-Tversky whole-validation aggregate-Dice reference: `run_20260828_010836_4ccc77`, Evaluation `eval_evalreq_abi068_wholeval_failure_buckets_v1`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice whole-validation precision/connectivity reference: `run_20260827_230540_bf4ce3`, Evaluation `eval_evalreq_abi066_wholeval_failure_buckets_v1`
- ABI-127 ASPP/detail decoder BCE-Dice Line+Centerline auxiliary capped follow-up: `run_20260831_094013_5ba974`

## Whole-validation metrics

At threshold 0.5 on the full 3,088-sample Working Validation Split, ABI-126 reached:

| Metric | ABI-126 whole validation |
| --- | ---: |
| Filtered Dice | 0.3892 |
| MIT filtered Dice | 0.3662 |
| Google filtered Dice | 0.4319 |
| Filtered precision | 0.4770 |
| Filtered recall | 0.3288 |
| Filtered contrail connectivity | 0.4563 |
| Filtered predicted-positive pixels | 489,005 |
| Filtered false-positive pixels | 255,773 |
| Filtered false-negative pixels | 476,131 |

The capped representative signal mostly survived in aggregate and in kind. Whole-validation filtered Dice 0.3892 is slightly above the capped best-validation filtered Dice 0.3859, and whole-validation Google filtered Dice 0.4319 remains high relative to the local comparison set. The source trade-off also survived: MIT filtered Dice stayed lower at 0.3662, with MIT filtered recall only 0.2913.

Relative to ABI-121 whole validation, ABI-126 is effectively tied in aggregate filtered Dice (0.3892 vs 0.3891) but with a different operating point: much higher precision (0.4770 vs 0.3527), higher connectivity (0.4563 vs 0.2337), fewer filtered predicted-positive pixels (489,005 vs 872,669), and higher Google Dice (0.4319 vs 0.3866), but lower recall (0.3288 vs 0.4339) and lower MIT Dice (0.3662 vs 0.3905).

Relative to ABI-068 whole validation, ABI-126 does not replace the aggregate reference: filtered Dice is lower (0.3892 vs 0.3951) and MIT Dice is lower (0.3662 vs 0.3908). ABI-126 does, however, have higher precision (0.4770 vs 0.3996), higher connectivity (0.4563 vs 0.3868), higher Google Dice (0.4319 vs 0.4032), and fewer false-positive pixels.

Relative to ABI-066 whole validation, ABI-126 has higher aggregate filtered Dice (0.3892 vs 0.3811), higher Google Dice (0.4319 vs 0.4130), higher precision (0.4770 vs 0.4434), slightly higher MIT filtered Dice (0.3662 vs 0.3639), and slightly lower false-positive count. ABI-066 remains slightly stronger on connectivity (0.4766 vs 0.4563) and recall (0.3342 vs 0.3288).

## Threshold behavior

The threshold sweep shows ABI-126 is materially threshold-sensitive. Filtered Dice improves from 0.3892 at the fixed 0.5 threshold to 0.4079 at threshold 0.05; raw Dice improves from 0.4042 at threshold 0.5 to 0.4214 at threshold 0.05. At the best filtered-Dice threshold, filtered precision is 0.3970 and filtered recall is 0.4195, a much more balanced operating point than threshold 0.5.

This does not authorize candidate-owned thresholding, calibration, postprocessing, or Artifact Filters. The useful design lesson is that ABI-126's full-validation under-segmentation is not only architectural capacity: its logits are conservative enough that a lower diagnostic threshold recovers recall and aggregate Dice. Future in-contract work should target calibration through architecture or allowlisted training choices rather than external threshold changes.

## Failure-bucket observations

The full-validation per-sample metrics show ABI-126 reduced clutter relative to ABI-121 but did not eliminate missed-positive behavior:

1. Negative-patch clutter is much lower than ABI-121 but still present. Among 2,003 negative validation patches, 986 had at least one filtered predicted-positive pixel. The median negative-patch false-positive count was 0 pixels; 162 negative patches exceeded 100 filtered false-positive pixels, 7 exceeded 500, and 1 exceeded 1,000.
2. Positive patches often remain under-segmented. Across 1,085 positive validation patches, 513 had filtered false-positive pixels greater than filtered true-positive pixels, 202 were below 0.1 filtered Dice, 282 were below 0.2 filtered Dice, and 313 were below 0.2 filtered recall. Median positive-patch filtered recall was 0.3596, while median positive-patch filtered precision was 0.5182.
3. The Dataset Source split explains the main trade-off. Positive-patch median filtered Dice was 0.3563 on MIT and 0.4252 on Google. MIT also had lower positive-patch median recall (0.3261) than Google (0.3977). ABI-126's high whole-validation precision/connectivity therefore comes with a real MIT under-recall weakness, not just an aggregate-count artifact.

Artifact Filters removed 30,827 pixels over 667 samples, with aggregate raw Dice 0.4042 versus filtered Dice 0.3892. The raw-to-filtered difference is modest and does not indicate a primary Artifact Filter-dependence result. The retained diagnostic sample pairs are useful traceability artifacts, but this note intentionally does not reproduce individual scene identifiers, coordinates, or images.

## Interpretation

Classify ABI-126's whole-validation evaluation as valid, non-collapsed diagnostic support for an ASPP/detail precision/connectivity branch. The full-validation result confirms the capped observation that BCE-Dice made the ASPP/detail decoder substantially cleaner than the focal-Tversky ABI-121 operating point while preserving similar aggregate Dice and improving Google performance.

The main weakness is not general failure or Artifact Filter dependence. It is a conservative calibration/source-transfer trade-off: ABI-126 suppresses false positives and improves line connectivity, but misses too many MIT positives at threshold 0.5. The diagnostic threshold sweep shows that much of the lost recall is recoverable at lower thresholds, but threshold selection is Harness/provider evaluation behavior rather than candidate-owned code.

ABI-127 already tested a simple Line+Centerline auxiliary addition on top of ABI-126 and produced an unfavorable capped trade-off. Therefore, do not spend the next step on another simple ASPP/detail auxiliary-head addition unless a new diagnostic specifically implicates auxiliary target choice.

## Decision

Do not promote ABI-126, and do not reinterpret capped or diagnostic threshold-sweep evidence as deployment evidence. Retain ABI-068 as the local whole-validation aggregate-Dice reference, ABI-066 as the mature precision/connectivity reference, ABI-121 as the ASPP/detail recall/source-balance comparator, and ABI-126 as the ASPP/detail precision/connectivity and Google-Dice comparator.

For the next in-contract hypothesis, broaden away from simple ASPP/detail loss swaps and auxiliary-head stacking. A useful direction is a calibration-aware architecture or allowlisted training-policy variant that preserves ABI-126-like positive-area discipline and connectivity while raising MIT recall at the fixed Harness threshold.

## Artifact references

- `run_20260831_085615_d05ab3/outputs/evaluations/eval_evalreq_abi126_wholeval_failure_buckets_v1/summary.json`
- `run_20260831_085615_d05ab3/outputs/evaluations/eval_evalreq_abi126_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_085615_d05ab3/outputs/evaluations/eval_evalreq_abi126_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260831_085615_d05ab3/outputs/evaluations/eval_evalreq_abi126_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260831_085615_d05ab3/outputs/evaluations/eval_evalreq_abi126_wholeval_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260831_041559_43da35/outputs/evaluations/eval_evalreq_abi121_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_094013_5ba974/outputs/best_metrics.json`
