# Full-spectral BTD frequency-gated line U-Net patch-objectness gate follow-up

research-figures: []

## Scope

This note records ABI-123 after Run `run_20260831_060046_508684` completed.

Source Runs:

- ABI-123 patch-objectness gated frequency-gated line U-Net follow-up: `run_20260831_060046_508684`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-121 ASPP/detail decoder focal-Tversky recall/source-balance comparator: `run_20260831_041559_43da35`

ABI-123 was a family-development continuation of ABI-068. It kept ABI-068's provider-approved `abi_16ch` input mode, deterministic raw-plus-BTD front-end features derived only from GOES ABI channels 1-16, learned spectral mixer, frequency-gated encoder/decoder, trusted `focal_tversky` primary loss, low-weight provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced sampling, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, and disabled early stopping. The controlled architectural change was replacing the plain mask head with a neutral-initialized patch-level objectness gate intended to reduce negative-patch clutter without candidate-owned thresholding, postprocessing, Artifact Filters, losses, metrics, target derivation, sampling, data loading, resource placement, or lifecycle behavior.

This is capped representative evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-123 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI Channel Input and deterministic BTD combinations from ABI channels 1-16. It did not introduce longitude, latitude, reconstructed coordinates, candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, filesystem writes, network access, pretrained weights, resource placement, or lifecycle behavior.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: focal_tversky`, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and one provider-derived Centerline Target auxiliary output `centerline_logits` with trusted `weighted_bce` weight 0.02. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records.

`outputs/model_summary.json` reported 12,089,542 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,692.7 seconds total wall time, 1,340.6 seconds training wall time, 1,349.9 seconds validation wall time, 8,156,299,264 bytes peak CUDA allocated, 9,539,944,448 bytes peak CUDA reserved, and no terminal execution failure. The selected best-validation checkpoint was epoch 10.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, centerline aux | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260831_041559_43da35` | ABI-121 | ASPP/detail decoder, focal-Tversky, centerline aux | 12 | 0.3884 | 0.3835 | 0.4005 | 0.3526 | 0.4323 | 0.2315 | 0.00444 |
| `run_20260831_060046_508684` | ABI-123 | ABI-068 plus neutral patch-objectness mask gate | 10 | 0.3453 | 0.3544 | 0.3267 | 0.2979 | 0.4106 | 0.1411 | 0.00499 |

ABI-123 did not meet the preregistered ABI-068-relative hypothesis. Relative to ABI-068, aggregate filtered Dice decreased from 0.3964 to 0.3453 (-0.0511), MIT filtered Dice from 0.3886 to 0.3544 (-0.0342), Google filtered Dice from 0.4161 to 0.3267 (-0.0894), filtered precision from 0.3992 to 0.2979 (-0.1013), and filtered connectivity from 0.3900 to 0.1411 (-0.2490). Filtered recall increased slightly from 0.3936 to 0.4106 (+0.0170), but the filtered predicted-positive fraction also increased from 0.00357 to 0.00499. The patch gate therefore did not reduce positive-area clutter; it shifted the branch toward lower precision and far weaker connectivity.

Relative to ABI-066, ABI-123 gained recall but lost aggregate/source filtered Dice, precision, connectivity, and positive-area discipline. Relative to ABI-121, ABI-123 was lower on aggregate filtered Dice, Google filtered Dice, precision, recall, and connectivity, while only modestly improving MIT Dice. This makes ABI-123 neither a useful frequency-gated-line continuation nor a better recall/source-balance comparator.

## ABI-123 trajectory

ABI-123 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.1630, 0.2173, 0.2821, 0.3103, 0.2694, 0.3057, 0.3185, 0.3145, 0.3453, 0.3453, 0.3281, and 0.3194. The selected checkpoint was epoch 10, effectively tied with epoch 9, and the final two epochs regressed while recall and predicted-positive fraction rose.

At the selected checkpoint, raw Dice was 0.3555 and filtered Dice was 0.3453. Filtered precision was 0.2979, filtered recall 0.4106, filtered connectivity 0.1411, and filtered predicted-positive fraction 0.00499. Source-stratified filtered Dice was 0.3544 MIT and 0.3267 Google. Both Dataset Sources remained finite and non-collapsed, but Google suffered the larger Dice drop relative to ABI-068 and the branch did not preserve source balance.

Raw-to-filtered differences were modest: raw Dice 0.3555 versus filtered Dice 0.3453, and raw predicted-positive fraction 0.00531 versus filtered 0.00499. This does not indicate primary Artifact Filter dependence. The failure mode is intrinsic low precision/connectivity and elevated positive area before filtering. The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` are available, but the retention policy is fixed `first_n`, so these bounded artifacts should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-123 as finite, resource-feasible, non-collapsed, but a negative capped family-development result for this exact patch-objectness gate. The neutral-initialized global gate did not act as the intended conservative suppressor under focal-Tversky training. Instead, it preserved or increased recall at the cost of precision, connectivity, Google Dice, and aggregate Dice.

The result is not a family-wide proof against all in-model calibration mechanisms, nor does it eliminate the ABI-068 frequency-gated line U-Net family. It does specifically argue against adding this patch-level multiplicative/objectness log-bias head to ABI-068 under the current loss, sampling, augmentation, and epoch budget. Whole-validation ABI-121 diagnostics showed negative-patch clutter as a real failure mode, but ABI-123 shows that a patch-level objectness gate is too blunt or poorly coupled to line geometry for this bounded setup.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-123 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-123. Do not request whole-validation diagnostics for ABI-123 ahead of stronger ABI-068, ABI-066, or ABI-121 references. Stop this exact patch-objectness gate branch unless later implementation review identifies a narrow candidate bug that explains the regression.

Retain ABI-068 as the local capped aggregate-Dice reference, ABI-066 as the precision/connectivity reference, and ABI-121 as the ASPP/detail recall/source-balance comparator. A useful next step should broaden away from blunt global suppressive heads. Reasonable in-contract next hypotheses include earlier feature-hierarchy calibration, non-suppressive spectral/detail evidence gating, or a different architecture family that targets false-positive discipline without candidate-owned thresholding, postprocessing, losses, sampling, metrics, Artifact Filters, resource placement, or lifecycle behavior.

## Artifact references

- `run_20260831_060046_508684/outputs/best_metrics.json`
- `run_20260831_060046_508684/outputs/final_metrics.json`
- `run_20260831_060046_508684/outputs/metrics.jsonl`
- `run_20260831_060046_508684/outputs/resource_profile.json`
- `run_20260831_060046_508684/outputs/model_summary.json`
- `run_20260831_060046_508684/outputs/prediction_samples/samples.json`
- `run_20260831_060046_508684/resolved_manifest.yaml`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260831_041559_43da35/outputs/best_metrics.json`
