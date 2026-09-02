# Full-spectral BTD+SZA full-scale skip ASPP/detail decoder centerline-weight 0.01 follow-up

research-figures: []

## Scope

This note records ABI-171 after Run `run_20260901_220525_8c0116` completed.

Source Runs:

- ABI-171 full-scale skip ASPP/detail decoder, Centerline Target auxiliary weight 0.01: `run_20260901_220525_8c0116`
- ABI-154 full-scale skip ASPP/detail decoder, Centerline Target auxiliary weight 0.02 reference: `run_20260901_071026_32d3ec`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice reference: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-165 soft ridge-gate U-Net BCE-Dice Line+Centerline auxiliary recent recall comparison: `run_20260901_163629_b45b2d`

ABI-171 was a controlled family-development continuation of ABI-154. It kept provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD features derived only from approved ABI channels, normalized/cosine Solar Geometry Input features, compact residual encoder, ASPP bottleneck, full-scale skip fusion, high-resolution detail path, line-aware final refinement, BCE-Dice primary loss, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled manifest change was lowering the provider-derived Centerline Target auxiliary `weighted_bce` weight from 0.02 to 0.01.

## Contract and resource observation

ABI-171 stayed inside the Candidate Experiment Contract. The manifest used `abi_16ch_plus_sza`, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, primary or auxiliary losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 9,741,850 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,511.0 seconds total wall time, 1,264.8 seconds training wall time, 1,244.2 seconds validation wall time, 19.43 training samples per second, 19.75 validation samples per second, 8,020,934,144 bytes peak CUDA allocated, and 9,439,281,152 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 8 rather than the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA, centerline w0.02 | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260901_163629_b45b2d` | ABI-165 | soft ridge-gate U-Net, BCE-Dice, ABI-16+BTD+SZA, line+centerline aux | 9 | 0.3887 | 0.3767 | 0.4172 | 0.3874 | 0.3901 | 0.3215 | 0.00365 |
| `run_20260901_220525_8c0116` | ABI-171 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA, centerline w0.01 | 8 | 0.3816 | 0.3703 | 0.4086 | 0.4101 | 0.3569 | 0.3473 | 0.00315 |

ABI-171 produced a mixed but overall negative answer to the centerline-weight hypothesis. Relative to ABI-154, lowering the auxiliary weight did raise best-checkpoint filtered recall from 0.3359 to 0.3569 (+0.0210) and predicted-positive fraction from 0.00255 to 0.00315. However, that recall recovery was not enough to preserve the branch's intended advantages: aggregate filtered Dice fell from 0.3944 to 0.3816 (-0.0128), MIT filtered Dice fell from 0.3824 to 0.3703 (-0.0121), Google filtered Dice fell from 0.4260 to 0.4086 (-0.0174), filtered precision fell from 0.4777 to 0.4101 (-0.0676), and filtered connectivity fell from 0.4374 to 0.3473 (-0.0901).

Relative to ABI-130 and ABI-068, ABI-171 remained below the stronger capped references on aggregate filtered Dice and most source/shape measures. Relative to ABI-165, it was more precise and less expansive but still lower on recall and aggregate/source Dice. It therefore does not justify promotion or whole-validation diagnostics.

## ABI-171 trajectory

ABI-171 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.1888, 0.2963, 0.3046, 0.3382, 0.3345, 0.3370, 0.3628, 0.3816, 0.3543, 0.3607, 0.3569, and 0.3481. The selected best checkpoint was epoch 8. The early trajectory showed meaningful learning, but the branch did not improve after epoch 8.

At the best epoch, raw Dice was 0.3957, filtered Dice was 0.3816, filtered precision was 0.4101, filtered recall was 0.3569, filtered connectivity was 0.3473, and filtered predicted-positive fraction was 0.00315. Source-stratified filtered Dice was 0.3703 for MIT and 0.4086 for Google. MIT had filtered precision 0.4269, recall 0.3269, connectivity 0.3736, and predicted-positive fraction 0.00414. Google had filtered precision 0.3780, recall 0.4446, connectivity 0.3211, and predicted-positive fraction 0.00217.

The final epoch shifted to a much more conservative and more connected operating point but at lower overlap: final filtered Dice was 0.3481, MIT/Google filtered Dice was 0.3337/0.3850, filtered precision was 0.5163, filtered recall was 0.2625, filtered connectivity was 0.3973, and filtered predicted-positive fraction was 0.00184. This late behavior suggests that reducing the centerline auxiliary weight did not stably recover the ABI-154 recall/precision trade-off. Instead, the run moved from a lower-precision recall gain at epoch 8 to under-recall by epoch 12.

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice was 0.3957 versus filtered Dice 0.3816, raw recall 0.3813 versus filtered recall 0.3569, and raw predicted-positive fraction 0.00336 versus filtered 0.00315. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples include two empty/near-empty successes and two near-zero per-sample Dice cases under the `first_n` retention policy; they are traceability artifacts rather than representative qualitative evidence for the full validation distribution.

## Interpretation

Classify ABI-171 as a completed, finite, non-collapsed, scientifically negative family-development result for the full-scale skip ASPP/detail centerline-weight branch. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The result shows that halving the Centerline Target auxiliary weight can loosen ABI-154's fixed-threshold recall, but the recovered recall came with too much loss of precision and connectivity at the selected checkpoint. The final checkpoint's high precision/connectivity and low recall further suggests instability in the desired operating point rather than a clean auxiliary-weight optimum. This narrows the local hypothesis: ABI-154's under-recall is unlikely to be fixed by another nearby centerline-weight-only manifest change.

## Decision

Do not promote ABI-171 and do not request whole-validation diagnostics for it. Stop the exact centerline-weight-only tuning path for the ABI-154 full-scale skip ASPP/detail branch. No Capability Request or Campaign Report is required from this result.

For a later Autonomy Step, broaden away from local full-scale-skip centerline-weight adjustments. Reasonable next frontiers include a different calibration mechanism for the ABI-154/130 family, a data-policy or loss/front-end change with explicit recall/precision stabilization, or a new architecture family with high-resolution thin-line representation that does not merely retune an existing auxiliary weight.

## Artifact references

- `run_20260901_220525_8c0116/outputs/best_metrics.json`
- `run_20260901_220525_8c0116/outputs/final_metrics.json`
- `run_20260901_220525_8c0116/outputs/metrics.jsonl`
- `run_20260901_220525_8c0116/outputs/resource_profile.json`
- `run_20260901_220525_8c0116/outputs/model_summary.json`
- `run_20260901_220525_8c0116/outputs/prediction_samples/samples.json`
- `run_20260901_220525_8c0116/resolved_manifest.yaml`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260901_163629_b45b2d/outputs/best_metrics.json`
