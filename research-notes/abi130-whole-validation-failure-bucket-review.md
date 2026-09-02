# ABI-130 whole-validation failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi130_wholeval_failure_buckets_v1` for ABI-130 Run `run_20260831_121006_7d24be`.

The evaluation request asked whether ABI-130's capped ASPP/detail decoder BTD+SZA BCE-Dice gains in aggregate filtered Dice, MIT recall, source balance, and Google filtered Dice survived on the full 3,088-sample Working Validation Split, and whether the added Solar Geometry Input produced acceptable calibration or introduced clutter/connectivity degradation relative to ABI-126, ABI-121, ABI-068, and ABI-066. This is diagnostic evidence only; promotion remains operator-reviewed.

Primary comparison references:

- ABI-130 ASPP/detail decoder BTD+SZA BCE-Dice Centerline-auxiliary Run: `run_20260831_121006_7d24be`, Evaluation `eval_evalreq_abi130_wholeval_failure_buckets_v1`
- ABI-126 ASPP/detail decoder BCE-Dice Centerline-auxiliary whole-validation comparator: `run_20260831_085615_d05ab3`, Evaluation `eval_evalreq_abi126_wholeval_failure_buckets_v1`
- ABI-121 ASPP/detail decoder focal-Tversky Centerline-auxiliary whole-validation recall/source-balance comparator: `run_20260831_041559_43da35`, Evaluation `eval_evalreq_abi121_wholeval_failure_buckets_v1`
- ABI-068 frequency-gated line U-Net focal-Tversky whole-validation aggregate-Dice reference: `run_20260828_010836_4ccc77`, Evaluation `eval_evalreq_abi068_wholeval_failure_buckets_v1`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice whole-validation precision/connectivity reference: `run_20260827_230540_bf4ce3`, Evaluation `eval_evalreq_abi066_wholeval_failure_buckets_v1`
- Canonical MCAST 1.1 and MCAST 2.1 summary metrics from `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`

## Whole-validation metrics

At threshold 0.5 on the full 3,088-sample Working Validation Split, ABI-130 reached:

| Metric | ABI-130 whole validation |
| --- | ---: |
| Filtered Dice | 0.3954 |
| MIT filtered Dice | 0.3797 |
| Google filtered Dice | 0.4256 |
| Filtered precision | 0.4436 |
| Filtered recall | 0.3566 |
| Filtered contrail connectivity | 0.3935 |
| Filtered predicted-positive pixels | 570,306 |
| Filtered false-positive pixels | 317,319 |
| Filtered false-negative pixels | 456,376 |

The capped SZA-calibration signal mostly survived. Whole-validation filtered Dice was 0.3954, essentially unchanged from ABI-130's capped best-validation filtered Dice 0.3953. Source-stratified behavior also stayed close in kind: MIT filtered Dice was 0.3797 versus 0.3779 capped, and Google filtered Dice was 0.4256 versus 0.4404 capped. The full split therefore did not turn ABI-130 into a cap-only artifact, though it did soften the capped Google advantage.

Relative to ABI-126 whole validation, ABI-130 improved aggregate filtered Dice (0.3954 vs 0.3892), MIT filtered Dice (0.3797 vs 0.3662), and recall (0.3566 vs 0.3288). It also reduced positive-patch complete misses from 48 to 37. This confirms the intended SZA effect: the ASPP/detail BCE-Dice branch became less under-segmenting, especially on MIT.

The improvement cost is also confirmed. Compared with ABI-126, ABI-130 lowered precision (0.4436 vs 0.4770) and connectivity (0.3935 vs 0.4563), increased filtered predicted-positive pixels (570,306 vs 489,005), increased negative-patch clutter from 986 to 1,187 nonempty negative patches, and increased negative-patch false-positive pixels from 59,769 to 77,746. ABI-130 recovered 19,755 positive false-negative pixels relative to ABI-126 but added 43,569 positive false-positive pixels and 17,977 negative-patch false-positive pixels. The SZA feature is therefore a real recall/calibration lever, not a free aggregate improvement.

Relative to ABI-068 whole validation, ABI-130 is an aggregate near-tie: filtered Dice 0.3954 versus 0.3951. It improves Google filtered Dice (0.4256 vs 0.4032), precision (0.4436 vs 0.3996), connectivity (0.3935 vs 0.3868), and positive-area discipline, but trails MIT filtered Dice (0.3797 vs 0.3908) and recall (0.3566 vs 0.3907). ABI-068 remains the more MIT-recall-balanced local aggregate reference, while ABI-130 is the stronger Google/precision ASPP-detail alternative.

Relative to ABI-066 whole validation, ABI-130 improves aggregate filtered Dice (0.3954 vs 0.3811), MIT filtered Dice (0.3797 vs 0.3639), Google filtered Dice (0.4256 vs 0.4130), and recall (0.3566 vs 0.3342), with nearly tied precision. ABI-066 remains clearly stronger on connectivity (0.4766 vs 0.3935). Relative to ABI-121, ABI-130 improves aggregate Dice, Google Dice, precision, connectivity, and false-positive discipline, but remains lower on MIT Dice and recall.

Against the canonical full-validation MCAST summaries, ABI-130's filtered Dice 0.3954 is above MCAST 1.1 (0.3842) and MCAST 2.1 (0.3873) in this shared evaluation context. Its precision/recall position is intermediate: it is below MCAST 1.1 precision but above MCAST 2.1 precision, and above MCAST 1.1 recall but below MCAST 2.1 recall. Its connectivity is below MCAST 1.1 and above MCAST 2.1. This is useful diagnostic context only; it is not a promotion claim.

