# Full-spectral BTD+SZA cross-scale directional-consensus ASPP foreground-calibrated follow-up

research-figures: []

## Scope

This note records the capped exploratory Result for ABI-203, Candidate `abi203_fullspectral_btd_sza_crossscale_directional_consensus_aspp_foreground_calibrated_bce_dice_line_centerline_aux_v1`, Run `run_20260904_073913_3edd12`.

ABI-203 was a controlled family-development continuation of ABI-202. It kept provider-approved `abi_16ch_plus_sza` input, deterministic ABI-channel brightness-temperature-difference features, trusted `bce_dice`, trusted Line and Centerline auxiliary targets, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW at 0.0003, batch size 4, constant learning rate, disabled early stopping, and the 12-epoch exploratory budget. The architecture-only change was replacing ABI-202's plain mask head with a bounded learned `ForegroundCalibrationMaskHead` residual intended to reduce unsupported foreground clutter without implementing thresholding, postprocessing, Artifact Filters, custom losses, target transforms, sampling behavior, or coordinate features.

Primary comparison target is ABI-202 `run_20260904_043143_ee0005`, the current whole-validation aggregate filtered-Dice reference after late36 and failure-bucket evaluation. Secondary references are ABI-201 `run_20260904_032624_7e855a`, the exploratory parent, and ABI-184 `run_20260902_213856_2c04ac`, the precision/connectivity and strict negative-patch-discipline reference.

## Capped exploratory metrics

ABI-203 completed 12/12 exploratory epochs with finite losses and non-collapsed, Dataset Source-informative predictions. The Harness selected epoch 12 as the best checkpoint by `val/filtered_dice`, so the selected and final operating points are the same.

| Metric | ABI-203 capped best |
| --- | ---: |
| Best epoch | 12 |
| Filtered Dice | 0.4023 |
| MIT filtered Dice | 0.3926 |
| Google filtered Dice | 0.4289 |
| Filtered precision | 0.4332 |
| Filtered recall | 0.3756 |
| Filtered contrail connectivity | 0.4004 |
| Filtered predicted-positive fraction | 0.003142 |
| Raw Dice | 0.4171 |
| Raw recall | 0.4027 |
| Train loss | 0.8475 |
| Validation loss | 0.8838 |

The training trajectory was finite and improved late, but did not show a new stronger tradeoff. Filtered Dice rose from 0.1835 at epoch 1 to 0.3683 at epoch 6, fluctuated through epochs 7-11, and peaked at 0.4023 at epoch 12. The last-epoch best checkpoint means the head did not plateau early, but the selected checkpoint remains well below ABI-202's late36 selected checkpoint.

## Comparison

