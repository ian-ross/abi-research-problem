# Full-spectral BTD dual-decoder region/line U-Net scout

research-figures: []

## Scope

This note records ABI-090 after Run `run_20260829_222651_34a8d2` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-085 low-learning-rate focal-Tversky continuation: `run_20260829_181201_01c5e7`
- ABI-089 context/detail agreement continuation: `run_20260829_212901_6bbc6f`
- ABI-090 dual-decoder region/line U-Net scout: `run_20260829_222651_34a8d2`

ABI-090 used provider-approved `abi_16ch` input only, ABI-channel-derived thermal brightness-temperature-difference features, combined source-balanced sampling, trusted `random_mirroring`, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, trusted `focal_tversky` primary loss, and a provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. The controlled architecture change was a two-stream decoder: one smooth region-context path and one high-frequency line-detail path, fused before the primary mask head with `centerline_logits` emitted from the line/detail stream. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-scout evidence rather than full-data promotion evidence.

## ABI-090 implementation and resource observation

ABI-090 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI tensors and BTD planes derived from approved ABI channels. It did not introduce candidate-owned data loading, sampling, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, pretrained weights, or longitude/latitude inputs.

Model summary reported 14,998,394 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 2,492.5 seconds wall time, 8,640,266,240 bytes peak CUDA reserved, and no terminal execution failure. Resource behavior was feasible under the current 3,600-second Docker training timeout and was lighter/faster than ABI-089 despite the two-stream decoder.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, `focal_tversky`, random mirroring, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | same family, `bce_dice_cldice`, random mirroring, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260829_181201_01c5e7` | ABI-085 | ABI-068 architecture/loss/aux, learning rate 0.0001 | 12 | 0.3826 | 0.3733 | 0.4059 | 0.3693 | 0.3968 | 0.3698 | 0.00389 |
| `run_20260829_212901_6bbc6f` | ABI-089 | context/detail agreement fusion before oriented line refinement | 12 | 0.3644 | 0.3599 | 0.3748 | 0.3404 | 0.3920 | 0.2374 | 0.00417 |
| `run_20260829_222651_34a8d2` | ABI-090 | two-stream region-context and line-detail decoder | 12 | 0.3547 | 0.3552 | 0.3536 | 0.3250 | 0.3905 | 0.2192 | 0.00435 |

ABI-090 did not meet its strongest local comparison targets. Relative to ABI-068, aggregate filtered Dice fell by about -0.0417, MIT filtered Dice by about -0.0334, Google filtered Dice by about -0.0625, precision by about -0.0742, recall by about -0.0031, and filtered connectivity by about -0.1708. The filtered predicted-positive fraction rose from 0.00357 to 0.00435, so splitting the decoder did not improve positive-area discipline.

Relative to ABI-066, ABI-090 recovered recall by about +0.0537 but lost aggregate Dice, both source-stratified Dice values, precision, connectivity, and positive-area control. Relative to ABI-085, ABI-090 also lost aggregate Dice, source Dice, precision, recall, connectivity, and positive-area discipline. Relative to ABI-089, ABI-090 was slightly worse on aggregate Dice, precision, recall, connectivity, and predicted-positive fraction, though it retained similar source balance and improved resource use.

## ABI-090 trajectory

Filtered Dice by epoch was 0.1732, 0.1864, 0.1734, 0.2630, 0.2745, 0.3003, 0.2631, 0.3272, 0.3120, 0.3336, 0.2905, and 0.3547. The selected checkpoint was epoch 12. The trajectory was finite and late-improving, with both Dataset Sources just above 0.35 at the selected epoch (MIT 0.3552; Google 0.3536), so this is not prediction collapse or an execution failure.

The trajectory was nevertheless noisy and remained below the ABI-068/066/085 band. Epoch 11 briefly shifted to very high recall (0.5312) with low precision (0.1999) and a high filtered predicted-positive fraction (0.00963), then epoch 12 returned to a more balanced but lower-Dice operating point. This mirrors ABI-089's instability pattern more than it solves it: the architecture can recover contrail pixels, but the region/line split did not supply a stable precision or connectivity advantage under the current constant learning-rate, 12-epoch capped policy.

The retained fixed first-four prediction samples all had near-zero sample Dice in `outputs/prediction_samples/samples.json`. Because prediction retention is fixed `first_n`, these are bounded artifacts and not representative qualitative evidence; aggregate and source-stratified validation metrics carry this decision.

## Interpretation

Classify ABI-090 as finite, resource-feasible, source-balanced but negative capped family-scout evidence for this exact dual-decoder design. The weak positive signal is that both MIT and Google filtered Dice cleared 0.35 and the best checkpoint was the final epoch. The stronger negative signal is that the dual-decoder branch did not recover ABI-066-like precision/connectivity, did not preserve ABI-068-like aggregate Dice, and slightly worsened the ABI-089 positive-area/precision/connectivity pattern it was meant to address.

This result does not eliminate all possible two-stream or multi-branch architectures, because the Run is finite, late-improving, and source-balanced. It does argue against repeating this exact region-context/line-detail decoder split unchanged as the next local move. The broader frequency-gated line U-Net family remains anchored by ABI-068 as the best capped primary-metric reference and ABI-066 as the precision/connectivity-forward reference.

Canonical MCAST 2.1 remains the promotion context, and all comparisons here are capped representative family-development evidence unless an explicitly requested whole-validation diagnostic is run.

## Decision

Do not promote ABI-090. Do not request whole-validation failure-bucket diagnostics for ABI-090 ahead of stronger references, because it did not improve aggregate Dice or secondary precision/connectivity behavior over ABI-068/066 and did not supply a unique failure mode beyond the recent post-decoder/two-stream variants.

Do not repeat the exact ABI-090 region/line dual-decoder branch unchanged. Future work should broaden away from additional ABI-068 post-decoder gates and same-decoder variants. A useful next hypothesis should either change architecture family more substantially or move along a clearly different trusted policy axis while keeping thresholding, Artifact Filters, data loading, sampling, augmentation implementation, target derivation, losses, metrics, resource placement, and lifecycle behavior out of Candidate code.

## Artifact references

- `run_20260829_222651_34a8d2/outputs/best_metrics.json`
- `run_20260829_222651_34a8d2/outputs/final_metrics.json`
- `run_20260829_222651_34a8d2/outputs/metrics.jsonl`
- `run_20260829_222651_34a8d2/outputs/resource_profile.json`
- `run_20260829_222651_34a8d2/outputs/model_summary.json`
- `run_20260829_222651_34a8d2/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260829_181201_01c5e7/outputs/best_metrics.json`
- `run_20260829_212901_6bbc6f/outputs/best_metrics.json`
