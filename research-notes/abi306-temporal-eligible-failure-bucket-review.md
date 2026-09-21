# ABI-306 temporal-eligible failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi306_temporal_eligible_failure_buckets_v1` for ABI-306 Run `run_20260914_124245_de843c`.

The evaluation asked whether ABI-306's late36 temporal C4 dual-evidence recall-calibrated line-state U-Net retained its selected epoch-36 temporal-eligible validation signal under failure-bucket and threshold diagnostics, and whether the branch repaired ABI-285 mainly through reduced negative-patch clutter, fewer fragmented positive-patch predictions, reduced Artifact Filter dependence, or a compact under-recall shift. The evaluation population is the provider-owned temporal-eligible validation subset for offsets `[-1, 0, 1]` (1,614 ABI Patches), not the full 3,088-sample Working Validation Split; treat it as diagnostic temporal-family evidence only.

Primary comparison references:

- ABI-306 temporal C4 dual-evidence recall-calibrated line-state late36 U-Net: Run `run_20260914_124245_de843c`, Evaluation `eval_evalreq_abi306_temporal_eligible_failure_buckets_v1`.
- ABI-305 exploratory parent: Run `run_20260914_115424_977db1`.
- ABI-285 temporal C4 orientation line-state late36 comparator: Run `run_20260913_100333_a250df`, Evaluation `eval_evalreq_abi285_temporal_eligible_failure_buckets_v1`.
- ABI-274 temporal line-state attention late36 comparator: Run `run_20260912_180856_79ba22`, Evaluation `eval_evalreq_abi274_temporal_eligible_failure_buckets_v1`.
- ABI-223 temporal-attention fusion late36 comparator: Run `run_20260908_154531_8c7e2b`, Evaluation `eval_evalreq_abi223_temporal_eligible_failure_buckets_v1`.
- ABI-255 compact recurrent temporal late36 comparator: Run `run_20260911_210922_27f346`, Evaluation `eval_evalreq_abi255_temporal_eligible_failure_buckets_v1`.
- ABI-238 temporal directional-context late36 comparator: Run `run_20260911_004137_f54c45`.

## Temporal-eligible aggregate metrics

At threshold 0.5 on 1,614 temporal-eligible validation ABI Patches, ABI-306 reached:

| Metric | ABI-306 temporal-eligible evaluation |
| --- | ---: |
| Filtered Dice | 0.4225 |
| MIT filtered Dice | 0.4028 |
| Google filtered Dice | 0.4762 |
| Filtered precision | 0.4934 |
| Filtered recall | 0.3695 |
| Filtered contrail connectivity | 0.2994 |
| Filtered predicted-positive pixels | 409,457 |
| Filtered false-positive pixels | 207,422 |
| Filtered false-negative pixels | 344,777 |
| Raw Dice | 0.4414 |

These metrics match ABI-306's selected epoch-36 checkpoint. The Result is finite, non-collapsed, and source-informative. Google remains stronger than MIT by about +0.0734 filtered Dice, but both Dataset Sources remain viable and neither shows a catastrophic source-specific failure.

| Comparator | Filtered Dice | MIT Dice | Google Dice | Precision | Recall | Connectivity | Predicted-positive pixels |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ABI-306 temporal C4 dual-evidence line-state late36 | 0.4225 | 0.4028 | 0.4762 | 0.4934 | 0.3695 | 0.2994 | 409,457 |
| ABI-285 temporal C4 orientation line-state late36 | 0.4222 | 0.4008 | 0.4774 | 0.4484 | 0.3989 | 0.2434 | 486,427 |
| ABI-274 temporal line-state attention late36 | 0.4194 | 0.3994 | 0.4726 | 0.4541 | 0.3895 | 0.2829 | 469,049 |
| ABI-223 temporal-attention fusion late36 | 0.4198 | 0.3985 | 0.4768 | 0.4838 | 0.3707 | 0.4124 | 419,056 |
| ABI-255 compact recurrent temporal late36 | 0.4173 | 0.4008 | 0.4631 | 0.4683 | 0.3764 | 0.2811 | 439,511 |
| ABI-238 temporal directional-context late36 | 0.4202 | 0.4054 | 0.4608 | 0.4887 | 0.3686 | 0.3522 | 412,381 |

ABI-306 narrowly becomes the highest capped temporal-eligible filtered-Dice Result in this comparison set, but only by +0.0004 over ABI-285. Its real distinction is a much cleaner operating point: precision rises by about +0.045 versus ABI-285, predicted-positive area drops by 76,970 pixels, and aggregate connectivity improves by about +0.056. The cost is lower recall than ABI-285, ABI-274, and ABI-255, with recall roughly tied to ABI-223/238.

## Threshold behavior

The threshold sweep shows modest low-threshold recall reserve:

| Threshold view | Threshold | Filtered Dice | Precision | Recall |
| --- | ---: | ---: | ---: | ---: |
| Primary evaluation | 0.50 | 0.4225 | 0.4934 | 0.3695 |
| Best filtered Dice | 0.10 | 0.4362 | 0.4476 | 0.4253 |
| Closest precision/recall balance | 0.15 | 0.4341 | 0.4617 | 0.4096 |

The best diagnostic threshold improves filtered Dice by about +0.0136 over the fixed 0.5 threshold. This is larger headroom than ABI-285's +0.0065 but still not a license for Candidate-owned thresholding, calibration, postprocessing, metrics, losses, or Artifact Filters. Architecturally, ABI-306 appears to have latent recall below the trusted threshold; future work should raise connected true-contrail evidence to 0.5 without reintroducing ABI-285's broader clutter.

