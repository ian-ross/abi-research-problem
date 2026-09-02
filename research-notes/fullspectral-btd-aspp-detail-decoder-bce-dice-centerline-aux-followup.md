# Full-spectral BTD ASPP/detail decoder BCE-Dice centerline-auxiliary follow-up

research-figures: []

## Scope

This note records ABI-126 after Run `run_20260831_085615_d05ab3` completed.

Source Runs:

- ABI-126 ASPP/detail decoder BCE-Dice centerline-auxiliary follow-up: `run_20260831_085615_d05ab3`
- ABI-121 ASPP/detail decoder focal-Tversky centerline-auxiliary comparison target: `run_20260831_041559_43da35`
- ABI-120 ASPP/detail decoder BCE-Dice-clDice centerline-auxiliary scout: `run_20260831_033037_bad0bb`
- ABI-122 ASPP/detail decoder directional-continuity focal-Tversky negative follow-up: `run_20260831_045937_fa4e34`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`

ABI-126 was a family-development continuation of ABI-121. It kept the compact full-spectral BTD ASPP/detail decoder architecture, provider-approved `abi_16ch` input mode, combined source-balanced sampling, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and low-weight provider-derived Centerline Target auxiliary supervision at weight 0.02. The controlled manifest change from ABI-121 was the trusted primary loss: `focal_tversky` was replaced by `bce_dice`. This is capped representative evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-126 stayed inside the Candidate Experiment Contract. Candidate code owned only the model architecture over provider-approved ABI Channel Input and deterministic brightness-temperature-difference planes derived from GOES ABI channels 1-16. It did not introduce longitude, latitude, reconstructed coordinates, Solar Geometry Input, candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or lifecycle behavior.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: bce_dice`, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and one provider-derived Centerline Target auxiliary output `centerline_logits` with trusted `weighted_bce` weight 0.02. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records.

