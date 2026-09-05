# Full-spectral BTD+SZA spectral-contrast bridge ASPP follow-up

research-figures: []

## Scope

This note records the capped exploratory Result for ABI-200, Candidate `abi200_fullspectral_btd_sza_spectral_contrast_bridge_aspp_bce_dice_line_centerline_aux_v1`, Run `run_20260904_022202_03c56b`.

ABI-200 was a controlled architecture/front-end continuation after the ABI-196 through ABI-199 ridge-detail and bridge probes. It kept approved `abi_16ch_plus_sza` inputs, deterministic ABI-channel BTD features, trusted `bce_dice`, trusted Line and Centerline auxiliary targets, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW at 0.0003, batch size 4, constant learning rate, disabled early stopping, and the 12-epoch exploratory budget.

The intended architecture-only change was to replace the ridge-detail bridge with `SpectralContrastDetailBridge`, fusing decoder/stem/detail features with front-end BTD plus SZA contrast evidence through a bounded residual before ordinary line-aware refinement and mask, line, and centerline heads. The hypothesis was that spectral-contrast reliability evidence could reduce unsupported cloud-edge/detail clutter while preserving source balance, without candidate-owned thresholding, postprocessing, Artifact Filters, target transforms, custom losses, metrics, data loading, or sampling policy.

Primary comparison is ABI-196 `run_20260903_195527_248472`, whose late36 selected checkpoint reached capped `val/filtered_dice` 0.4133 and whose whole-validation evaluation reached filtered Dice 0.4147. Secondary references are ABI-195 `run_20260903_135523_8976a0` as the high-precision ridge-detail parent, ABI-197/198/199 as negative local loss/head/oriented-bridge probes, ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity reference, and ABI-181/192 as the current whole-validation-tested frontier references.

## Capped exploratory metrics

ABI-200 completed 12/12 exploratory epochs with finite losses and non-collapsed, Dataset Source-informative predictions. The Harness selected epoch 11 as the best checkpoint by `val/filtered_dice`.

| Metric | ABI-200 capped best |
| --- | ---: |
| Best epoch | 11 |
| Filtered Dice | 0.3916 |
| MIT filtered Dice | 0.3854 |
| Google filtered Dice | 0.4074 |
| Filtered precision | 0.4264 |
| Filtered recall | 0.3620 |
| Filtered contrail connectivity | 0.2698 |
| Filtered predicted-positive fraction | 0.003077 |
| Raw Dice | 0.4064 |
| Raw recall | 0.3875 |
| Train loss | 0.8537 |
| Validation loss | 0.8842 |

The final epoch moved to a more recall-heavy but lower-Dice operating point: filtered Dice 0.3736, MIT/Google filtered Dice 0.3670/0.3904, precision 0.3492, recall 0.4018, connectivity 0.2600, and filtered predicted-positive fraction 0.004170. This final shift indicates that the spectral-contrast bridge did not stabilize the desired precision/recall balance by the end of exploratory training.

The trajectory was finite but volatile. Filtered Dice rose from 0.1862 at epoch 1 to 0.3773 at epoch 6, dipped and recovered to 0.3853 at epoch 9, fell to 0.3502 at epoch 10, peaked at 0.3916 at epoch 11, then dropped to 0.3736 at epoch 12. Validation loss improved overall from 0.9700 to 0.8842 at the selected epoch, but the selected metric alternated between conservative precision and recall-heavy positive-area expansion.

## Comparison

