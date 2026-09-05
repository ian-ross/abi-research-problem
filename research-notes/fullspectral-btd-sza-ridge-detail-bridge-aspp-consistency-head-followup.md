# Full-spectral BTD+SZA ridge-detail bridge ASPP consistency-head follow-up

research-figures: []

## Scope

This note records the capped exploratory Result for ABI-198, Candidate `abi198_fullspectral_btd_sza_ridge_detail_bridge_aspp_consistency_head_bce_dice_line_centerline_aux_v1`, Run `run_20260904_000632_1a04ae`.

ABI-198 was a controlled architecture continuation of the ABI-196 ridge-detail bridge ASPP branch. It kept approved `abi_16ch_plus_sza` inputs, deterministic ABI-channel BTD features, signed-detail streams, compact residual encoder, ASPP context, full-scale skip fusion, `RidgePreservingDetailBridge`, trusted `bce_dice`, trusted Line and Centerline auxiliary targets, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW at 0.0003, batch size 4, 12 exploratory epochs, constant learning rate, and disabled early stopping.

The intended architecture-only change was a differentiable `ConsistencyCalibratedMaskHead` that conditions the final mask logits on soft `line_logits` and `centerline_logits` support. The hypothesis was that line/centerline-conditioned mask calibration might reduce unsupported texture or ridge false positives without candidate-owned thresholding, postprocessing, Artifact Filters, target transforms, losses, metrics, data loading, or sampling policy.

Primary comparison is ABI-196 `run_20260903_195527_248472`, whose late36 selected checkpoint reached capped `val/filtered_dice` 0.4133 and whose whole-validation evaluation reached filtered Dice 0.4147. Secondary references are ABI-195 `run_20260903_135523_8976a0` as the 12-epoch `bce_dice` ridge-detail parent, ABI-197 `run_20260903_230028_82d11d` as the negative clDice loss-policy probe, and ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference.

## Capped exploratory metrics

ABI-198 completed 12/12 exploratory epochs with finite losses and non-collapsed, source-informative predictions. The Harness selected epoch 11 as the best checkpoint by `val/filtered_dice`.

| Metric | ABI-198 capped best |
| --- | ---: |
| Best epoch | 11 |
| Filtered Dice | 0.3789 |
| MIT filtered Dice | 0.3726 |
| Google filtered Dice | 0.3939 |
| Filtered precision | 0.3857 |
| Filtered recall | 0.3723 |
| Filtered contrail connectivity | 0.2366 |
| Filtered predicted-positive fraction | 0.003498 |
| Raw Dice | 0.3925 |
| Raw recall | 0.3978 |
| Train loss | 0.8515 |
| Validation loss | 0.8848 |

The final epoch shifted to a more conservative but not higher-Dice operating point: filtered Dice 0.3726, MIT/Google filtered Dice 0.3530/0.4234, precision 0.4731, recall 0.3074, connectivity 0.4111, and filtered predicted-positive fraction 0.002354. This final-epoch precision/connectivity recovery was too late and too recall-costly to become the selected checkpoint.

The trajectory was volatile rather than cleanly late-improving. Filtered Dice rose from 0.2047 at epoch 1 to 0.3431 at epoch 4, fluctuated through epochs 5-8, reached 0.3781 at epoch 9, dropped to 0.3459 at epoch 10, returned to the run-best 0.3789 at epoch 11, and softened to 0.3726 at epoch 12. The mask loss and validation loss remained finite and slowly improving, but the selected metric did not show the kind of near-frontier late trajectory that justified ABI-196's late36 continuation.

## Comparison

