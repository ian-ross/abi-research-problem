# Full-spectral BTD frequency-gated line U-Net line+centerline auxiliary follow-up

research-figures: []

## Scope

This note records ABI-108 after Run `run_20260830_115800_4a2363` completed.

Source Runs:

- ABI-108 line+centerline auxiliary focal-Tversky continuation: `run_20260830_115800_4a2363`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-105 conservative-skip focal-Tversky continuation: `run_20260830_091941_139456`
- ABI-107 feature-dropout focal-Tversky continuation: `run_20260830_110428_804d89`

ABI-108 was a family-development continuation of ABI-068. It retained the full-spectral ABI plus deterministic thermal BTD frequency-gated line U-Net architecture, trusted focal-Tversky primary loss, provider-owned `combined_source_balanced` traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled manifest/model change was adding a provider-derived `line_logits` auxiliary output with trusted `weighted_bce` weight 0.02 alongside the existing provider-derived `centerline_logits` auxiliary output at weight 0.02.

The hypothesis was that low-weight Line Target supervision would reinforce thin-line extent or improve precision/connectivity without moving target derivation, losses, metrics, thresholding, Artifact Filters, data loading, sampling, or augmentation into Candidate code. This is capped representative evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-108 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved `abi_16ch` tensors and deterministic BTD features derived from approved GOES ABI channels. It did not introduce candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: focal_tversky`, and two auxiliary outputs: `centerline_logits` and `line_logits`, both using trusted `weighted_bce` weight 0.02. `outputs/model_summary.json` reported 12,087,606 parameters against the 25,000,000-parameter smoke ceiling, confirmed GOES ABI channels 1-16 only with forbidden longitude/latitude source channels excluded, and confirmed outputs `mask_logits`, `centerline_logits`, and `line_logits`.

The Run completed at batch size 4 on the A100 with 2,646.4 seconds total wall time, 1,314.1 seconds training wall time, 1,330.4 seconds validation wall time, 9,542,041,600 bytes peak CUDA reserved, and no terminal execution failure. The best-validation checkpoint was epoch 9; the final epoch 12 was slightly lower by filtered Dice.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, centerline aux | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, centerline aux | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260830_091941_139456` | ABI-105 | ABI-068 branch, non-amplifying decoder skip gates | 12 | 0.3831 | 0.3820 | 0.3857 | 0.3344 | 0.4484 | 0.2520 | 0.00486 |
| `run_20260830_110428_804d89` | ABI-107 | ABI-068 branch, low-probability feature dropout | 12 | 0.3804 | 0.3701 | 0.4046 | 0.3630 | 0.3997 | 0.3182 | 0.00399 |
| `run_20260830_115800_4a2363` | ABI-108 | ABI-068 branch, added Line Target auxiliary head | 9 | 0.3822 | 0.3660 | 0.4242 | 0.3938 | 0.3713 | 0.3575 | 0.00342 |

ABI-108 did not meet the preregistered useful-continuation criteria relative to ABI-068. Aggregate filtered Dice decreased from 0.3964 to 0.3822 (-0.0141), missing the within-0.01 retention criterion. Filtered precision was nearly retained but slightly lower (-0.0053), filtered recall decreased (-0.0223), and filtered connectivity decreased (-0.0325). The filtered predicted-positive fraction decreased modestly from 0.00357 to 0.00342, but not enough to offset the Dice/connectivity loss. Source behavior was mixed: Google filtered Dice improved from 0.4161 to 0.4242, while MIT filtered Dice dropped from 0.3886 to 0.3660.

Relative to ABI-066, ABI-108 was effectively tied on aggregate filtered Dice (-0.0003) and recovered more recall (+0.0346), but it remained below ABI-066 on precision (-0.0489), connectivity (-0.1156), Google filtered Dice (-0.0050), and positive-area discipline. Relative to recent ABI-105 and ABI-107 continuations, ABI-108 was cleaner than ABI-105 on precision/connectivity/positive area and cleaner than ABI-107 on precision, connectivity, and Google Dice, but it still did not recover ABI-068's aggregate Dice or source balance.

