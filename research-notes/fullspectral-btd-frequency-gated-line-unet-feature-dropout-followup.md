# Full-spectral BTD frequency-gated line U-Net feature-dropout follow-up

research-figures: []

## Scope

This note records ABI-107 after Run `run_20260830_110428_804d89` completed.

Source Runs:

- ABI-107 feature-dropout regularization continuation: `run_20260830_110428_804d89`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-105 conservative-skip focal-Tversky continuation: `run_20260830_091941_139456`
- ABI-106 Google-only data-policy continuation: `run_20260830_101145_b69d10`

ABI-107 was a family-development continuation of ABI-068. It retained the ABI-068 full-spectral ABI plus deterministic thermal BTD frequency-gated line U-Net architecture, trusted focal-Tversky primary loss, provider-derived Centerline Target auxiliary supervision, trusted `combined_source_balanced` traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, and disabled early stopping. The controlled architecture change was adding low-probability `Dropout2d` regularization to intermediate feature tensors.

The hypothesis was that feature dropout would reduce brittle high-resolution clutter and source-specific spectral shortcuts while preserving ABI-068-like recall and source balance. This is capped representative evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-107 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved `abi_16ch` tensors and deterministic BTD features derived from approved GOES ABI channels. It did not introduce candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: focal_tversky`, and one `centerline_logits` auxiliary output with `weighted_bce` weight 0.02. `outputs/model_summary.json` reported 12,087,561 parameters against the 25,000,000-parameter smoke ceiling, confirmed GOES ABI channels 1-16 only with forbidden longitude/latitude source channels excluded, and confirmed outputs `mask_logits` plus `centerline_logits`.

The Run completed at batch size 4 on the A100 with 2,686.7 seconds total wall time, 1,311.8 seconds training wall time, 1,372.8 seconds validation wall time, 9,552,527,360 bytes peak CUDA reserved, and no terminal execution failure. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap; final and best-validation checkpoint was epoch 12.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, source-balanced | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, source-balanced | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260830_091941_139456` | ABI-105 | ABI-068 branch, non-amplifying decoder skip gates | 12 | 0.3831 | 0.3820 | 0.3857 | 0.3344 | 0.4484 | 0.2520 | 0.00486 |
| `run_20260830_101145_b69d10` | ABI-106 | ABI-068 branch, `google_only` sampling | 12 | 0.3590 | 0.3338 | 0.4199 | 0.3391 | 0.3815 | 0.3100 | 0.00408 |
| `run_20260830_110428_804d89` | ABI-107 | ABI-068 branch, low-probability feature dropout | 12 | 0.3804 | 0.3701 | 0.4046 | 0.3630 | 0.3997 | 0.3182 | 0.00399 |

ABI-107 did not meet the preregistered useful-continuation criteria. Relative to ABI-068, aggregate filtered Dice decreased from 0.3964 to 0.3804 (-0.0159), which is not catastrophic but misses the within-0.01 retention criterion. Filtered precision decreased by 0.0362, filtered connectivity decreased by 0.0718, and filtered predicted-positive fraction increased by about 11.7% rather than dropping by at least 10%. Filtered recall was essentially preserved, increasing from 0.3936 to 0.3997 (+0.0061), and both Dataset Sources stayed above 0.36 filtered Dice, but aggregate Dice did not improve.

Relative to ABI-066, ABI-107 had similar aggregate filtered Dice (-0.0021) but much lower precision (-0.0798), much lower connectivity (-0.1549), higher recall (+0.0629), and a larger predicted-positive fraction. Relative to ABI-105, ABI-107 recovered precision, connectivity, and positive-area discipline while giving up recall, but it still did not recover ABI-068's aggregate/source Dice or connectivity. Relative to ABI-106, ABI-107 improved aggregate and MIT Dice while giving back ABI-106's small Google-specialized advantage.

## ABI-107 trajectory

ABI-107 trained finitely and avoided terminal all-negative or all-positive collapse. Filtered Dice by epoch was 0.1973, 0.2222, 0.3036, 0.3033, 0.3349, 0.2784, 0.3124, 0.3441, 0.3611, 0.3547, 0.2767, and 0.3804. The selected checkpoint was epoch 12, so the run ended at its best validation point after a large epoch-11 dip. The trajectory is therefore noisy but not divergent.

At the selected checkpoint, filtered Dice was 0.3804, filtered precision 0.3630, filtered recall 0.3997, filtered connectivity 0.3182, and filtered predicted-positive fraction 0.00399. Source-stratified filtered Dice remained non-catastrophic but lower than ABI-068 on both sources: MIT 0.3701 and Google 0.4046. Training loss declined from 0.9317 at epoch 1 to 0.8556 at epoch 12, while validation loss moved from 0.9235 to 0.8824.

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice 0.3930 versus filtered Dice 0.3804, and raw predicted-positive fraction 0.00425 versus filtered 0.00399. This is not primarily an Artifact Filter dependence issue. The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` contain one empty/easy perfect sample and three near-zero-Dice samples; because prediction retention is fixed `first_n`, these are bounded artifacts and not representative qualitative evidence.

## Interpretation

Classify ABI-107 as finite, resource-feasible, non-collapsed, and useful negative capped evidence for the exact feature-dropout regularization branch. Feature dropout preserved ABI-068-like recall but failed to improve the intended clutter-control axes. The result suggests that this branch's bottleneck is not simple feature co-adaptation: adding dropout reduced neither positive-area burden nor false-positive pressure relative to ABI-068, and it damaged the connectivity signal that ABI-066 preserved better under BCE-Dice-clDice.

The result also reinforces the recent pattern that small local modifications around ABI-068 tend to trade precision, recall, connectivity, source balance, and positive area without a clear capped aggregate improvement. ABI-105 pushed recall up with worse precision/connectivity; ABI-106 shifted toward Google at MIT/aggregate cost; ABI-107 preserved recall but lost ABI-068's precision and connectivity. This does not eliminate the frequency-gated line U-Net family as a whole, but it weakens the case for further same-family small gates, sampling swaps, or regularizers unless tied to a sharper diagnostic hypothesis.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-107 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-107. Stop this exact feature-dropout branch and do not spend another step tuning only dropout placement or probability. Retain ABI-068 as the local aggregate-Dice reference and ABI-066 as the precision/connectivity reference for the frequency-gated line U-Net family.

No whole-validation failure-bucket evaluation is requested for ABI-107 at this point; ABI-068 and ABI-066 already have higher-priority whole-validation diagnostics for the same family. A future useful hypothesis should broaden beyond small same-family regularization toward a materially different contract-compliant mechanism for calibration, false-positive suppression, thin-line connectivity, or spectral/source robustness, while preserving provider/Harness ownership of thresholding, Artifact Filters, data loading, split logic, sampling implementation, augmentation implementation, target derivation, losses, metrics, resource placement, and lifecycle behavior.

## Artifact references

- `run_20260830_110428_804d89/outputs/best_metrics.json`
- `run_20260830_110428_804d89/outputs/final_metrics.json`
- `run_20260830_110428_804d89/outputs/metrics.jsonl`
- `run_20260830_110428_804d89/outputs/resource_profile.json`
- `run_20260830_110428_804d89/outputs/model_summary.json`
- `run_20260830_110428_804d89/outputs/prediction_samples/samples.json`
- `run_20260830_110428_804d89/resolved_manifest.yaml`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260830_091941_139456/outputs/best_metrics.json`
- `run_20260830_101145_b69d10/outputs/best_metrics.json`
