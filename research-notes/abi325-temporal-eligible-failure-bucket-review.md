# ABI-325 temporal-eligible failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi325_temporal_eligible_failure_buckets_v1` for ABI-325 Run `run_20260916_212722_d66d93`.

The evaluation asked whether ABI-325's five-frame positive-tail evidence reinjector reduced positive-patch zero-TP or low-recall tails relative to ABI-324, ABI-311, ABI-306, ABI-309, and ABI-223, or whether the apparent recall/MIT gain mainly broadened the fixed-threshold footprint and shifted errors across Dataset Sources. The evaluation population is the provider-owned temporal-eligible validation subset for offsets `[-2, -1, 0, 1, 2]`, with 1,614 validation ABI Patches. Treat this as temporal-family diagnostic evidence only, not full Working Validation Split promotion evidence.

Primary comparison references:

- ABI-325 temporal five-frame positive-tail evidence reinjector late36: Run `run_20260916_212722_d66d93`, Evaluation `eval_evalreq_abi325_temporal_eligible_failure_buckets_v1`.
- ABI-324 temporal five-frame detail-consensus stabilized line-state late36: Run `run_20260916_184108_954ec7`, Evaluation `eval_evalreq_abi324_temporal_eligible_failure_buckets_v1`.
- ABI-311 five-frame temporal C4 persistence/contrast line-state late36 parent: Run `run_20260915_015552_1ac51f`, Evaluation `eval_evalreq_abi311_temporal_eligible_failure_buckets_v1`.
- ABI-306 compact temporal C4 dual-evidence line-state late36 comparator: Run `run_20260914_124245_de843c`, Evaluation `eval_evalreq_abi306_temporal_eligible_failure_buckets_v1`.
- ABI-309 recall-heavy temporal C4 late line-support head late36: Run `run_20260914_205014_1794f8`, Evaluation `eval_evalreq_abi309_temporal_eligible_failure_buckets_v1`.
- ABI-223 temporal-attention fusion late36 continuity comparator: Run `run_20260908_154531_8c7e2b`, Evaluation `eval_evalreq_abi223_temporal_eligible_failure_buckets_v1`.

## Temporal-eligible aggregate metrics

At threshold 0.5 on 1,614 temporal-eligible validation ABI Patches, ABI-325 reached:

| Metric | ABI-325 temporal-eligible evaluation |
| --- | ---: |
| Filtered Dice | 0.4277 |
| MIT filtered Dice | 0.4129 |
| Google filtered Dice | 0.4665 |
| Filtered precision | 0.4257 |
| Filtered recall | 0.4298 |
| Filtered contrail connectivity | 0.3275 |
| Filtered predicted-positive pixels | 552,142 |
| Filtered false-positive pixels | 317,106 |
| Filtered false-negative pixels | 311,776 |
| Raw Dice | 0.4445 |

These metrics match ABI-325's selected epoch-27 checkpoint. The Result is finite, non-collapsed, and source-informative. It confirms the run note's tradeoff: ABI-325 moved toward higher fixed-threshold recall and stronger MIT Dice than ABI-324, but with a much broader footprint, lower precision, lower Google Dice, and a large aggregate connectivity regression.

| Comparator | Filtered Dice | MIT Dice | Google Dice | Precision | Recall | Connectivity | Predicted-positive pixels |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ABI-325 positive-tail reinjector | 0.4277 | 0.4129 | 0.4665 | 0.4257 | 0.4298 | 0.3275 | 552,142 |
| ABI-324 detail-consensus stabilized line-state | 0.4294 | 0.4082 | 0.4872 | 0.4704 | 0.3950 | 0.3979 | 459,172 |
| ABI-311 five-frame persistence/contrast line-state | 0.4250 | 0.4038 | 0.4826 | 0.4597 | 0.3952 | 0.3667 | 470,049 |
| ABI-306 compact dual-evidence line-state | 0.4225 | 0.4028 | 0.4762 | 0.4934 | 0.3695 | 0.2994 | 409,457 |
| ABI-309 late line-support recall head | 0.4235 | 0.4024 | 0.4785 | 0.4018 | 0.4478 | 0.3161 | 609,361 |
| ABI-223 temporal-attention fusion | 0.4198 | 0.3985 | 0.4768 | 0.4838 | 0.3707 | 0.4124 | 419,056 |

Relative to ABI-324, ABI-325 gains +0.0348 recall and +0.0047 MIT Dice, but loses -0.0447 precision, -0.0207 Google Dice, -0.0705 aggregate connectivity, and adds 92,970 filtered predicted-positive pixels. Relative to ABI-311, ABI-325 improves aggregate Dice (+0.0027), MIT Dice (+0.0090), and recall (+0.0347), but again loses Google Dice, precision, and connectivity while adding 82,093 predicted-positive pixels. Relative to ABI-309, ABI-325 is less broad and more precise, but it still does not recover ABI-324's balance.

