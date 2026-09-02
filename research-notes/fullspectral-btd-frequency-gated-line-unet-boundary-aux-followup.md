# Full-spectral BTD frequency-gated line U-Net boundary-auxiliary follow-up

research-figures: []

## Scope

This note records ABI-073 after Run `run_20260828_055812_4ba74e` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice and whole-validation reference: `run_20260828_010836_4ccc77`
- ABI-070 centerline-guided residual head comparison: `run_20260828_031118_326c4a`
- ABI-072 steerable-ridge negative architecture scout: `run_20260828_050329_c01ecf`
- ABI-073 frequency-gated line U-Net with centerline and boundary auxiliary heads: `run_20260828_055812_4ba74e`

ABI-073 used provider-approved `abi_16ch` inputs, ABI-channel-derived thermal BTD features, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, trusted focal-Tversky primary loss, the provider-derived `centerline` auxiliary target at trusted `weighted_bce` weight 0.02, and the provider-derived `boundary` auxiliary target at trusted `weighted_bce` weight 0.01. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-development evidence rather than full-data promotion evidence.

## ABI-073 implementation and resource observation

ABI-073 started from ABI-068's frequency-gated line U-Net backbone and added one low-capacity boundary auxiliary head from the same refined feature tensor as the primary mask and centerline heads. The hypothesis was that a very low-weight trusted Boundary Target could sharpen mask support and reduce clutter while retaining ABI-068's recall-forward focal-Tversky and centerline-supervised operating point.

The Run stayed inside the Candidate Experiment Contract: no longitude/latitude inputs, no reconstructed coordinate inputs, no candidate-owned data loading, no custom loss or target derivation, no candidate-owned augmentation, no metrics, no thresholding, no Artifact Filters, no postprocessing, no network access, and no pretrained weights.

Model summary reported 12,087,606 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on an A100 with 2,703.8 seconds wall time, 9,542,041,600 bytes peak CUDA reserved, and no terminal execution failure.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260828_031118_326c4a` | ABI-070 | ABI-068 plus bounded centerline-guided residual head | 12 | 0.3807 | 0.3644 | 0.4210 | 0.4158 | 0.3512 | 0.4064 | 0.00306 |
| `run_20260828_055812_4ba74e` | ABI-073 | ABI-068 plus boundary aux weight 0.01 | 10 | 0.3778 | 0.3631 | 0.4131 | 0.3983 | 0.3594 | 0.3620 | 0.00327 |

ABI-073 did not satisfy its main continuation criteria. Relative to ABI-068, aggregate filtered Dice fell by about -0.0185, MIT filtered Dice by about -0.0255, Google filtered Dice by about -0.0030, filtered recall by about -0.0342, and filtered connectivity by about -0.0280. Filtered precision was essentially tied (-0.0009) and the filtered predicted-positive fraction decreased from 0.00357 to 0.00327, so the boundary auxiliary did sharpen or reduce positive area slightly, but it did so by giving up recall and primary Dice rather than by improving the overall trade-off.

Relative to ABI-066, ABI-073 stayed close on aggregate filtered Dice (-0.0047) and improved recall (+0.0227), but it remained weaker on precision (-0.0444), Google filtered Dice (-0.0161), and connectivity (-0.1111). Relative to ABI-070, ABI-073 was nearly tied on filtered Dice (-0.0029) and recovered a little recall (+0.0082), but it still trailed on precision, connectivity, and Google filtered Dice.

## ABI-073 trajectory

ABI-073 trained finitely and avoided all-negative/all-positive prediction collapse. The best checkpoint was epoch 10 rather than the final epoch. Filtered Dice by epoch was 0.2176, 0.2450, 0.2977, 0.3195, 0.3292, 0.3134, 0.2310, 0.3032, 0.3435, 0.3778, 0.3521, and 0.3550 at epoch 12.

The trajectory shows useful recovery after a noisy mid-run degradation, but the late peak was not sustained. At best epoch, both Dataset Sources stayed above 0.35 filtered Dice: MIT 0.3631 and Google 0.4131. However, the operating profile remained below the local ABI-068 reference: filtered recall was only 0.3594 and connectivity was 0.3620, while the modest lower predicted-positive fraction did not produce a precision gain.

The fixed first-four retained prediction artifacts should not be treated as representative qualitative evidence. The useful evidence for this capped Run is the aggregate/source-stratified validation metrics, the non-degenerate predicted-positive fractions, and the epoch trajectory above.

## Interpretation

Classify ABI-073 as mixed-to-negative capped family-development evidence for this exact low-weight boundary-auxiliary branch, not as an execution failure and not as evidence against the whole frequency-gated architecture family. The candidate completed reliably within contract and resource limits, remained source-balanced enough to avoid catastrophic MIT or Google collapse, and showed that boundary supervision can slightly reduce the predicted-positive burden. But it failed to improve filtered Dice, precision, recall, or connectivity over ABI-068, and it did not recover ABI-066's precision/connectivity-forward behavior.

Together with ABI-069, ABI-070, ABI-071, and ABI-073, the local frequency-gated family evidence suggests that additional post-decoder heads, suppressors, gates, and auxiliary-head stacking are not improving the ABI-068 operating point under the active capped policy. ABI-068 remains the current strongest capped aggregate-Dice frequency-gated reference, and ABI-066 remains the precision/connectivity-forward reference. Canonical MCAST 2.1 remains the full Working Validation Split promotion context.

ABI-073 does not justify promotion interpretation or a whole-validation Evaluation Request. It also should not be repeated unchanged: its lower predicted-positive fraction came with lower Dice, lower recall, and lower connectivity.

## Decision

Do not promote ABI-073 and do not continue this exact boundary-auxiliary stacking branch unchanged. Retain it as evidence that low-weight trusted boundary supervision can modestly sharpen support but is insufficient to improve the ABI-068 focal-Tversky frequency-gated trade-off.

The next useful research step should broaden away from stacking auxiliary heads or adding suppressive/gated mask refiners to ABI-068. In-contract options include a materially different thin-line backbone, a lower-capacity continuity module that is not another output-head stack, or a different allowlisted loss/augmentation/training-policy axis while preserving provider/Harness ownership of data loading, sampling, augmentation, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle.

## Artifact references

- `run_20260828_055812_4ba74e/outputs/best_metrics.json`
- `run_20260828_055812_4ba74e/outputs/final_metrics.json`
- `run_20260828_055812_4ba74e/outputs/metrics.jsonl`
- `run_20260828_055812_4ba74e/outputs/resource_profile.json`
- `run_20260828_055812_4ba74e/outputs/model_summary.json`
- `run_20260828_055812_4ba74e/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260828_031118_326c4a/outputs/best_metrics.json`
- `run_20260828_050329_c01ecf/outputs/best_metrics.json`
