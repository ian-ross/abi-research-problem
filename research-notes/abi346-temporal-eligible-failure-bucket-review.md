# ABI-346 temporal-eligible failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi346_temporal_eligible_failure_buckets_v1` for ABI-346 Run `run_20260918_152331_c80150`.

The evaluation asked whether ABI-346's three-frame temporal C4 connected-recall ladder recovered true positive-tail contrail evidence from the compact ABI-306 branch, or whether its additional fixed-threshold footprint mostly became negative-patch clutter, fragmented line pieces, source-specific noise, or threshold-fragile area growth. The evaluation population is the provider-owned temporal-eligible validation subset for offsets `[-1, 0, 1]` with 1,614 validation ABI Patches. Treat this as temporal-family diagnostic evidence only, not full Working Validation Split promotion evidence.

Primary comparison references:

- ABI-346 connected-recall ladder: Run `run_20260918_152331_c80150`, Evaluation `eval_evalreq_abi346_temporal_eligible_failure_buckets_v1`.
- ABI-306 compact high-precision temporal C4 line-state comparator: Run `run_20260914_124245_de843c`, Evaluation `eval_evalreq_abi306_temporal_eligible_failure_buckets_v1`.
- ABI-285 recall-heavy temporal C4 comparator: Run `run_20260913_100333_a250df`, Evaluation `eval_evalreq_abi285_temporal_eligible_failure_buckets_v1`.
- ABI-324 balanced five-frame temporal C4/detail-consensus comparator: Run `run_20260916_184108_954ec7`, Evaluation `eval_evalreq_abi324_temporal_eligible_failure_buckets_v1`.
- ABI-223 temporal-attention connectivity comparator: Run `run_20260908_154531_8c7e2b`, Evaluation `eval_evalreq_abi223_temporal_eligible_failure_buckets_v1`.
- ABI-344 five-frame broad recall-sidecar diagnostic: Run `run_20260918_105020_e806bb`, Evaluation `eval_evalreq_abi344_temporal_eligible_failure_buckets_v1`.

## Temporal-eligible aggregate metrics

At threshold 0.5 on 1,614 temporal-eligible validation ABI Patches, ABI-346 reached:

| Metric | ABI-346 temporal-eligible evaluation |
| --- | ---: |
| Filtered Dice | 0.4278 |
| MIT filtered Dice | 0.4080 |
| Google filtered Dice | 0.4805 |
| Filtered precision | 0.4611 |
| Filtered recall | 0.3991 |
| Filtered contrail connectivity | 0.2993 |
| Filtered predicted-positive pixels | 473,249 |
| Filtered true-positive pixels | 218,209 |
| Filtered false-positive pixels | 255,040 |
| Filtered false-negative pixels | 328,603 |
| Raw Dice | 0.4456 |

These values match ABI-346's selected epoch-23 checkpoint. The Result is finite, non-collapsed, and source-informative. Google remains stronger than MIT by about +0.0725 filtered Dice, but both Dataset Sources remain viable and neither shows catastrophic source-specific failure.

| Comparator | Filtered Dice | MIT Dice | Google Dice | Precision | Recall | Connectivity | Predicted-positive pixels |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ABI-346 connected-recall ladder | 0.4278 | 0.4080 | 0.4805 | 0.4611 | 0.3991 | 0.2993 | 473,249 |
| ABI-306 compact temporal C4 | 0.4225 | 0.4028 | 0.4762 | 0.4934 | 0.3695 | 0.2994 | 409,457 |
| ABI-285 recall-heavy temporal C4 | 0.4222 | 0.4008 | 0.4774 | 0.4484 | 0.3989 | 0.2434 | 486,427 |
| ABI-324 five-frame balanced C4 | 0.4294 | 0.4082 | 0.4872 | 0.4704 | 0.3950 | 0.3979 | 459,172 |
| ABI-223 temporal-attention | 0.4198 | 0.3985 | 0.4768 | 0.4838 | 0.3707 | 0.4124 | 419,056 |
| ABI-344 broad recall sidecar | 0.4264 | 0.4122 | 0.4626 | 0.4267 | 0.4262 | 0.3157 | 546,166 |

Relative to ABI-306, ABI-346 improves aggregate filtered Dice by +0.0053, MIT by +0.0052, Google by +0.0043, recall by +0.0296, and true-positive pixels by +16,174. The cost is -0.0323 precision, +47,618 false-positive pixels, and +63,792 predicted-positive pixels. Connectivity is essentially unchanged (-0.0001). This confirms the run note's provisional interpretation: the connected-recall ladder recovered area/recall evidence, but not connected-line continuity.

