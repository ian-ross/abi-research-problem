# Full-spectral BTD+SZA cross-scale directional-consensus ASPP support-gated refiner follow-up

research-figures: []

## Scope

This note records the capped exploratory Result for ABI-204, Candidate `abi204_fullspectral_btd_sza_crossscale_directional_consensus_aspp_support_gated_refiner_bce_dice_line_centerline_aux_v1`, Run `run_20260904_084637_a1c72c`.

ABI-204 was a controlled family-development continuation of ABI-202/203. It kept provider-approved `abi_16ch_plus_sza` input, deterministic ABI-channel brightness-temperature-difference features, trusted `bce_dice`, trusted Line and Centerline auxiliary targets, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW at 0.0003, batch size 4, constant learning rate, disabled early stopping, and the 12-epoch exploratory budget. The architecture-only change replaced the ordinary line-aware refinement stage with a feature-space `SupportGatedLineAwareRefinement` module intended to suppress unsupported clutter before the final mask, line, and centerline heads. Candidate code did not implement data loading, losses, metrics, target derivation, Artifact Filters, thresholding, postprocessing, coordinate features, training loops, runtime downloads, or resource scheduling.

Primary comparison targets are ABI-202 `run_20260904_043143_ee0005`, the late36 cross-scale directional-consensus whole-validation reference, and ABI-203 `run_20260904_073913_3edd12`, the negative foreground-calibrated mask-head follow-up. Secondary references are ABI-201 `run_20260904_032624_7e855a`, the 12-epoch exploratory parent, and ABI-184 `run_20260902_213856_2c04ac`, retained as the precision/connectivity and negative-patch-discipline reference.

## Capped exploratory metrics

ABI-204 completed 12/12 exploratory epochs with finite losses and non-collapsed, Dataset Source-informative predictions. The Harness selected epoch 12 as the best checkpoint by `val/filtered_dice`, so the selected and final operating points are the same.

| Metric | ABI-204 capped best |
| --- | ---: |
| Best epoch | 12 |
| Filtered Dice | 0.3726 |
| MIT filtered Dice | 0.3631 |
| Google filtered Dice | 0.3961 |
| Filtered precision | 0.4327 |
| Filtered recall | 0.3272 |
| Filtered contrail connectivity | 0.2782 |
| Filtered predicted-positive fraction | 0.002740 |
| Raw Dice | 0.3872 |
| Raw recall | 0.3493 |
| Train loss | 0.8497 |
| Validation loss | 0.8852 |

The trajectory was finite but not compelling. Filtered Dice rose from 0.1927 at epoch 1 to 0.3411 at epoch 4, oscillated, reached 0.3628 at epoch 7, dipped again, and only peaked at 0.3726 at epoch 12. The last-epoch peak means the run was not an early plateau, but the branch remained substantially below the comparison targets and did not recover ABI-202/203 connectivity.

## Comparison

