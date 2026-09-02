# Full-spectral BTD patch-anomaly line U-Net follow-up

research-figures: []

## Scope

This note records ABI-113 after Run `run_20260830_220436_b4eadb` completed.

Source Runs:

- ABI-113 patch-anomaly front-end continuation: `run_20260830_220436_b4eadb`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-105 conservative-skip focal-Tversky continuation: `run_20260830_091941_139456`
- ABI-109 deterministic-front-end focal-Tversky continuation: `run_20260830_125040_95bfb5`
- ABI-111 MCAST-guided dual-branch scout: `run_20260830_201502_afa0c8`
- ABI-112 line-propagation U-Net continuation: `run_20260830_210213_520f36`

ABI-113 was a family-development continuation within the full-spectral BTD frequency-gated line U-Net branch. It kept provider-approved `abi_16ch` input, deterministic thermal BTD features derived only from GOES ABI channels 1-16, a learned 1x1 mixer, trusted focal-Tversky primary loss, provider-derived Centerline Target auxiliary supervision with trusted `weighted_bce` weight 0.02, provider-owned `combined_source_balanced` traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.

The controlled architecture change was adding patch-relative z-scored raw-channel and BTD anomaly planes beside fixed normalized raw/BTD features before the learned 1x1 mixer. The hypothesis was that local contrast features could improve source/background-adaptive thin-contrail calibration without moving thresholding, losses, Artifact Filters, postprocessing, data loading, sampling, augmentation, metrics, resource placement, or lifecycle behavior into Candidate code. This is capped representative evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-113 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI Channel Input and approved-channel combinations. It did not introduce candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: focal_tversky`, and one `centerline_logits` auxiliary output using trusted `weighted_bce` weight 0.02. `outputs/model_summary.json` reported 12,091,273 parameters against the 25,000,000-parameter smoke ceiling, confirmed GOES ABI channels 1-16 only with forbidden longitude/latitude source channels excluded, and confirmed outputs `mask_logits` plus `centerline_logits`.

The Run completed at batch size 4 on the A100 with 2,801.3 seconds total wall time, 1,379.3 seconds training wall time, 1,419.9 seconds validation wall time, 9,682,550,784 bytes peak CUDA reserved, and no terminal execution failure. The best-validation checkpoint was epoch 12.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260830_091941_139456` | ABI-105 | ABI-068 branch, conservative non-amplifying skip gates | 12 | 0.3831 | 0.3820 | 0.3857 | 0.3344 | 0.4484 | 0.2520 | 0.00486 |
| `run_20260830_125040_95bfb5` | ABI-109 | deterministic normalized raw+BTD front end | 12 | 0.3718 | 0.3579 | 0.4045 | 0.3507 | 0.3955 | 0.2976 | 0.00409 |
| `run_20260830_201502_afa0c8` | ABI-111 | MCAST-guided dual-branch thermal support stream | 10 | 0.3770 | 0.3636 | 0.4085 | 0.3887 | 0.3660 | 0.3560 | 0.00341 |
| `run_20260830_210213_520f36` | ABI-112 | non-wrapping directional line-propagation refiner | 12 | 0.3716 | 0.3608 | 0.3974 | 0.3774 | 0.3659 | 0.3312 | 0.00351 |
| `run_20260830_220436_b4eadb` | ABI-113 | patch-relative raw/BTD anomaly front end | 12 | 0.3670 | 0.3689 | 0.3627 | 0.3265 | 0.4191 | 0.1594 | 0.00465 |

ABI-113 produced a finite, non-collapsed operating point but missed the preregistered useful-continuation criteria. Relative to ABI-068, aggregate filtered Dice decreased from 0.3964 to 0.3670 (-0.0293), MIT filtered Dice decreased from 0.3886 to 0.3689 (-0.0197), Google filtered Dice decreased from 0.4161 to 0.3627 (-0.0534), precision decreased from 0.3992 to 0.3265 (-0.0727), recall increased from 0.3936 to 0.4191 (+0.0255), connectivity decreased sharply from 0.3900 to 0.1594 (-0.2306), and filtered predicted-positive fraction increased from 0.00357 to 0.00465.

