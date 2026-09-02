# Full-spectral BTD ConvNeXt U-Net ultra-stable repair

research-figures: []

## Scope

This note records ABI-102 after Run `run_20260830_070308_aeffc6` completed.

Source Runs:

- ABI-101 ConvNeXt-style U-Net non-finite scout: `run_20260830_065055_ef616d`
- ABI-102 ConvNeXt-style U-Net ultra-stable repair: `run_20260830_070308_aeffc6`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-085 low-learning-rate frequency-gated focal-Tversky reference: `run_20260829_181201_01c5e7`
- ABI-095 large-kernel line-context ultra-stable repair reference: `run_20260830_012033_a62afb`
- ABI-098 dense-detail U-Net scout reference: `run_20260830_040621_bb9ebc`
- ABI-100 deterministic-shuffle clDice reference: `run_20260830_055047_fb5c2f`

ABI-102 repaired ABI-101's Harness-recorded `candidate_bug` non-finite gradients in `front_end.learned_mixer.0.weight`. It preserved the ConvNeXt-style depthwise large-kernel U-Net scout idea while replacing the learned front-end mixer with deterministic bounded normalized ABI channels plus deterministic ABI-channel-derived thermal BTD planes, adding bounded internal activations, and lowering AdamW learning rate to `0.00005`. It retained provider-approved `abi_16ch` input, trusted `focal_tversky`, trusted `random_mirroring`, provider-owned `combined_source_balanced` traversal, batch size 4, 12 epochs, constant LR, disabled early stopping, and a provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped repair/scout evidence rather than full-data promotion evidence.

## ABI-102 implementation and resource observation

ABI-102 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI tensors and BTD features derived from approved ABI channels. It did not introduce candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.