`outputs/model_summary.json` reported 9,619,514 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,176.9 seconds total wall time, 972.4 seconds training wall time, 1,202.5 seconds validation wall time, 5,898,365,952 bytes peak CUDA allocated, 6,450,839,552 bytes peak CUDA reserved, and no terminal execution failure. The selected best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, centerline aux | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260831_033037_bad0bb` | ABI-120 | ASPP/detail decoder, `bce_dice_cldice`, centerline aux | 10 | 0.3667 | 0.3485 | 0.4078 | 0.4366 | 0.3161 | 0.3681 | 0.00262 |
| `run_20260831_041559_43da35` | ABI-121 | ASPP/detail decoder, focal-Tversky, centerline aux | 12 | 0.3884 | 0.3835 | 0.4005 | 0.3526 | 0.4323 | 0.2315 | 0.00444 |
| `run_20260831_045937_fa4e34` | ABI-122 | ABI-121 plus directional-continuity refinement | 8 | 0.3382 | 0.3471 | 0.3204 | 0.2869 | 0.4118 | 0.1690 | 0.00520 |
| `run_20260831_085615_d05ab3` | ABI-126 | ABI-121 architecture with BCE-Dice primary loss | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |

ABI-126 substantially met the loss-calibration hypothesis but with a source-skewed trade-off. Relative to ABI-121, aggregate filtered Dice was nearly tied but slightly lower, 0.3859 versus 0.3884 (-0.0026). ABI-126 strongly improved filtered precision from 0.3526 to 0.4746 (+0.1220), filtered connectivity from 0.2315 to 0.4517 (+0.2202), and filtered predicted-positive fraction from 0.00444 to 0.00248 (-0.00196). It also improved Google filtered Dice from 0.4005 to 0.4415 (+0.0410). The cost was recall and MIT sensitivity: filtered recall decreased from 0.4323 to 0.3251 (-0.1073), and MIT filtered Dice decreased from 0.3835 to 0.3635 (-0.0200).

Relative to ABI-120, ABI-126 is a clear improvement within the ASPP/detail family: aggregate filtered Dice increased by 0.0191, MIT filtered Dice by 0.0150, Google filtered Dice by 0.0336, precision by 0.0380, recall by 0.0089, connectivity by 0.0836, and predicted-positive fraction decreased slightly from 0.00262 to 0.00248. This means BCE-Dice did not merely return to the conservative clDice branch; it produced a cleaner and stronger ASPP/detail precision/connectivity point than ABI-120 while preserving a small recall gain.

Relative to ABI-068, ABI-126 is not the capped aggregate-Dice reference. Aggregate filtered Dice is lower by 0.0105 and MIT filtered Dice is lower by 0.0251. However, ABI-126 improves Google filtered Dice by 0.0254, precision by 0.0755, connectivity by 0.0617, and positive-area discipline by reducing filtered predicted-positive fraction from 0.00357 to 0.00248. Relative to ABI-066, ABI-126 has slightly higher aggregate filtered Dice, higher Google Dice, higher precision, and lower predicted-positive fraction, with slightly lower MIT Dice, recall, and connectivity.

## ABI-126 trajectory

ABI-126 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.1807, 0.2850, 0.3168, 0.3169, 0.3379, 0.3640, 0.3637, 0.3731, 0.3638, 0.3691, 0.3565, and 0.3859. The selected checkpoint was the final epoch 12, so the branch retained a late improvement signal rather than plateauing into a clear dead branch.

At the selected checkpoint, raw Dice was 0.4013 and filtered Dice was 0.3859. Filtered precision was 0.4746, filtered recall 0.3251, filtered connectivity 0.4517, and filtered predicted-positive fraction 0.00248. Source-stratified filtered Dice was unbalanced but informative: Google reached 0.4415 with precision 0.4672, recall 0.4185, connectivity 0.4653, and filtered predicted-positive fraction 0.00165, while MIT reached 0.3635 with precision 0.4784, recall 0.2931, connectivity 0.4381, and filtered predicted-positive fraction 0.00331. Both Dataset Sources were finite and non-collapsed, but the BCE-Dice calibration favored high precision and Google performance over MIT recall.

Raw-to-filtered differences were modest: raw Dice 0.4013 versus filtered Dice 0.3859, and raw predicted-positive fraction 0.00265 versus filtered 0.00248. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples had one perfect empty/negative sample and three near-zero per-sample Dice values, but the retention policy is fixed `first_n`, so these bounded artifacts should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-126 as finite, resource-feasible, non-collapsed, and positive capped family-development evidence for loss calibration in the ASPP/detail decoder family. The controlled BCE-Dice loss change mostly delivered the intended middle point: it sharply reduced ABI-121's focal-Tversky positive-area clutter and weak connectivity while staying near ABI-121 on aggregate filtered Dice and improving Google Dice. It also dominated ABI-120's clDice ASPP/detail scout on the main capped family diagnostics.

ABI-126 is not a promotion claim. All reported metrics are from the trusted capped representative 1,024-record-per-Dataset-Source/split policy, while canonical MCAST 2.1 remains the full Working Validation Split promotion context. Capped aggregate or Google improvements must not be interpreted as full-data evidence.

The main weakness is MIT recall. ABI-126 is now the strongest ASPP/detail precision/connectivity branch and a useful comparator to ABI-066, but it is not a clean replacement for ABI-121's recall/source-balance role or ABI-068's aggregate capped reference. The source split suggests the ASPP/detail architecture plus BCE-Dice may calibrate false positives well, especially on Google, while under-segmenting MIT positives relative to focal-Tversky.

## Decision

Do not promote ABI-126 and do not reinterpret capped representative evidence as full-data evidence. Retain ABI-068 as the local capped aggregate-Dice reference, ABI-066 as the mature precision/connectivity reference, ABI-121 as the ASPP/detail recall/source-balance result, and ABI-126 as the best ASPP/detail precision/connectivity and Google-Dice result.

Stop repeating simple ASPP/detail loss swaps: the trusted loss allowlist has now mapped three useful points for this architecture (`bce_dice_cldice`, `focal_tversky`, and `bce_dice`). A reasonable next step is either a bounded whole-validation failure-bucket diagnostic for ABI-126 if the campaign needs to compare its apparent clutter reduction against ABI-121 outside the capped subset, or a new in-contract Candidate that broadens away from ASPP/detail loss tuning toward architecture or data-policy mechanisms for preserving BCE-Dice precision/connectivity while recovering MIT recall. Do not repeat ABI-120, ABI-121, ABI-122, or ABI-126 unchanged.

## Artifact references

- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/final_metrics.json`
- `run_20260831_085615_d05ab3/outputs/metrics.jsonl`
- `run_20260831_085615_d05ab3/outputs/resource_profile.json`
- `run_20260831_085615_d05ab3/outputs/model_summary.json`
- `run_20260831_085615_d05ab3/outputs/prediction_samples/samples.json`
- `run_20260831_085615_d05ab3/resolved_manifest.yaml`
- `run_20260831_041559_43da35/outputs/best_metrics.json`
- `run_20260831_033037_bad0bb/outputs/best_metrics.json`
- `run_20260831_045937_fa4e34/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
