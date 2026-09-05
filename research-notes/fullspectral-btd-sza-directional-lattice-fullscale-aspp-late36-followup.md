# Full-spectral BTD+SZA directional-lattice full-scale skip ASPP late36 follow-up

research-figures: []

## Scope

This note records ABI-192 after late-improving Run `run_20260903_085513_f395ad` completed.

Source Runs:

- ABI-192 directional-lattice full-scale skip ASPP late36 continuation: `run_20260903_085513_f395ad`
- ABI-191 exploratory directional-lattice parent: `run_20260903_075132_5cff8c`
- ABI-181 signed-detail full-scale skip ASPP late36 whole-validation aggregate reference: `run_20260902_150611_cbbf35`; Evaluation `eval_evalreq_abi181_wholeval_failure_buckets_v1`
- ABI-184 Line plus Centerline auxiliary late36 whole-validation precision/connectivity reference: `run_20260902_213856_2c04ac`; Evaluation `eval_evalreq_abi184_wholeval_failure_buckets_v1`
- ABI-188/189 detached line-logit fusion references: `run_20260903_031950_88e745`, `run_20260903_041610_f244a9`
- ABI-068 broader frequency-gated line U-Net source-balance/connectivity comparator: `run_20260828_010836_4ccc77`

ABI-192 was a close late-improving continuation of ABI-191. It retained provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD features derived only from approved ABI channels, Solar Geometry Input, signed local/mid-scale detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, the zero-initialized multi-orientation directional lattice bridge, line-aware final refinement, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The only intended research change from ABI-191 was the Harness-reviewed `late_improving` budget request.

## Contract and resource observation

ABI-192 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary output `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 10,060,450 parameters, below the 25,000,000-parameter smoke ceiling. The late-improving request was approved with `budget_class_effective: late_improving`, `effective_max_epochs: 36`, and parent Run `run_20260903_075132_5cff8c`. The Run completed on the A100 at batch size 4 with 9,773.0 seconds total wall time, 5,452.0 seconds training wall time, 4,318.7 seconds validation wall time, 13.52 training samples per second, 17.07 validation samples per second, 10,720,424,960 bytes peak CUDA allocated, and 12,721,324,032 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 36.

## Best-validation comparison

| Run | Candidate | Best epoch | Filtered Dice | Raw Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260903_085513_f395ad` | ABI-192 directional lattice late36 | 36 | 0.4072 | 0.4222 | 0.3930 | 0.4429 | 0.4304 | 0.3864 | 0.3500 | 0.00325 |
| `run_20260903_075132_5cff8c` | ABI-191 directional lattice exploratory | 12 | 0.4041 | 0.4180 | 0.3939 | 0.4297 | 0.4036 | 0.4045 | 0.3554 | 0.00363 |
| `run_20260902_150611_cbbf35` | ABI-181 centerline-only late36 | 22 | 0.4104 | 0.4254 | 0.3962 | 0.4486 | 0.4423 | 0.3828 | 0.3639 | 0.00314 |
| `run_20260902_213856_2c04ac` | ABI-184 line+centerline late36 | 23 | 0.4066 | 0.4227 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.00261 |
| `run_20260903_041610_f244a9` | ABI-189 line-logit fusion late36 | 22 | 0.4022 | 0.4157 | 0.3917 | 0.4290 | 0.3964 | 0.4083 | 0.2962 | 0.00373 |
| `run_20260903_031950_88e745` | ABI-188 line-logit fusion exploratory | 12 | 0.4013 | 0.4160 | 0.3898 | 0.4317 | 0.4250 | 0.3801 | 0.3903 | 0.00324 |
| `run_20260828_010836_4ccc77` | ABI-068 frequency-gated line U-Net focal-Tversky | 12 | 0.3964 | 0.4100 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |

ABI-192 is a useful positive capped late-improving continuation. Relative to ABI-191, it improved aggregate filtered Dice by 0.0032, raw Dice by 0.0041, Google filtered Dice by 0.0132, precision by 0.0269, and positive-area discipline, while losing 0.0009 MIT filtered Dice, 0.0182 recall, and 0.0054 connectivity. The late budget therefore converted ABI-191's exploratory final-epoch jump into a slightly stronger and cleaner operating point, rather than revealing that the jump was only a one-epoch fluctuation.

Relative to ABI-181, ABI-192 remains lower on aggregate filtered Dice by 0.0032, raw Dice by 0.0032, MIT filtered Dice by 0.0032, Google filtered Dice by 0.0057, precision by 0.0119, and connectivity by 0.0138, while recall is slightly higher by 0.0035. Relative to ABI-184, ABI-192 edges the capped primary metric by 0.0006 and improves MIT filtered Dice and recall, but gives up ABI-184's main strength: precision is lower by 0.0546, connectivity by 0.1133, Google filtered Dice by 0.0126, and predicted-positive fraction is larger. These comparisons remain capped representative evidence, not full-data promotion evidence.

## Late-improving trajectory

ABI-192 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was:

