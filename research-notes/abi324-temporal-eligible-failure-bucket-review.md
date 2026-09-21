# ABI-324 temporal-eligible failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi324_temporal_eligible_failure_buckets_v1` for ABI-324 Run `run_20260916_184108_954ec7`.

The evaluation asked whether ABI-324's late36 five-frame temporal detail-consensus stabilized C4 line-state U-Net converted its selected epoch-27 improvement over ABI-311 into real connected true-contrail recovery and cleaner fixed-threshold evidence, or whether the gain was mostly checkpoint noise, source-specific behavior, negative-patch clutter, positive-patch fragmentation, or Artifact Filter dependence. The evaluation population is the provider-owned temporal-eligible validation subset for offsets `[-2, -1, 0, 1, 2]`, with 1,614 validation ABI Patches. Treat this as temporal-family diagnostic evidence only, not full Working Validation Split promotion evidence.

Primary comparison references:

- ABI-324 temporal five-frame detail-consensus stabilized line-state late36: Run `run_20260916_184108_954ec7`, Evaluation `eval_evalreq_abi324_temporal_eligible_failure_buckets_v1`.
- ABI-311 five-frame temporal C4 persistence/contrast line-state late36 parent: Run `run_20260915_015552_1ac51f`, Evaluation `eval_evalreq_abi311_temporal_eligible_failure_buckets_v1`.
- ABI-306 compact temporal C4 dual-evidence line-state late36 comparator: Run `run_20260914_124245_de843c`, Evaluation `eval_evalreq_abi306_temporal_eligible_failure_buckets_v1`.
- ABI-309 recall-heavy temporal C4 late line-support head late36: Run `run_20260914_205014_1794f8`, Evaluation `eval_evalreq_abi309_temporal_eligible_failure_buckets_v1`.
- ABI-223 temporal-attention fusion late36 continuity comparator: Run `run_20260908_154531_8c7e2b`, Evaluation `eval_evalreq_abi223_temporal_eligible_failure_buckets_v1`.
- ABI-322 clDice trusted-loss control: Run `run_20260915_191945_382cc4`, no failure-bucket Evaluation indexed.

## Temporal-eligible aggregate metrics

At threshold 0.5 on 1,614 temporal-eligible validation ABI Patches, ABI-324 reached:

| Metric | ABI-324 temporal-eligible evaluation |
| --- | ---: |
| Filtered Dice | 0.4294 |
| MIT filtered Dice | 0.4082 |
| Google filtered Dice | 0.4872 |
| Filtered precision | 0.4704 |
| Filtered recall | 0.3950 |
| Filtered contrail connectivity | 0.3979 |
| Filtered predicted-positive pixels | 459,172 |
| Filtered false-positive pixels | 243,172 |
| Filtered false-negative pixels | 330,812 |
| Raw Dice | 0.4480 |

These metrics match ABI-324's selected epoch-27 checkpoint. The Result is finite, non-collapsed, and source-informative. The Google-over-MIT gap remains material at about +0.0790 filtered Dice, but neither Dataset Source is failed.

| Comparator | Filtered Dice | MIT Dice | Google Dice | Precision | Recall | Connectivity | Predicted-positive pixels |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ABI-324 detail-consensus stabilized line-state | 0.4294 | 0.4082 | 0.4872 | 0.4704 | 0.3950 | 0.3979 | 459,172 |
| ABI-311 five-frame persistence/contrast line-state | 0.4250 | 0.4038 | 0.4826 | 0.4597 | 0.3952 | 0.3667 | 470,049 |
| ABI-306 compact dual-evidence line-state | 0.4225 | 0.4028 | 0.4762 | 0.4934 | 0.3695 | 0.2994 | 409,457 |
| ABI-309 late line-support recall head | 0.4235 | 0.4024 | 0.4785 | 0.4018 | 0.4478 | 0.3161 | 609,361 |
| ABI-223 temporal-attention fusion | 0.4198 | 0.3985 | 0.4768 | 0.4838 | 0.3707 | 0.4124 | 419,056 |

