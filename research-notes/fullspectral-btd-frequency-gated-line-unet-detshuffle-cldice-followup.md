# Full-spectral BTD frequency-gated line U-Net deterministic-shuffle clDice follow-up

research-figures: []

## Scope

This note records ABI-100 after Run `run_20260830_055047_fb5c2f` completed.

Source Runs:

- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-078 frequency-gated line U-Net BCE-Dice reference: `run_20260828_094949_ad2af0`
- ABI-085 frequency-gated line U-Net lower-learning-rate focal-Tversky reference: `run_20260829_181201_01c5e7`
- ABI-091 frequency-gated line U-Net lower-learning-rate clDice reference: `run_20260829_231700_96b245`
- ABI-096 deterministic-shuffle focal-Tversky reference: `run_20260830_021504_c112f8`
- ABI-100 deterministic-shuffle clDice continuation: `run_20260830_055047_fb5c2f`

ABI-100 preserved the ABI-066 full-spectral BTD frequency-gated line U-Net architecture, provider-approved `abi_16ch` input, ABI-channel-derived thermal brightness-temperature-difference features, trusted `bce_dice_cldice` primary loss, trusted `random_mirroring`, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, and provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. The controlled change from ABI-066 was manifest-selected trusted sampling traversal: `deterministic_shuffle` instead of `combined_source_balanced`. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped data-policy/family-development evidence rather than full-data promotion evidence.

## ABI-100 implementation and resource observation

ABI-100 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI tensors and BTD planes derived from approved ABI channels. It did not introduce candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.

