# Full-spectral BTD+SZA directional message-passing U-Net scout

research-figures: []

## Scope

This note records the capped exploratory Result for ABI-207, Candidate `abi207_fullspectral_btd_sza_directional_message_passing_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260904_120216_3ffbda`.

ABI-207 was a materially different architecture-family scout. It broadened away from the ABI-201/202 cross-scale directional-consensus ASPP branch and recent local auxiliary/gating follow-ups by testing a compact multi-scale directional message-passing U-Net. The Candidate used provider-approved `abi_16ch_plus_sza` input, ABI-channel-derived BTD features, normalized/cosine Solar Geometry features, trusted BCE-Dice primary loss, provider-derived Line and Centerline auxiliary targets, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW at 0.0003, batch size 4, constant learning rate, disabled early stopping, and the default 12-epoch exploratory budget.

Primary comparisons are ABI-201 `run_20260904_032624_7e855a` as the same source-balanced exploratory reference from the cross-scale directional-consensus ASPP family, ABI-202 `run_20260904_043143_ee0005` as the late36 reference for that branch, ABI-206 `run_20260904_105645_8f8ab1` as the immediately preceding boundary-auxiliary negative follow-up, and ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference.

Candidate code did not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, coordinate features, sampling behavior, augmentation, training loops, runtime downloads, persistence writes, or resource scheduling.

## Capped exploratory metrics

ABI-207 completed 12/12 exploratory epochs with finite losses and non-collapsed, Dataset Source-informative predictions. The Harness selected epoch 12 as the best checkpoint by `val/filtered_dice`, so the final checkpoint is also the selected checkpoint.

| Metric | ABI-207 capped best/final |
| --- | ---: |
| Best epoch | 12 |
| Filtered Dice | 0.3885 |
| MIT filtered Dice | 0.3752 |
| Google filtered Dice | 0.4212 |
| Filtered precision | 0.3923 |
| Filtered recall | 0.3848 |
| Filtered contrail connectivity | 0.2911 |
| Filtered predicted-positive fraction | 0.003554 |
| Raw Dice | 0.4020 |
| Raw recall | 0.4115 |
| Train loss | 0.8486 |
| Validation loss | 0.8845 |

The validation trajectory was noisy but improving late. Filtered Dice rose from 0.2336 at epoch 1 to 0.3521 at epoch 4, oscillated through epochs 5-8, reached 0.3809 at epoch 9, dipped at epochs 10-11, and ended at its best value of 0.3885 at epoch 12. The final predicted-positive fraction remained bounded, and the model did not collapse to all-negative or all-positive output.

## Comparison

