# Full-spectral BTD+SZA cross-scale directional-consensus ASPP follow-up

research-figures: []

## Scope

This note records the capped exploratory Result for ABI-201, Candidate `abi201_fullspectral_btd_sza_crossscale_directional_consensus_aspp_bce_dice_line_centerline_aux_v1`, Run `run_20260904_032624_7e855a`.

ABI-201 was a family-development continuation after ABI-196 through ABI-200. It kept approved `abi_16ch_plus_sza` inputs, deterministic ABI-channel brightness-temperature-difference features, trusted `bce_dice`, trusted Line and Centerline auxiliary targets, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW at 0.0003, batch size 4, constant learning rate, disabled early stopping, and the 12-epoch exploratory budget.

The architecture-only change was a `CrossScaleDirectionalConsensusBridge` that fuses decoder, signed-detail, stem, full-scale context, and horizontal/vertical/diagonal line-context evidence through a bounded residual before ordinary refinement and the mask, line, and centerline heads. The intended effect was to preserve the strong line/connectivity behavior of the signed-detail ASPP lineage while discouraging unsupported isolated clutter. The Candidate did not implement thresholding, postprocessing, Artifact Filters, target transforms, custom losses, metrics, data loading, sampling policy, coordinate use, or runtime downloads.

Primary comparison is ABI-196 `run_20260903_195527_248472`, the current whole-validation aggregate filtered-Dice reference after its late36 and failure-bucket evaluation. Secondary references are ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference; ABI-195 as the high-precision ridge-detail parent; ABI-199/200 as recent negative bridge probes; and ABI-191/192 as directional-lattice comparators.

## Capped exploratory metrics

ABI-201 completed 12/12 exploratory epochs with finite losses and non-collapsed, Dataset Source-informative predictions. The Harness selected epoch 12 as the best checkpoint by `val/filtered_dice`, so the selected and final operating points are the same.

| Metric | ABI-201 capped best |
| --- | ---: |
| Best epoch | 12 |
| Filtered Dice | 0.3958 |
| MIT filtered Dice | 0.3751 |
| Google filtered Dice | 0.4497 |
| Filtered precision | 0.4587 |
| Filtered recall | 0.3481 |
| Filtered contrail connectivity | 0.4630 |
| Filtered predicted-positive fraction | 0.002749 |
| Raw Dice | 0.4101 |
| Raw recall | 0.3720 |
| Train loss | 0.8460 |
| Validation loss | 0.8877 |

The trajectory was finite but volatile, with useful late improvement. Filtered Dice rose from 0.1858 at epoch 1 to 0.3578 at epoch 6, reached 0.3814 at epoch 9, dipped to 0.3575 and 0.3599 at epochs 10 and 11, then reached its best value, 0.3958, at epoch 12. Connectivity similarly recovered strongly at the final epoch, from 0.2492 at epoch 11 to 0.4630 at epoch 12. This is not a monotone curve, but the best checkpoint at the exploratory ceiling makes the branch late-improving/ambiguous rather than clearly plateaued.

## Comparison

