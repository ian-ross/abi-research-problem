# ABI-249 whole-validation failure-bucket review

research-figures: []

## Scope

This note records Harness-owned Post-Run Evaluation `eval_evalreq_abi249_wholeval_failure_buckets_v1` for ABI-249 Run `run_20260911_111909_dd7ef7`.

The evaluation request asked whether ABI-249's late36 C4 steerable line-context U-Net capped-best result (0.4164 `val/filtered_dice` at epoch 31) transfers beyond the trusted representative validation cap, and whether whole-validation failure buckets show a robust precision-preserving rotation-aware line-context tradeoff without excessive Artifact Filter dependence. This is diagnostic evidence only; promotion remains operator-reviewed.

Primary comparison references:

- ABI-249 C4 steerable line-context U-Net late36 Run: `run_20260911_111909_dd7ef7`, Evaluation `eval_evalreq_abi249_wholeval_failure_buckets_v1`
- ABI-248 exploratory C4 parent Run: `run_20260911_102833_5db7f8`
- ABI-202 current whole-validation aggregate reference: `run_20260904_043143_ee0005`, Evaluation `eval_evalreq_abi202_wholeval_failure_buckets_v1`
- ABI-196 prior late36 aggregate reference: `run_20260903_195527_248472`, Evaluation `eval_evalreq_abi196_wholeval_failure_buckets_v1`
- ABI-184 precision/connectivity and negative-patch-discipline reference: `run_20260902_213856_2c04ac`, Evaluation `eval_evalreq_abi184_wholeval_failure_buckets_v1`
- Canonical MCAST 1.1 and MCAST 2.1 summaries from `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`

## Whole-validation metrics

At threshold 0.5 on the full 3,088-sample Working Validation Split, ABI-249 reached:

| Metric | ABI-249 whole validation |
| --- | ---: |
| Filtered Dice | 0.4197 |
| MIT filtered Dice | 0.3991 |
| Google filtered Dice | 0.4601 |
| Filtered precision | 0.4865 |
| Filtered recall | 0.3690 |
| Filtered contrail connectivity | 0.3975 |
| Filtered predicted-positive pixels | 538,008 |
| Filtered false-positive pixels | 276,246 |
| Filtered false-negative pixels | 447,601 |
| Raw Dice | 0.4353 |

ABI-249's capped signal transferred to whole validation as a strong but not frontier-best Result. Whole-validation filtered Dice (0.4197) is slightly above the capped best checkpoint (0.4164), Google filtered Dice is close to the capped value (0.4601 whole versus 0.4689 capped), and MIT filtered Dice is also close (0.3991 whole versus 0.3964 capped). The branch is finite, source-informative, and non-collapsed on the canonical Working Validation Split.

Relative to ABI-202, ABI-249 remains below the aggregate whole-validation frontier by about -0.0115 filtered Dice. It is stronger on precision (0.4865 versus 0.4431) and predicts a much smaller filtered-positive area (538,008 versus 672,206 pixels), but gives up recall (0.3690 versus 0.4199), connectivity (0.3975 versus 0.4625), MIT filtered Dice (0.3991 versus 0.4141), and slightly Google filtered Dice (0.4601 versus 0.4644). This makes ABI-249 a high-precision/compact-prediction comparator rather than a replacement for ABI-202.

Relative to ABI-196, ABI-249 improves aggregate filtered Dice (0.4197 versus 0.4147), Google filtered Dice (0.4601 versus 0.4368), precision (0.4865 versus 0.4379), connectivity (0.3975 versus 0.3827), and false-positive burden, but gives up MIT filtered Dice (0.3991 versus 0.4026) and recall (0.3690 versus 0.3938). Relative to ABI-184, ABI-249 improves aggregate and Google filtered Dice and positive-patch miss tails, but ABI-184 remains slightly higher precision and much stronger connectivity/negative-patch discipline.

Against canonical MCAST context, ABI-249's filtered Dice 0.4197 is above MCAST 1.1 (0.3842) and MCAST 2.1 (0.3873). ABI-249's precision exceeds both MCAST references, its recall is above MCAST 1.1 but below MCAST 2.1, and its connectivity is below MCAST 1.1 but above MCAST 2.1. This is comparison context only, not a promotion claim.

