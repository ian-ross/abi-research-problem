# Full-spectral BTD frequency-gated line U-Net scout

research-figures: []

## Scope

This note records ABI-066, a frequency-gated thin-line segmentation family scout, after Run `run_20260827_230540_bf4ce3` completed.

Source Runs:

- ABI-058 oriented-context high-resolution BTD line U-Net local whole-validation-tested reference: `run_20260827_171331_c1769a`
- ABI-061 focal-Tversky oriented-context high-resolution BTD line U-Net precision/connectivity reference: `run_20260827_194725_c1d6c6`
- ABI-064 coarse-to-fine U-Net clDice/centerline scout: `run_20260827_212811_0e34e2`
- ABI-065 coarse-to-fine U-Net focal-Tversky follow-up: `run_20260827_221136_3d2736`
- ABI-066 frequency-gated line U-Net scout: `run_20260827_230540_bf4ce3`

All trained comparison Runs used provider-approved `abi_16ch` inputs, approved thermal BTD features derived only from ABI channels, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped feasibility results, not full-data promotion evidence.

## ABI-066 implementation and resource observation

ABI-066 uses normalized ABI channels 1-16, explicit thermal brightness-temperature-difference planes derived only from those approved channels, and a learned spectral mixer. Its distinctive change is an internal differentiable high/low spatial-frequency split: high-pass local residual features emphasize thin-line contrast, while smoothed context gates skip and decoder features before a frequency-pyramid/oriented line refiner emits `mask_logits` and provider-derived `centerline_logits`.

The Run stayed inside the Candidate Experiment Contract: no longitude/latitude inputs, no reconstructed coordinate inputs, no candidate-owned data loading, no custom loss or target derivation, no augmentation implementation, no metrics, no thresholding, no Artifact Filters, no postprocessing, no network access, and no pretrained weights. The manifest selected trusted `bce_dice_cldice` plus a provider-derived `centerline` auxiliary target with `weighted_bce` at weight 0.02.

