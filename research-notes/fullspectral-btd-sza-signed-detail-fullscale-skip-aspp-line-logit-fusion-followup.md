# Full-spectral BTD+SZA signed-detail full-scale skip ASPP line-logit fusion follow-up

research-figures: []

## Scope

This note records ABI-188 after Run `run_20260903_031950_88e745` completed.

Source Runs:

- ABI-188 signed-detail full-scale skip ASPP with detached Line/Centerline logit fusion into the primary mask logits: `run_20260903_031950_88e745`
- ABI-184 late36 Line plus Centerline auxiliary precision/connectivity reference: `run_20260902_213856_2c04ac`; whole-validation Evaluation `eval_evalreq_abi184_wholeval_failure_buckets_v1`
- ABI-183 exploratory Line plus Centerline auxiliary parent: `run_20260902_204128_bba815`
- ABI-181 signed-detail full-scale skip ASPP late36 aggregate reference: `run_20260902_150611_cbbf35`; whole-validation Evaluation `eval_evalreq_abi181_wholeval_failure_buckets_v1`
- ABI-185 shared recall-bridge negative reference: `run_20260903_002344_daa8ef`
- ABI-186 mask-sidecar negative reference: `run_20260903_012452_9e35a4`
- ABI-187 focal-Tversky Line plus Centerline recall-expansion reference: `run_20260903_022247_88e0dc`
- ABI-068 frequency-gated line U-Net focal-Tversky source-balance comparator: `run_20260828_010836_4ccc77`

ABI-188 was a close family-development continuation of the ABI-183/184 signed-detail full-scale skip ASPP Line plus Centerline branch. It retained provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD features derived only from approved ABI channels, Solar Geometry Input, signed local/mid-scale detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, line-aware final refinement, BCE-Dice primary loss, provider-derived Line Target auxiliary supervision at weight 0.01, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The intended research change from ABI-183/184 was adding a bounded positive residual from detached `line_logits` and `centerline_logits` into `mask_logits`, without Candidate-owned thresholding or postprocessing.

## Contract and resource observation

ABI-188 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary outputs `line_logits` and `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 9,838,851 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed under the exploratory budget on the A100 at batch size 4 with 2,872.1 seconds total wall time, 1,523.4 seconds training wall time, 1,346.7 seconds validation wall time, 16.13 training samples per second, 18.25 validation samples per second, 9,041,055,744 bytes peak CUDA allocated, and 10,506,731,520 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 12, the final exploratory epoch.

## Best-validation comparison

| Run | Candidate | Best epoch | Filtered Dice | Raw Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260903_031950_88e745` | ABI-188 detached line-logit fusion | 12 | 0.4013 | 0.4160 | 0.3898 | 0.4317 | 0.4250 | 0.3801 | 0.3903 | 0.00324 |
| `run_20260902_213856_2c04ac` | ABI-184 line+centerline late36 | 23 | 0.4066 | 0.4227 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.00261 |
| `run_20260902_204128_bba815` | ABI-183 line+centerline exploratory parent | 12 | 0.3966 | 0.4119 | 0.3805 | 0.4389 | 0.4468 | 0.3565 | 0.4546 | 0.00289 |
| `run_20260902_150611_cbbf35` | ABI-181 centerline-only late36 | 22 | 0.4104 | 0.4254 | 0.3962 | 0.4486 | 0.4423 | 0.3828 | 0.3639 | 0.00314 |
| `run_20260903_002344_daa8ef` | ABI-185 shared recall bridge | 12 | 0.3927 | 0.4080 | 0.3810 | 0.4228 | 0.4511 | 0.3477 | 0.3433 | 0.00279 |
| `run_20260903_012452_9e35a4` | ABI-186 mask sidecar | 12 | 0.3779 | 0.3934 | 0.3641 | 0.4131 | 0.4645 | 0.3185 | 0.3642 | 0.00248 |
| `run_20260903_022247_88e0dc` | ABI-187 focal-Tversky line+centerline | 12 | 0.3897 | 0.4033 | 0.3830 | 0.4068 | 0.3785 | 0.4017 | 0.2197 | 0.00385 |
| `run_20260828_010836_4ccc77` | ABI-068 frequency-gated line U-Net focal-Tversky | 12 | 0.3964 | 0.4100 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |

ABI-188 partially achieved the intended calibration effect. Relative to ABI-183, the detached auxiliary-logit residual improved aggregate filtered Dice by 0.0047, MIT filtered Dice by 0.0093, and filtered recall by 0.0236. It also produced a strong raw Dice of 0.4160 and became the top terminal `val/dice` entry in `ml-autoresearch-agent get-best-runs` at observation time. However, the v0 primary checkpoint metric is filtered Dice, and ABI-188's selected filtered Dice remains below ABI-181 and ABI-184. The recall/MIT gain over ABI-183 came with lower precision, lower Google filtered Dice, lower connectivity, and a larger filtered predicted-positive fraction.

