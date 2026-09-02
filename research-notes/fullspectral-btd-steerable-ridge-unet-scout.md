# Full-spectral BTD steerable ridge U-Net scout

research-figures: []

## Scope

This note records ABI-072 after Run `run_20260828_050329_c01ecf` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice and whole-validation reference: `run_20260828_010836_4ccc77`
- ABI-071 soft evidence-gate negative local follow-up: `run_20260828_040651_cb9403`
- ABI-072 steerable ridge U-Net scout: `run_20260828_050329_c01ecf`

ABI-072 used provider-approved `abi_16ch` inputs, ABI-channel-derived thermal BTD features, a learned 1x1 spectral mixture, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, trusted focal-Tversky primary loss, and the provider-derived `centerline` auxiliary target at trusted `weighted_bce` weight 0.02. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-scout evidence rather than full-data promotion evidence.

## ABI-072 implementation and resource observation

ABI-072 broadened away from late post-decoder suppression/gating by integrating non-suppressive steerable ridge-context blocks throughout a compact U-Net backbone. The ridge blocks softly mixed local residual detail with horizontal, vertical, and diagonal line-context branches in the stem, encoder, bottleneck, decoder, and multi-scale head. The hypothesis was that oriented backbone context could preserve ABI-068-like recall while recovering some ABI-066-like precision, connectivity, or lower predicted-positive burden without candidate-owned thresholding, postprocessing, Artifact Filters, data loading, losses, metrics, target derivation, or augmentation.

The Run stayed inside the Candidate Experiment Contract: no longitude/latitude inputs, no reconstructed coordinate inputs, no candidate-owned data loading, no custom loss or target derivation, no candidate-owned augmentation, no metrics, no thresholding, no Artifact Filters, no postprocessing, no network access, and no pretrained weights.

Model summary reported 20,097,759 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on an A100 with 2,809.1 seconds wall time, 10,506,731,520 bytes peak CUDA reserved, and no terminal execution failure.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260828_040651_cb9403` | ABI-071 | ABI-068 plus neutral soft feature-space evidence gate | 12 | 0.3712 | 0.3649 | 0.3867 | 0.3503 | 0.3947 | 0.2251 | 0.00408 |
| `run_20260828_050329_c01ecf` | ABI-072 | steerable ridge-context U-Net backbone, `focal_tversky`, centerline aux weight 0.02 | 10 | 0.3228 | 0.3236 | 0.3210 | 0.2720 | 0.3968 | 0.1675 | 0.00529 |

ABI-072 did not satisfy its main success criterion. Relative to ABI-068, aggregate filtered Dice fell by about -0.0736, MIT filtered Dice by about -0.0650, Google filtered Dice by about -0.0951, filtered precision by about -0.1272, and filtered connectivity by about -0.2225. Filtered recall was essentially preserved or slightly higher (+0.0032), but the filtered predicted-positive fraction increased from 0.00357 to 0.00529 instead of decreasing.

Relative to ABI-066, ABI-072 gained recall (+0.0601) but lost aggregate filtered Dice (-0.0598), precision (-0.1707), connectivity (-0.3056), and Google filtered Dice (-0.1082). Relative to ABI-071, the steerable ridge scout lost aggregate filtered Dice (-0.0484), precision (-0.0783), connectivity (-0.0576), and increased predicted-positive burden, while recall stayed nearly tied.

## ABI-072 trajectory

ABI-072 trained finitely and avoided all-negative/all-positive prediction collapse. The best checkpoint was epoch 10, not the final epoch. Filtered Dice moved from 0.1423 at epoch 1 to 0.1821, 0.2068, 0.1948, 0.2721, 0.2684, 0.2499, 0.2571, 0.3172, 0.3228, 0.3035, and 0.3173 at epoch 12.

The trajectory shows late improvement from the early low-Dice regime but no convincing late-epoch recovery toward the ABI-066/ABI-068 references. The best checkpoint was source-balanced enough to avoid a catastrophic source-specific collapse by the proposal's scout floor: MIT filtered Dice was 0.3236 and Google filtered Dice was 0.3210. The operating profile, however, was not useful: filtered precision was only 0.2720, connectivity only 0.1675, and filtered predicted-positive fraction 0.00529. The model preserved recall by predicting a larger positive area, not by finding a better line-continuity or clutter-control tradeoff.

The fixed first-four retained prediction artifacts should not be treated as representative qualitative evidence. The useful evidence for this capped Run is the aggregate/source-stratified validation metrics, the non-degenerate predicted-positive fractions, and the epoch trajectory above.

## Interpretation

Classify ABI-072 as negative capped family-scout evidence for this exact steerable-ridge configuration, not as an execution failure and not as proof that all oriented-context architectures are invalid. The candidate completed reliably within contract and resource limits, and both Dataset Sources remained finite and non-collapsed. But the intended non-suppressive oriented context did not recover ABI-066-style precision/connectivity or improve ABI-068's recall-forward operating point.

Together with ABI-069/070/071, this suggests that local head suppression/gating and this high-capacity steerable ridge backbone both fail to improve the current frequency-gated reference under the active capped policy. ABI-068 remains the current strongest local candidate by capped aggregate filtered Dice among the observed full-spectral BTD line-model family, with ABI-066 retained as the precision/connectivity-forward reference. Canonical MCAST 2.1 remains the full Working Validation Split promotion context.

ABI-072 does not justify promotion interpretation or a whole-validation Evaluation Request. It also should not be repeated unchanged: its added parameter/resource cost produced lower Dice, lower precision, lower connectivity, and higher predicted-positive burden than the lighter ABI-068 reference.

## Decision

Do not promote ABI-072 and do not continue this exact steerable-ridge configuration unchanged. Retain it as evidence that dense horizontal/vertical/diagonal ridge-context insertion throughout this compact U-Net is too clutter-permissive at the current focal-Tversky, centerline-auxiliary operating point.

The next useful research step should broaden beyond the current post-head gating and heavy steerable-ridge variants. In-contract options include returning to the ABI-068 frequency-gated backbone with a more targeted low-capacity continuity module, changing an allowlisted training/loss/auxiliary-weight factor, or scouting a materially different thin-line architecture that preserves provider/Harness ownership of losses, auxiliary targets, sampling, augmentation, metrics, thresholding, Artifact Filters, and data handling.

## Artifact references

- `run_20260828_050329_c01ecf/outputs/best_metrics.json`
- `run_20260828_050329_c01ecf/outputs/final_metrics.json`
- `run_20260828_050329_c01ecf/outputs/metrics.jsonl`
- `run_20260828_050329_c01ecf/outputs/resource_profile.json`
- `run_20260828_050329_c01ecf/outputs/model_summary.json`
- `run_20260828_050329_c01ecf/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260828_040651_cb9403/outputs/best_metrics.json`