Relative to ABI-066, ABI-113 was lower on aggregate filtered Dice (-0.0155), Google filtered Dice (-0.0665), precision (-0.1163), and connectivity (-0.3136), while recall was higher (+0.0824) and MIT filtered Dice was slightly higher (+0.0051). It therefore did not retain the precision/connectivity advantage that made ABI-066 useful as a secondary reference.

Relative to recent local continuations, ABI-113 improved MIT filtered Dice over ABI-109, ABI-111, and ABI-112, but that came with materially worse Google filtered Dice and the lowest connectivity of the compared set. Its recall-forward behavior was not cleaner than ABI-105 or ABI-110 because precision and connectivity fell more sharply while positive area remained elevated.

## ABI-113 trajectory

ABI-113 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.2003, 0.2170, 0.2736, 0.3227, 0.3076, 0.3080, 0.3452, 0.3384, 0.3323, 0.3560, 0.3349, and 0.3670. The selected checkpoint was the final epoch, so the Run retained late improvement after a noisy middle and late trajectory.

At the selected checkpoint, filtered Dice was 0.3670, raw Dice 0.3783, filtered IoU 0.2248, filtered precision 0.3265, filtered recall 0.4191, filtered connectivity 0.1594, and filtered predicted-positive fraction 0.00465. Source-stratified filtered Dice was 0.3689 MIT and 0.3627 Google. Google remained recall-forward (`0.2883` precision, `0.4886` recall), while MIT was less recall-forward (`0.3458` precision, `0.3954` recall).

Raw-to-filtered differences were modest: raw Dice 0.3783 versus filtered Dice 0.3670, and raw predicted-positive fraction 0.00497 versus filtered 0.00465. This does not look primarily like an Artifact Filter dependence issue. The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` all had near-zero per-sample Dice, but these are bounded `first_n` artifacts and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-113 as finite, resource-feasible, non-collapsed, late-improving but negative evidence for this exact patch-anomaly front-end branch. The added patch-relative anomaly planes shifted the model toward higher recall and larger positive area, but did not improve the intended source-robust calibration tradeoff. The most concerning result is the connectivity collapse to 0.1594, far below ABI-068, ABI-066, ABI-111, and ABI-112, which suggests the anomaly features encouraged fragmented or blob-like positives rather than continuous thin-line masks under the current head/loss policy.

ABI-113 also satisfies the preregistered hard-stop condition for this exact branch: aggregate filtered Dice is below 0.37 and no compensating secondary metric improved enough to justify continuation. The final checkpoint improved, so this is not a training-collapse failure; it is negative architectural evidence for this patch-relative anomaly formulation.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-113 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-113. Do not request whole-validation diagnostics for this checkpoint ahead of stronger ABI-068/ABI-066 references. Stop this exact patch-relative raw/BTD anomaly front-end branch unless a clear implementation bug is discovered.

Retain ABI-068 as the capped aggregate-Dice reference and ABI-066 as the precision/connectivity reference. The next useful hypothesis should broaden away from additional local front-end widening or high-resolution refiner variants in this branch, for example toward a materially different calibration mechanism, a trusted data-policy/loss/auxiliary-target comparison, or another thin-line segmentation family that can improve connectivity without a large recall-only positive-area shift.

## Artifact references

- `run_20260830_220436_b4eadb/outputs/best_metrics.json`
- `run_20260830_220436_b4eadb/outputs/final_metrics.json`
- `run_20260830_220436_b4eadb/outputs/metrics.jsonl`
- `run_20260830_220436_b4eadb/outputs/resource_profile.json`
- `run_20260830_220436_b4eadb/outputs/model_summary.json`
- `run_20260830_220436_b4eadb/outputs/prediction_samples/samples.json`
- `run_20260830_220436_b4eadb/resolved_manifest.yaml`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260830_091941_139456/outputs/best_metrics.json`
- `run_20260830_125040_95bfb5/outputs/best_metrics.json`
- `run_20260830_201502_afa0c8/outputs/best_metrics.json`
- `run_20260830_210213_520f36/outputs/best_metrics.json`
