# Full-spectral BTD frequency-gated line U-Net confidence-suppressor follow-up

research-figures: []

## Scope

This note records ABI-069 after Run `run_20260828_021352_6f4329` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-069 confidence-suppressor continuation: `run_20260828_021352_6f4329`

ABI-069 used provider-approved `abi_16ch` inputs, thermal BTD features derived only from ABI channels, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped family-development results, not full-data promotion evidence.

## ABI-069 implementation and resource observation

ABI-069 started from ABI-068's full-spectral BTD frequency-gated line U-Net with trusted focal-Tversky primary loss and the provider-derived `centerline` auxiliary target at trusted `weighted_bce` weight 0.02. The controlled architecture change was replacing the direct mask head with a differentiable confidence-suppressor head intended to reduce low-confidence clutter inside the model, without candidate-owned thresholding, postprocessing, Artifact Filters, data loading, sampling, losses, metrics, or target derivation.

The Run stayed inside the Candidate Experiment Contract: no longitude/latitude inputs, no reconstructed coordinate inputs, no candidate-owned augmentation, no custom loss or target derivation, no metrics, no thresholding, no Artifact Filters, no postprocessing, no network access, and no pretrained weights.

Model summary reported 12,192,547 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on an A100 with 2,969.4 seconds wall time, 9,630,121,984 bytes peak CUDA reserved, and no terminal execution failure.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_010836_4ccc77` | ABI-068 | same family, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260828_021352_6f4329` | ABI-069 | ABI-068 plus differentiable confidence-suppressor head | 10 | 0.3711 | 0.3602 | 0.3955 | 0.3789 | 0.3635 | 0.1451 | 0.00348 |

ABI-069 did not meet the proposal's competitive criterion. Relative to ABI-068, it lost about -0.0253 filtered Dice, -0.0284 MIT filtered Dice, -0.0206 Google filtered Dice, -0.0203 precision, -0.0301 recall, and -0.2449 connectivity. The intended clutter proxy improved only marginally: filtered predicted-positive fraction decreased from 0.00357 to 0.00348, not enough to offset the Dice, recall, and connectivity regression.

Relative to ABI-066, ABI-069 retained some recall-forward behavior (+0.0268 filtered recall) but was worse on filtered Dice (-0.0115), precision (-0.0638), connectivity (-0.3280), and predicted-positive fraction (+0.00072). It therefore does not recover ABI-066's precision/connectivity profile and does not improve ABI-068's aggregate-Dice profile.

## ABI-069 trajectory

ABI-069 trained finitely and avoided all-negative/all-positive prediction collapse. Filtered Dice improved from 0.2311 at epoch 1 to 0.3352 at epoch 5, dipped, then reached a narrow plateau at epochs 9 and 10: 0.3707 and the selected best 0.3711. It then regressed to 0.3634 at epoch 11 and 0.3441 at epoch 12.

At the selected best checkpoint, both Dataset Sources remained non-catastrophic by the proposal floor: MIT filtered Dice was 0.3602 and Google filtered Dice was 0.3955. However, filtered connectivity was very weak at 0.1451, well below ABI-068 and ABI-066. The confidence-suppressor head appears to suppress useful continuous line evidence along with a small amount of predicted-positive burden.

The fixed first-four prediction artifacts all had near-zero sample Dice. As in previous notes, these first-n artifacts are not representative qualitative evidence; aggregate and source-stratified validation metrics are the useful evidence for this capped Run.

## Interpretation

Classify ABI-069 as a finite but negative capped family-development result. It is not a contract/resource failure and it does not eliminate the broader frequency-gated line U-Net family, but this exact confidence-suppressor head did not provide the desired tradeoff. The architecture-side suppression mechanism produced only a small reduction in predicted-positive fraction while materially weakening aggregate Dice, recall, and especially connectivity.

ABI-068 remains the local aggregate-Dice reference and strongest whole-validation-tested Candidate in this branch. ABI-066 remains the precision/connectivity-forward reference. ABI-069 should not be promoted and does not justify a whole-validation failure-bucket evaluation before a stronger capped signal appears.

## Decision

Do not repeat or promote this exact ABI-069 confidence-suppressor branch. A safer next hypothesis should either return to ABI-068 and test a less suppressive precision-recovery mechanism, or broaden to a different in-contract architecture family that preserves line continuity while controlling negative-patch clutter without candidate-owned thresholding or Artifact Filters.

## Artifact references

- `run_20260828_021352_6f4329/outputs/best_metrics.json`
- `run_20260828_021352_6f4329/outputs/final_metrics.json`
- `run_20260828_021352_6f4329/outputs/metrics.jsonl`
- `run_20260828_021352_6f4329/outputs/resource_profile.json`
- `run_20260828_021352_6f4329/outputs/model_summary.json`
- `run_20260828_021352_6f4329/outputs/prediction_samples/samples.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
