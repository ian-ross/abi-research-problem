# Full-spectral BTD frequency-gated line U-Net additive directional-context follow-up

research-figures: []

## Scope

This note records ABI-125 after Run `run_20260831_075213_ee1519` completed.

Source Runs:

- ABI-125 additive directional-context frequency-gated line U-Net follow-up: `run_20260831_075213_ee1519`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-121 ASPP/detail decoder focal-Tversky recall/source-balance comparator: `run_20260831_041559_43da35`
- ABI-123 patch-objectness gated frequency-gated line U-Net negative calibration comparator: `run_20260831_060046_508684`
- ABI-124 stem detail-agreement calibrated frequency-gated line U-Net comparator: `run_20260831_065423_01a457`

ABI-125 was a family-development continuation of ABI-068. It kept the provider-approved `abi_16ch` input mode, deterministic raw-plus-BTD front-end features derived only from GOES ABI channels 1-16, the frequency-gated encoder/decoder, trusted `focal_tversky` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced sampling, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, and disabled early stopping. The controlled architectural change was one neutral-initialized additive directional-context bridge after high-resolution frequency-pyramid fusion, intended to add horizontal, vertical, dilated line, local-detail, and smoothed context features without multiplicatively suppressing weak contrail evidence.

This is capped representative evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-125 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI Channel Input and deterministic BTD combinations from ABI channels 1-16. It did not introduce longitude, latitude, reconstructed coordinates, candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, filesystem writes, network access, pretrained weights, resource placement, or lifecycle behavior.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: focal_tversky`, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and one provider-derived Centerline Target auxiliary output `centerline_logits` with trusted `weighted_bce` weight 0.02. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records.

`outputs/model_summary.json` reported 12,547,669 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 3,262.5 seconds total wall time, 1,696.1 seconds training wall time, 1,564.2 seconds validation wall time, 10,024,086,016 bytes peak CUDA allocated, 11,219,763,200 bytes peak CUDA reserved, and no terminal execution failure. The selected best-validation checkpoint was epoch 12.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, centerline aux | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260831_041559_43da35` | ABI-121 | ASPP/detail decoder, focal-Tversky, centerline aux | 12 | 0.3884 | 0.3835 | 0.4005 | 0.3526 | 0.4323 | 0.2315 | 0.00444 |
| `run_20260831_060046_508684` | ABI-123 | ABI-068 plus neutral patch-objectness mask gate | 10 | 0.3453 | 0.3544 | 0.3267 | 0.2979 | 0.4106 | 0.1411 | 0.00499 |
| `run_20260831_065423_01a457` | ABI-124 | ABI-068 plus neutral stem detail-agreement calibrator | 12 | 0.3753 | 0.3775 | 0.3702 | 0.3278 | 0.4388 | 0.2021 | 0.00485 |
| `run_20260831_075213_ee1519` | ABI-125 | ABI-068 plus neutral additive directional-context bridge | 12 | 0.3733 | 0.3663 | 0.3885 | 0.3538 | 0.3950 | 0.2077 | 0.00405 |

ABI-125 did not meet the preregistered ABI-068-relative success criterion. Relative to ABI-068, aggregate filtered Dice decreased from 0.3964 to 0.3733 (-0.0231), MIT filtered Dice from 0.3886 to 0.3663 (-0.0223), Google filtered Dice from 0.4161 to 0.3885 (-0.0276), filtered precision from 0.3992 to 0.3538 (-0.0454), and filtered connectivity from 0.3900 to 0.2077 (-0.1824). Filtered recall was essentially retained, 0.3950 versus 0.3936 (+0.0014), but the filtered predicted-positive fraction increased from 0.00357 to 0.00405.

Relative to ABI-124, ABI-125 was a cleaner calibration trade-off but not a stronger aggregate Result. It lowered the filtered predicted-positive fraction from 0.00485 to 0.00405 and raised precision from 0.3278 to 0.3538, while decreasing aggregate Dice slightly from 0.3753 to 0.3733, decreasing MIT Dice from 0.3775 to 0.3663, decreasing recall from 0.4388 to 0.3950, and improving Google Dice from 0.3702 to 0.3885. This suggests the non-suppressive additive bridge avoided ABI-123/ABI-124's worst over-recall behavior, but it still failed to recover ABI-068-level connectivity.

