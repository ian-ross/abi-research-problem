# Full-spectral BTD directional-top-hat U-Net follow-up

research-figures: []

## Scope

This note records ABI-117 after Run `run_20260831_015043_971dc3` completed.

Source Runs:

- ABI-117 directional-top-hat line U-Net continuation: `run_20260831_015043_971dc3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-105 conservative-skip focal-Tversky continuation: `run_20260830_091941_139456`
- ABI-114 clDice line+centerline auxiliary continuation: `run_20260830_225952_22da29`
- ABI-116 scale-selective ridge-gate continuation: `run_20260831_004912_1df8c4`

ABI-117 was a family-development continuation within the full-spectral BTD frequency-gated line U-Net branch. It retained provider-approved `abi_16ch` input, deterministic thermal BTD features derived only from GOES ABI channels 1-16, trusted provider-owned `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.

The controlled architecture change was moving oriented residual evidence to the front end through a `DirectionalTopHatStem` that fuses raw, local-detail, broad-context, horizontal-top-hat, and vertical-top-hat projections before the encoder. The hypothesis was that earlier oriented residual evidence would reduce diffuse clutter without acting as a late suppressive head or candidate-owned Artifact Filter surrogate. This is capped representative family-development evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-117 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI Channel Input and BTD combinations derived from approved ABI channels. It did not introduce candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: focal_tversky`, and auxiliary output `centerline_logits` with trusted `weighted_bce` weight 0.02. `outputs/model_summary.json` reported 12,392,041 parameters against the 25,000,000-parameter smoke ceiling.

The Run completed at batch size 4 on the A100 with 2,963.1 seconds total wall time, 1,519.6 seconds training wall time, 1,441.5 seconds validation wall time, 10,890,510,336 bytes peak CUDA reserved, and no terminal execution failure. The selected best-validation checkpoint was epoch 9.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, centerline aux | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | BCE-Dice-clDice precision/connectivity reference | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260830_091941_139456` | ABI-105 | conservative non-amplifying skip gates | 12 | 0.3831 | 0.3820 | 0.3857 | 0.3344 | 0.4484 | 0.2520 | 0.00486 |
| `run_20260830_225952_22da29` | ABI-114 | clDice with line+centerline auxiliary heads | 12 | 0.3806 | 0.3635 | 0.4229 | 0.4160 | 0.3508 | 0.4405 | 0.00306 |
| `run_20260831_004912_1df8c4` | ABI-116 | scale-selective ridge gate | 12 | 0.3729 | 0.3681 | 0.3836 | 0.3248 | 0.4378 | 0.2225 | 0.00488 |
| `run_20260831_015043_971dc3` | ABI-117 | stem-level directional top-hat residuals | 9 | 0.3793 | 0.3717 | 0.3978 | 0.3681 | 0.3912 | 0.2693 | 0.00385 |

ABI-117 did not meet its preregistered useful-continuation criteria. Relative to ABI-068, aggregate filtered Dice decreased from 0.3964 to 0.3793 (-0.0171), MIT filtered Dice decreased from 0.3886 to 0.3717 (-0.0169), Google filtered Dice decreased from 0.4161 to 0.3978 (-0.0183), filtered precision decreased from 0.3992 to 0.3681 (-0.0311), filtered recall was essentially tied but slightly lower (0.3936 to 0.3912, -0.0024), filtered connectivity decreased from 0.3900 to 0.2693 (-0.1207), and filtered predicted-positive fraction increased from 0.00357 to 0.00385.

Relative to ABI-066, ABI-117 had higher MIT filtered Dice (+0.0079) and recall (+0.0545), but lower aggregate filtered Dice (-0.0032), lower Google filtered Dice (-0.0314), lower precision (-0.0746), lower connectivity (-0.2038), and a larger predicted-positive fraction. It therefore does not challenge ABI-066's precision/connectivity reference role.

