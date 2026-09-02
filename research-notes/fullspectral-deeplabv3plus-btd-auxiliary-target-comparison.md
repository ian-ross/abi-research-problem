# Full-spectral DeepLabV3+ BTD auxiliary-target comparison: boundary vs centerline

research-figures: []

## Scope

This note records the bounded representative results for the two DeepLabV3+ BTD-mixer auxiliary-target continuations completed after the ABI-048/049 clDice and Line Target comparison.

Source Runs:

- ABI-046 BTD-mixer family baseline: `run_20260826_204203_732aee`
- ABI-048 BTD-mixer + trusted `bce_dice_cldice`: `run_20260827_112338_82a3a6`
- ABI-049 BTD-mixer + trusted `bce_dice_cldice` + low-weight trusted `line` auxiliary target: `run_20260827_114945_e5f83e`
- ABI-050 BTD-mixer + trusted `bce_dice_cldice` + low-weight trusted `boundary` auxiliary target: `run_20260827_122019_18b5c7`
- ABI-051 BTD-mixer + trusted `bce_dice_cldice` + low-weight trusted `centerline` auxiliary target: `run_20260827_124640_fc6836`

All Runs used provider-approved `abi_16ch` inputs, combined source-balanced sampling, random mirroring, batch size 4, 12 epochs, constant learning rate 0.0003, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped feasibility results, not full-data promotion evidence.

## Best-validation comparison

| Run | Candidate | Primary change vs ABI-048 | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260826_204203_732aee` | ABI-046 | BTD mixer + `bce_dice` | 12 | 0.2084 | 0.1960 | 0.2411 | 0.2546 | 0.1763 | 0.3839 | 0.00251 |
| `run_20260827_112338_82a3a6` | ABI-048 | `bce_dice_cldice` primary loss | 10 | 0.2169 | 0.2179 | 0.2150 | 0.1963 | 0.2424 | 0.2607 | 0.00447 |
| `run_20260827_114945_e5f83e` | ABI-049 | `bce_dice_cldice` + `line` aux weight 0.05 | 11 | 0.2192 | 0.2189 | 0.2200 | 0.1845 | 0.2701 | 0.2152 | 0.00531 |
| `run_20260827_122019_18b5c7` | ABI-050 | `bce_dice_cldice` + `boundary` aux weight 0.05 | 12 | 0.2084 | 0.1964 | 0.2343 | 0.2391 | 0.1846 | 0.2591 | 0.00280 |
| `run_20260827_124640_fc6836` | ABI-051 | `bce_dice_cldice` + `centerline` aux weight 0.05 | 10 | 0.2187 | 0.2104 | 0.2382 | 0.2392 | 0.2015 | 0.3176 | 0.00305 |

## Final-epoch comparison

| Run | Final epoch filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260826_204203_732aee` | 0.2084 | 0.1960 | 0.2411 | 0.2546 | 0.1763 | 0.3839 | 0.00251 |
| `run_20260827_112338_82a3a6` | 0.2097 | 0.1949 | 0.2484 | 0.2941 | 0.1629 | 0.4245 | 0.00201 |
| `run_20260827_114945_e5f83e` | 0.2102 | 0.1967 | 0.2447 | 0.2873 | 0.1657 | 0.3841 | 0.00209 |
| `run_20260827_122019_18b5c7` | 0.2084 | 0.1964 | 0.2343 | 0.2391 | 0.1846 | 0.2591 | 0.00280 |
| `run_20260827_124640_fc6836` | 0.2168 | 0.2012 | 0.2540 | 0.2824 | 0.1759 | 0.3388 | 0.00226 |

## Interpretation

ABI-050 shows that the low-weight Boundary Target auxiliary is not a useful aggregate improvement for this branch. It finishes at 0.2084 filtered Dice, essentially back at the ABI-046 BCE-Dice BTD-mixer baseline and below ABI-048/049. It is not a hard failure: training remained finite and non-degenerate, Google filtered Dice stayed relatively strong at 0.2343, and precision was higher than the high-recall Line Target branch. The weakness is MIT and aggregate lift, not execution reliability.

ABI-051 is the more useful auxiliary-target result. Its best checkpoint nearly ties ABI-049 by filtered Dice (0.2187 vs 0.2192) while improving filtered precision (0.2392 vs 0.1845), filtered connectivity (0.3176 vs 0.2152), and Google filtered Dice (0.2382 vs 0.2200). The trade-off is lower recall than ABI-049 and weaker MIT filtered Dice than the line-aux best checkpoint. At the final epoch, ABI-051 is the strongest member of this set by filtered Dice (0.2168) and Google filtered Dice (0.2540), suggesting better late-epoch stability than ABI-048/049 even though primary checkpoint selection still leaves ABI-049 as the capped best by `val/filtered_dice`.

The auxiliary-target axis therefore appears diagnostically useful but not decisive. Line auxiliary supervision pushes recall and best-checkpoint aggregate Dice, boundary auxiliary supervision does not improve the branch, and centerline auxiliary supervision gives a better precision/connectivity/stability compromise. None of these capped Runs should be promoted relative to the canonical MCAST 2.1 full-validation context, and none shows hard execution failure, non-finite behavior, persistent prediction collapse, or source-catastrophic failure.

## Decision

Keep ABI-049 as the current capped best by best-validation `val/filtered_dice`, but treat ABI-051 as the preferred trade-off reference for auxiliary-target development because it nearly ties ABI-049 while improving precision, connectivity, final-epoch Dice, and Google source behavior.

Do not repeat the exact ABI-050 boundary-auxiliary branch unchanged. Do not claim promotion from any of these capped Runs. The BTD-mixer DeepLabV3+ family remains extension-eligible, but the 0.05 auxiliary-weight variants show diminishing aggregate returns.

Recommended next hypothesis: run one controlled ABI-051 weight-tuning continuation with the same BTD-mixer DeepLabV3+ `bce_dice_cldice` model and trusted `centerline` auxiliary target, lowering only the auxiliary weight from 0.05 to 0.02. The aim is to test whether the centerline signal can retain ABI-051's precision/connectivity and final-epoch stability while reducing the recall suppression and MIT weakness seen at weight 0.05. If that does not produce a clearer trade-off than ABI-048/049/051, broaden the frontier to a materially different thin-structure architecture scout rather than adding more auxiliary heads to this decoder.

## Artifact references

- `run_20260826_204203_732aee/outputs/best_metrics.json`
- `run_20260827_112338_82a3a6/outputs/best_metrics.json`
- `run_20260827_114945_e5f83e/outputs/best_metrics.json`
- `run_20260827_122019_18b5c7/outputs/best_metrics.json`
- `run_20260827_122019_18b5c7/outputs/final_metrics.json`
- `run_20260827_124640_fc6836/outputs/best_metrics.json`
- `run_20260827_124640_fc6836/outputs/final_metrics.json`
- `run_20260827_124640_fc6836/outputs/resource_profile.json`
- `run_20260827_124640_fc6836/outputs/prediction_samples/samples.json`
