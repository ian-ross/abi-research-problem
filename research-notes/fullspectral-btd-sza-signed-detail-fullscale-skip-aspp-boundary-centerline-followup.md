# Full-spectral BTD+SZA signed-detail full-scale skip ASPP boundary+centerline follow-up

research-figures: []

## Scope

This note records the capped exploratory Result for ABI-193, Candidate `abi193_fullspectral_btd_sza_signed_detail_fullscale_skip_aspp_boundary_centerline_aux_v1`, Run `run_20260903_115807_8c4be1`.

ABI-193 was a family-development auxiliary-policy probe of the ABI-181 signed-detail full-scale skip ASPP lineage. It kept approved `abi_16ch_plus_sza` inputs, deterministic ABI-channel BTD features, signed detail streams, ASPP context, full-scale skip fusion, line-aware refinement, trusted `bce_dice`, `combined_source_balanced` traversal, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, and 12 exploratory epochs. The only intended policy change was adding a low-weight provider-derived Boundary Target auxiliary head beside the Centerline Target head.

Comparison references are ABI-181 `run_20260902_150611_cbbf35` as the current whole-validation aggregate filtered-Dice reference, ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference, ABI-192 `run_20260903_085513_f395ad` as the directional-lattice late36 recall comparator, and ABI-191 `run_20260903_075132_5cff8c` as the exploratory directional-lattice parent.

## Capped exploratory metrics

ABI-193 completed 12/12 exploratory epochs with finite losses and non-collapsed, source-informative predictions. The best checkpoint was also the final epoch.

| Metric | ABI-193 capped best |
| --- | ---: |
| Best epoch | 12 |
| Filtered Dice | 0.3934 |
| MIT filtered Dice | 0.3789 |
| Google filtered Dice | 0.4309 |
| Filtered precision | 0.4242 |
| Filtered recall | 0.3667 |
| Filtered contrail connectivity | 0.3919 |
| Filtered predicted-positive fraction | 0.003133 |
| Raw Dice | 0.4077 |
| Raw recall | 0.3923 |
| Train loss | 0.8527 |
| Validation loss | 0.8840 |

The epoch trajectory was noisy but still improving at the end: filtered Dice moved from 0.1784 at epoch 1 to 0.3710 at epoch 6, dipped through epochs 7-11, then reached the run best 0.3934 at epoch 12. The final jump makes the run finite and not plateau-proven, but the achieved operating point is below the existing signed-detail references under the same capped selection.

## Comparison

