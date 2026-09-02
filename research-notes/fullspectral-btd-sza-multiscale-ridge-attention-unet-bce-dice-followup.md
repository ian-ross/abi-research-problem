# Full-spectral BTD+SZA multiscale ridge-attention U-Net BCE-Dice follow-up

research-figures: []

## Scope

This note records ABI-142 after Run `run_20260831_215104_d4c318` completed.

Source Runs:

- ABI-142 full-spectral BTD+SZA multiscale ridge-attention U-Net BCE-Dice Centerline-auxiliary scout: `run_20260831_215104_d4c318`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice Centerline-auxiliary reference: `run_20260831_121006_7d24be`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice Centerline-auxiliary high-precision/connectivity comparator: `run_20260831_085615_d05ab3`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice high-connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-132 SZA-aware ASPP/detail region-line agreement comparator: `run_20260831_135752_1ac18c`
- ABI-141 SZA-aware ASPP/detail boundary-calibrated comparator: `run_20260831_210158_e9ce5e`

ABI-142 was a family scout that broadened away from incremental ASPP/detail decoder head changes. It kept provider-approved `abi_16ch_plus_sza` input, deterministic thermal brightness-temperature-difference and SZA-derived features from approved channels only, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.

## Contract and resource observation

ABI-142 stayed inside the Candidate Experiment Contract. Candidate code owned only the PyTorch architecture over provider-approved GOES ABI channels 1-16 plus Solar Geometry Input. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 9,617,130 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,796.6 seconds total wall time, 1,463.6 seconds training wall time, 1,331.0 seconds validation wall time, 6,675,088,896 bytes peak CUDA allocated, 7,327,449,088 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_215104_d4c318` | ABI-142 | multiscale ridge-attention U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3935 | 0.3762 | 0.4373 | 0.4398 | 0.3561 | 0.3819 | 0.00293 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260831_135752_1ac18c` | ABI-132 | ASPP/detail decoder, BCE-Dice, region-line agreement, ABI-16+BTD+SZA | 12 | 0.3853 | 0.3730 | 0.4163 | 0.4394 | 0.3431 | 0.2971 | 0.00283 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, ABI-16+BTD | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260831_210158_e9ce5e` | ABI-141 | ASPP/detail decoder, boundary-calibrated BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3815 | 0.3643 | 0.4245 | 0.4412 | 0.3360 | 0.3498 | 0.00276 |

ABI-142 did not beat the current capped best ABI-068 or the strongest SZA-aware ASPP/detail branch ABI-130, but it landed very close to both. Against ABI-130, aggregate filtered Dice was lower by only 0.0017, MIT filtered Dice by 0.0017, Google filtered Dice by 0.0031, filtered precision by 0.0017, filtered recall by 0.0017, and filtered connectivity by 0.0032, with effectively the same predicted-positive fraction. Against ABI-068, ABI-142 was lower by 0.0028 aggregate filtered Dice, lower by 0.0124 MIT filtered Dice, but higher by 0.0212 Google filtered Dice and higher by 0.0406 precision, while recall and connectivity were modestly lower.

The ridge-attention scout improved recent SZA-aware ASPP/detail local tweaks. It exceeded ABI-141 by +0.0121 aggregate filtered Dice, +0.0119 MIT filtered Dice, +0.0128 Google filtered Dice, +0.0201 recall, and +0.0321 connectivity. It exceeded ABI-132 by +0.0082 aggregate filtered Dice, +0.0032 MIT filtered Dice, +0.0210 Google filtered Dice, +0.0130 recall, and +0.0848 connectivity. This suggests the ridge-aware architecture changed the feature path usefully, even though it did not create a new leading operating point.

## ABI-142 trajectory

ABI-142 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.2374, 0.2738, 0.3231, 0.3473, 0.3360, 0.3217, 0.3319, 0.3664, 0.3690, 0.3398, 0.3711, and 0.3935. The final epoch was the selected best checkpoint, and the late improvement from epochs 8-12 argues against an optimization hard stop at the active budget.

The best checkpoint showed source-stratified filtered Dice of 0.3762 for MIT and 0.4373 for Google. MIT had filtered precision 0.4425, recall 0.3272, connectivity 0.3694, and predicted-positive fraction 0.00399. Google had filtered precision 0.4340, recall 0.4407, connectivity 0.3944, and predicted-positive fraction 0.00188. Both Dataset Sources were finite and non-collapsed. The source profile is close to ABI-130: strong Google behavior, disciplined positive area, and moderate MIT recall.

Raw-to-filtered differences were modest at the best checkpoint: raw Dice was 0.4079 versus filtered Dice 0.3935, and raw predicted-positive fraction was 0.00313 versus filtered 0.00293. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples contain one empty-background perfect Dice case and three near-zero Dice cases under the `first_n` retention policy; these bounded artifacts are traceability artifacts and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-142 as a completed, finite, non-collapsed, positive-but-not-leading family scout. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch. The scout answered its main feasibility question positively: moving line/ridge evidence into the encoder stem and final feature refinement can reach the current capped reference band under the SZA+BCE-Dice calibration axis.

The result does not prove that the ridge-attention family is superior to the mature frequency-gated line U-Net or SZA-aware ASPP/detail families. Its metrics are nearly isomorphic to ABI-130, with no decisive connectivity, source-balance, or predicted-positive advantage. However, because this is a first materially different ridge-attention family scout and it finished within 0.003 aggregate filtered Dice of both ABI-068 and ABI-130, low comparative margin is not elimination evidence. The family merits at most one bounded continuation if the continuation tests a controlled mechanism rather than repeating the architecture unchanged.

## Decision

Do not promote ABI-142 from representative capped evidence and do not request whole-validation diagnostics yet. It did not beat ABI-068/ABI-130 and did not establish a distinctive high-connectivity or source-balance advantage that would justify spending whole-validation evaluation budget immediately.

Do not abandon the ridge-attention family after this scout. A future Autonomy Step may prepare one bounded family-development continuation that keeps the in-contract SZA+BCE-Dice setup but tests a specific calibration axis, such as reducing ridge-gate aggressiveness, adding deterministic-shuffle traversal, or comparing a lower-parameter ridge stem against ABI-142. The continuation should preserve provider ownership of data loading, target derivation, losses, metrics, sampling, augmentation, thresholding, Artifact Filters, postprocessing, resources, and lifecycle.

No new Capability Request, Evaluation Request, or Campaign Report is required from this result.

## Artifact references

- `run_20260831_215104_d4c318/outputs/best_metrics.json`
- `run_20260831_215104_d4c318/outputs/final_metrics.json`
- `run_20260831_215104_d4c318/outputs/metrics.jsonl`
- `run_20260831_215104_d4c318/outputs/resource_profile.json`
- `run_20260831_215104_d4c318/outputs/model_summary.json`
- `run_20260831_215104_d4c318/outputs/prediction_samples/samples.json`
- `run_20260831_215104_d4c318/resolved_manifest.yaml`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260831_135752_1ac18c/outputs/best_metrics.json`
- `run_20260831_210158_e9ce5e/outputs/best_metrics.json`
