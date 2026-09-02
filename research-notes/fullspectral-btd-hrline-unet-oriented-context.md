# Full-spectral BTD high-resolution line U-Net oriented-context follow-up

research-figures: []

## Scope

This note records ABI-058, the controlled oriented-context continuation after ABI-053 through ABI-057 and the ABI-056 whole-validation failure-bucket review.

Source Runs:

- ABI-053 full-spectral BTD high-resolution line U-Net + trusted `bce_dice_cldice` + `centerline` auxiliary target weight 0.02: `run_20260827_134629_3ace34`
- ABI-054 same high-resolution line U-Net + `centerline` auxiliary target weight 0.05: `run_20260827_142319_ec8c29`
- ABI-055 high-resolution line U-Net with directional continuity refiner + `centerline` auxiliary target weight 0.02: `run_20260827_145929_e61464`
- ABI-056 high-resolution line U-Net with multi-scale skip fusion + `centerline` auxiliary target weight 0.02: `run_20260827_153716_1ac9d4`
- ABI-057 high-resolution line U-Net with line-gated mask refiner + `centerline` auxiliary target weight 0.02: `run_20260827_162936_6294f6`
- ABI-058 high-resolution line U-Net with oriented full-resolution context + `centerline` auxiliary target weight 0.02: `run_20260827_171331_c1769a`

All Runs used provider-approved `abi_16ch` inputs, approved thermal BTD features derived only from ABI channels, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped feasibility results, not full-data promotion evidence.

## ABI-058 implementation and resource observation

ABI-058 kept ABI-056's front end and trusted training policy: normalized ABI channels 1-16, explicit thermal BTD planes, learned channel mixing, trusted `bce_dice_cldice`, and the provider-derived `centerline` auxiliary target at weight 0.02. The controlled architecture change was replacing the isotropic full-resolution refiner with an oriented context refiner: local, horizontal-strip, vertical-strip, and broad dilated full-resolution branches are combined through a learned per-pixel softmax mixture before the primary mask and centerline heads.

The Run completed finite and non-degenerate. Model summary reported 14,213,030 parameters, within the 25,000,000-parameter smoke ceiling. Resource profile reported batch size 4, A100 execution, 2,189.1 seconds wall time, 7.79 GB peak CUDA allocated, 9.66 GB peak CUDA reserved, and completed status.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_134629_3ace34` | ABI-053 | high-resolution line U-Net + centerline aux weight 0.02 | 9 | 0.3221 | 0.3119 | 0.3467 | 0.3005 | 0.3472 | 0.2347 | 0.00419 |
| `run_20260827_142319_ec8c29` | ABI-054 | centerline aux weight 0.05 | 12 | 0.3160 | 0.2952 | 0.3676 | 0.3329 | 0.3006 | 0.2046 | 0.00327 |
| `run_20260827_145929_e61464` | ABI-055 | directional continuity refiner | 11 | 0.3152 | 0.3155 | 0.3148 | 0.3143 | 0.3162 | 0.2147 | 0.00365 |
| `run_20260827_153716_1ac9d4` | ABI-056 | multi-scale skip fusion | 11 | 0.3225 | 0.3108 | 0.3492 | 0.3310 | 0.3144 | 0.2245 | 0.00344 |
| `run_20260827_162936_6294f6` | ABI-057 | line-gated mask refiner | 12 | 0.3188 | 0.3042 | 0.3507 | 0.3365 | 0.3028 | 0.2677 | 0.00326 |
| `run_20260827_171331_c1769a` | ABI-058 | oriented full-resolution context | 10 | 0.3248 | 0.3139 | 0.3497 | 0.3144 | 0.3360 | 0.2335 | 0.00387 |

## ABI-058 trajectory

ABI-058 improved from filtered Dice 0.0590 at epoch 1 to 0.2232 at epoch 4, 0.2765 at epoch 6, 0.2883 at epoch 9, and its best 0.3248 at epoch 10. The last two epochs were unstable: epoch 11 dropped to 0.2665, and the final epoch recovered to 0.3121 but remained below ABI-056's best and final filtered Dice.

The best checkpoint is non-collapsed and source-informative: MIT filtered Dice 0.3139, Google filtered Dice 0.3497, filtered precision 0.3144, filtered recall 0.3360, filtered connectivity 0.2335, and filtered predicted-positive fraction 0.00387. The final checkpoint shifted toward higher Google recall and lower MIT/source-balanced overlap: final filtered Dice 0.3121, MIT filtered Dice 0.2931, Google filtered Dice 0.3585, filtered precision 0.2862, filtered recall 0.3432, and filtered predicted-positive fraction 0.00435. The fixed first-four prediction samples all have near-zero sample Dice values, so they should not be treated as representative qualitative evidence.

## Interpretation

ABI-058 is a small positive capped result by best-validation primary metric, but not a clean stability result. Its best filtered Dice 0.3248 is the highest capped `val/filtered_dice` observed in this high-resolution BTD line U-Net branch, exceeding ABI-056's 0.3225 by about +0.0024 and ABI-053's 0.3221 by about +0.0027. It also recovers more recall than ABI-056 at the best checkpoint while preserving acceptable MIT/Google behavior.

The benefit is narrow. ABI-058 does not improve on ABI-057's connectivity or precision signal, and its final checkpoint underperforms ABI-056's final filtered Dice by about -0.0100. The late epoch-11 drop and partial epoch-12 recovery suggest optimization or sampling noise under the capped policy rather than a decisive architecture improvement. The oriented-context mechanism is therefore extension-positive enough to justify diagnostics, but not strong enough to claim promotion or to repeat unchanged without full-validation evidence.

Canonical MCAST 2.1 remains the full Working Validation Split reference at filtered Dice 0.3873. ABI-058 is representative capped family-development evidence only and should not be interpreted as full-data promotion evidence.

## Decision

Treat ABI-058 as the current local capped best checkpoint for this family by primary `val/filtered_dice`, while retaining ABI-056 as the more stable whole-validation-tested reference. Do not promote ABI-058 from capped evidence.

A useful next handoff in a later Autonomy Step is a bounded Evaluation Request for whole-validation failure analysis of ABI-058, because the best-checkpoint capped gain is small and the final-epoch instability needs to be checked against the full 3,088-sample Working Validation Split. If whole-validation diagnostics do not preserve a meaningful advantage over ABI-056, broaden away from high-resolution decoder refinements toward a different architecture family or trusted policy axis rather than repeating ABI-058 unchanged.

## Artifact references

- `run_20260827_171331_c1769a/outputs/best_metrics.json`
- `run_20260827_171331_c1769a/outputs/final_metrics.json`
- `run_20260827_171331_c1769a/outputs/metrics.jsonl`
- `run_20260827_171331_c1769a/outputs/resource_profile.json`
- `run_20260827_171331_c1769a/outputs/model_summary.json`
- `run_20260827_171331_c1769a/outputs/prediction_samples/samples.json`
- `run_20260827_153716_1ac9d4/outputs/evaluations/eval_evalreq_abi056_wholeval_failure_buckets_v1/summary.json`
- `run_20260827_153716_1ac9d4/outputs/best_metrics.json`
- `run_20260827_153716_1ac9d4/outputs/final_metrics.json`
- `run_20260827_162936_6294f6/outputs/best_metrics.json`
- `run_20260827_134629_3ace34/outputs/best_metrics.json`
- `run_20260827_142319_ec8c29/outputs/best_metrics.json`
- `run_20260827_145929_e61464/outputs/best_metrics.json`
