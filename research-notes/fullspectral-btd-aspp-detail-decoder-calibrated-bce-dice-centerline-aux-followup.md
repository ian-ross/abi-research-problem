# Full-spectral BTD ASPP/detail decoder calibrated BCE-Dice centerline-auxiliary follow-up

research-figures: []

## Scope

This note records ABI-128 after Run `run_20260831_103509_961c81` completed.

Source Runs:

- ABI-128 ASPP/detail decoder calibrated BCE-Dice centerline-auxiliary follow-up: `run_20260831_103509_961c81`
- ABI-126 ASPP/detail decoder BCE-Dice centerline-auxiliary comparison target: `run_20260831_085615_d05ab3`
- ABI-127 ASPP/detail decoder BCE-Dice Line+Centerline auxiliary comparison: `run_20260831_094013_5ba974`
- ABI-121 ASPP/detail decoder focal-Tversky centerline-auxiliary recall/source-balance comparator: `run_20260831_041559_43da35`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`

ABI-128 was a controlled family-development continuation of ABI-126. It kept the compact full-spectral BTD ASPP/detail decoder, provider-approved `abi_16ch` input mode, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, trusted `bce_dice` primary loss, and provider-derived Centerline Target auxiliary supervision at weight 0.02. The controlled change was replacing ABI-126's single mask-logit projection with a calibration-aware foreground-minus-background margin head. This is capped representative evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-128 stayed inside the Candidate Experiment Contract. Candidate code owned only the PyTorch architecture over approved ABI Channel Input and deterministic brightness-temperature-difference planes derived from GOES ABI channels 1-16. It did not introduce longitude, latitude, reconstructed coordinates, Solar Geometry Input, candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or lifecycle behavior.

`resolved_manifest.yaml` records `input_mode: abi_16ch`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: bce_dice`, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and provider-derived Centerline Target auxiliary output `centerline_logits` with trusted `weighted_bce` weight 0.02. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records.

`outputs/model_summary.json` reported 9,668,079 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,387.8 seconds total wall time, 1,105.4 seconds training wall time, 1,280.3 seconds validation wall time, 6,537,558,016 bytes peak CUDA allocated, 7,163,871,232 bytes peak CUDA reserved, and no terminal execution failure. The selected best-validation checkpoint was epoch 9.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, centerline aux | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, centerline aux | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260831_041559_43da35` | ABI-121 | ASPP/detail decoder, focal-Tversky, centerline aux | 12 | 0.3884 | 0.3835 | 0.4005 | 0.3526 | 0.4323 | 0.2315 | 0.00444 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, centerline aux | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260831_094013_5ba974` | ABI-127 | ABI-126 plus Line Target auxiliary head | 9 | 0.3797 | 0.3653 | 0.4150 | 0.4280 | 0.3412 | 0.3054 | 0.00289 |
| `run_20260831_103509_961c81` | ABI-128 | ABI-126 plus calibrated margin mask head | 9 | 0.3787 | 0.3586 | 0.4298 | 0.4120 | 0.3504 | 0.3473 | 0.00308 |

ABI-128 partially met the calibration-head hypothesis but not enough to improve the branch. Relative to ABI-126, it increased filtered recall from 0.3251 to 0.3504 (+0.0253) at the selected checkpoint and kept filtered predicted-positive fraction closer to ABI-126 than to ABI-121. However, aggregate filtered Dice decreased from 0.3859 to 0.3787 (-0.0072), MIT filtered Dice decreased from 0.3635 to 0.3586 (-0.0049), Google filtered Dice decreased from 0.4415 to 0.4298 (-0.0117), filtered precision decreased from 0.4746 to 0.4120 (-0.0627), and filtered connectivity decreased from 0.4517 to 0.3473 (-0.1044). The recovered recall therefore came with a meaningful loss of ABI-126's best precision/connectivity strengths and did not recover the intended MIT weakness.

Relative to ABI-127, ABI-128 is approximately tied on aggregate filtered Dice but has a different trade-off. ABI-128 improves recall (0.3504 vs 0.3412), Google filtered Dice (0.4298 vs 0.4150), and connectivity (0.3473 vs 0.3054), but is lower on MIT filtered Dice (0.3586 vs 0.3653) and precision (0.4120 vs 0.4280). The calibrated head is therefore more useful than the simple Line+Centerline auxiliary addition for Google and connectivity, but it still does not solve the ASPP/detail BCE-Dice branch's MIT under-recall/source-balance problem.

