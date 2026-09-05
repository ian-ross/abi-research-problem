# Full-spectral BTD+SZA oriented gap bridge ASPP follow-up

research-figures: []

## Scope

This note records the capped exploratory Result for ABI-199, Candidate `abi199_fullspectral_btd_sza_oriented_gap_bridge_aspp_bce_dice_line_centerline_aux_v1`, Run `run_20260904_011242_2435ad`.

ABI-199 was a controlled architecture continuation after the ABI-196/197/198 ridge-detail bridge ASPP branch. It kept approved `abi_16ch_plus_sza` inputs, deterministic ABI-channel BTD features, trusted `bce_dice`, trusted Line and Centerline auxiliary targets, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW at 0.0003, batch size 4, constant learning rate, disabled early stopping, and the 12-epoch exploratory budget.

The intended architecture-only change was to move away from the local loss/head-calibration probes that hurt ABI-197/198 and instead place an ungated `OrientedGapBridge` plus `OrientedLineRefinement` before ordinary mask, line, and centerline heads. The hypothesis was that long horizontal/vertical and dilated gap-spanning feature evidence might preserve ABI-196's recall and source balance while reducing unsupported clutter, without candidate-owned thresholding, postprocessing, Artifact Filters, target transforms, losses, metrics, data loading, or sampling policy.

Primary comparison is ABI-196 `run_20260903_195527_248472`, whose late36 selected checkpoint reached capped `val/filtered_dice` 0.4133 and whose whole-validation evaluation reached filtered Dice 0.4147. Secondary references are ABI-195 `run_20260903_135523_8976a0` as the 12-epoch ridge-detail parent, ABI-197 `run_20260903_230028_82d11d` and ABI-198 `run_20260904_000632_1a04ae` as negative local calibration/loss probes, and ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference.

## Capped exploratory metrics

ABI-199 completed 12/12 exploratory epochs with finite losses and non-collapsed, source-informative predictions. The Harness selected epoch 11 as the best checkpoint by `val/filtered_dice`.

| Metric | ABI-199 capped best |
| --- | ---: |
| Best epoch | 11 |
| Filtered Dice | 0.3949 |
| MIT filtered Dice | 0.3860 |
| Google filtered Dice | 0.4162 |
| Filtered precision | 0.3883 |
| Filtered recall | 0.4016 |
| Filtered contrail connectivity | 0.2677 |
| Filtered predicted-positive fraction | 0.003748 |
| Raw Dice | 0.4081 |
| Raw recall | 0.4291 |
| Train loss | 0.8493 |
| Validation loss | 0.8803 |

The final epoch shifted to a more conservative but lower-overlap operating point: filtered Dice 0.3856, MIT/Google filtered Dice 0.3775/0.4061, precision 0.4335, recall 0.3472, connectivity 0.2813, and filtered predicted-positive fraction 0.002902. This final-epoch precision and predicted-positive-area recovery was too recall-costly to become the selected checkpoint.

The trajectory was finite and generally improving but volatile near the end. Filtered Dice rose from 0.2172 at epoch 1 to 0.3546 at epoch 6, reached 0.3726 at epoch 8, dipped to 0.3434 at epoch 10, peaked at 0.3949 at epoch 11, and softened to 0.3856 at epoch 12. The best checkpoint near the end is informative, but the late movement alternated between recall-heavy clutter and conservative under-recall rather than showing a clean frontier-improving trend.

## Comparison

