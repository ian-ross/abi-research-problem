# ABI-154 whole-validation failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi154_wholeval_failure_buckets_v1` for ABI-154 Run `run_20260901_071026_32d3ec`.

The evaluation request asked whether ABI-154's capped full-scale skip ASPP/detail decoder gains in filtered precision, connectivity, MIT filtered Dice, and positive-area discipline survived on the full 3,088-sample Working Validation Split, and whether the lower Google Dice and recall versus ABI-130 reflected an acceptable precision/connectivity trade-off rather than full-validation under-segmentation or source-specific failure. This is diagnostic evidence only; promotion remains operator-reviewed.

Primary comparison references:

- ABI-154 full-spectral BTD+SZA full-scale skip ASPP/detail decoder BCE-Dice Centerline-auxiliary Run: `run_20260901_071026_32d3ec`, Evaluation `eval_evalreq_abi154_wholeval_failure_buckets_v1`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice whole-validation reference: `run_20260831_121006_7d24be`, Evaluation `eval_evalreq_abi130_wholeval_failure_buckets_v1`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice whole-validation precision/connectivity comparator: `run_20260831_085615_d05ab3`, Evaluation `eval_evalreq_abi126_wholeval_failure_buckets_v1`
- ABI-068 frequency-gated line U-Net focal-Tversky whole-validation aggregate/source-balance reference: `run_20260828_010836_4ccc77`, Evaluation `eval_evalreq_abi068_wholeval_failure_buckets_v1`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice whole-validation connectivity reference: `run_20260827_230540_bf4ce3`, Evaluation `eval_evalreq_abi066_wholeval_failure_buckets_v1`
- ABI-142 and ABI-143 capped SZA-aware ridge/full-detail comparison Runs: `run_20260831_215104_d4c318`, `run_20260831_224534_27b73d`
- Canonical MCAST 1.1 and MCAST 2.1 summaries from `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`

## Whole-validation metrics

At threshold 0.5 on the full 3,088-sample Working Validation Split, ABI-154 reached:

| Metric | ABI-154 whole validation |
| --- | ---: |
| Filtered Dice | 0.3941 |
| MIT filtered Dice | 0.3832 |
| Google filtered Dice | 0.4158 |
| Filtered precision | 0.4812 |
| Filtered recall | 0.3338 |
| Filtered contrail connectivity | 0.4438 |
| Filtered predicted-positive pixels | 492,002 |
| Filtered false-positive pixels | 255,247 |
| Filtered false-negative pixels | 472,608 |

The capped signal largely survived. ABI-154's capped best-validation filtered Dice was 0.3944 and whole-validation filtered Dice was 0.3941. MIT filtered Dice was also stable, 0.3824 capped versus 0.3832 whole validation. The main softening was on Google filtered Dice, 0.4260 capped versus 0.4158 whole validation. Precision, recall, connectivity, and filtered positive area remained close to the capped operating point: whole-validation precision 0.4812, recall 0.3338, connectivity 0.4438, and 492,002 filtered predicted-positive pixels.

Relative to ABI-130, ABI-154 is not an aggregate improvement: filtered Dice is 0.3941 versus 0.3954, and Google filtered Dice is 0.4158 versus 0.4256. The intended trade-off did survive, however. ABI-154 improves MIT filtered Dice (0.3832 vs 0.3797), precision (0.4812 vs 0.4436), connectivity (0.4438 vs 0.3935), and positive-area discipline (492,002 vs 570,306 filtered predicted-positive pixels). It removes 62,072 filtered false-positive pixels relative to ABI-130, but adds 16,232 false-negative pixels. This confirms a real precision/connectivity shift rather than a free SZA-aware ASPP/detail improvement.

Relative to ABI-126, ABI-154 is modestly stronger on aggregate filtered Dice (0.3941 vs 0.3892), MIT filtered Dice (0.3832 vs 0.3662), precision (0.4812 vs 0.4770), and recall (0.3338 vs 0.3288). It remains lower on Google filtered Dice (0.4158 vs 0.4319) and connectivity (0.4438 vs 0.4563). The full-scale skip branch therefore improves ABI-126's MIT/default-threshold weakness without fully matching ABI-126's Google and connectivity profile.

Relative to ABI-068, ABI-154 is an aggregate near-tie but with different errors: filtered Dice is 0.3941 versus 0.3951. ABI-154 improves Google filtered Dice (0.4158 vs 0.4032), precision (0.4812 vs 0.3996), connectivity (0.4438 vs 0.3868), and reduces filtered false positives by 161,258 pixels, but trails MIT filtered Dice (0.3832 vs 0.3908) and recall (0.3338 vs 0.3907). Relative to ABI-066, ABI-154 improves aggregate, MIT, Google, precision, and false-positive burden while remaining slightly lower on the BCE-Dice-clDice branch's strongest feature, connectivity.

Against canonical full-validation MCAST summaries, ABI-154's filtered Dice 0.3941 is above MCAST 1.1 (0.3842) and MCAST 2.1 (0.3873) in this shared evaluation context. Its precision is above both canonical MCAST summaries, but its recall is below MCAST 2.1 and near MCAST 1.1. This is comparison context only, not a promotion claim.

