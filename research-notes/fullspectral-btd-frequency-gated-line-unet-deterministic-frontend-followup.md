# Full-spectral BTD frequency-gated line U-Net deterministic-front-end follow-up

research-figures: []

## Scope

This note records ABI-109 after Run `run_20260830_125040_95bfb5` completed.

Source Runs:

- ABI-109 deterministic-front-end focal-Tversky continuation: `run_20260830_125040_95bfb5`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-085 low-learning-rate focal-Tversky continuation: `run_20260829_181201_01c5e7`
- ABI-107 feature-dropout focal-Tversky continuation: `run_20260830_110428_804d89`
- ABI-108 line+centerline auxiliary focal-Tversky continuation: `run_20260830_115800_4a2363`

ABI-109 was a family-development continuation of ABI-068. It retained the full-spectral ABI frequency-gated line U-Net topology, trusted focal-Tversky primary loss, provider-derived Centerline Target auxiliary supervision at trusted `weighted_bce` weight 0.02, provider-owned `combined_source_balanced` traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.

The controlled architecture change was removing ABI-068's learned 1x1 spectral mixer and using deterministic normalized GOES ABI channels 1-16 plus explicit thermal BTD planes derived only from provider-approved ABI channels. The hypothesis was that the deterministic front end might reduce recall-forward clutter or learned-mixer numerical sensitivity while preserving ABI-068-like recall. This is capped representative evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-109 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved `abi_16ch` tensors and deterministic BTD features derived from approved GOES ABI channels. It did not introduce candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: focal_tversky`, and one `centerline_logits` auxiliary output using trusted `weighted_bce` weight 0.02. `outputs/model_summary.json` reported 12,085,177 parameters against the 25,000,000-parameter smoke ceiling, confirmed GOES ABI channels 1-16 only with forbidden longitude/latitude source channels excluded, and confirmed outputs `mask_logits` plus `centerline_logits`.

The Run completed at batch size 4 on the A100 with 2,553.6 seconds total wall time, 1,195.6 seconds training wall time, 1,356.0 seconds validation wall time, 9,460,252,672 bytes peak CUDA reserved, and no terminal execution failure. The best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, learned mixer | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260830_091941_139456` | ABI-105 | ABI-068 branch, non-amplifying decoder skip gates | 12 | 0.3831 | 0.3820 | 0.3857 | 0.3344 | 0.4484 | 0.2520 | 0.00486 |
| `run_20260829_181201_01c5e7` | ABI-085 | ABI-068 branch, low learning rate | 12 | 0.3826 | 0.3733 | 0.4059 | 0.3693 | 0.3968 | 0.3698 | 0.00389 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, centerline aux | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260830_115800_4a2363` | ABI-108 | ABI-068 branch, added Line Target auxiliary head | 9 | 0.3822 | 0.3660 | 0.4242 | 0.3938 | 0.3713 | 0.3575 | 0.00342 |
| `run_20260830_125040_95bfb5` | ABI-109 | ABI-068 branch, deterministic raw+BTD front end | 12 | 0.3718 | 0.3579 | 0.4045 | 0.3507 | 0.3955 | 0.2976 | 0.00409 |

ABI-109 did not meet the preregistered useful-continuation criteria relative to ABI-068. Aggregate filtered Dice decreased from 0.3964 to 0.3718 (-0.0246), which is more than the approximately 0.02 fallback threshold and outside the within-0.01 retention criterion. Filtered recall was effectively retained (+0.0019), and both Dataset Sources stayed above 0.35 filtered Dice, but this came with lower filtered precision (-0.0485), lower filtered connectivity (-0.0924), and a higher filtered predicted-positive fraction (+14.4%). MIT filtered Dice fell from 0.3886 to 0.3579, and Google filtered Dice fell from 0.4161 to 0.4045.

