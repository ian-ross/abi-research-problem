# ABI-279 whole-validation failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi279_wholeval_failure_buckets_v1` for ABI-279 Run `run_20260913_000141_3344db`.

The evaluation asked whether ABI-279's late36 C4 dual-evidence recall-bridge U-Net retained its selected epoch-22 capped signal on the full 3,088-sample Working Validation Split, and whether its recall/connectivity lift versus ABI-249 was limited mainly by precision loss, negative-patch clutter, source balance, fragmented thin-line continuity, or Artifact Filter dependence. This is diagnostic evidence only; promotion remains operator-reviewed.

Primary comparison references:

- ABI-279 C4 dual-evidence recall bridge late36: Run `run_20260913_000141_3344db`, Evaluation `eval_evalreq_abi279_wholeval_failure_buckets_v1`.
- ABI-249 C4 steerable line-context late36 comparator: Run `run_20260911_111909_dd7ef7`, Evaluation `eval_evalreq_abi249_wholeval_failure_buckets_v1`.
- ABI-202 current whole-validation aggregate reference: Run `run_20260904_043143_ee0005`, Evaluation `eval_evalreq_abi202_wholeval_failure_buckets_v1`.
- ABI-196 prior late36 aggregate reference: Run `run_20260903_195527_248472`, Evaluation `eval_evalreq_abi196_wholeval_failure_buckets_v1`.
- ABI-184 precision/connectivity and negative-patch-discipline reference: Run `run_20260902_213856_2c04ac`, Evaluation `eval_evalreq_abi184_wholeval_failure_buckets_v1`.

## Whole-validation metrics

At threshold 0.5 on the full 3,088-sample Working Validation Split, ABI-279 reached:

| Metric | ABI-279 whole validation |
| --- | ---: |
| Filtered Dice | 0.4165 |
| MIT filtered Dice | 0.4011 |
| Google filtered Dice | 0.4469 |
| Filtered precision | 0.4470 |
| Filtered recall | 0.3900 |
| Filtered contrail connectivity | 0.4502 |
| Filtered predicted-positive pixels | 618,929 |
| Filtered false-positive pixels | 342,298 |
| Filtered false-negative pixels | 432,732 |
| Raw Dice | 0.4312 |

The whole-validation Result is finite, non-collapsed, and source-informative, and it transfers the capped operating-point tradeoff observed in the prior ABI-279 note. Whole-validation filtered Dice (0.4165) is slightly above its capped selected checkpoint (0.4145), MIT filtered Dice also rises slightly (0.4011 whole versus 0.3984 capped), while Google filtered Dice drops modestly (0.4469 whole versus 0.4574 capped).

Relative to ABI-249, ABI-279 recovers the intended recall/connectivity direction but gives back ABI-249's main advantage. ABI-279 has higher recall (+0.0210), higher connectivity (+0.0527), slightly higher MIT Dice (+0.0020), and fewer false-negative pixels (-14,869), but lower aggregate filtered Dice (-0.0032), lower Google Dice (-0.0132), much lower precision (-0.0396), more predicted-positive pixels (+80,921), and more false-positive pixels (+66,052). The dual-evidence bridge therefore improves coverage and connectedness relative to ABI-249, but not cleanly enough to beat the compact C4 comparator on whole-validation filtered Dice.

Relative to ABI-202, ABI-279 remains below the aggregate frontier: filtered Dice is lower by about -0.0146, recall by about -0.0299, connectivity by about -0.0123, MIT Dice by about -0.0130, and Google Dice by about -0.0176. Precision is similar to ABI-202 and slightly higher, but ABI-202 remains the current aggregate whole-validation reference.

Relative to ABI-196, ABI-279 improves aggregate filtered Dice (+0.0019), connectivity (+0.0675), precision (+0.0091), and MIT source Dice, while being slightly lower on recall and lower on Google Dice. Relative to ABI-184, ABI-279 improves aggregate Dice, MIT Dice, Google Dice, recall, and false-negative count, but ABI-184 remains higher precision and slightly higher connectivity with a smaller predicted-positive footprint.

## Threshold behavior

The threshold sweep shows limited diagnostic headroom:

| Threshold view | Threshold | Filtered Dice | Precision | Recall |
| --- | ---: | ---: | ---: | ---: |
| Primary evaluation | 0.50 | 0.4165 | 0.4470 | 0.3900 |
| Best filtered Dice | 0.15 | 0.4218 | 0.4044 | 0.4408 |
| Closest precision/recall balance | 0.25 | 0.4212 | 0.4215 | 0.4209 |

Lowering the diagnostic threshold raises filtered Dice by about +0.0053 at best while trading precision for recall. This does not authorize Candidate-owned thresholding, calibration, postprocessing, metrics, losses, or Artifact Filters. The architectural lesson is that the bridge already lifts some true contrail evidence to threshold 0.5, but the remaining recall reserve is accompanied by enough extra false positives that threshold placement alone is not the main missing mechanism.

## Failure-bucket observations

Failure buckets clarify why the ABI-279 bridge did not surpass ABI-249:

