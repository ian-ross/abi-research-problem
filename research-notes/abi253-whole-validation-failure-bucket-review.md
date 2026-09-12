# ABI-253 whole-validation failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi253_wholeval_failure_buckets_v1` for ABI-253 Run `run_20260911_171333_f0b603`.

The evaluation asked whether ABI-253's late36 compact full-spectral BTD+SZA line-memory U-NetFormer capped-best result (0.4083 `val/filtered_dice` at epoch 23) transfers beyond the trusted representative validation cap, and whether whole-validation failure buckets show robust MIT/Google behavior without excessive Artifact Filter dependence. This is diagnostic evidence only; promotion remains operator-reviewed.

Primary comparison references:

- ABI-253 compact line-memory U-NetFormer late36: Run `run_20260911_171333_f0b603`, Evaluation `eval_evalreq_abi253_wholeval_failure_buckets_v1`.
- ABI-252 compact line-memory U-NetFormer parent: Run `run_20260911_161019_8c76cd`.
- ABI-244 shifted-window U-NetFormer comparator: Run `run_20260911_072719_ade068`.
- ABI-249 C4 high-precision whole-validation comparator: Run `run_20260911_111909_dd7ef7`, Evaluation `eval_evalreq_abi249_wholeval_failure_buckets_v1`.
- ABI-202 current whole-validation aggregate reference: Run `run_20260904_043143_ee0005`, Evaluation `eval_evalreq_abi202_wholeval_failure_buckets_v1`.

## Whole-validation metrics

At threshold 0.5 on the full 3,088-sample Working Validation Split, ABI-253 reached:

| Metric | ABI-253 whole validation |
| --- | ---: |
| Filtered Dice | 0.4097 |
| MIT filtered Dice | 0.3962 |
| Google filtered Dice | 0.4344 |
| Filtered precision | 0.4473 |
| Filtered recall | 0.3779 |
| Filtered contrail connectivity | 0.3299 |
| Filtered predicted-positive pixels | 599,360 |
| Filtered false-positive pixels | 331,274 |
| Filtered false-negative pixels | 441,277 |
| Raw Dice | 0.4244 |

ABI-253's capped signal transferred almost exactly to whole validation: capped-best filtered Dice was 0.4083 and whole-validation filtered Dice is 0.4097. MIT filtered Dice also stays close to capped validation (0.3962 whole versus 0.3944 capped). Google filtered Dice falls modestly from 0.4426 capped to 0.4344 whole, but it remains source-informative and non-collapsed.

Relative to ABI-202, ABI-253 remains lower by about -0.0215 filtered Dice, -0.0178 MIT Dice, -0.0300 Google Dice, -0.0420 recall, and -0.1326 connectivity. Precision is only slightly higher (+0.0042), and predicted-positive area is smaller than ABI-202's 672,206 filtered pixels, but not enough to offset the recall/connectivity gap.

Relative to ABI-249, ABI-253 is lower by about -0.0100 filtered Dice, -0.0029 MIT Dice, -0.0257 Google Dice, -0.0393 precision, and -0.0677 connectivity, while recall is slightly higher (+0.0089). ABI-253 therefore does not replace ABI-249 as the high-precision/compact-prediction comparator, nor ABI-202 as the aggregate reference. Its main value is as a whole-validation-tested U-NetFormer comparator showing that the line-memory branch improved over its capped U-NetFormer predecessors but did not create a new frontier.

## Threshold behavior

The threshold sweep shows moderate diagnostic headroom at lower thresholds:

| Threshold view | Threshold | Filtered Dice | Precision | Recall |
| --- | ---: | ---: | ---: | ---: |
| Primary evaluation | 0.50 | 0.4097 | 0.4473 | 0.3779 |
| Best filtered Dice | 0.10 | 0.4196 | 0.4023 | 0.4385 |

Lowering the diagnostic threshold would recover recall and raise Dice by about +0.0099, but the best threshold remains below ABI-202's primary-threshold filtered Dice (0.4312) and close to ABI-249's primary result (0.4197). This does not authorize Candidate-owned thresholding, calibration, postprocessing, losses, metrics, or Artifact Filters. The architectural lesson is that ABI-253 learned some useful lower-confidence contrail evidence, but the compact line-memory U-NetFormer head does not raise that evidence as effectively as ABI-202 or ABI-249 at the fixed trusted threshold.

## Failure-bucket observations

Failure buckets show that ABI-253 is finite and source-informative, but its compact line-memory operating point is neither as clean as ABI-249 nor as connected/recall-preserving as ABI-202:

1. Negative-patch clutter is worse than the main whole-validation comparators. Among 2,003 negative validation ABI Patches, ABI-253 produced at least one filtered predicted-positive pixel on 1,420 patches. Median negative-patch false-positive count was 24 pixels. Total negative-patch false-positive pixels were 96,617, with 294 negative patches above 100 filtered false-positive pixels, 9 above 500, and none above 1,000. This is substantially heavier than ABI-249's 66,218 total negative false-positive pixels and ABI-202's 71,310, despite ABI-253's lower aggregate predicted-positive area than ABI-202.
2. Positive-patch miss tails are mixed. ABI-253 had 21 positive validation patches with zero filtered predicted-positive pixels, 175 positive patches below 0.1 filtered Dice, 238 below 0.2 filtered Dice, and 273 below 0.2 filtered recall. The zero-prediction count is better than ABI-202 and ABI-249, but low-Dice and low-recall tails remain comparable or worse, explaining why aggregate recall and connectivity do not reach ABI-202.
3. Median positive-patch quality is usable but not frontier-leading. Median positive-patch filtered Dice was 0.4246, median precision 0.5129, and median recall 0.4091. By Dataset Source, median positive-patch filtered Dice was 0.3870 on MIT and 0.4664 on Google; median precision was 0.4691 on MIT and 0.5586 on Google; median recall was 0.3776 on MIT and 0.4603 on Google. This confirms non-collapse and a consistent Google advantage, but ABI-249 has stronger median Dice/precision and ABI-202 has stronger median recall.

