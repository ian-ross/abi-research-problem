# Full-spectral BTD frequency-gated line U-Net negative-bias follow-up

research-figures: []

## Scope

This note records ABI-097 after Run `run_20260830_030927_4f7d3d` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice and whole-validation reference: `run_20260828_010836_4ccc77`
- ABI-078 frequency-gated line U-Net BCE-Dice conservative operating-point reference: `run_20260828_094949_ad2af0`
- ABI-085 frequency-gated line U-Net low-learning-rate focal-Tversky reference: `run_20260829_181201_01c5e7`
- ABI-096 frequency-gated line U-Net deterministic-shuffle data-policy reference: `run_20260830_021504_c112f8`
- ABI-097 negative-bias focal-Tversky continuation: `run_20260830_030927_4f7d3d`

ABI-097 preserved the ABI-068 full-spectral BTD frequency-gated line U-Net architecture, provider-approved `abi_16ch` input, ABI-channel-derived thermal brightness-temperature-difference features, trusted `focal_tversky` primary loss, trusted `combined_source_balanced` sampling, trusted `random_mirroring`, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, and a provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. The controlled change was candidate-owned initialization of the trainable output-head biases: `mask_head.bias = -0.75` and `centerline_head.bias = -1.25`. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-development evidence rather than full-data promotion evidence.

## ABI-097 implementation and resource observation

ABI-097 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture and trainable initialization over provider-approved ABI tensors and BTD planes derived from approved ABI channels. It did not introduce candidate-owned data loading, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, pretrained weights, or longitude/latitude inputs.

Model summary reported 12,087,561 parameters against the 25,000,000-parameter smoke ceiling. The model summary confirmed provider-approved ABI channels 1-16 only, with forbidden longitude/latitude source channels excluded. The Run completed at batch size 4 on the A100 with 2,688.8 seconds wall time, 9,539,944,448 bytes peak CUDA reserved, and no terminal execution failure. Resource behavior remained within the recent ABI-068/085/096 frequency-gated envelope and the current 3,600-second Docker training timeout.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, `focal_tversky`, combined source-balanced | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, combined source-balanced | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_094949_ad2af0` | ABI-078 | ABI-068 branch, `bce_dice` | 11 | 0.3816 | 0.3704 | 0.4093 | 0.4072 | 0.3590 | 0.3061 | 0.00320 |
| `run_20260829_181201_01c5e7` | ABI-085 | ABI-068 branch, lower learning rate 0.0001 | 12 | 0.3826 | 0.3733 | 0.4059 | 0.3693 | 0.3968 | 0.3698 | 0.00389 |
| `run_20260830_021504_c112f8` | ABI-096 | ABI-068 branch, `deterministic_shuffle` sampling | 10 | 0.3628 | 0.3472 | 0.4024 | 0.4242 | 0.3169 | 0.4195 | 0.00271 |
| `run_20260830_030927_4f7d3d` | ABI-097 | ABI-068 branch, negative output-bias initialization | 12 | 0.3737 | 0.3737 | 0.3737 | 0.3231 | 0.4431 | 0.2614 | 0.00497 |

ABI-097 did not produce the intended conservative operating shift. Relative to ABI-068, aggregate filtered Dice fell by about -0.0226, Google filtered Dice fell by about -0.0424, filtered precision fell by about -0.0760, filtered connectivity fell by about -0.1286, and filtered predicted-positive fraction increased from 0.00357 to 0.00497. Recall increased by about +0.0495, but this was the opposite of the desired lower-clutter calibration effect. MIT filtered Dice fell by a smaller -0.0148 and remained source-balanced at 0.3737, but the Google-source drop removed the main usefulness case.

Relative to ABI-066, ABI-097 was lower on aggregate filtered Dice (-0.0088), Google filtered Dice (-0.0555), precision (-0.1196), connectivity (-0.2116), and positive-area discipline, while recall was higher (+0.1063). Relative to ABI-078 and ABI-085, ABI-097 again showed a recall-heavy, low-precision profile rather than a cleaner threshold-0.5 operating point. Relative to ABI-096, ABI-097 recovered some aggregate and MIT Dice, but lost ABI-096's precision/connectivity advantage and expanded predicted-positive area.

## ABI-097 trajectory

ABI-097 trained finitely and avoided terminal all-negative/all-positive collapse. Filtered Dice by epoch was 0.1844, 0.2493, 0.2674, 0.3290, 0.2952, 0.3088, 0.3367, 0.3214, 0.3581, 0.3497, 0.3333, and 0.3737. The selected checkpoint was the final epoch 12, so the trajectory was late-improving after an oscillatory middle phase.

The final selected checkpoint had filtered precision 0.3231, filtered recall 0.4431, filtered connectivity 0.2614, filtered predicted-positive fraction 0.00497, MIT filtered Dice 0.3737, and Google filtered Dice 0.3737. The raw-to-filtered gap was modest: raw Dice 0.3851 versus filtered Dice 0.3737, with raw predicted-positive fraction 0.00529 versus filtered 0.00497. The issue was therefore not excessive dependence on Artifact Filters but a worse precision/connectivity and source-transfer tradeoff at the trusted threshold.

The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` had per-sample Dice values of approximately 0, 1, 0, and 0. Because prediction retention is fixed `first_n`, these are bounded artifacts and not representative qualitative evidence; aggregate and source-stratified validation metrics carry this decision.