| Run | Branch | Budget | Best epoch | Filtered Dice | MIT | Google | Precision | Recall | Connectivity | Pred-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260904_032624_7e855a` | ABI-201 cross-scale directional consensus | exploratory | 12 | 0.3958 | 0.3751 | 0.4497 | 0.4587 | 0.3481 | 0.4630 | 0.002749 |
| `run_20260904_043143_ee0005` | ABI-202 cross-scale directional consensus late36 | late_improving | 34 | 0.4276 | 0.4120 | 0.4682 | 0.4395 | 0.4163 | 0.4578 | 0.003433 |
| `run_20260904_073913_3edd12` | ABI-203 foreground-calibrated head | exploratory | 12 | 0.4023 | 0.3926 | 0.4289 | 0.4332 | 0.3756 | 0.4004 | 0.003142 |
| `run_20260904_084637_a1c72c` | ABI-204 support-gated feature refiner | exploratory | 12 | 0.3726 | 0.3631 | 0.3961 | 0.4327 | 0.3272 | 0.2782 | 0.002740 |
| `run_20260902_213856_2c04ac` | ABI-184 signed-detail line+centerline | late_improving | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.002615 |

Relative to ABI-203, ABI-204 reduced the filtered predicted-positive fraction from 0.003142 to 0.002740, but this was not a useful tradeoff: aggregate filtered Dice fell by about 0.0297, MIT by about 0.0295, Google by about 0.0328, recall by about 0.0484, and connectivity by about 0.1222, while precision was essentially unchanged. The feature-space support gate therefore appears to remove line evidence rather than isolate false positives.

Relative to the exploratory parent ABI-201, ABI-204 is also negative: predicted-positive fraction is nearly unchanged, but aggregate Dice, both source Dice values, precision, recall, and especially connectivity all decline. Relative to ABI-202 late36, ABI-204 is far below the current whole-validation reference on every scientific metric except having fewer filtered positive pixels. Relative to ABI-184, it does not match the stricter precision/connectivity/positive-area discipline that motivated this false-positive-control branch.

## Resource and contract observations

The Run stayed inside the active Workspace Configuration: exploratory budget, 12 effective epochs, batch size 4, constant learning rate, disabled early stopping, provider-owned source-balanced capped selection, provider-owned random mirroring, and A100 execution. The resolved manifest uses approved `abi_16ch_plus_sza` input mode; forbidden longitude and latitude source channels are excluded; outputs are `mask_logits`, `line_logits`, and `centerline_logits`; and the model summary reports 8,181,431 parameters under the 25,000,000-parameter ceiling.

Resource profiling completed successfully with about 10.51 GiB peak allocated CUDA memory, about 11.93 GiB peak reserved CUDA memory, and about 3,459 seconds total run wall time. This is inside but very close to the 3,600-second exploratory timeout. No contract, resource, numerical, or lifecycle failure is indicated in the Harness-observed artifacts, but the near-timeout wall time argues against adding more local complexity to this exact branch without a stronger hypothesis.

## Failure classification

Classify ABI-204 as a valid finite but negative research Result, not a Candidate bug, contract violation, Resource Failure, Harness Failure, unknown failure, or hard stop for the broader cross-scale directional-consensus ASPP family. It completed cleanly and produced source-informative metrics.

Scientifically, the exact support-gated feature refiner did not meet its proposal-specific goal. It reduced predicted positive area, but did so by suppressing true contrail/line evidence: recall and connectivity regressed sharply, precision did not improve, and both MIT and Google filtered Dice declined. This provides evidence against repeating this exact support-gated refiner unchanged or escalating ABI-204 to whole-validation diagnostics.

## Decision

Do not promote ABI-204 and do not request whole-validation failure-bucket evaluation for this exploratory checkpoint. Retain ABI-202 as the current whole-validation aggregate filtered-Dice reference and retain ABI-184 as the precision/connectivity and negative-patch-discipline reference.

The broader cross-scale directional-consensus ASPP family remains viable because ABI-202 is strong, but the local false-positive-control refiners tested by ABI-203 and ABI-204 are not solving the failure mode cleanly. For the next in-contract hypothesis, broaden away from another support/calibration gate on this near-timeout branch unless the mechanism is materially different and cheaper. More useful frontier moves include a lower-complexity recall-preserving refinement, an allowlisted loss/auxiliary policy probe on the strong ABI-202/201 shape, or a different architecture family scout focused on connectivity and source balance. Candidate code must continue to use approved ABI channel inputs only and must not implement thresholding, data loading, losses, metrics, Artifact Filters, sampling behavior, or coordinate features.

No Capability Request, Evaluation Request, or Campaign Report is required from this Result.

## Artifact references

- `run_20260904_084637_a1c72c/outputs/best_metrics.json`
- `run_20260904_084637_a1c72c/outputs/final_metrics.json`
- `run_20260904_084637_a1c72c/outputs/metrics.jsonl`
- `run_20260904_084637_a1c72c/outputs/resource_profile.json`
- `run_20260904_084637_a1c72c/outputs/model_summary.json`
- `run_20260904_084637_a1c72c/outputs/prediction_samples/samples.json`
- `run_20260904_084637_a1c72c/resolved_manifest.yaml`
- `run_20260904_084637_a1c72c/candidate/PROPOSAL.md`
- `run_20260904_032624_7e855a/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260904_073913_3edd12/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