Relative to the latest local ridge/detail branch, ABI-117 improved over ABI-116 on aggregate filtered Dice (+0.0064), MIT filtered Dice (+0.0036), Google filtered Dice (+0.0142), precision (+0.0433), connectivity (+0.0467), and predicted-positive discipline, while losing recall (-0.0465). This suggests moving the oriented mechanism earlier is cleaner than the ABI-116 late ridge gate, but it remains below the ABI-068/066 references and below ABI-114's precision/connectivity profile.

## ABI-117 trajectory

ABI-117 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.2179, 0.2630, 0.3169, 0.2856, 0.2781, 0.3119, 0.3389, 0.3245, 0.3793, 0.3590, 0.3202, and 0.3671. The selected checkpoint was epoch 9; validation quality then declined at epochs 10 and 11 and partially recovered by epoch 12 without matching the selected checkpoint.

At the selected checkpoint, raw Dice was 0.3921 and filtered Dice was 0.3793. Filtered precision was 0.3681, filtered recall 0.3912, filtered connectivity 0.2693, and filtered predicted-positive fraction 0.00385. Source-stratified filtered Dice was 0.3717 MIT and 0.3978 Google. The source split stayed non-catastrophic: both Dataset Sources exceeded 0.36 filtered Dice, with Google more recall-forward (precision 0.3449, recall 0.4698) and MIT more balanced but lower-recall (precision 0.3793, recall 0.3644).

Raw-to-filtered differences were modest: raw Dice 0.3921 versus filtered Dice 0.3793, and raw predicted-positive fraction 0.00411 versus filtered 0.00385. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` are bounded artifacts under the Harness-owned `first_n` retention policy and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-117 as finite, resource-feasible, non-collapsed, but negative-to-mixed capped family-development evidence for this exact directional-top-hat branch. It is cleaner than ABI-116's late scale-selective ridge gate and avoids source-catastrophic behavior, but it does not recover the intended precision/connectivity gains relative to ABI-068 and does not create a better precision/connectivity operating point than ABI-066 or ABI-114.

The main failure mode is not optimization collapse: the model found a plausible, source-balanced checkpoint and the selected epoch was within 0.0032 filtered Dice of ABI-066. The problem is that the stem-level top-hat evidence did not improve the secondary metrics that justified the branch. Its connectivity remains much lower than ABI-068/066/114, and the final epochs show unstable calibration with a late shift toward larger positive area and lower precision.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-117 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-117. Do not request whole-validation diagnostics for ABI-117 ahead of stronger ABI-068, ABI-066, or ABI-114 references, because it did not improve aggregate Dice, precision/connectivity, or positive-area discipline relative to those references.

Stop this exact directional-top-hat branch. Retain ABI-068 as the local aggregate-Dice reference, ABI-066 as the precision/connectivity reference, and ABI-114 as a recent clDice line+centerline auxiliary precision/connectivity variant. The next useful hypothesis should broaden away from additional oriented/ridge/detail residual variants around the ABI-068 backbone and toward a materially different contract-compliant axis, such as a different architecture family, a trusted loss/auxiliary-target policy comparison, calibration-oriented architecture, or source-robustness mechanism that leaves data loading, split logic, sampling implementation, augmentation implementation, losses, metrics, Artifact Filters, postprocessing, resource placement, and lifecycle under provider/Harness ownership.

## Artifact references

- `run_20260831_015043_971dc3/outputs/best_metrics.json`
- `run_20260831_015043_971dc3/outputs/final_metrics.json`
- `run_20260831_015043_971dc3/outputs/metrics.jsonl`
- `run_20260831_015043_971dc3/outputs/resource_profile.json`
- `run_20260831_015043_971dc3/outputs/model_summary.json`
- `run_20260831_015043_971dc3/outputs/prediction_samples/samples.json`
- `run_20260831_015043_971dc3/resolved_manifest.yaml`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260830_091941_139456/outputs/best_metrics.json`
- `run_20260830_225952_22da29/outputs/best_metrics.json`
- `run_20260831_004912_1df8c4/outputs/best_metrics.json`
