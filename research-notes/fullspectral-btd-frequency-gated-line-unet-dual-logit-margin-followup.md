# Full-spectral BTD frequency-gated line U-Net dual-logit-margin follow-up

research-figures: []

## Scope

This note records ABI-110 after Run `run_20260830_192051_6b901b` completed.

Source Runs:

- ABI-110 dual-logit-margin focal-Tversky continuation: `run_20260830_192051_6b901b`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-105 conservative-skip focal-Tversky continuation: `run_20260830_091941_139456`
- ABI-107 feature-dropout focal-Tversky continuation: `run_20260830_110428_804d89`
- ABI-108 Line+Centerline auxiliary focal-Tversky continuation: `run_20260830_115800_4a2363`
- ABI-109 deterministic-front-end focal-Tversky continuation: `run_20260830_125040_95bfb5`

ABI-110 was a family-development continuation of ABI-068. It retained provider-approved `abi_16ch` input, deterministic thermal BTD features derived only from GOES ABI channels 1-16, the full-spectral BTD frequency-gated line U-Net branch, trusted focal-Tversky primary loss, provider-derived Centerline Target auxiliary supervision with trusted `weighted_bce` weight 0.02, provider-owned `combined_source_balanced` traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.

The controlled architecture change was replacing the single mask-logit head with a learned foreground-minus-background dual-logit margin head. The hypothesis was that an explicit local foreground/background logit competition could recover positive-area discipline and precision without moving thresholding, losses, Artifact Filters, or postprocessing into Candidate code. This is capped representative evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-110 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI Channel Input and deterministic BTD planes from approved ABI channels. It did not introduce candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: focal_tversky`, and one `centerline_logits` auxiliary output using trusted `weighted_bce` weight 0.02. `outputs/model_summary.json` reported 12,087,606 parameters against the 25,000,000-parameter smoke ceiling, confirmed GOES ABI channels 1-16 only with forbidden longitude/latitude source channels excluded, and confirmed outputs `mask_logits` plus `centerline_logits`.

The Run completed at batch size 4 on the A100 with 2,690.2 seconds total wall time, 1,309.9 seconds training wall time, 1,378.2 seconds validation wall time, 9,592,373,248 bytes peak CUDA reserved, and no terminal execution failure. The best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, learned mixer | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260830_091941_139456` | ABI-105 | ABI-068 branch, conservative non-amplifying skip gates | 12 | 0.3831 | 0.3820 | 0.3857 | 0.3344 | 0.4484 | 0.2520 | 0.00486 |
| `run_20260830_110428_804d89` | ABI-107 | ABI-068 branch, low-probability feature dropout | 12 | 0.3804 | 0.3701 | 0.4046 | 0.3630 | 0.3997 | 0.3182 | 0.00399 |
| `run_20260830_115800_4a2363` | ABI-108 | ABI-068 branch, added Line Target auxiliary head | 9 | 0.3822 | 0.3660 | 0.4242 | 0.3938 | 0.3713 | 0.3575 | 0.00342 |
| `run_20260830_125040_95bfb5` | ABI-109 | ABI-068 branch, deterministic raw+BTD front end | 12 | 0.3718 | 0.3579 | 0.4045 | 0.3507 | 0.3955 | 0.2976 | 0.00409 |
| `run_20260830_192051_6b901b` | ABI-110 | ABI-068 branch, foreground-minus-background dual-logit margin head | 12 | 0.3720 | 0.3706 | 0.3751 | 0.3210 | 0.4422 | 0.2267 | 0.00499 |

ABI-110 did not meet the preregistered useful-continuation criteria relative to ABI-068. Aggregate filtered Dice decreased from 0.3964 to 0.3720 (-0.0244), precision decreased from 0.3992 to 0.3210 (-0.0782), and filtered connectivity decreased from 0.3900 to 0.2267 (-0.1633). Recall increased from 0.3936 to 0.4422 (+0.0486), but the positive-area fraction also increased from roughly 0.00357 to 0.00499. The dual-logit-margin head therefore shifted the branch toward recall and larger positive area rather than improving precision or calibration.

Source behavior was finite and non-catastrophic but not reference-improving. MIT filtered Dice was 0.3706, below ABI-068 by 0.0180 but above ABI-109 by 0.0127. Google filtered Dice was 0.3751, below ABI-068 by 0.0410 and below ABI-109 by 0.0294. The larger Google drop is important because ABI-068's strongest source behavior came from Google filtered Dice above 0.416.

