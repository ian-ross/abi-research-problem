# Full-spectral BTD high-resolution line U-Net false-positive-suppressor follow-up

research-figures: []

## Scope

This note records ABI-059, a controlled follow-up after ABI-058 whole-validation diagnostics identified broad low-level false-positive behavior.

Source Runs:

- ABI-056 high-resolution line U-Net with multi-scale skip fusion + trusted `bce_dice_cldice` + `centerline` auxiliary target weight 0.02: `run_20260827_153716_1ac9d4`
- ABI-057 high-resolution line U-Net with line-gated mask refiner + `centerline` auxiliary target weight 0.02: `run_20260827_162936_6294f6`
- ABI-058 high-resolution line U-Net with oriented full-resolution context + `centerline` auxiliary target weight 0.02: `run_20260827_171331_c1769a`
- ABI-059 high-resolution line U-Net with oriented context plus a trainable false-positive suppressor head + `centerline` auxiliary target weight 0.02: `run_20260827_181006_6a9a1f`

All Runs used provider-approved `abi_16ch` inputs, approved thermal BTD features derived only from ABI channels, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped feasibility results, not full-data promotion evidence.

## ABI-059 implementation and resource observation

ABI-059 kept the ABI-058 stack fixed through the normalized full-spectral + thermal-BTD front end, learned channel mixer, high-resolution line U-Net, multi-scale skip fusion, oriented full-resolution context refiner, trusted `bce_dice_cldice`, and provider-derived `centerline` auxiliary target at weight 0.02.

The controlled change was a trainable false-positive suppressor head: low-resolution context is fused back into the oriented full-resolution features, a non-negative learned suppression term is predicted, and final `mask_logits` subtract a small suppression component from base logits. This remained model architecture only, not candidate-owned thresholding, postprocessing, Artifact Filtering, data loading, target derivation, or loss/metric implementation.

The Run completed finite and non-degenerate. Model summary reported 14,421,303 parameters, within the 25,000,000-parameter smoke ceiling. Resource profile reported batch size 4, A100 execution, 2,383.3 seconds wall time, 8.83 GB peak CUDA allocated, 10.35 GB peak CUDA reserved, and completed status.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_153716_1ac9d4` | ABI-056 | multi-scale skip fusion | 11 | 0.3225 | 0.3108 | 0.3492 | 0.3310 | 0.3144 | 0.2245 | 0.00344 |
| `run_20260827_162936_6294f6` | ABI-057 | line-gated mask refiner | 12 | 0.3188 | 0.3042 | 0.3507 | 0.3365 | 0.3028 | 0.2677 | 0.00326 |
| `run_20260827_171331_c1769a` | ABI-058 | oriented full-resolution context | 10 | 0.3248 | 0.3139 | 0.3497 | 0.3144 | 0.3360 | 0.2335 | 0.00387 |
| `run_20260827_181006_6a9a1f` | ABI-059 | trainable false-positive suppressor | 10 | 0.3135 | 0.3088 | 0.3231 | 0.3052 | 0.3222 | 0.1383 | 0.00383 |

## ABI-059 trajectory

ABI-059 improved from filtered Dice 0.0238 at epoch 1 to 0.2382 at epoch 5, 0.2645 at epoch 6, 0.2699 at epoch 9, and its best 0.3135 at epoch 10. Epoch 11 dropped to 0.2740, and epoch 12 recovered only to 0.2973 while shifting toward higher recall and more predicted-positive area.

At its best checkpoint, ABI-059 was non-collapsed and source-informative: MIT filtered Dice 0.3088, Google filtered Dice 0.3231, filtered precision 0.3052, filtered recall 0.3222, filtered connectivity 0.1383, and filtered predicted-positive fraction 0.00383. The final checkpoint had filtered Dice 0.2973, precision 0.2465, recall 0.3742, connectivity 0.1314, and predicted-positive fraction 0.00550.

## Interpretation

ABI-059 is a finite but negative/mixed family-development result. It did not meet its intended diagnostic signal: relative to ABI-058, the best checkpoint did not lower predicted-positive fraction meaningfully, did not improve precision, did not preserve Google/source-balanced Dice, and substantially reduced the filtered connectivity signal. Relative to ABI-056, it was also worse on filtered Dice, precision, connectivity, and predicted-positive fraction.

The result does not indicate a contract or implementation failure requiring repair. It instead suggests that this simple subtractive false-positive suppressor is not an effective way to control ABI-058's broad low-level false positives under the current trusted loss and capped training policy. Because the branch remains finite and non-collapsed, low Dice alone should not eliminate the broader high-resolution BTD line U-Net family; however, this exact suppressor-head mechanism should not be repeated unchanged.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context at filtered Dice 0.3873. ABI-058 remains the local whole-validation-tested reference for this branch, with whole-validation filtered Dice 0.3233, and ABI-056 remains the more precision-favorable whole-validation-tested comparator.

## Decision

Classify ABI-059 as `bad_research_result` / negative family-development evidence for the specific false-positive-suppressor head. Do not promote ABI-059 and do not request whole-validation diagnostics for this exact checkpoint unless a later comparison specifically needs it.

A useful next hypothesis should broaden away from incremental high-resolution decoder-head refinements. Two plausible later directions are: a different architecture family with explicit thin-line continuity bias but less diffuse background activation, or a trusted-policy axis that changes the optimization pressure on false positives without moving loss or sampling implementation into candidate code. If staying in the same family, the next change should be materially different from subtractive suppression, for example confidence-gated feature selection or a lower-capacity precision-oriented branch with a clear hard-stop criterion.

## Artifact references

- `run_20260827_181006_6a9a1f/outputs/best_metrics.json`
- `run_20260827_181006_6a9a1f/outputs/final_metrics.json`
- `run_20260827_181006_6a9a1f/outputs/metrics.jsonl`
- `run_20260827_181006_6a9a1f/outputs/resource_profile.json`
- `run_20260827_181006_6a9a1f/outputs/model_summary.json`
- `run_20260827_181006_6a9a1f/outputs/prediction_samples/samples.json`
- `run_20260827_171331_c1769a/outputs/evaluations/eval_evalreq_abi058_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_171331_c1769a/outputs/best_metrics.json`
- `run_20260827_153716_1ac9d4/outputs/evaluations/eval_evalreq_abi056_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_153716_1ac9d4/outputs/best_metrics.json`
- `run_20260827_162936_6294f6/outputs/best_metrics.json`
