# Full-spectral BTD frequency-gated line U-Net stem detail-agreement follow-up

research-figures: []

## Scope

This note records ABI-124 after Run `run_20260831_065423_01a457` completed.

Source Runs:

- ABI-124 stem detail-agreement calibrated frequency-gated line U-Net follow-up: `run_20260831_065423_01a457`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-121 ASPP/detail decoder focal-Tversky recall/source-balance comparator: `run_20260831_041559_43da35`
- ABI-123 patch-objectness gated frequency-gated line U-Net negative calibration comparator: `run_20260831_060046_508684`

ABI-124 was a family-development continuation of ABI-068. It kept the provider-approved `abi_16ch` input mode, deterministic raw-plus-BTD front-end features derived only from GOES ABI channels 1-16, the frequency-gated encoder/decoder, trusted `focal_tversky` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced sampling, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, and disabled early stopping. The controlled architectural change was one neutral-initialized full-resolution stem detail-agreement calibrator intended to make early high-frequency detail and smoothed context agree before clutter propagated through the encoder.

This is capped representative evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-124 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI Channel Input and deterministic BTD combinations from ABI channels 1-16. It did not introduce longitude, latitude, reconstructed coordinates, candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, filesystem writes, network access, pretrained weights, resource placement, or lifecycle behavior.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: focal_tversky`, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and one provider-derived Centerline Target auxiliary output `centerline_logits` with trusted `weighted_bce` weight 0.02. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records.

`outputs/model_summary.json` reported 12,186,869 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,921.4 seconds total wall time, 1,498.5 seconds training wall time, 1,420.8 seconds validation wall time, 9,247,859,200 bytes peak CUDA allocated, 10,651,435,008 bytes peak CUDA reserved, and no terminal execution failure. The selected best-validation checkpoint was epoch 12.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, centerline aux | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260831_041559_43da35` | ABI-121 | ASPP/detail decoder, focal-Tversky, centerline aux | 12 | 0.3884 | 0.3835 | 0.4005 | 0.3526 | 0.4323 | 0.2315 | 0.00444 |
| `run_20260831_060046_508684` | ABI-123 | ABI-068 plus neutral patch-objectness mask gate | 10 | 0.3453 | 0.3544 | 0.3267 | 0.2979 | 0.4106 | 0.1411 | 0.00499 |
| `run_20260831_065423_01a457` | ABI-124 | ABI-068 plus neutral stem detail-agreement calibrator | 12 | 0.3753 | 0.3775 | 0.3702 | 0.3278 | 0.4388 | 0.2021 | 0.00485 |

ABI-124 partially repaired the ABI-123 calibration failure but did not meet the ABI-068-relative hypothesis. Relative to ABI-123, ABI-124 increased aggregate filtered Dice from 0.3453 to 0.3753 (+0.0300), MIT Dice from 0.3544 to 0.3775 (+0.0231), Google Dice from 0.3267 to 0.3702 (+0.0435), filtered precision from 0.2979 to 0.3278 (+0.0299), filtered recall from 0.4106 to 0.4388 (+0.0282), and filtered connectivity from 0.1411 to 0.2021 (+0.0610), while slightly lowering the filtered predicted-positive fraction from 0.00499 to 0.00485. This supports the narrow interpretation that early pixelwise detail/context calibration is less harmful than a blunt patch-objectness mask gate.

The result still regressed relative to ABI-068. Aggregate filtered Dice decreased from 0.3964 to 0.3753 (-0.0211), Google filtered Dice from 0.4161 to 0.3702 (-0.0459), filtered precision from 0.3992 to 0.3278 (-0.0714), and filtered connectivity from 0.3900 to 0.2021 (-0.1879). Filtered recall increased from 0.3936 to 0.4388 (+0.0451), but that increase came with a higher filtered predicted-positive fraction, 0.00485 versus ABI-068's 0.00357. The preregistered success criterion of preserving ABI-068-like Dice within about 0.01 or improving precision/connectivity was not met.

