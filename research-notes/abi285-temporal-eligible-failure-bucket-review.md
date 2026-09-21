# ABI-285 temporal-eligible failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi285_temporal_eligible_failure_buckets_v1` for ABI-285 Run `run_20260913_100333_a250df`.

The evaluation asked whether ABI-285's late36 temporal C4 orientation line-state U-Net retained its selected epoch-32 temporal-eligible validation signal under failure-bucket and threshold diagnostics, and whether the branch's weak connected-line continuity was driven mainly by fragmented thin lines, broader negative-patch clutter, source-specific undercoverage, or Artifact Filter dependence. The evaluation population is the provider-owned temporal-eligible validation subset for offsets `[-1, 0, 1]` (1,614 ABI Patches), not the full 3,088-sample Working Validation Split; treat it as diagnostic temporal-family evidence only.

Primary comparison references:

- ABI-285 temporal C4 orientation line-state late36 U-Net: Run `run_20260913_100333_a250df`, Evaluation `eval_evalreq_abi285_temporal_eligible_failure_buckets_v1`.
- ABI-284 exploratory parent: Run `run_20260913_091156_167372`.
- ABI-274 temporal line-state attention U-Net late36 comparator: Run `run_20260912_180856_79ba22`, Evaluation `eval_evalreq_abi274_temporal_eligible_failure_buckets_v1`.
- ABI-223 temporal-attention fusion U-Net late36 comparator: Run `run_20260908_154531_8c7e2b`, Evaluation `eval_evalreq_abi223_temporal_eligible_failure_buckets_v1`.
- ABI-255 compact recurrent temporal late36 comparator: Run `run_20260911_210922_27f346`, Evaluation `eval_evalreq_abi255_temporal_eligible_failure_buckets_v1`.
- ABI-238 temporal directional-context late36 comparator: Run `run_20260911_004137_f54c45`.

## Temporal-eligible aggregate metrics

At threshold 0.5 on 1,614 temporal-eligible validation ABI Patches, ABI-285 reached:

| Metric | ABI-285 temporal-eligible evaluation |
| --- | ---: |
| Filtered Dice | 0.4222 |
| MIT filtered Dice | 0.4008 |
| Google filtered Dice | 0.4774 |
| Filtered precision | 0.4484 |
| Filtered recall | 0.3989 |
| Filtered contrail connectivity | 0.2434 |
| Filtered predicted-positive pixels | 486,427 |
| Filtered false-positive pixels | 268,313 |
| Filtered false-negative pixels | 328,698 |
| Raw Dice | 0.4394 |

These aggregate metrics match ABI-285's selected epoch-32 checkpoint. The Result is finite, non-collapsed, and source-informative. Google remains stronger than MIT by about +0.0766 filtered Dice, but both Dataset Sources remain viable and neither shows a catastrophic source-specific failure.

| Comparator | Filtered Dice | MIT Dice | Google Dice | Precision | Recall | Connectivity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| ABI-285 temporal C4 orientation line-state late36 | 0.4222 | 0.4008 | 0.4774 | 0.4484 | 0.3989 | 0.2434 |
| ABI-274 temporal line-state attention late36 | 0.4194 | 0.3994 | 0.4726 | 0.4541 | 0.3895 | 0.2829 |
| ABI-223 temporal-attention fusion late36 | 0.4198 | 0.3985 | 0.4768 | 0.4838 | 0.3707 | 0.4124 |
| ABI-255 compact recurrent temporal late36 | 0.4173 | 0.4008 | 0.4631 | 0.4683 | 0.3764 | 0.2811 |
| ABI-238 temporal directional-context late36 | 0.4202 | 0.4054 | 0.4608 | 0.4887 | 0.3686 | 0.3522 |

ABI-285 is the highest currently observed capped temporal-eligible aggregate filtered-Dice Result among these temporal comparators, narrowly above ABI-238, ABI-223, and ABI-274. It also has the highest filtered recall in this comparison set. The trade-off is clear: ABI-285 is lower on precision than ABI-223/238/255 and lower on connected-line continuity than every listed comparator.

## Threshold behavior

The threshold sweep shows only modest lower-threshold headroom:

| Threshold view | Threshold | Filtered Dice | Precision | Recall |
| --- | ---: | ---: | ---: | ---: |
| Primary evaluation | 0.50 | 0.4222 | 0.4484 | 0.3989 |
| Best filtered Dice | 0.10 | 0.4287 | 0.4051 | 0.4553 |
| Closest precision/recall balance | 0.20 | 0.4271 | 0.4239 | 0.4303 |

The best diagnostic threshold improves filtered Dice by about +0.0065 over the fixed 0.5 threshold. This is similar to ABI-274's small sweep headroom and much less than ABI-223's larger low-threshold recall reserve. This does not authorize Candidate-owned thresholding, calibration, postprocessing, metrics, losses, or Artifact Filters. The architecture lesson is that ABI-285 already raises more temporal evidence to the trusted threshold, but the extra evidence is not cleanly organized into continuous lines.

## Failure-bucket observations

Failure buckets clarify the operating point:

