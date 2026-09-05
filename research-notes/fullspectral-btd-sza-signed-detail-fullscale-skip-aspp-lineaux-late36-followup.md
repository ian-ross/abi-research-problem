# Full-spectral BTD+SZA signed-detail full-scale skip ASPP line-aux late36 follow-up

research-figures: []

## Scope

This note records ABI-184 after late-improving Run `run_20260902_213856_2c04ac` completed.

Source Runs:

- ABI-184 signed-detail full-scale skip ASPP with Line plus Centerline auxiliary supervision and late36 budget: `run_20260902_213856_2c04ac`
- ABI-183 exploratory parent with the same Line plus Centerline auxiliary branch: `run_20260902_204128_bba815`
- ABI-181 signed-detail full-scale skip ASPP late36 aggregate reference: `run_20260902_150611_cbbf35`; whole-validation Evaluation `eval_evalreq_abi181_wholeval_failure_buckets_v1`
- ABI-182 signed-detail line-consensus late36 comparator: `run_20260902_175152_51d2d9`
- ABI-173 signed-detail full-scale skip ASPP 12-epoch parent family reference: `run_20260901_234732_bd5917`; whole-validation Evaluation `eval_evalreq_abi173_wholeval_failure_buckets_v1`
- ABI-154 full-scale skip ASPP/detail decoder precision-connectivity reference: `run_20260901_071026_32d3ec`
- ABI-068 frequency-gated line U-Net focal-Tversky source-balance comparator: `run_20260828_010836_4ccc77`

ABI-184 was a close family-development continuation of ABI-183. It retained provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD features derived only from approved ABI channels, Solar Geometry Input, signed local/mid-scale detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, line-aware final refinement, BCE-Dice primary loss, provider-derived Line Target auxiliary supervision at weight 0.01, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The intended research change from ABI-183 was only the Harness-reviewed `late_improving` budget request for 36 effective epochs.

## Contract and resource observation