Model summary reported 8,720,210 parameters against the 25,000,000-parameter smoke ceiling. The model summary confirmed GOES ABI channels 1-16 only, forbidden longitude/latitude source channels excluded, and outputs `mask_logits` plus `centerline_logits`. The Run completed at batch size 4 on the A100 with 1,993.4 seconds total wall time, 809.2 seconds training wall time, 1,182.3 seconds validation wall time, 8,371,830,784 bytes peak CUDA reserved, and no terminal execution failure. The repair therefore solved the ABI-101 terminal numerical issue for this exact branch.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260829_181201_01c5e7` | ABI-085 | ABI-068 branch, low LR focal-Tversky | 12 | 0.3826 | 0.3733 | 0.4059 | 0.3693 | 0.3968 | 0.3698 | 0.00389 |
| `run_20260830_012033_a62afb` | ABI-095 | ultra-stable large-kernel line-context repair | 12 | 0.2642 | 0.2655 | 0.2614 | 0.2243 | 0.3214 | 0.1347 | 0.00519 |
| `run_20260830_040621_bb9ebc` | ABI-098 | dense-detail U-Net scout | 12 | 0.3229 | 0.3160 | 0.3393 | 0.2577 | 0.4322 | 0.1777 | 0.00608 |
| `run_20260830_055047_fb5c2f` | ABI-100 | deterministic-shuffle clDice follow-up | 10 | 0.3674 | 0.3508 | 0.4089 | 0.4321 | 0.3195 | 0.4411 | 0.00268 |
| `run_20260830_070308_aeffc6` | ABI-102 | ultra-stable ConvNeXt U-Net repair | 10 | 0.1952 | 0.2033 | 0.1796 | 0.1482 | 0.2860 | 0.0976 | 0.00699 |

ABI-102 did not satisfy the useful scout criteria from its proposal. Relative to ABI-068, aggregate filtered Dice fell by about -0.2011, MIT by -0.1853, Google by -0.2365, filtered precision by -0.2510, filtered recall by -0.1076, and filtered connectivity by -0.2925, while filtered predicted-positive fraction nearly doubled. Relative to ABI-095, which used a different ultra-stable deterministic raw+BTD repair pattern, ABI-102 was also lower on aggregate Dice, both Dataset Sources, precision, recall, connectivity, and positive-area discipline. The repair therefore provides terminalization evidence but not evidence that the ConvNeXt-style branch improves the current line-sensitive references.

## ABI-102 trajectory

ABI-102 trained finitely and avoided all-negative/all-positive aggregate collapse, but the validation trajectory remained far below the local family references. Filtered Dice by epoch was 0.0225, 0.0610, 0.0989, 0.0945, 0.1218, 0.1332, 0.1284, 0.1307, 0.1592, 0.1952, 0.1689, and 0.1928. The selected checkpoint was epoch 10; the final checkpoint partially recovered after epoch 11 but did not exceed the selected checkpoint.

The selected checkpoint had filtered precision 0.1482, filtered recall 0.2860, filtered connectivity 0.0976, filtered predicted-positive fraction 0.00699, MIT filtered Dice 0.2033, and Google filtered Dice 0.1796. The final checkpoint remained similar: filtered Dice 0.1928, precision 0.1361, recall 0.3306, connectivity 0.0907, filtered predicted-positive fraction 0.00880, MIT filtered Dice 0.2018, and Google filtered Dice 0.1754. This indicates a low-precision, low-connectivity regime rather than a late-improving branch approaching the frequency-gated references.

Raw-to-filtered differences were modest at the final epoch: raw Dice 0.1975 versus filtered Dice 0.1928, and raw predicted-positive fraction 0.00931 versus filtered 0.00880. The result is therefore not rescued by provider-owned Artifact Filters. The fixed first-four retained prediction samples all had near-zero per-sample Dice in `outputs/prediction_samples/samples.json`; because prediction retention is fixed `first_n`, these are bounded artifacts and not representative qualitative evidence.

## Interpretation

Classify ABI-102 as a successful numerical repair but negative capped scientific evidence for the exact ultra-stable ConvNeXt U-Net branch. It achieved the minimum repair objective of finite completion after ABI-101's non-finite learned-mixer failure, but it fell below the proposal's hard-stop floors: aggregate filtered Dice was below 0.35, both Dataset Sources were below about 0.32 filtered Dice, and the branch did not show a compensating connectivity, precision, or positive-area advantage.

The likely research implication is that simply replacing learned spectral mixing with bounded deterministic raw+BTD features and lowering LR can terminalize unstable modern-block scouts, but for this ConvNeXt shape it underpowered or miscalibrated the segmentation branch. This does not weaken ABI-068/066; those remain the capped frequency-gated references. It also does not justify additional minor stability-only ConvNeXt tweaks without a materially different mechanism for preserving thin-line evidence and threshold discipline.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-102 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-102. Do not repeat the exact ConvNeXt-style U-Net ultra-stable branch with another small stability, clamp, or learning-rate-only change. No whole-validation failure-bucket evaluation is warranted for ABI-102 ahead of stronger capped references, because the aggregate and both source-specific filtered Dice are far below the current family baselines and the result lacks a distinctive precision/connectivity strength.

A useful next hypothesis should broaden away from ConvNeXt stability repair and toward a different contract-compliant architecture or policy mechanism for line continuity and threshold calibration. Candidate code should continue to leave thresholding, Artifact Filters, data loading, sampling implementation, augmentation implementation, target derivation, losses, metrics, resource placement, and lifecycle behavior to the provider/Harness.

## Artifact references

- `run_20260830_070308_aeffc6/outputs/best_metrics.json`
- `run_20260830_070308_aeffc6/outputs/final_metrics.json`
- `run_20260830_070308_aeffc6/outputs/metrics.jsonl`
- `run_20260830_070308_aeffc6/outputs/resource_profile.json`
- `run_20260830_070308_aeffc6/outputs/model_summary.json`
- `run_20260830_070308_aeffc6/outputs/prediction_samples/samples.json`
- `run_20260830_065055_ef616d/outputs/logs/training.log`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260829_181201_01c5e7/outputs/best_metrics.json`
- `run_20260830_012033_a62afb/outputs/best_metrics.json`
- `run_20260830_040621_bb9ebc/outputs/best_metrics.json`
- `run_20260830_055047_fb5c2f/outputs/best_metrics.json`
