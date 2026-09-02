# Full-spectral DeepLabV3+ family-development update: focal-Tversky vs BTD mixer

research-figures: []

## Scope

This note records the bounded representative results for the two DeepLabV3+ family-development continuations submitted after the ABI-044 full-spectral DeepLabV3+ representative scout.

Source Runs:

- ABI-044 baseline family scout: `run_20260813_145951_a64a37`
- ABI-045 focal-Tversky continuation: `run_20260826_120037_b98df4`
- ABI-046 BTD-mixer continuation: `run_20260826_204203_732aee`

All three used provider-approved `abi_16ch` inputs, source-balanced sampling, random mirroring, batch size 4, 12 epochs, constant learning rate 0.0003, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped feasibility results, not full-data promotion evidence.

## Best-validation comparison

| Run | Candidate | Primary change vs ABI-044 | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260813_145951_a64a37` | ABI-044 | baseline full-spectral DeepLabV3+ + `bce_dice` | 12 | 0.1244 | 0.1125 | 0.1522 | 0.1772 | 0.0959 | 0.00196 |
| `run_20260826_120037_b98df4` | ABI-045 | `focal_tversky` loss | 12 | 0.1005 | 0.1287 | 0.0684 | 0.0620 | 0.2657 | 0.01554 |
| `run_20260826_204203_732aee` | ABI-046 | thermal BTD planes + learned channel mixer, `bce_dice` | 12 | 0.2084 | 0.1960 | 0.2411 | 0.2546 | 0.1763 | 0.00251 |

## Interpretation

ABI-045 shows the expected recall-seeking behavior from focal-Tversky, but the trade-off is unfavorable in this raw full-spectral DeepLabV3+ branch: predicted-positive area is much larger than ABI-044, precision falls sharply, and Google filtered Dice regresses. It remains finite and non-degenerate, but does not support repeating the raw full-spectral focal-Tversky branch unchanged.

ABI-046 is the strongest capped Candidate Result so far in the local history by `val/filtered_dice`. The BTD-mixer front end improves aggregate filtered Dice by +0.0839 over ABI-044 and +0.1079 over ABI-045, while maintaining non-collapsed predictions and improving both Dataset Source strata. The final source split remains balanced enough for further family development: Google filtered Dice 0.2411 and MIT filtered Dice 0.1960.

The BTD-mixer trajectory is also healthier than a one-off spike. It recovers from all-negative epoch 1 to 0.036 at epoch 2, 0.169 at epoch 6, 0.199 at epoch 10, and 0.208 at epoch 12. The result is still below the canonical MCAST 2.1 full-validation baseline context (filtered Dice 0.3873), and the evidence remains capped, so this should guide continued research rather than promotion.

## Decision

Continue the full-spectral DeepLabV3+ family with ABI-046 as the new capped family baseline. Do not continue the raw ABI-045 focal-Tversky branch unchanged.

Recommended next hypothesis: test a controlled BTD-mixer continuation that changes only the trusted primary loss from `bce_dice` to `focal_tversky`. The purpose would be to learn whether ABI-046's spectral front end can preserve its precision/source-balance advantage while recovering part of ABI-045's recall gain.

## Artifact references

- `run_20260813_145951_a64a37/outputs/best_metrics.json`
- `run_20260826_120037_b98df4/outputs/best_metrics.json`
- `run_20260826_204203_732aee/outputs/best_metrics.json`
- `run_20260826_204203_732aee/outputs/resource_profile.json`
- `run_20260826_204203_732aee/outputs/prediction_samples/samples.json`