| Run | Branch | Budget | Best epoch | Filtered Dice | MIT | Google | Precision | Recall | Connectivity | Pred-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260903_135523_8976a0` | ABI-195 ridge-detail `bce_dice` | exploratory | 12 | 0.3891 | 0.3706 | 0.4369 | 0.4649 | 0.3346 | 0.4391 | 0.002608 |
| `run_20260903_195527_248472` | ABI-196 ridge-detail `bce_dice` | late_improving | 34 | 0.4133 | 0.4007 | 0.4442 | 0.4350 | 0.3936 | 0.3746 | 0.003278 |
| `run_20260903_230028_82d11d` | ABI-197 ridge-detail `bce_dice_cldice` | exploratory | 12 | 0.3838 | 0.3727 | 0.4111 | 0.3907 | 0.3771 | 0.3633 | 0.003498 |
| `run_20260904_000632_1a04ae` | ABI-198 consistency head `bce_dice` | exploratory | 11 | 0.3789 | 0.3726 | 0.3939 | 0.3857 | 0.3723 | 0.2366 | 0.003498 |
| `run_20260904_011242_2435ad` | ABI-199 oriented gap bridge `bce_dice` | exploratory | 11 | 0.3949 | 0.3860 | 0.4162 | 0.3883 | 0.4016 | 0.2677 | 0.003748 |
| `run_20260902_213856_2c04ac` | ABI-184 signed-detail line+centerline | late_improving | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.002615 |

ABI-199 is a mixed but not frontier-improving Result. Relative to ABI-197 and ABI-198, it clearly recovers aggregate filtered Dice, MIT filtered Dice, Google filtered Dice, and recall. Relative to ABI-195, it improves aggregate filtered Dice, MIT filtered Dice, and recall, but loses Google filtered Dice, precision, connectivity, and positive-area discipline. Relative to ABI-196, it loses about 0.0185 filtered Dice, 0.0147 MIT filtered Dice, 0.0280 Google filtered Dice, 0.0467 precision, 0.1069 connectivity, and increases filtered predicted-positive fraction, while only slightly improving capped recall by about 0.0080.

The proposal-specific objective was not met. The oriented gap bridge did not reduce ABI-196's predicted-positive burden and did not improve precision or connectivity. Its best checkpoint achieved recall-heavy source-informative overlap, but at the cost of weaker line connectivity and higher predicted-positive fraction. The final checkpoint shows that the architecture can become more conservative, but that operating point gives up too much recall and still does not recover ABI-184/195/196-level connectivity.

## Resource and contract observations

The Run stayed inside the active Workspace Configuration: exploratory budget, 12 effective epochs, batch size 4, constant learning rate, disabled early stopping, provider-owned source-balanced capped selection, provider-owned random mirroring, and A100 execution. The model summary reports approved `abi_16ch_plus_sza` input shape `[17, 256, 256]`; forbidden longitude and latitude source channels are excluded; output names are `mask_logits`, `line_logits`, and `centerline_logits`; and the model has 10,148,411 parameters under the 25,000,000 parameter ceiling.

Resource profiling completed successfully with about 10.85 GB peak allocated CUDA memory, about 11.90 GB peak reserved CUDA memory, and about 3,543 seconds total run wall time. This is inside the 3,600-second exploratory timeout but leaves only about a one-minute margin. No contract, resource, numerical, or lifecycle failure is indicated in the Harness-observed artifacts, but substantially heavier continuations of this exact branch would carry timeout risk.

## Failure classification

Classify ABI-199 as `bad_research_result`, not a Candidate bug, contract violation, Resource Failure, Harness Failure, or unknown failure. The Run completed cleanly and produced finite, non-collapsed, Dataset Source-informative predictions, but the scientific outcome regressed against the intended comparison target and did not satisfy the clutter/structure indicators that motivated the architecture change.

This Result does not justify a whole-validation Evaluation Request. Its capped filtered Dice remains below the ABI-196, ABI-181, ABI-192, and ABI-184 whole-validation-tested frontier, and the intended false-positive/line-support indicators moved in the wrong direction relative to ABI-196 and ABI-184. It also does not justify a late-improving budget request: the best checkpoint was not the final epoch, the final epoch traded recall for precision without matching the main references, and the exploratory run already consumed almost the full 3,600-second wall-clock budget.

## Decision

Do not promote ABI-199, do not repeat it unchanged, do not request whole-validation diagnostics for it, and do not request late36 continuation for this exact oriented gap bridge branch.

Retain ABI-196 as the current whole-validation aggregate filtered-Dice reference and ABI-184 as the precision/connectivity and negative-patch-discipline reference. Treat ABI-197/198/199 together as evidence that local loss/head/oriented-bridge modifications around the ridge-detail ASPP lineage can recover some recall but have not solved the false-positive and connectivity tradeoff. The next in-contract hypothesis should broaden away from this exact ridge-detail bridge local-edit axis, for example toward a materially different line-continuity architecture family, a simpler precision-preserving decoder branch, or a trusted data/training-policy frontier already owned by the Harness/provider. Candidate code must continue to use approved ABI channel inputs only and must not implement thresholding, data loading, losses, metrics, Artifact Filters, sampling behavior, or coordinate features.

No Capability Request, Evaluation Request, or Campaign Report is required from this Result.

## Artifact references

- `run_20260904_011242_2435ad/outputs/best_metrics.json`
- `run_20260904_011242_2435ad/outputs/final_metrics.json`
- `run_20260904_011242_2435ad/outputs/metrics.jsonl`
- `run_20260904_011242_2435ad/outputs/resource_profile.json`
- `run_20260904_011242_2435ad/outputs/model_summary.json`
- `run_20260904_011242_2435ad/outputs/prediction_samples/samples.json`
- `run_20260904_011242_2435ad/resolved_manifest.yaml`
- `run_20260903_195527_248472/outputs/best_metrics.json`
- `run_20260903_195527_248472/outputs/evaluations/eval_evalreq_abi196_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260903_195527_248472/outputs/evaluations/eval_evalreq_abi196_wholeval_failure_buckets_v1/threshold_sweep.json`
- `run_20260903_135523_8976a0/outputs/best_metrics.json`
- `run_20260903_230028_82d11d/outputs/best_metrics.json`
- `run_20260904_000632_1a04ae/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