Relative to ABI-311, ABI-324 improves aggregate filtered Dice by +0.0044, MIT by +0.0044, Google by +0.0046, precision by +0.0107, and connectivity by +0.0312, while recall is essentially tied (-0.0002) and filtered footprint is smaller by 10,877 pixels. This supports the earlier run note: the detail-consensus stabilized head is a real operating-point improvement over ABI-311 rather than a broadening trick.

Relative to ABI-306, ABI-324 gives up compact high precision (-0.0230 precision and +49,715 predicted-positive pixels) but gains +0.0069 filtered Dice, +0.0255 recall, and +0.0985 connectivity. Relative to ABI-309, ABI-324 keeps much less recall but avoids the blunt recall-head clutter mode: precision is +0.0686 higher, connectivity +0.0819 higher, and footprint 150,189 pixels smaller. Relative to ABI-223, ABI-324 leads aggregate/source Dice and recall, but ABI-223 still has the strongest connectivity at 0.4124.

## Threshold behavior

The threshold sweep shows only modest low-threshold headroom:

| Threshold view | Threshold | Filtered Dice | Precision | Recall | Predicted-positive pixels |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best filtered Dice / closest precision-recall balance | 0.25 | 0.4339 | 0.4330 | 0.4347 | 548,883 |
| Primary evaluation | 0.50 | 0.4294 | 0.4704 | 0.3950 | 459,172 |
| High-precision reference | 0.70 | 0.4207 | 0.4956 | 0.3655 | 403,294 |
| Very high threshold reference | 0.90 | 0.3856 | 0.5399 | 0.2999 | 303,744 |

The best diagnostic threshold improves filtered Dice by about +0.0044 over the trusted fixed threshold. This is smaller than ABI-311's +0.0066, ABI-306's +0.0136, ABI-223's +0.0160, and larger than ABI-309's near-flat +0.0008. Architecturally, ABI-324 is not hiding a large clean calibration reserve below threshold 0.5; the selected fixed-threshold operating point is comparatively stable. This does not authorize Candidate-owned thresholding, calibration, postprocessing, metrics, losses, Artifact Filters, or validation selection.

## Failure-bucket observations

Failure buckets answer the diagnostic question as positive for aggregate clutter/connectivity balance, but not as a broad positive-patch-tail repair:

1. Negative-patch clutter improves versus ABI-311 and is far cleaner than ABI-309. Among 895 negative temporal-eligible validation ABI Patches, ABI-324 produced at least one filtered false-positive pixel on 533 patches, with median negative-patch false-positive count 7 pixels. Total negative-patch false-positive burden was 40,097 pixels, with 111 negative patches above 100 false-positive pixels, 7 above 500, and none above 1,000. This is cleaner than ABI-311's 584 touched negatives, 45,001 total negative false-positive pixels, and 133 patches above 100 pixels. It is much cleaner than ABI-309's 80,378 negative-patch false-positive pixels and heavy tail.
2. Positive-patch tail repair is mixed and slightly worse than ABI-311 on some count buckets. Among 719 positive temporal-eligible validation ABI Patches, ABI-324 had 72 patches with zero filtered true-positive pixels, 100 positive patches with filtered Dice below 0.1, 150 below 0.2, and 207 with filtered recall below 0.25. ABI-311 had 70, 96, 146, and 194 in those same buckets. ABI-324's aggregate gain therefore is not from uniformly fixing positive-patch complete misses or low-recall tails.
3. Positive-patch medians remain competitive but do not dominate all comparators. ABI-324 positive-patch median filtered Dice was 0.4265, precision 0.5087, recall 0.4231, and connectivity 0.4099. Compared with ABI-311, median Dice (+0.0050) and precision (+0.0107) improve, but median recall (-0.0082) and median connectivity (-0.0048) dip slightly. Compared with ABI-306, ABI-324 has lower median Dice and precision but higher median recall. Compared with ABI-309, it is much more precise but lower recall and slightly lower typical Dice/connectivity.
4. Source-stratified positive medians keep the same Google-over-MIT pattern. ABI-324 positive MIT patch medians were Dice 0.3938, precision 0.4762, recall 0.3961, and connectivity 0.3721. Positive Google patch medians were Dice 0.4784, precision 0.5649, recall 0.4746, and connectivity 0.4723. This is not source collapse, but the MIT positive-patch tail remains the harder residual failure mode.
5. Artifact Filters do not create the Result. Filters removed 37,212 predicted-positive pixels overall. Raw Dice was 0.4480 versus filtered Dice 0.4294, raw recall was 0.4273 versus filtered recall 0.3950, and raw predicted-positive pixels were 496,384 versus 459,172 filtered. Filtering lowers the score rather than hiding a failed raw operating point.

