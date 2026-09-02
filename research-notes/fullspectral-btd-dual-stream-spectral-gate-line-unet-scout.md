# Full-spectral BTD dual-stream spectral-gate line U-Net scout

research-figures: []

## Scope

This note records ABI-103 after Run `run_20260830_074456_5e0e5c` completed.

Source Runs:

- ABI-103 dual-stream spectral-gate line U-Net scout: `run_20260830_074456_5e0e5c`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-085 low-learning-rate frequency-gated focal-Tversky reference: `run_20260829_181201_01c5e7`
- ABI-097 negative-bias frequency-gated focal-Tversky reference: `run_20260830_030927_4f7d3d`
- ABI-100 deterministic-shuffle clDice reference: `run_20260830_055047_fb5c2f`
- ABI-102 ultra-stable ConvNeXt U-Net repair reference: `run_20260830_070308_aeffc6`

ABI-103 was a family scout for a dual-stream spectral-gate line U-Net. It separated provider-approved reflective ABI channels, thermal ABI channels, and ABI-channel-derived thermal BTD planes into separate stems before bounded cross-stream gating, then fused them into a compact line-aware U-Net. The intent was to test whether spectral specialization before spatial fusion could improve source-robust threshold discipline and thin-line evidence without candidate-owned thresholding, postprocessing, Artifact Filters, losses, metrics, sampling, or data loading.

The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, provider-approved `abi_16ch` input, trusted `focal_tversky`, trusted `random_mirroring`, provider-owned `combined_source_balanced` traversal, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant LR, disabled early stopping, and a provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. This is capped scout evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-103 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI tensors and deterministic BTD features derived from approved ABI channels. It did not introduce candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.

