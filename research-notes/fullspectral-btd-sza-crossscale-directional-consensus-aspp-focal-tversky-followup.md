# Full-spectral BTD+SZA cross-scale directional-consensus ASPP focal-Tversky follow-up

research-figures: []

## Scope

This note records the capped exploratory Result for ABI-205, Candidate `abi205_fullspectral_btd_sza_crossscale_directional_consensus_aspp_focal_tversky_line_centerline_aux_v1`, Run `run_20260904_095159_9df334`.

ABI-205 was a controlled loss-policy continuation of the ABI-201/202 cross-scale directional-consensus ASPP family. It kept provider-approved `abi_16ch_plus_sza` input, deterministic ABI-channel brightness-temperature-difference features, normalized/cosine Solar Geometry features, the ABI-201/202 architecture, trusted Line and Centerline auxiliary targets, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW at 0.0003, batch size 4, constant learning rate, disabled early stopping, and the 12-epoch exploratory budget. The intended one-factor change was the trusted primary loss switch from `bce_dice` to allowlisted `focal_tversky`. Candidate code did not implement data loading, losses, metrics, target derivation, Artifact Filters, thresholding, postprocessing, coordinate features, training loops, runtime downloads, or resource scheduling.

Primary comparison targets are ABI-201 `run_20260904_032624_7e855a`, the same-architecture 12-epoch BCE-Dice parent; ABI-202 `run_20260904_043143_ee0005`, the late36 whole-validation aggregate reference; and ABI-184 `run_20260902_213856_2c04ac`, retained as the precision/connectivity and negative-patch-discipline reference. ABI-203 and ABI-204 are recent negative local false-positive-control follow-ups.

## Capped exploratory metrics

ABI-205 completed 12/12 exploratory epochs with finite losses and non-collapsed, Dataset Source-informative predictions. The Harness selected epoch 9 as the best checkpoint by `val/filtered_dice`; final epoch 12 regressed substantially from that selected checkpoint.

| Metric | ABI-205 capped best | ABI-205 final |
| --- | ---: | ---: |
| Epoch | 9 | 12 |
| Filtered Dice | 0.3717 | 0.3516 |
| MIT filtered Dice | 0.3628 | 0.3592 |
| Google filtered Dice | 0.3921 | 0.3358 |
| Filtered precision | 0.3815 | 0.3065 |
| Filtered recall | 0.3623 | 0.4122 |
| Filtered contrail connectivity | 0.3210 | 0.1721 |
| Filtered predicted-positive fraction | 0.003442 | 0.004874 |
| Raw Dice | 0.3847 | 0.3626 |
| Raw recall | 0.3895 | 0.4406 |
| Train loss | 0.8463 | 0.8505 |
| Validation loss | 0.8848 | 0.8802 |

The trajectory was finite but volatile and scientifically negative. Filtered Dice improved from 0.1697 at epoch 1 to 0.3454 at epoch 5, reached 0.3575 at epoch 7, peaked at 0.3717 at epoch 9, then dropped to 0.3275 and 0.3211 before a partial final recovery to 0.3516. The late final state traded higher recall for much lower precision and connectivity, suggesting foreground expansion without useful line structure.

## Comparison

