# Full-spectral BTD frequency-gated line U-Net conservative-skip follow-up

research-figures: []

## Scope

This note records ABI-105 after Run `run_20260830_091941_139456` completed.

Source Runs:

- ABI-105 conservative-skip frequency-gated focal-Tversky continuation: `run_20260830_091941_139456`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-099 directional line-coherence-gate negative follow-up: `run_20260830_044731_a5c0bf`
- ABI-103 dual-stream spectral-gate scout: `run_20260830_074456_5e0e5c`
- ABI-104 dual-stream line-consensus continuation: `run_20260830_083020_16590b`

ABI-105 was a family-development continuation of ABI-068. It retained ABI-068's full-spectral ABI plus thermal BTD frequency-gated line U-Net setup, trusted focal-Tversky primary loss, provider-derived Centerline Target auxiliary supervision, trusted random mirroring, and provider-owned combined source-balanced traversal. The controlled architecture change was in decoder skip fusion: instead of ABI-068's amplifying skip gate `0.5 + sigmoid(gate)` with range 0.5x to 1.5x, ABI-105 used `0.35 + 0.65 * sigmoid(gate)`, a non-amplifying range of 0.35x to 1.0x. The hypothesis was that earlier conservative skip fusion might reduce uncorroborated high-resolution clutter without adding output-side thresholding, postprocessing, Artifact Filters, or late mask-head machinery.

The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, provider-approved `abi_16ch` input, trusted `focal_tversky`, trusted `random_mirroring`, provider-owned `combined_source_balanced` traversal, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and a provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. This is capped family-development evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-105 stayed inside the Candidate Experiment Contract. Candidate code owned only architecture over provider-approved ABI tensors and deterministic BTD features derived from approved ABI channels. It did not introduce candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.

