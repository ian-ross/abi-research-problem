# ABI-309 temporal-eligible failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi309_temporal_eligible_failure_buckets_v1` for ABI-309 Run `run_20260914_205014_1794f8`.

The evaluation asked whether ABI-309's late36 temporal C4 late line-support recall-head U-Net represented useful true-contrail recovery over ABI-306, or whether the extra fixed-threshold positives were mostly negative-patch clutter, source-specific overprediction, and fragmented positive-patch behavior. The evaluation population is the provider-owned temporal-eligible validation subset for offsets `[-1, 0, 1]` (1,614 ABI Patches), not the full Working Validation Split; treat this as temporal-family diagnostic evidence only.

Primary comparison references:

- ABI-309 temporal C4 late line-support recall head late36: Run `run_20260914_205014_1794f8`, Evaluation `eval_evalreq_abi309_temporal_eligible_failure_buckets_v1`.
- ABI-306 temporal C4 dual-evidence recall-calibrated line-state late36 compact comparator: Run `run_20260914_124245_de843c`, Evaluation `eval_evalreq_abi306_temporal_eligible_failure_buckets_v1`.
- ABI-307 temporal C4 center-detail recall bridge late36: Run `run_20260914_151259_e64cba`, Evaluation `eval_evalreq_abi307_temporal_eligible_failure_buckets_v1`.
- ABI-285 temporal C4 orientation line-state late36 recall-heavy comparator: Run `run_20260913_100333_a250df`, Evaluation `eval_evalreq_abi285_temporal_eligible_failure_buckets_v1`.
- ABI-223 temporal-attention fusion late36 continuity comparator: Run `run_20260908_154531_8c7e2b`, Evaluation `eval_evalreq_abi223_temporal_eligible_failure_buckets_v1`.
- ABI-238 temporal directional-context late36 comparator: Run `run_20260911_004137_f54c45`.

## Temporal-eligible aggregate metrics

At threshold 0.5 on 1,614 temporal-eligible validation ABI Patches, ABI-309 reached:

| Metric | ABI-309 temporal-eligible evaluation |
| --- | ---: |
| Filtered Dice | 0.4235 |
| MIT filtered Dice | 0.4024 |
| Google filtered Dice | 0.4785 |
| Filtered precision | 0.4018 |
| Filtered recall | 0.4478 |
| Filtered contrail connectivity | 0.3161 |
| Filtered predicted-positive pixels | 609,361 |
| Filtered false-positive pixels | 364,516 |
| Filtered false-negative pixels | 301,967 |
| Raw Dice | 0.4390 |

These metrics match ABI-309's selected epoch-29 checkpoint. The Result is finite, non-collapsed, source-informative, and recall-heavy. It narrowly improves temporal-eligible filtered Dice over ABI-306 and ABI-285, but does so with the broadest filtered prediction footprint in this comparison set.

| Comparator | Filtered Dice | MIT Dice | Google Dice | Precision | Recall | Connectivity | Predicted-positive pixels |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ABI-309 late line-support recall head | 0.4235 | 0.4024 | 0.4785 | 0.4018 | 0.4478 | 0.3161 | 609,361 |
| ABI-306 compact dual-evidence line-state | 0.4225 | 0.4028 | 0.4762 | 0.4934 | 0.3695 | 0.2994 | 409,457 |
| ABI-307 center-detail bridge | 0.4205 | 0.4049 | 0.4607 | 0.4702 | 0.3803 | 0.3253 | 442,234 |
| ABI-285 recall-heavy orientation line-state | 0.4222 | 0.4008 | 0.4774 | 0.4484 | 0.3989 | 0.2434 | 486,427 |
| ABI-223 temporal-attention fusion | 0.4198 | 0.3985 | 0.4768 | 0.4838 | 0.3707 | 0.4124 | 419,056 |
| ABI-238 temporal directional context | 0.4202 | 0.4054 | 0.4608 | 0.4887 | 0.3686 | 0.3522 | 412,381 |