Relative to ABI-121, ABI-128 remains more disciplined than the focal-Tversky ASPP/detail operating point, with higher precision (0.4120 vs 0.3526), higher connectivity (0.3473 vs 0.2315), and lower predicted-positive fraction (0.00308 vs 0.00444). It remains worse on aggregate filtered Dice, MIT filtered Dice, and recall. Relative to ABI-068, ABI-128 is below the capped aggregate reference on filtered Dice, MIT Dice, precision, recall, and connectivity, though it has higher Google filtered Dice. Relative to ABI-066, ABI-128 has slightly lower aggregate filtered Dice, MIT filtered Dice, precision, and connectivity, with higher recall and slightly higher Google filtered Dice.

## ABI-128 trajectory

ABI-128 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.1952, 0.2637, 0.2897, 0.3196, 0.3272, 0.3323, 0.3470, 0.3577, 0.3787, 0.3386, 0.3475, and 0.3738. The selected checkpoint was epoch 9, followed by a sharp epoch-10 drop and partial recovery by epoch 12. The trajectory is finite and generally constructive through epoch 9, but the final three epochs show calibration instability rather than a clean late-improving branch.

At the selected checkpoint, raw Dice was 0.3917 and filtered Dice was 0.3787. Filtered precision was 0.4120, filtered recall 0.3504, filtered connectivity 0.3473, and filtered predicted-positive fraction 0.00308. Source-stratified filtered Dice was 0.3586 for MIT and 0.4298 for Google. At final epoch 12, aggregate filtered Dice was 0.3738 with filtered precision 0.3858, recall 0.3626, connectivity 0.2719, MIT filtered Dice 0.3592, and Google filtered Dice 0.4093. Final recall rose further, but precision/connectivity weakened, reinforcing that the calibrated head mainly shifts the operating point toward recall rather than improving the Pareto frontier.

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice 0.3917 versus filtered Dice 0.3787, and raw predicted-positive fraction 0.00328 versus filtered 0.00308. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples are available for traceability, but the retention policy is fixed `first_n`, so these bounded artifacts should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-128 as finite, resource-feasible, non-collapsed, but negative-to-mixed capped family-development evidence for the specific calibrated-head hypothesis. The head did move ABI-126's fixed-threshold operating point toward higher recall, consistent with the ABI-126 threshold-sweep lesson that recall is recoverable by calibration. However, the gain did not target the intended MIT weakness and the cost in precision/connectivity was too large to justify this head as an improvement over ABI-126.

This result should not eliminate the ASPP/detail decoder family as a whole: ABI-121 remains the ASPP/detail recall/source-balance comparator, and ABI-126 remains the ASPP/detail precision/connectivity and Google-Dice comparator. It does weaken the case for continuing simple ASPP/detail mask-head or auxiliary-head tuning under BCE-Dice. ABI-120 through ABI-128 have now mapped clDice, focal-Tversky, BCE-Dice, directional-continuity refinement, Line+Centerline auxiliary, whole-validation ABI-126 diagnostics, and a calibration-aware margin head.

All metrics here are from the trusted capped representative 1,024-record-per-Dataset-Source/split policy. They are feasibility and family-development evidence only; they are not full-data promotion evidence and should not be compared to canonical MCAST Working Validation Split results as promotion-grade claims.

## Decision

Do not promote ABI-128. Do not repeat ABI-128 unchanged, and do not spend another Autonomy Step on another simple ASPP/detail BCE-Dice mask-head or auxiliary-head tweak unless a new diagnostic specifically identifies that mechanism as limiting.

Retain ABI-068 as the local capped aggregate-Dice reference, ABI-066 as the precision/connectivity reference, ABI-121 as the ASPP/detail recall/source-balance comparator, and ABI-126 as the ASPP/detail precision/connectivity and Google-Dice comparator. For the next in-contract step, prefer broadening away from ASPP/detail head tuning. Useful directions include a different architecture family or data/training-policy mechanism that targets the ABI-126/ABI-128 lesson directly: preserve positive-area discipline and connectivity while improving MIT recall at the fixed Harness threshold.

## Artifact references

- `run_20260831_103509_961c81/outputs/best_metrics.json`
- `run_20260831_103509_961c81/outputs/final_metrics.json`
- `run_20260831_103509_961c81/outputs/metrics.jsonl`
- `run_20260831_103509_961c81/outputs/resource_profile.json`
- `run_20260831_103509_961c81/outputs/model_summary.json`
- `run_20260831_103509_961c81/outputs/prediction_samples/samples.json`
- `run_20260831_103509_961c81/resolved_manifest.yaml`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/evaluations/eval_evalreq_abi126_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_094013_5ba974/outputs/best_metrics.json`
- `run_20260831_041559_43da35/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
