# Full-spectral BTD+SZA cross-scale directional-consensus ASPP boundary-auxiliary follow-up

research-figures: []

## Scope

This note records the capped exploratory Result for ABI-206, Candidate `abi206_fullspectral_btd_sza_crossscale_directional_consensus_aspp_boundary_bce_dice_line_centerline_aux_v1`, Run `run_20260904_105645_8f8ab1`.

ABI-206 was a controlled auxiliary-policy continuation of the ABI-201/202 cross-scale directional-consensus ASPP family. It kept provider-approved `abi_16ch_plus_sza` input, deterministic ABI-channel brightness-temperature-difference features, normalized/cosine Solar Geometry features, the ABI-201/202 architecture, trusted BCE-Dice primary loss, Line and Centerline auxiliary targets, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW at 0.0003, batch size 4, constant learning rate, disabled early stopping, and the 12-epoch exploratory budget. The intended change was adding one low-weight provider-derived Boundary Target auxiliary head with trusted `weighted_bce` weight 0.005.

Primary comparisons are ABI-201 `run_20260904_032624_7e855a`, the same architecture under the exploratory budget; ABI-202 `run_20260904_043143_ee0005`, the late36 cross-scale directional-consensus reference; ABI-203/204/205 as recent same-family negative follow-ups; and ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference.

Candidate code did not implement data loading, losses, metrics, target derivation, Artifact Filters, thresholding, postprocessing, coordinate features, training loops, runtime downloads, or resource scheduling.

## Capped exploratory metrics

ABI-206 completed 12/12 exploratory epochs with finite losses and non-collapsed, Dataset Source-informative predictions. The Harness selected epoch 12 as the best checkpoint by `val/filtered_dice`, so the final checkpoint is also the selected checkpoint.

| Metric | ABI-206 capped best/final |
| --- | ---: |
| Best epoch | 12 |
| Filtered Dice | 0.3787 |
| MIT filtered Dice | 0.3543 |
| Google filtered Dice | 0.4412 |
| Filtered precision | 0.4655 |
| Filtered recall | 0.3192 |
| Filtered contrail connectivity | 0.4257 |
| Filtered predicted-positive fraction | 0.002485 |
| Raw Dice | 0.3937 |
| Raw recall | 0.3407 |
| Train loss | 0.8476 |
| Validation loss | 0.8855 |

The trajectory was finite and ended at its best aggregate filtered Dice, but it was noisy. Filtered Dice rose from 0.1738 at epoch 1 to 0.3705 at epoch 7, dipped at epoch 8, recovered to 0.3741 at epoch 9, dipped again through epoch 10, shifted into a high-recall/low-connectivity state at epoch 11, and finished at 0.3787. The final operating point is precision-oriented and low-area, with strong Google filtered Dice but a weak MIT source result and lower recall than the stronger ABI-201/202 references.

## Comparison

