# ABI-307 temporal-eligible failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi307_temporal_eligible_failure_buckets_v1` for ABI-307 Run `run_20260914_151259_e64cba`.

The evaluation asked whether ABI-307's late36 temporal C4 center-detail recall-bridge U-Net genuinely repaired ABI-306's MIT positive-patch under-recall and fragmentation tail, or whether the added positives were mainly lower precision, broader footprint, Google regression, and negative-patch clutter. The evaluation population is the provider-owned temporal-eligible validation subset for offsets `[-1, 0, 1]` (1,614 ABI Patches), not the full 3,088-sample Working Validation Split; treat it as diagnostic temporal-family evidence only.

Primary comparison references:

- ABI-307 temporal C4 center-detail recall bridge late36: Run `run_20260914_151259_e64cba`, Evaluation `eval_evalreq_abi307_temporal_eligible_failure_buckets_v1`.
- ABI-306 temporal C4 dual-evidence recall-calibrated line-state late36 comparator: Run `run_20260914_124245_de843c`, Evaluation `eval_evalreq_abi306_temporal_eligible_failure_buckets_v1`.
- ABI-285 temporal C4 orientation line-state late36 recall-heavy comparator: Run `run_20260913_100333_a250df`, Evaluation `eval_evalreq_abi285_temporal_eligible_failure_buckets_v1`.
- ABI-223 temporal-attention fusion late36 continuity comparator: Run `run_20260908_154531_8c7e2b`, Evaluation `eval_evalreq_abi223_temporal_eligible_failure_buckets_v1`.
- ABI-238 temporal directional-context late36 comparator: Run `run_20260911_004137_f54c45`.

## Temporal-eligible aggregate metrics

At threshold 0.5 on 1,614 temporal-eligible validation ABI Patches, ABI-307 reached:

| Metric | ABI-307 temporal-eligible evaluation |
| --- | ---: |
| Filtered Dice | 0.4205 |
| MIT filtered Dice | 0.4049 |
| Google filtered Dice | 0.4607 |
| Filtered precision | 0.4702 |
| Filtered recall | 0.3803 |
| Filtered contrail connectivity | 0.3253 |
| Filtered predicted-positive pixels | 442,234 |
| Filtered false-positive pixels | 234,274 |
| Filtered false-negative pixels | 338,852 |
| Raw Dice | 0.4389 |

These metrics match ABI-307's selected epoch-36 checkpoint. The Result is finite, non-collapsed, and source-informative. Google remains stronger than MIT by about +0.0557 filtered Dice, and neither source is catastrophically failed, but the Google margin shrinks because Google regresses materially relative to ABI-306.

| Comparator | Filtered Dice | MIT Dice | Google Dice | Precision | Recall | Connectivity | Predicted-positive pixels |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ABI-306 temporal C4 dual-evidence line-state late36 | 0.4225 | 0.4028 | 0.4762 | 0.4934 | 0.3695 | 0.2994 | 409,457 |
| ABI-307 temporal C4 center-detail bridge late36 | 0.4205 | 0.4049 | 0.4607 | 0.4702 | 0.3803 | 0.3253 | 442,234 |
| ABI-285 temporal C4 orientation line-state late36 | 0.4222 | 0.4008 | 0.4774 | 0.4484 | 0.3989 | 0.2434 | 486,427 |
| ABI-223 temporal-attention fusion late36 | 0.4198 | 0.3985 | 0.4768 | 0.4838 | 0.3707 | 0.4124 | 419,056 |
| ABI-238 temporal directional-context late36 | 0.4202 | 0.4054 | 0.4608 | 0.4887 | 0.3686 | 0.3522 | 412,381 |

Relative to ABI-306, ABI-307 adds 5,925 true-positive pixels and reduces false negatives by the same amount, so the center-detail bridge did raise some true contrail evidence at threshold 0.5. However, it also adds 26,852 false-positive pixels and expands the filtered footprint by 32,777 pixels. This converts ABI-306's compact high-precision repair into a more recall-leaning operating point without recovering ABI-285's recall or ABI-223's continuity.

The most favorable ABI-307 aggregate change is MIT filtered Dice (+0.0022) and aggregate connectivity (+0.0259) versus ABI-306. The unfavorable changes are larger: filtered Dice -0.0020, precision -0.0232, and Google filtered Dice -0.0155. ABI-306 remains the capped temporal-eligible aggregate/precision C4 comparator; ABI-307 is mixed mechanism evidence rather than a comparator replacement.

## Threshold behavior

The threshold sweep shows low-threshold recall reserve but less useful headroom than ABI-306:

| Threshold view | Threshold | Filtered Dice | Precision | Recall | Predicted-positive pixels |
| --- | ---: | ---: | ---: | ---: | ---: |
| Primary evaluation | 0.50 | 0.4205 | 0.4702 | 0.3803 | 442,234 |
| Best filtered Dice | 0.10 | 0.4295 | 0.4180 | 0.4416 | 577,683 |
| Closest precision/recall balance | 0.15 | 0.4291 | 0.4341 | 0.4242 | 534,351 |

The best diagnostic threshold improves filtered Dice by about +0.0090 over the fixed 0.5 threshold. This is real calibration/evidence-sharpening headroom, but it is smaller than ABI-306's +0.0136 threshold-sweep headroom and does not authorize Candidate-owned thresholding, postprocessing, metrics, losses, or Artifact Filters. Architecturally, the center-detail bridge raises some evidence to 0.5, but the added evidence is not selective enough to improve the selected-threshold aggregate Result.

## Failure-bucket observations

Failure buckets answer the diagnostic question more negatively than the best-validation note alone implied:

