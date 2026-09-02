# Full-spectral BTD ASPP/detail decoder directional-continuity follow-up

research-figures: []

## Scope

This note records ABI-122 after Run `run_20260831_045937_fa4e34` completed.

Source Runs:

- ABI-122 ASPP/detail decoder directional-continuity focal-Tversky centerline-auxiliary follow-up: `run_20260831_045937_fa4e34`
- ABI-121 ASPP/detail decoder focal-Tversky centerline-auxiliary comparison target: `run_20260831_041559_43da35`
- ABI-120 ASPP/detail decoder BCE-Dice-clDice centerline-auxiliary scout: `run_20260831_033037_bad0bb`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`

ABI-122 was a family-development continuation of ABI-121. It kept ABI-121's compact full-spectral BTD ASPP/detail encoder-decoder setup, provider-approved `abi_16ch` input mode, combined source-balanced sampling, trusted random mirroring, trusted `focal_tversky` primary loss, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and low-weight provider-derived Centerline Target auxiliary supervision at weight 0.02. The controlled architectural change was a non-suppressive high-resolution directional-continuity refinement block before the output heads. This is capped representative evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-122 stayed inside the Candidate Experiment Contract. Candidate code owned only the model architecture over provider-approved ABI Channel Input and deterministic BTD combinations derived from GOES ABI channels 1-16. It did not introduce longitude, latitude, reconstructed coordinates, candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or lifecycle behavior.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: focal_tversky`, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and one provider-derived Centerline Target auxiliary output `centerline_logits` with trusted `weighted_bce` weight 0.02. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records.

`outputs/model_summary.json` reported 9,914,994 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,488.5 seconds total wall time, 1,208.6 seconds training wall time, 1,278.0 seconds validation wall time, 7,705,513,472 bytes peak CUDA allocated, 8,694,792,192 bytes peak CUDA reserved, and no terminal execution failure. The selected best-validation checkpoint was epoch 8.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, centerline aux | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260831_033037_bad0bb` | ABI-120 | ASPP/detail decoder, `bce_dice_cldice`, centerline aux | 10 | 0.3667 | 0.3485 | 0.4078 | 0.4366 | 0.3161 | 0.3681 | 0.00262 |
| `run_20260831_041559_43da35` | ABI-121 | ASPP/detail decoder, focal-Tversky, centerline aux | 12 | 0.3884 | 0.3835 | 0.4005 | 0.3526 | 0.4323 | 0.2315 | 0.00444 |
| `run_20260831_045937_fa4e34` | ABI-122 | ABI-121 plus directional-continuity refinement | 8 | 0.3382 | 0.3471 | 0.3204 | 0.2869 | 0.4118 | 0.1690 | 0.00520 |

ABI-122 did not meet the preregistered ABI-121-relative hypothesis. Relative to ABI-121, aggregate filtered Dice decreased from 0.3884 to 0.3382 (-0.0502), MIT filtered Dice from 0.3835 to 0.3471 (-0.0364), Google filtered Dice from 0.4005 to 0.3204 (-0.0801), filtered precision from 0.3526 to 0.2869 (-0.0657), filtered recall from 0.4323 to 0.4118 (-0.0206), and filtered connectivity from 0.2315 to 0.1690 (-0.0625). The filtered predicted-positive fraction increased from 0.00444 to 0.00520. The directional-continuity block therefore did not improve the intended line-quality diagnostic and also degraded Dice, precision, and source balance.

Relative to ABI-120, ABI-122 kept similar MIT Dice but lost aggregate filtered Dice (-0.0285), Google filtered Dice (-0.0874), precision (-0.1497), connectivity (-0.1991), and positive-area discipline while improving recall (+0.0956). This suggests the added continuity refinement shifted the ASPP/detail branch toward broader recall-forward masks without preserving the clDice branch's precision/connectivity behavior. Relative to ABI-068 and ABI-066, ABI-122 is clearly behind on aggregate/source Dice, precision, connectivity, and positive-area discipline.

## ABI-122 trajectory

ABI-122 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.1448, 0.1835, 0.2310, 0.2982, 0.3067, 0.2437, 0.2732, 0.3382, 0.3245, 0.3243, 0.3131, and 0.3263. The selected checkpoint was epoch 8; the final four epochs stayed below the selected checkpoint, so the branch did not show a late improving trajectory under the active 12-epoch budget.

At the selected checkpoint, raw Dice was 0.3484 and filtered Dice was 0.3382. Filtered precision was 0.2869, filtered recall 0.4118, filtered connectivity 0.1690, and filtered predicted-positive fraction 0.00520. Source-stratified filtered Dice was 0.3471 MIT and 0.3204 Google. Both Dataset Sources were finite and non-collapsed, but Google precision/connectivity and the aggregate positive-area fraction moved in the wrong direction for the proposed continuity refinement.

Raw-to-filtered differences were modest: raw Dice 0.3484 versus filtered Dice 0.3382, and raw predicted-positive fraction 0.00551 versus filtered 0.00520. This does not indicate primary Artifact Filter dependence; the failure mode is intrinsic low precision/connectivity and elevated positive area before filtering. The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` all had near-zero per-sample Dice, but the retention policy is fixed `first_n`, so these bounded artifacts should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-122 as finite, resource-feasible, non-collapsed, but a negative capped family-development result for this exact directional-continuity refinement. The candidate satisfied lifecycle, resource, coordinate-exclusion, and reporting expectations, but the controlled architectural addition worsened the ABI-121 comparison target on every preregistered useful diagnostic: filtered Dice, source-stratified Dice, precision, recall, connectivity, and predicted-positive fraction.