Relative to ABI-285, ABI-346 is a cleaner recall-heavy temporal C4 operating point: similar recall, higher filtered Dice, higher precision, much higher connectivity, and 13,178 fewer predicted-positive pixels. Relative to ABI-324, ABI-346 is close on aggregate and MIT Dice, but lower on Google Dice, precision, and especially connectivity. ABI-324 therefore remains the balanced temporal C4/detail-consensus comparator.

## Failure-bucket observations

Failure buckets show that ABI-346's extra footprint is not mostly negative-patch clutter, but the branch still does not solve connected-line continuity.

| Bucket metric | ABI-346 | ABI-306 | ABI-285 | ABI-324 | ABI-223 | ABI-344 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Positive samples | 719 | 719 | 719 | 719 | 719 | 719 |
| Complete positive misses (`true_positive_pixels == 0`) | 56 | 65 | 53 | 72 | 77 | 59 |
| Positive recall < 0.20 | 133 | 164 | 123 | 165 | 167 | 114 |
| Positive recall < 0.50 | 397 | 440 | 396 | 430 | 433 | 370 |
| Positive median recall | 0.4564 | 0.4111 | 0.4593 | 0.4231 | 0.4227 | 0.4887 |
| Positive median Dice | 0.4425 | 0.4348 | 0.4413 | 0.4265 | 0.4357 | 0.4345 |
| Positive median connectivity | 0.4197 | 0.4190 | 0.4291 | 0.4099 | 0.4226 | 0.4224 |
| Positive connectivity < 0.20 | 134 | 139 | 135 | 162 | 154 | 135 |
| Negative samples with any prediction | 700 | 703 | 795 | 533 | 515 | 671 |
| Negative samples >50 predicted pixels | 330 | 371 | 406 | 244 | 332 | 372 |
| Negative samples >200 predicted pixels | 64 | 33 | 51 | 44 | 53 | 80 |
| Total negative-patch predicted pixels | 56,477 | 49,513 | 61,780 | 40,097 | 51,290 | 66,687 |

The positive-tail signal is real. ABI-346 reduces ABI-306 complete misses by 9 patches and positive patches with recall below 0.20 by 31, while increasing positive median recall from 0.4111 to 0.4564. It nearly matches ABI-285's recall-tail behavior with better aggregate precision and connectivity. This supports retaining the compact-anchor-plus-bounded-recall-ladder idea as useful evidence, not dismissing it as a pure false-positive artifact.

The negative-patch clutter cost is moderate rather than dominant. ABI-346 touches nearly the same number of negative patches as ABI-306 (700 vs 703), reduces the number of negative patches above 50 pixels (330 vs 371), and remains cleaner than ABI-285/344 on total negative-patch burden. However, it does add 6,964 negative-patch predicted pixels over ABI-306 and doubles the count above 200 pixels (64 vs 33). The extra fixed-threshold area therefore includes both recovered true contrail evidence and a heavier high-tail clutter component.

Source buckets keep the usual Google-over-MIT pattern:

| Source bucket | MIT | Google |
| --- | ---: | ---: |
| Positive samples | 423 | 296 |
| Positive median recall | 0.4225 | 0.5080 |
| Positive median Dice | 0.4093 | 0.4894 |
| Positive median connectivity | 0.3784 | 0.4802 |
| Complete positive misses | 34 | 22 |
| Positive recall < 0.25 | 108 | 58 |
| Negative samples | 492 | 403 |
| Negative samples with any prediction | 378 | 322 |
| Negative samples >128 predicted pixels | 97 | 31 |
| Negative samples >512 predicted pixels | 8 | 0 |
| Total negative-patch predicted pixels | 38,010 | 18,467 |

The MIT side remains the harder residual failure mode. ABI-346's aggregate MIT Dice is competitive with ABI-324, but positive MIT medians and negative-patch heavy-tail clutter remain materially worse than Google.

Artifact Filters removed 37,729 predicted-positive pixels. Raw Dice was 0.4456 versus filtered Dice 0.4278, raw recall was 0.4310 versus filtered recall 0.3991, and raw predicted-positive pixels were 510,978 versus 473,249 filtered. Filtering lowers the metric rather than creating the Result, so ABI-346 is not an Artifact Filter-dependent success.

The retained diagnostic GeoTIFF samples and per-sample rows are bounded traceability artifacts selected by the Harness. This note does not reproduce raw samples, coordinates, scene identifiers, or images.

## Threshold behavior

The threshold sweep shows useful but not decisive low-threshold headroom:

| Threshold view | Threshold | Filtered Dice | Precision | Recall | Predicted-positive pixels |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best filtered Dice | 0.10 | 0.4366 | 0.4150 | 0.4607 | 607,068 |
| Near-balance reference | 0.20 | 0.4348 | 0.4356 | 0.4340 | 544,832 |
| Primary evaluation | 0.50 | 0.4278 | 0.4611 | 0.3991 | 473,249 |
| High-precision reference | 0.70 | 0.4214 | 0.4752 | 0.3785 | 435,532 |
| Very high threshold reference | 0.90 | 0.3933 | 0.5034 | 0.3227 | 350,453 |

