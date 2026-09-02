# Full-spectral BTD high-resolution line U-Net confidence-gated refiner follow-up

research-figures: []

## Scope

This note records ABI-060, a controlled follow-up after ABI-059 showed that a subtractive false-positive suppressor did not improve the high-resolution BTD line U-Net branch.

Source Runs:

- ABI-056 high-resolution line U-Net with multi-scale skip fusion + trusted `bce_dice_cldice` + `centerline` auxiliary target weight 0.02: `run_20260827_153716_1ac9d4`
- ABI-058 high-resolution line U-Net with oriented full-resolution context + `centerline` auxiliary target weight 0.02: `run_20260827_171331_c1769a`
- ABI-059 high-resolution line U-Net with oriented context plus trainable false-positive suppressor + `centerline` auxiliary target weight 0.02: `run_20260827_181006_6a9a1f`
- ABI-060 high-resolution line U-Net with confidence-gated feature selection + `centerline` auxiliary target weight 0.02: `run_20260827_185739_a17505`

All Runs used provider-approved `abi_16ch` inputs, approved thermal BTD features derived only from ABI channels, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped feasibility results, not full-data promotion evidence.

## ABI-060 implementation and resource observation

ABI-060 kept the ABI-058/ABI-059 stack fixed through the normalized full-spectral + thermal-BTD front end, learned channel mixer, high-resolution line U-Net, multi-scale skip fusion, oriented full-resolution context refiner, trusted `bce_dice_cldice`, and provider-derived `centerline` auxiliary target at weight 0.02.

The controlled change was replacing ABI-059's subtractive suppressor head with a confidence-gated mask head. Low-resolution context and oriented full-resolution line features predict differentiable soft gates that select how strongly line/context features enter final mask refinement. This remained model architecture only, not candidate-owned thresholding, postprocessing, Artifact Filtering, data loading, target derivation, or loss/metric implementation.

The Run completed finite and non-degenerate. Model summary reported 14,629,432 parameters, within the 25,000,000-parameter smoke ceiling. Resource profile reported batch size 4, A100 execution, 2,533.8 seconds wall time, 9.23 GiB peak CUDA allocated, 10.50 GiB peak CUDA reserved, and completed status.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_153716_1ac9d4` | ABI-056 | multi-scale skip fusion | 11 | 0.3225 | 0.3108 | 0.3492 | 0.3310 | 0.3144 | 0.2245 | 0.00344 |
| `run_20260827_171331_c1769a` | ABI-058 | oriented full-resolution context | 10 | 0.3248 | 0.3139 | 0.3497 | 0.3144 | 0.3360 | 0.2335 | 0.00387 |
| `run_20260827_181006_6a9a1f` | ABI-059 | trainable false-positive suppressor | 10 | 0.3135 | 0.3088 | 0.3231 | 0.3052 | 0.3222 | 0.1383 | 0.00383 |
| `run_20260827_185739_a17505` | ABI-060 | confidence-gated feature selection | 10 | 0.3147 | 0.2890 | 0.3733 | 0.3532 | 0.2837 | 0.3289 | 0.00291 |

## ABI-060 trajectory

ABI-060 improved from filtered Dice 0.0622 at epoch 1 to 0.2152 at epoch 3, 0.2406 at epoch 5, 0.2629 at epoch 7, then regressed through epoch 9 to 0.2159 before jumping to its best 0.3147 at epoch 10. Epoch 11 dropped to 0.2857, and the final epoch recovered to 0.3123.

At its best checkpoint, ABI-060 was non-collapsed and source-informative but source-asymmetric: MIT filtered Dice 0.2890, Google filtered Dice 0.3733, filtered precision 0.3532, filtered recall 0.2837, filtered connectivity 0.3289, and filtered predicted-positive fraction 0.00291. The final checkpoint remained close in aggregate filtered Dice at 0.3123, with precision 0.3213, recall 0.3038, connectivity 0.2808, predicted-positive fraction 0.00343, MIT filtered Dice 0.2872, and Google filtered Dice 0.3704.

The fixed first-four prediction samples again have near-zero sample Dice values, so they should not be treated as representative qualitative evidence.

## Interpretation

ABI-060 is a mixed capped family-development result. It did not meet the primary extension-positive criterion of tying or exceeding ABI-058's capped filtered Dice: best filtered Dice was 0.3147 versus ABI-058's 0.3248 and ABI-056's 0.3225. The shortfall is concentrated on MIT and recall. It also does not supersede ABI-058's whole-validation filtered Dice 0.3233 or ABI-056's whole-validation filtered Dice 0.3198.

The result is nevertheless diagnostically distinct from ABI-059. The confidence-gated head improved over ABI-059 on aggregate filtered Dice, Google filtered Dice, precision, predicted-positive fraction, and especially filtered connectivity. Relative to ABI-058, it traded lower aggregate/MIT Dice and recall for higher precision, lower predicted-positive burden, substantially higher capped connectivity, and stronger Google capped Dice. This suggests that soft feature gating is a more useful false-positive-control mechanism than subtractive logit suppression, but it introduces a source-balance and recall penalty under the current trusted loss and capped training policy.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context at filtered Dice 0.3873. ABI-060 is not promotion-ready and should not be interpreted as a full-data result.

## Decision

Classify ABI-060 as `bad_research_result` / mixed family-development evidence for this exact confidence-gated decoder-head branch. Do not promote ABI-060 and do not repeat the exact head unchanged.

Because ABI-060 produced a distinctive precision/connectivity/Google signal while underperforming on aggregate Dice, it may be worth a later bounded whole-validation diagnostic only if the campaign needs to determine whether this capped connectivity and false-positive-control signal survives the full Working Validation Split. Otherwise, the next architecture hypothesis should broaden away from incremental high-resolution decoder-head refinements toward a materially different thin-line architecture or a trusted-policy axis that improves false-positive control without sacrificing MIT recall.

## Artifact references

- `run_20260827_185739_a17505/outputs/best_metrics.json`
- `run_20260827_185739_a17505/outputs/final_metrics.json`
- `run_20260827_185739_a17505/outputs/metrics.jsonl`
- `run_20260827_185739_a17505/outputs/resource_profile.json`
- `run_20260827_185739_a17505/outputs/model_summary.json`
- `run_20260827_185739_a17505/outputs/prediction_samples/samples.json`
- `run_20260827_171331_c1769a/outputs/evaluations/eval_evalreq_abi058_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_171331_c1769a/outputs/best_metrics.json`
- `run_20260827_153716_1ac9d4/outputs/evaluations/eval_evalreq_abi056_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_153716_1ac9d4/outputs/best_metrics.json`
- `run_20260827_181006_6a9a1f/outputs/best_metrics.json`