The retained diagnostic GeoTIFF samples and per-sample rows are bounded traceability artifacts selected by the Harness. This note does not reproduce raw samples, coordinates, scene identifiers, or images.

## Interpretation

Classify ABI-324's temporal-eligible failure-bucket evaluation as valid positive/mixed evidence for the five-frame temporal detail-consensus C4 branch. The main positive signal is strong: ABI-324 improves ABI-311's aggregate/source Dice, precision, and aggregate connectivity while reducing both predicted-positive footprint and negative-patch clutter. The gain is not mostly Artifact Filter dependence, not a broad negative-patch false-positive tail, and not purely a threshold accident.

The caveat is equally important: ABI-324 does not solve complete positive-patch misses, low-recall tails, or the MIT positive-patch quality gap. Its aggregate connectivity gain appears concentrated in enough weighted structures to move the global metric, but typical positive-patch connectivity is not clearly better than ABI-311/306/309/223. ABI-223 remains the strongest temporal-attention connectivity comparator despite lower aggregate Dice.

Comparator roles after this evaluation:

- ABI-324 replaces ABI-311 as the local balanced temporal C4 aggregate/connectivity comparator.
- ABI-306 remains the compact high-precision temporal C4 comparator.
- ABI-309 remains the recall-heavy temporal C4 diagnostic variant, with known clutter and heavy-tail cost.
- ABI-223 remains the temporal-attention connectivity comparator.
- ABI-322 remains negative evidence for an unchanged ABI-311-style architecture trained with `bce_dice_cldice`.

ABI-324 is temporal-eligible capped diagnostic evidence only. It must not be treated as whole-validation evidence against ABI-202 or ABI-249, and it does not justify Candidate-owned thresholding, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, or resource scheduling.

## Decision

Do not promote ABI-324 and do not submit an unchanged ABI-324 late36 continuation. The diagnostic question supports ABI-324 as the best balanced temporal C4 comparator so far, but also shows the remaining failure mode: MIT/positive-patch undercoverage and typical continuity tails are not broadly repaired.

Future in-contract work should be mechanism-changing rather than another head-only continuation. A useful next Candidate would either preserve ABI-324's reduced negative-patch clutter while explicitly targeting positive-patch undercoverage, or broaden away from temporal C4 line-state heads toward a materially different temporal alignment/change or attention mechanism that raises connected true-positive evidence at threshold 0.5. Candidate code must still avoid Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, training loops, or prediction retention.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260916_184108_954ec7/outputs/evaluations/eval_evalreq_abi324_temporal_eligible_failure_buckets_v1/summary.json`
- `run_20260916_184108_954ec7/outputs/evaluations/eval_evalreq_abi324_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260916_184108_954ec7/outputs/evaluations/eval_evalreq_abi324_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260916_184108_954ec7/outputs/evaluations/eval_evalreq_abi324_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260916_184108_954ec7/outputs/evaluations/eval_evalreq_abi324_temporal_eligible_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260916_184108_954ec7/outputs/best_metrics.json`
- `run_20260916_184108_954ec7/outputs/final_metrics.json`
- `run_20260916_184108_954ec7/outputs/metrics.jsonl`
- `run_20260916_184108_954ec7/outputs/resource_profile.json`
- `run_20260916_184108_954ec7/outputs/model_summary.json`
- `run_20260916_184108_954ec7/resolved_manifest.yaml`
- `run_20260916_184108_954ec7/candidate/budget_request.yaml`
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
- `run_20260915_191945_382cc4/outputs/best_metrics.json`
- `/history/research-notes/abi324-temporal-fiveframe-detail-consensus-stabilized-line-state-late36.md`
- `/history/research-notes/abi311-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi306-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi309-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi322-temporal-fiveframe-c4-cldice-connectivity-line-state-late36.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