ABI-184 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary outputs `line_logits` and `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 9,838,851 parameters, below the 25,000,000-parameter smoke ceiling. The late-improving request was approved (`budget_class_effective: late_improving`, `effective_max_epochs: 36`). The Run completed on the A100 at batch size 4 with 8,634.9 seconds total wall time, 4,566.8 seconds training wall time, 4,065.7 seconds validation wall time, 16.14 training samples per second, 18.13 validation samples per second, 9,041,055,744 bytes peak CUDA allocated, and 10,508,828,672 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 23.

## Best-validation comparison

| Run | Candidate | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260902_213856_2c04ac` | ABI-184 line+centerline late36 | 23 | 0.4066 | 0.3879 | 0.4555 | 0.4850 | 0.3500 | 0.4634 | 0.00261 |
| `run_20260902_204128_bba815` | ABI-183 line+centerline exploratory parent | 12 | 0.3966 | 0.3805 | 0.4389 | 0.4468 | 0.3565 | 0.4546 | 0.00289 |
| `run_20260902_150611_cbbf35` | ABI-181 centerline-only late36 aggregate reference | 22 | 0.4104 | 0.3962 | 0.4486 | 0.4423 | 0.3828 | 0.3639 | 0.00314 |
| `run_20260902_175152_51d2d9` | ABI-182 line-consensus late36 | 32 | 0.4035 | 0.3898 | 0.4362 | 0.4010 | 0.4061 | 0.3365 | 0.00367 |
| `run_20260901_234732_bd5917` | ABI-173 signed-detail full-scale skip ASPP parent | 12 | 0.3962 | 0.3838 | 0.4269 | 0.4238 | 0.3720 | 0.3203 | 0.00318 |
| `run_20260901_071026_32d3ec` | ABI-154 full-scale skip ASPP/detail decoder | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260828_010836_4ccc77` | ABI-068 frequency-gated line U-Net focal-Tversky | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |

ABI-184 positively answers the narrow late-improving parent question: relative to ABI-183, the 36-epoch continuation improved aggregate filtered Dice by 0.0100, MIT filtered Dice by 0.0074, Google filtered Dice by 0.0166, precision by 0.0382, connectivity by 0.0088, and positive-area discipline from 0.00289 to 0.00261 filtered predicted-positive fraction. The tradeoff is lower recall, 0.3500 versus 0.3565.

ABI-184 does not displace ABI-181 on the v0 primary capped aggregate metric: it trails ABI-181 filtered Dice by 0.0039 and MIT filtered Dice by 0.0082. It does, however, exceed ABI-181 on Google filtered Dice, precision, connectivity, and smaller predicted-positive fraction. The connectivity gap is large: 0.4634 for ABI-184 versus 0.3639 for ABI-181. Relative to ABI-182, ABI-184 gives higher aggregate and Google filtered Dice, much higher precision/connectivity, and lower positive-area fraction, but lower recall and slightly lower MIT filtered Dice. These comparisons remain capped representative evidence, not full-data promotion evidence.

## Late-improving trajectory

ABI-184 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was:

`0.1772, 0.2887, 0.2701, 0.3090, 0.3380, 0.3658, 0.3723, 0.3405, 0.3338, 0.3649, 0.3761, 0.3960, 0.3718, 0.3575, 0.3992, 0.3833, 0.3676, 0.3816, 0.3827, 0.3534, 0.3980, 0.4046, 0.4066, 0.3758, 0.3804, 0.3976, 0.3808, 0.3922, 0.3905, 0.3822, 0.3972, 0.4018, 0.3914, 0.3856, 0.3932, 0.3957`.

The selected epoch 23 checkpoint confirms that ABI-183's final exploratory epoch was not the branch's ceiling. The late budget raised the branch above the exploratory parent and produced a better precision/connectivity point without expanding positive area. After epoch 23, the trajectory was noisy and did not find a higher checkpoint; the final epoch retained finite, non-collapsed predictions but declined to filtered Dice 0.3957 with lower connectivity 0.3162 and higher filtered predicted-positive fraction 0.00301. This argues against another unchanged epoch-extension of the same exact branch.

At the selected epoch 23 checkpoint, raw Dice was 0.4227, filtered Dice was 0.4066, filtered precision was 0.4850, filtered recall was 0.3500, filtered connectivity was 0.4634, and filtered predicted-positive fraction was 0.00261. Source-stratified filtered Dice was 0.3879 for MIT and 0.4555 for Google. MIT had filtered precision 0.4821, recall 0.3245, connectivity 0.4448, and predicted-positive fraction 0.00363; Google had filtered precision 0.4916, recall 0.4244, connectivity 0.4819, and predicted-positive fraction 0.00159.

Raw-to-filtered differences were modest: raw Dice 0.4227 versus filtered Dice 0.4066, raw recall 0.3743 versus filtered recall 0.3500, and raw predicted-positive fraction 0.00279 versus filtered predicted-positive fraction 0.00261. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples include three empty/negative perfect cases and one near-zero per-sample Dice case under the `first_n` retention policy; they are traceability samples and should not be treated as representative qualitative evidence for the validation distribution.

## Interpretation

Classify ABI-184 as a completed, finite, non-collapsed, scientifically useful capped late-improving continuation. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The direct Line Target auxiliary hypothesis is strengthened but still mixed. The late-improving budget improved ABI-183 on aggregate/source overlap and preserved or slightly improved the line-connectivity advantage, showing that the line-auxiliary branch was not exhausted at 12 epochs. ABI-184 also provides the strongest precision/connectivity combination in this recent signed-detail ASPP branch. The remaining weakness is recall, especially MIT recall, which keeps aggregate and MIT filtered Dice slightly below ABI-181 despite better Google Dice and much stronger connectivity.

The late36 evidence separates two useful continuation points: ABI-181 remains the current capped aggregate filtered-Dice reference, while ABI-184 is the stronger capped precision/connectivity tradeoff point. Because ABI-181 has already received whole-validation failure-bucket review, ABI-184's next question is not another unchanged training extension but whether its capped connectivity/precision gain survives the full Working Validation Split and whether the recall deficit produces unacceptable whole-validation false negatives.

## Decision

Do not promote ABI-184 and do not reinterpret this capped representative result as full-data evidence. Retain ABI-181 as the current capped aggregate filtered-Dice reference. Retain ABI-184 as the best current capped line-connectivity/precision continuation of the signed-detail full-scale skip ASPP branch and as evidence that low-weight Line Target auxiliary supervision is useful when paired with the late-improving budget.

Do not repeat ABI-184 unchanged and do not request another longer budget for the same exact branch. A reasonable next Autonomy Step is a bounded whole-validation Evaluation Request for `run_20260902_213856_2c04ac` to compare its precision/connectivity/Google gains and MIT/recall deficits against ABI-181, ABI-183, ABI-173, ABI-154, ABI-068, and canonical MCAST context on the full 3,088-sample Working Validation Split. If whole-validation diagnostics confirm that ABI-184 preserves connectivity without severe recall or source failure, use it as the next line-aware calibration/design reference; if diagnostics show missed contrails dominate, broaden to a different in-contract mechanism for combining ABI-181 recall/overlap with direct line supervision rather than another unchanged line-auxiliary epoch extension. No new Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260902_213856_2c04ac/outputs/best_metrics.json`
- `run_20260902_213856_2c04ac/outputs/final_metrics.json`
- `run_20260902_213856_2c04ac/outputs/metrics.jsonl`
- `run_20260902_213856_2c04ac/outputs/resource_profile.json`
- `run_20260902_213856_2c04ac/outputs/model_summary.json`
- `run_20260902_213856_2c04ac/outputs/prediction_samples/samples.json`
- `run_20260902_213856_2c04ac/outputs/validation_postprocessing/index.json`
- `run_20260902_213856_2c04ac/resolved_manifest.yaml`
- `run_20260902_213856_2c04ac/candidate/budget_request.yaml`
- `run_20260902_204128_bba815/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/best_metrics.json`
- `run_20260902_150611_cbbf35/outputs/evaluations/eval_evalreq_abi181_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260902_175152_51d2d9/outputs/best_metrics.json`
- `run_20260901_234732_bd5917/outputs/best_metrics.json`
- `run_20260901_234732_bd5917/outputs/evaluations/eval_evalreq_abi173_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