| Run | Branch | Best epoch | Filtered Dice | MIT | Google | Precision | Recall | Connectivity | Pred-positive fraction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260902_150611_cbbf35` | ABI-181 signed-detail late36 | 22 | 0.4104 | 0.3962 | 0.4486 | 0.4423 | 0.3828 | 0.3639 | 0.003136 |
| `run_20260902_213856_2c04ac` | ABI-184 line+centerline late36 | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.002615 |
| `run_20260903_085513_f395ad` | ABI-192 directional-lattice late36 | 36 | 0.4072 | 0.3930 | 0.4429 | 0.4304 | 0.3864 | 0.3500 | 0.003253 |
| `run_20260903_075132_5cff8c` | ABI-191 directional-lattice exploratory | 12 | 0.4041 | 0.3939 | 0.4297 | 0.4036 | 0.4045 | 0.3554 | 0.003633 |
| `run_20260903_115807_8c4be1` | ABI-193 boundary+centerline exploratory | 12 | 0.3934 | 0.3789 | 0.4309 | 0.4242 | 0.3667 | 0.3919 | 0.003133 |

The boundary+centerline auxiliary probe did not deliver the intended sharper-mask precision or negative-clutter gain. ABI-193's filtered Dice is about 0.017 below ABI-181 and about 0.013 below ABI-184/192. Precision is lower than ABI-181 and ABI-184, recall is lower than ABI-181/191/192, and source metrics are lower than the main references on MIT while only modestly competitive on Google. Connectivity improved over ABI-181/192 and ABI-191 but remained well below ABI-184's line+centerline value, so the boundary head did not replace the existing line-auxiliary connectivity signal.

The predicted-positive fraction is almost identical to ABI-181 and lower than ABI-191/192, but without the desired precision gain; it also remains higher than ABI-184. This suggests the low-weight boundary auxiliary did not primarily remove false-positive clutter, and may instead have spent capacity on edge localization without improving the aggregate precision/recall balance.

## Resource and contract observations

The Run stayed inside the active Workspace Configuration: exploratory budget, 12 effective epochs, batch size 4, constant learning rate, disabled early stopping, provider-owned source-balanced capped selection, and A100 execution. The model summary reports approved `abi_16ch_plus_sza` input shape `[17, 256, 256]`, forbidden longitude/latitude source channels excluded, auxiliary outputs `boundary_logits` and `centerline_logits`, and 9,838,851 parameters under the 25,000,000 parameter ceiling. Resource profile completed with about 9.0 GB peak allocated CUDA memory and about 2,890 seconds run wall time, within the 3,600-second exploratory timeout.

No contract, resource, numerical, or lifecycle failure is indicated in the Harness-observed artifacts.

## Interpretation

Classify ABI-193 as a valid, finite, scientifically negative capped exploratory Result for this exact boundary+centerline auxiliary policy. It is not a candidate_bug or resource failure, and it is not a basis for abandoning the broader signed-detail full-scale skip ASPP family. It does, however, argue against immediate further low-weight Boundary Target probes in this lineage: the main expected benefit, improved precision/connectivity or negative-patch discipline without a large recall cost, was not observed.

Because ABI-193 is clearly below the current whole-validation-tested frontier and does not show a distinctive positive tradeoff versus ABI-181, ABI-184, or ABI-192, a whole-validation failure-bucket Evaluation Request is not the best next handoff for this exact run. The more useful next step is to broaden away from auxiliary-target tweaks toward an in-contract architecture/front-end change that addresses the persistent precision/connectivity/negative-clutter tradeoff, or to revisit trusted loss/data-policy options only if they are tied to a clear hypothesis from existing diagnostics.

## Decision

Do not promote ABI-193, do not request late-improving budget for this boundary+centerline variant, and do not request whole-validation diagnostics for ABI-193 as the immediate next step.

Retain ABI-181 as the whole-validation aggregate filtered-Dice reference and ABI-184 as the precision/connectivity and negative-patch-discipline reference. Treat ABI-193 as evidence that a low-weight Boundary Target auxiliary head does not improve the current signed-detail ASPP operating point enough to justify continued local boundary-auxiliary tuning.

A reasonable next Candidate handoff is a broader in-contract scout or continuation that changes the representation rather than adding more auxiliary heads: for example, a high-resolution line-aware decoder with more explicit negative-clutter suppression in architecture only, a calibrated spectral/detail front end, or an allowed loss-policy variant selected to test precision/recall tradeoff without candidate-owned thresholding, data loading, losses, metrics, Artifact Filters, or coordinate features.

## Artifact references

- `run_20260903_115807_8c4be1/outputs/best_metrics.json`
- `run_20260903_115807_8c4be1/outputs/final_metrics.json`
- `run_20260903_115807_8c4be1/outputs/metrics.jsonl`
- `run_20260903_115807_8c4be1/outputs/resource_profile.json`
- `run_20260903_115807_8c4be1/outputs/model_summary.json`
- `run_20260903_115807_8c4be1/outputs/prediction_samples/samples.json`
- `run_20260903_115807_8c4be1/resolved_manifest.yaml`
- `run_20260902_150611_cbbf35/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260903_085513_f395ad/outputs/best_metrics.json`
- `run_20260903_085513_f395ad/outputs/evaluations/eval_evalreq_abi192_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
