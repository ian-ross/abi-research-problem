# Full-spectral BTD ASPP/detail decoder BCE-Dice Line+Centerline auxiliary follow-up

research-figures: []

## Scope

This note records ABI-127 after Run `run_20260831_094013_5ba974` completed.

Source Runs:

- ABI-127 ASPP/detail decoder BCE-Dice Line+Centerline auxiliary follow-up: `run_20260831_094013_5ba974`
- ABI-126 ASPP/detail decoder BCE-Dice Centerline auxiliary comparison target: `run_20260831_085615_d05ab3`
- ABI-121 ASPP/detail decoder focal-Tversky Centerline auxiliary recall/source-balance comparator: `run_20260831_041559_43da35`
- ABI-120 ASPP/detail decoder BCE-Dice-clDice Centerline auxiliary scout: `run_20260831_033037_bad0bb`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`

ABI-127 was a controlled family-development continuation of ABI-126. It kept the compact full-spectral BTD ASPP/detail decoder, provider-approved `abi_16ch` input mode, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and trusted `bce_dice` primary loss. The controlled change was adding a provider-derived Line Target auxiliary output `line_logits` with trusted `weighted_bce` weight 0.02 alongside the existing Centerline Target auxiliary output `centerline_logits` weight 0.02. This is capped representative evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-127 stayed inside the Candidate Experiment Contract. Candidate code owned only the PyTorch architecture over approved ABI Channel Input and deterministic brightness-temperature-difference planes derived from GOES ABI channels 1-16. It did not introduce longitude, latitude, reconstructed coordinates, Solar Geometry Input, candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or lifecycle behavior.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: bce_dice`, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and provider-derived Centerline and Line auxiliary targets using trusted `weighted_bce` at weight 0.02 each. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records.

`outputs/model_summary.json` reported 9,619,555 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,158.1 seconds total wall time, 976.3 seconds training wall time, 1,179.9 seconds validation wall time, 5,899,418,112 bytes peak CUDA allocated, 6,452,936,704 bytes peak CUDA reserved, and no terminal execution failure. The selected best-validation checkpoint was epoch 9.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, centerline aux | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, centerline aux | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260831_041559_43da35` | ABI-121 | ASPP/detail decoder, focal-Tversky, centerline aux | 12 | 0.3884 | 0.3835 | 0.4005 | 0.3526 | 0.4323 | 0.2315 | 0.00444 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, centerline aux | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260831_094013_5ba974` | ABI-127 | ABI-126 plus Line Target auxiliary head | 9 | 0.3797 | 0.3653 | 0.4150 | 0.4280 | 0.3412 | 0.3054 | 0.00289 |

ABI-127 only partially met the intended effect. At the selected best epoch, it improved recall over ABI-126 from 0.3251 to 0.3412 (+0.0161) and marginally improved MIT filtered Dice from 0.3635 to 0.3653 (+0.0018). However, the recovered recall was small and came with lower aggregate filtered Dice (0.3797 vs 0.3859, -0.0061), lower Google filtered Dice (0.4150 vs 0.4415, -0.0265), lower filtered precision (0.4280 vs 0.4746, -0.0466), and lower filtered connectivity (0.3054 vs 0.4517, -0.1463). This is not a favorable trade-off relative to ABI-126.

Relative to ABI-121, ABI-127 remained more conservative and more precise, but it did not reproduce ABI-121's recall/source-balance behavior. ABI-127 filtered recall was 0.3412 versus ABI-121's 0.4323, MIT filtered Dice was 0.3653 versus 0.3835, and Google filtered Dice was 0.4150 versus 0.4005. The Line auxiliary head moved ABI-127 slightly away from ABI-126's highest-precision/high-Google point but not far enough toward ABI-121's useful recall regime.

Relative to the broader local references, ABI-127 is below ABI-068 on aggregate filtered Dice (0.3797 vs 0.3964), MIT Dice (0.3653 vs 0.3886), recall (0.3412 vs 0.3936), and connectivity (0.3054 vs 0.3900). It is also below ABI-066's precision/connectivity reference on aggregate filtered Dice (0.3797 vs 0.3825), Google Dice (0.4150 vs 0.4292), precision (0.4280 vs 0.4427), and connectivity (0.3054 vs 0.4731), though it has slightly higher MIT Dice and recall.

