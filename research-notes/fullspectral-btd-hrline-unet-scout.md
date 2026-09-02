# Full-spectral BTD high-resolution line U-Net scout

research-figures: []

## Scope

This note records ABI-053, the first materially different thin-structure decoder scout after the full-spectral DeepLabV3+ BTD-mixer auxiliary-target sequence.

Source Runs:

- ABI-046 BTD-mixer DeepLabV3+ family baseline: `run_20260826_204203_732aee`
- ABI-048 BTD-mixer DeepLabV3+ + trusted `bce_dice_cldice`: `run_20260827_112338_82a3a6`
- ABI-049 BTD-mixer DeepLabV3+ + trusted `bce_dice_cldice` + `line` auxiliary target weight 0.05: `run_20260827_114945_e5f83e`
- ABI-051 BTD-mixer DeepLabV3+ + trusted `bce_dice_cldice` + `centerline` auxiliary target weight 0.05: `run_20260827_124640_fc6836`
- ABI-052 BTD-mixer DeepLabV3+ + trusted `bce_dice_cldice` + `centerline` auxiliary target weight 0.02: `run_20260827_131644_b76d09`
- ABI-053 full-spectral BTD high-resolution line U-Net + trusted `bce_dice_cldice` + `centerline` auxiliary target weight 0.02: `run_20260827_134629_3ace34`

All Runs used provider-approved `abi_16ch` inputs, combined source-balanced sampling, random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped feasibility results, not full-data promotion evidence.

## ABI-053 implementation and resource observation

ABI-053 preserved the ABI-052 input/loss policy: normalized approved ABI channels 1-16, explicit thermal BTD planes derived only from approved channels, a learned channel mixer, trusted `bce_dice_cldice`, and a trusted low-weight `centerline` auxiliary target. It replaced the DeepLabV3+ decoder with a pure-PyTorch high-resolution U-Net-style decoder with a full-resolution stem path, gated skip fusion, coarsest-scale dilated context, and a final full-resolution multi-dilation line refiner.

The Run completed finite and non-degenerate. Model summary reported 13,618,114 parameters, within the 25,000,000-parameter smoke ceiling. Resource profile reported batch size 4, A100 execution, 1,735.8 seconds wall time, 3.90 GB peak CUDA allocated, 4.49 GB peak CUDA reserved, and completed status.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260826_204203_732aee` | ABI-046 | BTD DeepLabV3+ + `bce_dice` | 12 | 0.2084 | 0.1960 | 0.2411 | 0.2546 | 0.1763 | 0.3839 | 0.00251 |
| `run_20260827_112338_82a3a6` | ABI-048 | DeepLabV3+ + `bce_dice_cldice` | 10 | 0.2169 | 0.2179 | 0.2150 | 0.1963 | 0.2424 | 0.2607 | 0.00447 |
| `run_20260827_114945_e5f83e` | ABI-049 | DeepLabV3+ + `line` aux weight 0.05 | 11 | 0.2192 | 0.2189 | 0.2200 | 0.1845 | 0.2701 | 0.2152 | 0.00531 |
| `run_20260827_124640_fc6836` | ABI-051 | DeepLabV3+ + `centerline` aux weight 0.05 | 10 | 0.2187 | 0.2104 | 0.2382 | 0.2392 | 0.2015 | 0.3176 | 0.00305 |
| `run_20260827_131644_b76d09` | ABI-052 | DeepLabV3+ + `centerline` aux weight 0.02 | 12 | 0.2214 | 0.2083 | 0.2542 | 0.2619 | 0.1918 | 0.3391 | 0.00265 |
| `run_20260827_134629_3ace34` | ABI-053 | high-resolution line U-Net decoder | 9 | 0.3221 | 0.3119 | 0.3467 | 0.3005 | 0.3472 | 0.2347 | 0.00419 |

## Final-epoch comparison

| Run | Final epoch filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260826_204203_732aee` | 0.2084 | 0.1960 | 0.2411 | 0.2546 | 0.1763 | 0.3839 | 0.00251 |
| `run_20260827_112338_82a3a6` | 0.2097 | 0.1949 | 0.2484 | 0.2941 | 0.1629 | 0.4245 | 0.00201 |
| `run_20260827_114945_e5f83e` | 0.2102 | 0.1967 | 0.2447 | 0.2873 | 0.1657 | 0.3841 | 0.00209 |
| `run_20260827_124640_fc6836` | 0.2168 | 0.2012 | 0.2540 | 0.2824 | 0.1759 | 0.3388 | 0.00226 |
| `run_20260827_131644_b76d09` | 0.2214 | 0.2083 | 0.2542 | 0.2619 | 0.1918 | 0.3391 | 0.00265 |
| `run_20260827_134629_3ace34` | 0.3152 | 0.2922 | 0.3697 | 0.3226 | 0.3081 | 0.3019 | 0.00346 |

