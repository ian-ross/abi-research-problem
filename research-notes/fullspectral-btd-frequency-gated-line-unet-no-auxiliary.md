# Full-spectral BTD frequency-gated line U-Net no-auxiliary follow-up

research-figures: []

## Scope

This note records ABI-081 after Run `run_20260829_143707_7c7d44` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-078 frequency-gated line U-Net BCE-Dice loss-swap reference: `run_20260828_094949_ad2af0`
- ABI-081 no-auxiliary focal-Tversky continuation: `run_20260829_143707_7c7d44`

ABI-081 used provider-approved `abi_16ch` input, ABI-channel-derived thermal BTD features, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, and trusted `focal_tversky` primary loss. The controlled change from ABI-068 was removal of the provider-derived `centerline` auxiliary target and `centerline_logits` output. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-development evidence rather than full-data promotion evidence.

## ABI-081 implementation and resource observation

ABI-081 kept the frequency-gated line U-Net backbone, BTD/mixer front end, frequency-pyramid fusion, and oriented line refiner used by ABI-068, but returned only the required primary `mask_logits` output. It did not introduce candidate-owned data loading, sampling, augmentation, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, or pretrained weights. The trusted model summary recorded `abi_16ch` input shape `[16, 256, 256]`, output name `mask_logits`, and forbidden longitude/latitude source channel indices 16 and 17 excluded.

Model summary reported 12,087,516 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 2,655.2 seconds wall time, 9,537,847,296 bytes peak CUDA reserved, and no terminal execution failure. Removing the auxiliary head was resource-feasible and marginally lighter/faster than ABI-068, but the difference is not a scientific result.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260828_094949_ad2af0` | ABI-078 | ABI-068 architecture with `bce_dice` primary loss | 11 | 0.3816 | 0.3704 | 0.4093 | 0.4072 | 0.3590 | 0.3061 | 0.00320 |
| `run_20260829_143707_7c7d44` | ABI-081 | ABI-068 architecture, no auxiliary head, `focal_tversky` | 9 | 0.3809 | 0.3624 | 0.4279 | 0.3797 | 0.3822 | 0.3893 | 0.00365 |

ABI-081 did not improve the strongest local ABI-068 reference. Relative to ABI-068, aggregate filtered Dice fell by about -0.0155, MIT filtered Dice by -0.0262, precision by -0.0195, recall by -0.0115, and connectivity by -0.0008. Google filtered Dice improved by about +0.0118 and the filtered predicted-positive fraction was similar, 0.00365 versus 0.00357, but this source-specific gain did not offset the aggregate and MIT losses.

Relative to ABI-078, ABI-081 was essentially tied on aggregate filtered Dice (-0.0007), lower on MIT and precision, but higher on Google, recall, and connectivity. Relative to ABI-066, ABI-081 was slightly lower on aggregate filtered Dice (-0.0016), much lower on precision and connectivity, but higher on recall. This shows that removing the centerline auxiliary head did not recover ABI-066-style positive-area discipline or connectivity, and it did not surpass the ABI-068 focal-Tversky operating point.

## ABI-081 trajectory

ABI-081 trained finitely and avoided all-negative/all-positive collapse. Filtered Dice by epoch was 0.1930, 0.2484, 0.2999, 0.3018, 0.3384, 0.3029, 0.3142, 0.3320, 0.3809, 0.3586, 0.3681, and 0.3678. The selected checkpoint was epoch 9; epochs 10-12 stayed non-degenerate but did not recover the best score.

At the selected checkpoint, both Dataset Sources were non-catastrophic: MIT filtered Dice was 0.3624 and Google filtered Dice was 0.4279. The operating point remained balanced enough for useful family-development evidence, with filtered precision 0.3797, filtered recall 0.3822, filtered connectivity 0.3893, and filtered predicted-positive fraction 0.00365. The final epoch shifted more recall-heavy and less precise, ending at 0.3678 filtered Dice, 0.3278 precision, 0.4189 recall, 0.2916 connectivity, and 0.00463 filtered predicted-positive fraction.

The fixed first-four retained prediction samples had Dice values near zero, one, near zero, and near zero. Because prediction retention is fixed `first_n`, these are bounded retained artifacts rather than representative qualitative evidence; aggregate and source-stratified validation metrics carry the decision.

## Interpretation

Classify ABI-081 as a useful but non-improving capped family-development continuation. It provides evidence that the centerline auxiliary head is not the sole cause of the focal-Tversky branch's precision/connectivity trade-off: removing it preserved non-degenerate source-balanced learning and nearly matched ABI-066/078 aggregate Dice, but it did not improve over ABI-068 or produce cleaner positive-area behavior.

This result does not eliminate the broader full-spectral BTD or frequency-gated line U-Net families. ABI-068 remains the strongest capped representative result in this branch, ABI-066 remains the precision/connectivity-forward reference, and ABI-081 indicates that future work should not assume that simply dropping auxiliary supervision is enough to fix calibration or false positives.

Canonical MCAST 2.1 remains the promotion context, and all comparisons here are capped representative family-development evidence rather than full-data promotion claims.

## Decision

Do not promote ABI-081. Do not repeat the exact no-auxiliary focal-Tversky branch unchanged. Prefer broadening away from auxiliary-head ablations and late refiner/head modules toward a materially different thin-line architecture or a trusted training/calibration frontier that can address precision/connectivity without moving thresholding, losses, Artifact Filters, postprocessing, data loading, sampling, augmentation, target derivation, metrics, resource placement, or lifecycle behavior into Candidate code.

## Artifact references

- `run_20260829_143707_7c7d44/outputs/best_metrics.json`
- `run_20260829_143707_7c7d44/outputs/final_metrics.json`
- `run_20260829_143707_7c7d44/outputs/metrics.jsonl`
- `run_20260829_143707_7c7d44/outputs/resource_profile.json`
- `run_20260829_143707_7c7d44/outputs/model_summary.json`
- `run_20260829_143707_7c7d44/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260828_094949_ad2af0/outputs/best_metrics.json`