Model summary reported 12,087,561 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 2,928.1 seconds wall time, 8,139,343,360 bytes peak CUDA allocated, 9,734,979,584 bytes peak CUDA reserved, and no terminal execution failure.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_171331_c1769a` | ABI-058 | oriented full-resolution context, clDice + centerline aux | 10 | 0.3248 | 0.3139 | 0.3497 | 0.3144 | 0.3360 | 0.2335 | 0.00387 |
| `run_20260827_194725_c1d6c6` | ABI-061 | focal-Tversky on ABI-058 architecture + centerline aux | 12 | 0.3221 | 0.2954 | 0.3896 | 0.3515 | 0.2973 | 0.2834 | 0.00306 |
| `run_20260827_212811_0e34e2` | ABI-064 | coarse soft-prior gating, clDice + centerline aux | 11 | 0.3255 | 0.3213 | 0.3348 | 0.3016 | 0.3535 | 0.1972 | 0.00425 |
| `run_20260827_221136_3d2736` | ABI-065 | focal-Tversky on ABI-064 architecture + centerline aux | 10 | 0.3132 | 0.2976 | 0.3478 | 0.3039 | 0.3230 | 0.1967 | 0.00385 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated high/low spatial features, clDice + centerline aux | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |

ABI-066 is the strongest completed capped local Run observed so far by the primary selection metric, `val/filtered_dice`. Relative to ABI-058, it improves filtered Dice by about +0.0577, filtered precision by about +0.1283, filtered connectivity by about +0.2395, and lowers filtered predicted-positive fraction by about -0.00112 while preserving essentially the same aggregate recall. Relative to ABI-064, it improves filtered Dice by about +0.0570, precision by about +0.1411, connectivity by about +0.2759, and lowers predicted-positive fraction by about -0.00149, while sacrificing only about -0.0168 recall.

The source pattern is encouraging but still asymmetric: Google capped filtered Dice reached 0.4292, while MIT capped filtered Dice reached 0.3638. Both are non-catastrophic and both exceed the local comparison Runs' capped source metrics. Canonical MCAST 2.1 remains the full Working Validation Split promotion context at filtered Dice 0.3873; ABI-066's capped score must not be interpreted as beating or matching that full-data baseline.

## ABI-066 trajectory

ABI-066 trained finitely and non-degenerately throughout the 12-epoch budget. Filtered Dice started unusually high for this campaign at 0.2453 on epoch 1, improved to 0.3204 by epoch 4, reached 0.3534 at epoch 6, dipped sharply to 0.2667 at epoch 7 during a recall-heavy/high-burden checkpoint, and then recovered to 0.3713 at epoch 8. The final three epochs were strong and stable relative to earlier branches: 0.3777 at epoch 10, 0.3778 at epoch 11, and the best 0.3825 at epoch 12.

At the selected final checkpoint, raw Dice was 0.3968 and filtered Dice was 0.3825. Artifact filtering reduced predicted-positive pixels from 393,896 raw to 369,937 filtered and reduced Dice rather than rescuing the model, so the capped result is not dependent on Artifact Filters for an apparent improvement. The best checkpoint is precision/connectivity-forward without all-negative collapse: filtered precision 0.4427, recall 0.3367, connectivity 0.4731, and filtered predicted-positive fraction 0.00276.

The fixed first-four prediction artifacts are not representative qualitative evidence: the first two retained samples are perfect empty-mask cases, while the next two have near-zero sample Dice. The aggregate and source-stratified validation metrics are the useful evidence for this note.

## Interpretation

ABI-066 provides strong positive capped family-scout evidence for the frequency-gated high/low spatial-feature idea. It directly addresses the recent campaign failure mode: many branches either increased recall by adding broad false positives or gained precision/connectivity while losing too much MIT recall. ABI-066 instead combines the lowest predicted-positive burden among the local high-performing branches with the best capped Dice, best capped precision, best capped connectivity, and better MIT and Google source Dice.

The result satisfies the proposal's continuation criteria: it exceeds ABI-058 and ABI-061 by the primary capped metric, improves precision and predicted-positive burden relative to ABI-058/ABI-064, keeps both MIT and Google filtered Dice above 0.25, and improves connectivity substantially. It is not a promotion result because it is still capped representative validation evidence and has not been tested on the full 3,088-sample Working Validation Split or through acceptance-gate diagnostics.

The strongest scientific risk is capped-to-full transfer. ABI-058 and ABI-064 both showed that small capped advantages may shrink or reverse on whole-validation diagnostics. ABI-066's improvement is much larger than those previous capped deltas, but the Google-skewed source profile and final-epoch best checkpoint still need full-validation confirmation before this branch should drive additional architecture tuning.

## Decision

Classify ABI-066 as positive capped family-scout evidence for the frequency-gated line U-Net branch. Do not promote ABI-066 from capped evidence, and do not treat it as a full-data Result.

The next useful primary handoff is a bounded Evaluation Request for whole-validation failure-bucket/acceptance-style diagnostics on `run_20260827_230540_bf4ce3`. The diagnostic question should be whether ABI-066's capped gains in precision, connectivity, predicted-positive burden, and both Dataset Source filtered Dice survive the full Working Validation Split, and whether its reduced false-positive burden remains better than ABI-058 and ABI-064 without causing a hidden recall failure. If whole-validation evidence preserves a meaningful advantage, then a later bounded family-development continuation could test whether trusted focal-Tversky or a small centerline auxiliary-weight adjustment improves the same frequency-gated architecture.

## Artifact references

- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/final_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/metrics.jsonl`
- `run_20260827_230540_bf4ce3/outputs/resource_profile.json`
- `run_20260827_230540_bf4ce3/outputs/model_summary.json`
- `run_20260827_230540_bf4ce3/outputs/prediction_samples/samples.json`
- `run_20260827_171331_c1769a/outputs/best_metrics.json`
- `run_20260827_171331_c1769a/outputs/evaluations/eval_evalreq_abi058_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_212811_0e34e2/outputs/best_metrics.json`
- `run_20260827_212811_0e34e2/outputs/evaluations/eval_evalreq_abi064_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_194725_c1d6c6/outputs/best_metrics.json`
- `run_20260827_221136_3d2736/outputs/best_metrics.json`