## Interpretation

Classify ABI-097 as finite, resource-feasible, non-collapsed, and source-balanced but negative capped family-development evidence for the exact negative-output-bias initialization branch. It fails the proposal's useful-continuation criteria: it is not within 0.01 of ABI-068's filtered Dice, does not improve filtered precision or connectivity, does not lower filtered predicted-positive fraction, and does not exceed ABI-066 filtered Dice while retaining ABI-066-like positive-area discipline. It does satisfy the weak condition that both Dataset Sources exceed 0.36 filtered Dice, but the mechanism moved in the wrong direction by producing broader positive predictions and poorer connectivity.

The result suggests that ABI-068's false-positive burden is not improved by a mild negative trainable output-logit prior under the current focal-Tversky, centerline-auxiliary, combined source-balanced, constant-LR budget. The bias appears either to have been overwritten or to have altered optimization toward a recall-heavy lower-precision endpoint. This does not eliminate the frequency-gated line U-Net family, because ABI-068 remains the strongest local whole-validation-tested aggregate-Dice reference and ABI-066 remains the precision/connectivity-forward reference. It does argue against additional bias-only tuning as the next use of capped Runs.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-097 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-097. Do not repeat ABI-068 with only trainable output-head bias tweaks under the current trusted loss, sampling, augmentation, and 12-epoch constant-LR budget. Do not request a whole-validation failure-bucket diagnostic for ABI-097 ahead of ABI-068 or ABI-066, because it did not meet the preregistered diagnostic trigger of preserving ABI-068-like Dice while improving precision/connectivity or lowering predicted-positive burden.

Retain ABI-068 as the local aggregate-Dice reference and ABI-066 as the precision/connectivity reference for this family. A useful next hypothesis should broaden beyond initialization-only calibration, for example by testing a materially different architecture family or a provider-approved policy axis that can reduce false-positive clutter without candidate-owned thresholding, postprocessing, Artifact Filters, sampling implementation, augmentation implementation, target derivation, losses, metrics, resource placement, or lifecycle behavior.

## Artifact references

- `run_20260830_030927_4f7d3d/outputs/best_metrics.json`
- `run_20260830_030927_4f7d3d/outputs/final_metrics.json`
- `run_20260830_030927_4f7d3d/outputs/metrics.jsonl`
- `run_20260830_030927_4f7d3d/outputs/resource_profile.json`
- `run_20260830_030927_4f7d3d/outputs/model_summary.json`
- `run_20260830_030927_4f7d3d/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260828_094949_ad2af0/outputs/best_metrics.json`
- `run_20260829_181201_01c5e7/outputs/best_metrics.json`
- `run_20260830_021504_c112f8/outputs/best_metrics.json`
