# Full-spectral BTD+SZA signed-detail full-scale skip ASPP line-aux follow-up

research-figures: []

## Scope

This note records ABI-183 after Run `run_20260902_204128_bba815` completed.

Source Runs:

- ABI-183 signed-detail full-scale skip ASPP with added Line Target auxiliary supervision: `run_20260902_204128_bba815`
- ABI-181 signed-detail full-scale skip ASPP late36 aggregate reference: `run_20260902_150611_cbbf35`; whole-validation Evaluation `eval_evalreq_abi181_wholeval_failure_buckets_v1`
- ABI-173 signed-detail full-scale skip ASPP 12-epoch parent: `run_20260901_234732_bd5917`; whole-validation Evaluation `eval_evalreq_abi173_wholeval_failure_buckets_v1`
- ABI-182 signed-detail line-consensus late36 comparator: `run_20260902_175152_51d2d9`
- ABI-154 full-scale skip ASPP/detail decoder precision-connectivity reference: `run_20260901_071026_32d3ec`
- ABI-068 frequency-gated line U-Net focal-Tversky source-balance comparator: `run_20260828_010836_4ccc77`

ABI-183 is a controlled family-development continuation of ABI-181/ABI-173. It retained provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD features derived only from approved ABI channels, Solar Geometry Input, signed local/mid-scale detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, BCE-Dice primary loss, source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The intended research change from ABI-181 was adding a provider-derived Line Target auxiliary head at weight 0.01 alongside the Centerline Target auxiliary head at weight 0.02.

## Contract and resource observation