## Threshold behavior

The threshold sweep shows substantial diagnostic headroom at lower thresholds. Filtered Dice improves from 0.4197 at threshold 0.5 to 0.4337 at threshold 0.05, with precision 0.4112 and recall 0.4589. The closest filtered precision/recall balance is threshold 0.10, with Dice 0.4336, precision 0.4364, recall 0.4308, and a 0.0055 absolute precision/recall gap. Raw Dice similarly improves from 0.4353 at threshold 0.5 to 0.4480 at threshold 0.10.

This does not authorize Candidate-owned thresholding, calibration, postprocessing, losses, metrics, or Artifact Filters. The design lesson is that ABI-249 learned a conservative fixed-threshold operating point: the orientation prior suppresses clutter and keeps precision high at 0.5, while lower-threshold diagnostics suggest recoverable recall if a future architecture can shift useful contrail evidence upward without simply changing the threshold.

## Failure-bucket observations

Failure buckets show that ABI-249 trades ABI-202-like recall for compact high-precision predictions and better clutter control:

1. Negative-patch clutter is better in total area than ABI-202/ABI-196 but not as clean as ABI-184. Among 2,003 negative validation ABI Patches, ABI-249 produced at least one filtered predicted-positive pixel on 1,217 patches. Median negative-patch false-positive count was 11 pixels. Total negative-patch false-positive pixels were 66,218, with 148 negative patches above 100 filtered false-positive pixels, 5 above 500, and none above 1,000. The total negative false-positive burden is below ABI-202's 71,310 and ABI-196's 88,298, but ABI-184 remains cleaner with 53,814 total, 946 any-FP negative patches, and median zero false-positive pixels.
2. Positive-patch miss tails are competitive but recall-limited. ABI-249 had 29 positive validation patches with zero filtered predicted-positive pixels, 167 positive patches below 0.1 filtered Dice, 227 below 0.2 filtered Dice, and 280 below 0.2 filtered recall. The zero-prediction and low-Dice tails improve ABI-202, ABI-196, and ABI-184, but the low-recall tail is worse than ABI-202 and ABI-196. This matches the aggregate pattern: ABI-249 often finds something on positive patches, but at threshold 0.5 it under-covers enough contrail pixels to trail ABI-202.
3. Median positive-patch quality is a strength, especially on Google. ABI-249's median positive-patch filtered Dice was 0.4310, median precision 0.5580, and median recall 0.3978. By Dataset Source, median positive-patch filtered Dice was 0.3912 on MIT and 0.4787 on Google; median precision was 0.4826 on MIT and 0.6079 on Google; median recall was 0.3636 on MIT and 0.4469 on Google. ABI-249 slightly exceeds ABI-202 on median positive Dice, but ABI-202 remains much stronger on median recall.

Artifact Filters removed 35,506 predicted-positive pixels over the full split, corresponding to 142,024 square kilometers under the evaluation metadata's pixel-area accounting. Raw Dice was 0.4353 versus filtered Dice 0.4197, and raw predicted-positive pixels were 573,514 versus 538,008 filtered. Filtering lowers Dice modestly rather than creating the result, and ABI-249 is not primarily Artifact Filter-dependent.

The retained diagnostic sample GeoTIFFs are traceability artifacts selected under the bounded evaluation policy. This note does not reproduce individual scene identifiers, coordinates, raw samples, or images.

## Training trajectory and resource observations

ABI-249 completed 36/36 late-improving epochs with finite losses and non-collapsed, Dataset Source-informative predictions. The Harness approved the candidate-local `late_improving` budget request against parent Run `run_20260911_102833_5db7f8`; effective max epochs were 36 and the Docker wall-clock budget was 10,800 seconds.

The best selected checkpoint occurred at epoch 31. The late trajectory was productive and validated the extended-budget request: ABI-248's exploratory endpoint was 0.3838 capped `val/filtered_dice`, while ABI-249 reached 0.4164 capped best validation and 0.4197 whole-validation filtered Dice. The final epoch remained close to the selected checkpoint on aggregate Dice while shifting toward higher recall and lower precision, indicating volatility but not collapse.

