# Full-spectral BTD+SZA signed-detail full-scale skip ASPP clutter-gate follow-up

research-figures: []

## Scope

This note records the capped exploratory Result for ABI-194, Candidate `abi194_fullspectral_btd_sza_signed_detail_fullscale_skip_aspp_clutter_gate_line_centerline_aux_v1`, Run `run_20260903_125403_548c08`.

ABI-194 was a family-development continuation of the signed-detail full-scale skip ASPP lineage. It kept approved `abi_16ch_plus_sza` inputs, deterministic ABI-channel BTD features, signed detail streams, ASPP context, full-scale skip fusion, line-aware refinement, trusted `bce_dice`, trusted `combined_source_balanced` traversal, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, and the 12-epoch exploratory budget. The intended architecture-only change was a learned clutter-gate refinement after the final line-aware refinement, supervised only through the trusted mask loss and provider-derived Line plus Centerline auxiliary targets.

Comparison references are ABI-181 `run_20260902_150611_cbbf35` as the whole-validation aggregate filtered-Dice reference, ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference, ABI-192 `run_20260903_085513_f395ad` as the directional-lattice late36 recall comparator, and ABI-193 `run_20260903_115807_8c4be1` as the most recent boundary+centerline negative-control probe.

## Capped exploratory metrics

ABI-194 completed 12/12 exploratory epochs with finite losses and non-collapsed, source-informative predictions. The best checkpoint was the final epoch.

| Metric | ABI-194 capped best |
| --- | ---: |
| Best epoch | 12 |
| Filtered Dice | 0.3813 |
| MIT filtered Dice | 0.3666 |
| Google filtered Dice | 0.4178 |
| Filtered precision | 0.4205 |
| Filtered recall | 0.3487 |
| Filtered contrail connectivity | 0.2139 |
| Filtered predicted-positive fraction | 0.003005 |
| Raw Dice | 0.3958 |
| Raw recall | 0.3728 |
| Train loss | 0.8501 |
| Validation loss | 0.8813 |

The trajectory was noisy but not collapsed: filtered Dice moved from 0.2197 at epoch 1 to 0.3676 at epoch 6, dipped and recovered to 0.3706 at epoch 9, fell at epoch 10, then reached 0.3813 at epoch 12. The predicted-positive fraction shrank from 0.00695 at epoch 1 to 0.00301 at epoch 12, but the shrinkage did not produce a useful precision/connectivity operating point.

## Comparison

| Run | Branch | Best epoch | Filtered Dice | MIT | Google | Precision | Recall | Connectivity | Pred-positive fraction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260902_150611_cbbf35` | ABI-181 signed-detail late36 | 22 | 0.4104 | 0.3962 | 0.4486 | 0.4423 | 0.3828 | 0.3639 | 0.003136 |
| `run_20260902_213856_2c04ac` | ABI-184 line+centerline late36 | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.002615 |
| `run_20260903_085513_f395ad` | ABI-192 directional-lattice late36 | 36 | 0.4072 | 0.3930 | 0.4429 | 0.4304 | 0.3864 | 0.3500 | 0.003253 |
| `run_20260903_115807_8c4be1` | ABI-193 boundary+centerline exploratory | 12 | 0.3934 | 0.3789 | 0.4309 | 0.4242 | 0.3667 | 0.3919 | 0.003133 |
| `run_20260903_125403_548c08` | ABI-194 clutter-gate line+centerline exploratory | 12 | 0.3813 | 0.3666 | 0.4178 | 0.4205 | 0.3487 | 0.2139 | 0.003005 |

The clutter-gate refinement did not meet the family-development success criterion. Relative to ABI-193, ABI-194 is lower in aggregate filtered Dice by about 0.012, lower on both Dataset Sources, slightly lower in precision, lower in recall, and much lower in filtered contrail connectivity. Its only favorable secondary movement is a small reduction in filtered predicted-positive fraction, but the reduction is not coupled to improved precision or overlap and remains less disciplined than ABI-184's lower-positive, much higher-precision operating point.

Relative to the whole-validation-tested frontier, ABI-194 is about 0.029 filtered-Dice behind ABI-181 capped best and about 0.025-0.026 behind ABI-184/192. The intended architecture-only negative-clutter suppression appears to have removed or weakened useful line continuity evidence rather than separating clutter from contrails.

## Resource and contract observations

The Run stayed inside the active Workspace Configuration: exploratory budget, 12 effective epochs, batch size 4, constant learning rate, disabled early stopping, provider-owned source-balanced capped selection, and A100 execution. The model summary reports approved `abi_16ch_plus_sza` input shape `[17, 256, 256]`, forbidden longitude/latitude source channels excluded, auxiliary outputs `line_logits` and `centerline_logits`, and 9,954,611 parameters under the 25,000,000 parameter ceiling.

Resource profiling completed successfully with about 10.5 GB peak allocated CUDA memory and about 3,244 seconds total run wall time, within the 3,600-second exploratory timeout. No contract, resource, numerical, or lifecycle failure is indicated in the Harness-observed artifacts.

## Interpretation

Classify ABI-194 as a valid, finite, scientifically negative capped exploratory Result for this exact learned clutter-gate continuation. It is not a candidate bug or resource failure, and it is not evidence to abandon the broader signed-detail full-scale skip ASPP family. It does argue against immediate continuation of this exact clutter-gate branch: the branch failed to improve ABI-193 and strongly regressed the connectivity signal that ABI-184's line+centerline variant had preserved.

Although the best checkpoint occurred at epoch 12, the achieved operating point is too far below the established capped and whole-validation-tested references, and the secondary tradeoff is not distinctive enough to justify a late-improving budget request. The small predicted-positive-fraction reduction without precision/connectivity gain suggests the gate is suppressing useful thin-line evidence along with clutter.

## Decision

Do not promote ABI-194, do not request whole-validation diagnostics for ABI-194, and do not request a late36 continuation for this exact clutter-gate design.

Retain ABI-181 as the current whole-validation aggregate filtered-Dice reference, ABI-184 as the precision/connectivity and negative-patch-discipline reference, and ABI-192 as the stronger recall-balanced directional-context comparator. Treat ABI-194 as evidence that local learned post-refinement clutter gating is a poor way to solve the current precision/connectivity tradeoff in this lineage.

A reasonable next Candidate handoff should broaden the frontier rather than make another small auxiliary/gate tweak: for example, a different high-resolution decoder/front-end that preserves line continuity earlier in the network, an in-contract spectral/detail calibration change that avoids post-hoc suppression, or an allowed trusted loss/data-policy probe tied to a concrete precision-recall hypothesis. Candidate code must continue to avoid thresholding, postprocessing, custom losses, data loading, sampling, augmentation transforms, Artifact Filters, runtime downloads, filesystem persistence, and coordinate features.

## Artifact references

- `run_20260903_125403_548c08/outputs/best_metrics.json`
- `run_20260903_125403_548c08/outputs/final_metrics.json`
- `run_20260903_125403_548c08/outputs/metrics.jsonl`
- `run_20260903_125403_548c08/outputs/resource_profile.json`
- `run_20260903_125403_548c08/outputs/model_summary.json`
- `run_20260903_125403_548c08/outputs/prediction_samples/samples.json`
- `run_20260903_125403_548c08/resolved_manifest.yaml`
- `run_20260902_150611_cbbf35/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260903_085513_f395ad/outputs/best_metrics.json`
- `run_20260903_115807_8c4be1/outputs/best_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
