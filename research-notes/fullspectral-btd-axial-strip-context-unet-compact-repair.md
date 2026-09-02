# Full-spectral BTD axial strip-context U-Net compact repair

research-figures: []

## Scope

This note records ABI-063, the compact repair of ABI-062's full-spectral BTD axial strip-context U-Net family scout. ABI-062 failed smoke testing before training because its base-width 44 implementation exceeded the 25,000,000-parameter ceiling with 38,128,851 parameters. ABI-063 preserved the same scientific hypothesis and reduced base width to 32.

Source Runs:

- ABI-062 axial strip-context U-Net, smoke-failed parameter-budget scout: `run_20260827_202953_b154e5`
- ABI-063 compact axial strip-context U-Net repair: `run_20260827_203436_96acf7`
- Primary comparison target ABI-058 oriented-context high-resolution BTD line U-Net: `run_20260827_171331_c1769a`
- Secondary comparison context ABI-061 focal-Tversky oriented-context high-resolution BTD line U-Net: `run_20260827_194725_c1d6c6`

All trained comparison Runs used provider-approved `abi_16ch` inputs, approved thermal BTD features derived only from ABI channels, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped feasibility results, not full-data promotion evidence.

## ABI-063 implementation and resource observation

ABI-063 normalized ABI channels 1-16, added explicit thermal brightness-temperature-difference planes, used a learned 1x1 channel mixer, and trained a compact encoder-decoder with row-pooled, column-pooled, and globally gated strip-context blocks. It emitted `mask_logits` and provider-derived `centerline_logits` with trusted `bce_dice_cldice` primary loss and a trusted weighted-BCE centerline auxiliary target at weight 0.02.

The Candidate stayed inside the contract: no longitude/latitude inputs, no custom data loading, no custom loss or target derivation, no candidate-owned augmentation, no metrics, no thresholding, no Artifact Filters, and no postprocessing.

The repair succeeded as a resource repair. Model summary reported 20,169,582 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 2,653.0 seconds wall time, 8.08 GiB peak CUDA allocated, 9.25 GiB peak CUDA reserved, and no terminal execution failure.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_171331_c1769a` | ABI-058 | oriented full-resolution context, clDice + centerline aux | 10 | 0.3248 | 0.3139 | 0.3497 | 0.3144 | 0.3360 | 0.2335 | 0.00387 | 14.21M |
| `run_20260827_194725_c1d6c6` | ABI-061 | focal-Tversky on ABI-058 architecture + centerline aux | 12 | 0.3221 | 0.2954 | 0.3896 | 0.3515 | 0.2973 | 0.2834 | 0.00306 | 14.21M |
| `run_20260827_203436_96acf7` | ABI-063 | compact axial strip context, clDice + centerline aux | 12 | 0.2782 | 0.2763 | 0.2820 | 0.2292 | 0.3538 | 0.1446 | 0.00559 | 20.17M |

## ABI-063 trajectory

ABI-063 was finite and non-degenerate throughout the observed trajectory. Filtered Dice rose from 0.0681 at epoch 1 to 0.1372 at epoch 2, 0.1661 at epoch 3, 0.2290 at epoch 4, and 0.2559 at epoch 5. It then oscillated: epoch 6 dropped to 0.2118, epochs 7-9 stayed around 0.236-0.253 with recall-heavy behavior, and epochs 10-12 improved from 0.2600 to the final/best 0.2782.

At the best checkpoint, ABI-063 was source-balanced in the narrow sense that MIT and Google capped Dice were similar: MIT filtered Dice 0.2763 and Google filtered Dice 0.2820. The balance came at a lower aggregate quality point than ABI-058/ABI-061. Filtered recall was 0.3538, but filtered precision was only 0.2292 and filtered predicted-positive fraction was 0.00559, indicating a heavier positive-prediction burden than the high-resolution line U-Net references. Filtered connectivity was 0.1446, lower than ABI-058's 0.2335 and ABI-061's 0.2834.

The fixed first-four prediction samples all have near-zero sample Dice values, so they should not be treated as representative qualitative evidence.

## Interpretation

ABI-063 repaired ABI-062's parameter-budget failure but did not support the axial strip-context scout hypothesis as a stronger local direction. It missed the primary ABI-058 comparison target by 0.0467 filtered Dice on the capped representative validation set. It also missed the proposal's continuation criterion of being within about 0.03 of ABI-058.

The expected distinctive secondary gains did not appear. The compact strip-context model did not lower predicted-positive burden, did not improve precision, and did not improve filtered connectivity. Instead, it produced a recall-heavier, lower-precision, lower-connectivity result while using more parameters and more wall time than the oriented-context high-resolution BTD line U-Net references.

The result is not an execution failure, non-finite failure, or prediction collapse. It is a negative/mixed family-scout result: the exact compact axial strip-context branch is viable to train, but the bounded evidence does not justify prioritizing another near-variant before broadening the frontier.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context at filtered Dice 0.3873. ABI-063 is not promotion-ready and must not be interpreted as full-data evidence.

## Decision

Classify ABI-063 as `bad_research_result` / negative capped family-scout evidence for the compact axial strip-context U-Net branch. Do not promote ABI-063. Do not repeat this exact axial strip-context formulation or simply widen it, since the wider ABI-062 version already violated the parameter ceiling and the compact repair lacked aggregate or secondary-metric payoff.

A useful next hypothesis should broaden away from axial strip pooling. Reasonable next directions include a different global-context mechanism with lower parameter cost, a two-stage coarse-to-fine architecture that preserves full-resolution thin-line detail, or a diagnostic whole-validation request for the current stronger local reference if the campaign needs to test whether ABI-058/ABI-061 capped source-transfer signals survive the full Working Validation Split.

## Artifact references

- `run_20260827_202953_b154e5/outputs/logs/smoke_test.log`
- `run_20260827_203436_96acf7/outputs/best_metrics.json`
- `run_20260827_203436_96acf7/outputs/final_metrics.json`
- `run_20260827_203436_96acf7/outputs/metrics.jsonl`
- `run_20260827_203436_96acf7/outputs/resource_profile.json`
- `run_20260827_203436_96acf7/outputs/model_summary.json`
- `run_20260827_203436_96acf7/outputs/prediction_samples/samples.json`
- `run_20260827_171331_c1769a/outputs/best_metrics.json`
- `run_20260827_194725_c1d6c6/outputs/best_metrics.json`
