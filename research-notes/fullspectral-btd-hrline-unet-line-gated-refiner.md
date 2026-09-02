# Full-spectral BTD high-resolution line U-Net line-gated refiner follow-up

research-figures: []

## Scope

This note records ABI-057, the controlled line-gated mask-refiner continuation after ABI-053 through ABI-056 and the ABI-056 whole-validation failure-bucket review.

Source Runs:

- ABI-053 full-spectral BTD high-resolution line U-Net + trusted `bce_dice_cldice` + `centerline` auxiliary target weight 0.02: `run_20260827_134629_3ace34`
- ABI-054 same high-resolution line U-Net + `centerline` auxiliary target weight 0.05: `run_20260827_142319_ec8c29`
- ABI-055 high-resolution line U-Net with directional continuity refiner + `centerline` auxiliary target weight 0.02: `run_20260827_145929_e61464`
- ABI-056 high-resolution line U-Net with multi-scale skip fusion + `centerline` auxiliary target weight 0.02: `run_20260827_153716_1ac9d4`
- ABI-057 high-resolution line U-Net with line-gated mask refiner + `centerline` auxiliary target weight 0.02: `run_20260827_162936_6294f6`

All Runs used provider-approved `abi_16ch` inputs, approved thermal BTD features derived only from ABI channels, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped feasibility results, not full-data promotion evidence.

## ABI-057 implementation and resource observation

ABI-057 kept ABI-056's front end and training policy: normalized ABI channels 1-16, explicit thermal BTD planes, learned channel mixing, trusted `bce_dice_cldice`, and the provider-derived `centerline` auxiliary target at weight 0.02. The controlled architecture change was replacing the shared full-resolution refiner/head with a `LineGatedMaskRefiner`: a centerline-supervised line branch emits `centerline_logits`; a differentiable internal attention map from those logits gates line and mask features before the final `mask_logits` head.

The Run completed finite and non-degenerate. Model summary reported 14,223,586 parameters, within the 25,000,000-parameter smoke ceiling. Resource profile reported batch size 4, A100 execution, 2,184.6 seconds wall time, 7.34 GB peak CUDA allocated, 8.55 GB peak CUDA reserved, and completed status.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_134629_3ace34` | ABI-053 | high-resolution line U-Net + centerline aux weight 0.02 | 9 | 0.3221 | 0.3119 | 0.3467 | 0.3005 | 0.3472 | 0.2347 | 0.00419 |
| `run_20260827_142319_ec8c29` | ABI-054 | centerline aux weight 0.05 | 12 | 0.3160 | 0.2952 | 0.3676 | 0.3329 | 0.3006 | 0.2046 | 0.00327 |
| `run_20260827_145929_e61464` | ABI-055 | directional continuity refiner | 11 | 0.3152 | 0.3155 | 0.3148 | 0.3143 | 0.3162 | 0.2147 | 0.00365 |
| `run_20260827_153716_1ac9d4` | ABI-056 | multi-scale skip fusion | 11 | 0.3225 | 0.3108 | 0.3492 | 0.3310 | 0.3144 | 0.2245 | 0.00344 |
| `run_20260827_162936_6294f6` | ABI-057 | line-gated mask refiner | 12 | 0.3188 | 0.3042 | 0.3507 | 0.3365 | 0.3028 | 0.2677 | 0.00326 |

## ABI-057 trajectory

ABI-057 improved from filtered Dice 0.0786 at epoch 1 to 0.2081 at epoch 3, 0.2731 at epoch 5, 0.2897 at epoch 7, 0.3058 at epoch 10, 0.3168 at epoch 11, and its best 0.3188 at epoch 12. The best checkpoint and final checkpoint are the same epoch, so there is no late best-to-final regression.

The final checkpoint is non-collapsed and source-informative: MIT filtered Dice 0.3042, Google filtered Dice 0.3507, filtered precision 0.3365, filtered recall 0.3028, filtered connectivity 0.2677, and filtered predicted-positive fraction 0.00326. The fixed first-four prediction samples all have near-zero sample Dice values, so they should not be treated as representative qualitative evidence.

## Interpretation

ABI-057 partially matched the intended diagnostic signal but did not improve the primary capped metric. Relative to ABI-056's best checkpoint, ABI-057 improved filtered precision from 0.3310 to 0.3365, lowered filtered predicted-positive fraction from 0.00344 to 0.00326, improved filtered connectivity from 0.2245 to 0.2677, and slightly improved Google filtered Dice from 0.3492 to 0.3507. Those changes support the idea that line-gated refinement can reduce diffuse positive tendency and strengthen connected line structure.

The cost is lower source-balanced overlap and recall. Aggregate filtered Dice decreased from ABI-056 best 0.3225 to ABI-057 0.3188, MIT filtered Dice decreased from 0.3108 to 0.3042, and filtered recall decreased from 0.3144 to 0.3028. Compared with ABI-056's final epoch, ABI-057 has better precision and connectivity but still lower filtered Dice and substantially lower recall. Compared with ABI-053, ABI-057 does not recover ABI-053's best filtered Dice or recall, though it improves precision and best-checkpoint connectivity.

Canonical MCAST 2.1 remains the full Working Validation Split reference at filtered Dice 0.3873. ABI-057 is representative capped family-development evidence only and should not be interpreted as full-data promotion evidence.

## Decision

Do not promote ABI-057 and do not repeat this exact line-gated head unchanged. Classify it as a finite, non-degenerate mixed result: diagnostically useful for precision, predicted-positive fraction, and connectivity, but negative against ABI-056 on the primary capped filtered-Dice objective.

The high-resolution BTD line U-Net family is not eliminated by this result, but the latest branch suggests that internal line attention alone is not enough to close the recall/overlap gap. A later Autonomy Step should either broaden to a different connectivity/false-positive mechanism or a different architecture family, rather than repeating centerline-weight tuning, directional refiner, multi-scale skip fusion, or this same line-gated refiner. If whole-validation diagnostics are requested later, they should be justified by the precision/connectivity signal rather than by a capped primary-metric improvement.

## Artifact references

- `run_20260827_162936_6294f6/outputs/best_metrics.json`
- `run_20260827_162936_6294f6/outputs/final_metrics.json`
- `run_20260827_162936_6294f6/outputs/metrics.jsonl`
- `run_20260827_162936_6294f6/outputs/resource_profile.json`
- `run_20260827_162936_6294f6/outputs/model_summary.json`
- `run_20260827_162936_6294f6/outputs/prediction_samples/samples.json`
- `run_20260827_153716_1ac9d4/outputs/evaluations/eval_evalreq_abi056_wholeval_failure_buckets_v1/summary.json`
- `run_20260827_153716_1ac9d4/outputs/best_metrics.json`
- `run_20260827_153716_1ac9d4/outputs/final_metrics.json`
- `run_20260827_134629_3ace34/outputs/best_metrics.json`
- `run_20260827_142319_ec8c29/outputs/best_metrics.json`
- `run_20260827_145929_e61464/outputs/best_metrics.json`
