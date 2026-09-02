# Full-spectral BTD frequency-gated line U-Net no-augmentation follow-up

research-figures: []

## Scope

This note records ABI-087 after Run `run_20260829_193824_241e30` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-078 BCE-Dice loss-swap conservative-operating-point reference: `run_20260828_094949_ad2af0`
- ABI-081 no-auxiliary focal-Tversky continuation: `run_20260829_143707_7c7d44`
- ABI-085 low-learning-rate continuation: `run_20260829_181201_01c5e7`
- ABI-087 no-augmentation focal-Tversky continuation: `run_20260829_193824_241e30`

ABI-087 used provider-approved `abi_16ch` input only, ABI-channel-derived thermal brightness-temperature-difference features, combined source-balanced sampling, trusted `none` augmentation, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, trusted `focal_tversky` primary loss, and a provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. The controlled change from ABI-068 was disabling trusted `random_mirroring` while holding architecture, loss, sampling, learning rate, and auxiliary supervision fixed. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-development evidence rather than full-data promotion evidence.

## ABI-087 implementation and resource observation

ABI-087 stayed inside the Candidate Experiment Contract. Candidate code owned only the model architecture over provider-approved ABI tensors. It did not introduce candidate-owned data loading, sampling, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, pretrained weights, or longitude/latitude inputs.

Model summary reported 12,087,561 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 2,674.0 seconds wall time, 9,539,944,448 bytes peak CUDA reserved, and no terminal execution failure. Resource behavior is therefore comparable to the ABI-068/085 frequency-gated line U-Net envelope.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, `focal_tversky`, random mirroring, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | same family, `bce_dice_cldice`, random mirroring, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_094949_ad2af0` | ABI-078 | same architecture/aux weight, `bce_dice` | 11 | 0.3816 | 0.3704 | 0.4093 | 0.4072 | 0.3590 | 0.3061 | 0.00320 |
| `run_20260829_143707_7c7d44` | ABI-081 | same architecture/loss, no auxiliary head | 9 | 0.3809 | 0.3624 | 0.4279 | 0.3797 | 0.3822 | 0.3893 | 0.00365 |
| `run_20260829_181201_01c5e7` | ABI-085 | same architecture/loss/aux, lower learning rate 0.0001 | 12 | 0.3826 | 0.3733 | 0.4059 | 0.3693 | 0.3968 | 0.3698 | 0.00389 |
| `run_20260829_193824_241e30` | ABI-087 | same architecture/loss/aux, augmentation policy `none` | 11 | 0.3704 | 0.3701 | 0.3710 | 0.3158 | 0.4478 | 0.2479 | 0.00514 |

ABI-087 completed finite and non-degenerate, and both Dataset Sources stayed above the proposal's approximate 0.33 filtered-Dice floor. It did not meet the stronger useful-continuation criteria. Relative to ABI-068, aggregate filtered Dice fell by about -0.0260, MIT filtered Dice by about -0.0185, Google filtered Dice by about -0.0451, precision by about -0.0833, and connectivity by about -0.1421. Recall increased by about +0.0541, but this came with a higher filtered predicted-positive fraction, 0.00514 versus ABI-068's 0.00357.

The source-specific Dice values were more numerically balanced than ABI-068, but the balance came mainly from a large Google degradation rather than a useful MIT improvement. Compared with ABI-066/078/081/085, ABI-087 was lower on aggregate filtered Dice and much weaker on the precision/connectivity axes that motivated the no-augmentation hypothesis.

## ABI-087 trajectory

Filtered Dice by epoch was 0.1983, 0.2745, 0.3098, 0.2508, 0.3532, 0.3091, 0.3314, 0.3701, 0.3636, 0.2987, 0.3704, and 0.3647. The selected checkpoint was epoch 11. The final epoch 12 retained a similar aggregate operating point, with filtered Dice 0.3647, precision 0.3330, recall 0.4030, connectivity 0.2736, and filtered predicted-positive fraction 0.00439.

The trajectory was finite but oscillatory. Disabling mirroring did not produce a cleaner or more stable late-training curve than ABI-068/085. Its best checkpoint was recall-heavy, with a larger predicted-positive burden and lower line connectivity, suggesting that trusted random mirroring was not the source of ABI-068's remaining precision/connectivity limitation.

The retained fixed first-four prediction samples all had near-zero sample Dice in `outputs/prediction_samples/samples.json`. Because prediction retention is fixed `first_n`, these are bounded artifacts and not representative qualitative evidence; aggregate and source-stratified validation metrics carry this decision.

## Interpretation

Classify ABI-087 as negative capped family-development evidence, not an execution failure. It establishes that the no-augmentation variant is contract-compliant and resource-feasible, but it underperformed the random-mirroring ABI-068 reference on aggregate filtered Dice, both source-specific Dice values, precision, connectivity, and predicted-positive discipline. The only clear gain was recall, and that gain appears tied to broader overprediction rather than improved thin-line discrimination.

This argues for keeping trusted `random_mirroring` as the default for this frequency-gated line U-Net family under the current representative-cap setting. It does not eliminate the family: ABI-068 remains the strongest local capped candidate by primary filtered Dice, ABI-066 remains the precision/connectivity-forward reference, and ABI-078/081/085 remain nearby alternatives that did not surpass ABI-068.

Canonical MCAST 2.1 remains the promotion context, and all comparisons here are capped representative family-development evidence rather than full-data promotion claims.

## Decision

Do not promote ABI-087. Do not repeat the exact no-augmentation branch unchanged. A whole-validation Evaluation Request for ABI-087 is not the next priority because the capped result did not improve ABI-068 and did not provide a secondary-metric advantage.

Future work should broaden beyond disabling augmentation. A useful next hypothesis should preserve ABI-068's aggregate-Dice strength while addressing precision/connectivity and predicted-positive burden through a materially different in-contract architecture or another trusted data/training-policy axis, without moving thresholding, Artifact Filters, data loading, sampling, augmentation implementation, target derivation, losses, metrics, resource placement, or lifecycle behavior into Candidate code.

## Artifact references

- `run_20260829_193824_241e30/outputs/best_metrics.json`
- `run_20260829_193824_241e30/outputs/final_metrics.json`
- `run_20260829_193824_241e30/outputs/metrics.jsonl`
- `run_20260829_193824_241e30/outputs/resource_profile.json`
- `run_20260829_193824_241e30/outputs/model_summary.json`
- `run_20260829_193824_241e30/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260828_094949_ad2af0/outputs/best_metrics.json`
- `run_20260829_143707_7c7d44/outputs/best_metrics.json`
- `run_20260829_181201_01c5e7/outputs/best_metrics.json`