Relative to ABI-105, ABI-110 had slightly lower aggregate Dice (-0.0111), lower precision (-0.0134), similar recall (-0.0062), and lower connectivity (-0.0254). Relative to ABI-107, ABI-110 had lower aggregate Dice (-0.0085), lower precision (-0.0420), higher recall (+0.0425), and lower connectivity (-0.0915). Relative to ABI-108, ABI-110 had lower aggregate Dice (-0.0103), much lower precision (-0.0893), higher recall (+0.0908), and lower connectivity (-0.0530). It did not recover the stronger ABI-066 BCE-Dice-clDice precision/connectivity operating point either.

## ABI-110 trajectory

ABI-110 trained finitely and avoided terminal all-negative or all-positive collapse. Filtered Dice by epoch was 0.2250, 0.2429, 0.3169, 0.3117, 0.3277, 0.2449, 0.2626, 0.3492, 0.3599, 0.3462, 0.3526, and 0.3720. The selected checkpoint was epoch 12 after a noisy mid-run dip, so the run ended at its best validation point.

At the selected checkpoint, filtered Dice was 0.3720, raw Dice 0.3830, filtered IoU 0.2285, filtered precision 0.3210, filtered recall 0.4422, filtered connectivity 0.2267, and filtered predicted-positive fraction 0.00499. Source-stratified filtered Dice was 0.3706 MIT and 0.3751 Google; source filtered recall was 0.4103 MIT and 0.5354 Google, while source filtered precision was 0.3379 MIT and 0.2886 Google. Training loss declined from 0.9329 at epoch 1 to 0.8530 at epoch 12; validation loss declined from 0.9194 to 0.8787.

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice 0.3830 versus filtered Dice 0.3720, and raw predicted-positive fraction 0.00531 versus filtered 0.00499. This is not primarily an Artifact Filter dependence issue. The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` are bounded artifacts under the Harness-owned `first_n` retention policy and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-110 as finite, resource-feasible, non-collapsed, but negative capped family-development evidence for the exact dual-logit-margin head. The head did create the intended foreground/background competition inside the architecture, but the observed effect was a recall-forward, low-precision operating point with reduced connectivity and a larger predicted-positive fraction. That is the opposite of the expected precision/calibration improvement.

This result weakens the idea that the current ABI-068 branch can be improved by another local logit-head competition mechanism alone. Together with ABI-109, it suggests that recent local head/front-end changes are not addressing the main failure mode. The stronger references remain ABI-068 for aggregate filtered Dice and balanced source behavior, ABI-066 for precision/connectivity, ABI-085/ABI-107 for moderate focal-Tversky variants, and ABI-105 as a recall-forward but source-balanced conservative-skip variant.

The broader full-spectral BTD frequency-gated line U-Net family remains viable because ABI-068 exceeded canonical MCAST 2.1 on capped representative filtered Dice and several neighboring variants remain finite and informative. ABI-110 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-110. Stop this exact dual-logit-margin-head branch and do not spend another step repairing or retuning it unless a clear implementation bug is found. A whole-validation failure-bucket Evaluation Request is not warranted for ABI-110 because it missed ABI-068-relative retention, did not improve precision/connectivity/positive-area discipline, and is below stronger frequency-gated references.

Retain ABI-068 as the local aggregate-Dice reference and ABI-066 as the precision/connectivity reference. The next useful hypothesis should broaden beyond local ABI-068 head/front-end/gate tweaks. Promising contract-compliant directions include a materially different calibration-control architecture, a data-policy or loss-policy comparison that the trusted allowlists already support, or a new thin-line continuity mechanism that preserves provider/Harness ownership of thresholding, Artifact Filters, data loading, split logic, sampling implementation, augmentation implementation, target derivation, losses, metrics, resource placement, and lifecycle behavior.

## Artifact references

- `run_20260830_192051_6b901b/outputs/best_metrics.json`
- `run_20260830_192051_6b901b/outputs/final_metrics.json`
- `run_20260830_192051_6b901b/outputs/metrics.jsonl`
- `run_20260830_192051_6b901b/outputs/resource_profile.json`
- `run_20260830_192051_6b901b/outputs/model_summary.json`
- `run_20260830_192051_6b901b/outputs/prediction_samples/samples.json`
- `run_20260830_192051_6b901b/resolved_manifest.yaml`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260830_091941_139456/outputs/best_metrics.json`
- `run_20260830_110428_804d89/outputs/best_metrics.json`
- `run_20260830_115800_4a2363/outputs/best_metrics.json`
- `run_20260830_125040_95bfb5/outputs/best_metrics.json`
