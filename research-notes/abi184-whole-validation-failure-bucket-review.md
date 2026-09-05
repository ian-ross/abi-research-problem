# ABI-184 whole-validation failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi184_wholeval_failure_buckets_v1` for ABI-184 Run `run_20260902_213856_2c04ac`.

The evaluation request asked whether ABI-184's capped Line plus Centerline auxiliary late36 precision and connectivity gains survive on the full 3,088-sample Working Validation Split, and whether the recall and MIT-source deficits versus ABI-181 create unacceptable false-negative or source-specific failure modes. This is diagnostic evidence only; promotion remains operator-reviewed.

Primary comparison references:

- ABI-184 signed-detail full-scale skip ASPP with Line plus Centerline auxiliary supervision and late36 budget: `run_20260902_213856_2c04ac`, Evaluation `eval_evalreq_abi184_wholeval_failure_buckets_v1`
- ABI-181 signed-detail full-scale skip ASPP late36 aggregate reference: `run_20260902_150611_cbbf35`, Evaluation `eval_evalreq_abi181_wholeval_failure_buckets_v1`
- ABI-173 signed-detail full-scale skip ASPP 12-epoch parent: `run_20260901_234732_bd5917`, Evaluation `eval_evalreq_abi173_wholeval_failure_buckets_v1`
- ABI-154 full-scale skip ASPP/detail precision-connectivity reference: `run_20260901_071026_32d3ec`, Evaluation `eval_evalreq_abi154_wholeval_failure_buckets_v1`
- ABI-130 SZA-aware ASPP/detail aggregate comparator: `run_20260831_121006_7d24be`, Evaluation `eval_evalreq_abi130_wholeval_failure_buckets_v1`
- ABI-068 frequency-gated line U-Net focal-Tversky source-balance comparator: `run_20260828_010836_4ccc77`, Evaluation `eval_evalreq_abi068_wholeval_failure_buckets_v1`
- Canonical MCAST 1.1 and MCAST 2.1 summaries from `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`

## Whole-validation metrics

At threshold 0.5 on the full 3,088-sample Working Validation Split, ABI-184 reached:

| Metric | ABI-184 whole validation |
| --- | ---: |
| Filtered Dice | 0.4093 |
| MIT filtered Dice | 0.3898 |
| Google filtered Dice | 0.4476 |
| Filtered precision | 0.4893 |
| Filtered recall | 0.3517 |
| Filtered contrail connectivity | 0.4763 |
| Filtered predicted-positive pixels | 509,971 |
| Filtered false-positive pixels | 260,462 |
| Filtered false-negative pixels | 459,854 |

ABI-184's capped precision/connectivity signal survived whole-validation evaluation, but its capped aggregate Dice did not displace ABI-181. Whole-validation filtered Dice was 0.4093, close to its capped best-validation filtered Dice of 0.4066, and whole-validation Google filtered Dice was 0.4476 versus 0.4555 capped. MIT filtered Dice rose slightly from 0.3879 capped to 0.3898 whole validation but remained the weaker source.

Relative to ABI-181, ABI-184 has lower aggregate filtered Dice (0.4093 versus 0.4124), lower MIT filtered Dice (0.3898 versus 0.3988), and lower recall (0.3517 versus 0.3832). The tradeoff is clearly favorable for precision, connectivity, and positive-area discipline: ABI-184 has higher precision (0.4893 versus 0.4466), higher connectivity (0.4763 versus 0.3676), fewer filtered predicted-positive pixels (509,971 versus 608,649), and fewer false positives (260,462 versus 336,853), while incurring more false negatives (459,854 versus 437,567).

Relative to ABI-173, ABI-184 improves aggregate filtered Dice, MIT filtered Dice, Google filtered Dice, precision, connectivity, false positives, and predicted-positive area, but lowers recall and increases false negatives slightly. Relative to ABI-154, ABI-184 has higher aggregate/source Dice, precision, recall, and connectivity, with similar false-positive burden. Relative to ABI-068, ABI-184 has higher aggregate and Google filtered Dice plus much better precision/connectivity and fewer false positives, while ABI-068 remains better on MIT filtered Dice and recall.

Against canonical MCAST context, ABI-184's filtered Dice 0.4093 is above MCAST 1.1 (0.3842) and MCAST 2.1 (0.3873). ABI-184's precision is above both MCAST summaries and its connectivity is above MCAST 2.1 but below MCAST 1.1. Its recall is above MCAST 1.1 but below MCAST 2.1. This is comparison context only, not a promotion claim.

## Threshold behavior

The threshold sweep indicates that ABI-184 is under-recalling at the fixed 0.5 threshold and has larger diagnostic threshold headroom than ABI-181. Filtered Dice improves from 0.4093 at threshold 0.5 to 0.4259 at threshold 0.05. At threshold 0.10, filtered Dice is 0.4252 with precision 0.4315 and recall 0.4191; at threshold 0.20, filtered Dice is 0.4212 with precision 0.4551 and recall 0.3919. Raw Dice improves from 0.4250 at threshold 0.5 to 0.4396 at threshold 0.10.

