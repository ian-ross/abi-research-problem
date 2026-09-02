# Full-spectral BTD frequency-gated line U-Net thermal-only input follow-up

research-figures: []

## Scope

This note records ABI-082 after Run `run_20260829_152950_e53671` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-081 no-auxiliary focal-Tversky continuation: `run_20260829_143707_7c7d44`
- ABI-082 thermal-only BTD frequency-gated line U-Net continuation: `run_20260829_152950_e53671`

ABI-082 used provider-approved `abi_thermal_10ch` input, ABI-channel-derived thermal BTD features, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, trusted `focal_tversky` primary loss, and a provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. The controlled change from ABI-068 was the input/preprocessing axis: remove reflective ABI channels 1-6 and train on thermal channels 7-16 plus thermal BTD evidence. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-development evidence rather than full-data promotion evidence.

## ABI-082 implementation and resource observation

ABI-082 kept the frequency-gated line U-Net pattern from ABI-068: thermal learned channel mixing, explicit thermal BTD planes, frequency-split stem, residual encoder/decoder, frequency-pyramid fusion, oriented line refiner, primary `mask_logits`, and provider-derived `centerline_logits`. It did not introduce candidate-owned data loading, sampling, augmentation, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, or pretrained weights.

Model summary reported 12,086,673 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 2,679.6 seconds wall time, 9,510,584,320 bytes peak CUDA reserved, and no terminal execution failure. The thermal-only variant was resource-feasible and comparable to the full-spectral ABI-068/081 envelope.

## Best-validation comparison

| Run | Candidate | Primary architecture/input/loss | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_230540_bf4ce3` | ABI-066 | full-spectral frequency-gated line U-Net, `bce_dice_cldice`, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_010836_4ccc77` | ABI-068 | full-spectral frequency-gated line U-Net, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260829_143707_7c7d44` | ABI-081 | ABI-068 architecture, no auxiliary head, `focal_tversky` | 9 | 0.3809 | 0.3624 | 0.4279 | 0.3797 | 0.3822 | 0.3893 | 0.00365 |
| `run_20260829_152950_e53671` | ABI-082 | thermal-only BTD frequency-gated line U-Net, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3698 | 0.3708 | 0.3678 | 0.3154 | 0.4469 | 0.2031 | 0.00513 |

ABI-082 completed finite and non-degenerate, and both Dataset Sources cleared the proposal's 0.33 filtered-Dice floor. However, it did not meet the stronger continuation criteria. Relative to ABI-068, aggregate filtered Dice fell by about -0.0265, MIT filtered Dice by -0.0178, Google filtered Dice by -0.0483, precision by -0.0838, and connectivity by -0.1869. Recall improved by about +0.0533, but the predicted-positive fraction rose from 0.00357 to 0.00513, indicating a more recall-heavy and less disciplined operating point rather than the hoped-for cleaner thermal-only behavior.

Relative to ABI-081, ABI-082 improved MIT filtered Dice by about +0.0084 and recall by about +0.0647, but lost about -0.0111 aggregate filtered Dice, -0.0601 Google filtered Dice, -0.0643 precision, and -0.1862 connectivity. Relative to ABI-066, ABI-082 was also lower on aggregate filtered Dice, precision, and connectivity while increasing recall. Thus the thermal-only input did not recover ABI-066-style precision/connectivity and did not improve on ABI-068's aggregate-Dice reference.

## ABI-082 trajectory

ABI-082 trained finitely and avoided all-negative/all-positive collapse. Filtered Dice by epoch was 0.2081, 0.2808, 0.2896, 0.2955, 0.3257, 0.2914, 0.3033, 0.3573, 0.3563, 0.3537, 0.2862, and 0.3698. The selected checkpoint was the final epoch 12, so the trajectory still contained late improvement after an epoch-11 drop.

The operating point moved substantially with epoch. Epoch 10 had higher precision and connectivity than the selected final checkpoint, but lower aggregate filtered Dice: 0.3537 filtered Dice, 0.3600 precision, 0.3475 recall, 0.3025 connectivity, and 0.00350 filtered predicted-positive fraction. Epoch 12 selected higher Dice through recall: 0.3698 filtered Dice, 0.3154 precision, 0.4469 recall, 0.2031 connectivity, and 0.00513 filtered predicted-positive fraction. The final selection therefore reinforces the interpretation that thermal-only evidence shifted this branch toward recall at the expense of positive-area discipline and line connectivity.

The fixed first-four retained prediction samples all had near-zero sample Dice. Because prediction retention is fixed `first_n`, these are bounded retained artifacts rather than representative qualitative evidence; aggregate and source-stratified validation metrics carry the decision.

## Interpretation

Classify ABI-082 as useful but non-improving capped family-development evidence. It shows that the thermal-only ABI channels 7-16 plus BTD front end are sufficient for finite, source-balanced learning in the frequency-gated line U-Net branch, but they do not improve the capped trade-off against full-spectral ABI-068. Removing reflective channels did not reduce the predicted-positive burden or improve precision/connectivity; instead it produced a more recall-heavy operating point, with a particularly large Google-source and connectivity drop.

This result does not eliminate thermal ABI evidence in general, nor the broader frequency-gated or BTD families. It does argue against repeating this exact thermal-only ABI-068-style branch unchanged under the current capped budget. The stronger local references remain ABI-068 for aggregate capped filtered Dice, ABI-066 for precision/connectivity-forward behavior, and ABI-081 as evidence that auxiliary-head removal alone is not the fix.

Canonical MCAST 2.1 remains the promotion context, and all comparisons here are capped representative family-development evidence rather than full-data promotion claims.

## Decision

Do not promote ABI-082. Do not repeat the exact thermal-only frequency-gated focal-Tversky centerline-auxiliary branch unchanged. Future work should broaden away from simple input removal within this branch, either toward a materially different thin-line architecture or a trusted training/calibration/data-policy axis that can address precision and connectivity without moving thresholding, losses, Artifact Filters, postprocessing, data loading, sampling, augmentation, target derivation, metrics, resource placement, or lifecycle behavior into Candidate code.

## Artifact references

- `run_20260829_152950_e53671/outputs/best_metrics.json`
- `run_20260829_152950_e53671/outputs/final_metrics.json`
- `run_20260829_152950_e53671/outputs/metrics.jsonl`
- `run_20260829_152950_e53671/outputs/resource_profile.json`
- `run_20260829_152950_e53671/outputs/model_summary.json`
- `run_20260829_152950_e53671/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260829_143707_7c7d44/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
