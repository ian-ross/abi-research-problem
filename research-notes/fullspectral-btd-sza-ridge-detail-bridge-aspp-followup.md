# Full-spectral BTD+SZA ridge-detail bridge ASPP follow-up

research-figures: []

## Scope

This note records the capped exploratory Result for ABI-195, Candidate `abi195_fullspectral_btd_sza_ridge_detail_bridge_aspp_bce_dice_line_centerline_aux_v1`, Run `run_20260903_135523_8976a0`.

ABI-195 was a family-development continuation of the signed-detail full-scale skip ASPP lineage. It kept approved `abi_16ch_plus_sza` inputs, deterministic ABI-channel BTD features, signed detail streams, ASPP context, full-scale skip fusion, trusted `bce_dice`, trusted `combined_source_balanced` traversal, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, and the 12-epoch exploratory budget. The intended architecture-only change was an additive `RidgePreservingDetailBridge` that fuses decoder context with signed-detail and stem features before final line-aware refinement, with provider-derived Line and Centerline auxiliary targets.

Comparison references are ABI-181 `run_20260902_150611_cbbf35` as the current whole-validation aggregate filtered-Dice reference, ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference, ABI-192 `run_20260903_085513_f395ad` as the directional-lattice late36 recall comparator, and ABI-194 `run_20260903_125403_548c08` as the negative clutter-gate result that ABI-195 was meant to recover from.

## Capped exploratory metrics

ABI-195 completed 12/12 exploratory epochs with finite losses and non-collapsed, source-informative predictions. The best checkpoint was the final epoch.

| Metric | ABI-195 capped best |
| --- | ---: |
| Best epoch | 12 |
| Filtered Dice | 0.3891 |
| MIT filtered Dice | 0.3706 |
| Google filtered Dice | 0.4369 |
| Filtered precision | 0.4649 |
| Filtered recall | 0.3346 |
| Filtered contrail connectivity | 0.4391 |
| Filtered predicted-positive fraction | 0.002608 |
| Raw Dice | 0.4045 |
| Raw recall | 0.3578 |
| Train loss | 0.8519 |
| Validation loss | 0.8864 |

The trajectory was noisy but still improving at the end: filtered Dice rose from 0.2157 at epoch 1 to 0.3664 at epoch 7, dipped at epoch 8, recovered to 0.3784 at epoch 9, dipped again at epoch 10, then improved through epochs 11 and 12 to the run-best 0.3891. The final epoch also delivered the highest filtered precision and highest connectivity of the run while keeping the filtered predicted-positive fraction low.

## Comparison

