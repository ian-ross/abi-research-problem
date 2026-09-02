# Full-spectral BTD high-resolution line U-Net centerline-weight follow-up

research-figures: []

## Scope

This note records ABI-054, the controlled high-resolution line U-Net continuation after ABI-053.

Source Runs:

- ABI-052 DeepLabV3+ BTD + trusted `bce_dice_cldice` + `centerline` auxiliary target weight 0.02: `run_20260827_131644_b76d09`
- ABI-053 full-spectral BTD high-resolution line U-Net + trusted `bce_dice_cldice` + `centerline` auxiliary target weight 0.02: `run_20260827_134629_3ace34`
- ABI-054 full-spectral BTD high-resolution line U-Net + trusted `bce_dice_cldice` + `centerline` auxiliary target weight 0.05: `run_20260827_142319_ec8c29`

All Runs used provider-approved `abi_16ch` inputs, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped feasibility results, not full-data promotion evidence.

## ABI-054 implementation and resource observation

ABI-054 kept the ABI-053 model family and input path: normalized approved ABI channels 1-16, explicit thermal BTD planes derived only from approved ABI channels, a learned 1x1 channel mixer, the high-resolution line U-Net decoder, trusted `bce_dice_cldice`, and a provider-derived `centerline` auxiliary output. The controlled change was increasing the manifest-declared `centerline` auxiliary loss weight from 0.02 to 0.05.

The Run completed finite and non-degenerate. Model summary reported 13,618,114 parameters, within the 25,000,000-parameter smoke ceiling. Resource profile reported batch size 4, A100 execution, 1,703.5 seconds wall time, 3.90 GB peak CUDA allocated, 4.49 GB peak CUDA reserved, and completed status.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_131644_b76d09` | ABI-052 | DeepLabV3+ BTD + centerline aux weight 0.02 | 12 | 0.2214 | 0.2083 | 0.2542 | 0.2619 | 0.1918 | 0.3391 | 0.00265 |
| `run_20260827_134629_3ace34` | ABI-053 | high-resolution line U-Net + centerline aux weight 0.02 | 9 | 0.3221 | 0.3119 | 0.3467 | 0.3005 | 0.3472 | 0.2347 | 0.00419 |
| `run_20260827_142319_ec8c29` | ABI-054 | high-resolution line U-Net + centerline aux weight 0.05 | 12 | 0.3160 | 0.2952 | 0.3676 | 0.3329 | 0.3006 | 0.2046 | 0.00327 |

## Final-epoch comparison

| Run | Final epoch filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_134629_3ace34` | 0.3152 | 0.2922 | 0.3697 | 0.3226 | 0.3081 | 0.3019 | 0.00346 |
| `run_20260827_142319_ec8c29` | 0.3160 | 0.2952 | 0.3676 | 0.3329 | 0.3006 | 0.2046 | 0.00327 |

ABI-054's best and final checkpoints were both epoch 12 because the primary filtered Dice peaked at the final epoch.

## ABI-054 trajectory

ABI-054 improved steadily after the initial epochs rather than showing the ABI-053 mid-run peak-and-dip pattern. Filtered Dice rose from 0.0859 at epoch 1 to 0.2189 at epoch 5, 0.2597 at epoch 6, 0.2857 at epoch 8, 0.2974 at epoch 9, and 0.3160 at epoch 12. Validation loss also declined to its best value at epoch 12.

The final checkpoint is source-informative and non-collapsed: MIT filtered Dice 0.2952, Google filtered Dice 0.3676, filtered precision 0.3329, filtered recall 0.3006, and filtered predicted-positive fraction 0.00327. The fixed first-four prediction samples again have near-zero sample Dice values, so they should not be treated as representative qualitative evidence.

## Interpretation

Increasing the centerline auxiliary weight from 0.02 to 0.05 did not achieve the intended connectivity recovery. ABI-054 filtered connectivity was 0.2046, below ABI-053's best-checkpoint 0.2347 and well below ABI-053's final-epoch 0.3019. It also reduced recall relative to ABI-053 best by about 0.0466 and reduced MIT filtered Dice by about 0.0167.

The result is still useful rather than failed. ABI-054 finished at its best epoch, slightly exceeded ABI-053's final filtered Dice, improved filtered precision relative to both ABI-053 best and final checkpoints, and reached the strongest Google filtered Dice among the best-checkpoint high-resolution line U-Net comparisons. However, by the primary checkpoint metric ABI-053 remains the capped best: ABI-053 best filtered Dice 0.3221 versus ABI-054 0.3160.

The centerline-weight result suggests that simply strengthening the existing auxiliary target regularizes predictions toward fewer/higher-precision positives but does not restore the continuity metric in this decoder. ABI-054's lower predicted-positive fraction and lower recall are consistent with over-regularization rather than a better line-continuity trade-off.

None of these capped Runs should be promoted relative to the canonical MCAST 2.1 full-validation context. Canonical MCAST 2.1 remains the full Working Validation Split reference at filtered Dice 0.3873, while ABI-053/054 are representative capped family-development evidence.

## Decision

Keep ABI-053 as the current capped best by primary `val/filtered_dice`. Treat ABI-054 as a finite, resource-safe, source-informative negative-to-mixed result for the specific centerline auxiliary weight 0.05 branch. Do not repeat this exact weight increase unchanged.

Continue the high-resolution line U-Net family, because ABI-054 did not show collapse, non-finite behavior, resource failure, or source-specific catastrophic failure, and it preserved most of ABI-053's large improvement over the DeepLabV3+ BTD family. The useful signal is that precision and final-epoch stability can be improved, but the desired continuity recovery likely needs an architecture-level change rather than another simple centerline-weight adjustment.

Recommended next hypothesis: prepare one sequential high-resolution line U-Net family-development Candidate that returns to the ABI-053 auxiliary weight 0.02 or keeps auxiliary policy fixed, but changes the architecture-level continuity path. A bounded option is to adjust the full-resolution line refiner or skip-fusion gating to preserve thin connected structures while avoiding the lower-recall over-regularization seen in ABI-054. The target should be to recover ABI-053-like Dice and recall while improving final-epoch connectivity/stability, still under the same provider-owned capped execution policy.

## Artifact references

- `run_20260827_142319_ec8c29/outputs/best_metrics.json`
- `run_20260827_142319_ec8c29/outputs/final_metrics.json`
- `run_20260827_142319_ec8c29/outputs/metrics.jsonl`
- `run_20260827_142319_ec8c29/outputs/resource_profile.json`
- `run_20260827_142319_ec8c29/outputs/model_summary.json`
- `run_20260827_142319_ec8c29/outputs/prediction_samples/samples.json`
- `run_20260827_134629_3ace34/outputs/best_metrics.json`
- `run_20260827_134629_3ace34/outputs/final_metrics.json`
- `run_20260827_131644_b76d09/outputs/best_metrics.json`