| Run | Branch | Budget | Best epoch | Filtered Dice | MIT | Google | Precision | Recall | Connectivity | Pred-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260904_032624_7e855a` | ABI-201 same architecture, BCE-Dice | exploratory | 12 | 0.3958 | 0.3751 | 0.4497 | 0.4587 | 0.3481 | 0.4630 | 0.002749 |
| `run_20260904_043143_ee0005` | ABI-202 same architecture, BCE-Dice | late_improving | 34 | 0.4276 | 0.4120 | 0.4682 | 0.4395 | 0.4163 | 0.4578 | 0.003433 |
| `run_20260904_073913_3edd12` | ABI-203 foreground-calibrated head | exploratory | 12 | 0.4023 | 0.3926 | 0.4289 | 0.4332 | 0.3756 | 0.4004 | 0.003142 |
| `run_20260904_084637_a1c72c` | ABI-204 support-gated feature refiner | exploratory | 12 | 0.3726 | 0.3631 | 0.3961 | 0.4327 | 0.3272 | 0.2782 | 0.002740 |
| `run_20260904_095159_9df334` | ABI-205 focal-Tversky loss probe | exploratory | 9 | 0.3717 | 0.3628 | 0.3921 | 0.3815 | 0.3623 | 0.3210 | 0.003442 |
| `run_20260904_105645_8f8ab1` | ABI-206 boundary auxiliary | exploratory | 12 | 0.3787 | 0.3543 | 0.4412 | 0.4655 | 0.3192 | 0.4257 | 0.002485 |
| `run_20260902_213856_2c04ac` | ABI-184 signed-detail line+centerline | late_improving | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.002615 |

ABI-206 partially achieved the intended false-positive-control direction: it has the lowest filtered predicted-positive fraction in this comparison table and higher precision than ABI-201, ABI-202, ABI-203, ABI-204, and ABI-205. It also recovered much of the connectivity lost by ABI-204/205.

However, the tradeoff is not favorable enough. Relative to the same-budget ABI-201 parent, ABI-206 loses about 0.0171 aggregate filtered Dice, 0.0208 MIT filtered Dice, 0.0086 Google filtered Dice, 0.0289 recall, and 0.0373 connectivity, while gaining only about 0.0068 precision and reducing predicted-positive fraction by about 0.000265. Relative to ABI-203, it is lower on aggregate Dice, MIT Dice, recall, and only higher on Google Dice, precision, and area discipline. Relative to ABI-184, it is still less precise, less connected, lower recall, and lower on both Dataset Sources despite slightly lower predicted-positive fraction.

The main concern is source balance. The boundary auxiliary helped make a compact high-precision operating point, especially on Google, but MIT filtered Dice and recall are too weak. This resembles over-constraining the mask support rather than broadly improving clutter rejection.

## Resource and contract observations

The Run stayed inside the active Workspace Configuration: exploratory budget, 12 effective epochs, batch size 4, constant learning rate, disabled early stopping, provider-owned source-balanced capped selection, trusted random mirroring, and A100 execution. The resolved model summary uses approved `abi_16ch_plus_sza` input mode; forbidden longitude and latitude source channels are excluded; outputs are `mask_logits`, `line_logits`, `boundary_logits`, and `centerline_logits`; and the model summary reports 8,172,324 parameters under the 25,000,000-parameter ceiling.

Resource profiling completed successfully with about 9.74 GiB peak allocated CUDA memory, about 11.08 GiB peak reserved CUDA memory, and about 3,326 seconds total run wall time. This is inside but close to the 3,600-second exploratory timeout. No contract, resource, numerical, or lifecycle failure is indicated in the Harness-observed artifacts.

## Interpretation

Classify ABI-206 as a valid, finite, scientifically mixed but negative capped exploratory Result for this exact boundary-auxiliary policy. It is not a Candidate bug, contract violation, Resource Failure, Harness Failure, unknown failure, or a hard stop for the broader cross-scale directional-consensus ASPP family.

The low-weight Boundary Target auxiliary produced a clearer precision/area-discipline signal than ABI-204/205, but not enough aggregate/source benefit to justify promotion or immediate whole-validation diagnostics. The run's final-epoch best checkpoint means the exact trajectory was not plateau-proven, but the achieved 12-epoch operating point is below ABI-201 and ABI-203 on aggregate Dice and is especially weak on MIT. Given the prior ABI-193 boundary-auxiliary probe was also negative in a related signed-detail ASPP lineage, the evidence argues against further local boundary-head tuning as the next step.

## Decision

Do not promote ABI-206, do not request whole-validation failure-bucket evaluation for this exact run, and do not request a late36 continuation for this boundary-auxiliary branch as the immediate next handoff.

Retain ABI-202 as the current whole-validation aggregate filtered-Dice reference for the cross-scale directional-consensus ASPP family and ABI-184 as the precision/connectivity and stricter negative-patch-discipline reference. Treat ABI-206 as evidence that boundary supervision can tighten predicted support, but at the current weight and shared-decoder placement it costs too much MIT/source-balanced recall.

For the next in-contract hypothesis, broaden away from local auxiliary/gating/loss tweaks in this exact family. Prefer either a materially different architecture scout focused on source-balanced connectivity, or an architecture-local change that preserves the ABI-202 recall/connectivity path while addressing clutter through representation rather than extra target pressure. Candidate code must continue to use approved ABI channel inputs only and must not implement data loading, losses, metrics, Artifact Filters, thresholding, sampling behavior, augmentation, coordinate features, or resource scheduling.

No Capability Request, Evaluation Request, or Campaign Report is required from this Result.

## Artifact references

- `run_20260904_105645_8f8ab1/outputs/best_metrics.json`
- `run_20260904_105645_8f8ab1/outputs/final_metrics.json`
- `run_20260904_105645_8f8ab1/outputs/metrics.jsonl`
- `run_20260904_105645_8f8ab1/outputs/resource_profile.json`
- `run_20260904_105645_8f8ab1/outputs/model_summary.json`
- `run_20260904_105645_8f8ab1/outputs/prediction_samples/samples.json`
- `run_20260904_105645_8f8ab1/resolved_manifest.yaml`
- `run_20260904_105645_8f8ab1/candidate/PROPOSAL.md`
- `run_20260904_032624_7e855a/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260904_073913_3edd12/outputs/best_metrics.json`
- `run_20260904_084637_a1c72c/outputs/best_metrics.json`
- `run_20260904_095159_9df334/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
