# Full-spectral BTD frequency-gated line U-Net context/detail agreement follow-up

research-figures: []

## Scope

This note records ABI-089 after Run `run_20260829_212901_6bbc6f` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-085 low-learning-rate focal-Tversky continuation: `run_20260829_181201_01c5e7`
- ABI-088 SE-recalibrated focal-Tversky continuation: `run_20260829_203135_e22164`
- ABI-089 context/detail agreement continuation: `run_20260829_212901_6bbc6f`

ABI-089 used provider-approved `abi_16ch` input only, ABI-channel-derived thermal brightness-temperature-difference features, combined source-balanced sampling, trusted `random_mirroring`, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, trusted `focal_tversky` primary loss, and a provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. The controlled architecture change from ABI-068 was replacing the final frequency-pyramid fusion block with a context/detail agreement fusion module before the oriented line refiner. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-development evidence rather than full-data promotion evidence.

## ABI-089 implementation and resource observation

ABI-089 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI tensors and BTD planes derived from approved ABI channels. It did not introduce candidate-owned data loading, sampling, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, pretrained weights, or longitude/latitude inputs.

Model summary reported 12,284,153 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 3,005.9 seconds wall time, 11,205,083,136 bytes peak CUDA reserved, and no terminal execution failure. Resource behavior was feasible under the current 3,600-second Docker training timeout, but it is slower/heavier than the leaner ABI-066/068 frequency-gated reference branch.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, `focal_tversky`, random mirroring, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | same family, `bce_dice_cldice`, random mirroring, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260829_181201_01c5e7` | ABI-085 | ABI-068 architecture/loss/aux, learning rate 0.0001 | 12 | 0.3826 | 0.3733 | 0.4059 | 0.3693 | 0.3968 | 0.3698 | 0.00389 |
| `run_20260829_203135_e22164` | ABI-088 | distributed spectral-spatial feature recalibration | 9 | 0.3594 | 0.3449 | 0.3948 | 0.3559 | 0.3629 | 0.1464 | 0.00369 |
| `run_20260829_212901_6bbc6f` | ABI-089 | context/detail agreement fusion before oriented line refinement | 12 | 0.3644 | 0.3599 | 0.3748 | 0.3404 | 0.3920 | 0.2374 | 0.00417 |

ABI-089 did not meet its strongest continuation criteria. Relative to ABI-068, aggregate filtered Dice fell by about -0.0320, MIT filtered Dice by about -0.0287, Google filtered Dice by about -0.0413, precision by about -0.0587, recall by about -0.0016, and filtered connectivity by about -0.1526. The filtered predicted-positive fraction rose from 0.00357 to 0.00417, so the context/detail agreement module did not lower the false-positive burden.

Relative to ABI-066, ABI-089 recovered recall by about +0.0553 but lost aggregate Dice, Google Dice, precision, connectivity, and positive-area discipline. Relative to ABI-088, ABI-089 recovered some aggregate Dice, MIT Dice, recall, and connectivity, but the gain was not enough to approach ABI-068/066/085 and came with lower precision and higher predicted-positive fraction.

## ABI-089 trajectory

Filtered Dice by epoch was 0.1962, 0.1914, 0.2910, 0.2792, 0.3109, 0.3346, 0.2890, 0.3245, 0.3090, 0.3617, 0.3048, and 0.3644. The selected checkpoint was epoch 12. The trajectory was finite and late-improving, with both Dataset Sources near the aggregate at the selected epoch (MIT 0.3599; Google 0.3748), so this is not prediction collapse or an execution failure.

The trajectory was also noisy after epoch 6 and never entered the ABI-068/085 primary-metric band. Epoch 11 briefly shifted toward high recall (0.5175) with low precision (0.2160) and the largest positive fraction (0.00868), then epoch 12 returned to a more balanced but still sub-reference point. This suggests the context/detail agreement block did not stabilize the precision/recall trade-off under the current constant learning-rate, 12-epoch capped policy.

The retained fixed first-four prediction samples all had near-zero sample Dice in `outputs/prediction_samples/samples.json`. Because prediction retention is fixed `first_n`, these are bounded artifacts and not representative qualitative evidence; aggregate and source-stratified validation metrics carry this decision.

## Interpretation

Classify ABI-089 as negative capped family-development evidence, not a Harness or Candidate execution failure. The context/detail agreement idea was contract-compliant and resource-feasible, and it avoided ABI-088's most severe connectivity collapse, but it did not preserve ABI-068-like aggregate Dice or recover ABI-066-like precision/connectivity. The most important scientific signal is that separating full-resolution detail and smoothed context only at the final fusion stage increased positive-area burden while reducing precision and connectivity versus ABI-068.

This result does not eliminate the broader frequency-gated line U-Net family. ABI-068 remains the strongest local capped Candidate by primary filtered Dice, ABI-066 remains the precision/connectivity-forward reference, and ABI-085 remains a nearby learning-rate-policy alternative. ABI-089 specifically argues against further single-stage post-decoder agreement/gating refinements as the next local move.

Canonical MCAST 2.1 remains the promotion context, and all comparisons here are capped representative family-development evidence unless an explicitly requested whole-validation diagnostic is run.

## Decision

Do not promote ABI-089. Do not repeat the exact context/detail agreement branch unchanged. A whole-validation Evaluation Request for ABI-089 is not the next priority because it did not improve ABI-068 and did not provide a secondary-metric advantage worth diagnosing.

Future work should broaden away from additional ABI-068 post-decoder gates or agreement modules. A useful next hypothesis should move to a materially different in-contract architecture family or a clearly different trusted policy axis that can address false positives and connectivity without moving thresholding, Artifact Filters, data loading, sampling, augmentation implementation, target derivation, losses, metrics, resource placement, or lifecycle behavior into Candidate code.

## Artifact references

- `run_20260829_212901_6bbc6f/outputs/best_metrics.json`
- `run_20260829_212901_6bbc6f/outputs/final_metrics.json`
- `run_20260829_212901_6bbc6f/outputs/metrics.jsonl`
- `run_20260829_212901_6bbc6f/outputs/resource_profile.json`
- `run_20260829_212901_6bbc6f/outputs/model_summary.json`
- `run_20260829_212901_6bbc6f/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260829_181201_01c5e7/outputs/best_metrics.json`
- `run_20260829_203135_e22164/outputs/best_metrics.json`