`outputs/model_summary.json` reported 13,189,885 parameters against the 25,000,000-parameter smoke ceiling. The model summary confirmed GOES ABI channels 1-16 only, forbidden longitude/latitude source channels excluded, and outputs `mask_logits` plus `centerline_logits`. The Run completed at batch size 4 on the A100 with 2,268.3 seconds total wall time, 1,016.4 seconds training wall time, 1,249.8 seconds validation wall time, 10,122,952,704 bytes peak CUDA reserved, and no terminal execution failure. The scout was therefore resource-feasible under the current capped sequential policy.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260829_181201_01c5e7` | ABI-085 | ABI-068 branch, low LR focal-Tversky | 12 | 0.3826 | 0.3733 | 0.4059 | 0.3693 | 0.3968 | 0.3698 | 0.00389 |
| `run_20260830_030927_4f7d3d` | ABI-097 | ABI-068 branch, negative logit bias | 12 | 0.3737 | 0.3737 | 0.3737 | 0.3231 | 0.4431 | 0.2614 | 0.00497 |
| `run_20260830_055047_fb5c2f` | ABI-100 | deterministic-shuffle clDice follow-up | 10 | 0.3674 | 0.3508 | 0.4089 | 0.4321 | 0.3195 | 0.4411 | 0.00268 |
| `run_20260830_070308_aeffc6` | ABI-102 | ultra-stable ConvNeXt U-Net repair | 10 | 0.1952 | 0.2033 | 0.1796 | 0.1482 | 0.2860 | 0.0976 | 0.00699 |
| `run_20260830_074456_5e0e5c` | ABI-103 | dual-stream spectral-gate line U-Net scout | 12 | 0.3305 | 0.3248 | 0.3427 | 0.2715 | 0.4225 | 0.1742 | 0.00564 |

ABI-103 did not reach the primary local targets. Relative to ABI-068, aggregate filtered Dice was lower by about 0.0658, MIT filtered Dice by 0.0638, Google filtered Dice by 0.0734, filtered precision by 0.1277, and filtered connectivity by 0.2158. ABI-103 did improve filtered recall over ABI-068 by about 0.0289, but the gain came with a larger filtered predicted-positive fraction and much weaker precision/connectivity.

Relative to ABI-066, ABI-103 was lower in aggregate filtered Dice by about 0.0520, lower in precision by 0.1713, and lower in connectivity by 0.2989, while recall was higher by about 0.0857. Relative to ABI-097, ABI-103 had a more balanced MIT/Google split and lower predicted-positive area, but lower aggregate Dice and substantially weaker precision/connectivity. It was much stronger than the ABI-102 ConvNeXt repair, so the dual-stream scout is not in the same catastrophic low-Dice regime, but it also does not supply a distinctive secondary-metric advantage over the established frequency-gated references.

## ABI-103 trajectory

ABI-103 trained finitely and avoided all-negative/all-positive aggregate collapse. Filtered Dice by epoch was 0.0849, 0.0827, 0.1522, 0.2331, 0.2519, 0.2717, 0.1815, 0.2929, 0.2793, 0.1393, 0.2282, and 0.3305. The selected checkpoint was the final epoch 12, so the run has late improvement rather than a clear plateau. Training loss declined from 0.9583 at epoch 1 to 0.8689 at epoch 12.

The final/best checkpoint had filtered Dice 0.3305, filtered precision 0.2715, filtered recall 0.4225, filtered connectivity 0.1742, and filtered predicted-positive fraction 0.00564. Source-stratified metrics were reasonably balanced but both below the strongest references: MIT filtered Dice 0.3248 with recall 0.3796 and Google filtered Dice 0.3427 with recall 0.5479. The Google recall advantage did not translate into high precision or connectivity.

Raw-to-filtered differences were modest at the final epoch: raw Dice 0.3375 versus filtered Dice 0.3305, and raw predicted-positive fraction 0.00603 versus filtered 0.00564. The result is not primarily rescued or harmed by provider-owned Artifact Filters. The fixed first-four retained prediction samples all had near-zero per-sample Dice in `outputs/prediction_samples/samples.json`; because prediction retention is fixed `first_n`, these are bounded artifacts and not representative qualitative evidence.

## Interpretation

Classify ABI-103 as finite, resource-feasible, and mixed but below-target capped scout evidence for the exact dual-stream spectral-gate design. It missed the proposal's strong scout criteria: it was not within 0.015 filtered Dice of ABI-068, did not match ABI-066, did not put both Dataset Sources above 0.35 filtered Dice, and did not recover ABI-066-like connectivity or precision. It also stayed above the hard-stop aggregate floor of 0.30, kept both Dataset Sources above 0.25, avoided collapse, and selected the final epoch as best, so the broader spectral-specialization idea is not disproven by this single scout.

The main failure mode is a recall-favoring but low-precision, low-connectivity regime. The dual-stream gates may preserve more candidate contrail evidence than the negative modern-block repairs, but the present fusion/head does not enforce enough line coherence or threshold discipline. A bounded follow-up would need a materially targeted precision/connectivity mechanism, not just another minor gate or learning-rate change. Examples that remain inside the contract include reusing spectral specialization with a stronger line-consensus decoder, adding a low-weight boundary auxiliary head if the next hypothesis specifically targets edge clutter, or lowering the focal-Tversky branch's positive-area tendency through architecture initialization rather than candidate-owned thresholding.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-103 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-103 and do not request whole-validation diagnostics for this exact checkpoint ahead of ABI-068/066-style references. Do not repeat the exact dual-stream spectral-gate line U-Net without a stronger precision/connectivity modification, because the current scout's recall benefit is outweighed by lower Dice, precision, and connectivity.

A future hypothesis may still develop the spectral-specialization frontier if it explicitly targets the observed low-connectivity and positive-area failure mode while preserving provider/Harness ownership of thresholding, Artifact Filters, data loading, sampling implementation, augmentation implementation, target derivation, losses, metrics, resource placement, and lifecycle behavior.

## Artifact references

- `run_20260830_074456_5e0e5c/outputs/best_metrics.json`
- `run_20260830_074456_5e0e5c/outputs/final_metrics.json`
- `run_20260830_074456_5e0e5c/outputs/metrics.jsonl`
- `run_20260830_074456_5e0e5c/outputs/resource_profile.json`
- `run_20260830_074456_5e0e5c/outputs/model_summary.json`
- `run_20260830_074456_5e0e5c/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260829_181201_01c5e7/outputs/best_metrics.json`
- `run_20260830_030927_4f7d3d/outputs/best_metrics.json`
- `run_20260830_055047_fb5c2f/outputs/best_metrics.json`
- `run_20260830_070308_aeffc6/outputs/best_metrics.json`
