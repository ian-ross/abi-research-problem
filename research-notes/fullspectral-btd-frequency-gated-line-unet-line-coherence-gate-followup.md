# Full-spectral BTD frequency-gated line U-Net line-coherence-gate follow-up

research-figures: []

## Scope

This note records ABI-099 after Run `run_20260830_044731_a5c0bf` completed.

Source Runs:

- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-078 frequency-gated line U-Net BCE-Dice conservative operating-point reference: `run_20260828_094949_ad2af0`
- ABI-085 frequency-gated line U-Net lower-learning-rate focal-Tversky reference: `run_20260829_181201_01c5e7`
- ABI-097 frequency-gated line U-Net negative-bias focal-Tversky reference: `run_20260830_030927_4f7d3d`
- ABI-098 dense-detail U-Net negative scout context: `run_20260830_040621_bb9ebc`
- ABI-099 directional line-coherence-gate continuation: `run_20260830_044731_a5c0bf`

ABI-099 kept ABI-068's full-spectral ABI plus thermal BTD frequency-gated line U-Net setup and added a small directional line-coherence gate after final frequency-pyramid fusion. The intended effect was to favor elongated directional feature agreement over smoothed blob-like context, improving precision or connectivity without losing ABI-068's focal-Tversky recall.

The Run used provider-approved `abi_16ch` input only, trusted `focal_tversky` primary loss, trusted `combined_source_balanced` sampling, trusted `random_mirroring`, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, and a provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. It used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-development evidence rather than full-data promotion evidence.

## ABI-099 implementation and resource observation

ABI-099 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI tensors and BTD planes derived from approved ABI channels. It did not introduce candidate-owned data loading, split logic, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.

Model summary reported 12,515,420 parameters against the 25,000,000-parameter smoke ceiling. The model summary confirmed GOES ABI channels 1-16 only, with forbidden longitude/latitude source channels excluded, and outputs `mask_logits` plus `centerline_logits`. The Run completed at batch size 4 on the A100 with 3,289.6 seconds total wall time, 1,715.7 seconds training wall time, 1,571.8 seconds validation wall time, 12,423,528,448 bytes peak CUDA reserved, and no terminal execution failure. Resource behavior stayed within the 3,600-second Docker training timeout but is substantially heavier than compact frequency-gated variants.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, `focal_tversky` | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice` | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_094949_ad2af0` | ABI-078 | ABI-068 branch, `bce_dice` | 11 | 0.3816 | 0.3704 | 0.4093 | 0.4072 | 0.3590 | 0.3061 | 0.00320 |
| `run_20260829_181201_01c5e7` | ABI-085 | ABI-068 branch, lower learning rate 0.0001 | 12 | 0.3826 | 0.3733 | 0.4059 | 0.3693 | 0.3968 | 0.3698 | 0.00389 |
| `run_20260830_030927_4f7d3d` | ABI-097 | ABI-068 branch, negative output-bias initialization | 12 | 0.3737 | 0.3737 | 0.3737 | 0.3231 | 0.4431 | 0.2614 | 0.00497 |
| `run_20260830_040621_bb9ebc` | ABI-098 | dense-detail U-Net scout | 12 | 0.3229 | 0.3160 | 0.3393 | 0.2577 | 0.4322 | 0.1777 | 0.00608 |
| `run_20260830_044731_a5c0bf` | ABI-099 | ABI-068 branch plus directional line-coherence gate | 11 | 0.3401 | 0.3499 | 0.3187 | 0.2558 | 0.5074 | 0.1421 | 0.00719 |

ABI-099 did not meet the preregistered useful-continuation criteria. Relative to ABI-068, aggregate filtered Dice fell by about -0.0563, MIT filtered Dice by -0.0387, Google filtered Dice by -0.0974, filtered precision by -0.1434, and filtered connectivity by -0.2479. Filtered recall increased by +0.1138, but the filtered predicted-positive fraction doubled from 0.00357 to 0.00719.

