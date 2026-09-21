# ABI-311 temporal-eligible failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi311_temporal_eligible_failure_buckets_v1` for ABI-311 Run `run_20260915_015552_1ac51f`.

The evaluation asked whether ABI-311's five-frame temporal C4 persistence/contrast line-state U-Net converted its apparent capped gains over ABI-306, ABI-309, and ABI-310 into real connected true-contrail recovery, or whether the gains were mostly source/threshold noise, negative-patch clutter, or a broad false-positive tail. The evaluation population is the provider-owned temporal-eligible validation subset for offsets `[-2, -1, 0, 1, 2]` / temporal-eligible center selection, with 1,614 validation ABI Patches. Treat this as temporal-family diagnostic evidence only, not full Working Validation Split promotion evidence.

Primary comparison references:

- ABI-311 five-frame temporal C4 persistence/contrast line-state late36: Run `run_20260915_015552_1ac51f`, Evaluation `eval_evalreq_abi311_temporal_eligible_failure_buckets_v1`.
- ABI-306 compact temporal C4 dual-evidence line-state late36 comparator: Run `run_20260914_124245_de843c`, Evaluation `eval_evalreq_abi306_temporal_eligible_failure_buckets_v1`.
- ABI-307 temporal C4 center-detail recall bridge late36: Run `run_20260914_151259_e64cba`, Evaluation `eval_evalreq_abi307_temporal_eligible_failure_buckets_v1`.
- ABI-309 recall-heavy temporal C4 late line-support head late36: Run `run_20260914_205014_1794f8`, Evaluation `eval_evalreq_abi309_temporal_eligible_failure_buckets_v1`.
- ABI-310 agreement-gated temporal C4 line-support late36: Run `run_20260914_232554_0320e8`.
- ABI-223 temporal-attention fusion late36 continuity comparator: Run `run_20260908_154531_8c7e2b`, Evaluation `eval_evalreq_abi223_temporal_eligible_failure_buckets_v1`.
- ABI-238 temporal directional-context late36 comparator: Run `run_20260911_004137_f54c45`.

## Temporal-eligible aggregate metrics

At threshold 0.5 on 1,614 temporal-eligible validation ABI Patches, ABI-311 reached:

| Metric | ABI-311 temporal-eligible evaluation |
| --- | ---: |
| Filtered Dice | 0.4250 |
| MIT filtered Dice | 0.4038 |
| Google filtered Dice | 0.4826 |
| Filtered precision | 0.4597 |
| Filtered recall | 0.3952 |
| Filtered contrail connectivity | 0.3667 |
| Filtered predicted-positive pixels | 470,049 |
| Filtered false-positive pixels | 253,966 |
| Filtered false-negative pixels | 330,729 |
| Raw Dice | 0.4427 |

These metrics match ABI-311's selected epoch-27 checkpoint. The Result is finite, non-collapsed, and source-informative. Google remains stronger than MIT by about +0.0788 filtered Dice; neither source is catastrophically failed, but the source gap remains material.

| Comparator | Filtered Dice | MIT Dice | Google Dice | Precision | Recall | Connectivity | Predicted-positive pixels |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ABI-311 five-frame persistence/contrast line-state | 0.4250 | 0.4038 | 0.4826 | 0.4597 | 0.3952 | 0.3667 | 470,049 |
| ABI-306 compact dual-evidence line-state | 0.4225 | 0.4028 | 0.4762 | 0.4934 | 0.3695 | 0.2994 | 409,457 |
| ABI-307 center-detail recall bridge | 0.4205 | 0.4049 | 0.4607 | 0.4702 | 0.3803 | 0.3253 | 442,234 |
| ABI-309 late line-support recall head | 0.4235 | 0.4024 | 0.4785 | 0.4018 | 0.4478 | 0.3161 | 609,361 |
| ABI-310 agreement-gated line support | 0.4175 | 0.4034 | 0.4536 | 0.4385 | 0.3985 | 0.2848 | 496,940 |
| ABI-223 temporal-attention fusion | 0.4198 | 0.3985 | 0.4768 | 0.4838 | 0.3707 | 0.4124 | 419,056 |
| ABI-238 temporal directional context | 0.4202 | 0.4054 | 0.4608 | 0.4887 | 0.3686 | 0.3522 | 412,381 |