ABI-183 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary outputs `line_logits` and `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 9,838,851 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,874.4 seconds total wall time, 1,524.6 seconds training wall time, 1,347.6 seconds validation wall time, 16.12 training samples per second, 18.24 validation samples per second, 9,041,055,744 bytes peak CUDA allocated, and 10,508,828,672 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 12, the final exploratory epoch.

## Best-validation comparison

| Run | Candidate | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260902_204128_bba815` | ABI-183 signed-detail full-scale skip ASPP + line aux | 12 | 0.3966 | 0.3805 | 0.4389 | 0.4468 | 0.3565 | 0.4546 | 0.00289 |
| `run_20260902_150611_cbbf35` | ABI-181 signed-detail full-scale skip ASPP late36 | 22 | 0.4104 | 0.3962 | 0.4486 | 0.4423 | 0.3828 | 0.3639 | 0.00314 |
| `run_20260901_234732_bd5917` | ABI-173 signed-detail full-scale skip ASPP parent | 12 | 0.3962 | 0.3838 | 0.4269 | 0.4238 | 0.3720 | 0.3203 | 0.00318 |
| `run_20260902_175152_51d2d9` | ABI-182 signed-detail line-consensus late36 | 32 | 0.4035 | 0.3898 | 0.4362 | 0.4010 | 0.4061 | 0.3365 | 0.00367 |
| `run_20260901_071026_32d3ec` | ABI-154 full-scale skip ASPP/detail decoder | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260828_010836_4ccc77` | ABI-068 frequency-gated line U-Net focal-Tversky | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |

ABI-183 produced the highest raw Dice among the local best-runs listing observed in this step (`val/raw_dice` 0.4119), but the v0 primary metric is `val/filtered_dice`. On the primary metric, ABI-183 did not displace ABI-181's late36 reference. It narrowly exceeds ABI-173 on aggregate filtered Dice, with a large connectivity improvement and better precision/positive-area discipline, but lower MIT Dice and lower recall.

Relative to ABI-181, ABI-183 trails aggregate filtered Dice by 0.0138, MIT by 0.0157, Google by 0.0098, and recall by 0.0263. It improves filtered connectivity substantially, 0.4546 versus 0.3639, and slightly improves precision/positive-area discipline. Relative to ABI-182, ABI-183 has lower aggregate and MIT Dice and lower recall, but better Google Dice, precision, connectivity, and a smaller predicted-positive fraction. Relative to ABI-154, ABI-183 gives similar aggregate Dice with lower precision but slightly higher recall and connectivity. Relative to ABI-068, ABI-183 has similar aggregate Dice and better Google Dice/connectivity, but worse MIT Dice and recall.

## Exploratory trajectory

ABI-183 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was:

`0.1928, 0.2914, 0.2920, 0.3046, 0.3376, 0.3536, 0.3621, 0.3600, 0.3871, 0.3604, 0.3622, 0.3966`.

The best checkpoint occurred at epoch 12, with a late jump from 0.3622 at epoch 11 to 0.3966 at epoch 12. At the selected checkpoint, raw Dice was 0.4119, filtered Dice was 0.3966, filtered precision was 0.4468, filtered recall was 0.3565, filtered connectivity was 0.4546, and filtered predicted-positive fraction was 0.00289. Source-stratified filtered Dice was 0.3805 for MIT and 0.4389 for Google. MIT had filtered precision 0.4448, recall 0.3325, connectivity 0.4353, and predicted-positive fraction 0.00404; Google had filtered precision 0.4516, recall 0.4269, connectivity 0.4739, and predicted-positive fraction 0.00175.

Raw-to-filtered differences were modest: raw Dice 0.4119 versus filtered Dice 0.3966, raw recall 0.3820 versus filtered recall 0.3565, and raw predicted-positive fraction 0.00310 versus filtered predicted-positive fraction 0.00289. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples include three empty/negative perfect cases and one near-zero per-sample Dice case under the `first_n` retention policy; they are traceability samples and should not be treated as representative qualitative evidence for the validation distribution.

## Interpretation

Classify ABI-183 as a completed, finite, non-collapsed, scientifically useful capped exploratory continuation. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The line auxiliary hypothesis is partially supported. Adding a low-weight Line Target auxiliary head recovered or improved the connectivity behavior that ABI-182's line-consensus late extension failed to retain, and it did so with better precision and a smaller predicted-positive fraction than ABI-173/ABI-182. The drawback is that ABI-183 did not improve MIT-source overlap or recall, and it remains below ABI-181 on the primary aggregate/source filtered Dice metrics. The result suggests direct line supervision is a better path for connectivity than the conservative line-consensus gate, but it is not by itself an aggregate-overlap improvement at the 12-epoch budget.

The selected checkpoint at the final exploratory epoch is important. Combined with finite training, source-informative metrics, non-degenerate predictions, and the late epoch-12 improvement, ABI-183 is eligible evidence for a bounded late-improving continuation if the campaign prioritizes testing whether the line-auxiliary connectivity gain survives longer optimization. That continuation would be a close continuation, not a new architecture family, and should keep the trusted late-improving budget request path rather than changing Candidate-owned training behavior.

## Decision

Do not promote ABI-183 and do not reinterpret this capped representative result as full-data evidence. Retain ABI-181 as the current primary capped aggregate reference. Do not repeat ABI-183 unchanged at the exploratory budget.

The next useful in-contract direction is a late-improving ABI-183 continuation, preserving the exact architecture and training policy while requesting the reviewed 36-epoch budget, because ABI-183 selected the final exploratory epoch and uniquely combined near-reference filtered Dice with strong connectivity and restrained positive area. If that continuation fails to improve aggregate/source filtered Dice while preserving connectivity, broaden to a different mechanism for combining ABI-181 overlap with direct line supervision rather than further adjusting this exact auxiliary-weight branch. No new Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260902_204128_bba815/outputs/best_metrics.json`
- `run_20260902_204128_bba815/outputs/final_metrics.json`
- `run_20260902_204128_bba815/outputs/metrics.jsonl`
- `run_20260902_204128_bba815/outputs/resource_profile.json`
- `run_20260902_204128_bba815/outputs/model_summary.json`
- `run_20260902_204128_bba815/outputs/prediction_samples/samples.json`
- `run_20260902_204128_bba815/outputs/validation_postprocessing/index.json`
- `run_20260902_204128_bba815/resolved_manifest.yaml`
- `run_20260902_150611_cbbf35/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_234732_bd5917/outputs/best_metrics.json`
- `run_20260901_234732_bd5917/outputs/evaluations/eval_evalreq_abi173_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_175152_51d2d9/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
