# Full-spectral BTD+SZA compact spectral-ridge support ASPP follow-up

research-figures: []

## Scope

This note records the capped exploratory Result for ABI-210, Candidate `abi210_fullspectral_btd_sza_compact_spectral_ridge_support_aspp_bce_dice_line_centerline_aux_v1`, Run `run_20260904_152018_ce1309`.

ABI-210 was a resource-safe family-development continuation after ABI-209, the full-width spectral-ridge support variant, failed with a Harness-recorded wall-clock `resource_failure`. It kept provider-approved `abi_16ch_plus_sza` inputs, ABI-channel-derived brightness-temperature-difference features, Solar Geometry Input, trusted BCE-Dice primary loss, provider-derived Line and Centerline auxiliary targets, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW at 0.0003, batch size 4, constant learning rate, disabled early stopping, and the 12-epoch exploratory budget.

The architecture-only change relative to ABI-209 was compaction: smaller learned spectral projection, base width 32 instead of 36, and a reduced broad support window in the spectral-ridge support bridge. Candidate code did not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, coordinate features, sampling behavior, augmentation, training loops, runtime downloads, persistence writes, or resource scheduling.

Primary comparisons are ABI-209 `run_20260904_141405_62591c` for resource feasibility, ABI-202 `run_20260904_043143_ee0005` as the strongest cross-scale directional-consensus ASPP reference, ABI-201 `run_20260904_032624_7e855a` as the same-family exploratory parent, ABI-203 `run_20260904_073913_3edd12` as the foreground-calibrated exploratory probe, and ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference.

## Capped exploratory metrics

ABI-210 completed 12/12 exploratory epochs with finite losses and non-collapsed, Dataset Source-informative predictions. The Harness selected epoch 12 as the best checkpoint by `val/filtered_dice`, so the final checkpoint is also the selected checkpoint.

| Metric | ABI-210 capped best/final |
| --- | ---: |
| Best epoch | 12 |
| Filtered Dice | 0.3952 |
| MIT filtered Dice | 0.3865 |
| Google filtered Dice | 0.4163 |
| Filtered precision | 0.3974 |
| Filtered recall | 0.3931 |
| Filtered contrail connectivity | 0.2515 |
| Filtered predicted-positive fraction | 0.003584 |
| Raw Dice | 0.4090 |
| Raw recall | 0.4200 |
| Train loss | 0.8474 |
| Validation loss | 0.8792 |

The trajectory was finite but volatile. Filtered Dice reached 0.3778 at epoch 8, 0.3850 at epoch 9, collapsed to a weaker 0.3352 at epoch 10, recovered to 0.3886 at epoch 11, and finished at the selected high point of 0.3952 at epoch 12. Validation loss also improved late, from 0.8930 at epoch 10 to 0.8792 at epoch 12. The late recovery shows the compact candidate was still trainable at the exploratory ceiling, but the operating point was recall-heavy and low-connectivity rather than the intended precision/area-discipline improvement.

## Comparison

