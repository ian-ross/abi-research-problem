# Full-spectral BTD+SZA cross-scale directional-consensus ASPP centerline-w005 follow-up

research-figures: []

## Scope

This note records the capped exploratory Result for ABI-213, Candidate `abi213_fullspectral_btd_sza_crossscale_directional_consensus_aspp_centerline_w005_bce_dice_line_centerline_aux_v1`, Run `run_20260904_182354_bfa5db`.

ABI-213 was a controlled auxiliary-policy continuation of the ABI-201/202 cross-scale directional-consensus ASPP branch. It kept the ABI-201 architecture unchanged and changed only the manifest-declared provider-derived Centerline auxiliary `weighted_bce` weight from 0.02 to 0.05 while keeping the Line auxiliary weight at 0.01 and trusted BCE-Dice primary loss. The intended question was whether stronger Centerline Target supervision would improve thin-line discipline, connectivity, precision, or positive-area control without sacrificing the recall and source transfer that made ABI-202 the current whole-validation aggregate reference.

The Run used provider-approved `abi_16ch_plus_sza` inputs, ABI-channel-derived BTD/SZA/cos-SZA features, trusted `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW at learning rate 0.0003, batch size 4, constant learning rate, disabled early stopping, and the 12-epoch exploratory budget. Candidate code did not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, coordinate features, sampling behavior, augmentation, training loops, runtime downloads, persistence writes, or resource scheduling.

Primary comparisons are ABI-201 `run_20260904_032624_7e855a` as the same-architecture exploratory parent, ABI-202 `run_20260904_043143_ee0005` as the late-improving same-architecture and current whole-validation reference, ABI-203 `run_20260904_073913_3edd12` as the stronger foreground-calibrated exploratory probe, ABI-210/212 as recent support-bridge probes, and ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and stricter positive-area-discipline reference.

## Capped exploratory metrics

ABI-213 completed 12/12 exploratory epochs with finite losses and non-collapsed, Dataset Source-informative predictions. The Harness selected epoch 11 as best by `val/filtered_dice`; final epoch 12 had lower validation loss but did not improve the primary metric.

| Metric | ABI-213 capped best | ABI-213 final |
| --- | ---: | ---: |
| Epoch | 11 | 12 |
| Filtered Dice | 0.3889 | 0.3810 |
| MIT filtered Dice | 0.3818 | 0.3627 |
| Google filtered Dice | 0.4063 | 0.4261 |
| Filtered precision | 0.4116 | 0.4198 |
| Filtered recall | 0.3685 | 0.3488 |
| Filtered contrail connectivity | 0.3159 | 0.3146 |
| Filtered predicted-positive fraction | 0.003244 | 0.003011 |
| Raw Dice | 0.4035 | 0.3951 |
| Raw recall | 0.3946 | 0.3728 |
| Train loss | 0.8483 | 0.8497 |
| Validation loss | 0.8831 | 0.8810 |

The trajectory was finite but not cleanly improving in the target metric. Filtered Dice rose from 0.1850 at epoch 1 to 0.3672 at epoch 6, dipped, recovered to 0.3839 at epoch 9, fell to 0.3478 at epoch 10, peaked at 0.3889 at epoch 11, and finished lower at 0.3810. Validation loss continued to edge down at epoch 12, but the primary filtered-Dice and MIT values did not finish at the budget ceiling.

## Comparison

| Run | Branch | Budget | Best epoch | Filtered Dice | MIT | Google | Precision | Recall | Connectivity | Pred-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260904_182354_bfa5db` | ABI-213 centerline weight 0.05 | exploratory | 11 | 0.3889 | 0.3818 | 0.4063 | 0.4116 | 0.3685 | 0.3159 | 0.003244 |
| `run_20260904_032624_7e855a` | ABI-201 same architecture, centerline weight 0.02 | exploratory | 12 | 0.3958 | 0.3751 | 0.4497 | 0.4587 | 0.3481 | 0.4630 | 0.002749 |
| `run_20260904_073913_3edd12` | ABI-203 foreground-calibrated same-family probe | exploratory | 12 | 0.4023 | 0.3926 | 0.4289 | 0.4332 | 0.3756 | 0.4004 | 0.003142 |
| `run_20260904_152018_ce1309` | ABI-210 compact spectral-ridge support | exploratory | 12 | 0.3952 | 0.3865 | 0.4163 | 0.3974 | 0.3931 | 0.2515 | 0.003584 |
| `run_20260904_172606_3f797b` | ABI-212 compact line-preserving coarse support | exploratory | 12 | 0.3875 | 0.3759 | 0.4172 | 0.4170 | 0.3618 | 0.3235 | 0.003144 |
| `run_20260904_043143_ee0005` | ABI-202 same architecture late-improving | late_improving | 34 | 0.4276 | 0.4120 | 0.4682 | 0.4395 | 0.4163 | 0.4578 | 0.003433 |
| `run_20260902_213856_2c04ac` | ABI-184 signed-detail line+centerline | late_improving | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.002615 |