## ABI-053 trajectory

ABI-053 improved rapidly after the initial epochs. Filtered Dice rose from 0.0918 at epoch 1 to 0.2519 at epoch 4, 0.2920 at epoch 6, and 0.3221 at epoch 9. Epoch 10 dipped to 0.2383, then the Run recovered to 0.2871 at epoch 11 and 0.3152 at epoch 12. Final validation loss was lower than the best-Dice checkpoint validation loss, so the Dice fluctuation is not a simple optimization divergence signal.

The best checkpoint is source-informative and non-collapsed: MIT filtered Dice 0.3119, Google filtered Dice 0.3467, filtered precision 0.3005, filtered recall 0.3472, and filtered predicted-positive fraction 0.00419. The final checkpoint retained most of the aggregate gain and improved filtered precision to 0.3226, final Google filtered Dice to 0.3697, and filtered connectivity to 0.3019, at the cost of lower recall and lower MIT filtered Dice than the best checkpoint.

## Interpretation

ABI-053 is a large capped improvement over the prior ABI-052 DeepLabV3+ BTD centerline-weight reference. Best filtered Dice improved by +0.1007, MIT filtered Dice by +0.1036, Google filtered Dice by +0.0925, precision by +0.0386, and recall by +0.1554. This directly addresses the previous note's concern that DeepLabV3+ auxiliary-head tuning was no longer the highest-value path and that decoder/feature geometry might be limiting MIT behavior and recall.

The result is not a promotion result. It used the representative cap, while canonical MCAST 2.1 remains the full Working Validation Split context at filtered Dice 0.3873. However, the capped ABI-053 best checkpoint is now the strongest local Candidate Result by a wide margin and is close enough to the MCAST context to merit focused family development rather than returning to DeepLabV3+ auxiliary-head tuning.

The main trade-off is continuity. ABI-053's best-checkpoint filtered connectivity 0.2347 is below ABI-052's 0.3391 and below the final-epoch DeepLabV3+ precision/connectivity references. The final ABI-053 checkpoint partially recovers connectivity to 0.3019 while retaining filtered Dice 0.3152 and achieving the strongest Google filtered Dice in the local history. This suggests the high-resolution decoder is beneficial, but its checkpoint selection may favor higher-recall masks before the best continuity/precision balance is reached.

The fixed first-four prediction samples are not representative diagnostics here: all four sample Dice values are near zero despite strong aggregate validation metrics, so qualitative or per-sample conclusions should not be drawn from that retained first_n subset alone.

## Decision

Treat ABI-053 as the current capped best by `val/filtered_dice` and as an extension-positive scout for the high-resolution line U-Net family. Do not claim full-data promotion. Do not eliminate the family for the observed connectivity trade-off; it is finite, resource-safe, non-degenerate, strongly source-informative, and materially better than the mature DeepLabV3+ BTD branch under the same cap.

Retain ABI-052 and ABI-048 as precision/connectivity trade-off references, ABI-049 as the high-recall DeepLabV3+ auxiliary reference, and ABI-053 as the new architecture-family baseline.

Recommended next hypothesis: run one sequential controlled ABI-053 family-development continuation that keeps the high-resolution line U-Net, BTD front end, trusted `bce_dice_cldice`, source-balanced sampling, random mirroring, and capped execution policy unchanged, but increases the trusted `centerline` auxiliary weight from 0.02 to 0.05. The aim is to test whether stronger provider-derived centerline supervision can recover ABI-052-like connectivity and final-epoch stability while preserving most of ABI-053's large Dice, MIT, Google, and recall gains. If that follow-up sacrifices too much recall or aggregate Dice, the next branch should focus on architecture-level continuity refinement rather than returning to DeepLabV3+ auxiliary-head tuning.

## Artifact references

- `run_20260827_134629_3ace34/outputs/best_metrics.json`
- `run_20260827_134629_3ace34/outputs/final_metrics.json`
- `run_20260827_134629_3ace34/outputs/metrics.jsonl`
- `run_20260827_134629_3ace34/outputs/resource_profile.json`
- `run_20260827_134629_3ace34/outputs/model_summary.json`
- `run_20260827_134629_3ace34/outputs/prediction_samples/samples.json`
- `run_20260827_131644_b76d09/outputs/best_metrics.json`
- `run_20260827_131644_b76d09/outputs/final_metrics.json`
- `run_20260827_124640_fc6836/outputs/best_metrics.json`
- `run_20260827_112338_82a3a6/outputs/best_metrics.json`
- `run_20260827_114945_e5f83e/outputs/best_metrics.json`
- `run_20260826_204203_732aee/outputs/best_metrics.json`