This does not authorize Candidate-owned thresholding, calibration, postprocessing, losses, metrics, or Artifact Filters. The design lesson is that the Line plus Centerline branch learned a strong connected and precise representation, but its fixed-threshold operating point is too conservative relative to the aggregate-Dice objective. A future in-contract architecture continuation should seek recall-preserving calibration in model logits/features rather than relying on a changed evaluation threshold.

## Failure-bucket observations

Failure buckets explain the precision/connectivity versus recall tradeoff:

1. Negative-patch clutter is much better than ABI-181. Among 2,003 negative validation patches, ABI-184 produced at least one filtered predicted-positive pixel on 946 patches, versus 1,286 for ABI-181. Median negative-patch false-positive count was 0 pixels. Total negative-patch false-positive pixels were 53,814, with 152 negative patches above 100 filtered false-positive pixels, 6 above 500, and 1 above 1,000. This improves on ABI-181's 77,592 negative-patch false-positive pixels and also improves ABI-154's 61,426 reference value in total negative-patch false-positive burden.
2. Positive-patch misses are worse. ABI-184 had 48 positive validation patches with zero filtered predicted-positive pixels, 196 positive patches below 0.1 filtered Dice, 267 below 0.2 filtered Dice, and 312 below 0.2 filtered recall. ABI-181 had 32 zero-prediction positives, 169 below 0.1 Dice, 239 below 0.2 Dice, and 258 below 0.2 recall. The line-supervised operating point is therefore cleaner but misses too many true contrail pixels and patches.
3. Median positive-patch quality shows high precision with insufficient recall. ABI-184's median positive-patch filtered Dice was 0.4024, median precision 0.5455, and median recall 0.3710. ABI-181's corresponding medians were 0.4118, 0.4928, and 0.4207. By Dataset Source, ABI-184's median positive-patch filtered Dice was 0.3758 on MIT and 0.4343 on Google; median precision was 0.4827 on MIT and 0.5961 on Google; median recall was 0.3529 on MIT and 0.4037 on Google. The Google precision/connectivity behavior is strong, but MIT and low-recall positive patches remain the main failure mode.

Artifact Filters removed 33,698 predicted-positive pixels over the full split, corresponding to 134,792 square kilometers under the evaluation metadata's pixel-area accounting. Raw Dice was 0.4250 versus filtered Dice 0.4093; raw predicted-positive pixels were 543,669 versus 509,971 filtered. The filter removed enough true positives to lower Dice slightly. This does not indicate primary Artifact Filter dependence, but it reinforces that ABI-184's conservative mask area leaves little spare recall after filtering.

The retained diagnostic sample GeoTIFFs are traceability artifacts selected under the bounded evaluation policy. This note does not reproduce individual scene identifiers, coordinates, raw samples, or images.

## Interpretation

Classify ABI-184's whole-validation evaluation as valid, finite, non-collapsed diagnostic evidence for the late-improving signed-detail full-scale skip ASPP Line plus Centerline auxiliary branch. The whole-validation result confirms that direct Line Target auxiliary supervision can produce a cleaner, more connected operating point than ABI-181 without relying on capped-subset luck.

However, ABI-184 should not replace ABI-181 as the aggregate filtered-Dice reference because its recall and MIT-source deficits are real on the full Working Validation Split. ABI-181 remains the current whole-validation aggregate filtered-Dice reference. ABI-184 should replace ABI-154 as the local precision/connectivity reference within this signed-detail ASPP lineage, because it preserves or improves ABI-154's precision/connectivity while materially improving aggregate/source Dice and recall.

The actionable design lesson is not another unchanged epoch extension. ABI-184 needs a recall-preserving calibration mechanism that keeps the Line Target's high precision and connected structure while softening the overly conservative fixed-threshold mask behavior, especially for MIT positives.

## Decision

Do not promote ABI-184 or reinterpret this whole-validation diagnostic as deployment evidence. Retain ABI-181 as the whole-validation-tested aggregate filtered-Dice reference. Retain ABI-184 as the best whole-validation-tested precision/connectivity and negative-patch discipline reference in the signed-detail full-scale skip ASPP family.

Do not repeat ABI-184 unchanged and do not request another longer budget for the same exact branch. A reasonable next in-contract hypothesis is a close continuation that combines ABI-184's direct Line plus Centerline supervision with a recall-preserving calibration or residual foreground-expansion mechanism under trusted `bce_dice` or `focal_tversky`, approved `abi_16ch_plus_sza` input, trusted random mirroring, Harness-owned sampling/loss/metric/Artifact Filter boundaries, and no Candidate-owned thresholding or postprocessing. No Capability Request or Campaign Report is required from this diagnostic result.

## Artifact references

- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/summary.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/final_metrics.json`
- `run_20260902_213856_2c04ac/outputs/metrics.jsonl`
- `run_20260902_213856_2c04ac/outputs/resource_profile.json`
- `run_20260902_213856_2c04ac/outputs/model_summary.json`
- `run_20260902_213856_2c04ac/resolved_manifest.yaml`
- `run_20260902_213856_2c04ac/candidate/budget_request.yaml`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260901_234732_bd5917/outputs/evaluations/eval_evalreq_abi173_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