Relative to ABI-066, ABI-099 lost about -0.0424 filtered Dice, -0.0139 MIT Dice, -0.1105 Google Dice, -0.1869 precision, and -0.3310 connectivity while predicting about 2.6x as many filtered-positive pixels by fraction. Relative to ABI-098, ABI-099 recovered +0.0172 aggregate filtered Dice and +0.0339 MIT Dice, but Google Dice remained lower, precision was essentially unchanged, connectivity worsened further, and positive area expanded again. The line-coherence gate therefore did not act as the intended precision/connectivity-preserving feature selector under the current focal-Tversky, centerline-auxiliary, constant-LR budget.

## ABI-099 trajectory

ABI-099 trained finitely and avoided terminal all-negative/all-positive collapse. Filtered Dice by epoch was 0.1842, 0.2698, 0.2350, 0.2741, 0.3215, 0.3094, 0.2713, 0.3276, 0.3365, 0.3340, 0.3401, and 0.3391. The selected checkpoint was epoch 11, with epoch 12 essentially tied, suggesting a plateau around 0.34 rather than a strong late-improving trajectory.

At the selected checkpoint, filtered precision was 0.2558, filtered recall 0.5074, filtered connectivity 0.1421, and filtered predicted-positive fraction 0.00719. The MIT/Google filtered Dice split was 0.3499/0.3187. Raw-to-filtered differences were modest: raw Dice 0.3488 versus filtered Dice 0.3401, and raw predicted-positive fraction 0.00766 versus filtered 0.00719. This points to an intrinsic low-precision, low-connectivity positive-area expansion at the trusted threshold rather than an Artifact Filter dependence issue.

The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` all had near-zero per-sample Dice. Because prediction retention is fixed `first_n`, these samples are bounded artifacts and not representative qualitative evidence; aggregate and source-stratified validation metrics carry this decision.

## Interpretation

Classify ABI-099 as finite, resource-feasible, non-collapsed, but negative capped family-development evidence for the exact directional line-coherence gate branch. The gate did not approach ABI-068 within 0.01, did not improve precision or connectivity, did not reduce predicted-positive burden, and left Google filtered Dice below the approximate 0.36 continuation floor. The branch's main effect appears to be recall-heavy positive expansion with especially poor connectivity, despite its directional-context intent.

This does not eliminate the broader full-spectral BTD frequency-gated family, where ABI-068 remains the local aggregate-Dice reference and ABI-066 remains the precision/connectivity reference. It does argue against repeating this line-coherence-gate mechanism unchanged or requesting whole-validation failure-bucket diagnostics for ABI-099 ahead of stronger branches.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-099 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-099. Do not repeat the directional line-coherence gate unchanged. Prefer the next hypothesis to broaden away from additive high-resolution/detail/coherence gates that have repeatedly expanded positive area, and toward a different contract-compliant mechanism for threshold discipline, calibrated precision, or source-robust line continuity. Any follow-up must continue leaving data loading, split logic, sampling implementation, augmentation implementation, losses, metrics, Artifact Filters, postprocessing, resource placement, and lifecycle under provider/Harness ownership.

## Artifact references

- `run_20260830_044731_a5c0bf/outputs/best_metrics.json`
- `run_20260830_044731_a5c0bf/outputs/final_metrics.json`
- `run_20260830_044731_a5c0bf/outputs/metrics.jsonl`
- `run_20260830_044731_a5c0bf/outputs/resource_profile.json`
- `run_20260830_044731_a5c0bf/outputs/model_summary.json`
- `run_20260830_044731_a5c0bf/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260828_094949_ad2af0/outputs/best_metrics.json`
- `run_20260829_181201_01c5e7/outputs/best_metrics.json`
- `run_20260830_030927_4f7d3d/outputs/best_metrics.json`
- `run_20260830_040621_bb9ebc/outputs/best_metrics.json`
