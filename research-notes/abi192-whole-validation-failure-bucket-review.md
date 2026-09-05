# ABI-192 whole-validation failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi192_wholeval_failure_buckets_v1` for ABI-192 Run `run_20260903_085513_f395ad`.

The evaluation request asked whether ABI-192's capped directional-lattice late36 aggregate, source-balance, and recall gains survived on the full 3,088-sample Working Validation Split, and whether failure buckets show that its small capped differences versus ABI-181 and ABI-184 are useful full-validation behavior or capped-subset noise. This is diagnostic evidence only; promotion remains operator-reviewed.

Primary comparison references:

- ABI-192 directional-lattice full-scale skip ASPP late36 Run: `run_20260903_085513_f395ad`, Evaluation `eval_evalreq_abi192_wholeval_failure_buckets_v1`
- ABI-191 exploratory directional-lattice parent Run: `run_20260903_075132_5cff8c`
- ABI-181 signed-detail full-scale skip ASPP late36 aggregate reference: `run_20260902_150611_cbbf35`, Evaluation `eval_evalreq_abi181_wholeval_failure_buckets_v1`
- ABI-184 signed-detail full-scale skip ASPP Line plus Centerline auxiliary precision/connectivity reference: `run_20260902_213856_2c04ac`, Evaluation `eval_evalreq_abi184_wholeval_failure_buckets_v1`
- Canonical MCAST 1.1 and MCAST 2.1 summaries from `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`

## Whole-validation metrics

At threshold 0.5 on the full 3,088-sample Working Validation Split, ABI-192 reached:

| Metric | ABI-192 whole validation |
| --- | ---: |
| Filtered Dice | 0.4096 |
| MIT filtered Dice | 0.3948 |
| Google filtered Dice | 0.4367 |
| Filtered precision | 0.4329 |
| Filtered recall | 0.3886 |
| Filtered contrail connectivity | 0.3535 |
| Filtered predicted-positive pixels | 636,758 |
| Filtered false-positive pixels | 361,081 |
| Filtered false-negative pixels | 433,686 |

ABI-192's capped late36 signal mostly survived whole-validation evaluation but did not displace ABI-181. The capped best-validation filtered Dice was 0.4072 at epoch 36; whole-validation filtered Dice was 0.4096. MIT filtered Dice was similar-to-better relative to the cap, 0.3930 capped versus 0.3948 whole validation. Google filtered Dice softened from 0.4429 capped to 0.4367 whole validation. Precision, recall, connectivity, and predicted-positive area stayed close to the capped operating point, so the capped evidence was directionally representative rather than a misleading collapse.

Relative to ABI-181, ABI-192 has lower aggregate filtered Dice (0.4096 versus 0.4124), lower MIT filtered Dice (0.3948 versus 0.3988), lower Google filtered Dice (0.4367 versus 0.4395), lower precision (0.4329 versus 0.4466), and lower connectivity (0.3535 versus 0.3676). ABI-192 has slightly higher recall (0.3886 versus 0.3832), fewer false negatives (433,686 versus 437,567), and more true positives, but at the cost of more predicted-positive pixels and false positives. ABI-181 therefore remains the strongest whole-validation-tested aggregate filtered-Dice reference.

Relative to ABI-184, ABI-192 narrowly improves aggregate filtered Dice (0.4096 versus 0.4093), MIT filtered Dice (0.3948 versus 0.3898), and recall (0.3886 versus 0.3517), with fewer false negatives. The tradeoff is unfavorable for the main ABI-184 strengths: ABI-192 has lower Google filtered Dice (0.4367 versus 0.4476), much lower precision (0.4329 versus 0.4893), much lower connectivity (0.3535 versus 0.4763), and far more false positives and predicted-positive pixels. ABI-184 remains the precision/connectivity and negative-patch-discipline reference.

Against the canonical full-validation MCAST summaries, ABI-192's filtered Dice 0.4096 is above MCAST 1.1 (0.3842) and MCAST 2.1 (0.3873). ABI-192's precision is below MCAST 1.1 but above MCAST 2.1, its recall is above MCAST 1.1 and below MCAST 2.1, and its connectivity is between MCAST 2.1 and MCAST 1.1. This is comparison context only, not a promotion claim.

## Threshold behavior

The threshold sweep shows modest filtered-Dice upside at lower thresholds. ABI-192 improves from filtered Dice 0.4096 at threshold 0.5 to 0.4167 at threshold 0.15. At threshold 0.15, filtered precision is 0.3970 and recall is 0.4385. The closest filtered precision/recall balance is threshold 0.30, with Dice 0.4143, precision 0.4168, recall 0.4119, and a precision/recall gap of about 0.0049. Raw Dice similarly improves from 0.4242 at threshold 0.5 to 0.4303 at threshold 0.15.

This does not authorize Candidate-owned thresholding, calibration, postprocessing, losses, metrics, or Artifact Filters. The design lesson is that ABI-192 is not severely miscalibrated, but it has less useful threshold-sweep headroom than ABI-184 and does not exceed ABI-181's best-threshold filtered Dice. The directional-lattice bridge did not recover the clean connected high-precision representation needed to make threshold tuning a compelling next focus.