1. Negative-patch clutter is materially worse than ABI-249 and ABI-184. Among 2,003 negative validation ABI Patches, ABI-279 produced at least one filtered false-positive pixel on 1,034 patches. The median negative-patch false-positive count was 2 pixels. Total negative-patch false-positive burden was 75,431 pixels, with 220 negative patches above 100 false-positive pixels, 11 above 500, and none above 1,000. The small median indicates many negative patches remain nearly clean, but the total and tail burden increased relative to ABI-249's compact-prediction behavior.
2. Positive-patch coverage improves versus ABI-249 in aggregate recall but not enough to match ABI-202. Among 1,085 positive validation ABI Patches, ABI-279 had 36 patches with zero filtered predicted-positive pixels, 159 below 0.1 filtered Dice, 237 below 0.2 filtered Dice, and 249 below 0.2 filtered recall. Median positive-patch filtered Dice was 0.4157, median precision 0.5073, and median recall 0.4316.
3. Source stratification shows viable but uneven behavior. Positive Google patches had median filtered Dice 0.4611, precision 0.5580, and recall 0.4693. Positive MIT patches had median filtered Dice 0.3843, precision 0.4515, and recall 0.3927. ABI-279 is not source-collapsed, and it slightly improves ABI-249's MIT aggregate Dice, but the Google drop versus ABI-249 contributes to the aggregate regression.
4. Connectivity is a real strength of the bridge but not a standalone promotion argument. ABI-279's filtered connectivity (0.4502) is far above ABI-249 and ABI-196 and close to ABI-202, but it comes with more clutter and lower precision. The likely failure mode is not absence of line support; it is insufficient discrimination between useful line/detail evidence and clutter when the bridge broadens predictions.

Artifact Filters removed 41,394 predicted-positive pixels, corresponding to 165,576 square kilometers under the evaluation metadata's pixel-area accounting. Raw Dice was 0.4312 versus filtered Dice 0.4165, and raw predicted-positive pixels were 660,323 versus 618,929 filtered. Filtering lowers Dice rather than creating the result, so ABI-279 is not primarily Artifact Filter-dependent. Removed pixels were concentrated on positive patches (37,905) rather than negative patches (3,489), so the filters are not hiding a large negative-patch clutter failure.

The retained diagnostic GeoTIFF samples and per-sample rows are traceability artifacts selected under the bounded evaluation policy. This note does not reproduce raw samples, coordinates, scene identifiers, or images.

## Training and resource observations

ABI-279 completed the approved late-improving budget with no contract, smoke, shape, numerical, resource, or lifecycle failure. The run used provider-approved `abi_16ch_plus_sza` input, trusted source-balanced capped selection, BCE-Dice primary loss, trusted Line and Centerline auxiliary targets, random mirroring, batch size 4, constant learning rate, disabled early stopping, and the A100 execution environment.

The selected checkpoint was epoch 22, with capped `val/filtered_dice` 0.4145, precision 0.4426, recall 0.3898, and connectivity 0.4392. The final epoch remained close on aggregate Dice (0.4135) but lower on connectivity (0.4300), confirming a finite but oscillatory late trajectory rather than a clean late rise. Resource use stayed inside policy: 8,880,854 parameters, about 8.55 GiB peak allocated CUDA memory, and about 7,997 seconds total wall time within the 10,800-second late-improving timeout.

## Interpretation

Classify ABI-279's whole-validation evaluation as valid, finite diagnostic evidence for a C4 recall/connectivity bridge, but not as a new frontier. The bridge answered the ABI-249 follow-up question: adding bounded line/detail evidence to the C4 orientation prior can raise recall and connectivity at threshold 0.5, and this effect transfers to the full Working Validation Split. However, the same mechanism dilutes ABI-249's high-precision compact-prediction behavior and does not recover enough true-positive coverage to challenge ABI-202.

ABI-279 should be retained as a C4-family recall/connectivity tradeoff comparator, while ABI-249 remains the stronger high-precision compact C4 comparator and ABI-202 remains the aggregate whole-validation filtered-Dice reference. The exact ABI-279 branch has now used a late36 budget and a whole-validation diagnostic; further unchanged continuation is not warranted.

## Decision

Do not promote ABI-279. Do not repeat ABI-279 unchanged and do not request another longer budget for the same dual-evidence recall bridge. Future C4/orientation-prior work should be mechanism-changing: preserve ABI-249's compact high-precision behavior while adding more selective recall/connectivity support, for example through a gated center-frame detail bypass, source-balanced evidence calibration, or cross-scale continuity support that suppresses negative-patch clutter without Candidate-owned thresholding, postprocessing, losses, metrics, Artifact Filters, data loading, sample selection, coordinates, or resource scheduling.

If the next step broadens away from C4, use ABI-279 as evidence that connectivity support alone is insufficient unless precision and negative-patch clutter are controlled. Prefer a new hypothesis that directly targets fixed-threshold recall without broadening false-positive tails.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260913_000141_3344db/outputs/evaluations/eval_evalreq_abi279_wholeval_failure_buckets_v1/summary.json`
- `run_20260913_000141_3344db/outputs/evaluations/eval_evalreq_abi279_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260913_000141_3344db/outputs/evaluations/eval_evalreq_abi279_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260913_000141_3344db/outputs/evaluations/eval_evalreq_abi279_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260913_000141_3344db/outputs/evaluations/eval_evalreq_abi279_wholeval_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260913_000141_3344db/outputs/best_metrics.json`
- `run_20260913_000141_3344db/outputs/final_metrics.json`
- `run_20260913_000141_3344db/outputs/metrics.jsonl`
- `run_20260913_000141_3344db/outputs/resource_profile.json`
- `run_20260913_000141_3344db/outputs/model_summary.json`
- `run_20260913_000141_3344db/resolved_manifest.yaml`
- `run_20260913_000141_3344db/candidate/budget_request.yaml`
- `run_20260911_111909_dd7ef7/outputs/evaluations/eval_evalreq_abi249_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260911_111909_dd7ef7/outputs/evaluations/eval_evalreq_abi249_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260911_111909_dd7ef7/outputs/evaluations/eval_evalreq_abi249_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260903_195527_248472/outputs/evaluations/eval_evalreq_abi196_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