Relative to ABI-066, ABI-125 had lower aggregate Dice, lower Google Dice, lower precision, lower connectivity, and a higher predicted-positive fraction, with higher recall. Relative to ABI-121, ABI-125 had lower aggregate Dice, lower MIT Dice, lower Google Dice, much lower recall, slightly higher precision, lower connectivity, and a lower predicted-positive fraction. It is therefore not a better aggregate reference, precision/connectivity reference, or recall/source-balance reference.

## ABI-125 trajectory

ABI-125 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.1985, 0.2769, 0.3131, 0.2782, 0.3219, 0.2948, 0.3146, 0.3286, 0.3469, 0.3320, 0.3212, and 0.3733. The selected checkpoint was the final epoch 12, so there was a late improvement after several noisy mid-run regressions.

At the selected checkpoint, raw Dice was 0.3856 and filtered Dice was 0.3733. Filtered precision was 0.3538, filtered recall 0.3950, filtered connectivity 0.2077, and filtered predicted-positive fraction 0.00405. Source-stratified filtered Dice was 0.3663 MIT and 0.3885 Google. Google recall remained high at 0.5075, while Google precision and connectivity were only 0.3147 and 0.1812. MIT precision was higher at 0.3766, but MIT recall was lower at 0.3566.

Raw-to-filtered differences were modest: raw Dice 0.3856 versus filtered Dice 0.3733, and raw predicted-positive fraction 0.00430 versus filtered 0.00405. This does not indicate primary Artifact Filter dependence. The failure mode is intrinsic: the added context bridge retained recall but diluted the frequency-gated family’s precision/connectivity discipline.

The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` have near-zero individual Dice, but the retention policy is fixed `first_n`, so these bounded artifacts should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-125 as finite, resource-feasible, non-collapsed, and informative, but unsuccessful against its preregistered ABI-068-relative goal. The result gives a useful distinction within the recent calibration/add-on attempts: additive directional context is less damaging to precision and positive-area calibration than the patch-objectness gate and stem detail-agreement branch, yet it still substantially loses the connectivity that made ABI-068 and ABI-066 useful capped references.

The repeated pattern across ABI-123, ABI-124, and ABI-125 argues against continuing small ABI-068 add-on calibration/context bridges under the current focal-Tversky, centerline-auxiliary, combined source-balanced, random-mirroring, 12-epoch configuration. The broader frequency-gated line U-Net family remains viable through earlier references, especially ABI-068 for aggregate Dice and ABI-066 for precision/connectivity. The next useful in-contract step should broaden away from additive/suppressive/agreement post-fusion add-ons and either revisit the better frequency-gated reference through a controlled loss/data-policy diagnostic or scout a different non-suppressive line-aware architecture family.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-125 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-125. Do not request whole-validation diagnostics for ABI-125 ahead of stronger references. Stop this exact additive directional-context bridge branch unless later implementation review identifies a narrow candidate bug that explains the connectivity regression.

Retain ABI-068 as the local capped aggregate-Dice reference, ABI-066 as the precision/connectivity reference, and ABI-121 as the ASPP/detail recall/source-balance comparator. A reasonable next hypothesis should broaden the frontier rather than add another small calibrator to ABI-068; candidate directions include a simpler ABI-068 loss/data-policy comparison, a non-gated line-aware decoder scout, or a bounded diagnostic proposal around the recall-versus-connectivity trade-off in focal-Tversky frequency-gated variants.

## Artifact references

- `run_20260831_075213_ee1519/outputs/best_metrics.json`
- `run_20260831_075213_ee1519/outputs/final_metrics.json`
- `run_20260831_075213_ee1519/outputs/metrics.jsonl`
- `run_20260831_075213_ee1519/outputs/resource_profile.json`
- `run_20260831_075213_ee1519/outputs/model_summary.json`
- `run_20260831_075213_ee1519/outputs/prediction_samples/samples.json`
- `run_20260831_075213_ee1519/resolved_manifest.yaml`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260831_041559_43da35/outputs/best_metrics.json`
- `run_20260831_060046_508684/outputs/best_metrics.json`
- `run_20260831_065423_01a457/outputs/best_metrics.json`
