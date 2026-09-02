# Full-spectral BTD frequency-gated line U-Net SE-recalibrated follow-up

research-figures: []

## Scope

This note records ABI-088 after Run `run_20260829_203135_e22164` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice and whole-validation reference: `run_20260828_010836_4ccc77`
- ABI-078 BCE-Dice loss-swap conservative-operating-point reference: `run_20260828_094949_ad2af0`
- ABI-081 no-auxiliary focal-Tversky continuation: `run_20260829_143707_7c7d44`
- ABI-085 low-learning-rate focal-Tversky continuation: `run_20260829_181201_01c5e7`
- ABI-087 no-augmentation focal-Tversky continuation: `run_20260829_193824_241e30`
- ABI-088 SE-recalibrated focal-Tversky continuation: `run_20260829_203135_e22164`

ABI-088 used provider-approved `abi_16ch` input only, ABI-channel-derived thermal brightness-temperature-difference features, combined source-balanced sampling, trusted `random_mirroring`, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, trusted `focal_tversky` primary loss, and a provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. The controlled architecture change from ABI-068 was adding lightweight spectral-spatial recalibration inside residual feature blocks. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-development evidence rather than full-data promotion evidence.

## ABI-088 implementation and resource observation

ABI-088 stayed inside the Candidate Experiment Contract. Candidate code owned only the model architecture over provider-approved ABI tensors and ABI-channel-derived BTD planes. It did not introduce candidate-owned data loading, sampling, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, pretrained weights, or longitude/latitude inputs.

Model summary reported 12,240,045 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 2,921.0 seconds wall time, 10,684,989,440 bytes peak CUDA reserved, and no terminal execution failure. Resource behavior remains feasible but somewhat heavier/slower than the ABI-068/085 frequency-gated line U-Net envelope.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, `focal_tversky`, random mirroring, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | same family, `bce_dice_cldice`, random mirroring, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_094949_ad2af0` | ABI-078 | same architecture/aux weight, `bce_dice` | 11 | 0.3816 | 0.3704 | 0.4093 | 0.4072 | 0.3590 | 0.3061 | 0.00320 |
| `run_20260829_143707_7c7d44` | ABI-081 | ABI-068 architecture/loss, no auxiliary head | 9 | 0.3809 | 0.3624 | 0.4279 | 0.3797 | 0.3822 | 0.3893 | 0.00365 |
| `run_20260829_181201_01c5e7` | ABI-085 | ABI-068 architecture/loss/aux, learning rate 0.0001 | 12 | 0.3826 | 0.3733 | 0.4059 | 0.3693 | 0.3968 | 0.3698 | 0.00389 |
| `run_20260829_193824_241e30` | ABI-087 | ABI-068 architecture/loss/aux, augmentation policy `none` | 11 | 0.3704 | 0.3701 | 0.3710 | 0.3158 | 0.4478 | 0.2479 | 0.00514 |
| `run_20260829_203135_e22164` | ABI-088 | distributed spectral-spatial feature recalibration | 9 | 0.3594 | 0.3449 | 0.3948 | 0.3559 | 0.3629 | 0.1464 | 0.00369 |

ABI-088 completed finite and non-degenerate, but it did not meet the proposal's useful-continuation criteria. Relative to ABI-068, aggregate filtered Dice fell by about -0.0370, MIT filtered Dice by about -0.0437, Google filtered Dice by about -0.0213, precision by about -0.0433, recall by about -0.0307, and filtered connectivity by about -0.2436. The filtered predicted-positive fraction was slightly higher than ABI-068, 0.00369 versus 0.00357, so recalibration did not improve positive-area discipline.

Compared with ABI-066, ABI-088 lost aggregate Dice, both source-specific Dice values, precision, recall, connectivity, and positive-area discipline. Compared with ABI-087, ABI-088 recovered some precision and Google-source Dice and reduced the overprediction burden, but it lost recall, MIT-source Dice, aggregate Dice, and especially connectivity. The intended precision/connectivity recovery signal is therefore absent.

## ABI-088 trajectory

Filtered Dice by epoch was 0.2011, 0.2366, 0.2940, 0.2305, 0.3134, 0.2995, 0.3221, 0.3492, 0.3594, 0.3454, 0.3243, and 0.3575. The selected checkpoint was epoch 9. The final epoch 12 nearly recovered the selected aggregate Dice at 0.3575 and had recall 0.4512, but precision fell to 0.2960 and connectivity stayed low at 0.1825.

The trajectory was finite and late-enough improving to avoid treating this as an optimization or execution failure, but it plateaued below the ABI-066/068/078/081/085 band and was persistently weak on connectivity. The best checkpoint was not an all-negative or all-positive collapse, yet the distributed recalibration appears to have disrupted the line-continuity behavior that made ABI-066 and ABI-068 useful family references.

The retained fixed first-four prediction samples all had near-zero sample Dice in `outputs/prediction_samples/samples.json`. Because prediction retention is fixed `first_n`, these are bounded artifacts and not representative qualitative evidence; aggregate and source-stratified validation metrics carry this decision.

## Interpretation

Classify ABI-088 as negative capped family-development evidence, not an execution failure. The SE-recalibrated residual blocks were contract-compliant and resource-feasible, but they underperformed ABI-068 on the primary metric and all intended secondary axes. The large connectivity regression is the clearest scientific signal: recalibrating residual features did not recover ABI-066-like line continuity and did not provide a conservative operating point worth diagnosing with whole-validation failure buckets.

This result does not eliminate the broader frequency-gated line U-Net family. ABI-068 remains the current strongest local capped Candidate by primary filtered Dice, ABI-066 remains the precision/connectivity-forward reference, and ABI-078/081/085 remain nearby alternatives. ABI-088 specifically argues against stacking generic spectral-spatial recalibration gates inside this architecture under the current capped 12-epoch constant-LR policy.

Canonical MCAST 2.1 remains the promotion context, and all comparisons here are capped representative family-development evidence unless an explicitly requested whole-validation diagnostic is run.

## Decision

Do not promote ABI-088. Do not repeat the exact SE-recalibration branch unchanged. A whole-validation Evaluation Request for ABI-088 is not the next priority because it did not improve ABI-068 and did not provide a secondary-metric advantage.

Future work should broaden away from additional generic gates on ABI-068. A useful next hypothesis should either move to a materially different in-contract architecture family or test another trusted policy axis that can address false positives and connectivity without moving thresholding, Artifact Filters, data loading, sampling, augmentation implementation, target derivation, losses, metrics, resource placement, or lifecycle behavior into Candidate code.

## Artifact references

- `run_20260829_203135_e22164/outputs/best_metrics.json`
- `run_20260829_203135_e22164/outputs/final_metrics.json`
- `run_20260829_203135_e22164/outputs/metrics.jsonl`
- `run_20260829_203135_e22164/outputs/resource_profile.json`
- `run_20260829_203135_e22164/outputs/model_summary.json`
- `run_20260829_203135_e22164/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260828_094949_ad2af0/outputs/best_metrics.json`
- `run_20260829_143707_7c7d44/outputs/best_metrics.json`
- `run_20260829_181201_01c5e7/outputs/best_metrics.json`
- `run_20260829_193824_241e30/outputs/best_metrics.json`
