# Full-spectral BTD coarse-to-fine U-Net focal-Tversky follow-up

research-figures: []

## Scope

This note records ABI-065, the controlled focal-Tversky follow-up to the ABI-064 full-spectral BTD coarse-to-fine U-Net scout, after Run `run_20260827_221136_3d2736` completed.

Source Runs:

- ABI-064 coarse-to-fine U-Net scout with trusted `bce_dice_cldice` + provider-derived `centerline` auxiliary target weight 0.02: `run_20260827_212811_0e34e2`
- ABI-065 coarse-to-fine U-Net continuation with trusted `focal_tversky` + provider-derived `centerline` auxiliary target weight 0.02: `run_20260827_221136_3d2736`
- ABI-061 oriented-context high-resolution BTD line U-Net with trusted `focal_tversky` + provider-derived `centerline` auxiliary target weight 0.02: `run_20260827_194725_c1d6c6`
- ABI-058 oriented-context high-resolution BTD line U-Net local reference with trusted `bce_dice_cldice` + provider-derived `centerline` auxiliary target weight 0.02: `run_20260827_171331_c1769a`

All trained comparison Runs used provider-approved `abi_16ch` inputs, approved thermal BTD features derived only from ABI channels, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped feasibility results, not full-data promotion evidence.

## ABI-065 implementation and resource observation

ABI-065 intentionally kept the ABI-064 architecture unchanged and changed only the trusted primary loss from `bce_dice_cldice` to `focal_tversky`. The model used normalized ABI channels 1-16, explicit thermal BTD planes derived from approved channels, a learned spectral mixer, a differentiable low-resolution coarse-prior branch, full-resolution gated decoder/refiner features, primary `mask_logits`, and provider-derived `centerline_logits`.

The Run stayed inside the Candidate Experiment Contract: no longitude/latitude inputs, no reconstructed coordinate inputs, no candidate-owned data loading, no custom loss or target derivation, no augmentation implementation, no metrics, no thresholding, no Artifact Filters, no postprocessing, no network access, and no pretrained weights.

The model summary reported 14,548,983 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 2,032.8 seconds wall time, 7.03 GiB peak CUDA allocated, 8.71 GiB peak CUDA reserved, and no terminal execution failure.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_171331_c1769a` | ABI-058 | oriented full-resolution context, clDice + centerline aux | 10 | 0.3248 | 0.3139 | 0.3497 | 0.3144 | 0.3360 | 0.2335 | 0.00387 |
| `run_20260827_194725_c1d6c6` | ABI-061 | focal-Tversky on ABI-058 architecture + centerline aux | 12 | 0.3221 | 0.2954 | 0.3896 | 0.3515 | 0.2973 | 0.2834 | 0.00306 |
| `run_20260827_212811_0e34e2` | ABI-064 | coarse soft-prior gating, clDice + centerline aux | 11 | 0.3255 | 0.3213 | 0.3348 | 0.3016 | 0.3535 | 0.1972 | 0.00425 |
| `run_20260827_221136_3d2736` | ABI-065 | focal-Tversky on ABI-064 architecture + centerline aux | 10 | 0.3132 | 0.2976 | 0.3478 | 0.3039 | 0.3230 | 0.1967 | 0.00385 |

ABI-065 did not match ABI-064 by the primary capped selection metric: best `val/filtered_dice` was 0.3132, trailing ABI-064 by 0.0124. It also did not reproduce ABI-061's strong focal-Tversky precision/connectivity shift. Relative to ABI-064, ABI-065 modestly reduced the best-checkpoint filtered predicted-positive fraction from 0.00425 to 0.00385 and slightly improved Google filtered Dice from 0.3348 to 0.3478, but it lost MIT filtered Dice, aggregate recall, and aggregate Dice while leaving precision/connectivity essentially flat.

## ABI-065 trajectory

ABI-065 trained finitely and non-degenerately. Filtered Dice rose from 0.0823 at epoch 1 to 0.1806 at epoch 3, then improved more gradually through 0.2343 at epoch 5 and 0.2590 at epoch 8. Epoch 9 dipped to 0.2415, followed by the best checkpoint at epoch 10 with filtered Dice 0.3132. The final two epochs were unstable: epoch 11 fell to 0.2854 and epoch 12 recovered only to 0.3015.

The final checkpoint was more recall-heavy than the selected checkpoint, with filtered recall 0.3704 and predicted-positive fraction 0.00528, but lower precision 0.2541, lower connectivity 0.1411, and lower filtered Dice 0.3015. This weakens the hypothesis that focal-Tversky would steer the coarse-prior branch toward a cleaner low-burden operating point under the current 12-epoch cap.

The fixed first-four prediction samples all have near-zero sample Dice values, so they should not be treated as representative qualitative evidence.

## Interpretation

ABI-065 is finite, resource-safe, and source-informative, but its controlled loss change is negative/mixed evidence for this exact focal-Tversky coarse-to-fine branch. It avoided prediction collapse and kept both source Dice values above 0.25, so it is not a hard architecture-family failure. However, it missed the proposal's stronger continuation criteria: it did not match or exceed ABI-064's capped filtered Dice, did not improve precision or connectivity, and did not reduce the predicted-positive burden enough to compensate for the loss in MIT Dice and aggregate recall.

The focal-Tversky pattern is now architecture-dependent but not clearly beneficial. On ABI-061, focal-Tversky produced a distinct precision/connectivity and Google-skewed profile. On ABI-065, it produced only a smaller Google gain and lower predicted-positive fraction while removing ABI-064's source-balanced aggregate advantage. This suggests the ABI-064 coarse prior's useful signal came mainly from the architecture under clDice/centerline supervision, not from focal-Tversky loss selection.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context at filtered Dice 0.3873. ABI-065 is not promotion-ready and must not be interpreted as full-data evidence.

## Decision

Classify ABI-065 as `bad_research_result` / negative mixed capped family-development evidence for changing ABI-064's primary loss to trusted `focal_tversky`. Do not promote ABI-065 and do not repeat this exact focal-Tversky coarse-to-fine branch unchanged.

Retain ABI-064 as the local coarse-to-fine reference because it remains finite, source-balanced at its best checkpoint, and the best completed capped Run by `val/filtered_dice` in the observed history. A useful next step is a bounded whole-validation diagnostic for ABI-064 if the campaign wants to test whether its capped source balance and coarse-prior false-positive behavior survive the full Working Validation Split. If the campaign instead continues with new Candidates, broaden away from simple focal-Tversky loss substitution toward a materially different topology/connectivity mechanism or another trusted policy axis that can reduce false positives without sacrificing MIT recall.

## Artifact references

- `run_20260827_221136_3d2736/outputs/best_metrics.json`
- `run_20260827_221136_3d2736/outputs/final_metrics.json`
- `run_20260827_221136_3d2736/outputs/metrics.jsonl`
- `run_20260827_221136_3d2736/outputs/resource_profile.json`
- `run_20260827_221136_3d2736/outputs/model_summary.json`
- `run_20260827_221136_3d2736/outputs/prediction_samples/samples.json`
- `run_20260827_212811_0e34e2/outputs/best_metrics.json`
- `run_20260827_212811_0e34e2/outputs/final_metrics.json`
- `run_20260827_194725_c1d6c6/outputs/best_metrics.json`
- `run_20260827_171331_c1769a/outputs/best_metrics.json`