## Threshold behavior

The threshold sweep shows almost no diagnostic Dice headroom below the trusted fixed threshold:

| Threshold view | Threshold | Filtered Dice | Precision | Recall | Predicted-positive pixels |
| --- | ---: | ---: | ---: | ---: | ---: |
| Low-threshold recall reference | 0.05 | 0.3923 | 0.3017 | 0.5604 | 1,015,465 |
| Broad recall reference | 0.25 | 0.4275 | 0.3916 | 0.4705 | 656,870 |
| Best filtered Dice | 0.35 | 0.4286 | 0.4077 | 0.4518 | 606,000 |
| Primary evaluation | 0.50 | 0.4277 | 0.4257 | 0.4298 | 552,142 |
| High-precision reference | 0.70 | 0.4227 | 0.4492 | 0.3992 | 485,931 |
| Very high threshold reference | 0.90 | 0.3902 | 0.4910 | 0.3237 | 360,483 |

The best diagnostic threshold improves filtered Dice by only about +0.0008 over threshold 0.5, while requiring 53,858 additional predicted-positive pixels. ABI-325 therefore is not hiding a large clean calibration reserve. Its recall behavior is already expressed at the trusted fixed threshold, and lower thresholds mostly broaden the footprint. This does not authorize Candidate-owned thresholding, calibration, postprocessing, metrics, losses, validation selection, or Artifact Filters.

## Failure-bucket observations

Failure buckets answer the diagnostic question as genuinely positive for positive-patch undercoverage, but negative for overall operating-point quality:

1. Positive-patch tail repair is real versus ABI-324. Among 719 positive temporal-eligible validation ABI Patches, ABI-325 had 70 patches with zero filtered true-positive pixels, 8 with zero filtered predicted-positive pixels, 93 positive patches with filtered Dice below 0.1, 131 below 0.2, 131 with filtered recall below 0.2, and 156 with filtered recall below 0.25. ABI-324 had 72 zero-TP patches, 17 zero-predicted-positive patches, 100 Dice-below-0.1 patches, 150 Dice-below-0.2 patches, 165 recall-below-0.2 patches, and 207 recall-below-0.25 patches. The reinjector therefore did reduce the low-recall tail; the earlier recall/MIT gain was not only aggregate noise.
2. The repair is not as clean as ABI-309's blunt recall head on positive-tail counts. ABI-309 remained stronger on several positive recovery buckets, while ABI-325 keeps better precision and smaller footprint than ABI-309. This positions ABI-325 between ABI-324's balanced mode and ABI-309's broad recall mode rather than as a new balanced frontier.
3. Negative-patch clutter materially worsens versus ABI-324. Among 895 negative temporal-eligible validation ABI Patches, ABI-325 produced at least one filtered false-positive pixel on 651 patches, with median negative-patch false-positive count 32 pixels. Total negative-patch false-positive burden was 59,887 pixels, with 188 negative patches above 100 false-positive pixels, 12 above 500, and 1 above 1,000. ABI-324 had 533 touched negatives, median 7 pixels, 40,097 total negative false-positive pixels, 111 above 100, 7 above 500, and none above 1,000. This is the main cost of the reinjection mechanism.
4. Positive-patch medians confirm higher recall but lower precision. ABI-325 positive-patch median filtered Dice was 0.4419, precision 0.4527, recall 0.4839, and connectivity 0.4277. ABI-324's corresponding medians were Dice 0.4265, precision 0.5087, recall 0.4231, and connectivity 0.4099. The median positive-patch signal improved in Dice/recall/connectivity, but the precision drop and negative-patch clutter explain why aggregate connectivity and aggregate Dice do not improve.
5. Source-stratified positive medians keep the Google-over-MIT pattern but lift MIT recall. ABI-325 positive MIT patch medians were Dice 0.4098, precision 0.4150, recall 0.4490, and connectivity 0.3818. Positive Google patch medians were Dice 0.4871, precision 0.4880, recall 0.5184, and connectivity 0.4758. Compared with ABI-324, MIT median Dice and recall improve, but MIT precision falls and Google aggregate Dice regresses.
6. Artifact Filters do not create the Result, but the broader footprint increases filter interaction. Filters removed 44,305 predicted-positive pixels overall. Raw Dice was 0.4445 versus filtered Dice 0.4277, raw recall was 0.4646 versus filtered recall 0.4298, and raw predicted-positive pixels were 596,447 versus 552,142 filtered. Filtering lowers the score rather than hiding a failed raw operating point, but removed pixels exceed ABI-324's 37,212 because ABI-325 paints more broadly.