ABI-311 remains the strongest capped temporal-eligible aggregate score among these temporal comparators. Relative to ABI-306, it gains +0.0025 filtered Dice, +0.0257 recall, +0.0674 aggregate connectivity, and +0.0065 Google filtered Dice while spending 60,592 additional filtered predicted-positive pixels and giving up 0.0337 precision. Relative to ABI-309, ABI-311 gives up 0.0526 recall but recovers 0.0579 precision, reduces the filtered footprint by 139,312 pixels, reduces false-positive burden by 110,550 pixels, and improves aggregate connectivity by 0.0507. This supports the original interpretation that ABI-311 is a more balanced persistence/contrast mechanism rather than another broad recall head.

## Threshold behavior

The threshold sweep shows moderate but not decisive low-threshold headroom:

| Threshold view | Threshold | Filtered Dice | Precision | Recall | Predicted-positive pixels |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best filtered Dice | 0.15 | 0.4316 | 0.4186 | 0.4455 | 581,999 |
| Closest precision/recall balance | 0.20 | 0.4312 | 0.4293 | 0.4331 | 551,561 |
| Primary evaluation | 0.50 | 0.4250 | 0.4597 | 0.3952 | 470,049 |
| High-precision reference | 0.80 | 0.4091 | 0.4907 | 0.3508 | 390,909 |
| Very high threshold reference | 0.95 | 0.3351 | 0.5499 | 0.2410 | 239,682 |

The best diagnostic threshold improves filtered Dice by about +0.0066 over the fixed 0.5 threshold. That is smaller than ABI-306's +0.0136 reserve and much larger than ABI-309's near-flat +0.0008 reserve. Architecturally, ABI-311 has some lower-confidence recall available, but the fixed threshold is not wildly miscalibrated: the closest precision/recall balance at 0.20 is only +0.0062 filtered Dice above the trusted threshold. This does not authorize Candidate-owned thresholding, calibration, postprocessing, metrics, losses, or Artifact Filters.

## Failure-bucket observations

Failure buckets answer the diagnostic question as mostly positive for aggregate/clutter balance, but weaker for typical positive-patch repair:

1. Negative-patch clutter is cleaner than the recent temporal C4 comparators. Among 895 negative temporal-eligible validation ABI Patches, ABI-311 produced at least one filtered false-positive pixel on 584 patches. Median negative-patch false-positive count was 17 pixels. Total negative-patch false-positive burden was 45,001 pixels, with 133 negative patches above 100 false-positive pixels, 7 above 500, and none above 1,000. This is lower total negative-patch burden than ABI-306 (49,513), ABI-307 (46,353), and ABI-309 (80,378), and far cleaner than ABI-309's heavy-tail clutter. It touches more negative patches than ABI-223 (515), but with the same median false-positive count and without >1,000-pixel failures.
2. Positive-patch complete misses and undercoverage are not broadly repaired. Among 719 positive temporal-eligible validation ABI Patches, ABI-311 had 70 complete true-positive misses and 194 patches with filtered recall below 0.25. That is better than ABI-223 on complete misses (77) and ABI-306 on under-recall below 0.25 (209), but worse than ABI-309's 53 complete misses and 128 low-recall patches. The five-frame stem therefore improves balanced aggregate evidence without becoming the recall-tail repair that ABI-309 provided.
3. Positive-patch medians are mixed. Median positive-patch filtered Dice was 0.4215, precision 0.4980, recall 0.4313, and connectivity 0.4147. Compared with ABI-306, ABI-311 raises median recall (+0.0201) but lowers median Dice (-0.0132), precision (-0.0499), and slightly lowers median connectivity (-0.0043). Compared with ABI-309, ABI-311 is much more precise but lower in median recall and slightly lower in median positive-patch Dice/connectivity. Thus the aggregate connectivity gain is not a uniform typical-patch continuity repair; it is likely concentrated in a subset of higher-weight or larger connected structures.
4. Source-stratified positive-patch medians show that Google benefits more than MIT. Positive Google patches had median filtered Dice 0.4892, precision 0.5649, recall 0.4775, and connectivity 0.4733. Positive MIT patches had median filtered Dice 0.3914, precision 0.4474, recall 0.3915, and connectivity 0.3672. The Google median quality is competitive with or above recent temporal C4 comparators, but the MIT median remains below ABI-306/307 on Dice and below ABI-306 on connectivity. The remaining failure mode is a MIT-heavy positive-patch undercoverage/quality tail rather than general source collapse.
5. Artifact Filters do not create the Result. Filters removed 37,553 predicted-positive pixels overall. Raw Dice was 0.4427 versus filtered Dice 0.4250, raw recall was 0.4268 versus filtered recall 0.3952, and raw predicted-positive pixels were 507,602 versus 470,049 filtered. Filtering lowers the score rather than hiding a failed raw operating point.