## Failure-bucket observations

Failure buckets clarify the operating point:

1. Negative-patch clutter is materially lower than ABI-285. Among 895 negative temporal-eligible validation ABI Patches, ABI-306 produced at least one filtered false-positive pixel on 703 patches. Median negative-patch false-positive count was 40 pixels. Total negative-patch false-positive burden was 49,513 pixels, with 132 negative patches above 100 false-positive pixels, 3 above 500, and none above 1,000. ABI-285 had 795 negative patches with predictions and 61,780 negative-patch false-positive pixels, so ABI-306 is a genuine clutter/precision repair.
2. Positive-patch complete misses are worse than ABI-285, but the positive-patch median remains usable. Among 719 positive temporal-eligible validation ABI Patches, 8 had zero filtered predicted-positive pixels, 85 had filtered Dice below 0.1, 130 had filtered Dice below 0.2, and 164 had filtered recall below 0.2. Median positive-patch filtered Dice was 0.4348, median precision 0.5479, median recall 0.4111, and median connectivity 0.4190. This confirms that the precision repair came with an under-recall tail.
3. Source-stratified positive-patch medians preserve the same Google-over-MIT pattern as the aggregate metrics. Positive Google patches had median filtered Dice 0.4798, precision 0.5911, recall 0.4531, and connectivity 0.4659. Positive MIT patches had median filtered Dice 0.4065, precision 0.5222, recall 0.3896, and connectivity 0.3856. The branch is not source-collapsed, but MIT continues to carry the harder undercoverage tail.
4. Connectivity improves over ABI-285/274/255 but remains below the strongest temporal continuity comparators. ABI-306's aggregate filtered connectivity is 0.2994, above ABI-285 (0.2434), ABI-274 (0.2829), and ABI-255 (0.2811), but still below ABI-238 (0.3522) and far below ABI-223 (0.4124). The dual-evidence line-state mechanism made predictions more compact and somewhat better connected than ABI-285, but it did not solve connected thin-line continuity.

Artifact Filters removed 32,556 predicted-positive pixels over the temporal-eligible validation subset. Raw Dice was 0.4414 versus filtered Dice 0.4225, and raw predicted-positive pixels were 442,013 versus 409,457 filtered. Filtering lowers the metric rather than creating the Result, so ABI-306 is not excessively Artifact Filter-dependent. Removed pixels were concentrated on positive patches (28,937) rather than negative patches (3,619), so the filters are not hiding a large negative-patch clutter failure.

The retained diagnostic GeoTIFF samples and per-sample rows are traceability artifacts selected under the bounded evaluation policy. This note does not reproduce raw samples, coordinates, scene identifiers, or images.

## Interpretation

Classify ABI-306's temporal-eligible failure-bucket evaluation as valid, finite diagnostic evidence for a compact high-precision temporal C4 line-state repair. ABI-306 should replace ABI-285 as the capped temporal-eligible aggregate/precision C4 comparator because it very slightly improves aggregate filtered Dice while substantially reducing predicted-positive area and negative-patch clutter.

The mechanism question is answered: ABI-306's gain is not a recall breakthrough. It trades ABI-285's recall-heavy, cluttered signal for a cleaner compact signal with better precision and moderate connectivity recovery. This is scientifically useful, but the remaining under-recall tail and lower connectivity than ABI-223/238 mean it is not a promotion candidate and not a whole-validation claim.

ABI-306 is temporal-eligible capped diagnostic evidence only. It must not be compared as though it were a full Working Validation Split Result against ABI-202 or ABI-249.

## Decision

Do not submit another unchanged late36 continuation of the ABI-305/306 temporal C4 dual-evidence line-state branch. The late-budget and temporal-eligible diagnostic questions have both been answered: ABI-306 is a useful compact high-precision temporal C4 comparator, but it did not recover enough fixed-threshold recall or connected-line continuity to be a frontier promotion candidate.

Future work should be mechanism-changing: preserve ABI-306's compact precision and lower clutter while adding architecture-level connected-recall support. In-contract directions include a temporal detail/recall bypass gated by center-frame evidence, an orientation-consensus continuity head that raises connected true positives instead of merely suppressing positives, or a temporal attention/recurrent line state with explicit support for missed MIT positive-patch tails. Do not use Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, or resource scheduling.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/summary.json`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260914_124245_de843c/outputs/best_metrics.json`
- `run_20260914_124245_de843c/outputs/final_metrics.json`
- `run_20260914_124245_de843c/outputs/metrics.jsonl`
- `run_20260914_124245_de843c/outputs/resource_profile.json`
- `run_20260914_124245_de843c/outputs/model_summary.json`
- `run_20260914_124245_de843c/resolved_manifest.yaml`
- `run_20260914_124245_de843c/candidate/budget_request.yaml`
- `run_20260914_115424_977db1/outputs/best_metrics.json`
- `run_20260913_100333_a250df/outputs/evaluations/eval_evalreq_abi285_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260913_100333_a250df/outputs/evaluations/eval_evalreq_abi285_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260913_100333_a250df/outputs/evaluations/eval_evalreq_abi285_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260912_180856_79ba22/outputs/evaluations/eval_evalreq_abi274_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260911_210922_27f346/outputs/evaluations/eval_evalreq_abi255_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260911_004137_f54c45/outputs/best_metrics.json`
- `/history/research-notes/abi306-temporal-c4-dual-evidence-recall-calibrated-line-state-late36.md`
- `/history/research-notes/abi285-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
