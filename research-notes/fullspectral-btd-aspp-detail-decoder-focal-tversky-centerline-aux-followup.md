# Full-spectral BTD ASPP/detail decoder focal-Tversky centerline-auxiliary follow-up

research-figures: []

## Scope

This note records ABI-121 after Run `run_20260831_041559_43da35` completed.

Source Runs:

- ABI-121 ASPP/detail decoder focal-Tversky centerline-auxiliary follow-up: `run_20260831_041559_43da35`
- ABI-120 ASPP/detail decoder BCE-Dice-clDice centerline-auxiliary scout: `run_20260831_033037_bad0bb`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-105 recent high-recall frequency-gated conservative-skip reference: `run_20260830_091941_139456`

ABI-121 was a family-development continuation of ABI-120. It kept the compact full-spectral BTD ASPP/detail decoder geometry, provider-approved `abi_16ch` input mode, combined source-balanced sampling, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and low-weight provider-derived Centerline Target auxiliary supervision at weight 0.02. The controlled change from ABI-120 was the trusted primary loss: `bce_dice_cldice` was replaced by trusted `focal_tversky`. This is capped representative evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-121 stayed inside the Candidate Experiment Contract. Candidate code owned only the model architecture over provider-approved ABI Channel Input and deterministic BTD combinations derived from GOES ABI channels 1-16. It did not introduce longitude, latitude, reconstructed coordinates, candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or lifecycle behavior.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: focal_tversky`, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and one provider-derived Centerline Target auxiliary output `centerline_logits` with trusted `weighted_bce` weight 0.02. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records.

`outputs/model_summary.json` reported 9,619,514 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,168.2 seconds total wall time, 972.9 seconds training wall time, 1,193.4 seconds validation wall time, 5,899,635,712 bytes peak CUDA allocated, 6,450,839,552 bytes peak CUDA reserved, and no terminal execution failure. The selected best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, centerline aux | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260830_091941_139456` | ABI-105 | frequency-gated line U-Net conservative-skip, focal-Tversky, centerline aux | 12 | 0.3831 | 0.3820 | 0.3857 | 0.3344 | 0.4484 | 0.2520 | 0.00486 |
| `run_20260831_033037_bad0bb` | ABI-120 | ASPP/detail decoder, `bce_dice_cldice`, centerline aux | 10 | 0.3667 | 0.3485 | 0.4078 | 0.4366 | 0.3161 | 0.3681 | 0.00262 |
| `run_20260831_041559_43da35` | ABI-121 | ASPP/detail decoder, focal-Tversky, centerline aux | 12 | 0.3884 | 0.3835 | 0.4005 | 0.3526 | 0.4323 | 0.2315 | 0.00444 |

ABI-121 improved the controlled ASPP/detail family comparison against ABI-120 on aggregate filtered Dice from 0.3667 to 0.3884 (+0.0217), MIT filtered Dice from 0.3485 to 0.3835 (+0.0350), and filtered recall from 0.3161 to 0.4323 (+0.1162). It also selected the final epoch, whereas ABI-120 peaked at epoch 10. The cost was lower precision (0.3526 vs 0.4366), lower connectivity (0.2315 vs 0.3681), higher filtered predicted-positive fraction (0.00444 vs 0.00262), and a small Google filtered-Dice decrease (0.4005 vs 0.4078). This is the expected focal-Tversky trade-off: stronger recall and MIT recovery at the expense of precision/connectivity discipline.

Relative to the mature ABI-068 aggregate-Dice reference, ABI-121 is close but not better: aggregate filtered Dice is lower by 0.0079, MIT by 0.0051, Google by 0.0156, precision by 0.0465, and connectivity by 0.1585. ABI-121 does improve filtered recall over ABI-068 by 0.0387, but with a higher filtered predicted-positive fraction. Relative to ABI-066, ABI-121 improves aggregate filtered Dice by 0.0059, MIT by 0.0197, and recall by 0.0956, but remains below ABI-066 on Google filtered Dice, precision, connectivity, and positive-area discipline. Relative to ABI-105, ABI-121 has higher aggregate Dice and source balance with lower predicted-positive fraction, but lower recall and slightly weaker connectivity.

