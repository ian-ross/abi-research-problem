# Full-spectral BTD high-resolution line U-Net focal-Tversky follow-up

research-figures: []

## Scope

This note records ABI-061, a controlled loss-policy follow-up after the high-resolution BTD line U-Net branch reached a narrow whole-validation-tested local reference with ABI-058 and then found that ABI-059/ABI-060 decoder-head refinements did not produce a clean aggregate gain.

Source Runs:

- ABI-056 high-resolution line U-Net with multi-scale skip fusion + trusted `bce_dice_cldice` + `centerline` auxiliary target weight 0.02: `run_20260827_153716_1ac9d4`
- ABI-058 high-resolution line U-Net with oriented full-resolution context + trusted `bce_dice_cldice` + `centerline` auxiliary target weight 0.02: `run_20260827_171331_c1769a`
- ABI-060 high-resolution line U-Net with confidence-gated feature selection + trusted `bce_dice_cldice` + `centerline` auxiliary target weight 0.02: `run_20260827_185739_a17505`
- ABI-061 high-resolution line U-Net with oriented full-resolution context + trusted `focal_tversky` + `centerline` auxiliary target weight 0.02: `run_20260827_194725_c1d6c6`

All Runs used provider-approved `abi_16ch` inputs, approved thermal BTD features derived only from ABI channels, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped feasibility results, not full-data promotion evidence.

## ABI-061 implementation and resource observation

ABI-061 kept the ABI-058 oriented-context high-resolution line U-Net architecture: normalized full-spectral ABI channels 1-16, explicit thermal BTD planes, learned channel mixing, multi-scale skip fusion, oriented full-resolution context, a primary `mask_logits` head, and a provider-derived `centerline_logits` auxiliary output. The controlled change was selecting trusted `focal_tversky` as the primary loss instead of trusted `bce_dice_cldice`.

This remained within the Candidate Experiment Contract. ABI-061 did not use longitude/latitude, custom data loading, custom losses, custom target derivation, candidate-owned augmentation, thresholding, Artifact Filters, or postprocessing.

The Run completed finite and non-degenerate. Model summary reported 14,213,030 parameters, within the 25,000,000-parameter smoke ceiling. Resource profile reported batch size 4, A100 execution, 2,072.4 seconds wall time, 7.15 GiB peak CUDA allocated, 8.81 GiB peak CUDA reserved, and completed status.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_153716_1ac9d4` | ABI-056 | multi-scale skip fusion, clDice + centerline aux | 11 | 0.3225 | 0.3108 | 0.3492 | 0.3310 | 0.3144 | 0.2245 | 0.00344 |
| `run_20260827_171331_c1769a` | ABI-058 | oriented full-resolution context, clDice + centerline aux | 10 | 0.3248 | 0.3139 | 0.3497 | 0.3144 | 0.3360 | 0.2335 | 0.00387 |
| `run_20260827_185739_a17505` | ABI-060 | confidence-gated feature selection, clDice + centerline aux | 10 | 0.3147 | 0.2890 | 0.3733 | 0.3532 | 0.2837 | 0.3289 | 0.00291 |
| `run_20260827_194725_c1d6c6` | ABI-061 | focal-Tversky on ABI-058 architecture + centerline aux | 12 | 0.3221 | 0.2954 | 0.3896 | 0.3515 | 0.2973 | 0.2834 | 0.00306 |

## ABI-061 trajectory

ABI-061 started collapsed/all-negative at epoch 1 by predicted-positive fraction, then became non-degenerate at epoch 2. Filtered Dice rose from 0.0903 at epoch 2 to 0.1791 at epoch 4, 0.2415 at epoch 5, and 0.2656 at epoch 7. Epochs 8 and 9 were recall-heavy but noisy: filtered recall reached 0.4814 at epoch 8 while filtered Dice fell to 0.1916, then filtered Dice recovered to 0.2550 at epoch 9. The final three epochs oscillated sharply: 0.3175 at epoch 10, 0.2475 at epoch 11, and the best 0.3221 at epoch 12.

At the best checkpoint, ABI-061 was non-collapsed and source-informative. Aggregate filtered Dice was 0.3221 with filtered precision 0.3515, filtered recall 0.2973, filtered connectivity 0.2834, and filtered predicted-positive fraction 0.00306. The Dataset Source pattern was strongly asymmetric: MIT filtered Dice 0.2954 with filtered recall 0.2620, while Google filtered Dice reached 0.3896 with filtered recall 0.4003.

The fixed first-four prediction samples all have near-zero sample Dice values, so they should not be treated as representative qualitative evidence.

## Interpretation

ABI-061 did not beat the ABI-058 oriented-context local reference by the primary capped selection metric: best filtered Dice was 0.3221 versus ABI-058's 0.3248 and ABI-056's 0.3225. It also does not supersede ABI-058's whole-validation filtered Dice 0.3233, because ABI-061 has not been evaluated on the full 3,088-sample Working Validation Split and its capped primary score is slightly lower.

The focal-Tversky loss nevertheless changes the error profile. Relative to ABI-058, ABI-061 trades lower MIT Dice and lower aggregate recall for higher precision, higher filtered connectivity, lower predicted-positive burden, and a large capped Google gain. Relative to ABI-060, ABI-061 nearly matches the precision-oriented behavior while recovering aggregate filtered Dice and preserving more connectivity than ABI-058. This is not the expected recall-improving outcome for focal-Tversky in this branch; instead, under the current architecture and centerline auxiliary target, it behaves more like a precision/source-transfer shift toward Google validation patches.

The trajectory remains unstable. Best epoch is the final epoch after a large epoch-11 drop, which keeps extension evidence ambiguous rather than decisive. The result is not a hard failure, non-finite failure, or prediction collapse, but it is also not a clean aggregate improvement.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context at filtered Dice 0.3873. ABI-061 is not promotion-ready and must not be interpreted as full-data evidence.

## Decision

Classify ABI-061 as `bad_research_result` / mixed capped family-development evidence for applying trusted `focal_tversky` to the ABI-058 oriented-context high-resolution BTD line U-Net. Do not promote ABI-061 and do not repeat the exact focal-Tversky branch unchanged.

The useful signal is diagnostic: focal-Tversky plus oriented context increases Google capped Dice, precision, and connectivity while sacrificing MIT overlap and recall. A later bounded whole-validation diagnostic could be justified only if the campaign specifically needs to test whether that source-transfer/precision/connectivity signal survives the full Working Validation Split. Otherwise, the next hypothesis should broaden away from incremental high-resolution line U-Net decoder/loss tweaks toward a materially different architecture family or a trusted-policy axis that can reduce negative-patch false positives without losing MIT recall.

## Artifact references

- `run_20260827_194725_c1d6c6/outputs/best_metrics.json`
- `run_20260827_194725_c1d6c6/outputs/final_metrics.json`
- `run_20260827_194725_c1d6c6/outputs/metrics.jsonl`
- `run_20260827_194725_c1d6c6/outputs/resource_profile.json`
- `run_20260827_194725_c1d6c6/outputs/model_summary.json`
- `run_20260827_194725_c1d6c6/outputs/prediction_samples/samples.json`
- `run_20260827_171331_c1769a/outputs/evaluations/eval_evalreq_abi058_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_171331_c1769a/outputs/best_metrics.json`
- `run_20260827_153716_1ac9d4/outputs/best_metrics.json`
- `run_20260827_185739_a17505/outputs/best_metrics.json`
