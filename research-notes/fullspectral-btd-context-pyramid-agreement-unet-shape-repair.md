# Full-spectral BTD context-pyramid agreement U-Net shape repair

research-figures: []

## Scope

This note records ABI-119 after Run `run_20260831_025229_09ef74` completed.

Source Runs:

- ABI-119 context-pyramid agreement U-Net shape repair: `run_20260831_025229_09ef74`
- ABI-118 original context-pyramid agreement U-Net scout smoke failure: `run_20260831_024833_2d90b0`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-114 clDice line+centerline auxiliary precision/connectivity context: `run_20260830_225952_22da29`
- ABI-116 scale-selective ridge-gate continuation context: `run_20260831_004912_1df8c4`
- ABI-117 directional-top-hat line U-Net continuation context: `run_20260831_015043_971dc3`

ABI-119 was a Repair Candidate for ABI-118. ABI-118 failed smoke with a candidate-bug decoder spatial mismatch (`32` vs `64` at the first FPN lateral addition). ABI-119 preserved the original context-pyramid family-scout hypothesis and comparison target while fixing only the FPN spatial alignment by upsampling the projected low-resolution neck tensor to the `enc2` lateral feature size before the first additive merge.

The branch tested whether low-frequency patch/cloud context plus local/context feature agreement could calibrate high-resolution thin-line evidence and reduce diffuse clutter without candidate-owned thresholding, postprocessing, Artifact Filters, sampling, target derivation, losses, metrics, resource placement, or lifecycle behavior. This is capped representative feasibility evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-119 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved `abi_16ch` ABI Channel Input and deterministic BTD combinations derived from GOES ABI channels 1-16. It did not introduce longitude, latitude, reconstructed coordinates, candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or lifecycle behavior.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: focal_tversky`, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and one provider-derived Centerline Target auxiliary output `centerline_logits` with trusted `weighted_bce` weight 0.02. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records.

`outputs/model_summary.json` reported 11,843,034 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 1,751.6 seconds total wall time, 639.4 seconds training wall time, 1,110.0 seconds validation wall time, 4,898,195,456 bytes peak CUDA allocated, 6,119,489,536 bytes peak CUDA reserved, and no terminal execution failure. The selected best-validation checkpoint was epoch 12.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, centerline aux | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | BCE-Dice-clDice precision/connectivity reference | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260830_225952_22da29` | ABI-114 | clDice with line+centerline auxiliary heads | 12 | 0.3806 | 0.3635 | 0.4229 | 0.4160 | 0.3508 | 0.4405 | 0.00306 |
| `run_20260831_004912_1df8c4` | ABI-116 | scale-selective ridge gate | 12 | 0.3729 | 0.3681 | 0.3836 | 0.3248 | 0.4378 | 0.2225 | 0.00488 |
| `run_20260831_015043_971dc3` | ABI-117 | stem-level directional top-hat residuals | 9 | 0.3793 | 0.3717 | 0.3978 | 0.3681 | 0.3912 | 0.2693 | 0.00385 |
| `run_20260831_025229_09ef74` | ABI-119 | context pyramid plus local/context agreement calibrator | 12 | 0.2869 | 0.2932 | 0.2748 | 0.2319 | 0.3761 | 0.1287 | 0.00588 |

ABI-119 did not meet its preregistered useful-continuation criteria. Relative to ABI-068, aggregate filtered Dice decreased from 0.3964 to 0.2869 (-0.1095), MIT filtered Dice decreased from 0.3886 to 0.2932 (-0.0954), Google filtered Dice decreased from 0.4161 to 0.2748 (-0.1413), filtered precision decreased from 0.3992 to 0.2319 (-0.1673), filtered recall decreased from 0.3936 to 0.3761 (-0.0175), filtered connectivity decreased from 0.3900 to 0.1287 (-0.2613), and filtered predicted-positive fraction increased from 0.00357 to 0.00588.

Relative to ABI-066, ABI-119 had higher filtered recall (+0.0394), but lower aggregate filtered Dice (-0.0956), lower MIT filtered Dice (-0.0706), lower Google filtered Dice (-0.1544), much lower precision (-0.2108), much lower connectivity (-0.3444), and a larger predicted-positive fraction. It therefore does not challenge ABI-066's precision/connectivity reference role.