The Run stayed inside the active Workspace Configuration: approved late-improving budget, batch size 4, constant learning rate, disabled early stopping, provider-owned source-balanced capped selection, trusted random mirroring, and A100 execution. The resolved manifest uses approved `abi_16ch_plus_sza` input mode; forbidden longitude and latitude source channels are excluded; outputs are `mask_logits`, `line_logits`, and `centerline_logits`; and the model summary reports 8,802,052 parameters under the 25,000,000-parameter ceiling. Resource profiling completed successfully with about 7.70 GiB peak allocated CUDA memory and about 7,642 seconds total run wall time, within the late-improving timeout. No contract, resource, numerical, or lifecycle failure is indicated in the Harness-observed artifacts.

## Interpretation

Classify ABI-249's whole-validation evaluation as valid, finite, non-collapsed diagnostic evidence for the rotation-aware C4 steerable line-context family. The late36 continuation was worthwhile and converted ABI-248 from a mid-0.38 capped scout into a whole-validation Result that exceeds ABI-196 on aggregate filtered Dice while preserving a compact, high-precision prediction style.

ABI-249 should enter the whole-validation-tested frontier as a serious high-precision/Google-strength comparator, but it should not replace ABI-202 as the aggregate reference. ABI-202 remains better on aggregate filtered Dice, MIT filtered Dice, recall, and connectivity. ABI-184 remains the strict negative-patch-discipline and connectivity reference. ABI-249's main remaining weakness is fixed-threshold recall/coverage, especially on MIT, not instability or Artifact Filter dependence.

The C4 family is sufficiently characterized as an orientation-prior mechanism. The next C4-related branch should be mechanism-changing rather than an unchanged epoch or auxiliary-head repeat: it should attempt to recover recall/connectivity while retaining ABI-249's compact high-precision behavior.

## Decision

Do not promote ABI-249 or reinterpret this whole-validation diagnostic as deployment evidence. Retain ABI-202 as the current aggregate whole-validation filtered-Dice reference; retain ABI-184 as the negative-patch-discipline/connectivity reference; add ABI-249 as a high-precision and compact-prediction C4 orientation-prior comparator that also improves ABI-196's aggregate full-validation Dice.

Do not repeat ABI-249 unchanged and do not request another longer budget for the same exact branch. A reasonable next in-contract hypothesis is a recall-preserving architecture continuation that combines ABI-249's C4 steerable line-context with stronger high-resolution support, such as a center-anchored detail bypass, cross-scale support bridge, or compact logit-calibration head that raises true contrail evidence without Candidate-owned thresholding or postprocessing. If the next step broadens instead, prioritize another underexplored family rather than more local auxiliary-head shuffling.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_111909_dd7ef7/outputs/evaluations/eval_evalreq_abi249_wholeval_failure_buckets_v1/summary.json`
- `run_20260911_111909_dd7ef7/outputs/evaluations/eval_evalreq_abi249_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260911_111909_dd7ef7/outputs/evaluations/eval_evalreq_abi249_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260911_111909_dd7ef7/outputs/evaluations/eval_evalreq_abi249_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260911_111909_dd7ef7/outputs/evaluations/eval_evalreq_abi249_wholeval_failure_buckets_v1/diagnostic_samples/samples.json`
- `run_20260911_111909_dd7ef7/outputs/best_metrics.json`
- `run_20260911_111909_dd7ef7/outputs/final_metrics.json`
- `run_20260911_111909_dd7ef7/outputs/metrics.jsonl`
- `run_20260911_111909_dd7ef7/outputs/resource_profile.json`
- `run_20260911_111909_dd7ef7/outputs/model_summary.json`
- `run_20260911_111909_dd7ef7/resolved_manifest.yaml`
- `run_20260911_111909_dd7ef7/candidate/budget_request.yaml`
- `run_20260911_102833_5db7f8/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260903_195527_248472/outputs/evaluations/eval_evalreq_abi196_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260903_195527_248472/outputs/evaluations/eval_evalreq_abi196_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
