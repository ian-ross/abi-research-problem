# Full-spectral BTD frequency-gated line U-Net soft-evidence-gate follow-up

research-figures: []

## Scope

This note records ABI-071 after Run `run_20260828_040651_cb9403` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice and whole-validation reference: `run_20260828_010836_4ccc77`
- ABI-069 confidence-suppressor negative control for suppressive head changes: `run_20260828_021352_6f4329`
- ABI-070 centerline-guided output residual comparison: `run_20260828_031118_326c4a`
- ABI-071 soft feature-space evidence-gate continuation: `run_20260828_040651_cb9403`

ABI-071 used provider-approved `abi_16ch` inputs, ABI-channel-derived thermal BTD features, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, trusted focal-Tversky primary loss, and the provider-derived `centerline` auxiliary target at trusted `weighted_bce` weight 0.02. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-development evidence rather than full-data promotion evidence.

## ABI-071 implementation and resource observation

ABI-071 started from ABI-068's frequency-gated line U-Net and added a neutral-initialized, low-amplitude feature-space evidence gate after decoder/frequency-pyramid fusion. The gate used refined decoder features, local high-frequency detail, smoothed broader context, and the jointly trained centerline auxiliary prediction to apply a small bounded residual to features before the primary mask head. This was intended to recover precision or connectivity without applying candidate-owned thresholding, postprocessing, Artifact Filters, or hard logit suppression.

The Run stayed inside the Candidate Experiment Contract: no longitude/latitude inputs, no reconstructed coordinate inputs, no candidate-owned data loading, no custom loss or target derivation, no candidate-owned augmentation, no metrics, no thresholding, no Artifact Filters, no postprocessing, no network access, and no pretrained weights.

Model summary reported 12,182,821 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on an A100 with 2,936.5 seconds wall time, 9,913,237,504 bytes peak CUDA reserved, and no terminal execution failure.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_010836_4ccc77` | ABI-068 | same family, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260828_021352_6f4329` | ABI-069 | ABI-068 plus differentiable confidence-suppressor head | 10 | 0.3711 | 0.3602 | 0.3955 | 0.3789 | 0.3635 | 0.1451 | 0.00348 |
| `run_20260828_031118_326c4a` | ABI-070 | ABI-068 plus bounded centerline-guided residual head | 12 | 0.3807 | 0.3644 | 0.4210 | 0.4158 | 0.3512 | 0.4064 | 0.00306 |
| `run_20260828_040651_cb9403` | ABI-071 | ABI-068 plus neutral soft feature-space evidence gate | 12 | 0.3712 | 0.3649 | 0.3867 | 0.3503 | 0.3947 | 0.2251 | 0.00408 |

ABI-071 did not satisfy its main success criterion. Relative to ABI-068, aggregate filtered Dice fell by about -0.0252, MIT filtered Dice by about -0.0237, Google filtered Dice by about -0.0294, filtered precision by about -0.0488, and filtered connectivity by about -0.1649. Recall was essentially preserved or slightly higher (+0.0011), but the filtered predicted-positive fraction increased from 0.00357 to 0.00408 rather than decreasing.

Relative to ABI-070, ABI-071 recovered recall (+0.0435) but lost aggregate filtered Dice (-0.0095), precision (-0.0654), connectivity (-0.1812), and Google filtered Dice (-0.0343). Relative to ABI-069, ABI-071 was roughly tied on aggregate filtered Dice (+0.0001) with better recall and connectivity, but worse precision and more predicted-positive burden. Relative to ABI-066, ABI-071 retained the higher-recall operating profile but gave up too much precision/connectivity to be a useful replacement.

## ABI-071 trajectory

ABI-071 trained finitely and avoided all-negative/all-positive prediction collapse. The best checkpoint was the final epoch, which is continuation-friendly in isolation, but the path was noisy: filtered Dice moved from 0.2314 at epoch 1 to 0.2201, 0.1838, 0.3268, 0.3306, 0.1813, 0.3155, 0.3466, 0.3462, 0.3417, 0.3606, and finally 0.3712 at epoch 12.

The final checkpoint remained source-balanced by the proposal's loose non-catastrophic criterion: MIT filtered Dice was 0.3649 and Google filtered Dice was 0.3867. However, the operating-profile objective was not met. Filtered precision was 0.3503, recall was 0.3947, connectivity was 0.2251, and filtered predicted-positive fraction was 0.00408. This is recall-preserving but clutter/connectivity-degrading behavior, not the intended soft recovery of ABI-066-style precision/connectivity.

The fixed first-four retained prediction artifacts should not be treated as representative qualitative evidence. The useful evidence for this capped Run is the aggregate/source-stratified validation metrics and the trajectory above.

## Interpretation

Classify ABI-071 as negative capped family-development evidence for this exact soft evidence-gate branch, not as an execution failure and not as evidence that the broader frequency-gated family is invalid. The candidate completed reliably and remained non-degenerate, but the proposed feature-space gate failed to move ABI-068 toward a better precision/connectivity/clutter tradeoff. It preserved recall by permitting more positives while lowering precision and line-continuity metrics.

The sequence ABI-069/ABI-070/ABI-071 suggests that suppressive or gated post-decoder head variants are not the best next local direction for the current frequency-gated architecture. ABI-069 over-suppressed connectivity, ABI-070 was safer but still paid a recall/Dice cost, and ABI-071 preserved recall only by losing precision/connectivity. ABI-068 remains the current strongest frequency-gated aggregate-Dice reference, with whole-validation failure-bucket diagnostics already available. ABI-066 remains the precision/connectivity-forward reference.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-071's capped evidence is below ABI-068 and does not justify a promotion interpretation or a whole-validation Evaluation Request.

## Decision

Do not promote ABI-071 and do not continue this exact soft evidence-gate branch unchanged. Retain it as evidence that neutral feature-space gating is not sufficient to recover ABI-066-style precision/connectivity from the ABI-068 focal-Tversky operating point.

The next useful research step should broaden away from post-decoder suppressive/gated head changes. In-contract options include a non-suppressive architecture-family scout, a different line-continuity backbone, or a training/loss/augmentation frontier that preserves provider/Harness ownership of losses, auxiliary targets, sampling, augmentation, metrics, thresholding, Artifact Filters, and data handling.

## Artifact references

- `run_20260828_040651_cb9403/outputs/best_metrics.json`
- `run_20260828_040651_cb9403/outputs/final_metrics.json`
- `run_20260828_040651_cb9403/outputs/metrics.jsonl`
- `run_20260828_040651_cb9403/outputs/resource_profile.json`
- `run_20260828_040651_cb9403/outputs/model_summary.json`
- `run_20260828_040651_cb9403/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260828_021352_6f4329/outputs/best_metrics.json`
- `run_20260828_031118_326c4a/outputs/best_metrics.json`