| Run | Branch | Budget | Best epoch | Filtered Dice | MIT | Google | Precision | Recall | Connectivity | Pred-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260904_032624_7e855a` | ABI-201 cross-scale directional consensus | exploratory | 12 | 0.3958 | 0.3751 | 0.4497 | 0.4587 | 0.3481 | 0.4630 | 0.002749 |
| `run_20260904_043143_ee0005` | ABI-202 cross-scale directional consensus late36 | late_improving | 34 | 0.4276 | 0.4120 | 0.4682 | 0.4395 | 0.4163 | 0.4578 | 0.003433 |
| `run_20260904_073913_3edd12` | ABI-203 foreground-calibrated head | exploratory | 12 | 0.4023 | 0.3926 | 0.4289 | 0.4332 | 0.3756 | 0.4004 | 0.003142 |
| `run_20260902_213856_2c04ac` | ABI-184 signed-detail line+centerline | late_improving | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.002615 |

Relative to ABI-201, ABI-203 improves aggregate filtered Dice by about 0.0065, MIT filtered Dice by about 0.0175, and recall by about 0.0275. Those gains come at the cost of worse Google filtered Dice, precision, connectivity, and predicted-positive discipline. This is a mixed exploratory improvement over the 12-epoch parent, not a clean continuation win.

Relative to ABI-202, ABI-203 is a clear regression on the capped selected checkpoint: filtered Dice is lower by about 0.0252, MIT by about 0.0194, Google by about 0.0393, precision by about 0.0063, recall by about 0.0407, and connectivity by about 0.0574. The foreground-calibrated head reduces filtered predicted-positive fraction modestly from 0.003433 to 0.003142, but this reduction does not translate into better precision and is accompanied by substantial recall/connectivity loss. Relative to ABI-184, ABI-203 is slightly higher on MIT and recall but remains lower on aggregate, Google, precision, connectivity, and positive-area discipline.

## Resource and contract observations

The Run stayed inside the active Workspace Configuration: exploratory budget, 12 effective epochs, batch size 4, constant learning rate, disabled early stopping, provider-owned source-balanced capped selection, provider-owned random mirroring, and A100 execution. The resolved manifest uses approved `abi_16ch_plus_sza` input mode; forbidden longitude and latitude source channels are excluded; outputs are `mask_logits`, `line_logits`, and `centerline_logits`; and the model summary reports 8,201,089 parameters under the 25,000,000-parameter ceiling.

Resource profiling completed successfully with about 10.09 GiB peak allocated CUDA memory, about 11.57 GiB peak reserved CUDA memory, and about 3,442 seconds total run wall time, inside but close to the 3,600-second exploratory timeout. No contract, resource, numerical, or lifecycle failure is indicated in the Harness-observed artifacts.

## Failure classification

Classify ABI-203 as a valid finite but negative/mixed research Result, not a Candidate bug, contract violation, Resource Failure, Harness Failure, unknown failure, or hard architecture-family stop. It completed cleanly and produced source-informative predictions. Scientifically, the exact foreground-calibrated mask-head modification did not achieve its proposal-specific goal: it modestly reduced positive area versus ABI-202, but did not improve precision and sacrificed too much recall, Google Dice, and connectivity.

This does not eliminate the broader cross-scale directional-consensus ASPP family, because ABI-202 remains the current whole-validation aggregate reference and ABI-201/202 already show the branch is viable. It does argue against repeating this exact foreground-calibration head unchanged or escalating ABI-203 to whole-validation diagnostics.

## Decision

Do not promote ABI-203 and do not request whole-validation failure-bucket evaluation for this exploratory checkpoint. Retain ABI-202 as the current whole-validation aggregate filtered-Dice reference and retain ABI-184 as the precision/connectivity and negative-patch-discipline reference.

For the next in-contract hypothesis, avoid another bounded residual mask-head calibration repeat unless it has a materially different mechanism and a clearer source/precision rationale. More useful frontier moves include a different false-positive-control architecture that acts before final refinement, an allowlisted loss/auxiliary policy probe, or a broader architecture family scout that preserves ABI-202's cross-source recall/connectivity without adding near-timeout resource pressure. Candidate code must continue to use approved ABI channel inputs only and must not implement thresholding, data loading, losses, metrics, Artifact Filters, sampling behavior, or coordinate features.

No Capability Request, Evaluation Request, or Campaign Report is required from this Result.

## Artifact references

- `run_20260904_073913_3edd12/outputs/best_metrics.json`
- `run_20260904_073913_3edd12/outputs/final_metrics.json`
- `run_20260904_073913_3edd12/outputs/metrics.jsonl`
- `run_20260904_073913_3edd12/outputs/resource_profile.json`
- `run_20260904_073913_3edd12/outputs/model_summary.json`
- `run_20260904_073913_3edd12/outputs/prediction_samples/samples.json`
- `run_20260904_073913_3edd12/resolved_manifest.yaml`
- `run_20260904_073913_3edd12/candidate/PROPOSAL.md`
- `run_20260904_032624_7e855a/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/per_sample_metrics.jsonl`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