ABI-119 also underperformed recent weaker context and ridge/detail variants. Relative to ABI-116, it lost aggregate filtered Dice (-0.0860), MIT filtered Dice (-0.0749), Google filtered Dice (-0.1088), precision (-0.0929), recall (-0.0616), and connectivity (-0.0938) while increasing positive area. Relative to ABI-117, it lost aggregate filtered Dice (-0.0924), MIT filtered Dice (-0.0785), Google filtered Dice (-0.1230), precision (-0.1362), recall (-0.0151), and connectivity (-0.1406) while again increasing positive area.

## ABI-119 trajectory

ABI-119 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.0654, 0.0844, 0.0967, 0.1178, 0.2068, 0.2124, 0.2323, 0.2835, 0.2478, 0.2247, 0.2429, and 0.2869. The selected checkpoint was the final epoch, so the repair was still improving after the mid-run regression, but it remained far below the branch's comparison targets and below the recent negative-to-mixed local variants.

At the selected checkpoint, raw Dice was 0.2942 and filtered Dice was 0.2869. Filtered precision was 0.2319, filtered recall 0.3761, filtered connectivity 0.1287, and filtered predicted-positive fraction 0.00588. Source-stratified filtered Dice was 0.2932 MIT and 0.2748 Google. Both Dataset Sources were finite and non-collapsed, but both were far below the `0.36` source-Dice continuation target. Google was especially recall-forward, with filtered precision 0.1920 and filtered recall 0.4829, while MIT had filtered precision 0.2579 and filtered recall 0.3396.

Raw-to-filtered differences were modest: raw Dice 0.2942 versus filtered Dice 0.2869, and raw predicted-positive fraction 0.00625 versus filtered 0.00588. This does not indicate primary Artifact Filter dependence; the failure mode is low precision/connectivity and excessive positive area before filtering. The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` all had near-zero per-sample Dice, but the retention policy is fixed `first_n`, so these bounded artifacts should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-119 as a successful candidate-bug repair in lifecycle terms but a bad research result for this exact context-pyramid agreement branch. The Run repaired the ABI-118 smoke-time FPN shape bug, stayed finite, completed within resource limits, and selected a late best epoch. However, the context-pyramid agreement calibrator did not deliver the intended source-robust precision, connectivity, or positive-area discipline. Instead, it produced the lowest aggregate/source Dice and connectivity among the compared recent branches, with elevated predicted-positive fraction and particularly poor Google precision.

The evidence is negative for this exact context-pyramid agreement formulation under the current trusted focal-Tversky, centerline-auxiliary, random-mirroring, constant-LR, representative-capped budget. Because this was a repaired family scout and the final epoch was still improving, the result is not proof that all scene-context architectures are exhausted. It is enough to stop this specific FPN context-pyramid plus local/context agreement-calibrator branch, and it argues against another immediate repair of ABI-118/119 unless an additional implementation defect is found.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-119 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-119. Do not request whole-validation diagnostics for ABI-119 ahead of stronger ABI-068, ABI-066, or ABI-114 references, because ABI-119 did not improve aggregate Dice, source-stratified Dice, precision/connectivity, recall, positive-area discipline, or any preregistered continuation criterion.

Stop the exact ABI-118/119 context-pyramid agreement branch. Retain ABI-068 as the local aggregate-Dice reference, ABI-066 as the precision/connectivity reference, and ABI-114 as a recent clDice line+centerline auxiliary precision/connectivity context. The next useful hypothesis should broaden away from FPN context-pyramid agreement calibration and additional high-resolution ridge/detail residual refiners around ABI-068, while remaining contract-compliant: for example, a materially different segmentation architecture family, a controlled trusted loss/auxiliary-target policy comparison, a calibration-oriented architecture that does not implement thresholding or postprocessing, or a source-robustness mechanism that leaves data loading, splits, sampling implementation, augmentation implementation, losses, metrics, Artifact Filters, postprocessing, resource placement, and lifecycle under provider/Harness ownership.

## Artifact references

- `run_20260831_025229_09ef74/outputs/best_metrics.json`
- `run_20260831_025229_09ef74/outputs/final_metrics.json`
- `run_20260831_025229_09ef74/outputs/metrics.jsonl`
- `run_20260831_025229_09ef74/outputs/resource_profile.json`
- `run_20260831_025229_09ef74/outputs/model_summary.json`
- `run_20260831_025229_09ef74/outputs/prediction_samples/samples.json`
- `run_20260831_025229_09ef74/resolved_manifest.yaml`
- `run_20260831_024833_2d90b0/outputs/logs/smoke_test.log`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260830_225952_22da29/outputs/best_metrics.json`
- `run_20260831_004912_1df8c4/outputs/best_metrics.json`
- `run_20260831_015043_971dc3/outputs/best_metrics.json`