| Run | Branch | Budget | Best epoch | Filtered Dice | MIT | Google | Precision | Recall | Connectivity | Pred-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260903_135523_8976a0` | ABI-195 ridge-detail `bce_dice` | exploratory | 12 | 0.3891 | 0.3706 | 0.4369 | 0.4649 | 0.3346 | 0.4391 | 0.002608 |
| `run_20260903_195527_248472` | ABI-196 ridge-detail `bce_dice` | late_improving | 34 | 0.4133 | 0.4007 | 0.4442 | 0.4350 | 0.3936 | 0.3746 | 0.003278 |
| `run_20260903_230028_82d11d` | ABI-197 ridge-detail `bce_dice_cldice` | exploratory | 12 | 0.3838 | 0.3727 | 0.4111 | 0.3907 | 0.3771 | 0.3633 | 0.003498 |
| `run_20260904_011242_2435ad` | ABI-199 oriented gap bridge `bce_dice` | exploratory | 11 | 0.3949 | 0.3860 | 0.4162 | 0.3883 | 0.4016 | 0.2677 | 0.003748 |
| `run_20260904_022202_03c56b` | ABI-200 spectral-contrast bridge `bce_dice` | exploratory | 11 | 0.3916 | 0.3854 | 0.4074 | 0.4264 | 0.3620 | 0.2698 | 0.003077 |
| `run_20260904_032624_7e855a` | ABI-201 cross-scale directional consensus | exploratory | 12 | 0.3958 | 0.3751 | 0.4497 | 0.4587 | 0.3481 | 0.4630 | 0.002749 |
| `run_20260902_213856_2c04ac` | ABI-184 signed-detail line+centerline | late_improving | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.002615 |
| `run_20260903_085513_f395ad` | ABI-192 directional lattice | late_improving | 36 | 0.4072 | 0.3930 | 0.4429 | 0.4304 | 0.3864 | 0.3500 | 0.003253 |

ABI-201 is not a new aggregate frontier, but it is a useful tradeoff result. Relative to ABI-199, it improved aggregate filtered Dice slightly, improved Google filtered Dice by about 0.0335, improved precision by about 0.0704, improved connectivity by about 0.1953, and reduced filtered predicted-positive fraction by about 0.0010. The cost was lower recall and lower MIT filtered Dice. Relative to ABI-200, it improved aggregate Dice, Google Dice, precision, connectivity, and positive-area discipline, while again losing MIT Dice and some recall.

Relative to ABI-196's selected late36 checkpoint, ABI-201 remains lower on aggregate filtered Dice by about 0.0174 and lower on MIT Dice by about 0.0255, but it is higher on Google Dice, precision, connectivity, and predicted-positive discipline at the capped selected checkpoint. Relative to ABI-184, ABI-201 nearly matches connectivity but remains lower on aggregate, MIT, Google, precision, recall, and predicted-positive discipline. This makes ABI-201 a promising exploratory bridge tradeoff, not a whole-validation promotion candidate.

## Resource and contract observations

The Run stayed inside the active Workspace Configuration: exploratory budget, 12 effective epochs, batch size 4, constant learning rate, disabled early stopping, provider-owned source-balanced capped selection, provider-owned random mirroring, and A100 execution. The resolved manifest uses approved `abi_16ch_plus_sza` input mode; forbidden longitude and latitude source channels are excluded; outputs are `mask_logits`, `line_logits`, and `centerline_logits`; and the model summary reports 8,172,287 parameters under the 25,000,000 parameter ceiling.

Resource profiling completed successfully with about 9.73 GiB peak allocated CUDA memory, about 11.08 GiB peak reserved CUDA memory, and about 3,304 seconds total run wall time, inside the 3,600-second exploratory timeout. This is near the timeout but still completed without contract, resource, numerical, or lifecycle failure.

## Failure classification

Classify ABI-201 as a valid finite exploratory Result, not a Candidate bug, contract violation, Resource Failure, Harness Failure, unknown failure, or hard scientific stop. It completed cleanly and produced non-collapsed, Dataset Source-informative predictions. The scientific result did not beat ABI-196/184 on the primary aggregate frontier, but it achieved the proposal-specific goal better than ABI-199/200 by restoring precision, connectivity, and positive-area discipline while remaining near their capped filtered-Dice range.

This Result does not yet justify a promotion claim. A whole-validation Evaluation Request would be defensible only after either a stronger capped checkpoint or a late-improving continuation, because ABI-201 is still below ABI-196, ABI-192, and ABI-184 on capped aggregate filtered Dice. However, the final-epoch best checkpoint, finite source-informative behavior, high Google Dice, high connectivity, and conservative predicted-positive fraction make it eligible for a close-continuation late36 budget request under the approved policy.

## Decision

Do not promote ABI-201 and do not request whole-validation diagnostics for this exact exploratory checkpoint yet.

Retain ABI-196 as the current whole-validation aggregate filtered-Dice reference and ABI-184 as the precision/connectivity and negative-patch-discipline reference. Treat ABI-201 as the strongest recent bridge result after ABI-199/200 for precision/connectivity/positive-area discipline, but with an unresolved MIT and recall regression.

A reasonable next in-contract handoff is a late-improving close-continuation of the ABI-201 cross-scale directional-consensus bridge, with a candidate-local `budget_request.yaml` citing parent Run `run_20260904_032624_7e855a`, requesting the approved 36-epoch `late_improving` budget, and falling back to exploratory if denied. The expected diagnostic is whether the final-epoch improvement can recover MIT/recalibrated recall while preserving the ABI-201 connectivity and predicted-positive discipline. Candidate code must continue to use approved ABI channel inputs only and must not implement thresholding, data loading, losses, metrics, Artifact Filters, sampling behavior, or coordinate features.

No Capability Request, Evaluation Request, or Campaign Report is required from this Result.

## Artifact references

- `run_20260904_032624_7e855a/outputs/best_metrics.json`
- `run_20260904_032624_7e855a/outputs/final_metrics.json`
- `run_20260904_032624_7e855a/outputs/metrics.jsonl`
- `run_20260904_032624_7e855a/outputs/resource_profile.json`
- `run_20260904_032624_7e855a/outputs/model_summary.json`
- `run_20260904_032624_7e855a/outputs/prediction_samples/samples.json`
- `run_20260904_032624_7e855a/resolved_manifest.yaml`
- `run_20260904_032624_7e855a/candidate/PROPOSAL.md`
- `run_20260903_195527_248472/outputs/best_metrics.json`
- `run_20260903_195527_248472/outputs/evaluations/eval_evalreq_abi196_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260903_135523_8976a0/outputs/best_metrics.json`
- `run_20260903_230028_82d11d/outputs/best_metrics.json`
- `run_20260904_011242_2435ad/outputs/best_metrics.json`
- `run_20260904_022202_03c56b/outputs/best_metrics.json`
- `run_20260903_085513_f395ad/outputs/best_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