## ABI-121 trajectory

ABI-121 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.1619, 0.2549, 0.2451, 0.2296, 0.3315, 0.2814, 0.3486, 0.3634, 0.3481, 0.3581, 0.3443, and 0.3884. The selected checkpoint was the final epoch 12. The trajectory was noisy but continued to recover after mid-run drops rather than plateauing into a clear dead branch.

At the selected checkpoint, raw Dice was 0.4007 and filtered Dice was 0.3884. Filtered precision was 0.3526, filtered recall 0.4323, filtered connectivity 0.2315, and filtered predicted-positive fraction 0.00444. Source-stratified filtered Dice was balanced: 0.3835 MIT and 0.4005 Google. Google retained high recall at 0.5079 with precision 0.3306; MIT reached recall 0.4065 with precision 0.3630. Both Dataset Sources were finite and non-collapsed.

Raw-to-filtered differences were modest: raw Dice 0.4007 versus filtered Dice 0.3884, and raw predicted-positive fraction 0.00474 versus filtered 0.00444. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples in `outputs/prediction_samples/samples.json` all had near-zero per-sample Dice, but the retention policy is fixed `first_n`, so these bounded artifacts should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-121 as finite, resource-feasible, non-collapsed, and strongly positive capped family-development evidence for the ASPP/detail decoder family. The focal-Tversky continuation converted ABI-120 from a precision-forward scout into a source-balanced high-recall contender. It also establishes the ASPP/detail family as the strongest non-frequency-gated architecture branch observed in the current capped leaderboard, ranking second by capped `val/filtered_dice` behind ABI-068 at the time of this note.

The result is not a promotion claim. All reported metrics are from the trusted capped representative 1,024-record-per-Dataset-Source/split policy, while canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-121's capped aggregate filtered Dice slightly exceeds the canonical MCAST 2.1 full-validation filtered Dice number, but these are different evidence scopes and must not be compared as promotion evidence.

The main weakness is connectivity. ABI-121 recovered recall and MIT Dice, but its filtered connectivity is much lower than ABI-068 and ABI-066. That suggests the ASPP/detail focal-Tversky branch may be segmenting more contrail area while fragmenting or thickening thin-line structure. Whole-validation diagnostics would be useful after this note if the campaign needs failure buckets for a non-frequency-gated near-top capped architecture, but the current step records only the completed capped Run.

## Decision

Do not promote ABI-121 and do not reinterpret capped representative evidence as full-data evidence. Keep ABI-068 as the current local capped aggregate-Dice reference and ABI-066 as the precision/connectivity reference. Retain ABI-121 as the best ASPP/detail-family result and a strong next diagnostic or family-development target.

Recommended next hypothesis: request bounded whole-validation failure analysis for ABI-121 or continue the ASPP/detail branch with an in-contract connectivity-focused refinement that preserves its focal-Tversky recall and source balance while improving line continuity. A reasonable follow-up would keep `focal_tversky`, `abi_16ch`, BTD front-end features, centerline auxiliary weight 0.02, combined source-balanced sampling, random mirroring, batch size 4, and 12 epochs, while adding a minimal high-resolution line-continuity refinement inside the architecture. Do not repeat ABI-120 or ABI-121 unchanged.

## Artifact references

- `run_20260831_041559_43da35/outputs/best_metrics.json`
- `run_20260831_041559_43da35/outputs/final_metrics.json`
- `run_20260831_041559_43da35/outputs/metrics.jsonl`
- `run_20260831_041559_43da35/outputs/resource_profile.json`
- `run_20260831_041559_43da35/outputs/model_summary.json`
- `run_20260831_041559_43da35/outputs/prediction_samples/samples.json`
- `run_20260831_041559_43da35/resolved_manifest.yaml`
- `run_20260831_033037_bad0bb/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260830_091941_139456/outputs/best_metrics.json`
