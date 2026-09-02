# Full-spectral DeepLabV3+ BTD follow-up: focal-Tversky, clDice, and Line Target auxiliary

research-figures: []

## Scope

This note records the bounded representative results for the three DeepLabV3+ BTD-mixer family-development continuations submitted after ABI-046 became the capped family baseline.

Source Runs:

- ABI-046 BTD-mixer family baseline: `run_20260826_204203_732aee`
- ABI-047 BTD-mixer + trusted `focal_tversky`: `run_20260827_110027_1c679a`
- ABI-048 BTD-mixer + trusted `bce_dice_cldice`: `run_20260827_112338_82a3a6`
- ABI-049 BTD-mixer + trusted `bce_dice_cldice` + low-weight trusted `line` auxiliary target: `run_20260827_114945_e5f83e`

All four Runs used provider-approved `abi_16ch` inputs, combined source-balanced sampling, random mirroring, batch size 4, 12 epochs, constant learning rate 0.0003, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped feasibility results, not full-data promotion evidence.

## Best-validation comparison

| Run | Candidate | Primary change vs ABI-046 | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260826_204203_732aee` | ABI-046 | BTD mixer + `bce_dice` | 12 | 0.2084 | 0.1960 | 0.2411 | 0.2546 | 0.1763 | 0.3839 | 0.00251 |
| `run_20260827_110027_1c679a` | ABI-047 | `focal_tversky` primary loss | 12 | 0.1970 | 0.1945 | 0.2024 | 0.1744 | 0.2264 | 0.2419 | 0.00471 |
| `run_20260827_112338_82a3a6` | ABI-048 | `bce_dice_cldice` primary loss | 10 | 0.2169 | 0.2179 | 0.2150 | 0.1963 | 0.2424 | 0.2607 | 0.00447 |
| `run_20260827_114945_e5f83e` | ABI-049 | `bce_dice_cldice` + `line` aux weight 0.05 | 11 | 0.2192 | 0.2189 | 0.2200 | 0.1845 | 0.2701 | 0.2152 | 0.00531 |

## Final-epoch comparison

| Run | Final epoch filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260826_204203_732aee` | 0.2084 | 0.1960 | 0.2411 | 0.2546 | 0.1763 | 0.3839 | 0.00251 |
| `run_20260827_110027_1c679a` | 0.1970 | 0.1945 | 0.2024 | 0.1744 | 0.2264 | 0.2419 | 0.00471 |
| `run_20260827_112338_82a3a6` | 0.2097 | 0.1949 | 0.2484 | 0.2941 | 0.1629 | 0.4245 | 0.00201 |
| `run_20260827_114945_e5f83e` | 0.2102 | 0.1967 | 0.2447 | 0.2873 | 0.1657 | 0.3841 | 0.00209 |

## Interpretation

ABI-047 confirms that focal-Tversky remains a recall-seeking branch even after the BTD mixer is added. Compared with ABI-046, recall rises from 0.1763 to 0.2264, but precision drops from 0.2546 to 0.1744 and aggregate filtered Dice falls from 0.2084 to 0.1970. The branch is finite, non-collapsed, and much healthier than raw full-spectral focal-Tversky ABI-045 on Google, but it does not improve the BTD family baseline.

ABI-048 is the strongest clean primary-loss continuation. It improves best filtered Dice to 0.2169 and gives the best final-epoch connectivity and precision among the follow-ups. Its best epoch is source-balanced, with MIT 0.2179 and Google 0.2150, while the final epoch shifts back toward higher precision and stronger Google Dice. This suggests the continuity-aware primary loss is useful, but the optimum may be sensitive to checkpoint timing within the 12-epoch capped budget.

ABI-049 is a small best-validation improvement over ABI-048: filtered Dice rises from 0.2169 to 0.2192, source scores remain nearly balanced at the selected checkpoint, and filtered recall increases from 0.2424 to 0.2701. The cost is lower precision and lower filtered connectivity at the best checkpoint. By final epoch, ABI-049 and ABI-048 converge to similar aggregate Dice near 0.210, with ABI-049 slightly lower than ABI-048 on final Google Dice and connectivity. The low-weight Line Target auxiliary head is therefore useful as recall-bias evidence, but the gain is modest rather than a decisive new family baseline.

No run shows hard execution failure, non-finite behavior, persistent prediction collapse, or source-catastrophic failure. The BTD-mixer DeepLabV3+ family remains extension-eligible under capped-evidence policy, but none of these Runs should be treated as promotion-grade relative to the canonical MCAST 2.1 full-validation context.

## Decision

Use ABI-049 as the current capped best by `val/filtered_dice`, while treating ABI-048 and ABI-046 as important trade-off references: ABI-048 for precision/connectivity behavior under `bce_dice_cldice`, and ABI-046 for a simpler high-precision BTD baseline.

Do not repeat the exact ABI-047 focal-Tversky branch unchanged. Do not over-interpret the ABI-049 margin over ABI-048; it is a small capped best-checkpoint gain paired with weaker connectivity.

Recommended next hypothesis: continue the BTD-mixer DeepLabV3+ family with a controlled auxiliary-target variant that aims to regain boundary precision without abandoning the recall benefit seen from `bce_dice_cldice`. The safest next in-contract probe is a BTD-mixer `bce_dice_cldice` model with the trusted `boundary` auxiliary target at the same low auxiliary weight used by ABI-049, comparing directly against ABI-048 and ABI-049. If that also trades connectivity away, broaden to an architecture-frontier scout rather than adding more auxiliary heads to the same decoder.

## Artifact references

- `run_20260826_204203_732aee/outputs/best_metrics.json`
- `run_20260827_110027_1c679a/outputs/best_metrics.json`
- `run_20260827_112338_82a3a6/outputs/best_metrics.json`
- `run_20260827_114945_e5f83e/outputs/best_metrics.json`
- `run_20260827_114945_e5f83e/outputs/final_metrics.json`
- `run_20260827_114945_e5f83e/outputs/resource_profile.json`
- `run_20260827_114945_e5f83e/outputs/prediction_samples/samples.json`
