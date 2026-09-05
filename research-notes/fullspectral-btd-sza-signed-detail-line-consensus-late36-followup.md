# Full-spectral BTD+SZA signed-detail line-consensus late36 follow-up

research-figures: []

## Scope

This note records ABI-182 after late-improving Run `run_20260902_175152_51d2d9` completed.

Source Runs:

- ABI-182 signed-detail line-consensus full-scale skip ASPP late36 BCE-Dice Centerline-auxiliary continuation: `run_20260902_175152_51d2d9`
- ABI-174 direct parent signed-detail line-consensus 12-epoch Run: `run_20260902_005632_5651ef`
- ABI-181 current signed-detail full-scale skip ASPP late36 aggregate reference: `run_20260902_150611_cbbf35`; whole-validation Evaluation `eval_evalreq_abi181_wholeval_failure_buckets_v1`
- ABI-154 precision/connectivity reference: `run_20260901_071026_32d3ec`
- ABI-068 recall/connectivity and MIT/source-balance comparator: `run_20260828_010836_4ccc77`

ABI-182 was an exact architecture close-continuation of ABI-174. It kept provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized/cosine Solar Geometry Input features, learned spectral projection, signed local/mid-scale positive and negative detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, line-aware refinement, conservative line-consensus calibration, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.

The only intended research change from ABI-174 was the Harness-reviewed late-improving budget request. The request was approved: `budget_class_effective: late_improving`, `effective_max_epochs: 36`, and `effective_training_wall_clock_timeout_seconds: 10800`.

## Contract and resource observation

ABI-182 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 10,078,210 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 9,655.9 seconds total wall time, 5,330.2 seconds training wall time, 4,323.3 seconds validation wall time, 13.83 training samples per second, 17.05 validation samples per second, 11,014,247,936 bytes peak CUDA allocated, and 13,172,211,712 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 32.

## Best-validation comparison

| Run | Candidate | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260902_175152_51d2d9` | ABI-182 signed-detail line-consensus late36 | 32 | 0.4035 | 0.3898 | 0.4362 | 0.4010 | 0.4061 | 0.3365 | 0.00367 |
| `run_20260902_150611_cbbf35` | ABI-181 signed-detail full-scale skip ASPP late36 | 22 | 0.4104 | 0.3962 | 0.4486 | 0.4423 | 0.3828 | 0.3639 | 0.00314 |
| `run_20260902_005632_5651ef` | ABI-174 signed-detail line-consensus parent | 12 | 0.3929 | 0.3833 | 0.4178 | 0.4158 | 0.3724 | 0.3460 | 0.00325 |
| `run_20260901_071026_32d3ec` | ABI-154 full-scale skip ASPP/detail decoder | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260828_010836_4ccc77` | ABI-068 frequency-gated line U-Net focal-Tversky | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |

Relative to ABI-174, the late-improving budget improved capped filtered Dice from 0.3929 to 0.4035, MIT filtered Dice from 0.3833 to 0.3898, Google filtered Dice from 0.4178 to 0.4362, and recall from 0.3724 to 0.4061. The tradeoff was lower precision, 0.4158 to 0.4010; lower connectivity, 0.3460 to 0.3365; and a slightly larger filtered predicted-positive fraction, 0.00325 to 0.00367.

Relative to ABI-181, ABI-182 did not catch the current aggregate reference. It trails ABI-181 in aggregate, MIT, and Google capped filtered Dice, precision, connectivity, and positive-area discipline, while improving recall. The recall gain is useful evidence that the line-consensus branch did not collapse, but it came with the wrong connectivity direction for the proposal's main hypothesis.

Relative to ABI-154, ABI-182 improves aggregate/source capped filtered Dice and recall but remains far below ABI-154 precision and connectivity. Relative to ABI-068, ABI-182 modestly improves aggregate/source Dice and recall, but it trails ABI-068 substantially on connectivity. These are capped representative comparisons only; ABI-182 has not received a whole-validation diagnostic.

## Late-improving trajectory

ABI-182 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was:

`0.2034, 0.2891, 0.3022, 0.3391, 0.2964, 0.3416, 0.3606, 0.3411, 0.3694, 0.3483, 0.3466, 0.3663, 0.3229, 0.3552, 0.3812, 0.3036, 0.3619, 0.3445, 0.3620, 0.4017, 0.3863, 0.3996, 0.3599, 0.3862, 0.3835, 0.3827, 0.3948, 0.3837, 0.3886, 0.3899, 0.4032, 0.4035, 0.3975, 0.3864, 0.3876, 0.3877`.

