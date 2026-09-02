# Full-spectral DeepLabV3+ BTD centerline auxiliary weight tuning

research-figures: []

## Scope

This note records ABI-052, the lower-weight Centerline Target continuation after ABI-051.

Source Runs:

- ABI-046 BTD-mixer family baseline: `run_20260826_204203_732aee`
- ABI-048 BTD-mixer + trusted `bce_dice_cldice`: `run_20260827_112338_82a3a6`
- ABI-049 BTD-mixer + trusted `bce_dice_cldice` + low-weight trusted `line` auxiliary target: `run_20260827_114945_e5f83e`
- ABI-051 BTD-mixer + trusted `bce_dice_cldice` + trusted `centerline` auxiliary target weight 0.05: `run_20260827_124640_fc6836`
- ABI-052 BTD-mixer + trusted `bce_dice_cldice` + trusted `centerline` auxiliary target weight 0.02: `run_20260827_131644_b76d09`

All Runs used provider-approved `abi_16ch` inputs, combined source-balanced sampling, random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped feasibility results, not full-data promotion evidence.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260826_204203_732aee` | ABI-046 | BTD mixer + `bce_dice` | 12 | 0.2084 | 0.1960 | 0.2411 | 0.2546 | 0.1763 | 0.3839 | 0.00251 |
| `run_20260827_112338_82a3a6` | ABI-048 | `bce_dice_cldice` primary loss | 10 | 0.2169 | 0.2179 | 0.2150 | 0.1963 | 0.2424 | 0.2607 | 0.00447 |
| `run_20260827_114945_e5f83e` | ABI-049 | `bce_dice_cldice` + `line` aux weight 0.05 | 11 | 0.2192 | 0.2189 | 0.2200 | 0.1845 | 0.2701 | 0.2152 | 0.00531 |
| `run_20260827_124640_fc6836` | ABI-051 | `bce_dice_cldice` + `centerline` aux weight 0.05 | 10 | 0.2187 | 0.2104 | 0.2382 | 0.2392 | 0.2015 | 0.3176 | 0.00305 |
| `run_20260827_131644_b76d09` | ABI-052 | `bce_dice_cldice` + `centerline` aux weight 0.02 | 12 | 0.2214 | 0.2083 | 0.2542 | 0.2619 | 0.1918 | 0.3391 | 0.00265 |

## ABI-052 trajectory and resource observations

ABI-052 completed finite and non-degenerate under the trusted envelope. The model stayed within the smoke budget with 12,445,858 parameters. Runtime was 1,320.5 seconds, peak CUDA reservation was 964,689,920 bytes, and no retry or lifecycle issue is visible in the agent-safe Run summary.

The filtered-Dice trajectory was not monotonic but ended at the best checkpoint: epoch 2 reached 0.1080 after an all-negative-like first epoch, epoch 5 reached 0.1661, epoch 8 reached 0.1971, epoch 10 reached 0.2061, and epoch 12 reached 0.2214. The final selected checkpoint has filtered precision 0.2619, recall 0.1918, connectivity 0.3391, and filtered predicted-positive fraction 0.00265.

## Interpretation

Lowering the centerline auxiliary weight from 0.05 to 0.02 produced the best capped `val/filtered_dice` observed so far in this local history: ABI-052 improves ABI-049 by +0.0022 and ABI-051 by +0.0027. The improvement is small, so it should be treated as a useful trade-off refinement rather than a decisive architecture breakthrough.

The trade-off is clearer than ABI-049. ABI-052 gives much higher precision and connectivity than the line-auxiliary branch while retaining enough recall to slightly exceed ABI-049 by filtered Dice. It also improves Google filtered Dice to 0.2542, the strongest Google source score in this DeepLabV3+ BTD set. The cost is MIT filtered Dice: ABI-052 at 0.2083 remains below ABI-048/049 and slightly below ABI-051, so the lower centerline weight did not solve the MIT weakness identified for ABI-051.

Compared with ABI-046, the clDice-plus-centerline direction remains useful: aggregate filtered Dice improves from 0.2084 to 0.2214 and Google improves from 0.2411 to 0.2542. Compared with ABI-048, ABI-052 improves aggregate and Google behavior while recovering precision/connectivity, but it gives up some MIT score and recall. This looks like diminishing but still positive auxiliary-weight tuning evidence, not an elimination signal.

None of these capped Runs should be promoted relative to the canonical MCAST 2.1 full-validation context. Canonical MCAST 2.1 remains far higher at filtered Dice 0.3873 on the 3,088-sample Working Validation Split. The capped DeepLabV3+ evidence remains useful for family development only.

## Decision

Treat ABI-052 as the current capped best by `val/filtered_dice` and as the preferred centerline-auxiliary trade-off reference. Retain ABI-049 as the high-recall auxiliary reference and ABI-048/046 as simpler precision/connectivity references.

Do not repeat ABI-050 or the exact ABI-051 weight 0.05 branch unchanged. Do not claim promotion from ABI-052. The centerline weight 0.02 result is finite, source-informative, and extension-positive, but the small margin and persistent MIT weakness indicate that more auxiliary-head-only tuning is unlikely to be the highest-value next step.

Recommended next hypothesis: broaden the frontier to a materially different thin-structure architecture scout that keeps the successful BTD-mixer input front end and trusted `bce_dice_cldice` policy, but changes the decoder/feature geometry to preserve higher-resolution line evidence more directly. The goal should be to test whether architecture, rather than another low-weight auxiliary-head variant, can improve MIT behavior and recall while retaining ABI-052's precision/connectivity gains. This should remain a sequential capped scout unless a reviewed resource profile exists.

## Artifact references

- `run_20260826_204203_732aee/outputs/best_metrics.json`
- `run_20260827_112338_82a3a6/outputs/best_metrics.json`
- `run_20260827_114945_e5f83e/outputs/best_metrics.json`
- `run_20260827_124640_fc6836/outputs/best_metrics.json`
- `run_20260827_124640_fc6836/outputs/final_metrics.json`
- `run_20260827_131644_b76d09/outputs/best_metrics.json`
- `run_20260827_131644_b76d09/outputs/final_metrics.json`
- `run_20260827_131644_b76d09/outputs/resource_profile.json`
- `run_20260827_131644_b76d09/outputs/model_summary.json`
- `run_20260827_131644_b76d09/outputs/prediction_samples/samples.json`