Relative to ABI-066, ABI-109 had higher recall (+0.0587) but lower aggregate filtered Dice (-0.0108), lower precision (-0.0920), lower connectivity (-0.1755), lower Google filtered Dice (-0.0247), and substantially larger positive area. It therefore did not recover ABI-066's precision/connectivity-forward operating profile. Relative to ABI-085 and ABI-108, ABI-109 was also lower on aggregate filtered Dice, precision, connectivity, and Google Dice. ABI-109 only slightly exceeded ABI-071 among nearby frequency-gated variants and did not displace the current references.

## ABI-109 trajectory

ABI-109 trained finitely and avoided terminal all-negative or all-positive collapse. Filtered Dice by epoch was 0.1845, 0.1950, 0.2476, 0.3078, 0.3063, 0.2981, 0.3269, 0.3439, 0.3430, 0.3214, 0.2917, and 0.3718. The selected checkpoint was epoch 12 after a noisy epoch-10/11 dip, so the run ended at its best validation point.

At the selected checkpoint, filtered Dice was 0.3718, raw Dice 0.3833, filtered precision 0.3507, filtered recall 0.3955, filtered connectivity 0.2976, and filtered predicted-positive fraction 0.00409. Source-stratified filtered Dice was 0.3579 MIT and 0.4045 Google. Training loss declined from 0.9275 at epoch 1 to 0.8544 at epoch 12; validation loss declined from 0.9265 to 0.8847.

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice 0.3833 versus filtered Dice 0.3718, and raw predicted-positive fraction 0.00435 versus filtered 0.00409. This is not primarily an Artifact Filter dependence issue. The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` all have near-zero per-sample Dice; because prediction retention is fixed `first_n`, these are bounded artifacts and not representative qualitative evidence.

## Interpretation

Classify ABI-109 as finite, resource-feasible, non-collapsed, but negative capped family-development evidence for the exact deterministic-front-end ablation. Removing the learned spectral mixer did not improve positive-area discipline, precision, connectivity, or source behavior. Instead, it preserved recall while increasing predicted-positive fraction and reducing the metrics that motivated the ablation.

This result weakens the hypothesis that ABI-068's learned 1x1 mixer is the main cause of recall-forward clutter in the frequency-gated branch. The deterministic raw+BTD front end may be numerically stable, but it appears less calibrated for the current focal-Tversky operating point. The learned mixer should not be removed from the current ABI-068-like branch without a stronger accompanying mechanism for precision/connectivity recovery.

The broader frequency-gated line U-Net family remains viable because ABI-068, ABI-066, ABI-085, and several neighboring variants remain stronger capped references. Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-109 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-109. Stop this exact deterministic-front-end ablation and do not spend another step repairing or retuning it unless a clear implementation bug is found. A whole-validation failure-bucket Evaluation Request is not warranted for ABI-109 because it missed the ABI-068-relative retention criterion, did not improve precision/connectivity/positive-area discipline, and is below stronger frequency-gated references.

Retain ABI-068 as the local aggregate-Dice reference and ABI-066 as the precision/connectivity reference. A future useful hypothesis should broaden beyond another local ABI-068 front-end/gate/small-auxiliary tweak toward a materially different contract-compliant mechanism for calibration, false-positive suppression, source robustness, or thin-line continuity while preserving provider/Harness ownership of thresholding, Artifact Filters, data loading, split logic, sampling implementation, augmentation implementation, target derivation, losses, metrics, resource placement, and lifecycle behavior.

## Artifact references

- `run_20260830_125040_95bfb5/outputs/best_metrics.json`
- `run_20260830_125040_95bfb5/outputs/final_metrics.json`
- `run_20260830_125040_95bfb5/outputs/metrics.jsonl`
- `run_20260830_125040_95bfb5/outputs/resource_profile.json`
- `run_20260830_125040_95bfb5/outputs/model_summary.json`
- `run_20260830_125040_95bfb5/outputs/prediction_samples/samples.json`
- `run_20260830_125040_95bfb5/resolved_manifest.yaml`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260829_181201_01c5e7/outputs/best_metrics.json`
- `run_20260830_110428_804d89/outputs/best_metrics.json`
- `run_20260830_115800_4a2363/outputs/best_metrics.json`
