# ABI-255 temporal-eligible failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi255_temporal_eligible_failure_buckets_v1` for ABI-255 Run `run_20260911_210922_27f346`.

The evaluation asked whether ABI-255's late36 compact recurrent change-state U-Net retained its selected epoch-36 temporal-eligible validation signal under failure-bucket and threshold diagnostics, and whether its remaining deficit is primarily fragmented thin-line continuity rather than source imbalance or Artifact Filter dependence. The evaluation population is the provider-owned temporal-eligible validation subset for offsets `[-1, 0, 1]` (1,614 ABI Patches), not the full 3,088-sample Working Validation Split; treat it as diagnostic temporal-family evidence only.

Primary comparison references:

- ABI-255 temporal recurrent change-state U-Net late36: Run `run_20260911_210922_27f346`, Evaluation `eval_evalreq_abi255_temporal_eligible_failure_buckets_v1`.
- ABI-242 exploratory recurrent change-state parent: Run `run_20260911_055200_52c75f`.
- ABI-223 temporal-attention fusion U-Net late36 comparator: Run `run_20260908_154531_8c7e2b`, Evaluation `eval_evalreq_abi223_temporal_eligible_failure_buckets_v1`.
- ABI-238 temporal directional-attention late36 comparator: Run `run_20260911_004137_f54c45`.
- ABI-240 temporal line-accumulator late36 comparator: Run `run_20260911_031326_43ed12`.
- ABI-202 current whole-validation aggregate reference: Run `run_20260904_043143_ee0005`, Evaluation `eval_evalreq_abi202_wholeval_failure_buckets_v1`.

## Temporal-eligible aggregate metrics

At threshold 0.5 on 1,614 temporal-eligible validation ABI Patches, ABI-255 reached:

| Metric | ABI-255 temporal-eligible evaluation |
| --- | ---: |
| Filtered Dice | 0.4173 |
| MIT filtered Dice | 0.4008 |
| Google filtered Dice | 0.4631 |
| Filtered precision | 0.4683 |
| Filtered recall | 0.3764 |
| Filtered contrail connectivity | 0.2811 |
| Filtered predicted-positive pixels | 439,511 |
| Filtered false-positive pixels | 233,691 |
| Filtered false-negative pixels | 340,992 |
| Raw Dice | 0.4357 |

The aggregate metrics match ABI-255's selected epoch-36 checkpoint, confirming that the diagnostic request evaluated the intended checkpoint and temporal-eligible population. The Result is finite, non-collapsed, and source-informative. Google remains stronger than MIT by about +0.0623 filtered Dice, but both sources remain viable; the diagnostics do not indicate a catastrophic source-specific failure.

Relative to ABI-223 on the same temporal-eligible population, ABI-255 is lower by about -0.0024 filtered Dice, -0.0155 precision, -0.0136 Google filtered Dice, and -0.1313 connectivity, while being higher by about +0.0057 recall and +0.0023 MIT filtered Dice. Relative to ABI-238, ABI-255 is lower by about -0.0029 filtered Dice and -0.0711 connectivity, but slightly higher in recall. Relative to ABI-240, ABI-255 is slightly higher in filtered Dice and precision but lower in recall and only modestly higher in connectivity. This places ABI-255 near the temporal overlap frontier but behind the best attention-style temporal comparators for line continuity.

Relative to ABI-202's capped best-validation reference, ABI-255 remains lower by about -0.0102 filtered Dice, -0.0399 recall, -0.1767 connectivity, -0.0112 MIT Dice, and -0.0050 Google Dice while being higher in precision. Because ABI-255 is evaluated on the temporal-eligible subset rather than the full Working Validation Split, this is not a promotion or whole-validation comparison.

## Threshold behavior

The threshold sweep shows useful lower-confidence contrail evidence below the fixed primary threshold:

| Threshold view | Threshold | Filtered Dice | Precision | Recall |
| --- | ---: | ---: | ---: | ---: |
| Primary evaluation | 0.50 | 0.4173 | 0.4683 | 0.3764 |
| Best filtered Dice | 0.05 | 0.4302 | 0.4008 | 0.4644 |
| Closest precision/recall balance | 0.10 | 0.4299 | 0.4255 | 0.4343 |

Lower thresholds recover recall and raise filtered Dice by about +0.0129, but the best diagnostic threshold remains slightly below ABI-223's best-threshold filtered Dice. This does not authorize Candidate-owned thresholding, calibration, postprocessing, metrics, losses, or Artifact Filters. The architectural lesson is that the recurrent change-state model learns real but under-confident temporal contrail evidence; future work should raise true contrail logits at the model level while preserving recall and connectivity at the trusted threshold.

## Failure-bucket observations

Failure buckets clarify that ABI-255's weakness is not collapse or simple source imbalance, but a combination of fragmented continuity and widespread small negative-patch clutter:

1. Negative-patch clutter is broader than ABI-223's. Among 895 negative temporal-eligible validation ABI Patches, ABI-255 produced at least one filtered predicted-positive pixel on 728 patches. Median negative-patch false-positive count was 39 pixels. Total negative-patch false-positive burden was 56,586 pixels, with 153 negative patches above 100 false-positive pixels, 5 above 500, and 2 above 1,000. Compared with ABI-223, ABI-255 has more negative patches with any false positives and a higher median false-positive count, even though its count above 100 pixels is lower.
2. Positive-patch complete misses are improved, but under-coverage remains. Among 719 positive temporal-eligible validation ABI Patches, only 5 had zero filtered predicted-positive pixels, 88 had filtered Dice below 0.1, 134 had filtered Dice below 0.2, and 154 had filtered recall below 0.2. The low zero-prediction count supports the late36 note's conclusion that ABI-255 learned broad temporal evidence, but the recall tail remains large enough to limit aggregate Dice and continuity.
3. Positive-patch medians are usable but not clearly better than the temporal-attention comparator. Median positive-patch filtered Dice was 0.4252, median precision 0.5098, and median recall 0.4250. Positive Google patches had median filtered Dice 0.4689, precision 0.5711, and recall 0.4409; positive MIT patches had median filtered Dice 0.4050, precision 0.4761, and recall 0.4162. MIT median Dice is comparable to ABI-223, but Google median Dice and precision trail ABI-223, consistent with the aggregate Google gap.

Artifact Filters removed 34,500 predicted-positive pixels over the temporal-eligible validation subset. Raw Dice was 0.4357 versus filtered Dice 0.4173, and raw predicted-positive pixels were 474,011 versus 439,511 filtered. Filtering lowers Dice rather than creating the Result, so ABI-255 is not excessively Artifact Filter-dependent.

The retained diagnostic GeoTIFF samples and per-sample rows are traceability artifacts selected under the bounded evaluation policy. This note does not reproduce raw samples, coordinates, scene identifiers, or images.

## Interpretation

Classify ABI-255's temporal-eligible failure-bucket evaluation as valid, finite diagnostic evidence for compact recurrent temporal change modeling. It confirms the late36 Run observation: the recurrent state branch can mature into a near-frontier temporal overlap Result with low resource use, nondegenerate MIT/Google behavior, and no Artifact Filter dependence.

The same diagnostics also confirm the branch's main limitation. ABI-255 covers more positive patches than ABI-223 in the sense of fewer complete zero-prediction misses, but it does not preserve thin-line continuity or negative-patch cleanliness as well as the strongest temporal-attention comparator. The recurrent state appears to spread lower-confidence temporal evidence broadly rather than form sufficiently connected high-confidence contrail structures at threshold 0.5.

ABI-255 should remain the compact recurrent temporal comparator alongside ABI-223/238/240, but ABI-223 remains the clearer temporal-attention diagnostic comparator and ABI-202 remains the aggregate whole-validation frontier. ABI-255 should not be promoted and should not be treated as whole-validation evidence.

## Decision

Do not promote ABI-255 and do not submit another unchanged late36 continuation of the ABI-242/255 recurrent change-state branch. The late-budget and diagnostic questions have both been answered: the branch is real and useful, but its remaining weakness is mechanism-level line continuity and evidence sharpening rather than simply insufficient epochs.

A reasonable next Candidate, if the campaign continues with temporal modeling, should be mechanism-changing: add line-aware recurrent state, centerline-preserving temporal decoding, or a recall-preserving evidence/calibration head over temporal features without Candidate-owned thresholding, postprocessing, losses, metrics, data loading, temporal lookup, temporal selection, coordinates, or resource scheduling. If broadening away from temporal modeling, use ABI-255 as a compact recurrent comparator rather than a new frontier target.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_210922_27f346/outputs/evaluations/eval_evalreq_abi255_temporal_eligible_failure_buckets_v1/summary.json`
- `run_20260911_210922_27f346/outputs/evaluations/eval_evalreq_abi255_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260911_210922_27f346/outputs/evaluations/eval_evalreq_abi255_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260911_210922_27f346/outputs/evaluations/eval_evalreq_abi255_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260911_210922_27f346/outputs/evaluations/eval_evalreq_abi255_temporal_eligible_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260911_210922_27f346/outputs/best_metrics.json`
- `run_20260911_210922_27f346/outputs/final_metrics.json`
- `run_20260911_210922_27f346/outputs/metrics.jsonl`
- `run_20260911_210922_27f346/outputs/resource_profile.json`
- `run_20260911_210922_27f346/outputs/model_summary.json`
- `run_20260911_210922_27f346/resolved_manifest.yaml`
- `run_20260911_210922_27f346/candidate/budget_request.yaml`
- `run_20260911_055200_52c75f/outputs/best_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260911_004137_f54c45/outputs/best_metrics.json`
- `run_20260911_031326_43ed12/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