Artifact Filters removed 38,183 predicted-positive pixels over the full split, corresponding to 152,732 square kilometers under the evaluation metadata's pixel-area accounting. Raw Dice was 0.4244 versus filtered Dice 0.4097, and raw predicted-positive pixels were 637,543 versus 599,360 filtered. Filtering lowers Dice modestly rather than creating the Result, so ABI-253 is not primarily Artifact Filter-dependent.

The retained diagnostic GeoTIFF samples and per-sample rows are traceability artifacts selected under the bounded evaluation policy. This note does not reproduce raw samples, coordinates, scene identifiers, or images.

## Training and resource context

ABI-253 completed the approved late-improving 36-epoch budget as an exact close continuation of ABI-252. The selected capped checkpoint was epoch 23, and the whole-validation evaluation used the intended best checkpoint artifact. The Run stayed inside the active Workspace Configuration: approved `late_improving` budget, `abi_16ch_plus_sza` input mode, trusted source-balanced capped selection, trusted random mirroring, BCE-Dice primary loss, trusted Line/Centerline auxiliary outputs, batch size 4, constant learning rate, disabled early stopping, A100 execution, and Harness-owned metrics/Artifact Filters.

The model had 5,007,108 parameters, under the 25,000,000-parameter ceiling. However, the late36 execution consumed about 10,220 seconds of the 10,800-second late-improving wall-clock budget. That resource profile makes any compute-added line-memory U-NetFormer continuation unsafe without substantial simplification or a separate operator-approved capability change.

## Interpretation

Classify ABI-253's whole-validation evaluation as valid, finite, non-collapsed diagnostic evidence for the compact line-memory U-NetFormer branch. The late36 continuation answered the key family-development question: ABI-252 was genuinely budget-truncated, and the compact row/column line-memory plus low-resolution shifted-window attention design can transfer its capped score to the canonical Working Validation Split.

The same evidence also provides a hard comparative stop for this exact branch. ABI-253 does not beat ABI-202, does not beat ABI-249, and shows weaker connectivity plus heavier negative-patch clutter than its stronger comparators. The branch is useful as a whole-validation-tested modern-backbone/U-NetFormer comparator, not as a new promotion candidate or a reason to spend another unchanged late-budget run.

## Decision

Do not promote ABI-253 and do not reinterpret this whole-validation diagnostic as deployment evidence. Retain ABI-202 as the current aggregate whole-validation filtered-Dice reference, ABI-249 as the high-precision rotation-aware comparator, ABI-223 as the temporal-family diagnostic comparator on its temporal-eligible population, and ABI-253 as the U-NetFormer/line-memory comparator.

Stop exact compact line-memory U-NetFormer continuations unless a future hypothesis changes the mechanism while reducing or preserving resource cost. A reasonable next research step is to broaden again rather than add attention to ABI-253: prioritize a recall-preserving architecture-level calibration or evidence-raising mechanism, a temporal change/detail design informed by ABI-223, or another lightweight modern backbone that explicitly targets MIT recall/connectivity and negative-patch clutter without Candidate-owned thresholding or postprocessing.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_171333_f0b603/outputs/evaluations/eval_evalreq_abi253_wholeval_failure_buckets_v1/summary.json`
- `run_20260911_171333_f0b603/outputs/evaluations/eval_evalreq_abi253_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260911_171333_f0b603/outputs/evaluations/eval_evalreq_abi253_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260911_171333_f0b603/outputs/evaluations/eval_evalreq_abi253_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260911_171333_f0b603/outputs/evaluations/eval_evalreq_abi253_wholeval_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260911_171333_f0b603/outputs/best_metrics.json`
- `run_20260911_171333_f0b603/outputs/final_metrics.json`
- `run_20260911_171333_f0b603/outputs/metrics.jsonl`
- `run_20260911_171333_f0b603/outputs/resource_profile.json`
- `run_20260911_171333_f0b603/outputs/model_summary.json`
- `run_20260911_171333_f0b603/resolved_manifest.yaml`
- `run_20260911_171333_f0b603/candidate/budget_request.yaml`
- `run_20260911_161019_8c76cd/outputs/best_metrics.json`
- `run_20260911_072719_ade068/outputs/best_metrics.json`
- `run_20260911_111909_dd7ef7/outputs/evaluations/eval_evalreq_abi249_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260911_111909_dd7ef7/outputs/evaluations/eval_evalreq_abi249_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260911_111909_dd7ef7/outputs/evaluations/eval_evalreq_abi249_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260908_154531_8c7e2b/outputs/evaluations/eval_evalreq_abi223_temporal_eligible_failure_buckets_v1/aggregate_metrics.json`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