Relative to ABI-306, ABI-309 adds 42,810 true-positive pixels and removes the same number of false negatives, so the line-support recall head genuinely raises true contrail evidence across the fixed 0.5 threshold. That useful recovery is expensive: it also adds 157,094 false-positive pixels and expands the filtered prediction footprint by 199,904 pixels. Precision falls by about 0.092, while aggregate connectivity improves only +0.0167 and remains below ABI-307, ABI-238, and ABI-223.

The Dataset Source pattern is mixed rather than collapsed. ABI-309 slightly improves Google filtered Dice versus ABI-306 (+0.0024) and nearly ties MIT (-0.0003), but the operating point is materially less compact on both sources. It therefore does not replace ABI-306 as the compact high-precision temporal C4 comparator.

## Threshold behavior

The threshold sweep shows very little filtered-Dice headroom around the fixed threshold:

| Threshold view | Threshold | Filtered Dice | Precision | Recall | Predicted-positive pixels |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best filtered Dice | 0.30 | 0.4243 | 0.3867 | 0.4701 | 664,607 |
| Primary evaluation | 0.50 | 0.4235 | 0.4018 | 0.4478 | 609,361 |
| Higher precision reference | 0.70 | 0.4209 | 0.4167 | 0.4251 | 557,862 |
| Very high threshold reference | 0.90 | 0.4037 | 0.4526 | 0.3643 | 440,093 |

The best diagnostic threshold improves filtered Dice by only about +0.0008 over the trusted threshold 0.5. This differs from ABI-306's larger low-threshold reserve (+0.0136), and suggests ABI-309 already exposes most of its recall at the fixed threshold by broadening predictions rather than by retaining a clean calibration reserve. This does not authorize Candidate-owned thresholding, postprocessing, metrics, losses, Artifact Filters, or validation selection.

## Failure-bucket observations

Failure buckets answer the diagnostic question as positive but not clean:

1. Positive-patch recovery is real. Among 719 positive temporal-eligible validation ABI Patches, ABI-309 had 7 complete filtered misses, 77 positive patches with filtered Dice below 0.1, 128 below 0.2, and 110 with filtered recall below 0.2. These tail counts improve ABI-306's 8, 85, 130, and 164, and improve ABI-307's 10, 107, 153, and 168. Median positive-patch recall rises to 0.5132 versus ABI-306's 0.4111, and median positive-patch Dice edges up to 0.4405 versus ABI-306's 0.4348. The late line-support head is therefore not merely painting background; it does recover some missed true contrail pixels.
2. Negative-patch clutter substantially worsens. Among 895 negative temporal-eligible validation ABI Patches, ABI-309 produced at least one filtered false-positive pixel on 672 patches. This is fewer touched negative patches than ABI-306's 703, but the total negative-patch false-positive burden grows to 80,378 pixels versus ABI-306's 49,513 and ABI-285's 61,780. The heavy-tail clutter is worse: 252 negative patches exceed 100 false-positive pixels, 27 exceed 500, and 1 exceeds 1,000. ABI-306 had only 132, 3, and 0 in those buckets.
3. Positive-patch medians confirm the recall-for-precision trade. Median positive-patch precision drops to 0.4332 versus ABI-306's 0.5479, while median connectivity is essentially tied/slightly higher at 0.4213 versus 0.4190. The added positives therefore improve recall and slightly improve typical Dice, but they do not produce a broad continuity breakthrough.
4. Source-stratified positive medians keep the Google-over-MIT pattern. ABI-309's MIT positive-patch medians are Dice 0.4009, precision 0.3984, recall 0.4878, and connectivity 0.3784. Google medians are Dice 0.4997, precision 0.4703, recall 0.5772, and connectivity 0.4785. The source pattern is not degenerate, but MIT precision/quality remains weaker and the recall gain is achieved by broader low-precision predictions.
5. Artifact Filters do not create the Result. Filters removed 48,585 predicted-positive pixels overall, with 42,982 removed on positive patches and 5,603 on negative patches. Raw Dice was 0.4390 versus filtered Dice 0.4235, and raw predicted-positive pixels were 657,946 versus 609,361 filtered. Filtering lowers the score rather than hiding a failed raw operating point.

