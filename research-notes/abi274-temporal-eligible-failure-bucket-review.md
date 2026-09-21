# ABI-274 temporal-eligible failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi274_temporal_eligible_failure_buckets_v1` for ABI-274 Run `run_20260912_180856_79ba22`.

The evaluation asked whether ABI-274's late36 three-frame temporal line-state attention U-Net retained its selected epoch-36 temporal-eligible validation signal under failure-bucket and threshold diagnostics, and whether its recall/source lift versus ABI-223/238 was limited mainly by fragmented thin-line continuity, negative-patch clutter, source imbalance, or Artifact Filter dependence. The evaluation population is the provider-owned temporal-eligible validation subset for offsets `[-1, 0, 1]` (1,614 ABI Patches), not the full 3,088-sample Working Validation Split; treat it as diagnostic temporal-family evidence only.

Primary comparison references:

- ABI-274 temporal line-state attention U-Net late36: Run `run_20260912_180856_79ba22`, Evaluation `eval_evalreq_abi274_temporal_eligible_failure_buckets_v1`.
- ABI-273 exploratory parent: Run `run_20260912_171825_ff0d00`.
- ABI-223 temporal-attention fusion U-Net late36 comparator: Run `run_20260908_154531_8c7e2b`, Evaluation `eval_evalreq_abi223_temporal_eligible_failure_buckets_v1`.
- ABI-255 compact recurrent temporal late36 comparator: Run `run_20260911_210922_27f346`, Evaluation `eval_evalreq_abi255_temporal_eligible_failure_buckets_v1`.
- ABI-238 temporal directional-context late36 comparator: Run `run_20260911_004137_f54c45`.
- ABI-202 current whole-validation aggregate reference: Run `run_20260904_043143_ee0005`, Evaluation `eval_evalreq_abi202_wholeval_failure_buckets_v1`.

## Temporal-eligible aggregate metrics

At threshold 0.5 on 1,614 temporal-eligible validation ABI Patches, ABI-274 reached:

| Metric | ABI-274 temporal-eligible evaluation |
| --- | ---: |
| Filtered Dice | 0.4194 |
| MIT filtered Dice | 0.3994 |
| Google filtered Dice | 0.4726 |
| Filtered precision | 0.4541 |
| Filtered recall | 0.3895 |
| Filtered contrail connectivity | 0.2829 |
| Filtered predicted-positive pixels | 469,049 |
| Filtered false-positive pixels | 256,041 |
| Filtered false-negative pixels | 333,804 |
| Raw Dice | 0.4368 |

The aggregate metrics match ABI-274's selected epoch-36 checkpoint, confirming that the diagnostic request evaluated the intended checkpoint and temporal-eligible population. The Result is finite, non-collapsed, and source-informative. Google remains stronger than MIT by about +0.0732 filtered Dice; both sources remain viable, with no catastrophic source-specific failure.

Relative to ABI-223 on the same temporal-eligible population, ABI-274 is essentially tied on filtered Dice (-0.0004) and improves filtered recall (+0.0188), MIT Dice (+0.0009), and Google true-positive coverage, but it is lower on precision (-0.0296) and far lower on connectivity (-0.1295). Relative to ABI-255, ABI-274 is slightly higher on filtered Dice (+0.0020), recall (+0.0131), Google Dice (+0.0095), and connectivity (+0.0018), but lower on precision (-0.0142) and slightly lower on MIT Dice (-0.0014). Relative to ABI-238's run-level temporal-eligible best metrics, ABI-274 is effectively tied on filtered Dice and has higher recall, but lower precision and connectivity.

The evaluation therefore confirms ABI-274 as a useful temporal-family diagnostic comparator for recall/source behavior, not as a promotion candidate or a replacement for ABI-223's cleaner connected-line evidence.

## Threshold behavior

The threshold sweep shows modest lower-threshold headroom but not a large calibration reserve:

| Threshold view | Threshold | Filtered Dice | Precision | Recall |
| --- | ---: | ---: | ---: | ---: |
| Primary evaluation | 0.50 | 0.4194 | 0.4541 | 0.3895 |
| Best filtered Dice | 0.10 | 0.4264 | 0.4065 | 0.4483 |
| Closest precision/recall balance | 0.20 | 0.4254 | 0.4284 | 0.4224 |

Lowering the diagnostic threshold raises filtered Dice by only about +0.0070 while trading away precision. This is less headroom than the prior ABI-223 and ABI-255 temporal diagnostic sweeps, so ABI-274's fixed-threshold limitation is not simply a threshold-placement issue. This does not authorize Candidate-owned thresholding, calibration, postprocessing, metrics, losses, or Artifact Filters. The architectural lesson is that early line-state attention already raises more temporal evidence to the trusted threshold than ABI-223/255, but the extra evidence is less cleanly connected and less precise.

## Failure-bucket observations

Failure buckets clarify the operating point:

1. Negative-patch clutter is broader than ABI-223 and similar to or slightly worse than ABI-255. Among 895 negative temporal-eligible validation ABI Patches, ABI-274 produced at least one filtered false-positive pixel on 733 patches. Median negative-patch false-positive count was 45 pixels. Total negative-patch false-positive burden was 56,798 pixels, with 158 negative patches above 100 false-positive pixels, 5 above 500, and none above 1,000.
2. Positive-patch complete misses are low, but a large under-coverage tail remains. Among 719 positive temporal-eligible validation ABI Patches, 4 had zero filtered predicted-positive pixels, 86 had filtered Dice below 0.1, 131 had filtered Dice below 0.2, and 145 had filtered recall below 0.2. Median positive-patch filtered Dice was 0.4408, median precision 0.4975, and median recall 0.4490.
3. Source-stratified positive-patch medians show the same Google-over-MIT pattern as the aggregate metrics. Positive Google patches had median filtered Dice 0.5032, precision 0.5669, and recall 0.5000; positive MIT patches had median filtered Dice 0.4098, precision 0.4641, and recall 0.4125. The model is not source-collapsed, but MIT remains the harder source and contributes more of the recall-tail burden.
4. Connectivity is the main scientific weakness. ABI-274 has few complete positive-patch misses and better aggregate recall than ABI-223/255, but its filtered connectivity is only 0.2829, near ABI-255 and far below ABI-223's 0.4124. The result is consistent with fragmented or cluttered temporal evidence rather than absence of temporal signal.

Artifact Filters removed 38,710 predicted-positive pixels over the temporal-eligible validation subset. Raw Dice was 0.4368 versus filtered Dice 0.4194, and raw predicted-positive pixels were 507,759 versus 469,049 filtered. Filtering lowers Dice rather than creating the Result, so ABI-274 is not excessively Artifact Filter-dependent. The removed pixels are concentrated on positive patches (34,148) rather than negative patches (4,562), reinforcing that the filters are not masking a large negative-patch clutter failure.

The retained diagnostic GeoTIFF samples and per-sample rows are traceability artifacts selected under the bounded evaluation policy. This note does not reproduce raw samples, coordinates, scene identifiers, or images.

## Interpretation

Classify ABI-274's temporal-eligible failure-bucket evaluation as valid, finite diagnostic evidence that the early temporal line-state mechanism improves recall and positive-patch coverage enough to join the temporal comparator set. It successfully answered the late-budget question from ABI-273: longer training brought the branch into the ABI-223/238 primary-Dice band and above ABI-255 on aggregate temporal-eligible filtered Dice.

The same diagnostics answer the mechanism question negatively for connected thin-line continuity. ABI-274's extra recall arrives with broader negative-patch clutter, lower precision than ABI-223/255, and connectivity near the weaker recurrent comparator rather than the stronger temporal-attention comparator. The branch therefore appears to improve evidence presence but not evidence organization: it sees more true contrail pixels at threshold 0.5, especially on Google, but does not reliably form continuous thin-line masks.

ABI-274 should be retained as a temporal recall/source-balance comparator alongside ABI-223 and ABI-255, but ABI-223 remains the better temporal line-continuity comparator. ABI-202 remains the aggregate whole-validation reference, and ABI-249 remains the high-precision C4/rotation-aware whole-validation comparator. ABI-274 should not be interpreted as whole-validation promotion evidence.

## Decision

Do not promote ABI-274 and do not submit another unchanged late36 continuation of the ABI-273/274 early line-state injector. The late-budget and temporal-eligible diagnostic questions have both been answered: the mechanism is useful for recall/source balance but did not solve connected thin-line continuity or negative-patch cleanliness.

Future temporal work should be mechanism-changing and should preserve ABI-274's recall/source lift while adding stronger continuity support before logits reach the trusted threshold. High-value in-contract directions include a center-frame detail bridge over temporal attention, a compact orientation-consensus/C4 line prior integrated into the temporal decoder, or a line-aware recurrent/attention state that explicitly supports continuity without Candidate-owned thresholding, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, or resource scheduling. If the next step broadens away from temporal modeling, use ABI-274 as the recall-oriented temporal comparator rather than a new frontier target.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_180856_79ba22/outputs/evaluations/eval_evalreq_abi274_temporal_eligible_failure_buckets_v1/summary.json`
- `run_20260912_180856_79ba22/outputs/evaluations/eval_evalreq_abi274_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260912_180856_79ba22/outputs/evaluations/eval_evalreq_abi274_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260912_180856_79ba22/outputs/evaluations/eval_evalreq_abi274_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260912_180856_79ba22/outputs/evaluations/eval_evalreq_abi274_temporal_eligible_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260912_180856_79ba22/outputs/best_metrics.json`
- `run_20260912_180856_79ba22/outputs/final_metrics.json`
- `run_20260912_180856_79ba22/outputs/metrics.jsonl`
- `run_20260912_180856_79ba22/outputs/resource_profile.json`
- `run_20260912_180856_79ba22/outputs/model_summary.json`
- `run_20260912_180856_79ba22/resolved_manifest.yaml`
- `run_20260912_180856_79ba22/candidate/budget_request.yaml`
- `run_20260912_171825_ff0d00/outputs/best_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260911_210922_27f346/outputs/evaluations/eval_evalreq_abi255_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260911_210922_27f346/outputs/evaluations/eval_evalreq_abi255_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260911_210922_27f346/outputs/evaluations/eval_evalreq_abi255_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260911_004137_f54c45/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
