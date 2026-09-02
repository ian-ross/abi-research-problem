# ABI-173 whole-validation failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi173_wholeval_failure_buckets_v1` for ABI-173 Run `run_20260901_234732_bd5917`.

The evaluation request asked whether ABI-173's capped signed-detail full-scale skip ASPP decoder gains in aggregate filtered Dice, MIT filtered Dice, Google filtered Dice, and default-threshold recall over ABI-154 survived on the full 3,088-sample Working Validation Split, and whether the lower precision/connectivity reflected acceptable recall recovery or unacceptable clutter, fragmentation, or source-specific degradation. This is diagnostic evidence only; promotion remains operator-reviewed.

Primary comparison references:

- ABI-173 signed-detail full-scale skip ASPP decoder BCE-Dice Centerline-auxiliary Run: `run_20260901_234732_bd5917`, Evaluation `eval_evalreq_abi173_wholeval_failure_buckets_v1`
- ABI-154 full-scale skip ASPP/detail decoder BCE-Dice whole-validation precision/connectivity reference: `run_20260901_071026_32d3ec`, Evaluation `eval_evalreq_abi154_wholeval_failure_buckets_v1`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice whole-validation aggregate reference: `run_20260831_121006_7d24be`, Evaluation `eval_evalreq_abi130_wholeval_failure_buckets_v1`
- ABI-068 frequency-gated line U-Net focal-Tversky whole-validation aggregate/source-balance reference: `run_20260828_010836_4ccc77`, Evaluation `eval_evalreq_abi068_wholeval_failure_buckets_v1`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice whole-validation precision/connectivity comparator: `run_20260831_085615_d05ab3`, Evaluation `eval_evalreq_abi126_wholeval_failure_buckets_v1`
- Canonical MCAST 1.1 and MCAST 2.1 summaries from `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`

## Whole-validation metrics

At threshold 0.5 on the full 3,088-sample Working Validation Split, ABI-173 reached:

| Metric | ABI-173 whole validation |
| --- | ---: |
| Filtered Dice | 0.3973 |
| MIT filtered Dice | 0.3870 |
| Google filtered Dice | 0.4161 |
| Filtered precision | 0.4263 |
| Filtered recall | 0.3719 |
| Filtered contrail connectivity | 0.3197 |
| Filtered predicted-positive pixels | 618,932 |
| Filtered false-positive pixels | 355,097 |
| Filtered false-negative pixels | 445,528 |

The capped signal largely survived. ABI-173's capped best-validation filtered Dice was 0.3962 and whole-validation filtered Dice was 0.3973. MIT filtered Dice improved from 0.3838 capped to 0.3870 whole validation. Google filtered Dice softened from 0.4269 capped to 0.4161 whole validation, but did not collapse. Precision, recall, and connectivity stayed close to the capped operating point: whole-validation precision 0.4263, recall 0.3719, and connectivity 0.3197.

Relative to ABI-154, ABI-173 achieved the intended recall recovery and modest overlap gains on the full validation split: filtered Dice rose from 0.3941 to 0.3973, MIT filtered Dice from 0.3832 to 0.3870, Google filtered Dice from 0.4158 to 0.4161, and filtered recall from 0.3338 to 0.3719. The cost also survived: precision fell from 0.4812 to 0.4263, connectivity fell from 0.4438 to 0.3197, and filtered false-positive pixels rose by about 99,850.

Relative to ABI-130, ABI-173 is now the stronger whole-validation-tested SZA-aware ASPP/detail aggregate branch by filtered Dice, 0.3973 versus 0.3954, and by MIT filtered Dice, 0.3870 versus 0.3797. It also recovers more recall, 0.3719 versus 0.3566. However, ABI-173 remains lower on Google filtered Dice, 0.4161 versus 0.4256, lower on precision, 0.4263 versus 0.4436, lower on connectivity, 0.3197 versus 0.3935, and higher in filtered false-positive pixels, 355,097 versus 317,319.

Relative to ABI-068, ABI-173 improves aggregate filtered Dice, Google filtered Dice, precision, and false-positive burden, but trails MIT filtered Dice, recall, and connectivity. ABI-068 therefore remains the more MIT-recall-balanced comparator, while ABI-173 becomes the stronger SZA-aware ASPP/detail aggregate result and ABI-154 remains the cleaner connected branch.

Against the canonical full-validation MCAST summaries, ABI-173's filtered Dice 0.3973 is above MCAST 1.1 (0.3842) and MCAST 2.1 (0.3873) in this shared evaluation context. ABI-173's precision is above MCAST 2.1 but below MCAST 1.1; its recall is above MCAST 1.1 but below MCAST 2.1; and its connectivity is above MCAST 2.1 but below MCAST 1.1. This is comparison context only, not a promotion claim.

## Threshold behavior

The threshold sweep shows moderate residual calibration upside. ABI-173's filtered Dice improves from 0.3973 at the fixed 0.5 threshold to 0.4043 at threshold 0.15. The closest filtered precision/recall balance is threshold 0.30, with precision 0.4043, recall 0.4005, and a very small precision/recall gap. Raw Dice similarly improves from 0.4114 at threshold 0.5 to 0.4172 at threshold 0.15.

This does not authorize candidate-owned thresholding, postprocessing, calibration outside the manifest contract, or Artifact Filters. The design lesson is that signed-detail preprocessing moved ABI-154 closer to a useful default-threshold recall point, but still leaves some threshold-sweep Dice available and did not preserve ABI-154-like connectivity.

