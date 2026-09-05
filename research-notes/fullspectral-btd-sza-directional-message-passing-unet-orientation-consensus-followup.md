# Full-spectral BTD+SZA directional message-passing U-Net orientation-consensus follow-up

research-figures: []

## Scope

This note records the capped exploratory Result for ABI-208, Candidate `abi208_fullspectral_btd_sza_directional_message_passing_unet_orientation_consensus_bce_dice_line_centerline_aux_v1`, Run `run_20260904_130809_8896f4`.

ABI-208 was a family-development continuation of ABI-207. It kept the provider-approved `abi_16ch_plus_sza` input mode, ABI-channel-derived brightness-temperature-difference features, Solar Geometry Input, trusted BCE-Dice primary loss, provider-derived Line and Centerline auxiliary targets, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW at 0.0003, batch size 4, constant learning rate, disabled early stopping, and the default 12-epoch exploratory budget. The intended change was to replace ABI-207's broad directional residual message mixing with a lighter soft orientation-consensus message block and smaller base width.

Primary comparisons are ABI-207 `run_20260904_120216_3ffbda` as the same directional-message-passing family scout, ABI-201 `run_20260904_032624_7e855a` and ABI-202 `run_20260904_043143_ee0005` as cross-scale directional-consensus ASPP references, and ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference.

Candidate code did not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, coordinate features, sampling behavior, augmentation, training loops, runtime downloads, persistence writes, or resource scheduling.

## Capped exploratory metrics

ABI-208 completed 12/12 exploratory epochs with finite losses and non-collapsed, Dataset Source-informative predictions. The Harness selected epoch 9 as the best checkpoint by `val/filtered_dice`.

| Metric | ABI-208 capped best | ABI-208 final |
| --- | ---: | ---: |
| Epoch | 9 | 12 |
| Filtered Dice | 0.3739 | 0.3599 |
| MIT filtered Dice | 0.3557 | 0.3474 |
| Google filtered Dice | 0.4206 | 0.3902 |
| Filtered precision | 0.4437 | 0.4010 |
| Filtered recall | 0.3230 | 0.3264 |
| Filtered contrail connectivity | 0.3711 | 0.2479 |
| Filtered predicted-positive fraction | 0.002638 | 0.002950 |
| Raw Dice | 0.3882 | 0.3740 |
| Raw recall | 0.3449 | 0.3491 |
| Train loss | 0.8564 | 0.8540 |
| Validation loss | 0.8900 | 0.8873 |

The trajectory was finite but unstable after the best checkpoint. Filtered Dice rose from 0.1953 at epoch 1 to 0.3149 at epoch 4, produced a high-precision/high-connectivity but low-recall point at epoch 5, recovered to 0.3545 at epoch 6, peaked at 0.3739 at epoch 9, then declined to 0.3568, 0.3486, and 0.3599 across epochs 10-12. Validation loss continued a small downward trend, but the primary metric and connectivity did not finish at the budget ceiling.

## Comparison

