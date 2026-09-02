# Full-spectral BTD frequency-gated line U-Net MIT-only follow-up

research-figures: []

## Scope

This note records ABI-115 after Run `run_20260830_235533_487b1c` completed.

Source Runs:

- ABI-115 MIT-only data-policy continuation: `run_20260830_235533_487b1c`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-106 analogous Google-only data-policy continuation: `run_20260830_101145_b69d10`
- ABI-096 deterministic-shuffle data-policy continuation: `run_20260830_021504_c112f8`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`

ABI-115 was a family-development continuation within the full-spectral BTD frequency-gated line U-Net branch. It retained the ABI-068 architecture, provider-approved `abi_16ch` input, deterministic thermal BTD features derived only from GOES ABI channels 1-16, trusted `focal_tversky` primary loss, provider-derived Centerline Target auxiliary supervision at `weighted_bce` weight 0.02, trusted `random_mirroring`, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.

The controlled manifest change was selecting provider/Harness-owned `mit_only` sampling traversal instead of ABI-068's `combined_source_balanced` traversal. The hypothesis was that MIT-only training might improve ABI-068's weaker MIT operating point or connectivity while exposing the Google transfer cost. This is capped representative data-policy evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-115 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI Channel Input and approved-channel BTD combinations. It did not introduce candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: mit_only`, `data.augmentation_policy: random_mirroring`, `training.loss: focal_tversky`, and auxiliary output `centerline_logits` with trusted `weighted_bce` weight 0.02. `outputs/model_summary.json` reported 12,087,561 parameters against the 25,000,000-parameter smoke ceiling.