| Run | Branch | Budget | Best epoch | Filtered Dice | MIT | Google | Precision | Recall | Connectivity | Pred-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260903_135523_8976a0` | ABI-195 ridge-detail `bce_dice` | exploratory | 12 | 0.3891 | 0.3706 | 0.4369 | 0.4649 | 0.3346 | 0.4391 | 0.002608 |
| `run_20260903_195527_248472` | ABI-196 ridge-detail `bce_dice` | late_improving | 34 | 0.4133 | 0.4007 | 0.4442 | 0.4350 | 0.3936 | 0.3746 | 0.003278 |
| `run_20260903_230028_82d11d` | ABI-197 ridge-detail `bce_dice_cldice` | exploratory | 12 | 0.3838 | 0.3727 | 0.4111 | 0.3907 | 0.3771 | 0.3633 | 0.003498 |
| `run_20260904_000632_1a04ae` | ABI-198 consistency head `bce_dice` | exploratory | 11 | 0.3789 | 0.3726 | 0.3939 | 0.3857 | 0.3723 | 0.2366 | 0.003498 |
| `run_20260902_213856_2c04ac` | ABI-184 signed-detail line+centerline | late_improving | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.002615 |

ABI-198 did not meet its proposal-specific success criterion. Relative to ABI-196's selected capped checkpoint, it lost about 0.0344 filtered Dice, 0.0281 MIT filtered Dice, 0.0503 Google filtered Dice, 0.0493 precision, 0.0213 recall, and 0.1380 connectivity while slightly increasing filtered predicted-positive fraction. Relative to ABI-195's 12-epoch parent, the selected checkpoint roughly tied MIT filtered Dice and improved recall, but lost aggregate and Google filtered Dice, precision, connectivity, and positive-area discipline. Relative to ABI-197, it was also weaker on aggregate Dice, Google Dice, precision, recall, and connectivity, with the same selected predicted-positive fraction.

The final epoch shows that the consistency head can move into an ABI-195-like conservative precision/connectivity regime, but only by sacrificing too much recall and MIT/source balance. The selected epoch behaves more like an unsupported local gate: it does not reduce predicted-positive burden relative to ABI-196/197, and it does not preserve the ridge-detail branch's connectivity advantage.

## Resource and contract observations

The Run stayed inside the active Workspace Configuration: exploratory budget, 12 effective epochs, batch size 4, constant learning rate, disabled early stopping, provider-owned source-balanced capped selection, provider-owned random mirroring, and A100 execution. The model summary reports approved `abi_16ch_plus_sza` input shape `[17, 256, 256]`; forbidden longitude and latitude source channels are excluded; output names are `mask_logits`, `line_logits`, and `centerline_logits`; and the model has 10,080,173 parameters under the 25,000,000 parameter ceiling.

Resource profiling completed successfully with about 11.4 GB peak allocated CUDA memory and about 3,456 seconds total run wall time, within the 3,600-second exploratory timeout but with a narrow margin. No contract, resource, numerical, or lifecycle failure is indicated in the Harness-observed artifacts. Substantially heavier exploratory continuations of this branch would need a strong resource-aware reason.

## Failure classification

Classify ABI-198 as `bad_research_result`, not a Candidate bug, contract violation, Resource Failure, Harness Failure, or unknown failure. The Run completed cleanly and produced finite, non-collapsed, Dataset Source-informative predictions, but the scientific outcome regressed against the intended comparison targets.

This Result does not justify a whole-validation Evaluation Request: the capped selected checkpoint is below ABI-196, ABI-195, ABI-197, ABI-184, ABI-181, and ABI-192, and the intended false-positive/consistency indicators did not improve. It also does not justify a late-improving budget request. The best checkpoint occurred before the final epoch, the final epoch traded recall for precision rather than lifting aggregate Dice, and the branch-specific objective was to improve calibration/discipline rather than chase recovery from a weaker gated head.

## Decision

Do not promote ABI-198, do not repeat it unchanged, do not request whole-validation diagnostics for it, and do not request late36 continuation for this exact consistency-calibrated head.

Retain ABI-196 as the current whole-validation aggregate filtered-Dice reference and ABI-184 as the precision/connectivity and negative-patch-discipline reference. Treat ABI-197 and ABI-198 together as negative evidence for local mask-head/loss-policy fixes to the ridge-detail bridge's false-positive burden: both preserved finite training but weakened the branch relative to ABI-196, and neither produced a cleaner near-frontier capped tradeoff.

The next in-contract hypothesis should broaden away from this exact ridge-detail bridge head-calibration axis. Reasonable directions include a materially different line-continuity architecture scout, a controlled data/training-policy probe already owned by the Harness/provider, or a simpler architecture change that preserves ABI-196's median-positive recall while explicitly avoiding another post-refinement gate. Candidate code must continue to use approved ABI channel inputs only and must not implement thresholding, data loading, losses, metrics, Artifact Filters, sampling behavior, or coordinate features.

No Capability Request, Evaluation Request, or Campaign Report is required from this Result.

## Artifact references

- `run_20260904_000632_1a04ae/outputs/best_metrics.json`
- `run_20260904_000632_1a04ae/outputs/final_metrics.json`
- `run_20260904_000632_1a04ae/outputs/metrics.jsonl`
- `run_20260904_000632_1a04ae/outputs/resource_profile.json`
- `run_20260904_000632_1a04ae/outputs/model_summary.json`
- `run_20260904_000632_1a04ae/outputs/prediction_samples/samples.json`
- `run_20260904_000632_1a04ae/resolved_manifest.yaml`
- `run_20260903_195527_248472/outputs/best_metrics.json`
- `run_20260903_195527_248472/outputs/evaluations/eval_evalreq_abi196_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260903_195527_248472/outputs/evaluations/eval_evalreq_abi196_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260903_135523_8976a0/outputs/best_metrics.json`
- `run_20260903_230028_82d11d/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
