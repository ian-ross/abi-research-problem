# Full-spectral BTD frequency-gated line U-Net centerline-guided head follow-up

research-figures: []

## Scope

This note records ABI-070 after Run `run_20260828_031118_326c4a` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice and whole-validation reference: `run_20260828_010836_4ccc77`
- ABI-069 confidence-suppressor negative control for over-suppressive head changes: `run_20260828_021352_6f4329`
- ABI-070 centerline-guided residual head continuation: `run_20260828_031118_326c4a`

ABI-070 used provider-approved `abi_16ch` inputs, ABI-channel-derived thermal BTD features, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, trusted focal-Tversky primary loss, and the provider-derived `centerline` auxiliary target at trusted `weighted_bce` weight 0.02. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-development evidence rather than full-data promotion evidence.

## ABI-070 implementation and resource observation

ABI-070 started from ABI-068's full-spectral BTD frequency-gated line U-Net and replaced the plain mask head with a bounded centerline-guided residual head. The direct mask-logit path remained primary; a zero-initialized residual was bounded by `0.20 * tanh(...)` and gated by the jointly trained centerline auxiliary output. The intent was to recover some ABI-066-style precision or line continuity without repeating ABI-069's subtractive confidence-suppressor behavior.

The Run stayed inside the Candidate Experiment Contract: no longitude/latitude inputs, no reconstructed coordinate inputs, no candidate-owned data loading, no custom loss or target derivation, no candidate-owned augmentation, no metrics, no thresholding, no Artifact Filters, no postprocessing, no network access, and no pretrained weights.

Model summary reported 12,192,502 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on an A100 with 2,939.7 seconds wall time, 9,630,121,984 bytes peak CUDA reserved, and no terminal execution failure.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_010836_4ccc77` | ABI-068 | same family, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260828_021352_6f4329` | ABI-069 | ABI-068 plus differentiable confidence-suppressor head | 10 | 0.3711 | 0.3602 | 0.3955 | 0.3789 | 0.3635 | 0.1451 | 0.00348 |
| `run_20260828_031118_326c4a` | ABI-070 | ABI-068 plus bounded centerline-guided residual head | 12 | 0.3807 | 0.3644 | 0.4210 | 0.4158 | 0.3512 | 0.4064 | 0.00306 |

ABI-070 did not match ABI-068's capped aggregate filtered Dice: it trailed by about -0.0156. The head change did, however, move the operating profile in the intended precision/connectivity direction relative to ABI-068: filtered precision improved by about +0.0166, filtered connectivity by about +0.0164, and filtered predicted-positive fraction fell from 0.00357 to 0.00306. The cost was a material filtered-recall drop of about -0.0424 and a MIT filtered-Dice drop of about -0.0242. Google filtered Dice slightly exceeded ABI-068 by about +0.0049.

Relative to ABI-066, ABI-070 nearly tied aggregate filtered Dice (-0.0018) and improved recall (+0.0144), while remaining worse on precision (-0.0270), connectivity (-0.0667), and Google filtered Dice (-0.0082). It did not recover ABI-066's precision/connectivity-forward profile, but it was clearly less damaging than ABI-069's suppressor head: ABI-070 exceeded ABI-069 by about +0.0097 filtered Dice, +0.0369 precision, +0.0429 recall, and +0.2613 connectivity.

## ABI-070 trajectory

ABI-070 trained finitely and avoided all-negative/all-positive prediction collapse. Filtered Dice improved from 0.1852 at epoch 1 to 0.3239 at epoch 3, then oscillated. Later epochs were 0.3615 at epoch 8, 0.3516 at epoch 9, 0.3639 at epoch 10, 0.3290 at epoch 11, and the selected best 0.3807 at epoch 12.

The late best checkpoint is continuation-friendly evidence for the exact training budget, but the branch did not satisfy the proposal's strongest success criteria. It was not within about 0.01 of ABI-068 while improving precision/connectivity, and recall fell below the proposed 0.37 recall target. It did satisfy the non-collapse/source-balance portion of the criteria: MIT filtered Dice was 0.3644, Google filtered Dice was 0.4210, precision was 0.4158, and filtered predicted-positive fraction was bounded at 0.00306.

The first-four retained prediction artifacts should not be treated as representative qualitative evidence. As in prior notes, aggregate and source-stratified validation metrics are the useful evidence for this capped Run.

## Interpretation

Classify ABI-070 as mixed capped family-development evidence. The bounded centerline-guided residual head avoided the ABI-069-style connectivity collapse and shifted the model toward a more conservative, higher-precision operating profile than ABI-068. That validates part of the architectural intuition: centerline-guided additive residuals are less harmful than subtractive confidence suppression.

The tradeoff was still not superior to ABI-068. The aggregate Dice and recall loss are too large for ABI-070 to replace ABI-068 as the frequency-gated aggregate-Dice reference, and it does not restore ABI-066's stronger precision/connectivity. ABI-068 remains the current strongest local whole-validation-tested Candidate by aggregate filtered Dice; ABI-066 remains the precision/connectivity-forward reference.

Because ABI-070 did not beat ABI-068 capped and did not clearly improve the full precision/recall/connectivity tradeoff, a whole-validation failure-bucket evaluation is not the next best use of diagnostic budget. The better next hypothesis should preserve ABI-068's recall-forward focal-Tversky behavior while adding a softer, less recall-costly precision mechanism, or broaden to another in-contract architecture family/control path.

## Decision

Do not promote ABI-070 and do not repeat this exact centerline-guided residual-head branch unchanged. Retain it as evidence that additive centerline guidance is safer than ABI-069's suppressor head, but insufficient as implemented.

A future bounded continuation, if pursued, should reduce the residual's ability to pull probability mass away from true contrail pixels or separate line-continuity assistance from clutter suppression more explicitly, while keeping losses, targets, sampling, augmentation, metrics, thresholding, Artifact Filters, and data handling provider/Harness-owned.

## Artifact references

- `run_20260828_031118_326c4a/outputs/best_metrics.json`
- `run_20260828_031118_326c4a/outputs/final_metrics.json`
- `run_20260828_031118_326c4a/outputs/metrics.jsonl`
- `run_20260828_031118_326c4a/outputs/resource_profile.json`
- `run_20260828_031118_326c4a/outputs/model_summary.json`
- `run_20260828_031118_326c4a/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260828_021352_6f4329/outputs/best_metrics.json`