Model summary reported 12,087,561 parameters against the 25,000,000-parameter smoke ceiling. The model summary confirmed GOES ABI channels 1-16 only, with forbidden longitude/latitude source channels excluded, and outputs `mask_logits` plus `centerline_logits`. The Run completed at batch size 4 on the A100 with 2,849.3 seconds total wall time, 1,440.8 seconds training wall time, 1,406.4 seconds validation wall time, 9,734,979,584 bytes peak CUDA reserved, and no terminal execution failure. Resource behavior remained within the current 3,600-second Docker training timeout and matched the profiled frequency-gated line U-Net resource envelope.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, `focal_tversky`, combined source-balanced | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, combined source-balanced | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_094949_ad2af0` | ABI-078 | ABI-068 branch, `bce_dice` | 11 | 0.3816 | 0.3704 | 0.4093 | 0.4072 | 0.3590 | 0.3061 | 0.00320 |
| `run_20260829_181201_01c5e7` | ABI-085 | ABI-068 branch, low LR `focal_tversky` | 12 | 0.3826 | 0.3733 | 0.4059 | 0.3693 | 0.3968 | 0.3698 | 0.00389 |
| `run_20260829_231700_96b245` | ABI-091 | ABI-066 branch, low LR `bce_dice_cldice` | 12 | 0.3679 | 0.3613 | 0.3835 | 0.3872 | 0.3505 | 0.3085 | 0.00328 |
| `run_20260830_021504_c112f8` | ABI-096 | ABI-068 branch, `deterministic_shuffle` | 10 | 0.3628 | 0.3472 | 0.4024 | 0.4242 | 0.3169 | 0.4195 | 0.00271 |
| `run_20260830_055047_fb5c2f` | ABI-100 | ABI-066 branch, `deterministic_shuffle` | 10 | 0.3674 | 0.3508 | 0.4089 | 0.4321 | 0.3195 | 0.4411 | 0.00268 |

ABI-100 produced a conservative, precision/connectivity-forward operating point, but it did not meet the local bar set by ABI-066. Relative to ABI-066, aggregate filtered Dice fell by about -0.0152, MIT filtered Dice by -0.0130, Google filtered Dice by -0.0203, filtered precision by -0.0106, filtered recall by -0.0173, and filtered connectivity by -0.0320. The only favorable movement was a very small reduction in filtered predicted-positive fraction from 0.00276 to 0.00268, which is not enough to offset the lower overlap, source, and connectivity metrics.

Relative to ABI-096, ABI-100 shows that deterministic shuffle is less damaging on the clDice branch than on the focal-Tversky branch: aggregate filtered Dice improved by about +0.0046, MIT by +0.0036, Google by +0.0065, precision by +0.0080, recall by +0.0025, connectivity by +0.0215, and predicted-positive fraction stayed essentially unchanged. Relative to ABI-091, ABI-100 traded recall and MIT Dice for materially better Google Dice, precision, connectivity, and lower predicted-positive burden. However, the aggregate result remained essentially tied with ABI-091 and still below ABI-066/078/085/068.

## ABI-100 trajectory

ABI-100 trained finitely and avoided all-negative/all-positive collapse, but its validation trajectory was oscillatory. Filtered Dice by epoch was 0.2627, 0.3065, 0.3094, 0.3355, 0.2554, 0.3347, 0.3121, 0.3368, 0.3549, 0.3674, 0.3587, and 0.3614. The selected checkpoint was epoch 10 rather than the final epoch.

The selected checkpoint had filtered precision 0.4321, filtered recall 0.3195, filtered connectivity 0.4411, filtered predicted-positive fraction 0.00268, MIT filtered Dice 0.3508, and Google filtered Dice 0.4089. The final checkpoint shifted toward a recall-heavy, positive-area-expanded profile: filtered precision 0.3069, recall 0.4397, connectivity 0.3072, filtered predicted-positive fraction 0.00519, MIT filtered Dice 0.3545, and Google filtered Dice 0.3778. This late shift is milder than ABI-096's final-epoch deterioration but still argues against deterministic shuffle as a stabilizing replacement for combined source-balanced traversal under the current 12-epoch constant-LR budget.

Raw-to-filtered differences were modest at the final epoch: raw Dice 0.3718 versus filtered Dice 0.3614, and raw predicted-positive fraction 0.00553 versus filtered 0.00519. The result is therefore not a case where provider-owned Artifact Filters rescued a poor raw prediction into a misleading capped score. The fixed first-four retained prediction samples all had near-zero per-sample Dice in `outputs/prediction_samples/samples.json`; because prediction retention is fixed `first_n`, these are bounded artifacts and not representative qualitative evidence.

## Interpretation

Classify ABI-100 as finite, resource-feasible, non-collapsed, and diagnostically useful but negative capped family-development evidence for the exact deterministic-shuffle `bce_dice_cldice` branch. It partially preserved the clDice branch's intended conservative positive-area discipline and gave the strongest deterministic-shuffle precision/connectivity profile seen so far, but it failed the useful-continuation criterion relative to ABI-066. The combined source-balanced ABI-066 branch remains stronger on aggregate filtered Dice, both Dataset Sources, filtered precision, filtered recall, and Contrail Connectivity Metric.

The paired ABI-096 and ABI-100 results suggest that deterministic shuffle can reduce positive-area burden but does not improve the current frequency-gated family enough to justify replacing source-balanced traversal. The source-balanced policy remains important for preserving the best observed combination of MIT/Google balance, overlap, and line continuity. This does not eliminate the frequency-gated line U-Net family; ABI-068 remains the local capped aggregate-Dice reference, ABI-066 remains the precision/connectivity reference, and ABI-078/085 remain stronger capped comparator branches than ABI-100.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-100 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-100. Do not repeat the exact ABI-066 architecture plus `bce_dice_cldice` plus centerline auxiliary branch with `deterministic_shuffle` unchanged. Retain `combined_source_balanced` as the preferred traversal for this frequency-gated line U-Net family unless a materially different trusted data-policy hypothesis is introduced.

Do not request whole-validation failure-bucket diagnostics for ABI-100 ahead of stronger frequency-gated references. The result is close enough to ABI-091/096 to be informative about sampling-policy behavior, but it does not beat ABI-066 on the precision/connectivity branch and does not beat ABI-068 on aggregate Dice. A useful next hypothesis should broaden away from small local sampling, learning-rate, and additive gate tweaks and toward a different contract-compliant mechanism for threshold discipline or source-robust line continuity. Candidate code should continue to leave thresholding, Artifact Filters, data loading, sampling implementation, augmentation implementation, target derivation, losses, metrics, resource placement, and lifecycle behavior to the provider/Harness.

## Artifact references

- `run_20260830_055047_fb5c2f/outputs/best_metrics.json`
- `run_20260830_055047_fb5c2f/outputs/final_metrics.json`
- `run_20260830_055047_fb5c2f/outputs/metrics.jsonl`
- `run_20260830_055047_fb5c2f/outputs/resource_profile.json`
- `run_20260830_055047_fb5c2f/outputs/model_summary.json`
- `run_20260830_055047_fb5c2f/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260828_094949_ad2af0/outputs/best_metrics.json`
- `run_20260829_181201_01c5e7/outputs/best_metrics.json`
- `run_20260829_231700_96b245/outputs/best_metrics.json`
- `run_20260830_021504_c112f8/outputs/best_metrics.json`