| Run | Branch | Budget | Best epoch | Filtered Dice | MIT | Google | Precision | Recall | Connectivity | Pred-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260904_032624_7e855a` | ABI-201 same architecture, BCE-Dice | exploratory | 12 | 0.3958 | 0.3751 | 0.4497 | 0.4587 | 0.3481 | 0.4630 | 0.002749 |
| `run_20260904_043143_ee0005` | ABI-202 same architecture, BCE-Dice late36 | late_improving | 34 | 0.4276 | 0.4120 | 0.4682 | 0.4395 | 0.4163 | 0.4578 | 0.003433 |
| `run_20260904_073913_3edd12` | ABI-203 foreground-calibrated head | exploratory | 12 | 0.4023 | 0.3926 | 0.4289 | 0.4332 | 0.3756 | 0.4004 | 0.003142 |
| `run_20260904_084637_a1c72c` | ABI-204 support-gated feature refiner | exploratory | 12 | 0.3726 | 0.3631 | 0.3961 | 0.4327 | 0.3272 | 0.2782 | 0.002740 |
| `run_20260904_095159_9df334` | ABI-205 same architecture, focal-Tversky | exploratory | 9 | 0.3717 | 0.3628 | 0.3921 | 0.3815 | 0.3623 | 0.3210 | 0.003442 |
| `run_20260902_213856_2c04ac` | ABI-184 signed-detail line+centerline | late_improving | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.002615 |

Relative to the same-budget ABI-201 parent, ABI-205 did not meet its proposal goal. It slightly increased best-checkpoint recall by about 0.0142, but aggregate filtered Dice fell by about 0.0241, MIT by about 0.0124, Google by about 0.0575, precision by about 0.0772, connectivity by about 0.1420, and filtered predicted-positive fraction increased rather than decreased. This is not a cleaner false-positive tradeoff.

Relative to ABI-202 late36, ABI-205 is far below the current whole-validation-tested aggregate reference and also below ABI-202's capped best on both Dataset Sources, precision, recall, and connectivity. Relative to ABI-203, the loss switch underperforms the architecture-local foreground-calibrated follow-up on Dice, source balance, precision, recall, and connectivity. Relative to ABI-204, ABI-205 has similar aggregate/source Dice, a small recall/connectivity recovery, but much lower precision and a higher predicted-positive fraction.

## Resource and contract observations

The Run stayed inside the active Workspace Configuration: exploratory budget, 12 effective epochs, batch size 4, constant learning rate, disabled early stopping, provider-owned source-balanced capped selection, provider-owned random mirroring, and A100 execution. The resolved model summary uses approved `abi_16ch_plus_sza` input mode; forbidden longitude and latitude source channels are excluded; outputs are `mask_logits`, `line_logits`, and `centerline_logits`; and the model summary reports 8,172,287 parameters under the 25,000,000-parameter ceiling.

Resource profiling completed successfully with about 9.74 GiB peak allocated CUDA memory, about 11.08 GiB peak reserved CUDA memory, and about 3,357 seconds total run wall time. This is inside but close to the 3,600-second exploratory timeout. No contract, resource, numerical, or lifecycle failure is indicated in the Harness-observed artifacts.

## Failure classification

Classify ABI-205 as a valid finite but negative research Result, not a Candidate bug, contract violation, Resource Failure, Harness Failure, unknown failure, or hard stop for the broader cross-scale directional-consensus ASPP family. It completed cleanly and produced source-informative, non-collapsed predictions.

Scientifically, the exact focal-Tversky loss-policy probe failed to improve the target tradeoff. It did not reduce positive-area burden, did not improve precision, substantially weakened connectivity, and especially regressed Google filtered Dice relative to the same-architecture BCE-Dice parent. The best selected epoch was 9 rather than 12, and the final-epoch behavior shows expansion/recall without stable line quality, so the run does not justify a `late_improving` continuation or whole-validation failure-bucket evaluation for this exact loss setting.

## Decision

Do not promote ABI-205, do not request whole-validation diagnostics, and do not request a late36 continuation for this focal-Tversky branch. Retain ABI-202 as the current whole-validation aggregate filtered-Dice reference and ABI-184 as the precision/connectivity and stricter negative-patch-discipline reference.

The broader cross-scale directional-consensus ASPP family remains viable because ABI-202 is strong, but recent local variants suggest that neither added false-positive gates nor a focal-Tversky switch cleanly controls residual clutter. For the next in-contract hypothesis, prefer broadening away from this exact loss probe: either test a different allowlisted auxiliary/loss combination that preserves BCE-Dice optimization, use a cheaper recall-preserving refinement, or scout a materially different architecture family focused on connectivity/source balance. Candidate code must continue to use approved ABI channel inputs only and must not implement thresholding, data loading, losses, metrics, Artifact Filters, sampling behavior, or coordinate features.

No Capability Request, Evaluation Request, or Campaign Report is required from this Result.

## Artifact references

- `run_20260904_095159_9df334/outputs/best_metrics.json`
- `run_20260904_095159_9df334/outputs/final_metrics.json`
- `run_20260904_095159_9df334/outputs/metrics.jsonl`
- `run_20260904_095159_9df334/outputs/resource_profile.json`
- `run_20260904_095159_9df334/outputs/model_summary.json`
- `run_20260904_095159_9df334/outputs/prediction_samples/samples.json`
- `run_20260904_095159_9df334/resolved_manifest.yaml`
- `run_20260904_095159_9df334/candidate/PROPOSAL.md`
- `run_20260904_032624_7e855a/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/best_metrics.json`
- `run_20260904_043143_ee0005/outputs/evaluations/eval_evalreq_abi202_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260904_073913_3edd12/outputs/best_metrics.json`
- `run_20260904_084637_a1c72c/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