Relative to ABI-184, ABI-188 improved MIT filtered Dice by 0.0019 and recall by 0.0301, but lost 0.0053 aggregate filtered Dice, 0.0238 Google filtered Dice, 0.0600 precision, 0.0731 connectivity, and increased filtered predicted-positive fraction from 0.00261 to 0.00324. This is a better recall bridge than ABI-185/186 and a much better line-connectivity preservation point than ABI-187 focal-Tversky, but it does not preserve the ABI-184 precision/connectivity operating point. Relative to ABI-181, ABI-188 has slightly higher connectivity and slightly larger positive area, but lower primary/source Dice, precision, and recall.

## Exploratory trajectory

ABI-188 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was:

`0.2098, 0.2865, 0.2776, 0.3372, 0.3551, 0.3156, 0.3348, 0.3519, 0.3756, 0.3641, 0.3631, 0.4013`.

The final epoch was the selected checkpoint. At epoch 12, raw Dice was 0.4160, filtered Dice was 0.4013, filtered precision was 0.4250, filtered recall was 0.3801, filtered connectivity was 0.3903, and filtered predicted-positive fraction was 0.00324. Source-stratified filtered Dice was 0.3898 for MIT and 0.4317 for Google. MIT had filtered precision 0.4259, recall 0.3593, connectivity 0.3759, and predicted-positive fraction 0.00456; Google had filtered precision 0.4229, recall 0.4409, connectivity 0.4047, and predicted-positive fraction 0.00193.

Raw-to-filtered differences were modest: raw Dice 0.4160 versus filtered Dice 0.4013, raw recall 0.4072 versus filtered recall 0.3801, and raw predicted-positive fraction 0.00347 versus filtered predicted-positive fraction 0.00324. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples include two empty/negative perfect cases and two near-zero per-sample Dice cases under the `first_n` retention policy; they are traceability samples and should not be treated as representative qualitative evidence for the validation distribution.

The epoch-12 best checkpoint is genuine late-improving evidence for this exact mechanism: filtered Dice jumped from 0.3631 at epoch 11 to 0.4013 at epoch 12 while remaining finite and source-informative. Unlike ABI-185/186, the late jump brought the branch above ABI-183 on aggregate filtered Dice and MIT recall. Unlike ABI-187, it did not buy recall by destroying connectivity entirely. The trajectory is still noisy and capped, so it is not promotion evidence.

## Interpretation

Classify ABI-188 as a completed, finite, non-collapsed, scientifically mixed-to-positive capped exploratory continuation. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The detached line-logit fusion hypothesis is partially supported. It is the best local attempt so far at softening the ABI-184 conservative fixed-threshold mask without perturbing the line heads as severely as the shared ABI-185 bridge or the ABI-187 focal-Tversky loss switch. It improved the ABI-183 exploratory parent on the primary filtered metric, MIT source metric, and recall, and it retained a connectivity level comparable to ABI-068 and above ABI-181/185/186/187. The negative signal is that the mechanism still erodes the strongest ABI-184 properties: precision, Google overlap, positive-area discipline, and line connectivity.

Because ABI-188's capped primary filtered Dice is below the whole-validation-tested ABI-181 aggregate reference and the ABI-184 precision/connectivity reference, it should not be promoted or treated as a new best Result on the v0 primary metric. Its value is as a late-improving calibration branch that may warrant a bounded late36 continuation before whole-validation diagnostics, not as a full-data claim.

## Decision

Do not promote ABI-188 and do not reinterpret this capped representative result as full-data evidence. Retain ABI-181 as the current whole-validation-tested aggregate filtered-Dice reference. Retain ABI-184 as the current whole-validation-tested precision/connectivity and negative-patch-discipline reference in the signed-detail full-scale skip ASPP family.

Do not repeat ABI-188 unchanged at the exploratory budget. A reasonable next in-contract step is a close late-improving continuation of ABI-188 under the approved `late_improving` budget-request mechanism, because the selected checkpoint is the final exploratory epoch, the trajectory is finite and improving, predictions are non-collapsed, and the branch improved the ABI-183 parent on recall/MIT overlap without the severe connectivity collapse seen in ABI-187. The late36 question should be narrow: can detached auxiliary-logit fusion recover ABI-181/184-level filtered Dice while retaining its MIT recall gain and at least ABI-068-level connectivity, or was the epoch-12 jump representative-subset noise?

If a late36 ABI-188 continuation plateaus below ABI-181/184 or further expands positives, stop this auxiliary-logit-fusion branch and broaden away from additive mask-logit calibration toward a different high-resolution line-aware architecture, data-policy probe, or other provider-allowlisted loss/auxiliary configuration. No new Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260903_031950_88e745/outputs/best_metrics.json`
- `run_20260903_031950_88e745/outputs/final_metrics.json`
- `run_20260903_031950_88e745/outputs/metrics.jsonl`
- `run_20260903_031950_88e745/outputs/resource_profile.json`
- `run_20260903_031950_88e745/outputs/model_summary.json`
- `run_20260903_031950_88e745/outputs/prediction_samples/samples.json`
- `run_20260903_031950_88e745/outputs/validation_postprocessing/index.json`
- `run_20260903_031950_88e745/resolved_manifest.yaml`
- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/evaluations/eval_evalreq_abi184_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_204128_bba815/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260903_002344_daa8ef/outputs/best_metrics.json`
- `run_20260903_012452_9e35a4/outputs/best_metrics.json`
- `run_20260903_022247_88e0dc/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