1. Negative-patch clutter is broader than ABI-223 and slightly broader than ABI-274. Among 895 negative temporal-eligible validation ABI Patches, ABI-285 produced at least one filtered false-positive pixel on 795 patches. Median negative-patch false-positive count was 46 pixels. Total negative-patch false-positive burden was 61,780 pixels, with 163 negative patches above 100 false-positive pixels, 9 above 500, and none above 1,000.
2. Positive-patch complete misses are low, and positive-patch coverage is better than ABI-223 and ABI-274 on several miss-tail counts. Among 719 positive temporal-eligible validation ABI Patches, 1 had zero filtered predicted-positive pixels, 79 had filtered Dice below 0.1, 124 had filtered Dice below 0.2, and 123 had filtered recall below 0.2. Median positive-patch filtered Dice was 0.4413, median precision 0.4713, median recall 0.4593, and median connectivity 0.4291.
3. Source-stratified positive-patch medians show the same Google-over-MIT pattern as the aggregate metrics. Positive Google patches had median filtered Dice 0.4861, precision 0.5219, recall 0.5149, and connectivity 0.4944. Positive MIT patches had median filtered Dice 0.4137, precision 0.4333, recall 0.4230, and connectivity 0.3889. The model is not source-collapsed, but MIT remains the harder source and contributes more of the undercoverage tail.
4. Connectivity remains the main scientific weakness. ABI-285 reduces complete positive misses and raises aggregate recall, but aggregate filtered connectivity is only 0.2434, far below ABI-223 (0.4124), ABI-238 (0.3522), ABI-274 (0.2829), and ABI-255 (0.2811). This is consistent with recall-heavy but fragmented or cluttered temporal evidence rather than absent temporal signal.

Artifact Filters removed 37,512 predicted-positive pixels over the temporal-eligible validation subset. Raw Dice was 0.4394 versus filtered Dice 0.4222, and raw predicted-positive pixels were 523,939 versus 486,427 filtered. Filtering lowers the metric rather than creating the Result, so ABI-285 is not excessively Artifact Filter-dependent. Removed pixels were concentrated on positive patches (33,302) rather than negative patches (4,210), so the filters are not hiding a large negative-patch clutter failure.

The retained diagnostic GeoTIFF samples and per-sample rows are traceability artifacts selected under the bounded evaluation policy. This note does not reproduce raw samples, coordinates, scene identifiers, or images.

## Interpretation

Classify ABI-285's temporal-eligible failure-bucket evaluation as valid, finite diagnostic evidence that the late temporal C4 orientation line-state branch improved temporal-family aggregate filtered Dice and fixed-threshold recall. It should replace ABI-274 as the capped temporal-eligible aggregate filtered-Dice comparator, while ABI-223 remains the cleaner temporal line-continuity comparator and ABI-238 remains a useful high-precision directional temporal comparator.

The same diagnostics answer the mechanism question negatively for connected thin-line continuity. ABI-285's advantage comes from fewer positive-patch misses and higher recall, especially on Google, but it also brings broader negative-patch clutter and the weakest aggregate connectivity among the listed temporal comparators. The C4/orientation line-state mechanism therefore appears to raise evidence presence more than evidence organization.

ABI-285 is not whole-validation promotion evidence. It is a temporal-eligible capped diagnostic Result and must not be compared as if it were a full Working Validation Split Result against ABI-202 or ABI-249.

## Decision

Do not promote ABI-285 and do not submit another unchanged late36 continuation of the ABI-284/285 temporal C4 orientation line-state branch. The late-budget and temporal-eligible diagnostic questions have both been answered: ABI-285 is a useful aggregate temporal comparator, but it did not solve connected thin-line continuity or negative-patch cleanliness.

Future temporal work should be mechanism-changing: preserve ABI-285's recall/source-balance gains while adding explicit architecture-level continuity support before logits reach the trusted threshold. In-contract directions include a center-frame detail bridge, an orientation-consensus/C4 continuity head with stricter evidence agreement, or a line-aware attention/recurrent state that supports connected thin lines without Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, or resource scheduling.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260913_100333_a250df/outputs/evaluations/eval_evalreq_abi285_temporal_eligible_failure_buckets_v1/summary.json`
- `run_20260913_100333_a250df/outputs/evaluations/eval_evalreq_abi285_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260913_100333_a250df/outputs/evaluations/eval_evalreq_abi285_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260913_100333_a250df/outputs/evaluations/eval_evalreq_abi285_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260913_100333_a250df/outputs/evaluations/eval_evalreq_abi285_temporal_eligible_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260913_100333_a250df/outputs/best_metrics.json`
- `run_20260913_100333_a250df/outputs/final_metrics.json`
- `run_20260913_100333_a250df/outputs/metrics.jsonl`
- `run_20260913_100333_a250df/outputs/resource_profile.json`
- `run_20260913_100333_a250df/outputs/model_summary.json`
- `run_20260913_100333_a250df/resolved_manifest.yaml`
- `run_20260913_100333_a250df/candidate/budget_request.yaml`
- `run_20260913_091156_167372/outputs/best_metrics.json`
- `run_20260912_180856_79ba22/outputs/evaluations/eval_evalreq_abi274_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260912_180856_79ba22/outputs/evaluations/eval_evalreq_abi274_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260912_180856_79ba22/outputs/evaluations/eval_evalreq_abi274_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260911_210922_27f346/outputs/evaluations/eval_evalreq_abi255_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260911_210922_27f346/outputs/best_metrics.json`
- `run_20260911_004137_f54c45/outputs/best_metrics.json`
- `/history/research-notes/abi285-temporal-c4-orientation-line-state-late36.md`
- `/history/research-notes/abi274-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
