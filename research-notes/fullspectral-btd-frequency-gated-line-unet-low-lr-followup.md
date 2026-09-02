# Full-spectral BTD frequency-gated line U-Net low-learning-rate follow-up

research-figures: []

## Scope

This note records ABI-085 after Run `run_20260829_181201_01c5e7` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice and whole-validation reference: `run_20260828_010836_4ccc77`
- ABI-078 BCE-Dice loss-swap conservative-operating-point reference: `run_20260828_094949_ad2af0`
- ABI-081 no-auxiliary focal-Tversky continuation: `run_20260829_143707_7c7d44`
- ABI-085 low-learning-rate focal-Tversky continuation: `run_20260829_181201_01c5e7`

ABI-085 used provider-approved `abi_16ch` input, ABI-channel-derived thermal BTD features, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0001, 12 epochs, disabled early stopping, trusted `focal_tversky` primary loss, and a provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. The controlled change from ABI-068 was the trusted training-policy axis: lower AdamW learning rate from 0.0003 to 0.0001. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-development evidence rather than full-data promotion evidence.

## ABI-085 implementation and resource observation

ABI-085 intentionally kept ABI-068's frequency-gated line U-Net architecture unchanged: normalized approved ABI channels, explicit thermal BTD planes derived only from ABI channels, learned channel mixing, frequency-split stem, residual encoder/decoder, dilated bottleneck context, frequency-pyramid fusion, oriented line refiner, primary `mask_logits`, and provider-derived `centerline_logits` auxiliary output.

The Run stayed inside the Candidate Experiment Contract. Candidate code did not use longitude/latitude inputs or reconstruct coordinate features, and did not implement data loading, sampling, augmentation, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, or pretrained weights.

Model summary reported 12,087,561 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 2,689.5 seconds wall time, 9,539,944,448 bytes peak CUDA reserved, and no terminal execution failure. The low-learning-rate variant therefore stayed in the same feasible resource envelope as ABI-068/078.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_010836_4ccc77` | ABI-068 | same architecture/aux weight, `focal_tversky`, learning rate 0.0003 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260828_094949_ad2af0` | ABI-078 | same architecture/aux weight, `bce_dice` | 11 | 0.3816 | 0.3704 | 0.4093 | 0.4072 | 0.3590 | 0.3061 | 0.00320 |
| `run_20260829_143707_7c7d44` | ABI-081 | ABI-068 architecture, no auxiliary head, `focal_tversky` | 9 | 0.3809 | 0.3624 | 0.4279 | 0.3797 | 0.3822 | 0.3893 | 0.00365 |
| `run_20260829_181201_01c5e7` | ABI-085 | ABI-068 architecture/loss/aux, learning rate 0.0001 | 12 | 0.3826 | 0.3733 | 0.4059 | 0.3693 | 0.3968 | 0.3698 | 0.00389 |

ABI-085 completed finite and non-degenerate, and both Dataset Sources cleared the proposal's approximate 0.33 filtered-Dice floor. It did not validate the stronger low-learning-rate hypothesis. Relative to ABI-068, aggregate filtered Dice fell by about -0.0138, MIT filtered Dice by about -0.0153, Google filtered Dice by about -0.0102, precision by about -0.0298, and connectivity by about -0.0202. Recall improved only marginally, by about +0.0032, while filtered predicted-positive fraction rose from 0.00357 to 0.00389.

Relative to ABI-066, ABI-085 essentially tied aggregate filtered Dice (+0.00005) and improved MIT filtered Dice and recall, but it lost Google filtered Dice, precision, connectivity, and positive-area discipline. Relative to ABI-078, ABI-085 had nearly the same aggregate filtered Dice with higher recall and connectivity but lower precision and slightly lower Google filtered Dice. Thus the lower learning rate did not recover ABI-066's precision/connectivity-forward profile and did not preserve ABI-068's aggregate-Dice advantage.

## ABI-085 trajectory

ABI-085 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.1911, 0.2307, 0.2911, 0.2747, 0.3430, 0.2659, 0.3158, 0.3445, 0.3539, 0.3376, 0.3528, and 0.3826. The selected checkpoint was the final epoch 12.

The trajectory was late-improving, but not clearly smoother than ABI-068. It still had sizeable epoch-to-epoch oscillations, including an epoch-6 drop after epoch 5 and an epoch-10 drop after epoch 9. The final checkpoint was balanced enough to be useful evidence: filtered precision 0.3693, filtered recall 0.3968, filtered connectivity 0.3698, filtered predicted-positive fraction 0.00389, MIT filtered Dice 0.3733, and Google filtered Dice 0.4059. However, the operating point is weaker than ABI-068 on the proposal's intended stabilization axes.

The fixed first-four prediction artifacts are not representative qualitative evidence under the `first_n` retention policy; aggregate and source-stratified validation metrics carry this decision.

## Interpretation

Classify ABI-085 as mixed but non-improving capped family-development evidence. The lower learning rate produced a finite, source-balanced, non-collapsed Run and remained close to the ABI-066/078 aggregate-Dice band, but it did not tie ABI-068 within the proposal's approximate 0.01 margin and did not improve precision, connectivity, Google-source behavior, or trajectory stability enough to justify this exact training-policy change.

This does not eliminate the frequency-gated line U-Net family. ABI-068 remains the current strongest local whole-validation-tested Candidate by primary filtered Dice, while ABI-066 remains the precision/connectivity-forward reference. ABI-085 specifically argues against simply lowering the ABI-068 learning rate to 0.0001 under the current capped 12-epoch constant-LR policy.

Canonical MCAST 2.1 remains the promotion context, and all comparisons here are capped representative family-development evidence unless an explicitly requested whole-validation diagnostic is run.

## Decision

Do not promote ABI-085. Do not repeat the exact low-learning-rate ABI-068 branch unchanged. Because ABI-085 did not improve ABI-068 and did not open a clearly new diagnostic question, a whole-validation Evaluation Request for ABI-085 is not the next priority.

Future work should broaden beyond this simple learning-rate reduction. A useful next hypothesis should either preserve ABI-068's full-validation aggregate strength while addressing negative-patch clutter/precision/connectivity through a materially different in-contract architecture or use another trusted training/data-policy axis without moving thresholding, Artifact Filters, data loading, sampling, augmentation, target derivation, losses, metrics, resource placement, or lifecycle behavior into Candidate code.

## Artifact references

- `run_20260829_181201_01c5e7/outputs/best_metrics.json`
- `run_20260829_181201_01c5e7/outputs/final_metrics.json`
- `run_20260829_181201_01c5e7/outputs/metrics.jsonl`
- `run_20260829_181201_01c5e7/outputs/resource_profile.json`
- `run_20260829_181201_01c5e7/outputs/model_summary.json`
- `run_20260829_181201_01c5e7/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260828_094949_ad2af0/outputs/best_metrics.json`
- `run_20260829_143707_7c7d44/outputs/best_metrics.json`