## Failure-bucket observations

Failure buckets show that ABI-192's recall gain is paid for mostly by negative-patch clutter rather than a uniformly better positive-patch operating point:

1. Negative-patch clutter worsened. Among 2,003 negative validation patches, ABI-192 produced at least one filtered predicted-positive pixel on 1,345 patches. Median negative-patch false-positive count was 22 pixels. Total negative-patch false-positive pixels were 100,925, with 305 negative patches above 100 filtered false-positive pixels, 10 above 500, and none above 1,000. This is worse than ABI-181's 77,592 negative-patch false-positive pixels and much worse than ABI-184's 53,814, so the directional-lattice branch does not solve false-positive discipline.
2. Positive-patch severe misses are mixed. ABI-192 had 28 positive validation patches with zero filtered predicted-positive pixels, 180 positive patches below 0.1 filtered Dice, 242 below 0.2 filtered Dice, and 267 below 0.2 filtered recall. The zero-prediction count improves on ABI-181 and ABI-184, and ABI-192 improves the recall-tail counts versus ABI-184, but it is not consistently better than ABI-181 on low-Dice or low-recall positive patches.
3. Median positive-patch quality is encouraging but not enough to offset clutter. Median positive-patch filtered Dice was 0.4213, median precision 0.5000, and median recall 0.4333. By Dataset Source, median positive-patch filtered Dice was 0.3922 on MIT and 0.4682 on Google; median precision was 0.4538 on MIT and 0.5444 on Google; median recall was 0.3933 on MIT and 0.4779 on Google. These medians are stronger than ABI-181 on central positive-patch overlap/recall, but the low-quality tail and negative-patch false positives keep the aggregate metric below ABI-181.

Artifact Filters removed 40,376 predicted-positive pixels over the full split, corresponding to 161,504 square kilometers under the evaluation metadata's pixel-area accounting. Raw Dice was 0.4242 versus filtered Dice 0.4096; raw predicted-positive pixels were 677,134 versus 636,758 filtered. Filtering lowered Dice modestly, as in recent SZA-aware ASPP branches, and does not indicate primary Artifact Filter dependence.

The retained diagnostic sample GeoTIFFs are traceability artifacts selected under the bounded evaluation policy. This note does not reproduce individual scene identifiers, coordinates, raw samples, or images.

## Interpretation

Classify ABI-192's whole-validation evaluation as valid, finite, non-collapsed diagnostic evidence for the late-improving directional-lattice signed-detail full-scale skip ASPP branch. The late-improving budget was informative: ABI-192's final-epoch capped gain remained close on the full Working Validation Split and the branch became a plausible recall/positive-patch-median comparator.

However, ABI-192 should not replace ABI-181 or ABI-184 as the main references. ABI-181 remains the best whole-validation-tested aggregate filtered-Dice Result, while ABI-184 remains the best precision/connectivity and negative-patch discipline Result in this lineage. ABI-192 sits between them only on aggregate Dice and recall; it does not preserve ABI-184's connected-line behavior and it increases negative-patch clutter beyond ABI-181.

The directional-lattice mechanism is therefore not a hard failure, but the exact late36 branch is sufficiently characterized. Its remaining weakness is not another epoch-budget question; it is the same unresolved precision/connectivity/negative-clutter tradeoff seen throughout the signed-detail full-scale skip ASPP family.

## Decision

Do not promote ABI-192 or reinterpret this whole-validation diagnostic as deployment evidence. Retain ABI-181 as the whole-validation aggregate filtered-Dice reference and ABI-184 as the precision/connectivity and negative-patch-discipline reference.

Do not repeat ABI-192 unchanged, do not request another longer budget for the same exact branch, and do not continue the directional-lattice line as the next immediate local tweak. A reasonable next in-contract step is to broaden from this signed-detail/directional-lattice branch toward a different high-resolution line-aware architecture or a trusted data/loss/auxiliary policy probe that explicitly targets negative-patch clutter while preserving ABI-192's better positive-patch median recall. No Capability Request or Campaign Report is required from this diagnostic result.

## Artifact references

- `run_20260903_085513_f395ad/outputs/evaluations/eval_evalreq_abi192_wholeval_failure_buckets_v1/summary.json`
- `run_20260903_085513_f395ad/outputs/evaluations/eval_evalreq_abi192_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260903_085513_f395ad/outputs/evaluations/eval_evalreq_abi192_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260903_085513_f395ad/outputs/evaluations/eval_evalreq_abi192_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260903_085513_f395ad/outputs/evaluations/eval_evalreq_abi192_wholeval_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260903_085513_f395ad/outputs/best_metrics.json`
- `run_20260903_085513_f395ad/outputs/final_metrics.json`
- `run_20260903_085513_f395ad/outputs/metrics.jsonl`
- `run_20260903_085513_f395ad/outputs/resource_profile.json`
- `run_20260903_085513_f395ad/outputs/model_summary.json`
- `run_20260903_085513_f395ad/resolved_manifest.yaml`
- `run_20260903_085513_f395ad/candidate/budget_request.yaml`
- `run_20260903_075132_5cff8c/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