The retained diagnostic GeoTIFF samples and per-sample rows are bounded traceability artifacts selected by the Harness. This note does not reproduce raw samples, coordinates, scene identifiers, or images.

## Interpretation

Classify ABI-325's temporal-eligible failure-bucket evaluation as mixed evidence: positive for the narrow hypothesis that feature-level evidence reinjection can reduce positive-patch low-recall tails, but negative for the exact branch as a comparator or promotion path. The mechanism repaired some ABI-324 residual undercoverage, especially in MIT-positive median behavior, but it did so by shifting the operating point toward clutter and away from ABI-324's source balance and connected compactness.

The key lesson is that positive-tail support must be more selective. ABI-325 shows that useful true-contrail evidence exists in the skipped center/detail/line-state features, but an unrestricted residual reinjection is too blunt. Future work should either preserve ABI-324-like compactness while making the reinjection conditional on stronger line/temporal agreement, or broaden to a materially different temporal alignment/change or attention mechanism that raises connected true-positive evidence without painting negative patches.

Comparator roles after this evaluation:

- ABI-324 remains the local balanced temporal C4 aggregate/connectivity comparator.
- ABI-325 is a positive-tail repair diagnostic, not a new comparator or promotion candidate.
- ABI-306 remains the compact high-precision temporal C4 comparator.
- ABI-309 remains the recall-heavy broad-footprint temporal C4 diagnostic variant.
- ABI-223 remains the temporal-attention connectivity comparator.
- ABI-322 remains negative evidence for an unchanged ABI-311-style architecture trained with `bce_dice_cldice`.

ABI-325 is temporal-eligible capped diagnostic evidence only. It must not be treated as whole-validation evidence against ABI-202 or ABI-249, and it does not justify Candidate-owned thresholding, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, training loops, or prediction retention.

## Decision

Do not promote ABI-325 and do not submit another unchanged positive-tail reinjector continuation. The diagnostic question is answered: the mechanism can reduce low-recall positive-patch tails, but the branch is too blunt because negative-patch clutter, precision loss, source imbalance, and aggregate connectivity regression outweigh the repair.

A future Candidate should be mechanism-changing. Reasonable in-contract directions include a more selective ABI-324-style temporal C4 support path with explicit agreement/background guards, or a broader temporal alignment/change/attention architecture that targets connected true-positive evidence at threshold 0.5. The next hypothesis should preserve ABI-324's reduced negative-patch clutter and compact footprint while intentionally retaining ABI-325's positive-tail gains.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260916_212722_d66d93/outputs/evaluations/eval_evalreq_abi325_temporal_eligible_failure_buckets_v1/summary.json`
- `run_20260916_212722_d66d93/outputs/evaluations/eval_evalreq_abi325_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260916_212722_d66d93/outputs/evaluations/eval_evalreq_abi325_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260916_212722_d66d93/outputs/evaluations/eval_evalreq_abi325_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260916_212722_d66d93/outputs/evaluations/eval_evalreq_abi325_temporal_eligible_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260916_212722_d66d93/outputs/best_metrics.json`
- `run_20260916_212722_d66d93/outputs/final_metrics.json`
- `run_20260916_212722_d66d93/outputs/metrics.jsonl`
- `run_20260916_212722_d66d93/outputs/resource_profile.json`
- `run_20260916_212722_d66d93/outputs/model_summary.json`
- `run_20260916_212722_d66d93/resolved_manifest.yaml`
- `run_20260916_212722_d66d93/candidate/budget_request.yaml`
- `run_20260916_184108_954ec7/outputs/evaluations/eval_evalreq_abi324_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260916_184108_954ec7/outputs/evaluations/eval_evalreq_abi324_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260916_184108_954ec7/outputs/evaluations/eval_evalreq_abi324_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260915_015552_1ac51f/outputs/evaluations/eval_evalreq_abi311_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260915_015552_1ac51f/outputs/evaluations/eval_evalreq_abi311_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260915_015552_1ac51f/outputs/evaluations/eval_evalreq_abi311_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260914_124245_de843c/outputs/evaluations/eval_evalreq_abi306_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260914_205014_1794f8/outputs/evaluations/eval_evalreq_abi309_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260914_205014_1794f8/outputs/evaluations/eval_evalreq_abi309_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260914_205014_1794f8/outputs/evaluations/eval_evalreq_abi309_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `/history/research-notes/abi325-temporal-fiveframe-positive-tail-evidence-reinjector-late36.md`
- `/history/research-notes/abi324-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi311-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi306-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi309-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
