# Full-spectral BTD coarse-to-fine U-Net scout

research-figures: []

## Scope

This note records ABI-064, the full-spectral BTD coarse-to-fine U-Net family scout, after Run `run_20260827_212811_0e34e2` completed. ABI-064 was proposed as a new coarse-to-fine architecture mechanism: an internal 64-pixel soft mask prior gates a full-resolution decoder/refiner while still emitting only provider-approved `mask_logits` and provider-derived `centerline_logits`.

Source Runs:

- ABI-064 coarse-to-fine U-Net scout: `run_20260827_212811_0e34e2`
- Primary local comparison ABI-058 oriented-context high-resolution BTD line U-Net: `run_20260827_171331_c1769a`
- Secondary comparison ABI-061 focal-Tversky oriented-context high-resolution BTD line U-Net: `run_20260827_194725_c1d6c6`
- Recent negative context ABI-063 compact axial strip-context U-Net repair: `run_20260827_203436_96acf7`

All trained comparison Runs used provider-approved `abi_16ch` inputs, approved thermal BTD features derived only from ABI channels, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. These are capped feasibility results, not full-data promotion evidence.

## ABI-064 implementation and resource observation

ABI-064 stayed inside the Candidate Experiment Contract: no longitude/latitude inputs, no reconstructed coordinate inputs, no candidate-owned data loading, no loss or target derivation, no augmentation implementation, no metrics, no thresholding, no Artifact Filters, no postprocessing, no network access, and no pretrained weights.

The model summary reported provider-approved `abi_16ch` input, `mask_logits` plus `centerline_logits`, and 14,548,983 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 2,206.1 seconds wall time, 7.55 GiB peak CUDA allocated, 9.55 GiB peak CUDA reserved, and no terminal execution failure.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_171331_c1769a` | ABI-058 | oriented full-resolution context, clDice + centerline aux | 10 | 0.3248 | 0.3139 | 0.3497 | 0.3144 | 0.3360 | 0.2335 | 0.00387 | 14.21M |
| `run_20260827_194725_c1d6c6` | ABI-061 | focal-Tversky on ABI-058 architecture + centerline aux | 12 | 0.3221 | 0.2954 | 0.3896 | 0.3515 | 0.2973 | 0.2834 | 0.00306 | 14.21M |
| `run_20260827_203436_96acf7` | ABI-063 | compact axial strip context, clDice + centerline aux | 12 | 0.2782 | 0.2763 | 0.2820 | 0.2292 | 0.3538 | 0.1446 | 0.00559 | 20.17M |
| `run_20260827_212811_0e34e2` | ABI-064 | coarse soft-prior gating, clDice + centerline aux | 11 | 0.3255 | 0.3213 | 0.3348 | 0.3016 | 0.3535 | 0.1972 | 0.00425 | 14.55M |

ABI-064 is the best completed capped Run by `val/filtered_dice` in the current read-only Run history, but only by a narrow margin over ABI-058 (+0.0007). Its best-checkpoint behavior is recall-heavier than ABI-058 and ABI-061: filtered recall improved relative to ABI-058, but filtered precision, connectivity, and predicted-positive fraction did not improve at the selected checkpoint.

## ABI-064 trajectory

ABI-064 trained finitely and non-degenerately. Filtered Dice rose from 0.0878 at epoch 1 to 0.1743 at epoch 2 and 0.2239 at epoch 3. Epoch 4 dipped to 0.1826 while recall rose and precision fell, then epoch 5 recovered to 0.2824. Epochs 6-10 ranged from 0.2886 to 0.3116. The selected checkpoint was epoch 11 at 0.3255, followed by a final epoch-12 drop to 0.3163.

The source behavior changed across the last two epochs. At best epoch 11, MIT filtered Dice was 0.3213 and Google filtered Dice was 0.3348, giving the most balanced source split among the recent high-scoring candidates. At final epoch 12, aggregate filtered Dice dropped to 0.3163, but Google improved to 0.3716 while MIT fell to 0.2943. Final precision and connectivity improved over the best checkpoint, and final predicted-positive fraction dropped to 0.00319, but the trusted checkpoint selector is still epoch 11 by `val/filtered_dice`.

The fixed first-four prediction samples all have near-zero sample Dice values, so they should not be treated as representative qualitative evidence.

## Interpretation

The coarse-to-fine scout produced a small capped aggregate improvement and avoided the axial strip-context branch's low-precision/low-connectivity failure mode. It met the broad continuation criterion of matching or slightly exceeding ABI-058 capped filtered Dice while keeping both MIT and Google above 0.25. It also stayed within the expected resource envelope.

The original false-positive-control hypothesis is only partially supported. The best checkpoint did not reduce predicted-positive burden or improve precision relative to ABI-058. The final checkpoint had a lower predicted-positive fraction, better precision, and better connectivity, but at lower aggregate Dice and lower MIT recall/Dice. This suggests the coarse prior changes the precision/recall trajectory in a useful way, but the current clDice version does not cleanly dominate the oriented-context high-resolution line U-Net reference.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context at filtered Dice 0.3873. ABI-064 is not promotion-ready and must not be interpreted as full-data evidence.

## Decision

Classify ABI-064 as positive/mixed capped family-scout evidence for the coarse-to-fine U-Net mechanism. Do not promote it from capped evidence. Do not abandon the coarse-to-fine branch: the Run is finite, non-degenerate, resource-safe, source-balanced at the best checkpoint, and now marginally leads the capped `val/filtered_dice` ranking.

A useful next step is either a bounded whole-validation failure-analysis Evaluation Request for ABI-064, if the campaign needs to test whether the capped source balance and false-positive behavior survive the full Working Validation Split, or one family-development continuation that changes only the trusted loss to `focal_tversky` to test whether the final-epoch precision/connectivity tendency can be reached without the epoch-11 recall-heavy burden. Broader frontier work remains appropriate if future diagnostics show the coarse prior is merely redistributing errors rather than reducing negative-patch false positives.

## Artifact references

- `run_20260827_212811_0e34e2/outputs/best_metrics.json`
- `run_20260827_212811_0e34e2/outputs/final_metrics.json`
- `run_20260827_212811_0e34e2/outputs/metrics.jsonl`
- `run_20260827_212811_0e34e2/outputs/resource_profile.json`
- `run_20260827_212811_0e34e2/outputs/model_summary.json`
- `run_20260827_212811_0e34e2/outputs/prediction_samples/samples.json`
- `run_20260827_171331_c1769a/outputs/best_metrics.json`
- `run_20260827_194725_c1d6c6/outputs/best_metrics.json`
- `run_20260827_203436_96acf7/outputs/best_metrics.json`