1. Negative-patch clutter is not the main regression. Among 895 negative temporal-eligible validation ABI Patches, ABI-307 produced at least one filtered false-positive pixel on 649 patches. Median negative-patch false-positive count was 26 pixels. Total negative-patch false-positive burden was 46,353 pixels, with 146 negative patches above 100 false-positive pixels, 2 above 500, and none above 1,000. This is lower total negative-patch burden than ABI-306 (49,513) and ABI-285 (61,780), though still less clean than ABI-223 by the count of negative patches touched.
2. Positive-patch miss tails are worse than ABI-306 and ABI-285, not repaired. Among 719 positive temporal-eligible validation ABI Patches, ABI-307 had 10 complete filtered prediction misses, 107 positive patches with filtered Dice below 0.1, 153 below 0.2, and 168 with filtered recall below 0.2. ABI-306 had 8, 85, 130, and 164 on these same tail counts; ABI-285 had 1, 79, 124, and 123. The center-detail bridge therefore did not fix the positive-patch under-recall tail even though aggregate recall rose.
3. Positive-patch medians show a precision/typical-quality regression. Median positive-patch filtered Dice was 0.4206, precision 0.4957, recall 0.4179, and connectivity 0.4067. Versus ABI-306, median recall improves slightly (+0.0068), but median Dice (-0.0142), precision (-0.0522), and connectivity (-0.0123) fall. The aggregate connectivity gain is therefore likely concentrated in a subset of larger or higher-weight positive pixels rather than a broad repair of typical positive-patch continuity.
4. Source-stratified positive-patch medians keep the Google-over-MIT pattern but do not show a MIT-tail repair. MIT positive-patch median filtered Dice was 0.4053, precision 0.4785, recall 0.3864, and connectivity 0.3810, all slightly worse than ABI-306's MIT medians except for only negligible differences. Google positive-patch median Dice was 0.4593 and precision 0.5176, a clear drop from ABI-306's 0.4797 and 0.5910, while Google median recall rose to 0.4690. This is consistent with broader, less precise positive-patch predictions rather than selective connected recall.
5. Artifact Filters removed 35,384 predicted-positive pixels over the temporal-eligible validation subset, with 32,173 removed on positive patches and 3,211 on negative patches. Raw Dice was 0.4389 versus filtered Dice 0.4205, and raw predicted-positive pixels were 477,618 versus 442,234 filtered. Filtering lowers the score rather than creating the Result; ABI-307 is not excessively Artifact Filter-dependent.

The retained diagnostic GeoTIFF samples and per-sample rows are traceability artifacts selected under the bounded evaluation policy. This note does not reproduce raw samples, coordinates, scene identifiers, or images.

## Interpretation

Classify ABI-307's temporal-eligible failure-bucket evaluation as valid, finite diagnostic evidence that the center-detail bridge is only a partial and insufficient repair. It does raise aggregate recall and aggregate connectivity relative to ABI-306, and it slightly improves MIT aggregate filtered Dice. But the deeper bucket evidence shows the added detail path does not reduce the positive-patch miss/undercoverage tail; instead, it broadens predictions on positive patches, lowers precision, hurts Google, and degrades typical positive-patch Dice and connectivity.

This means ABI-307 should not replace ABI-306 as the compact high-precision temporal C4 comparator, should not replace ABI-285 as the recall-heavy temporal C4 comparator, and should not replace ABI-223 as the temporal connectivity comparator. It is useful primarily as a mechanism lesson: center-frame detail support can recover some true-positive pixels, but this residual bridge needs a stronger selectivity/consensus mechanism before it can improve fixed-threshold recall without reopening clutter and source-regression failure modes.

ABI-307 is temporal-eligible capped diagnostic evidence only. It must not be interpreted as full Working Validation Split evidence against ABI-202 or ABI-249.

## Decision

Do not promote ABI-307 and do not submit an unchanged ABI-307 late36 continuation. The diagnostic question is answered: the center-detail recall bridge's gains are not mostly negative-patch clutter, but they also are not a real repair of ABI-306's MIT positive-patch under-recall and fragmentation tail. The added positives are mainly a broader, less precise positive-patch operating point with Google regression.

Future temporal C4 work should be mechanism-changing and more selective: preserve ABI-306's compact precision and low negative-patch burden, then add connected-recall support through stronger orientation/temporal consensus, agreement-gated center detail, or evidence sharpening that raises true contrail logits to threshold 0.5 without Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, or resource scheduling.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260914_151259_e64cba/outputs/evaluations/eval_evalreq_abi307_temporal_eligible_failure_buckets_v1/summary.json`
- `run_20260914_151259_e64cba/outputs/evaluations/eval_evalreq_abi307_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260914_151259_e64cba/outputs/evaluations/eval_evalreq_abi307_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260914_151259_e64cba/outputs/evaluations/eval_evalreq_abi307_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260914_151259_e64cba/outputs/evaluations/eval_evalreq_abi307_temporal_eligible_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260914_151259_e64cba/outputs/best_metrics.json`
- `run_20260914_151259_e64cba/outputs/final_metrics.json`
- `run_20260914_151259_e64cba/outputs/metrics.jsonl`
- `run_20260914_151259_e64cba/outputs/resource_profile.json`
- `run_20260914_151259_e64cba/outputs/model_summary.json`
- `run_20260914_151259_e64cba/resolved_manifest.yaml`
- `run_20260914_151259_e64cba/candidate/budget_request.yaml`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260913_100333_a250df/outputs/evaluations/eval_evalreq_abi285_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260913_100333_a250df/outputs/evaluations/eval_evalreq_abi285_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260911_004137_f54c45/outputs/best_metrics.json`
- `/history/research-notes/abi307-temporal-c4-center-detail-recall-bridge-late36.md`
- `/history/research-notes/abi306-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi285-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