| Run | Branch | Best epoch | Filtered Dice | MIT | Google | Precision | Recall | Connectivity | Pred-positive fraction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260902_150611_cbbf35` | ABI-181 signed-detail late36 | 22 | 0.4104 | 0.3962 | 0.4486 | 0.4423 | 0.3828 | 0.3639 | 0.003136 |
| `run_20260902_213856_2c04ac` | ABI-184 line+centerline late36 | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.002615 |
| `run_20260903_085513_f395ad` | ABI-192 directional-lattice late36 | 36 | 0.4072 | 0.3930 | 0.4429 | 0.4304 | 0.3864 | 0.3500 | 0.003253 |
| `run_20260903_115807_8c4be1` | ABI-193 boundary+centerline exploratory | 12 | 0.3934 | 0.3789 | 0.4309 | 0.4242 | 0.3667 | 0.3919 | 0.003133 |
| `run_20260903_125403_548c08` | ABI-194 clutter-gate exploratory | 12 | 0.3813 | 0.3666 | 0.4178 | 0.4205 | 0.3487 | 0.2139 | 0.003005 |
| `run_20260903_135523_8976a0` | ABI-195 ridge-detail bridge exploratory | 12 | 0.3891 | 0.3706 | 0.4369 | 0.4649 | 0.3346 | 0.4391 | 0.002608 |

ABI-195 substantially repaired the specific ABI-194 clutter-gate regression. Relative to ABI-194, it improved aggregate filtered Dice by about 0.0079, Google filtered Dice by about 0.0191, precision by about 0.0443, and filtered contrail connectivity by about 0.225 while reducing the predicted-positive fraction. This supports the hypothesis that preserving ridge/detail evidence in the decoder is better than post-refinement learned clutter suppression for this lineage.

Against the stronger references, ABI-195 is mixed rather than competitive on aggregate overlap. It remains about 0.0174 filtered Dice behind ABI-184 and about 0.0213 behind ABI-181 capped best. Its precision and predicted-positive fraction are close to ABI-184's disciplined operating point, and its connectivity is much closer to ABI-184 than to ABI-181/192/194, but recall is the lowest among the main comparators. The result therefore looks like a high-precision, high-connectivity but recall-limited operating point, especially on MIT.

## Resource and contract observations

The Run stayed inside the active Workspace Configuration: exploratory budget, 12 effective epochs, batch size 4, constant learning rate, disabled early stopping, provider-owned source-balanced capped selection, and A100 execution. The model summary reports approved `abi_16ch_plus_sza` input shape `[17, 256, 256]`, forbidden longitude/latitude source channels excluded, auxiliary outputs `line_logits` and `centerline_logits`, and 10,041,211 parameters under the 25,000,000 parameter ceiling.

Resource profiling completed successfully with about 10.9 GB peak allocated CUDA memory and about 3,423 seconds total run wall time, within the 3,600-second exploratory timeout. No contract, resource, numerical, or lifecycle failure is indicated in the Harness-observed artifacts.

## Interpretation

Classify ABI-195 as a valid, finite, scientifically mixed capped exploratory Result. It is not a candidate bug or resource failure. It does not beat the current whole-validation-tested frontier, but it did meet the branch-specific recovery criterion versus ABI-194: the ridge-preserving bridge restored connectivity and precision discipline without predicted-positive inflation.

The final-epoch best checkpoint, improving late trajectory, finite non-collapsed predictions, source-informative behavior, and distinctive precision/connectivity tradeoff make ABI-195 eligible for a bounded late-improving close-continuation under the approved `late_improving` budget policy. The justification is not that ABI-195 is already promotion-competitive; it is that the 12-epoch cap may be truncating a branch that only reached its best high-connectivity, low-positive operating point at epoch 12.

## Decision

Do not promote ABI-195 and do not request whole-validation diagnostics for this 12-epoch checkpoint as the immediate next handoff. The capped score is below ABI-181/184/192 and remains representative feasibility evidence only.

Keep ABI-181 as the whole-validation aggregate filtered-Dice reference, ABI-184 as the precision/connectivity and negative-patch-discipline reference, and ABI-192 as the recall-balanced directional-context comparator. Treat ABI-195 as evidence that the ridge-detail bridge branch is worth one late36 close-continuation, with unchanged architecture/training policy except for a candidate-local `budget_request.yaml` referencing `run_20260903_135523_8976a0`. If that continuation fails to lift recall/source balance while preserving precision/connectivity, broaden away from this exact bridge branch rather than adding another post-refinement gate.

## Artifact references

- `run_20260903_135523_8976a0/outputs/best_metrics.json`
- `run_20260903_135523_8976a0/outputs/final_metrics.json`
- `run_20260903_135523_8976a0/outputs/metrics.jsonl`
- `run_20260903_135523_8976a0/outputs/resource_profile.json`
- `run_20260903_135523_8976a0/outputs/model_summary.json`
- `run_20260903_135523_8976a0/outputs/prediction_samples/samples.json`
- `run_20260903_135523_8976a0/resolved_manifest.yaml`
- `run_20260902_150611_cbbf35/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260903_085513_f395ad/outputs/best_metrics.json`
- `run_20260903_115807_8c4be1/outputs/best_metrics.json`
- `run_20260903_125403_548c08/outputs/best_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
