# Full-spectral BTD line-propagation U-Net follow-up

research-figures: []

## Scope

This note records ABI-112 after Run `run_20260830_210213_520f36` completed.

Source Runs:

- ABI-112 line-propagation U-Net continuation: `run_20260830_210213_520f36`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-105 conservative-skip focal-Tversky continuation: `run_20260830_091941_139456`
- ABI-111 MCAST-guided dual-branch scout: `run_20260830_201502_afa0c8`

ABI-112 was a family-development continuation within the full-spectral BTD thin-line U-Net branch. It kept provider-approved `abi_16ch` input, deterministic thermal BTD features derived only from GOES ABI channels 1-16, a learned 1x1 mixer, trusted focal-Tversky primary loss, provider-derived Centerline Target auxiliary supervision with trusted `weighted_bce` weight 0.02, provider-owned `combined_source_balanced` traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.

The controlled architecture change was replacing the ABI-068-style oriented high-resolution refiner with non-wrapping directional feature propagation along horizontal, vertical, and diagonal paths. The hypothesis was that explicit same-line feature propagation could recover thin-contrail continuity or precision/recall balance without moving thresholding, losses, Artifact Filters, postprocessing, data loading, sampling, augmentation, metrics, resource placement, or lifecycle behavior into Candidate code. This is capped representative evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-112 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI Channel Input and approved-channel combinations. It did not introduce candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: focal_tversky`, and one `centerline_logits` auxiliary output using trusted `weighted_bce` weight 0.02. `outputs/model_summary.json` reported 12,183,614 parameters against the 25,000,000-parameter smoke ceiling, confirmed GOES ABI channels 1-16 only with forbidden longitude/latitude source channels excluded, and confirmed outputs `mask_logits` plus `centerline_logits`.

The Run completed at batch size 4 on the A100 with 3,134.6 seconds total wall time, 1,674.9 seconds training wall time, 1,457.5 seconds validation wall time, 12,058,624,000 bytes peak CUDA reserved, and no terminal execution failure. The best-validation checkpoint was epoch 12.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260830_091941_139456` | ABI-105 | ABI-068 branch, conservative non-amplifying skip gates | 12 | 0.3831 | 0.3820 | 0.3857 | 0.3344 | 0.4484 | 0.2520 | 0.00486 |
| `run_20260830_201502_afa0c8` | ABI-111 | MCAST-guided dual-branch thermal support stream | 10 | 0.3770 | 0.3636 | 0.4085 | 0.3887 | 0.3660 | 0.3560 | 0.00341 |
| `run_20260830_210213_520f36` | ABI-112 | non-wrapping directional line-propagation refiner | 12 | 0.3716 | 0.3608 | 0.3974 | 0.3774 | 0.3659 | 0.3312 | 0.00351 |

ABI-112 produced a finite, non-collapsed operating point but did not improve the frequency-gated family references. Relative to ABI-068, aggregate filtered Dice decreased from 0.3964 to 0.3716 (-0.0248), MIT filtered Dice decreased from 0.3886 to 0.3608 (-0.0278), Google filtered Dice decreased from 0.4161 to 0.3974 (-0.0187), precision decreased from 0.3992 to 0.3774 (-0.0218), recall decreased from 0.3936 to 0.3659 (-0.0277), and connectivity decreased from 0.3900 to 0.3312 (-0.0588). The predicted-positive fraction was similar to ABI-068, 0.00351 versus 0.00357, so the loss was not simply a conservative-area shift.

Relative to ABI-066, ABI-112 remained lower in aggregate filtered Dice (-0.0110), Google filtered Dice (-0.0317), precision (-0.0654), and connectivity (-0.1419), while recall was higher (+0.0292) and MIT filtered Dice was close (-0.0030). It therefore did not recover ABI-066's precision/connectivity advantage. Relative to ABI-105, ABI-112 gave better precision (+0.0430) and connectivity (+0.0791), but lower Dice (-0.0115), lower recall (-0.0824), and lower MIT/Google source Dice. Relative to ABI-111, ABI-112 was lower on Dice (-0.0055), precision (-0.0113), connectivity (-0.0248), and Google filtered Dice (-0.0111), while being essentially tied on recall and slightly lower in positive area.

## ABI-112 trajectory

ABI-112 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.1330, 0.1814, 0.3033, 0.2314, 0.3331, 0.2793, 0.3521, 0.3203, 0.3456, 0.3587, 0.3050, and 0.3716. The selected checkpoint was the final epoch, so the Run did finish with late improvement after a noisy middle/late trajectory.

At the selected checkpoint, filtered Dice was 0.3716, raw Dice 0.3845, filtered IoU 0.2282, filtered precision 0.3774, filtered recall 0.3659, filtered connectivity 0.3312, and filtered predicted-positive fraction 0.00351. Source-stratified filtered Dice was 0.3608 MIT and 0.3974 Google. Google remained the recall-forward source (`0.3557` precision, `0.4503` recall), while MIT was more precision-forward (`0.3882` precision, `0.3371` recall).

Raw-to-filtered differences were modest: raw Dice 0.3845 versus filtered Dice 0.3716, and raw predicted-positive fraction 0.00374 versus filtered 0.00351. This does not look primarily like an Artifact Filter dependence issue. The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` all had near-zero per-sample Dice, but these are bounded `first_n` artifacts and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-112 as finite, resource-feasible, non-collapsed, late-improving but negative-to-mixed evidence for the exact non-wrapping directional line-propagation refiner. It met one preregistered useful-continuation criterion by keeping both source filtered Dice values at about 0.36 or higher and keeping predicted-positive fraction between the ABI-066 conservative profile and ABI-105 recall-forward profile. However, it missed the more important hypothesis tests: it did not approach ABI-068 within 0.01 while improving precision or connectivity, did not exceed ABI-066 while retaining connectivity above 0.39, and did not produce a cleaner tradeoff than recent ABI-109 through ABI-111.

The directional propagation block increased resource cost relative to ABI-068 without delivering the intended continuity gain. Its connectivity was better than low-connectivity recall-forward branches such as ABI-105 and ABI-110, but still well below ABI-068 and far below ABI-066. Because the final checkpoint improved, this is not an optimization-collapse failure; it is evidence that this particular high-resolution propagation formulation is not the right mechanism for recovering both continuity and aggregate/source balance under the current training policy.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-112 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-112. Do not request whole-validation diagnostics for this checkpoint ahead of stronger ABI-068/ABI-066 references. Stop this exact line-propagation refiner unless a clear implementation bug is discovered.

Retain ABI-068 as the capped aggregate-Dice reference and ABI-066 as the precision/connectivity reference. The next useful hypothesis should broaden away from additional local high-resolution refiner variants in this branch, for example toward a materially different calibration mechanism, data-policy test, loss/auxiliary policy within the trusted allowlist, or another thin-line segmentation family that does not add substantial wall-time without improving connectivity.

## Artifact references

- `run_20260830_210213_520f36/outputs/best_metrics.json`
- `run_20260830_210213_520f36/outputs/final_metrics.json`
- `run_20260830_210213_520f36/outputs/metrics.jsonl`
- `run_20260830_210213_520f36/outputs/resource_profile.json`
- `run_20260830_210213_520f36/outputs/model_summary.json`
- `run_20260830_210213_520f36/outputs/prediction_samples/samples.json`
- `run_20260830_210213_520f36/resolved_manifest.yaml`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260830_091941_139456/outputs/best_metrics.json`
- `run_20260830_201502_afa0c8/outputs/best_metrics.json`