## Threshold behavior

The ABI-130 diagnostic threshold sweep shows modest but actionable threshold sensitivity. Filtered Dice improves from 0.3954 at the fixed 0.5 threshold to 0.4041 at threshold 0.15. The precision/recall-equal filtered operating point is threshold 0.20, with precision 0.4021 and recall 0.4050. Raw Dice similarly improves from 0.4100 at threshold 0.5 to 0.4175 at threshold 0.15.

This does not authorize candidate-owned thresholding, calibration, postprocessing, or Artifact Filters. The design lesson is that ABI-130 is less severely conservative than ABI-126 at threshold 0.5, but still leaves some fixed-threshold Dice on the table. ABI-126's best diagnostic filtered Dice was higher at 0.4079 with threshold 0.05, indicating that ABI-126 remains a latent high-recall branch if calibration can be shifted in-contract. ABI-130's value is that it moves the default threshold closer to that balanced regime without an external threshold change.

## Failure-bucket observations

The per-sample metrics identify a cleaner but still imperfect clutter/under-recall trade-off:

1. Negative-patch clutter increased relative to ABI-126 but stayed below recall-heavy branches. Among 2,003 negative validation patches, 1,187 had at least one filtered predicted-positive pixel. The median negative-patch false-positive count was 6 pixels; 207 negative patches exceeded 100 filtered false-positive pixels, 10 exceeded 500, and 2 exceeded 1,000. This is worse than ABI-126 and ABI-066 on negative-patch discipline, but better than ABI-121 and lower in total negative false positives than ABI-068.
2. Positive patches remain under-segmented, especially for large or difficult MIT examples. Among 1,085 positive validation patches, 37 had zero filtered predicted-positive pixels, 557 had more false-positive than true-positive pixels, 192 were below 0.1 filtered Dice, 275 were below 0.2 filtered Dice, and 303 were below 0.2 filtered recall. Median positive-patch filtered recall was 0.3943, median precision 0.4869, and median Dice 0.3890.
3. The Dataset Source split remains real. Positive-patch median filtered Dice was 0.3701 on MIT and 0.4162 on Google. Median filtered recall was 0.3826 on MIT and 0.4098 on Google; median filtered precision was 0.4419 on MIT and 0.5383 on Google. ABI-130 improved the MIT under-recall issue relative to ABI-126, but did not eliminate the MIT-vs-Google gap.

Artifact Filters removed 36,735 pixels over 746 samples, corresponding to 146,940 square kilometers under the evaluation metadata's pixel-area accounting. Raw Dice was 0.4100 versus filtered Dice 0.3954; raw predicted-positive pixels were 607,041 versus 570,306 filtered. The filter reduced 19,831 false-positive pixels while also removing 16,904 true-positive pixels. This raw-to-filtered difference is modest and does not indicate primary Artifact Filter dependence, but it reinforces that ABI-130's clutter increase relative to ABI-126 is genuine after filtering. The retained diagnostic sample pairs are traceability artifacts selected under a bounded policy; this note intentionally does not reproduce individual scene identifiers, coordinates, or images.

## Interpretation

Classify ABI-130's whole-validation evaluation as valid, non-collapsed diagnostic support for Solar Geometry Input in the ASPP/detail BCE-Dice branch. The evaluation confirms the capped conclusion: adding provider-approved SZA features improved default-threshold recall and aggregate Dice relative to ABI-126, while preserving a much cleaner operating point than ABI-121.

ABI-130 does not cleanly replace the local references. ABI-068 remains the more MIT-recall-balanced aggregate reference despite nearly identical aggregate Dice. ABI-066 remains the stronger connectivity reference. ABI-126 remains the ASPP/detail precision/connectivity branch and has stronger latent threshold-sweep upside if in-contract calibration can recover recall. ABI-130 should be retained as the ASPP/detail SZA-calibrated default-threshold reference and as evidence that illumination geometry can shift a conservative branch toward better recall without catastrophic false-positive expansion.

This result argues against another simple SZA-only or auxiliary-only ASPP/detail tweak as the next immediate handoff. The useful frontier is a calibration/continuity design that keeps ABI-130's default-threshold recall improvement while recovering some ABI-126/ABI-066 connectivity and negative-patch discipline, or a broader architecture/preprocessing scout if the ASPP/detail family begins to saturate.

## Decision

Do not promote ABI-130, and do not reinterpret this whole-validation diagnostic as deployment evidence. Retain ABI-130 as the best whole-validation-tested ASPP/detail SZA-calibrated capped branch, but keep ABI-068, ABI-066, and ABI-126 as active comparison references for aggregate Dice/source balance, connectivity, and precision respectively.

A reasonable next in-contract hypothesis is a conservative calibration/continuity continuation: use the SZA-aware ASPP/detail evidence path only if the architecture can add neutral or non-suppressive continuity/detail constraints that reduce negative-patch clutter without reverting to ABI-126-style MIT under-recall. If that cannot be stated as a controlled, contract-compliant Candidate Experiment, broaden away from ASPP/detail input/loss tuning toward another architecture, calibration, preprocessing, or training-policy frontier.

No new Capability Request or Campaign Report is required from this diagnostic result.

## Artifact references

- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/summary.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/evaluations/eval_evalreq_abi126_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_085615_d05ab3/outputs/evaluations/eval_evalreq_abi126_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260831_041559_43da35/outputs/evaluations/eval_evalreq_abi121_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
