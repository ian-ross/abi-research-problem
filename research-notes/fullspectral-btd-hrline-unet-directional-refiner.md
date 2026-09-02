# Full-spectral BTD high-resolution line U-Net directional-refiner follow-up

research-figures: []

## Scope

This note records ABI-055, the controlled architecture-level directional-refiner continuation after ABI-053 and ABI-054.

Source Runs:

- ABI-053 full-spectral BTD high-resolution line U-Net + trusted `bce_dice_cldice` + `centerline` auxiliary target weight 0.02: `run_20260827_134629_3ace34`
- ABI-054 same high-resolution line U-Net + `centerline` auxiliary target weight 0.05: `run_20260827_142319_ec8c29`
- ABI-055 high-resolution line U-Net with directional continuity refiner + `centerline` auxiliary target weight 0.02: `run_20260827_145929_e61464`

All Runs used provider-approved `abi_16ch` inputs, approved thermal BTD features derived only from ABI channels, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped feasibility results, not full-data promotion evidence.

## ABI-055 implementation and resource observation

ABI-055 kept the ABI-053 policy baseline: normalized approved ABI channels 1-16, explicit thermal BTD planes, a learned channel mixer, trusted `bce_dice_cldice`, and the provider-derived `centerline` auxiliary target at weight 0.02. The controlled change was replacing the isotropic full-resolution line refiner with a directional continuity refiner using horizontal and vertical elongated convolution branches and a learned feature-fusion gate.

The Run completed finite and non-degenerate. Model summary reported 13,632,274 parameters, within the 25,000,000-parameter smoke ceiling. Resource profile reported batch size 4, A100 execution, 1,766.1 seconds wall time, 4.30 GB peak CUDA allocated, 4.77 GB peak CUDA reserved, and completed status.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_134629_3ace34` | ABI-053 | high-resolution line U-Net + centerline aux weight 0.02 | 9 | 0.3221 | 0.3119 | 0.3467 | 0.3005 | 0.3472 | 0.2347 | 0.00419 |
| `run_20260827_142319_ec8c29` | ABI-054 | centerline aux weight 0.05 | 12 | 0.3160 | 0.2952 | 0.3676 | 0.3329 | 0.3006 | 0.2046 | 0.00327 |
| `run_20260827_145929_e61464` | ABI-055 | directional continuity refiner | 11 | 0.3152 | 0.3155 | 0.3148 | 0.3143 | 0.3162 | 0.2147 | 0.00365 |

## Final-epoch comparison

| Run | Final epoch filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_134629_3ace34` | 0.3152 | 0.2922 | 0.3697 | 0.3226 | 0.3081 | 0.3019 | 0.00346 |
| `run_20260827_142319_ec8c29` | 0.3160 | 0.2952 | 0.3676 | 0.3329 | 0.3006 | 0.2046 | 0.00327 |
| `run_20260827_145929_e61464` | 0.2910 | 0.2844 | 0.3045 | 0.2723 | 0.3126 | 0.1266 | 0.00416 |

## ABI-055 trajectory

ABI-055 improved from filtered Dice 0.0898 at epoch 1 to 0.2784 at epoch 6, 0.2881 at epoch 8, 0.3151 at epoch 9, and its best 0.3152 at epoch 11. Epoch 10 showed high recall, 0.3874, but lower precision, 0.2467. The final epoch regressed to 0.2910 filtered Dice and 0.1266 filtered connectivity despite retaining non-collapsed predictions.

The best checkpoint is source-balanced and non-degenerate: MIT filtered Dice 0.3155, Google filtered Dice 0.3148, filtered precision 0.3143, filtered recall 0.3162, and filtered predicted-positive fraction 0.00365. This is the most balanced MIT/Google result in the high-resolution line U-Net branch, but it does not improve the primary capped metric over ABI-053.

## Interpretation

The directional refiner did not produce the intended continuity recovery. ABI-055 best filtered connectivity, 0.2147, is slightly above ABI-054's 0.2046 but below ABI-053 best, 0.2347, and well below ABI-053 final, 0.3019. The final checkpoint's connectivity drop to 0.1266 argues against treating the axis-aligned elongated-kernel refiner as a stability improvement.

The result is mixed rather than a hard failure. It stayed finite, resource-safe, non-collapsed, and source-informative. It also improved MIT filtered Dice relative to ABI-053 best by about +0.0036 and substantially reduced the MIT/Google gap. However, it reduced Google filtered Dice by about -0.0319, aggregate filtered Dice by about -0.0069, recall by about -0.0310, and did not beat ABI-054 precision or final-epoch stability.

Canonical MCAST 2.1 remains the full Working Validation Split reference at filtered Dice 0.3873. ABI-053/054/055 remain representative capped family-development evidence only and should not be interpreted as full-data promotion evidence.

## Decision

Keep ABI-053 as the current local capped best by primary `val/filtered_dice`. Treat ABI-055 as a finite, resource-safe, source-informative negative-to-mixed result for this exact directional-refiner branch. Do not repeat the same axis-aligned directional-refiner change unchanged.

Continue the high-resolution line U-Net family rather than abandoning it: ABI-055 did not collapse, and ABI-053/054/055 remain materially stronger than the earlier DeepLabV3+ BTD branch under the same representative cap. The useful signal is that architecture-level changes can shift source balance and precision/recall, but this directional refiner is not the right continuity/stability mechanism.

Recommended next hypothesis: broaden within the same high-resolution family toward skip-fusion or decoder-scale changes instead of another simple centerline-weight or elongated-kernel refiner tweak. A bounded next Candidate could keep ABI-053's loss/input/auxiliary policy fixed and adjust multi-scale skip fusion or decoder capacity to preserve ABI-053-like aggregate Dice and recall while improving final-epoch stability and connectivity.

## Artifact references

- `run_20260827_145929_e61464/outputs/best_metrics.json`
- `run_20260827_145929_e61464/outputs/final_metrics.json`
- `run_20260827_145929_e61464/outputs/metrics.jsonl`
- `run_20260827_145929_e61464/outputs/resource_profile.json`
- `run_20260827_145929_e61464/outputs/model_summary.json`
- `run_20260827_145929_e61464/outputs/prediction_samples/samples.json`
- `run_20260827_134629_3ace34/outputs/best_metrics.json`
- `run_20260827_134629_3ace34/outputs/final_metrics.json`
- `run_20260827_142319_ec8c29/outputs/best_metrics.json`
- `run_20260827_142319_ec8c29/outputs/final_metrics.json`