The retained diagnostic GeoTIFF samples and per-sample rows are bounded traceability artifacts selected by the Harness. This note does not reproduce raw samples, coordinates, scene identifiers, or images.

## Interpretation

Classify ABI-309's temporal-eligible failure-bucket evaluation as valid, finite positive/mixed evidence for the temporal C4 line-support branch. The line-support recall head genuinely repairs part of ABI-306's positive-patch under-recall tail and reaches the best filtered Dice in this temporal-eligible comparison set, but only by accepting a large false-positive and predicted-footprint cost.

The diagnostic outcome sharpens the branch roles:

- ABI-306 remains the compact high-precision temporal C4 comparator.
- ABI-307 remains evidence that center-detail support can add true positives but not selectively enough.
- ABI-308 remains high-connectivity/over-suppression evidence, not a frontier target.
- ABI-309 becomes the recall-support temporal C4 variant, not a clean comparator replacement.
- ABI-223 remains the temporal continuity comparator because ABI-309's connectivity is far lower despite its recall gain.

ABI-309 is temporal-eligible capped diagnostic evidence only. It must not be treated as whole-validation evidence against ABI-202 or ABI-249, and it does not justify Candidate-owned thresholding, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, or resource scheduling.

## Decision

Do not promote ABI-309 and do not submit another unchanged ABI-306/307/308/309 late36 continuation. The diagnostic question is answered: ABI-309's extra positives include useful true-contrail recovery, but the mechanism is too blunt because negative-patch false-positive burden and heavy-tail clutter rise sharply while connectivity remains below the better temporal continuity comparators.

Future temporal C4 work should be mechanism-changing and more selective: preserve ABI-306's compact high-precision mask evidence, then add ABI-309-style line-state support only where center-frame detail, temporal agreement, or orientation continuity supports connected true-contrail evidence. If that cannot be expressed within the Candidate Experiment Contract without candidate-owned thresholds or postprocessing, broaden to a different temporal attention or calibration-head family rather than continuing late line-support heads unchanged.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260914_205014_1794f8/outputs/evaluations/eval_evalreq_abi309_temporal_eligible_failure_buckets_v1/summary.json`
- `run_20260914_205014_1794f8/outputs/evaluations/eval_evalreq_abi309_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260914_205014_1794f8/outputs/evaluations/eval_evalreq_abi309_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260914_205014_1794f8/outputs/evaluations/eval_evalreq_abi309_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260914_205014_1794f8/outputs/evaluations/eval_evalreq_abi309_temporal_eligible_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260914_205014_1794f8/outputs/best_metrics.json`
- `run_20260914_205014_1794f8/outputs/final_metrics.json`
- `run_20260914_205014_1794f8/outputs/metrics.jsonl`
- `run_20260914_205014_1794f8/outputs/resource_profile.json`
- `run_20260914_205014_1794f8/outputs/model_summary.json`
- `run_20260914_205014_1794f8/resolved_manifest.yaml`
- `run_20260914_205014_1794f8/candidate/budget_request.yaml`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260914_151259_e64cba/outputs/evaluations/eval_evalreq_abi307_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260914_151259_e64cba/outputs/evaluations/eval_evalreq_abi307_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260913_100333_a250df/outputs/evaluations/eval_evalreq_abi285_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260913_100333_a250df/outputs/evaluations/eval_evalreq_abi285_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260911_004137_f54c45/outputs/best_metrics.json`
- `/history/research-notes/abi309-temporal-c4-late-line-support-recall-head-late36.md`
- `/history/research-notes/abi306-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi307-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi308-temporal-c4-selective-agreement-center-detail-late36.md`
- `/history/research-notes/abi285-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