## Threshold behavior

The threshold sweep shows ABI-154 is conservative at the fixed 0.5 threshold. Filtered Dice improves from 0.3941 at threshold 0.5 to 0.4107 at threshold 0.05. The closest filtered precision/recall balance is threshold 0.10, with precision 0.4194, recall 0.4003, and filtered Dice 0.4096. Raw Dice similarly improves from 0.4100 at threshold 0.5 to 0.4246 at threshold 0.05.

This does not authorize candidate-owned thresholding, postprocessing, calibration, or Artifact Filters. The design lesson is that ABI-154's full-scale skip aggregation produces useful precision/connectivity at the default threshold but leaves substantial latent recall and Dice in lower-threshold regimes. A future in-contract continuation should try to shift default-threshold calibration without giving back the negative-patch discipline that differentiates ABI-154 from ABI-130 and ABI-068.

## Failure-bucket observations

The full-validation failure buckets show a cleaner but more under-recall-prone profile than ABI-130:

1. Negative-patch clutter improved relative to ABI-130 and ABI-068, though not below the cleanest comparator. Among 2,003 negative validation patches, 1,032 had at least one filtered predicted-positive pixel. Median negative-patch false-positive count was 2 pixels; 179 negative patches exceeded 100 filtered false-positive pixels, 6 exceeded 500, and 1 exceeded 1,000. Total negative-patch false-positive pixels were 61,426, below ABI-130's 77,746 and ABI-068's 100,641, but slightly above ABI-126's 59,769.
2. Positive-patch under-recall is the main cost. Among 1,085 positive validation patches, 52 had zero filtered predicted-positive pixels, 479 had more false-positive than true-positive pixels, 209 were below 0.1 filtered Dice, 281 were below 0.2 filtered Dice, and 314 were below 0.2 filtered recall. The zero-predicted-positive count is worse than ABI-130's 37 and ABI-068's 26, and slightly worse than ABI-126's 48.
3. Median positive-patch behavior is precision-forward. Median positive-patch filtered Dice was 0.3908, precision 0.5422, and recall 0.3518. Positive-patch median filtered Dice was 0.3805 on MIT and 0.3997 on Google; median precision was 0.4985 on MIT and 0.5848 on Google; median recall was nearly source-balanced at 0.3518 on MIT and 0.3533 on Google. Source balance in recall is encouraging, but it is balanced at a low default-threshold recall level.

Artifact Filters removed 32,228 pixels over 655 samples, corresponding to 128,912 square kilometers under the evaluation metadata's pixel-area accounting. Raw Dice was 0.4100 versus filtered Dice 0.3941; raw predicted-positive pixels were 524,230 versus 492,002 filtered. The filters removed similar numbers of true-positive and false-positive pixels, 16,146 and 16,082 respectively. This does not indicate primary Artifact Filter dependence, but it explains why ABI-154's raw-to-filtered gap is not a simple cleanup gain.

## Interpretation

Classify ABI-154's whole-validation evaluation as valid, finite, non-collapsed diagnostic support for full-scale skip aggregation as a precision/connectivity lever inside the SZA-aware ASPP/detail family. The result confirms the capped conclusion that ABI-154 is a cleaner, more connected branch than ABI-130, not that it is an aggregate replacement.

ABI-130 remains the stronger whole-validation-tested SZA-aware ASPP/detail aggregate/reference branch because it has slightly higher filtered Dice and better Google Dice/recall. ABI-154 should be retained as the SZA-aware ASPP/detail precision/connectivity branch because it materially improves false-positive discipline and connectivity while preserving aggregate Dice near ABI-130. ABI-068 remains the more MIT-recall-balanced local aggregate reference, and ABI-066 remains the frequency-gated connectivity reference. ABI-126 remains a useful non-SZA ASPP/detail comparator, but ABI-154 is a better MIT/default-threshold continuation than ABI-126.

The evaluation argues against repeating all-scale skip fusion unchanged. The useful frontier is not more skip capacity by itself; it is default-threshold calibration or recall recovery that preserves ABI-154's negative-patch discipline and connectivity. In-contract options include a conservative logit/calibration head, a controlled loss/sampling-policy continuation, or broadening away from ASPP/detail skip fusion if the family saturates.

## Decision

Do not promote ABI-154, and do not reinterpret this whole-validation diagnostic as deployment evidence. Retain ABI-154 as the whole-validation-tested SZA-aware ASPP/detail precision/connectivity reference, while keeping ABI-130 as the SZA-aware ASPP/detail aggregate reference and ABI-068 as the local aggregate/source-balance comparator.

A reasonable next hypothesis is a calibration-focused continuation that starts from the SZA-aware ASPP/detail evidence path and attempts to recover default-threshold recall without expanding negative-patch clutter. If that cannot be stated as a controlled, contract-compliant Candidate Experiment, broaden to another architecture, loss, preprocessing, or data-policy frontier rather than repeating simple full-scale skip variants.

No new Capability Request or Campaign Report is required from this diagnostic result.

## Artifact references

- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/summary.json`
- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260831_085615_d05ab3/outputs/evaluations/eval_evalreq_abi126_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_085615_d05ab3/outputs/evaluations/eval_evalreq_abi126_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
