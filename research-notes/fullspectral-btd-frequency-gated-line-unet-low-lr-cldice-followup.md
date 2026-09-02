# Full-spectral BTD frequency-gated line U-Net low-learning-rate clDice follow-up

research-figures: []

## Scope

This note records ABI-091 after Run `run_20260829_231700_96b245` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-078 frequency-gated line U-Net BCE-Dice reference: `run_20260828_094949_ad2af0`
- ABI-085 frequency-gated line U-Net low-learning-rate focal-Tversky reference: `run_20260829_181201_01c5e7`
- ABI-091 low-learning-rate clDice continuation: `run_20260829_231700_96b245`

ABI-091 used provider-approved `abi_16ch` input only, ABI-channel-derived thermal brightness-temperature-difference features, combined source-balanced sampling, trusted `random_mirroring`, batch size 4, constant learning rate 0.0001, 12 epochs, disabled early stopping, trusted `bce_dice_cldice` primary loss, and a provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. The controlled change from ABI-066 was lowering the learning rate from 0.0003 to 0.0001 while preserving the same frequency-gated line U-Net architecture and loss/auxiliary branch. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-development evidence rather than full-data promotion evidence.

## ABI-091 implementation and resource observation

ABI-091 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI tensors and BTD planes derived from approved ABI channels. It did not introduce candidate-owned data loading, sampling, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, pretrained weights, or longitude/latitude inputs.

Model summary reported 12,087,561 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 2,883.4 seconds wall time, 9,734,979,584 bytes peak CUDA reserved, and no terminal execution failure. Resource behavior stayed within the current 3,600-second Docker training timeout, though it was slower than the recent ABI-085/089/090 runs.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, `focal_tversky`, random mirroring, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | same architecture, `bce_dice_cldice`, learning rate 0.0003 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260829_181201_01c5e7` | ABI-085 | ABI-068 architecture/loss/aux, learning rate 0.0001 | 12 | 0.3826 | 0.3733 | 0.4059 | 0.3693 | 0.3968 | 0.3698 | 0.00389 |
| `run_20260828_094949_ad2af0` | ABI-078 | ABI-068 architecture, `bce_dice`, centerline aux weight 0.02 | 11 | 0.3816 | 0.3704 | 0.4093 | 0.4072 | 0.3590 | 0.3061 | 0.00320 |
| `run_20260829_231700_96b245` | ABI-091 | ABI-066 architecture/loss/aux, learning rate 0.0001 | 12 | 0.3679 | 0.3613 | 0.3835 | 0.3872 | 0.3505 | 0.3085 | 0.00328 |

ABI-091 did not meet its primary local target. Relative to ABI-066, aggregate filtered Dice fell by about -0.0146, Google filtered Dice by about -0.0456, filtered precision by about -0.0555, filtered connectivity by about -0.1646, and filtered predicted-positive fraction increased from 0.00276 to 0.00328. MIT filtered Dice was nearly preserved (-0.0025) and recall increased by about +0.0137, but these gains were not the intended precision/connectivity-forward effect.

Relative to ABI-068, ABI-091 lost aggregate filtered Dice (-0.0285), both source Dice values, precision, recall, and connectivity. Relative to ABI-085, the same low-learning-rate policy under the focal-Tversky branch remained stronger on aggregate Dice, both source Dice values, recall, and connectivity, while ABI-091 recovered only precision (+0.0178) and lower positive-area burden. Relative to ABI-078's BCE-Dice branch, ABI-091 was also lower on aggregate and source Dice and did not add a connectivity advantage.

## ABI-091 trajectory

Filtered Dice by epoch was 0.1634, 0.2725, 0.2840, 0.2959, 0.3216, 0.3305, 0.3487, 0.3309, 0.3617, 0.3490, 0.3531, and 0.3679. The selected checkpoint was epoch 12. The trajectory was finite, non-degenerate, and late-improving, with both Dataset Sources above the proposal's 0.33 floor at the selected epoch (MIT 0.3613; Google 0.3835).

The issue is not optimization collapse. Instead, lowering the learning rate moved the clDice branch toward a smoother but less distinctive operating point: recall improved slightly over ABI-066, but precision and the Contrail Connectivity Metric fell sharply, and the positive-pixel burden increased. The final epoch was the best checkpoint, so the branch might still have improved with more epochs, but the current Workspace Configuration caps training at 12 epochs and the low-learning-rate change did not provide enough benefit under that budget.

The retained fixed first-four prediction samples included one empty/empty perfect sample and three near-zero Dice samples in `outputs/prediction_samples/samples.json`. Because prediction retention is fixed `first_n`, these are bounded artifacts and not representative qualitative evidence; aggregate and source-stratified validation metrics carry this decision.

## Interpretation

Classify ABI-091 as a finite, resource-feasible, source-balanced but negative capped family-development result for the exact low-learning-rate `bce_dice_cldice` branch. It passes the non-finite/non-degenerate and source-catastrophe checks, but it fails the proposal's useful-continuation criterion because it is more than about 0.01 below ABI-066 aggregate filtered Dice and does not improve ABI-066 precision, connectivity, or positive-area discipline.

This result does not eliminate the whole frequency-gated line U-Net family. ABI-068 remains the best capped aggregate-Dice reference, ABI-066 remains the precision/connectivity-forward reference, and ABI-085 remains the stronger low-learning-rate result under focal-Tversky. It does argue against treating lower learning rate as the next local fix for the clDice branch under the current 12-epoch constant-LR budget.

Canonical MCAST 2.1 remains the promotion context, and all comparisons here are capped representative family-development evidence unless an explicitly requested whole-validation diagnostic is run.

## Decision

Do not promote ABI-091. Do not repeat the exact ABI-066 architecture plus `bce_dice_cldice` plus learning rate 0.0001 branch unchanged. Do not request whole-validation failure-bucket diagnostics for ABI-091 ahead of stronger references, because it did not improve aggregate Dice or secondary precision/connectivity behavior over ABI-066/068/085 and did not supply a unique failure mode.

Future work should avoid another small local learning-rate or post-decoder tweak on the same branch unless paired with a clearly different trusted policy axis. A useful next hypothesis should broaden the frontier, for example by testing a materially different architecture family or a provider-approved training/data/loss axis that directly targets the remaining precision-connectivity tradeoff while keeping thresholding, Artifact Filters, data loading, sampling, augmentation implementation, target derivation, losses, metrics, resource placement, and lifecycle behavior out of Candidate code.

## Artifact references

- `run_20260829_231700_96b245/outputs/best_metrics.json`
- `run_20260829_231700_96b245/outputs/final_metrics.json`
- `run_20260829_231700_96b245/outputs/metrics.jsonl`
- `run_20260829_231700_96b245/outputs/resource_profile.json`
- `run_20260829_231700_96b245/outputs/model_summary.json`
- `run_20260829_231700_96b245/outputs/prediction_samples/samples.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260829_181201_01c5e7/outputs/best_metrics.json`
- `run_20260828_094949_ad2af0/outputs/best_metrics.json`