| Run | Branch | Budget | Best epoch | Filtered Dice | MIT | Google | Precision | Recall | Connectivity | Pred-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260904_141405_62591c` | ABI-209 full-width spectral-ridge support | exploratory | failed after epoch 11 | 0.3695 observed | 0.3550 | 0.4052 | 0.4185 | 0.3308 | 0.2998 | 0.002864 |
| `run_20260904_152018_ce1309` | ABI-210 compact spectral-ridge support | exploratory | 12 | 0.3952 | 0.3865 | 0.4163 | 0.3974 | 0.3931 | 0.2515 | 0.003584 |
| `run_20260904_032624_7e855a` | ABI-201 cross-scale directional-consensus ASPP | exploratory | 12 | 0.3958 | 0.3751 | 0.4497 | 0.4587 | 0.3481 | 0.4630 | 0.002749 |
| `run_20260904_073913_3edd12` | ABI-203 foreground-calibrated same-family probe | exploratory | 12 | 0.4023 | 0.3926 | 0.4289 | 0.4332 | 0.3756 | 0.4004 | 0.003142 |
| `run_20260904_043143_ee0005` | ABI-202 cross-scale directional-consensus ASPP | late_improving | 34 | 0.4276 | 0.4120 | 0.4682 | 0.4395 | 0.4163 | 0.4578 | 0.003433 |
| `run_20260902_213856_2c04ac` | ABI-184 signed-detail line+centerline | late_improving | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.002615 |

ABI-210 successfully repaired the ABI-209 resource feasibility problem and exceeded ABI-209's best observed partial validation filtered Dice by about 0.0257 while completing the missing final validation. This supports the compaction as an operationally valid reformulation of the spectral-ridge support question.

Scientifically, the tradeoff is mixed and mostly negative for the exact compact bridge. Relative to ABI-201, ABI-210 is nearly tied on aggregate filtered Dice and improves MIT filtered Dice by about 0.0113 and recall by about 0.0450, but loses Google filtered Dice by about 0.0334, precision by about 0.0613, connectivity by about 0.2115, and predicted-positive discipline. Relative to ABI-203, it is lower on aggregate Dice, both Dataset Sources, precision, connectivity, and positive-area discipline, with only a recall advantage. Relative to ABI-202, it is substantially below the late-improving reference on aggregate, MIT, Google, precision, recall, and especially connectivity.

The result therefore does not show that spectral-ridge support solved the ABI-202 false-positive problem. Instead, the compact bridge shifted the model toward higher recall and a larger predicted-positive fraction while weakening continuity and Google performance.

## Resource and contract observations

The Run stayed inside the active Workspace Configuration: exploratory budget, 12 effective epochs, batch size 4, constant learning rate, disabled early stopping, provider-owned source-balanced capped selection, trusted random mirroring, and A100 execution. The resolved model summary uses approved `abi_16ch_plus_sza` input mode; forbidden longitude and latitude source channels are excluded; outputs are `mask_logits`, `line_logits`, and `centerline_logits`; and the model summary reports 6,485,723 parameters under the 25,000,000-parameter ceiling.

Resource profiling completed successfully with about 10.62 GiB peak allocated CUDA memory, about 12.16 GiB peak reserved CUDA memory, and about 3,110 seconds total run wall time. This is within the 3,600-second exploratory timeout, unlike ABI-209, but remains close enough to the limit that larger local variants should not be batched or expanded without new resource evidence. No contract, numerical, or lifecycle failure is indicated in the Harness-observed ABI-210 artifacts.

## Interpretation

Classify ABI-210 as a valid, finite, resource-repairing but scientifically mixed capped exploratory Result. It is not a Candidate bug, contract violation, Resource Failure, Harness Failure, unknown failure, or a hard stop for all ABI-202 descendants.

The compaction achieved the operational goal of turning ABI-209's wall-clock-failed spectral-ridge support into a completed 12-epoch Run. However, it did not achieve the scientific goal of improving precision or predicted-positive discipline while preserving ABI-202/203 recall and connectivity. The final-epoch best checkpoint and late recovery make the trajectory ambiguous rather than plateau-proven, but the selected operating point is below ABI-202 and ABI-203 and has poor connectivity. That is not enough evidence to justify an immediate late36 request for this exact compact spectral-ridge support branch.

The useful design lesson is that representation-level clutter support must not dilute the line-continuity path. A spectral/ridge support cue may still be useful if used more narrowly, but the current compact bridge behaves like a recall-biased support expander rather than a precision-preserving clutter controller.

## Decision

Do not promote ABI-210, do not request whole-validation failure-bucket evaluation for this exact Run, and do not request a late36 continuation for this exact compact spectral-ridge support branch as the next handoff.

Retain ABI-202 as the current whole-validation-tested aggregate filtered-Dice reference, ABI-184 as the precision/connectivity and stricter negative-patch-discipline reference, and ABI-203 as the stronger same-family exploratory foreground-calibration probe. Treat ABI-210 as resource-feasibility evidence and as negative evidence against further broad spectral-ridge support expansion under the current exploratory envelope.

A reasonable next in-contract hypothesis is to broaden away from this local support-expansion branch: either a new architecture scout that separates coarse contrail-support estimation from thin-line continuity refinement, or a more conservative ABI-202 continuation where spectral evidence modulates only high-confidence clutter features and cannot overwrite the signed-detail/ASPP line path. Candidate code must continue to use only provider-approved ABI/SZA inputs and must not implement data loading, losses, metrics, Artifact Filters, thresholding, sampling behavior, augmentation, coordinate features, or resource scheduling.

No Capability Request, Evaluation Request, or Campaign Report is required from this Result.

## Artifact references

- `run_20260904_152018_ce1309/outputs/best_metrics.json`
- `run_20260904_152018_ce1309/outputs/final_metrics.json`
- `run_20260904_152018_ce1309/outputs/metrics.jsonl`
- `run_20260904_152018_ce1309/outputs/resource_profile.json`
- `run_20260904_152018_ce1309/outputs/model_summary.json`
- `run_20260904_152018_ce1309/outputs/prediction_samples/samples.json`
- `run_20260904_152018_ce1309/resolved_manifest.yaml`
- `run_20260904_152018_ce1309/candidate/PROPOSAL.md`
- `run_20260904_141405_62591c/outputs/metrics.jsonl`
- `run_20260904_141405_62591c/outputs/logs/harness_timeout.log`
- `run_20260904_032624_7e855a/outputs/best_metrics.json`
- `run_20260904_073913_3edd12/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