| Run | Branch | Budget | Best epoch | Filtered Dice | MIT | Google | Precision | Recall | Connectivity | Pred-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260903_135523_8976a0` | ABI-195 ridge-detail `bce_dice` | exploratory | 12 | 0.3891 | 0.3706 | 0.4369 | 0.4649 | 0.3346 | 0.4391 | 0.002608 |
| `run_20260903_195527_248472` | ABI-196 ridge-detail `bce_dice` | late_improving | 34 | 0.4133 | 0.4007 | 0.4442 | 0.4350 | 0.3936 | 0.3746 | 0.003278 |
| `run_20260903_230028_82d11d` | ABI-197 ridge-detail `bce_dice_cldice` | exploratory | 12 | 0.3838 | 0.3727 | 0.4111 | 0.3907 | 0.3771 | 0.3633 | 0.003498 |
| `run_20260904_000632_1a04ae` | ABI-198 consistency head `bce_dice` | exploratory | 11 | 0.3789 | 0.3726 | 0.3939 | 0.3857 | 0.3723 | 0.2366 | 0.003498 |
| `run_20260904_011242_2435ad` | ABI-199 oriented gap bridge `bce_dice` | exploratory | 11 | 0.3949 | 0.3860 | 0.4162 | 0.3883 | 0.4016 | 0.2677 | 0.003748 |
| `run_20260904_022202_03c56b` | ABI-200 spectral-contrast bridge `bce_dice` | exploratory | 11 | 0.3916 | 0.3854 | 0.4074 | 0.4264 | 0.3620 | 0.2698 | 0.003077 |
| `run_20260902_213856_2c04ac` | ABI-184 signed-detail line+centerline | late_improving | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.002615 |

ABI-200 is mixed but not frontier-improving. Relative to ABI-199, it improved precision by about 0.0381 and reduced filtered predicted-positive fraction by about 0.00067, but lost 0.0033 aggregate filtered Dice, 0.0006 MIT filtered Dice, 0.0089 Google filtered Dice, 0.0396 recall, and remained similarly weak on connectivity. Relative to ABI-195, it slightly improved aggregate and MIT filtered Dice and recall, but lost Google filtered Dice, precision, connectivity, and positive-area discipline. Relative to ABI-196, it lost about 0.0217 filtered Dice, 0.0153 MIT filtered Dice, 0.0368 Google filtered Dice, 0.0086 precision, 0.0315 recall, and 0.1048 connectivity, with only a slightly lower predicted-positive fraction.

The proposal-specific objective was not met. The spectral-contrast bridge did improve precision and positive-area discipline compared with ABI-199's oriented gap bridge, but it did not recover ABI-184/195/196-level connectivity or ABI-196-level source-balanced overlap. It appears to be a partial correction of the recall-heavy ABI-199 failure mode rather than a better solution to the ridge-detail ASPP false-positive/connectivity tradeoff.

## Resource and contract observations

The Run stayed inside the active Workspace Configuration: exploratory budget, 12 effective epochs, batch size 4, constant learning rate, disabled early stopping, provider-owned source-balanced capped selection, provider-owned random mirroring, and A100 execution. The resolved manifest reports approved `abi_16ch_plus_sza` input mode; forbidden longitude and latitude source channels are excluded; output names are `mask_logits`, `line_logits`, and `centerline_logits`; and the model summary reports 9,975,611 parameters under the 25,000,000 parameter ceiling.

Resource profiling completed successfully with about 10.20 GiB peak allocated CUDA memory, about 11.55 GiB peak reserved CUDA memory, and about 3,262 seconds total run wall time. This is inside the 3,600-second exploratory timeout, with more margin than ABI-199 but still a relatively heavy resource envelope for local bridge continuations. No contract, resource, numerical, or lifecycle failure is indicated in the Harness-observed artifacts.

## Failure classification

Classify ABI-200 as `bad_research_result`, not a Candidate bug, contract violation, Resource Failure, Harness Failure, or unknown failure. The Run completed cleanly and produced finite, non-collapsed, Dataset Source-informative predictions, but the scientific outcome regressed against the intended comparison target and did not satisfy the bridge-specific precision/connectivity objective.

This Result does not justify a whole-validation Evaluation Request. Its capped selected checkpoint is below ABI-196, ABI-181, ABI-192, ABI-184, and ABI-199, and the intended connectivity/false-positive indicators remain inferior to the main references. It also does not justify a late-improving budget request: the best checkpoint was not the final epoch, the final epoch degraded filtered Dice, and the trajectory was volatile rather than clearly still improving at the exploratory ceiling.

## Decision

Do not promote ABI-200, do not repeat it unchanged, do not request whole-validation diagnostics for it, and do not request late36 continuation for this exact spectral-contrast bridge branch.

Retain ABI-196 as the strongest local whole-validation aggregate filtered-Dice reference and ABI-184 as the precision/connectivity and negative-patch-discipline reference. Treat ABI-197 through ABI-200 together as evidence that local loss/head/bridge modifications around the ridge-detail ASPP lineage can adjust precision-recall tradeoffs but have not solved the false-positive and connectivity burden. ABI-200 partially corrected ABI-199's positive-area expansion, yet still landed below the frontier with weak connectivity.

The next in-contract hypothesis should broaden away from this exact ridge-detail/local-bridge edit axis. Reasonable directions include a materially different line-continuity architecture family, a simpler precision-preserving decoder branch, or a trusted data/training-policy probe already owned by the Harness/provider. Candidate code must continue to use approved ABI channel inputs only and must not implement thresholding, data loading, losses, metrics, Artifact Filters, sampling behavior, or coordinate features.

No Capability Request, Evaluation Request, or Campaign Report is required from this Result.

## Artifact references

- `run_20260904_022202_03c56b/outputs/best_metrics.json`
- `run_20260904_022202_03c56b/outputs/final_metrics.json`
- `run_20260904_022202_03c56b/outputs/metrics.jsonl`
- `run_20260904_022202_03c56b/outputs/resource_profile.json`
- `run_20260904_022202_03c56b/outputs/model_summary.json`
- `run_20260904_022202_03c56b/outputs/prediction_samples/samples.json`
- `run_20260904_022202_03c56b/resolved_manifest.yaml`
- `run_20260903_195527_248472/outputs/best_metrics.json`
- `run_20260903_195527_248472/outputs/evaluations/eval_evalreq_abi196_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260903_135523_8976a0/outputs/best_metrics.json`
- `run_20260903_230028_82d11d/outputs/best_metrics.json`
- `run_20260904_000632_1a04ae/outputs/best_metrics.json`
- `run_20260904_011242_2435ad/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