## ABI-127 trajectory

ABI-127 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.2204, 0.2713, 0.3135, 0.3061, 0.3397, 0.3629, 0.3493, 0.3636, 0.3797, 0.3318, 0.3610, and 0.3759. The best checkpoint was epoch 9, while the final epoch recovered to 0.3759 after a sharp epoch-10 drop. This is a noisy but finite trajectory, not a hard optimization failure.

At the best checkpoint, raw Dice was 0.3941 and filtered Dice was 0.3797. Filtered precision was 0.4280, filtered recall 0.3412, filtered connectivity 0.3054, and filtered predicted-positive fraction 0.00289. Source-stratified filtered Dice was 0.3653 for MIT and 0.4150 for Google. At the final epoch, precision rose to 0.4966 and predicted-positive fraction fell to 0.00221, but recall fell to 0.3024 and aggregate filtered Dice to 0.3759. The final state suggests the Line+Centerline auxiliary branch can become even more conservative under BCE-Dice, rather than reliably restoring MIT recall.

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice 0.3941 versus filtered Dice 0.3797, and raw predicted-positive fraction 0.00308 versus filtered 0.00289. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples are available for traceability, but the retention policy is fixed `first_n`, so these bounded artifacts should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-127 as finite, resource-feasible, non-collapsed, but a negative-to-mixed capped family-development result for the specific ABI-126 Line+Centerline auxiliary hypothesis. The added Line Target auxiliary signal produced a small recall and MIT-Dice gain over ABI-126's Centerline-only BCE-Dice branch, but it did not solve the MIT recall weakness and it degraded the main precision/connectivity strengths that made ABI-126 interesting.

This result does not eliminate the ASPP/detail decoder family as a whole: ABI-121 remains a useful focal-Tversky recall/source-balance point and ABI-126 remains a useful BCE-Dice precision/connectivity and Google-Dice point. It does, however, weaken the case for further simple auxiliary-head additions within the ASPP/detail BCE-Dice branch. The family has now mapped clDice, focal-Tversky, BCE-Dice, directional-continuity refinement, and Line+Centerline auxiliary variants under the capped policy.

All metrics here are from the trusted capped representative 1,024-record-per-Dataset-Source/split policy. They are feasibility and family-development evidence only; they are not full-data promotion evidence and should not be compared to canonical MCAST Working Validation Split results as promotion-grade claims.

## Decision

Do not promote ABI-127. Do not repeat ABI-127 unchanged, and do not spend another Autonomy Step on a simple additional auxiliary-head variant for the ASPP/detail BCE-Dice branch unless a new diagnostic specifically identifies the auxiliary target as the limiting factor.

Retain ABI-068 as the local capped aggregate-Dice reference, ABI-066 as the precision/connectivity reference, ABI-121 as the ASPP/detail recall/source-balance comparator, and ABI-126 as the ASPP/detail precision/connectivity and Google-Dice comparator. For the next in-contract step, prefer broadening beyond simple ASPP/detail auxiliary tuning: either a bounded whole-validation diagnostic comparing ABI-121 and ABI-126 failure modes, or a new architecture/training-policy/data-policy mechanism aimed at preserving ABI-126-like positive-area discipline while recovering MIT recall.

## Artifact references

- `run_20260831_094013_5ba974/outputs/best_metrics.json`
- `run_20260831_094013_5ba974/outputs/final_metrics.json`
- `run_20260831_094013_5ba974/outputs/metrics.jsonl`
- `run_20260831_094013_5ba974/outputs/resource_profile.json`
- `run_20260831_094013_5ba974/outputs/model_summary.json`
- `run_20260831_094013_5ba974/outputs/prediction_samples/samples.json`
- `run_20260831_094013_5ba974/resolved_manifest.yaml`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260831_041559_43da35/outputs/best_metrics.json`
- `run_20260831_033037_bad0bb/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