## Failure-bucket observations

The failure buckets show that the recall recovery is real but paid for with materially worse negative-patch clutter than ABI-154 and ABI-130:

1. Among 2,003 negative validation patches, 1,423 had at least one filtered predicted-positive pixel. Median negative-patch false-positive count was 20 pixels; 295 negative patches exceeded 100 filtered false-positive pixels, 8 exceeded 500, and none exceeded 1,000. Total negative-patch false-positive pixels were 100,043. This is substantially worse than ABI-154's 1,032 nonempty negative patches and 61,426 negative-patch false-positive pixels, worse than ABI-130's 1,187 and 77,746, and close to ABI-068's higher-clutter recall-forward profile.
2. Positive-patch misses improved strongly relative to ABI-154. Among 1,085 positive validation patches, 17 had zero filtered predicted-positive pixels, compared with ABI-154's 52, ABI-130's 37, and ABI-068's 26. ABI-173 had 174 positive patches below 0.1 filtered Dice, 247 below 0.2 filtered Dice, and 256 below 0.2 filtered recall. This confirms that signed detail reduced the severe under-recall tail.
3. Median positive-patch behavior shifted toward recall but lost precision. Median positive-patch filtered Dice was 0.4000, median precision 0.4615, and median recall 0.4081. By Dataset Source, median positive-patch filtered Dice was 0.3715 on MIT and 0.4317 on Google; median precision was 0.4357 on MIT and 0.5068 on Google; median recall was 0.3798 on MIT and 0.4453 on Google. The Google positive-patch median Dice is strong, but the aggregate Google Dice remains below ABI-130 because false positives and lower connectivity offset the recall gains.

Artifact Filters removed 40,056 predicted-positive pixels over the full split, corresponding to 160,224 square kilometers under the evaluation metadata's pixel-area accounting. Raw Dice was 0.4114 versus filtered Dice 0.3973; raw predicted-positive pixels were 658,988 versus 618,932 filtered. Filtering removed 22,391 false-positive pixels and 17,665 true-positive pixels. This does not indicate primary Artifact Filter dependence; the raw-to-filtered gap is consistent with the fixed provider-owned filter removing both artifacts and some true contrail pixels.

The retained diagnostic sample pairs and GeoTIFFs are traceability artifacts selected under the bounded evaluation policy. This note does not reproduce individual scene identifiers, coordinates, raw samples, or images.

## Interpretation

Classify ABI-173's whole-validation evaluation as valid, finite, non-collapsed diagnostic evidence for signed-detail preprocessing inside the SZA-aware full-scale skip ASPP/detail branch. The evaluation confirms the capped conclusion that signed positive/negative detail streams can recover default-threshold recall and improve aggregate filtered Dice relative to ABI-154.

The result is scientifically positive but mixed. ABI-173 should replace ABI-130 as the whole-validation-tested SZA-aware ASPP/detail aggregate filtered-Dice reference, because its aggregate and MIT Dice gains survived beyond the representative cap. ABI-154 should remain the precision/connectivity reference, because ABI-173 gave back much of ABI-154's false-positive discipline and connected-line structure. ABI-068 remains the local aggregate/source-balance comparator because it is stronger on MIT Dice and recall with better connectivity than ABI-173, even though ABI-173 is cleaner and stronger on Google Dice.

The main design lesson is that recall recovery from signed detail is useful but not enough by itself. Another unconstrained positive-area expansion is unlikely to be helpful. The next in-contract hypothesis should preserve ABI-173's signed-detail recall benefits while adding a conservative connectivity-preserving or false-positive-disciplined mechanism that does not move thresholding, Artifact Filters, losses, target derivation, data loading, sampling, or metrics into Candidate code.

## Decision

Do not promote ABI-173 and do not reinterpret this whole-validation diagnostic as deployment evidence. Retain ABI-173 as the whole-validation-tested SZA-aware ASPP/detail aggregate branch, ABI-154 as the SZA-aware ASPP/detail precision/connectivity branch, ABI-130 as the prior SZA-aware ASPP/detail aggregate reference, and ABI-068 as the broader aggregate/source-balance comparator.

Do not repeat ABI-173 unchanged. A reasonable next hypothesis is a controlled family-development continuation that keeps ABI-173's signed-detail front end but constrains the decoder/head toward connected, low-clutter line evidence, for example with a neutral connectivity-preserving refinement or conservative objectness/line-evidence gate under the existing trusted `bce_dice` primary loss and provider-derived Centerline Target auxiliary supervision. No Capability Request or Campaign Report is required from this diagnostic result.

## Artifact references

- `run_20260901_234732_bd5917/outputs/evaluations/eval_evalreq_abi173_wholeval_failure_buckets_v1/summary.json`
- `run_20260901_234732_bd5917/outputs/evaluations/eval_evalreq_abi173_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_234732_bd5917/outputs/evaluations/eval_evalreq_abi173_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260901_234732_bd5917/outputs/evaluations/eval_evalreq_abi173_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260901_234732_bd5917/outputs/evaluations/eval_evalreq_abi173_wholeval_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260901_234732_bd5917/outputs/best_metrics.json`
- `run_20260901_234732_bd5917/outputs/final_metrics.json`
- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260831_085615_d05ab3/outputs/evaluations/eval_evalreq_abi126_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