| Run | Branch | Budget | Best epoch | Filtered Dice | MIT | Google | Precision | Recall | Connectivity | Pred-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260904_032624_7e855a` | ABI-201 cross-scale directional-consensus ASPP | exploratory | 12 | 0.3958 | 0.3751 | 0.4497 | 0.4587 | 0.3481 | 0.4630 | 0.002749 |
| `run_20260904_043143_ee0005` | ABI-202 cross-scale directional-consensus ASPP | late_improving | 34 | 0.4276 | 0.4120 | 0.4682 | 0.4395 | 0.4163 | 0.4578 | 0.003433 |
| `run_20260904_105645_8f8ab1` | ABI-206 boundary auxiliary | exploratory | 12 | 0.3787 | 0.3543 | 0.4412 | 0.4655 | 0.3192 | 0.4257 | 0.002485 |
| `run_20260904_120216_3ffbda` | ABI-207 directional message-passing U-Net | exploratory | 12 | 0.3885 | 0.3752 | 0.4212 | 0.3923 | 0.3848 | 0.2911 | 0.003554 |
| `run_20260902_213856_2c04ac` | ABI-184 signed-detail line+centerline | late_improving | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.002615 |

ABI-207 is a useful positive/mixed scout rather than a promotion candidate. Relative to ABI-206, it recovers about 0.0098 aggregate filtered Dice, 0.0209 MIT filtered Dice, and 0.0656 recall, while giving up Google Dice, precision, connectivity, and area discipline. Relative to the same-budget ABI-201 exploratory reference, it is close on aggregate filtered Dice and essentially tied on MIT, but lower on Google, precision, and especially connectivity; its main advantage is higher recall. Relative to ABI-184 and ABI-202, it remains behind the stronger frontier.

The central scientific signal is that compact directional message passing can learn a competitive source-balanced mask operating point on the 12-epoch capped budget, but the implementation did not realize its intended connectivity advantage. It appears to thicken or extend recall-support more than it preserves thin continuous structures under the filtered connectivity metric.

## Resource and contract observations

The Run stayed inside the active Workspace Configuration: exploratory budget, 12 effective epochs, batch size 4, constant learning rate, disabled early stopping, provider-owned capped source-balanced selection, trusted random mirroring, and A100 execution. The resolved model summary uses approved `abi_16ch_plus_sza` input mode, excludes forbidden longitude and latitude source channels, returns `mask_logits`, `line_logits`, and `centerline_logits`, and reports 9,295,456 parameters under the 25,000,000-parameter ceiling.

Resource profiling completed successfully with about 10.49 GiB peak allocated CUDA memory, about 11.86 GiB peak reserved CUDA memory, and about 3,350 seconds total run wall time. This is within but close to the 3,600-second exploratory timeout. No contract, resource, numerical, or lifecycle failure is indicated in the Harness-observed artifacts.

## Interpretation

Classify ABI-207 as a valid, finite, scientifically mixed but useful capped exploratory Result. It is not a Candidate bug, contract violation, Resource Failure, Harness Failure, unknown failure, or evidence to abandon the new directional message-passing family after a single scout.

The result meets the scout continuation bar from its proposal: it is finite, non-collapsed, source-informative, ends at its best epoch, and lands within about 0.007 filtered Dice of the ABI-201 exploratory reference. However, the low filtered connectivity and near-timeout runtime mean the next step should not simply enlarge the model or request late36 immediately. The family needs one bounded refinement that improves precision/connectivity discipline without adding heavy post-decoder complexity or moving filtering into Candidate code.

## Decision

Do not promote ABI-207 and do not request whole-validation failure-bucket evaluation for this exact run yet. Do not request a late36 continuation for ABI-207 as the immediate next handoff, because the branch has only one exploratory scout and has not shown the connectivity strength that would make longer training clearly diagnostic.

Retain ABI-181 as the current whole-validation-tested campaign frontier, ABI-202 as the strongest capped/late reference for the cross-scale directional-consensus ASPP branch, and ABI-184 as the precision/connectivity reference. Treat ABI-207 as justification for one in-contract directional-message-passing family-development continuation focused on improving thin-line connectivity and precision at similar or lower resource cost.

A reasonable next hypothesis is to keep the ABI-207 approved input/loss/data policy but replace the broad directional residual mixing with a lighter orientation-consensus bottleneck or full-scale detail bridge that gates directional messages by local spectral/ridge agreement. The continuation should remain exploratory, avoid Candidate-owned Artifact Filters or thresholds, avoid coordinate inputs, and keep parameter/runtime risk below the ABI-207 near-timeout profile.

No Capability Request, Evaluation Request, or Campaign Report is required from this Result.

## Artifact references

- `run_20260904_120216_3ffbda/outputs/best_metrics.json`
- `run_20260904_120216_3ffbda/outputs/final_metrics.json`
- `run_20260904_120216_3ffbda/outputs/metrics.jsonl`
- `run_20260904_120216_3ffbda/outputs/resource_profile.json`
- `run_20260904_120216_3ffbda/outputs/model_summary.json`
- `run_20260904_120216_3ffbda/outputs/prediction_samples/samples.json`
- `run_20260904_120216_3ffbda/resolved_manifest.yaml`
- `run_20260904_120216_3ffbda/candidate/PROPOSAL.md`
- `run_20260904_032624_7e855a/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260904_105645_8f8ab1/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