`0.1898, 0.2756, 0.2955, 0.3332, 0.2929, 0.3675, 0.3390, 0.3650, 0.3804, 0.3671, 0.3434, 0.3960, 0.3473, 0.3722, 0.3678, 0.3795, 0.3753, 0.3576, 0.3881, 0.3794, 0.4041, 0.3961, 0.3543, 0.4020, 0.3772, 0.3901, 0.3882, 0.3772, 0.4009, 0.3630, 0.3905, 0.3930, 0.3935, 0.3684, 0.3855, 0.4072`.

The selected checkpoint was the final late36 epoch. The trajectory stayed noisy after epoch 12, but repeatedly returned to the 0.40 filtered-Dice range at epochs 21, 24, 29, and finally 36. This supports the late-improving extension as informative: ABI-191's final-epoch jump was not a strict ceiling, and the branch still had recoverable aggregate performance late in training. It does not by itself justify a further budget request, because the active trusted policy defines the late-improving ceiling at 36 epochs and capped evidence is already sufficient to decide whether to request diagnostics.

At the selected epoch 36 checkpoint, raw Dice was 0.4222 versus filtered Dice 0.4072, raw recall 0.4132 versus filtered recall 0.3864, and raw predicted-positive fraction 0.00347 versus filtered predicted-positive fraction 0.00325. Source-stratified filtered Dice was 0.3930 for MIT and 0.4429 for Google. MIT had filtered precision 0.4359, recall 0.3578, connectivity 0.3782, and predicted-positive fraction 0.00443. Google had filtered precision 0.4187, recall 0.4701, connectivity 0.3219, and predicted-positive fraction 0.00207. Raw-to-filtered differences are modest enough that this does not indicate primary Artifact Filter dependence.

The fixed first-four retained prediction samples include one empty/negative perfect case and three near-zero per-sample Dice cases under the Harness `first_n` retention policy. They are traceability samples and should not be treated as representative qualitative evidence for the validation distribution.

## Interpretation

Classify ABI-192 as a completed, finite, non-collapsed, scientifically useful positive capped late-improving continuation. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The narrow late36 hypothesis is partly supported. The directional-lattice mechanism improved over its ABI-191 parent and now sits between ABI-181's aggregate whole-validation reference and ABI-184's precision/connectivity reference on the capped primary metric. It also avoids ABI-189's severe connectivity decline and ABI-190's local calibration failure. The tradeoff is still not solved: ABI-192 did not reach ABI-181's aggregate/source Dice or ABI-184's connected high-precision operating point, and its Google connectivity is weaker than desired.

The result argues for diagnostic evaluation rather than another architecture tweak immediately. ABI-192 is close enough to ABI-181 and ABI-184 on capped aggregate filtered Dice, selected the final late36 epoch, and changes the error tradeoff toward more recall than ABI-184 with cleaner precision than ABI-191. A whole-validation failure-bucket review can test whether this capped signal survives on the full Working Validation Split and whether its MIT/Google and negative-patch behavior is more useful than the existing ABI-181/184 references.

## Decision

Do not promote ABI-192 and do not reinterpret this capped representative result as full-data evidence. Retain ABI-181 as the strongest whole-validation-tested aggregate filtered-Dice Result and ABI-184 as the strongest whole-validation-tested precision/connectivity and negative-patch-discipline reference in this signed-detail/full-scale skip ASPP lineage.

Do not repeat ABI-192 unchanged and do not request a further epoch extension. A reasonable next Autonomy Step is a bounded whole-validation failure-bucket Evaluation Request for `run_20260903_085513_f395ad`. The diagnostic should compare ABI-192 with ABI-181 and ABI-184 on full-validation aggregate/source Dice, precision/recall calibration, connectivity, negative-patch clutter, positive-patch misses, and Artifact Filter dependence. If whole validation confirms an aggregate/recall improvement without excessive connectivity or source degradation, ABI-192 can become a new directional-lattice diagnostic reference; if it falls below ABI-181/184 on the full split, stop this directional-lattice late-budget branch and broaden to a different high-resolution line-aware architecture, trusted data-policy probe, or allowed loss/auxiliary configuration. No Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260903_085513_f395ad/outputs/best_metrics.json`
- `run_20260903_085513_f395ad/outputs/final_metrics.json`
- `run_20260903_085513_f395ad/outputs/metrics.jsonl`
- `run_20260903_085513_f395ad/outputs/resource_profile.json`
- `run_20260903_085513_f395ad/outputs/model_summary.json`
- `run_20260903_085513_f395ad/outputs/prediction_samples/samples.json`
- `run_20260903_085513_f395ad/outputs/validation_postprocessing/index.json`
- `run_20260903_085513_f395ad/resolved_manifest.yaml`
- `run_20260903_085513_f395ad/candidate/PROPOSAL.md`
- `run_20260903_085513_f395ad/candidate/budget_request.yaml`
- `run_20260903_075132_5cff8c/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260903_041610_f244a9/outputs/best_metrics.json`
- `run_20260903_031950_88e745/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