The extension hypothesis was partly supported: ABI-182 exceeded ABI-174's 12-epoch selected checkpoint and reached its own best checkpoint late, at epoch 32. However, the line-consensus-specific hypothesis was not supported, because the best checkpoint did not preserve ABI-174's connectivity advantage and did not recover ABI-181's aggregate/source Dice or precision. The post-32 trajectory declined, with final filtered Dice 0.3877, MIT filtered Dice 0.3691, Google filtered Dice 0.4334, precision 0.4268, recall 0.3551, connectivity 0.3199, and filtered predicted-positive fraction 0.00302.

At selected epoch 32, raw Dice was 0.4175, filtered Dice was 0.4035, filtered precision was 0.4010, filtered recall was 0.4061, filtered connectivity was 0.3365, and filtered predicted-positive fraction was 0.00367. Source-stratified filtered Dice was 0.3898 for MIT and 0.4362 for Google. MIT had filtered precision 0.4109, recall 0.3708, connectivity 0.3518, and predicted-positive fraction 0.00487; Google had filtered precision 0.3815, recall 0.5091, connectivity 0.3212, and predicted-positive fraction 0.00246.

Raw-to-filtered differences were modest: raw Dice 0.4175 versus filtered Dice 0.4035, raw recall 0.4344 versus filtered recall 0.4061, and raw predicted-positive fraction 0.00392 versus filtered predicted-positive fraction 0.00367. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples include one empty/negative perfect case and three near-zero per-sample Dice cases under the `first_n` retention policy; these are traceability samples and should not be treated as representative qualitative evidence for the full validation distribution.

## Interpretation

Classify ABI-182 as a completed, finite, non-collapsed, scientifically mixed capped late-improving continuation. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The main positive finding is that ABI-174's line-consensus branch was indeed epoch-truncated for aggregate overlap: 36 trusted epochs improved aggregate, MIT, and Google capped filtered Dice and shifted the operating point toward higher recall. The main negative finding is that the extension did not retain the line-consensus branch's intended connectivity benefit. ABI-182's selected checkpoint has lower connectivity than ABI-174, ABI-181, ABI-154, and ABI-068, and its recall gain versus ABI-181 is paired with lower precision and larger predicted-positive area.

Therefore ABI-182 does not replace ABI-181 as the current capped or whole-validation-tested aggregate reference, and it does not justify another unchanged late-epoch repeat of the same line-consensus architecture. The result does not eliminate line-aware calibration as a broad family, but it is a hard stop for this exact ABI-174/ABI-182 line-consensus late-budget branch unless new diagnostics motivate a specific repair.

## Decision

Do not promote ABI-182 and do not reinterpret this capped representative result as full-data evidence. Do not repeat ABI-182 unchanged. A whole-validation Evaluation Request is lower priority than it was for ABI-181: ABI-182 did improve over ABI-174, but it did not meet the proposal's strong criterion of approaching ABI-181 while improving connectivity or MIT/source balance.

Retain ABI-181 as the current aggregate reference. Treat ABI-182 as evidence that simply extending the conservative line-consensus calibration changes the recall/precision operating point but does not solve the connected-line weakness. The next useful in-contract direction should broaden away from this exact line-consensus continuation toward a different mechanism for preserving ABI-181 overlap while improving connectivity or MIT balance, such as a new architecture scout or a controlled loss/auxiliary/data-policy variant under the trusted allowlists. No Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260902_175152_51d2d9/outputs/best_metrics.json`
- `run_20260902_175152_51d2d9/outputs/final_metrics.json`
- `run_20260902_175152_51d2d9/outputs/metrics.jsonl`
- `run_20260902_175152_51d2d9/outputs/resource_profile.json`
- `run_20260902_175152_51d2d9/outputs/model_summary.json`
- `run_20260902_175152_51d2d9/outputs/prediction_samples/samples.json`
- `run_20260902_175152_51d2d9/outputs/validation_postprocessing/index.json`
- `run_20260902_175152_51d2d9/resolved_manifest.yaml`
- `run_20260902_175152_51d2d9/candidate/budget_request.yaml`
- `run_20260902_005632_5651ef/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
