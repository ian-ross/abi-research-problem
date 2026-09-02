# Full-spectral BTD frequency-gated line U-Net centerline-weight follow-up

research-figures: []

## Scope

This note records ABI-067 after Run `run_20260828_001300_16c885` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net local whole-validation-tested reference: `run_20260827_230540_bf4ce3`
- ABI-067 frequency-gated line U-Net centerline-auxiliary weight continuation: `run_20260828_001300_16c885`

Both Runs used provider-approved `abi_16ch` inputs, approved thermal BTD features derived only from ABI channels, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped feasibility results, not full-data promotion evidence.

## ABI-067 implementation and resource observation

ABI-067 intentionally kept the ABI-066 frequency-gated architecture unchanged. The controlled change was manifest-only: the provider-derived `centerline` auxiliary target remained enabled, but its trusted `weighted_bce` loss weight was lowered from 0.02 to 0.01. The primary loss remained trusted `bce_dice_cldice`.

The Run stayed inside the Candidate Experiment Contract: no longitude/latitude inputs, no reconstructed coordinate inputs, no candidate-owned data loading, no custom loss or target derivation, no augmentation implementation, no metrics, no thresholding, no Artifact Filters, no postprocessing, no network access, and no pretrained weights.

Model summary reported 12,087,561 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 2,908.2 seconds wall time, 9,734,979,584 bytes peak CUDA reserved, and no terminal execution failure.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_001300_16c885` | ABI-067 | same architecture, centerline aux weight 0.01 | 11 | 0.3772 | 0.3723 | 0.3896 | 0.3608 | 0.3953 | 0.3463 | 0.00397 |

Lowering the centerline auxiliary weight produced the expected recall movement but did not improve the primary capped metric. Relative to ABI-066's best checkpoint, ABI-067 gained about +0.0585 filtered recall and +0.0085 MIT filtered Dice, but lost about -0.0053 aggregate filtered Dice, -0.0396 Google filtered Dice, -0.0820 filtered precision, and -0.1268 filtered connectivity. The filtered predicted-positive fraction also increased from 0.00276 to 0.00397.

The result is non-degenerate and source-balanced enough to be scientifically useful, but it weakens the precision/connectivity-forward behavior that made ABI-066 distinctive.

## ABI-067 trajectory

ABI-067 trained finitely throughout the 12-epoch budget. Filtered Dice rose quickly from 0.2357 at epoch 1 to 0.3173 at epoch 2, then improved more gradually: 0.3413 at epoch 4, 0.3543 at epoch 6, 0.3605 at epoch 8, and 0.3772 at epochs 10-11. The final epoch remained close at 0.3728.

The late trajectory shows no collapse. Instead, it shows an operating-profile tradeoff. The selected epoch 11 checkpoint had the strongest recall at 0.3953 but carried lower precision and connectivity. The final epoch shifted back toward precision, with filtered precision 0.4074 and connectivity 0.3995, but recall fell to 0.3437 and aggregate filtered Dice remained below ABI-066.

The fixed first-four prediction artifacts are not representative qualitative evidence: one retained sample was a perfect empty-mask case and three had near-zero sample Dice. Aggregate and source-stratified validation metrics are the useful evidence for this note.

## Interpretation

ABI-067 is mixed-to-negative family-development evidence for the simple centerline-auxiliary weight reduction hypothesis. The lower auxiliary weight did relax the branch toward recall, which supports the diagnosis that ABI-066 has an operating-point/coverage gap. However, the gain was bought by enough extra predicted-positive burden, precision loss, connectivity loss, and Google-source Dice loss that this exact manifest-only change should not replace ABI-066 as the local reference.

The proposal's strong continuation criteria are not met. ABI-067 did not match or exceed ABI-066's capped filtered Dice, did not preserve filtered precision above 0.40 at the best selected checkpoint, and did not keep connectivity above 0.40 at that checkpoint. Its finite late trajectory and improved MIT/recall signal remain useful for designing a more targeted recall-recovery hypothesis, but they are not enough to justify promotion or to treat the lowered auxiliary weight as a clear improvement.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context, and ABI-066 remains the strongest local whole-validation-tested Candidate reference for this branch.

## Decision

Classify ABI-067 as a completed, finite, non-collapsed but non-improving frequency-gated family-development continuation. Retain ABI-066 as the local reference. Avoid further simple centerline-auxiliary weight sweeps unless a later diagnostic identifies a specific target for them.

The next useful hypothesis should recover recall without surrendering ABI-066's false-positive suppression and connectivity. A bounded in-contract option is to keep the ABI-066 frequency-gated architecture and test trusted `focal_tversky`, or an architecture-level recall path that affects mask evidence rather than simply weakening centerline regularization. Whole-validation diagnostics are more urgent for candidates that credibly improve or tie ABI-066; ABI-067's capped tradeoff does not require immediate full-validation evaluation.

## Artifact references

- `run_20260828_001300_16c885/outputs/best_metrics.json`
- `run_20260828_001300_16c885/outputs/final_metrics.json`
- `run_20260828_001300_16c885/outputs/metrics.jsonl`
- `run_20260828_001300_16c885/outputs/resource_profile.json`
- `run_20260828_001300_16c885/outputs/model_summary.json`
- `run_20260828_001300_16c885/outputs/prediction_samples/samples.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/threshold_sweep.json`
