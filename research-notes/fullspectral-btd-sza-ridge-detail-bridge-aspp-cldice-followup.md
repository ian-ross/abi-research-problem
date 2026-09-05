# Full-spectral BTD+SZA ridge-detail bridge ASPP clDice follow-up

research-figures: []

## Scope

This note records the capped exploratory Result for ABI-197, Candidate `abi197_fullspectral_btd_sza_ridge_detail_bridge_aspp_cldice_line_centerline_aux_v1`, Run `run_20260903_230028_82d11d`.

ABI-197 was a controlled trusted-loss-policy continuation of ABI-196. It kept the approved `abi_16ch_plus_sza` input mode, deterministic ABI-channel BTD features, signed detail streams, compact residual encoder, ASPP context, full-scale skip fusion, `RidgePreservingDetailBridge`, line-aware final refinement, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, 12 exploratory epochs, and Line plus Centerline auxiliary targets. The intended manifest-only scientific change was the trusted primary loss selection from `bce_dice` to `bce_dice_cldice`.

Primary comparison is ABI-196 `run_20260903_195527_248472`, whose late36 selected checkpoint reached capped `val/filtered_dice` 0.4133 and whose whole-validation evaluation reached filtered Dice 0.4147. Secondary references are ABI-195 `run_20260903_135523_8976a0` as the 12-epoch `bce_dice` ridge-detail parent and ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference.

## Capped exploratory metrics

ABI-197 completed 12/12 exploratory epochs with finite losses and non-collapsed, source-informative predictions. The best checkpoint was the final epoch.

| Metric | ABI-197 capped best |
| --- | ---: |
| Best epoch | 12 |
| Filtered Dice | 0.3838 |
| MIT filtered Dice | 0.3727 |
| Google filtered Dice | 0.4111 |
| Filtered precision | 0.3907 |
| Filtered recall | 0.3771 |
| Filtered contrail connectivity | 0.3633 |
| Filtered predicted-positive fraction | 0.003498 |
| Raw Dice | 0.3972 |
| Train loss | 1.2604 |
| Validation loss | 1.3132 |
| Validation Line auxiliary loss | 0.000609 |
| Validation Centerline auxiliary loss | 0.000492 |

The validation trajectory improved late but from a weaker operating point: filtered Dice was 0.2175 at epoch 1, 0.3569 at epoch 7, 0.3665 at epoch 9, 0.3708 at epoch 11, and 0.3838 at epoch 12. The final epoch improved precision and connectivity relative to epochs 9-11, but it did not recover ABI-195/196-level overlap or discipline.

## Comparison

| Run | Branch | Budget | Best epoch | Filtered Dice | MIT | Google | Precision | Recall | Connectivity | Pred-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260903_135523_8976a0` | ABI-195 ridge-detail `bce_dice` | exploratory | 12 | 0.3891 | 0.3706 | 0.4369 | 0.4649 | 0.3346 | 0.4391 | 0.002608 |
| `run_20260903_195527_248472` | ABI-196 ridge-detail `bce_dice` late36 | late_improving | 34 | 0.4133 | 0.4007 | 0.4442 | 0.4350 | 0.3936 | 0.3746 | 0.003278 |
| `run_20260902_213856_2c04ac` | ABI-184 signed-detail line+centerline | late_improving | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.002615 |
| `run_20260903_230028_82d11d` | ABI-197 ridge-detail `bce_dice_cldice` | exploratory | 12 | 0.3838 | 0.3727 | 0.4111 | 0.3907 | 0.3771 | 0.3633 | 0.003498 |

ABI-197 did not meet its intended success criterion. Relative to ABI-196's capped selected checkpoint, it lost about 0.0295 filtered Dice, 0.0443 precision, 0.0164 recall, and 0.0113 connectivity, while increasing filtered predicted-positive fraction. Relative to ABI-195's 12-epoch `bce_dice` parent, it slightly improved MIT filtered Dice and recall but lost aggregate filtered Dice, Google filtered Dice, precision, connectivity, and positive-area discipline. This is not the desired trade of small overlap for cleaner connected thin lines; it is a lower-quality, more clutter-prone operating point on the capped validation subset.

The loss-policy probe is still useful negative evidence: the currently trusted `bce_dice_cldice` objective did not repair ABI-196's negative-patch false-positive burden in this architecture, and it weakened the ridge-detail bridge's main precision/connectivity advantage.

## Resource and contract observations

The Run stayed inside the active Workspace Configuration: exploratory budget, 12 effective epochs, batch size 4, constant learning rate, disabled early stopping, provider-owned source-balanced capped selection, provider-owned random mirroring, and A100 execution. The model summary reports approved `abi_16ch_plus_sza` input shape `[17, 256, 256]`; forbidden longitude and latitude source channels are excluded; output names are `mask_logits`, `line_logits`, and `centerline_logits`; and the model has 10,041,211 parameters under the 25,000,000 parameter ceiling.

Resource profiling completed successfully with about 11.1 GB peak allocated CUDA memory and about 3,464 seconds total run wall time, within the 3,600-second exploratory timeout. No contract, resource, numerical, or lifecycle failure is indicated in the Harness-observed artifacts, though the wall-clock margin is narrow enough that substantially heavier continuations of this branch should not be submitted without a resource-aware reason.

## Failure classification

Classify ABI-197 as `bad_research_result`, not a Candidate bug, contract violation, Resource Failure, Harness Failure, or unknown failure. It completed cleanly and produced finite, source-informative predictions, but the scientific outcome regressed against the intended comparison targets.

This Result does not justify a whole-validation Evaluation Request: the capped score is below ABI-196, ABI-184, and the 12-epoch ABI-195 parent, and the intended clutter/structure indicators did not improve. It also does not justify a late-improving budget request despite the final-epoch best checkpoint, because the proposal-specific indicators failed in the wrong direction and the branch would be spending late36 budget to chase recovery from a loss-policy regression rather than continuing an already promising capped tradeoff.

## Decision

Do not promote ABI-197, do not repeat it unchanged, do not request whole-validation diagnostics for it, and do not request a late36 continuation for this exact `bce_dice_cldice` ridge-detail bridge branch.

Retain ABI-196 as the current whole-validation-tested aggregate filtered-Dice reference and ABI-184 as the precision/connectivity and negative-patch-discipline reference. Treat ABI-197 as evidence that the current trusted clDice loss does not solve the ridge-detail bridge's false-positive burden. The next in-contract hypothesis should broaden away from this local loss-policy axis, for example by changing architecture calibration/fusion in a controlled way or by scouting a materially different line-continuity architecture, while keeping provider-owned data, losses, metrics, augmentation, Artifact Filters, sampling, and thresholding out of Candidate code.

No Capability Request, Evaluation Request, or Campaign Report is required from this Result.

## Artifact references

- `run_20260903_230028_82d11d/outputs/best_metrics.json`
- `run_20260903_230028_82d11d/outputs/final_metrics.json`
- `run_20260903_230028_82d11d/outputs/metrics.jsonl`
- `run_20260903_230028_82d11d/outputs/resource_profile.json`
- `run_20260903_230028_82d11d/outputs/model_summary.json`
- `run_20260903_230028_82d11d/outputs/prediction_samples/samples.json`
- `run_20260903_230028_82d11d/resolved_manifest.yaml`
- `run_20260903_195527_248472/outputs/best_metrics.json`
- `run_20260903_195527_248472/outputs/evaluations/eval_evalreq_abi196_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260903_135523_8976a0/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