Relative to ABI-066, ABI-124 recovered some recall but lost precision, connectivity, Google Dice, and aggregate Dice. Relative to ABI-121, ABI-124 had slightly higher recall but lower aggregate/source Dice, lower precision, lower connectivity, and higher predicted-positive fraction. Thus ABI-124 is not a better aggregate reference, precision/connectivity reference, or source-balance reference.

## ABI-124 trajectory

ABI-124 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.2052, 0.2241, 0.2922, 0.3130, 0.3401, 0.2691, 0.3149, 0.3146, 0.3615, 0.3578, 0.3148, and 0.3753. The selected checkpoint was the final epoch 12, so the branch retained a late improving signal despite high epoch-to-epoch variance.

At the selected checkpoint, raw Dice was 0.3871 and filtered Dice was 0.3753. Filtered precision was 0.3278, filtered recall 0.4388, filtered connectivity 0.2021, and filtered predicted-positive fraction 0.00485. Source-stratified filtered Dice was balanced but not strong: 0.3775 MIT and 0.3702 Google. Google recall was high at 0.5256, but Google precision and connectivity remained weak enough to pull Google Dice far below the ABI-068 reference.

Raw-to-filtered differences were modest: raw Dice 0.3871 versus filtered Dice 0.3753, and raw predicted-positive fraction 0.00517 versus filtered 0.00485. This does not indicate primary Artifact Filter dependence. The failure mode is intrinsic loss of precision/connectivity and elevated positive area before filtering. The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` have near-zero individual Dice, but the retention policy is fixed `first_n`, so these bounded artifacts should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-124 as finite, resource-feasible, non-collapsed, and informative but not successful against its preregistered ABI-068-relative goal. The stem detail-agreement calibrator improved over the ABI-123 patch-objectness gate, which means not all neutral calibration blocks are equally damaging. However, the improvement was still insufficient: ABI-124 remained below ABI-068 on aggregate Dice, below ABI-066 on precision/connectivity discipline, and below ABI-121 on aggregate/source Dice.

The result argues against continuing this exact stem detail-agreement calibrator under the current focal-Tversky, centerline-auxiliary, combined source-balanced, random-mirroring, 12-epoch configuration. It does not eliminate the broader frequency-gated line U-Net family or all in-model calibration ideas. The useful lesson is more specific: suppressive or agreement-style calibrators added to ABI-068 have repeatedly traded precision/connectivity discipline for recall or variance without recovering the ABI-068 aggregate-Dice reference.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-124 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-124. Do not request whole-validation diagnostics for ABI-124 ahead of stronger references. Stop this exact stem detail-agreement branch unless later implementation review identifies a narrow candidate bug that explains the regression.

Retain ABI-068 as the local capped aggregate-Dice reference, ABI-066 as the precision/connectivity reference, and ABI-121 as the ASPP/detail recall/source-balance comparator. A useful next step should broaden away from additional suppressive or agreement-gated variants of ABI-068. In-contract options include a different line-aware architecture family with non-suppressive context aggregation, a loss/data-policy comparison around the better ABI-068 reference, or bounded diagnostics focused on why the current focal-Tversky line-family variants gain recall at the cost of precision and connectivity.

## Artifact references

- `run_20260831_065423_01a457/outputs/best_metrics.json`
- `run_20260831_065423_01a457/outputs/final_metrics.json`
- `run_20260831_065423_01a457/outputs/metrics.jsonl`
- `run_20260831_065423_01a457/outputs/resource_profile.json`
- `run_20260831_065423_01a457/outputs/model_summary.json`
- `run_20260831_065423_01a457/outputs/prediction_samples/samples.json`
- `run_20260831_065423_01a457/resolved_manifest.yaml`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260831_041559_43da35/outputs/best_metrics.json`
- `run_20260831_060046_508684/outputs/best_metrics.json`