## ABI-108 trajectory

ABI-108 trained finitely and avoided terminal all-negative or all-positive collapse. Filtered Dice by epoch was 0.2443, 0.2603, 0.3080, 0.2768, 0.3472, 0.2881, 0.3111, 0.3154, 0.3822, 0.3773, 0.3334, and 0.3785. The selected checkpoint was epoch 9, after which the run remained finite but noisy: epoch 11 shifted into a high-recall/low-precision operating point before epoch 12 recovered to 0.3785 filtered Dice.

At the selected checkpoint, filtered Dice was 0.3822, filtered precision 0.3938, filtered recall 0.3713, filtered connectivity 0.3575, and filtered predicted-positive fraction 0.00342. Source-stratified filtered Dice was 0.3660 MIT and 0.4242 Google. Training loss declined from 0.9333 at epoch 1 to 0.8516 at epoch 9 and 0.8551 at epoch 12; validation loss declined from 0.9222 at epoch 1 to 0.8878 at epoch 9 and 0.8855 at epoch 12.

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice 0.3956 versus filtered Dice 0.3822, and raw predicted-positive fraction 0.00364 versus filtered 0.00342. This is not primarily an Artifact Filter dependence issue. The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` all have near-zero sample Dice; because prediction retention is fixed `first_n`, these are bounded artifacts and not representative qualitative evidence.

## Interpretation

Classify ABI-108 as finite, resource-feasible, non-collapsed, but mixed-to-negative capped family-development evidence for the exact line+centerline auxiliary branch. The additional Line Target auxiliary head did not provide the intended connectivity or precision improvement relative to ABI-068, and it weakened MIT/source-balanced behavior. It did produce a cleaner operating point than ABI-105 and ABI-107 on some axes, especially positive-area discipline and Google Dice, but the primary comparison target was ABI-068 and that target remains stronger by capped aggregate Dice, MIT Dice, recall, and connectivity.

The result suggests that simply stacking low-weight provider-derived Line Target supervision on the focal-Tversky frequency-gated branch is not enough to recover ABI-066's connectivity regime. The auxiliary signal may have shifted the branch toward more conservative positive area and better Google source behavior, but not toward a stronger aggregate or source-balanced solution. This does not eliminate the frequency-gated line U-Net family as a whole, but it weakens the case for further small auxiliary-head additions around ABI-068 unless tied to a sharper diagnostic hypothesis.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-108 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-108. Stop this exact equal-weight line+centerline auxiliary branch. Do not request whole-validation failure-bucket diagnostics for ABI-108 ahead of ABI-068/066 references because it missed the preregistered ABI-068-relative criteria and did not recover ABI-066-like connectivity.

Retain ABI-068 as the local aggregate-Dice reference and ABI-066 as the precision/connectivity reference for the frequency-gated line U-Net family. A future useful hypothesis should broaden beyond small local ABI-068 additions toward a materially different contract-compliant mechanism for calibration, false-positive suppression, source robustness, or thin-line continuity, while preserving provider/Harness ownership of thresholding, Artifact Filters, data loading, split logic, sampling implementation, augmentation implementation, target derivation, losses, metrics, resource placement, and lifecycle behavior.

## Artifact references

- `run_20260830_115800_4a2363/outputs/best_metrics.json`
- `run_20260830_115800_4a2363/outputs/final_metrics.json`
- `run_20260830_115800_4a2363/outputs/metrics.jsonl`
- `run_20260830_115800_4a2363/outputs/resource_profile.json`
- `run_20260830_115800_4a2363/outputs/model_summary.json`
- `run_20260830_115800_4a2363/outputs/prediction_samples/samples.json`
- `run_20260830_115800_4a2363/resolved_manifest.yaml`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260830_091941_139456/outputs/best_metrics.json`
- `run_20260830_110428_804d89/outputs/best_metrics.json`