The Run completed at batch size 4 on the A100 with 2,704.5 seconds total wall time, 1,306.6 seconds training wall time, 1,395.9 seconds validation wall time, 9,539,944,448 bytes peak CUDA reserved, and no terminal execution failure. It processed 2,048 capped training samples and 2,048 capped validation samples per epoch. The selected best-validation checkpoint was epoch 9; final epoch 12 was lower on filtered Dice.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, source-balanced | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | BCE-Dice-clDice precision/connectivity reference | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260830_021504_c112f8` | ABI-096 | ABI-068 branch, deterministic-shuffle sampling | 10 | 0.3628 | 0.3472 | 0.4024 | 0.4242 | 0.3169 | 0.4195 | 0.00271 |
| `run_20260830_101145_b69d10` | ABI-106 | ABI-068 branch, `google_only` sampling | 12 | 0.3590 | 0.3338 | 0.4199 | 0.3391 | 0.3815 | 0.3100 | 0.00408 |
| `run_20260830_235533_487b1c` | ABI-115 | ABI-068 branch, `mit_only` sampling | 9 | 0.3515 | 0.3588 | 0.3345 | 0.3085 | 0.4084 | 0.2795 | 0.00480 |

ABI-115 did not meet the preregistered useful-continuation criteria. Relative to ABI-068, aggregate filtered Dice decreased from 0.3964 to 0.3515 (-0.0449), Google filtered Dice decreased from 0.4161 to 0.3345 (-0.0816), MIT filtered Dice decreased from 0.3886 to 0.3588 (-0.0298), precision decreased from 0.3992 to 0.3085 (-0.0907), connectivity decreased from 0.3900 to 0.2795 (-0.1105), and filtered predicted-positive fraction increased from 0.00357 to 0.00480. Filtered recall increased modestly from 0.3936 to 0.4084, but this was a recall/positive-area expansion with worse precision, connectivity, aggregate Dice, and source-stratified Dice.

Relative to the analogous ABI-106 Google-only run, ABI-115 was worse on aggregate filtered Dice (-0.0075), Google filtered Dice (-0.0854), precision (-0.0306), connectivity (-0.0305), and positive-area discipline, while improving MIT filtered Dice (+0.0250) and recall (+0.0269). The MIT gain over ABI-106 did not surpass ABI-068's MIT result and came with substantially weaker Google transfer.

Relative to ABI-066, ABI-115 lost aggregate Dice (-0.0310), MIT Dice (-0.0050), Google Dice (-0.0947), precision (-0.1342), connectivity (-0.1936), and positive-area discipline, while improving recall (+0.0717). The result therefore does not challenge ABI-066's precision/connectivity reference role.

## ABI-115 trajectory

ABI-115 trained finitely and avoided terminal all-negative or all-positive collapse, but its trajectory was unstable and peaked before the final budget. Filtered Dice by epoch was 0.2374, 0.2811, 0.2105, 0.2740, 0.3020, 0.2797, 0.3109, 0.3291, 0.3515, 0.2956, 0.3155, and 0.3146. The selected checkpoint was epoch 9; epochs 10-12 shifted toward a larger positive mask area and lower precision.

At the selected checkpoint, filtered Dice was 0.3515, raw Dice 0.3623, filtered precision 0.3085, filtered recall 0.4084, filtered connectivity 0.2795, and filtered predicted-positive fraction 0.00480. Source-stratified filtered Dice was 0.3588 MIT and 0.3345 Google. The final checkpoint at epoch 12 had still higher recall (0.4817) but lower Dice (0.3146), lower precision (0.2336), lower connectivity (0.2216), lower Google Dice (0.2839), and a larger filtered predicted-positive fraction (0.00747), which supports the interpretation that the branch moved into recall-heavy clutter rather than stable MIT specialization.

Raw-to-filtered differences were modest at the best checkpoint: raw Dice 0.3623 versus filtered Dice 0.3515, and raw predicted-positive fraction 0.00512 versus filtered 0.00480. This is not primarily an Artifact Filter dependence issue. The fixed first-four retained prediction samples included one perfect empty-mask case and three near-zero-Dice positive cases; because retention is fixed `first_n`, these are bounded artifacts rather than representative qualitative evidence.

## Interpretation

Classify ABI-115 as finite, resource-feasible, non-collapsed, and negative capped evidence for the exact MIT-only data-policy branch. It did not improve MIT filtered Dice over ABI-068, failed the Google-source floor from the proposal, and showed a recall-heavy positive-area expansion with weaker precision and connectivity. The data-policy contrast is useful diagnostically: Google-only traversal produced a small Google-oriented shift but hurt MIT and aggregate metrics, while MIT-only traversal did not produce the symmetric hoped-for MIT improvement and damaged Google transfer more severely.

Together with ABI-096 and ABI-106, ABI-115 argues against simple allowlisted traversal swaps as the next high-value axis for the current ABI-068 architecture. `combined_source_balanced` remains the better default for this branch because it preserved the strongest aggregate Dice, better source balance, and more stable precision/connectivity tradeoff under the current capped 12-epoch constant-LR budget.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-115 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-115. Stop the exact ABI-068 architecture plus focal-Tversky plus centerline auxiliary branch with `mit_only` sampling. Do not request whole-validation diagnostics for ABI-115 ahead of ABI-068 or ABI-066, because it did not improve the balanced reference, the MIT-source reference, or the precision/connectivity reference.

Retain ABI-068 as the local aggregate-Dice reference and ABI-066 as the precision/connectivity reference for the frequency-gated line U-Net family. Prefer `combined_source_balanced` traversal for this branch unless a materially different provider-owned data-policy capability is introduced. The next useful hypothesis should broaden away from simple sampling traversal swaps and small auxiliary variants toward a materially different contract-compliant calibration, false-positive suppression, source-robustness, or thin-line continuity mechanism, while continuing to leave thresholding, Artifact Filters, data loading, sampling implementation, augmentation implementation, target derivation, losses, metrics, resource placement, and lifecycle behavior to the provider/Harness.

## Artifact references

- `run_20260830_235533_487b1c/outputs/best_metrics.json`
- `run_20260830_235533_487b1c/outputs/final_metrics.json`
- `run_20260830_235533_487b1c/outputs/metrics.jsonl`
- `run_20260830_235533_487b1c/outputs/resource_profile.json`
- `run_20260830_235533_487b1c/outputs/model_summary.json`
- `run_20260830_235533_487b1c/outputs/prediction_samples/samples.json`
- `run_20260830_235533_487b1c/resolved_manifest.yaml`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260830_021504_c112f8/outputs/best_metrics.json`
- `run_20260830_101145_b69d10/outputs/best_metrics.json`