Relative to ABI-201, stronger centerline supervision improved MIT filtered Dice by about 0.0067 and recall by about 0.0204, but the intended line-discipline gains did not appear. Aggregate filtered Dice fell by about 0.0069, Google filtered Dice fell sharply by about 0.0434, precision fell by about 0.0471, connectivity fell by about 0.1471, and the filtered predicted-positive fraction increased.

Relative to ABI-203, ABI-213 is lower on aggregate filtered Dice, both Dataset Sources, precision, recall, connectivity, and predicted-positive discipline. Relative to ABI-210, ABI-213 trades away recall and aggregate Dice for some precision/connectivity recovery, but still does not approach ABI-201/202/184 connectivity. Relative to ABI-212, ABI-213 is essentially tied on aggregate Dice while shifting toward higher MIT and recall but lower Google, precision, connectivity, and positive-area discipline.

The result therefore does not support increasing Centerline auxiliary weight to 0.05 as a standalone improvement for the ABI-201/202 architecture. It appears to bias the model toward a noisier MIT/recall operating point while weakening Google transfer and the very connectivity/line-discipline behavior the change was meant to strengthen.

## Resource and contract observations

The Run stayed inside the active Workspace Configuration: exploratory budget, 12 effective epochs, batch size 4, constant learning rate, disabled early stopping, provider-owned source-balanced capped selection, trusted random mirroring, and A100 execution. The resolved model used approved `abi_16ch_plus_sza` input mode, excluded forbidden longitude/latitude source channels, and emitted `mask_logits`, `line_logits`, and `centerline_logits`.

The model summary reports 8,172,287 parameters, under the 25,000,000-parameter ceiling. Resource profiling completed successfully with peak CUDA allocation of 10,452,130,304 bytes, peak reserved CUDA memory of 11,892,948,992 bytes, and total Run wall time of 3,314.8 seconds. This is within the 3,600-second exploratory timeout but close enough that broader/heavier variants of this exact architecture should remain sequential and conservative.

## Interpretation

Classify ABI-213 as a valid, finite, scientifically negative capped exploratory Result for this exact auxiliary-weight direction. It is not a Candidate bug, contract violation, Resource Failure, Harness Failure, unknown failure, or evidence against the whole ABI-201/202 cross-scale directional-consensus ASPP family.

The branch answered a narrow policy question: raising centerline auxiliary weight from 0.02 to 0.05 does not improve the line-discipline tradeoff of the same architecture under the exploratory cap. The finite epoch-11 selection near the budget ceiling is not enough for a late36 request because the selected Result is below ABI-201/203 on aggregate filtered Dice and well below ABI-201/202/184 on connectivity and Google performance. The final epoch also regressed in the primary metric despite lower validation loss.

The useful lesson is that stronger centerline supervision can increase MIT/recall evidence but may over-constrain or miscalibrate the shared decoder in a way that harms source transfer and continuity. Further ABI-202-family work should avoid simply increasing auxiliary weights and instead use architecture-local mechanisms that preserve the high-connectivity signed-detail/ASPP line path while constraining clutter more narrowly.

## Decision

Do not promote ABI-213, do not request whole-validation diagnostics for this exact Run, and do not request a late36 continuation for this exact centerline-w005 auxiliary-policy branch.

Retain ABI-202 as the current whole-validation-tested aggregate filtered-Dice reference, ABI-184 as the precision/connectivity and positive-area-discipline reference, ABI-203 as the stronger same-family exploratory foreground-calibration probe, and ABI-201 as the better same-architecture exploratory baseline. Treat ABI-213 as negative evidence against further standalone Centerline auxiliary weight increases.

A reasonable next in-contract hypothesis is to broaden away from auxiliary-weight escalation and broad support expansion: either a conservative ABI-202-family continuation that applies narrow clutter modulation without overwriting signed-detail line features, or a new sequential architecture scout focused on thin-line continuity refinement with recall-preserving context. Candidate code must continue to use only provider-approved ABI/SZA inputs and must not implement data loading, losses, metrics, Artifact Filters, thresholding, sampling behavior, augmentation, coordinate features, or resource scheduling.

No Capability Request, Evaluation Request, or Campaign Report is required from this Result.

## Artifact references

- `run_20260904_182354_bfa5db/outputs/best_metrics.json`
- `run_20260904_182354_bfa5db/outputs/final_metrics.json`
- `run_20260904_182354_bfa5db/outputs/metrics.jsonl`
- `run_20260904_182354_bfa5db/outputs/resource_profile.json`
- `run_20260904_182354_bfa5db/outputs/model_summary.json`
- `run_20260904_182354_bfa5db/outputs/prediction_samples/samples.json`
- `run_20260904_182354_bfa5db/resolved_manifest.yaml`
- `run_20260904_182354_bfa5db/candidate/PROPOSAL.md`
- `run_20260904_032624_7e855a/outputs/best_metrics.json`
- `run_20260904_073913_3edd12/outputs/best_metrics.json`
- `run_20260904_152018_ce1309/outputs/best_metrics.json`
- `run_20260904_172606_3f797b/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
