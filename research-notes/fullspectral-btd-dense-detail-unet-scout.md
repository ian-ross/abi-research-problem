# Full-spectral BTD dense-detail U-Net scout

research-figures: []

## Scope

This note records ABI-098 after Run `run_20260830_040621_bb9ebc` completed.

Source Runs:

- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-078 frequency-gated line U-Net BCE-Dice conservative operating-point reference: `run_20260828_094949_ad2af0`
- ABI-085 frequency-gated line U-Net lower-learning-rate focal-Tversky reference: `run_20260829_181201_01c5e7`
- ABI-097 frequency-gated line U-Net negative-bias focal-Tversky reference: `run_20260830_030927_4f7d3d`
- ABI-098 dense-detail U-Net scout: `run_20260830_040621_bb9ebc`

ABI-098 tested a compact dense-detail U-Net branch intended to preserve shallow full-spectral ABI and thermal BTD line evidence through dense local feature reuse, detail-gated skip fusion, a compact atrous bottleneck, and a high-resolution detail refiner. The Run used provider-approved `abi_16ch` input only, trusted `focal_tversky` primary loss, trusted `combined_source_balanced` sampling, trusted `random_mirroring`, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, and a provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. It used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-scout evidence rather than full-data promotion evidence.

## ABI-098 implementation and resource observation

ABI-098 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI tensors and BTD planes derived from approved ABI channels. It did not introduce candidate-owned data loading, split logic, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.

Model summary reported 3,014,026 parameters against the 25,000,000-parameter smoke ceiling. The model summary confirmed GOES ABI channels 1-16 only, with forbidden longitude/latitude source channels excluded, and outputs `mask_logits` plus `centerline_logits`. The Run completed at batch size 4 on the A100 with 2,000.2 seconds wall time, 8,111,783,936 bytes peak CUDA reserved, and no terminal execution failure. Resource behavior was feasible within the 3,600-second Docker training timeout and lighter than several recent frequency-gated variants.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, `focal_tversky` | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice` | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_094949_ad2af0` | ABI-078 | ABI-068 branch, `bce_dice` | 11 | 0.3816 | 0.3704 | 0.4093 | 0.4072 | 0.3590 | 0.3061 | 0.00320 |
| `run_20260829_181201_01c5e7` | ABI-085 | ABI-068 branch, lower learning rate 0.0001 | 12 | 0.3826 | 0.3733 | 0.4059 | 0.3693 | 0.3968 | 0.3698 | 0.00389 |
| `run_20260830_030927_4f7d3d` | ABI-097 | ABI-068 branch, negative output-bias initialization | 12 | 0.3737 | 0.3737 | 0.3737 | 0.3231 | 0.4431 | 0.2614 | 0.00497 |
| `run_20260830_040621_bb9ebc` | ABI-098 | dense-detail U-Net scout | 12 | 0.3229 | 0.3160 | 0.3393 | 0.2577 | 0.4322 | 0.1777 | 0.00608 |

ABI-098 did not meet the preregistered useful-scout criteria. Relative to ABI-068, aggregate filtered Dice fell by about -0.0735, MIT filtered Dice by -0.0726, Google filtered Dice by -0.0768, filtered precision by -0.1414, filtered connectivity by -0.2123, and filtered predicted-positive fraction increased from 0.00357 to 0.00608. Recall increased by about +0.0386, but the gain came with substantially broader positive area and poor connectivity.

Relative to ABI-066, ABI-098 lost about -0.0596 filtered Dice, -0.0478 MIT Dice, -0.0899 Google Dice, -0.1850 precision, -0.2954 connectivity, and more than doubled the filtered predicted-positive fraction. Relative to ABI-097, ABI-098 retained a recall-heavy endpoint but worsened aggregate Dice, precision, source metrics, connectivity, and positive-area discipline. The dense-detail hypothesis therefore did not produce the intended thin-line preservation advantage under the current focal-Tversky, centerline-auxiliary, constant-LR budget.

## ABI-098 trajectory

ABI-098 trained finitely and avoided terminal all-negative/all-positive collapse. Filtered Dice by epoch was 0.0825, 0.0964, 0.2054, 0.2212, 0.2635, 0.2311, 0.2150, 0.2999, 0.2714, 0.2540, 0.3059, and 0.3229. The selected checkpoint was the final epoch 12, so the trajectory was still improving late, but it remained well below the useful-scout floor and below both Dataset Sources' approximate 0.32 hard-stop threshold on MIT.

At the selected checkpoint, filtered precision was 0.2577, filtered recall 0.4322, filtered connectivity 0.1777, and filtered predicted-positive fraction 0.00608. The MIT/Google filtered Dice split was 0.3160/0.3393. Raw-to-filtered differences were modest: raw Dice 0.3295 versus filtered Dice 0.3229, and raw predicted-positive fraction 0.00652 versus filtered 0.00608. This suggests the main failure mode was not excessive dependence on Artifact Filters, but a low-precision, low-connectivity positive-area expansion at the trusted threshold.

The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` all had near-zero per-sample Dice. Because prediction retention is fixed `first_n`, these samples are bounded artifacts and not representative qualitative evidence; aggregate and source-stratified validation metrics carry this decision.

## Interpretation

Classify ABI-098 as finite, resource-feasible, non-collapsed, but negative capped family-scout evidence for the exact compact dense-detail U-Net branch. The branch did not approach ABI-068 within 0.02, did not improve connectivity, did not lower predicted-positive burden, and did not exceed ABI-066 while retaining acceptable source-stratified Dice. Its final MIT filtered Dice of 0.3160 also falls below the proposal's hard-stop guidance for Dataset Source behavior.

The late-improving trajectory means the architecture family is not disproven in an absolute sense, but under the active 12-epoch constant-LR representative cap this exact dense-detail design is not a good follow-up target. The dominant pattern repeats recent recall-heavy, low-precision expansion failures: adding high-resolution detail reuse without a stronger precision/connectivity mechanism increased positive area rather than preserving clean thin contrails.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-098 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-098. Do not repeat this dense-detail U-Net unchanged, and do not request a whole-validation failure-bucket diagnostic for it ahead of ABI-068 or ABI-066. Retain ABI-068 as the local aggregate-Dice reference and ABI-066 as the precision/connectivity reference. A useful next hypothesis should broaden away from local dense-detail reuse toward a mechanism that can improve precision/connectivity or threshold discipline without candidate-owned postprocessing, Artifact Filters, target derivation, losses, metrics, sampling implementation, augmentation implementation, resource placement, or lifecycle behavior.

## Artifact references

- `run_20260830_040621_bb9ebc/outputs/best_metrics.json`
- `run_20260830_040621_bb9ebc/outputs/final_metrics.json`
- `run_20260830_040621_bb9ebc/outputs/metrics.jsonl`
- `run_20260830_040621_bb9ebc/outputs/resource_profile.json`
- `run_20260830_040621_bb9ebc/outputs/model_summary.json`
- `run_20260830_040621_bb9ebc/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260828_094949_ad2af0/outputs/best_metrics.json`
- `run_20260829_181201_01c5e7/outputs/best_metrics.json`
- `run_20260830_030927_4f7d3d/outputs/best_metrics.json`