`outputs/model_summary.json` reported 12,087,561 parameters against the 25,000,000-parameter smoke ceiling. The model summary confirmed GOES ABI channels 1-16 only, forbidden longitude/latitude source channels excluded, and outputs `mask_logits` plus `centerline_logits`. The Run completed at batch size 4 on the A100 with 2,718.2 seconds total wall time, 1,310.0 seconds training wall time, 1,405.9 seconds validation wall time, 9,539,944,448 bytes peak CUDA reserved, and no terminal execution failure. ABI-105 was therefore resource-feasible under the current capped sequential policy.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260830_091941_139456` | ABI-105 | ABI-068 branch with non-amplifying decoder skip gates | 12 | 0.3831 | 0.3820 | 0.3857 | 0.3344 | 0.4484 | 0.2520 | 0.00486 |
| `run_20260830_044731_a5c0bf` | ABI-099 | ABI-068 branch plus directional line-coherence gate | 11 | 0.3401 | 0.3499 | 0.3187 | 0.2558 | 0.5074 | 0.1421 | 0.00719 |
| `run_20260830_074456_5e0e5c` | ABI-103 | dual-stream spectral-gate line U-Net scout | 12 | 0.3305 | 0.3248 | 0.3427 | 0.2715 | 0.4225 | 0.1742 | 0.00564 |
| `run_20260830_083020_16590b` | ABI-104 | ABI-103 branch, consensus-gated line decoder | 9 | 0.3220 | 0.3140 | 0.3389 | 0.2739 | 0.3904 | 0.1733 | 0.00516 |

ABI-105 did not meet the preregistered useful-continuation criteria. Relative to ABI-068, aggregate filtered Dice decreased by about 0.0133, MIT filtered Dice decreased by about 0.0066, Google filtered Dice decreased by about 0.0304, filtered precision decreased by about 0.0648, and filtered connectivity decreased by about 0.1380. Filtered recall increased by about 0.0547, but the filtered predicted-positive fraction increased from 0.00357 to 0.00486, about a 36% relative increase rather than the hoped-for 10% reduction.

Relative to ABI-066, ABI-105 was essentially tied on aggregate filtered Dice but lost about 0.1083 filtered precision, 0.2211 filtered connectivity, and 0.0435 Google filtered Dice while gaining about 0.1117 filtered recall and 0.0182 MIT filtered Dice. This keeps ABI-105 in a recall-forward operating regime rather than moving it toward ABI-066's precision/connectivity profile.

ABI-105 was stronger than recent low-precision branches such as ABI-099, ABI-103, and ABI-104 by aggregate Dice and source balance, but that comparison does not rescue the exact conservative-skip hypothesis. The controlled change was expected to lower high-resolution clutter; instead it produced lower precision/connectivity and higher predicted-positive area than ABI-068.

## ABI-105 trajectory

ABI-105 trained finitely and avoided terminal all-negative/all-positive collapse. Filtered Dice by epoch was 0.2385, 0.2465, 0.2976, 0.3079, 0.3150, 0.2907, 0.3264, 0.3499, 0.3654, 0.3769, 0.3657, and 0.3831. The selected checkpoint was the final epoch 12, so the trajectory was late-improving rather than plateaued or divergent.

At the selected checkpoint, filtered Dice was 0.3831, filtered precision 0.3344, filtered recall 0.4484, filtered connectivity 0.2520, and filtered predicted-positive fraction 0.00486. Source-stratified filtered Dice was balanced at 0.3820 MIT and 0.3857 Google, with Google recall 0.5291 and MIT recall 0.4208. Training loss declined from 0.9301 at epoch 1 to 0.8517 at epoch 12, while validation loss declined from 0.9197 to 0.8797.

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice 0.3949 versus filtered Dice 0.3831, and raw predicted-positive fraction 0.00519 versus filtered 0.00486. This is not primarily an Artifact Filter dependence issue. The fixed first-four retained prediction samples include one perfect empty-mask case and three near-zero sample-Dice cases in `outputs/prediction_samples/samples.json`; because prediction retention is fixed `first_n`, these are bounded artifacts and not representative qualitative evidence.

## Interpretation

Classify ABI-105 as finite, resource-feasible, source-balanced, non-collapsed, but negative capped family-development evidence for the exact conservative-skip branch. It isolates skip amplification as unlikely to be the main lever behind ABI-068's false-positive burden under the current trusted focal-Tversky, centerline-auxiliary, random-mirroring, combined source-balanced, constant-LR budget. Preventing skip amplification did not improve precision, connectivity, or positive-area discipline; instead it shifted the operating point toward higher recall with lower precision/connectivity.

The late-improving trajectory and balanced source metrics argue against treating ABI-105 as a broken implementation or a broad family collapse. However, the branch matches the proposal's hard-stop pattern for this exact mechanism: compared with ABI-068, it has lower precision, lower connectivity, higher predicted-positive fraction, and no primary-metric gain. Small additional skip-range tuning is therefore unlikely to be a useful next step.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-105 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-105. Do not request whole-validation failure-bucket diagnostics for this exact checkpoint ahead of ABI-068/066-style references. Stop the conservative-skip branch and avoid further small decoder skip-gate range adjustments unless a future hypothesis changes a materially different mechanism.

Retain ABI-068 as the local aggregate-Dice reference and ABI-066 as the precision/connectivity reference. A future useful hypothesis should broaden away from additive late gates and small skip-gate calibrations toward a materially different contract-compliant mechanism for precision, calibration, or thin-line connectivity, while preserving provider/Harness ownership of thresholding, Artifact Filters, data loading, split logic, sampling implementation, augmentation implementation, target derivation, losses, metrics, resource placement, and lifecycle behavior.

## Artifact references

- `run_20260830_091941_139456/outputs/best_metrics.json`
- `run_20260830_091941_139456/outputs/final_metrics.json`
- `run_20260830_091941_139456/outputs/metrics.jsonl`
- `run_20260830_091941_139456/outputs/resource_profile.json`
- `run_20260830_091941_139456/outputs/model_summary.json`
- `run_20260830_091941_139456/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260830_044731_a5c0bf/outputs/best_metrics.json`
- `run_20260830_074456_5e0e5c/outputs/best_metrics.json`
- `run_20260830_083020_16590b/outputs/best_metrics.json`
