# Full-spectral BTD frequency-gated line U-Net focal-Tversky follow-up

research-figures: []

## Scope

This note records ABI-068 after Run `run_20260828_010836_4ccc77` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net local whole-validation-tested reference: `run_20260827_230540_bf4ce3`
- ABI-067 frequency-gated line U-Net centerline-auxiliary weight continuation: `run_20260828_001300_16c885`
- ABI-068 frequency-gated line U-Net focal-Tversky continuation: `run_20260828_010836_4ccc77`

ABI-068 used provider-approved `abi_16ch` inputs, approved thermal BTD features derived only from ABI channels, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped feasibility and family-development results, not full-data promotion evidence.

## ABI-068 implementation and resource observation

ABI-068 intentionally kept the ABI-066 frequency-gated architecture and the provider-derived `centerline` auxiliary target at trusted `weighted_bce` weight 0.02. The controlled change was the trusted primary loss: ABI-066 used `bce_dice_cldice`, while ABI-068 used `focal_tversky`.

The Run stayed inside the Candidate Experiment Contract: no longitude/latitude inputs, no reconstructed coordinate inputs, no candidate-owned data loading, no custom loss or target derivation, no augmentation implementation, no metrics, no thresholding, no Artifact Filters, no postprocessing, no network access, and no pretrained weights.

Model summary reported 12,087,561 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 2,693.3 seconds wall time, 9,539,944,448 bytes peak CUDA reserved, and no terminal execution failure.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_001300_16c885` | ABI-067 | same architecture/loss, centerline aux weight 0.01 | 11 | 0.3772 | 0.3723 | 0.3896 | 0.3608 | 0.3953 | 0.3463 | 0.00397 |
| `run_20260828_010836_4ccc77` | ABI-068 | same architecture/aux weight, `focal_tversky` | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |

ABI-068 is the strongest capped best-validation result observed so far in the frequency-gated branch by aggregate filtered Dice. Relative to ABI-066, it gained about +0.0138 filtered Dice, +0.0569 filtered recall, and +0.0248 MIT filtered Dice, while losing about -0.0436 filtered precision, -0.0831 filtered connectivity, and -0.0131 Google filtered Dice. The filtered predicted-positive fraction rose from 0.00276 to 0.00357.

Relative to ABI-067, ABI-068 retained essentially the same recall while recovering precision, connectivity, MIT filtered Dice, Google filtered Dice, and aggregate filtered Dice. This makes the focal-Tversky loss swap a better recall-recovery path than simply lowering the centerline auxiliary weight, although it does not preserve ABI-066's precision/connectivity-forward profile.

## ABI-068 trajectory

ABI-068 trained finitely throughout the 12-epoch budget. Filtered Dice improved from 0.2046 at epoch 1 to 0.3328 at epoch 4 and 0.3653 at epoch 9. Epochs 10 and 11 regressed to 0.3478 and 0.3232, then the final epoch jumped to the selected best checkpoint at 0.3964. The late best epoch supports continued evaluation rather than elimination, but the non-monotonic middle/late trajectory means this should be treated as bounded feasibility evidence rather than a settled operating point.

The final/best checkpoint was non-collapsed: filtered predicted-positive fraction was 0.00357, filtered precision was 0.3992, filtered recall was 0.3936, and both Dataset Sources remained above the proposal's 0.33 source-Dice floor. The source profile shifted relative to ABI-066: MIT improved materially, while Google remained strong but below ABI-066.

The fixed first-four prediction artifacts are not representative qualitative evidence. One retained sample was a perfect empty-mask case and three retained samples had near-zero sample Dice. Aggregate and source-stratified validation metrics are the useful evidence for this note.

## Interpretation

ABI-068 partially validates the proposal hypothesis. Trusted focal-Tversky moved the frequency-gated architecture toward recall without the broader deterioration seen in ABI-067, and it improved the capped primary metric beyond ABI-066. It also met the proposal's source-balance/non-degeneracy criterion: MIT and Google filtered Dice were both above 0.33, and the best checkpoint was finite and late-improving.

The result is not an unqualified replacement for ABI-066. ABI-066 remains the stronger precision/connectivity reference and has whole-validation diagnostic evidence showing its capped improvement survived on the full 3,088-sample Working Validation Split. ABI-068's capped score is higher, but the precision/connectivity losses and Google-source dip need full-validation diagnostics before any promotion interpretation.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-068's capped filtered Dice is numerically above the canonical MCAST 2.1 default-threshold filtered Dice from the campaign context, but capped representative evidence must not be interpreted as a full-data win.

## Decision

Classify ABI-068 as positive capped family-development evidence for the frequency-gated line U-Net branch and as the best current capped checkpoint to diagnose next. Do not promote from this capped Run alone.

The next useful handoff is a bounded whole-validation failure-bucket Evaluation Request for `run_20260828_010836_4ccc77`, using the same diagnostic pattern applied to ABI-066. The diagnostic should test whether ABI-068's capped recall and aggregate-Dice gains survive on the full Working Validation Split, whether its precision/connectivity losses remain acceptable, and whether the MIT/Google source tradeoff persists.

## Artifact references

- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/final_metrics.json`
- `run_20260828_010836_4ccc77/outputs/metrics.jsonl`
- `run_20260828_010836_4ccc77/outputs/resource_profile.json`
- `run_20260828_010836_4ccc77/outputs/model_summary.json`
- `run_20260828_010836_4ccc77/outputs/prediction_samples/samples.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260828_001300_16c885/outputs/best_metrics.json`