The result is not a family-wide proof against ASPP/detail decoders. ABI-120 and ABI-121 remain informative: ABI-120 is the cleaner precision-forward clDice ASPP/detail scout, and ABI-121 remains the strongest ASPP/detail result by aggregate Dice and recall/source balance. ABI-122 specifically argues that stacking an additional high-resolution directional-continuity residual after ABI-121's existing line/detail path does not recover connectivity under trusted focal-Tversky plus centerline auxiliary supervision.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-122 is capped representative evidence only and should not be interpreted as a full-data promotion result.

## Decision

Do not promote ABI-122. Do not request whole-validation diagnostics for ABI-122 ahead of stronger ABI-068, ABI-066, ABI-120, or ABI-121 references. Stop this exact ASPP/detail directional-continuity refinement branch unless a later implementation review identifies a narrow candidate bug that explains the metric regression.

Retain ABI-068 as the local capped aggregate-Dice reference, ABI-066 as the precision/connectivity reference, ABI-120 as the ASPP/detail precision-forward clDice result, and ABI-121 as the best ASPP/detail focal-Tversky result. A useful next step should broaden away from additive high-resolution directional-continuity blocks on ABI-121. Reasonable in-contract next hypotheses include bounded whole-validation diagnostics for ABI-121, a different ASPP/detail connectivity mechanism that is not another post-decoder residual line-context block, or a broader architecture frontier focused on calibration/precision without candidate-owned thresholding, postprocessing, losses, sampling, metrics, Artifact Filters, resource placement, or lifecycle behavior.

## Artifact references

- `run_20260831_045937_fa4e34/outputs/best_metrics.json`
- `run_20260831_045937_fa4e34/outputs/final_metrics.json`
- `run_20260831_045937_fa4e34/outputs/metrics.jsonl`
- `run_20260831_045937_fa4e34/outputs/resource_profile.json`
- `run_20260831_045937_fa4e34/outputs/model_summary.json`
- `run_20260831_045937_fa4e34/outputs/prediction_samples/samples.json`
- `run_20260831_045937_fa4e34/resolved_manifest.yaml`
- `run_20260831_041559_43da35/outputs/best_metrics.json`
- `run_20260831_033037_bad0bb/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