The best diagnostic threshold improves filtered Dice by +0.0088 over the trusted fixed 0.5 threshold. This is less threshold headroom than ABI-306 (+0.0136) and ABI-223 (+0.0160), but more than ABI-324 (+0.0044) and ABI-344 (+0.0021). Architecturally, ABI-346 has remaining sub-threshold recall reserve, but the fixed-threshold operating point is not merely a calibration accident. This does not authorize Candidate-owned thresholding, calibration, postprocessing, metrics, losses, Artifact Filters, or validation selection.

## Interpretation

Classify ABI-346's temporal-eligible diagnostic as mixed-positive evidence for a three-frame temporal C4 connected-recall ladder, but negative evidence for this exact head as a connectivity solution.

The ladder succeeds at the narrow ABI-306 under-recall objective: it recovers true-positive pixels, lowers positive-patch complete misses, improves aggregate/source Dice, and avoids ABI-344-level broad clutter. The gain is not mostly Artifact Filter dependence and not mostly negative-patch clutter.

The key failure remains connected-line continuity. Aggregate connectivity is unchanged from ABI-306 and far below ABI-324 and ABI-223. Per-positive median connectivity is typical rather than improved, and the MIT positive-patch tail remains weak. The mechanism raises more contrail area to threshold 0.5, but it does not bind those positives into the continuous thin-line structures needed for a new connectivity comparator.

Comparator roles after this evaluation:

- ABI-324 remains the balanced temporal C4/detail-consensus comparator.
- ABI-306 remains the compact high-precision three-frame temporal C4 comparator.
- ABI-346 becomes useful positive evidence for a three-frame temporal C4 recall/aggregate trade-off and a potential design ingredient, but not a replacement comparator for ABI-324 or ABI-223.
- ABI-223 remains the temporal-attention connectivity comparator on the temporal-eligible validation population.
- ABI-344 remains a broad five-frame recall-sidecar diagnostic, not a comparator.

ABI-346 is temporal-eligible capped diagnostic evidence only. It must not be treated as whole-validation evidence against ABI-202 or ABI-249, and it does not justify Candidate-owned thresholding, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-346 and do not submit another unchanged late36 connected-recall ladder continuation. The diagnostic question is answered: the head can recover true-positive-tail evidence while keeping clutter below broader recall sidecars, but it does not add the connected-line mechanism needed to move beyond ABI-324/223.

Future work should be mechanism-changing. A defensible continuation would keep ABI-346's bounded recall recovery only if paired with an explicit connected-line continuity mechanism that protects ABI-306-style compactness, such as a stronger orientation-consensus bridge, temporal alignment/change evidence that lifts continuous center-frame line segments, or a temporal-attention anchor that raises true contrail logits before adding any recall residual. Simple ladder gain changes, another soft uncertainty-band reinjector, or another unchanged temporal C4 residual-recall head are not justified by this diagnostic.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260918_152331_c80150/outputs/evaluations/eval_evalreq_abi346_temporal_eligible_failure_buckets_v1/summary.json`
- `run_20260918_152331_c80150/outputs/evaluations/eval_evalreq_abi346_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260918_152331_c80150/outputs/evaluations/eval_evalreq_abi346_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260918_152331_c80150/outputs/evaluations/eval_evalreq_abi346_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260918_152331_c80150/outputs/best_metrics.json`
- `run_20260918_152331_c80150/outputs/final_metrics.json`
- `run_20260918_152331_c80150/outputs/metrics.jsonl`
- `run_20260918_152331_c80150/outputs/resource_profile.json`
- `run_20260918_152331_c80150/outputs/model_summary.json`
- `run_20260918_152331_c80150/resolved_manifest.yaml`
- `run_20260918_152331_c80150/candidate/budget_request.yaml`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260913_100333_a250df/outputs/evaluations/eval_evalreq_abi285_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260913_100333_a250df/outputs/evaluations/eval_evalreq_abi285_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260913_100333_a250df/outputs/evaluations/eval_evalreq_abi285_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260916_184108_954ec7/outputs/evaluations/eval_evalreq_abi324_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260916_184108_954ec7/outputs/evaluations/eval_evalreq_abi324_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260916_184108_954ec7/outputs/evaluations/eval_evalreq_abi324_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260918_105020_e806bb/outputs/evaluations/eval_evalreq_abi344_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `/history/research-notes/abi346-temporal-c4-connected-recall-ladder-late36.md`
- `/history/research-notes/abi306-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi324-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi344-temporal-fiveframe-connectivity-anchor-recall-sidecar-late36.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
