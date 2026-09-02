# Full-spectral BTD frequency-gated line U-Net scale-selective ridge-gate follow-up

research-figures: []

## Scope

This note records ABI-116 after Run `run_20260831_004912_1df8c4` completed.

Source Runs:

- ABI-116 scale-selective ridge-gate continuation: `run_20260831_004912_1df8c4`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-099 earlier directional line-coherence gate negative context: `run_20260830_044731_a5c0bf`
- ABI-113 patch-anomaly line U-Net follow-up context: `run_20260830_220436_b4eadb`
- ABI-115 MIT-only data-policy follow-up context: `run_20260830_235533_487b1c`

ABI-116 was a family-development continuation within the full-spectral BTD frequency-gated line U-Net branch. It retained provider-approved `abi_16ch` input, deterministic thermal BTD features derived only from GOES ABI channels 1-16, trusted provider-owned `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.

The controlled architecture change was a low-capacity `ScaleSelectiveRidgeGate` before the mask and centerline heads. The hypothesis was that soft selection among local residual scales plus horizontal/vertical anisotropic line averages would recover precision, Contrail Connectivity, or positive-area discipline relative to ABI-068 while preserving source-balanced Dice. This is capped representative family-development evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-116 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI Channel Input and BTD combinations derived from approved ABI channels. It did not introduce candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: focal_tversky`, and auxiliary output `centerline_logits` with trusted `weighted_bce` weight 0.02. `outputs/model_summary.json` reported 12,177,280 parameters against the 25,000,000-parameter smoke ceiling and confirmed GOES ABI channels 1-16 only with forbidden longitude/latitude source channels excluded.

The Run completed at batch size 4 on the A100 with 3,190.0 seconds total wall time, 1,689.5 seconds training wall time, 1,498.2 seconds validation wall time, 10,926,161,920 bytes peak CUDA reserved, and no terminal execution failure. The selected best-validation checkpoint was epoch 12.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, centerline aux | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | BCE-Dice-clDice precision/connectivity reference | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260830_044731_a5c0bf` | ABI-099 | directional line-coherence gate | 11 | 0.3401 | 0.3499 | 0.3187 | 0.2558 | 0.5074 | 0.1421 | 0.00719 |
| `run_20260830_220436_b4eadb` | ABI-113 | patch-relative anomaly features | 12 | 0.3670 | 0.3689 | 0.3627 | 0.3265 | 0.4191 | 0.1594 | 0.00465 |
| `run_20260830_235533_487b1c` | ABI-115 | MIT-only sampling traversal | 9 | 0.3515 | 0.3588 | 0.3345 | 0.3085 | 0.4084 | 0.2795 | 0.00480 |
| `run_20260831_004912_1df8c4` | ABI-116 | scale-selective ridge gate | 12 | 0.3729 | 0.3681 | 0.3836 | 0.3248 | 0.4378 | 0.2225 | 0.00488 |

ABI-116 did not meet the preregistered useful-continuation criteria. Relative to ABI-068, aggregate filtered Dice decreased from 0.3964 to 0.3729 (-0.0234), MIT filtered Dice decreased from 0.3886 to 0.3681 (-0.0205), Google filtered Dice decreased from 0.4161 to 0.3836 (-0.0325), filtered precision decreased from 0.3992 to 0.3248 (-0.0744), and filtered connectivity decreased from 0.3900 to 0.2225 (-0.1675). Filtered recall increased from 0.3936 to 0.4378 (+0.0441), but the filtered predicted-positive fraction also increased from 0.00357 to 0.00488.

Relative to ABI-066, ABI-116 had slightly higher MIT filtered Dice (+0.0043) and substantially higher recall (+0.1010), but lower aggregate filtered Dice (-0.0096), lower Google filtered Dice (-0.0456), lower precision (-0.1179), much lower connectivity (-0.2505), and a larger positive mask area. It therefore does not challenge ABI-066's precision/connectivity reference role.

Relative to ABI-099, the new scale-selective ridge gate avoided the most severe directional-gate failure mode: ABI-116 improved aggregate filtered Dice by +0.0328, Google filtered Dice by +0.0649, precision by +0.0690, connectivity by +0.0804, and positive-area discipline. However, it remained a recall-forward gate branch with materially worse precision and connectivity than ABI-068 or ABI-066. Relative to ABI-113 and ABI-115, ABI-116 improved aggregate Dice and Google Dice, but it did not provide a new best local operating point or the intended secondary-metric recovery.

## ABI-116 trajectory

ABI-116 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.1986, 0.2092, 0.2958, 0.2658, 0.3233, 0.2818, 0.3214, 0.3259, 0.3453, 0.3518, 0.3575, and 0.3729. The selected checkpoint was the final epoch, so the branch retained late improvement rather than plateauing early.

At the selected checkpoint, raw Dice was 0.3845 and filtered Dice was 0.3729. Filtered precision was 0.3248, filtered recall 0.4378, filtered connectivity 0.2225, and filtered predicted-positive fraction 0.00488. Source-stratified filtered Dice was 0.3681 MIT and 0.3836 Google. The source split stayed non-catastrophic and source-balanced enough to be useful evidence, but both sources remained below ABI-068.

Raw-to-filtered differences were modest: raw Dice 0.3845 versus filtered Dice 0.3729, and raw predicted-positive fraction 0.00520 versus filtered 0.00488. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` all had near-zero per-sample Dice; because prediction retention is fixed `first_n`, these are bounded artifacts rather than representative qualitative evidence.

