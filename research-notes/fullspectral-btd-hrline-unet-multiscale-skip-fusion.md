# Full-spectral BTD high-resolution line U-Net multi-scale skip-fusion follow-up

research-figures: []

## Scope

This note records ABI-056, the controlled multi-scale skip-fusion continuation after ABI-053, ABI-054, and ABI-055.

Source Runs:

- ABI-053 full-spectral BTD high-resolution line U-Net + trusted `bce_dice_cldice` + `centerline` auxiliary target weight 0.02: `run_20260827_134629_3ace34`
- ABI-054 same high-resolution line U-Net + `centerline` auxiliary target weight 0.05: `run_20260827_142319_ec8c29`
- ABI-055 high-resolution line U-Net with directional continuity refiner + `centerline` auxiliary target weight 0.02: `run_20260827_145929_e61464`
- ABI-056 high-resolution line U-Net with multi-scale skip fusion + `centerline` auxiliary target weight 0.02: `run_20260827_153716_1ac9d4`

All Runs used provider-approved `abi_16ch` inputs, approved thermal BTD features derived only from ABI channels, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped feasibility results, not full-data promotion evidence.

## ABI-056 implementation and resource observation

ABI-056 kept ABI-053's input and trusted training policy: normalized approved ABI channels 1-16, explicit thermal BTD planes, a learned channel mixer, trusted `bce_dice_cldice`, and the provider-derived `centerline` auxiliary target at weight 0.02. The controlled change was adding multi-scale skip fusion before the full-resolution line refiner: half- and quarter-resolution decoder outputs are projected to the full-resolution channel width, upsampled, gated together with the full-resolution stream and stem features, concatenated, and fused through residual convolution blocks.

The Run completed finite and non-degenerate. Model summary reported 14,057,122 parameters, within the 25,000,000-parameter smoke ceiling. Resource profile reported batch size 4, A100 execution, 2,007.9 seconds wall time, 6.27 GB peak CUDA allocated, 7.54 GB peak CUDA reserved, and completed status.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_134629_3ace34` | ABI-053 | high-resolution line U-Net + centerline aux weight 0.02 | 9 | 0.3221 | 0.3119 | 0.3467 | 0.3005 | 0.3472 | 0.2347 | 0.00419 |
| `run_20260827_142319_ec8c29` | ABI-054 | centerline aux weight 0.05 | 12 | 0.3160 | 0.2952 | 0.3676 | 0.3329 | 0.3006 | 0.2046 | 0.00327 |
| `run_20260827_145929_e61464` | ABI-055 | directional continuity refiner | 11 | 0.3152 | 0.3155 | 0.3148 | 0.3143 | 0.3162 | 0.2147 | 0.00365 |
| `run_20260827_153716_1ac9d4` | ABI-056 | multi-scale skip fusion | 11 | 0.3225 | 0.3108 | 0.3492 | 0.3310 | 0.3144 | 0.2245 | 0.00344 |

## Final-epoch comparison

| Run | Final epoch filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_134629_3ace34` | 0.3152 | 0.2922 | 0.3697 | 0.3226 | 0.3081 | 0.3019 | 0.00346 |
| `run_20260827_142319_ec8c29` | 0.3160 | 0.2952 | 0.3676 | 0.3329 | 0.3006 | 0.2046 | 0.00327 |
| `run_20260827_145929_e61464` | 0.2910 | 0.2844 | 0.3045 | 0.2723 | 0.3126 | 0.1266 | 0.00416 |
| `run_20260827_153716_1ac9d4` | 0.3221 | 0.3102 | 0.3482 | 0.2982 | 0.3502 | 0.2147 | 0.00426 |

## ABI-056 trajectory

ABI-056 improved from filtered Dice 0.0693 at epoch 1 to 0.2363 at epoch 4, 0.2761 at epoch 6, 0.2991 at epoch 8, 0.3141 at epoch 9, and its best 0.3225 at epoch 11. The final epoch essentially tied the best checkpoint at 0.3221, with a larger predicted-positive fraction and recall: filtered recall rose from 0.3144 at epoch 11 to 0.3502 at epoch 12 while precision fell from 0.3310 to 0.2982.

The best checkpoint is non-collapsed and source-informative: MIT filtered Dice 0.3108, Google filtered Dice 0.3492, filtered precision 0.3310, filtered recall 0.3144, and filtered predicted-positive fraction 0.00344. The fixed first-four prediction samples again have near-zero sample Dice values, so they should not be treated as representative qualitative evidence.

## Interpretation

ABI-056 is a small positive result for the multi-scale skip-fusion branch by the capped primary metric. Its best filtered Dice, 0.3225, is a marginal new capped local best over ABI-053's 0.3221, and its final epoch, 0.3221, removes the ABI-053 best-to-final drop. That supports the intended stability part of the hypothesis.

The effect is not a broad continuity breakthrough. ABI-056 best connectivity, 0.2245, remains below ABI-053 best, 0.2347, and below ABI-053 final, 0.3019. ABI-056 trades ABI-053's higher best-checkpoint recall for higher precision at nearly identical aggregate Dice; its final epoch recovers ABI-053-like recall but loses precision. Source behavior is acceptable but not clearly improved: MIT best Dice is essentially tied/slightly below ABI-053, while Google best Dice is slightly above ABI-053 and below ABI-054.

Canonical MCAST 2.1 remains the full Working Validation Split reference at filtered Dice 0.3873. ABI-056 is representative capped family-development evidence only and should not be interpreted as full-data promotion evidence.

## Decision

Treat ABI-056 as the current local capped best by primary `val/filtered_dice`, but only by a very small margin over ABI-053. The multi-scale skip-fusion idea is useful for late-epoch stability and preserves the high-resolution line U-Net family trajectory, but it does not solve filtered connectivity.

Do not claim promotion from this capped result. A reasonable next handoff in a later Autonomy Step is a bounded Evaluation Request for whole-validation failure analysis of ABI-056, if the Harness policy supports it, to test whether the tiny capped advantage and final-epoch stability survive beyond the representative cap. If another Candidate is required instead, avoid repeating centerline-weight, directional-refiner, or the same skip-fusion change unchanged; broaden toward a different connectivity mechanism or another architecture family.

## Artifact references

- `run_20260827_153716_1ac9d4/outputs/best_metrics.json`
- `run_20260827_153716_1ac9d4/outputs/final_metrics.json`
- `run_20260827_153716_1ac9d4/outputs/metrics.jsonl`
- `run_20260827_153716_1ac9d4/outputs/resource_profile.json`
- `run_20260827_153716_1ac9d4/outputs/model_summary.json`
- `run_20260827_153716_1ac9d4/outputs/prediction_samples/samples.json`
- `run_20260827_134629_3ace34/outputs/best_metrics.json`
- `run_20260827_134629_3ace34/outputs/final_metrics.json`
- `run_20260827_142319_ec8c29/outputs/best_metrics.json`
- `run_20260827_142319_ec8c29/outputs/final_metrics.json`
- `run_20260827_145929_e61464/outputs/best_metrics.json`
- `run_20260827_145929_e61464/outputs/final_metrics.json`
