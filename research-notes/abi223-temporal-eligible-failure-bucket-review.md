# ABI-223 temporal-eligible failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi223_temporal_eligible_failure_buckets_v1` for ABI-223 Run `run_20260908_154531_8c7e2b`.

The evaluation asked whether ABI-223's late36 three-frame temporal-attention fusion U-Net retained its strong capped temporal-eligible validation signal under failure-bucket and threshold diagnostics, whether it showed a robust advantage over the ABI-218 matched temporal-eligible single-frame control, and whether the Result depended excessively on provider-owned Artifact Filters. The evaluation population is the provider-owned temporal-eligible validation subset for offsets `[-1, 0, 1]` (1,614 ABI Patches), not the full 3,088-sample Working Validation Split; treat it as diagnostic temporal-family evidence only.

Primary comparison references:

- ABI-223 temporal-attention fusion U-Net late36: Run `run_20260908_154531_8c7e2b`, Evaluation `eval_evalreq_abi223_temporal_eligible_failure_buckets_v1`.
- ABI-222 exploratory temporal-attention parent: Run `run_20260908_150315_9aea3f`.
- ABI-218 matched temporal-eligible single-frame control: Run `run_20260908_123030_05ad37`.
- ABI-202 current whole-validation aggregate reference: Run `run_20260904_043143_ee0005`, Evaluation `eval_evalreq_abi202_wholeval_failure_buckets_v1`.
- ABI-249 high-precision C4 whole-validation comparator: Run `run_20260911_111909_dd7ef7`, Evaluation `eval_evalreq_abi249_wholeval_failure_buckets_v1`.

## Temporal-eligible aggregate metrics

At threshold 0.5 on 1,614 temporal-eligible validation ABI Patches, ABI-223 reached:

| Metric | ABI-223 temporal-eligible evaluation |
| --- | ---: |
| Filtered Dice | 0.4198 |
| MIT filtered Dice | 0.3985 |
| Google filtered Dice | 0.4768 |
| Filtered precision | 0.4838 |
| Filtered recall | 0.3707 |
| Filtered contrail connectivity | 0.4124 |
| Filtered predicted-positive pixels | 419,056 |
| Filtered false-positive pixels | 216,332 |
| Filtered false-negative pixels | 344,088 |
| Raw Dice | 0.4385 |

The aggregate metrics match the Run's selected epoch-36 validation checkpoint, confirming that the diagnostic request evaluated the intended best checkpoint and temporal-eligible population. The Result is finite, non-collapsed, and source-informative. Google remains stronger than MIT by about +0.0783 filtered Dice; both sources are nevertheless viable, with no catastrophic source-specific failure.

Relative to the ABI-218 matched single-frame control on the same temporal-eligible selection, ABI-223 improves filtered Dice by +0.0742, filtered recall by +0.0706, connectivity by +0.1810, MIT filtered Dice by +0.0681, and Google filtered Dice by +0.0916. This supports a real temporal-context advantage for the attention-fusion design rather than only a temporal-eligibility population effect.

Relative to ABI-202's capped best-validation reference, ABI-223 remains slightly lower on filtered Dice, recall, MIT Dice, and connectivity while being higher on precision and Google Dice. Because this evaluation is temporal-eligible rather than whole validation, it should not be interpreted as a promotion or whole-data comparison.

## Threshold behavior

The threshold sweep shows substantial diagnostic recall headroom below the fixed primary threshold:

| Threshold view | Threshold | Filtered Dice | Precision | Recall |
| --- | ---: | ---: | ---: | ---: |
| Primary evaluation | 0.50 | 0.4198 | 0.4838 | 0.3707 |
| Best filtered Dice | 0.05 | 0.4358 | 0.4089 | 0.4665 |
| Closest precision/recall balance | 0.10 | 0.4349 | 0.4348 | 0.4351 |

This does not authorize Candidate-owned thresholding, calibration, postprocessing, metrics, losses, or Artifact Filters. The architectural lesson is that ABI-223 learned useful lower-confidence contrail evidence that is suppressed at the fixed 0.5 threshold. Future temporal architecture work should try to raise true contrail evidence at the model-logit level while preserving ABI-223's precision and nondegenerate source behavior.