| Run | Branch | Budget | Best epoch | Filtered Dice | MIT | Google | Precision | Recall | Connectivity | Pred-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260904_120216_3ffbda` | ABI-207 directional message-passing U-Net | exploratory | 12 | 0.3885 | 0.3752 | 0.4212 | 0.3923 | 0.3848 | 0.2911 | 0.003554 |
| `run_20260904_130809_8896f4` | ABI-208 orientation-consensus continuation | exploratory | 9 | 0.3739 | 0.3557 | 0.4206 | 0.4437 | 0.3230 | 0.3711 | 0.002638 |
| `run_20260904_032624_7e855a` | ABI-201 cross-scale directional-consensus ASPP | exploratory | 12 | 0.3958 | 0.3751 | 0.4497 | 0.4587 | 0.3481 | 0.4630 | 0.002749 |
| `run_20260904_043143_ee0005` | ABI-202 cross-scale directional-consensus ASPP | late_improving | 34 | 0.4276 | 0.4120 | 0.4682 | 0.4395 | 0.4163 | 0.4578 | 0.003433 |
| `run_20260902_213856_2c04ac` | ABI-184 signed-detail line+centerline | late_improving | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.002615 |

ABI-208 achieved the intended precision/area-discipline direction relative to ABI-207: best-checkpoint precision improved by about 0.0514, connectivity improved by about 0.0800, and filtered predicted-positive fraction dropped by about 0.000916. However, the tradeoff was unfavorable for aggregate performance: filtered Dice fell by about 0.0146, MIT filtered Dice by about 0.0195, and recall by about 0.0617. Google filtered Dice was essentially tied with ABI-207 at the best checkpoint, but still below ABI-201/202 and ABI-184.

Relative to ABI-201, ABI-208 is lower on aggregate Dice, MIT, Google, precision, recall, and connectivity. Relative to ABI-184, it matches the low-area discipline but remains less precise, less connected, lower recall, and lower on both Dataset Sources. The result suggests that soft orientation consensus can suppress diffuse over-prediction and recover some connectivity compared with ABI-207, but it over-constrains the support and does not supply enough source-balanced recall.

## Resource and contract observations

The Run stayed inside the active Workspace Configuration: exploratory budget, 12 effective epochs, batch size 4, constant learning rate, disabled early stopping, provider-owned source-balanced capped selection, trusted random mirroring, and A100 execution. The resolved model summary uses approved `abi_16ch_plus_sza` input mode; forbidden longitude and latitude source channels are excluded; outputs are `mask_logits`, `line_logits`, and `centerline_logits`; and the model summary reports 7,197,400 parameters under the 25,000,000-parameter ceiling.

Resource profiling completed successfully with about 10.64 GiB peak allocated CUDA memory, about 11.66 GiB peak reserved CUDA memory, and about 3,406 seconds total run wall time. This is within but close to the 3,600-second exploratory timeout. No contract, resource, numerical, or lifecycle failure is indicated in the Harness-observed artifacts.

## Interpretation

Classify ABI-208 as a valid, finite, scientifically mixed but negative capped exploratory Result for this exact orientation-consensus message block. It is not a Candidate bug, contract violation, Resource Failure, Harness Failure, unknown failure, or a reason to abandon all directional-message-passing ideas after two exploratory Runs.

The orientation-consensus block solved part of ABI-207's failure mode by improving precision, connectivity, and predicted-positive area discipline, but the recall and MIT penalties are too large and the best epoch occurred at epoch 9 rather than near the exploratory ceiling. This does not meet the bar for a late36 continuation of ABI-208: prior late-improving requests should be close continuations with strong or still-improving exploratory evidence near the final epoch, while this branch regressed after its peak and remains below ABI-201/202 and ABI-184.

The broader scientific signal is that over-regularized directional consensus is not enough on its own. Successful branches still need the full-scale signed/detail and cross-scale ASPP paths that preserve weak thin-contrail support before constraining it. The current evidence favors using orientation-aware features as a limited support cue, not as the main message-passing mechanism.

## Decision

Do not promote ABI-208, do not request whole-validation failure-bucket evaluation for this exact Run, and do not request a late36 continuation for this exact branch as the next handoff.

Retain ABI-181 as the current whole-validation-tested campaign frontier, ABI-202 as the strongest capped/late cross-scale directional-consensus ASPP reference, ABI-184 as the precision/connectivity reference, and ABI-207 as the better directional-message-passing recall scout. Treat ABI-208 as evidence against further local orientation-consensus tightening in the message-passing U-Net branch unless paired with a stronger recall-preserving feature path.

A reasonable next hypothesis is to return to the stronger ABI-202/203 cross-scale directional-consensus ASPP frontier and develop a recall-preserving, representation-level clutter-control variant, or to scout a different architecture family that separates coarse contrail support from thin-line refinement without making orientation consensus the bottleneck. Candidate code must continue to use only provider-approved ABI inputs and must not implement data loading, losses, metrics, Artifact Filters, thresholding, sampling, augmentation, coordinate features, or resource scheduling.

No Capability Request, Evaluation Request, or Campaign Report is required from this Result.

## Artifact references

- `run_20260904_130809_8896f4/outputs/best_metrics.json`
- `run_20260904_130809_8896f4/outputs/final_metrics.json`
- `run_20260904_130809_8896f4/outputs/metrics.jsonl`
- `run_20260904_130809_8896f4/outputs/resource_profile.json`
- `run_20260904_130809_8896f4/outputs/model_summary.json`
- `run_20260904_130809_8896f4/outputs/prediction_samples/samples.json`
- `run_20260904_130809_8896f4/resolved_manifest.yaml`
- `run_20260904_130809_8896f4/candidate/PROPOSAL.md`
- `run_20260904_120216_3ffbda/outputs/best_metrics.json`
- `run_20260904_032624_7e855a/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