## Interpretation

Classify ABI-116 as finite, resource-feasible, non-collapsed, but negative capped family-development evidence for the exact scale-selective ridge-gate branch. The gate did not recover precision, connectivity, or lower predicted-positive burden relative to ABI-068, and it stayed below ABI-068 on aggregate and both Dataset Source filtered Dice. It also stayed below ABI-066 on the precision/connectivity profile that motivated the branch.

The Run is not a candidate bug or contract failure: it completed safely, selected a late best epoch, and avoided source-catastrophic collapse. It does, however, add to the pattern that post-decoder high-resolution/ridge/detail gates around the ABI-068 backbone tend to shift toward recall and extra positive area without delivering stable connectivity or precision gains under the current focal-Tversky, centerline-auxiliary, constant-LR budget.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-116 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-116. Do not request whole-validation diagnostics for ABI-116 ahead of ABI-068 or ABI-066, because it did not improve aggregate Dice, source-stratified Dice, precision/connectivity, or positive-area discipline relative to those references.

Stop this exact scale-selective ridge-gate branch. Retain ABI-068 as the local aggregate-Dice reference and ABI-066 as the precision/connectivity reference for the frequency-gated line U-Net family. The next useful hypothesis should broaden away from additional post-decoder ridge/detail gates on ABI-068 and toward a materially different contract-compliant mechanism for calibration, source robustness, false-positive suppression, or thin-line continuity while continuing to leave data loading, split logic, sampling implementation, augmentation implementation, losses, metrics, Artifact Filters, postprocessing, resource placement, and lifecycle under provider/Harness ownership.

## Artifact references

- `run_20260831_004912_1df8c4/outputs/best_metrics.json`
- `run_20260831_004912_1df8c4/outputs/final_metrics.json`
- `run_20260831_004912_1df8c4/outputs/metrics.jsonl`
- `run_20260831_004912_1df8c4/outputs/resource_profile.json`
- `run_20260831_004912_1df8c4/outputs/model_summary.json`
- `run_20260831_004912_1df8c4/outputs/prediction_samples/samples.json`
- `run_20260831_004912_1df8c4/resolved_manifest.yaml`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260830_044731_a5c0bf/outputs/best_metrics.json`
- `run_20260830_220436_b4eadb/outputs/best_metrics.json`
- `run_20260830_235533_487b1c/outputs/best_metrics.json`