## Failure-bucket observations

Failure buckets show a useful but still imperfect operating point:

1. Negative-patch clutter is present but bounded. Among 895 negative temporal-eligible validation ABI Patches, 515 had at least one filtered false-positive pixel. Median negative-patch false-positive count was 17 pixels. Total negative-patch false-positive burden was 51,290 pixels, with 179 negative patches above 100 false-positive pixels, 9 above 500, and none above 1,000.
2. Positive-patch miss tails remain the main weakness. Among 719 positive temporal-eligible validation ABI Patches, 22 had zero filtered predicted-positive pixels, 103 had filtered Dice below 0.1, 147 had filtered Dice below 0.2, and 167 had filtered recall below 0.2. Median positive-patch filtered Dice was 0.4357, median precision 0.5450, and median recall 0.4227.
3. Source-stratified positive-patch medians mirror the aggregate pattern. Positive Google patches had median filtered Dice 0.4883, precision 0.5828, and recall 0.4630; positive MIT patches had median filtered Dice 0.4015, precision 0.5000, and recall 0.3991. The model is not source-collapsed, but MIT remains the harder source for this temporal branch.

Artifact Filters removed 34,074 predicted-positive pixels over the temporal-eligible validation subset. Raw Dice was 0.4385 versus filtered Dice 0.4198, and raw predicted-positive pixels were 453,130 versus 419,056 filtered. Filtering lowers the metric rather than creating the Result, so ABI-223 is not excessively Artifact Filter-dependent.

The retained diagnostic GeoTIFF samples and per-sample rows are traceability artifacts selected under the bounded evaluation policy. This note does not reproduce raw samples, coordinates, scene identifiers, or images.

## Interpretation

Classify ABI-223's temporal-eligible failure-bucket evaluation as valid, finite diagnostic evidence that three-frame provider-owned temporal context can materially improve over a matched single-frame control. The strongest evidence is the simultaneous improvement in aggregate filtered Dice, recall, connectivity, and both Dataset Sources over ABI-218 while retaining a modest predicted-positive fraction and no Artifact Filter dependence.

The same evidence also clarifies the remaining failure mode: ABI-223 is conservative at threshold 0.5 and still misses or under-covers a substantial tail of positive temporal-eligible patches, especially on MIT. The low-threshold sweep suggests recoverable recall, but trusted evaluation uses the fixed primary threshold, so the next useful work should be architecture-level evidence sharpening rather than threshold changes.

ABI-223 remains the temporal-family diagnostic comparator. Later five-frame and temporal-line variants did not yet supersede it on the capped temporal frontier, and ABI-223's evaluation provides the clearest temporal advantage over the single-frame control. It still should not replace ABI-202 as the aggregate whole-validation frontier or ABI-249 as the high-precision C4 whole-validation comparator.

## Decision

Do not promote ABI-223 and do not reinterpret temporal-eligible diagnostics as full Working Validation evidence. Retain ABI-223 as the strongest temporal-family comparator and as evidence that temporal context is worth continued bounded exploration.

The next temporal hypothesis should be mechanism-changing and recall/connectivity-preserving, not another unchanged late36 continuation of ABI-223. Good in-contract directions include a temporal architecture that combines ABI-223-style attention with stronger center-frame detail/support logits, confidence-calibrated dual-head agreement, or a compact motion/change stream that raises true contrail logits at threshold 0.5 without Candidate-owned thresholding or postprocessing. If the next step broadens instead, use ABI-223 as the temporal reference when comparing modern compact attention/backbone or calibration-style candidates.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/summary.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/threshold_sweep.json`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/final_metrics.json`
- `run_20260908_154531_8c7e2b/outputs/metrics.jsonl`
- `run_20260908_154531_8c7e2b/outputs/resource_profile.json`
- `run_20260908_154531_8c7e2b/outputs/model_summary.json`
- `run_20260908_154531_8c7e2b/resolved_manifest.yaml`
- `run_20260908_154531_8c7e2b/candidate/budget_request.yaml`
- `run_20260908_150315_9aea3f/outputs/best_metrics.json`
- `run_20260908_123030_05ad37/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260911_111909_dd7ef7/outputs/evaluations/eval_evalreq_abi249_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