The retained diagnostic GeoTIFF samples and per-sample rows are bounded traceability artifacts selected by the Harness. This note does not reproduce raw samples, coordinates, scene identifiers, or images.

## Interpretation

Classify ABI-311's temporal-eligible failure-bucket evaluation as valid, finite positive/mixed evidence for five-frame temporal C4 persistence/contrast. The key positive result is that ABI-311 improves the temporal C4 aggregate/connectivity operating point while reducing negative-patch clutter relative to the broad recall ABI-309 branch. Its gain is not mostly Artifact Filter dependence, not a broad negative-patch false-positive tail, and not pure threshold noise.

The caveat is that ABI-311 does not solve the positive-patch tail. Typical positive-patch Dice/connectivity do not clearly beat ABI-306 or ABI-309, and MIT positive-patch medians remain weak. The branch therefore should be treated as the best balanced temporal C4 comparator, not as a promotion candidate or an answered continuity solution.

Comparator roles after this evaluation:

- ABI-306 remains the compact high-precision temporal C4 comparator.
- ABI-309 remains the recall-heavy temporal C4 diagnostic variant, with known false-positive/heavy-tail cost.
- ABI-310 remains a negative/mixed agreement-gated interpolation.
- ABI-311 becomes the local balanced five-frame persistence/contrast temporal C4 comparator.
- ABI-223 remains the stronger temporal-attention continuity comparator because its aggregate connectivity remains higher, despite ABI-311's higher filtered Dice.

ABI-311 is temporal-eligible capped diagnostic evidence only. It must not be treated as whole-validation evidence against ABI-202 or ABI-249, and it does not justify Candidate-owned thresholding, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, or resource scheduling.

## Decision

Do not promote ABI-311 and do not submit an unchanged ABI-311 late36 continuation. The diagnostic question supports continuing the family only with a mechanism-changing hypothesis: preserve ABI-311's five-frame persistence/contrast balance and low negative-patch clutter, then specifically repair MIT/positive-patch undercoverage and typical connected-line continuity.

A future in-contract Candidate could test a selective stabilization/calibration mechanism for ABI-311-style evidence, such as a center-frame detail and temporal-consensus gate that raises connected true contrail logits only where persistence/contrast and orientation support agree. It should not add Candidate-owned thresholds, postprocessing, new losses, metrics, Artifact Filters, temporal lookup, sample selection, coordinates, or resource scheduling. If the next proposal cannot explicitly target the positive-patch tail while preserving the negative-patch clutter gain, broaden away from temporal C4 head/stem variants.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260915_015552_1ac51f/outputs/evaluations/eval_evalreq_abi311_temporal_eligible_failure_buckets_v1/summary.json`
- `run_20260915_015552_1ac51f/outputs/evaluations/eval_evalreq_abi311_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260915_015552_1ac51f/outputs/evaluations/eval_evalreq_abi311_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260915_015552_1ac51f/outputs/evaluations/eval_evalreq_abi311_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260915_015552_1ac51f/outputs/evaluations/eval_evalreq_abi311_temporal_eligible_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260915_015552_1ac51f/outputs/best_metrics.json`
- `run_20260915_015552_1ac51f/outputs/final_metrics.json`
- `run_20260915_015552_1ac51f/outputs/metrics.jsonl`
- `run_20260915_015552_1ac51f/outputs/resource_profile.json`
- `run_20260915_015552_1ac51f/outputs/model_summary.json`
- `run_20260915_015552_1ac51f/resolved_manifest.yaml`
- `run_20260915_015552_1ac51f/candidate/budget_request.yaml`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260914_151259_e64cba/outputs/evaluations/eval_evalreq_abi307_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260914_151259_e64cba/outputs/evaluations/eval_evalreq_abi307_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260914_205014_1794f8/outputs/evaluations/eval_evalreq_abi309_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260914_205014_1794f8/outputs/evaluations/eval_evalreq_abi309_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260914_205014_1794f8/outputs/evaluations/eval_evalreq_abi309_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260914_232554_0320e8/outputs/best_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260911_004137_f54c45/outputs/best_metrics.json`
- `/history/research-notes/abi311-temporal-fiveframe-c4-persistence-contrast-line-state-late36.md`
- `/history/research-notes/abi306-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi307-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi309-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi310-temporal-c4-agreement-gated-line-support-late36.md`
- `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
