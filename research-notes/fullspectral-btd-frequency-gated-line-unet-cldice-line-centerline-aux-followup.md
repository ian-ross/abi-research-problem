# Full-spectral BTD frequency-gated line U-Net clDice line+centerline auxiliary follow-up

research-figures: []

## Scope

This note records ABI-114 after Run `run_20260830_225952_22da29` completed.

Source Runs:

- ABI-114 BCE-Dice-clDice with Line and Centerline Target auxiliary supervision: `run_20260830_225952_22da29`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-108 line+centerline auxiliary focal-Tversky reference: `run_20260830_115800_4a2363`
- ABI-105 conservative-skip focal-Tversky continuation: `run_20260830_091941_139456`
- ABI-107 feature-dropout focal-Tversky continuation: `run_20260830_110428_804d89`

ABI-114 was a family-development continuation within the full-spectral BTD frequency-gated line U-Net branch. It kept provider-approved `abi_16ch` input, deterministic thermal BTD features derived only from GOES ABI channels 1-16, trusted provider-owned `combined_source_balanced` traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.

The controlled change was combining ABI-108's low-weight provider-derived Line Target plus Centerline Target auxiliary heads with ABI-066's trusted `bce_dice_cldice` primary loss. The hypothesis was that Line Target supervision might improve the clDice branch's recall or MIT/Google balance while retaining ABI-066-like positive-area discipline and connectivity. This is capped representative evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-114 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI Channel Input and approved-channel combinations. It did not introduce candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: bce_dice_cldice`, and two auxiliary outputs: `centerline_logits` and `line_logits`, both using trusted `weighted_bce` weight 0.02. `outputs/model_summary.json` reported 12,087,606 parameters against the 25,000,000-parameter smoke ceiling, confirmed GOES ABI channels 1-16 only with forbidden longitude/latitude source channels excluded, and confirmed outputs `mask_logits`, `centerline_logits`, and `line_logits`.

The Run completed at batch size 4 on the A100 with 2,877.5 seconds total wall time, 1,446.1 seconds training wall time, 1,429.2 seconds validation wall time, 9,737,076,736 bytes peak CUDA reserved, and no terminal execution failure. The best-validation checkpoint was epoch 12.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, centerline aux | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, centerline aux | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260830_115800_4a2363` | ABI-108 | focal-Tversky with Line and Centerline Target auxiliary heads | 9 | 0.3822 | 0.3660 | 0.4242 | 0.3938 | 0.3713 | 0.3575 | 0.00342 |
| `run_20260830_091941_139456` | ABI-105 | ABI-068 branch, conservative non-amplifying skip gates | 12 | 0.3831 | 0.3820 | 0.3857 | 0.3344 | 0.4484 | 0.2520 | 0.00486 |
| `run_20260830_110428_804d89` | ABI-107 | ABI-068 branch, low-probability feature dropout | 12 | 0.3804 | 0.3701 | 0.4046 | 0.3630 | 0.3997 | 0.3182 | 0.00399 |
| `run_20260830_225952_22da29` | ABI-114 | BCE-Dice-clDice with Line and Centerline Target auxiliary heads | 12 | 0.3806 | 0.3635 | 0.4229 | 0.4160 | 0.3508 | 0.4405 | 0.00306 |

ABI-114 did not meet a useful-continuation criterion relative to ABI-068. Aggregate filtered Dice decreased from 0.3964 to 0.3806 (-0.0157), MIT filtered Dice decreased from 0.3886 to 0.3635 (-0.0251), and filtered recall decreased from 0.3936 to 0.3508 (-0.0428). It did improve Google filtered Dice (+0.0068), filtered precision (+0.0169), filtered connectivity (+0.0504), and positive-area discipline (filtered predicted-positive fraction 0.00306 versus 0.00357), but not enough to offset the aggregate and MIT/source-balanced loss.

Relative to ABI-066, ABI-114 was effectively close on aggregate filtered Dice (-0.0019) and MIT filtered Dice (-0.0003), with higher recall (+0.0140), but it lost the specific strengths ABI-066 was retained for: Google filtered Dice (-0.0063), precision (-0.0267), connectivity (-0.0326), and lower predicted-positive fraction. Relative to ABI-108, changing the primary loss from focal-Tversky to BCE-Dice-clDice kept aggregate/source Dice approximately tied, improved precision (+0.0222), connectivity (+0.0830), and positive-area discipline, but reduced recall (-0.0205).

## ABI-114 trajectory

ABI-114 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.2543, 0.3083, 0.3273, 0.2643, 0.3362, 0.3567, 0.3504, 0.3573, 0.3734, 0.3669, 0.3674, and 0.3806. The selected checkpoint was the final epoch, so the Run retained late improvement despite a noisy epoch-4 high-recall/low-precision excursion.

At the selected checkpoint, filtered Dice was 0.3806, raw Dice 0.3944, filtered IoU 0.2351, filtered precision 0.4160, filtered recall 0.3508, filtered connectivity 0.4405, and filtered predicted-positive fraction 0.00306. Source-stratified filtered Dice was 0.3635 MIT and 0.4229 Google. Google remained stronger than MIT and more recall-forward (`0.4067` precision, `0.4405` recall), while MIT was more conservative (`0.4206` precision, `0.3201` recall).

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice 0.3944 versus filtered Dice 0.3806, and raw predicted-positive fraction 0.00325 versus filtered 0.00306. This does not look primarily like an Artifact Filter dependence issue. The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` all had near-zero per-sample Dice, but these are bounded `first_n` artifacts and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-114 as finite, resource-feasible, non-collapsed, and mixed capped family-development evidence. It validates that the line+centerline auxiliary configuration can train under the clDice primary loss and can reach a cleaner precision/connectivity operating point than the same auxiliary configuration under focal-Tversky. However, it does not improve over ABI-066's clDice centerline-only reference, and it remains below ABI-068's capped aggregate/source-balanced reference.

The result suggests the extra Line Target auxiliary head is not harmful enough to be a candidate bug, but it also does not add useful new information to the clDice branch. It trades ABI-066's stronger precision/connectivity and Google Dice for a small recall gain and a slightly larger positive mask area. That is not a compelling continuation direction when ABI-066 already occupies the precision/connectivity reference role and ABI-068 remains the aggregate-Dice reference.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-114 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-114. Stop this exact BCE-Dice-clDice plus equal-weight Line and Centerline Target auxiliary branch. Do not request whole-validation diagnostics for ABI-114 ahead of ABI-068 or ABI-066, because it did not improve the aggregate-Dice reference or the precision/connectivity reference.

Retain ABI-068 as the local aggregate-Dice reference and ABI-066 as the precision/connectivity reference for the frequency-gated line U-Net family. The next useful step should broaden beyond small auxiliary-head combinations around this architecture, preferably toward a materially different calibration, false-positive suppression, source-robustness, loss/data-policy, or thin-line continuity mechanism that remains inside the Candidate Experiment Contract.

## Artifact references

- `run_20260830_225952_22da29/outputs/best_metrics.json`
- `run_20260830_225952_22da29/outputs/final_metrics.json`
- `run_20260830_225952_22da29/outputs/metrics.jsonl`
- `run_20260830_225952_22da29/outputs/resource_profile.json`
- `run_20260830_225952_22da29/outputs/model_summary.json`
- `run_20260830_225952_22da29/outputs/prediction_samples/samples.json`
- `run_20260830_225952_22da29/resolved_manifest.yaml`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260830_115800_4a2363/outputs/best_metrics.json`
- `run_20260830_091941_139456/outputs/best_metrics.json`
- `run_20260830_110428_804d89/outputs/best_metrics.json`
