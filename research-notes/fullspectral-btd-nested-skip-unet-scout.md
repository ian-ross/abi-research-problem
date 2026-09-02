# Full-spectral BTD nested-skip U-Net scout

research-figures: []

## Scope

This note records ABI-079 after Run `run_20260828_104353_1455f1` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice and whole-validation reference: `run_20260828_010836_4ccc77`
- ABI-078 frequency-gated line U-Net BCE-Dice loss-swap reference: `run_20260828_094949_ad2af0`
- ABI-079 nested-skip U-Net scout: `run_20260828_104353_1455f1`

ABI-079 used provider-approved `abi_16ch` input, ABI-channel-derived thermal BTD features, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, trusted `focal_tversky` primary loss, and the provider-derived `centerline` auxiliary target with trusted `weighted_bce` at weight 0.02. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-scout evidence rather than full-data promotion evidence.

## ABI-079 implementation and resource observation

ABI-079 broadened away from the ABI-068 frequency-gated late-refiner branch by using a compact UNet++-style nested decoder. The hypothesis was that repeated multi-depth fusion could preserve high-resolution thin-line evidence while letting deeper cloud-context features suppress false positives before the final mask head.

The Run stayed inside the Candidate Experiment Contract: no longitude/latitude inputs, no reconstructed coordinate inputs, no candidate-owned data loading, no custom loss or target derivation, no candidate-owned augmentation, no metrics, no thresholding, no Artifact Filters, no postprocessing, no network access, and no pretrained weights. The trusted model summary recorded `abi_16ch` input shape `[16, 256, 256]`, forbidden source channel indices 16 and 17 excluded, primary `mask_logits`, and one `centerline_logits` auxiliary output.

Model summary reported 6,629,139 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on an A100 with 1,690.8 seconds wall time, 6,413,090,816 bytes peak CUDA reserved, and no terminal execution failure. Resource behavior is therefore feasible for the current capped sequential policy.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260828_094949_ad2af0` | ABI-078 | ABI-068 architecture with `bce_dice` primary loss | 11 | 0.3816 | 0.3704 | 0.4093 | 0.4072 | 0.3590 | 0.3061 | 0.00320 |
| `run_20260828_104353_1455f1` | ABI-079 | compact nested-skip U-Net, `focal_tversky`, centerline aux weight 0.02 | 9 | 0.2984 | 0.3153 | 0.2650 | 0.2284 | 0.4300 | 0.1265 | 0.00682 |

ABI-079 did not meet the scout success criteria. Relative to ABI-068, aggregate filtered Dice fell by about -0.0980, MIT filtered Dice by -0.0733, Google filtered Dice by -0.1511, filtered precision by -0.1707, and filtered connectivity by -0.2635. Filtered recall improved by about +0.0364, but it came with a much larger predicted-positive fraction: 0.00682 versus ABI-068's 0.00357.

Relative to ABI-066, ABI-079 was lower on aggregate filtered Dice by about -0.0842, lower on Google filtered Dice by about -0.1641, lower on precision by about -0.2143, lower on connectivity by about -0.3466, and more permissive in predicted-positive fraction. Relative to ABI-078, ABI-079 also lost aggregate Dice, both source Dice values, precision, and connectivity despite higher recall.

## ABI-079 trajectory

ABI-079 trained finitely and avoided all-negative/all-positive collapse, but it settled into a permissive low-precision operating point. Filtered Dice by epoch was 0.1094, 0.1197, 0.1595, 0.1992, 0.2245, 0.2509, 0.2017, 0.2234, 0.2984, 0.2542, 0.2818, and 0.2870. The selected checkpoint was epoch 9; epochs 10-12 partially recovered from the epoch-10 drop but did not surpass the epoch-9 best.

At the best checkpoint, both Dataset Sources were nonzero but weak: MIT filtered Dice was 0.3153 and Google filtered Dice was 0.2650. The source split is notable because Google, which has often been stronger in the frequency-gated branch, became the weaker source here. The operating point was recall-forward rather than cleaner: filtered recall was 0.4300, filtered precision was 0.2284, filtered connectivity was 0.1265, and filtered predicted-positive fraction was 0.00682.

The final epoch remained below the selected checkpoint on the primary metric: aggregate filtered Dice 0.2870, MIT 0.3060, Google 0.2506, precision 0.2333, recall 0.3729, connectivity 0.1209, and predicted-positive fraction 0.00579. The fixed first-four retained prediction samples all had near-zero sample Dice; because the policy is `first_n`, these samples are useful only as bounded retained artifacts, not representative qualitative evidence.

## Interpretation

Classify ABI-079 as a negative capped family scout, not as a promotion candidate. The nested-skip architecture was resource-feasible and numerically stable, but it did not deliver the intended precision/connectivity recovery or reduced clutter. Its best checkpoint stayed below 0.30 aggregate filtered Dice, was much more permissive than ABI-068, and had materially weaker Google-source behavior.

This does not prove that all nested-skip designs are exhausted: it is one compact scout under capped representative evidence. However, the exact ABI-079 branch has enough negative evidence to avoid repeating it unchanged. Any nested-skip continuation would need a specific corrective hypothesis for precision/connectivity and Google-source degradation, rather than simply adding more dense decoder fusion. ABI-068 remains the strongest local whole-validation-tested aggregate-Dice reference, and ABI-066 remains the precision/connectivity-forward reference. Canonical MCAST 2.1 remains promotion context; this capped Run should not be interpreted as full-data promotion evidence.

## Decision

Do not promote ABI-079. Do not repeat the exact compact nested-skip U-Net scout unchanged. Prefer broadening to a different architecture family or a targeted follow-up that directly addresses ABI-079's permissive positive-area profile and weak connectivity without moving thresholding, losses, Artifact Filters, postprocessing, data loading, sampling, augmentation, target derivation, metrics, resource placement, or lifecycle behavior into Candidate code.

## Artifact references

- `run_20260828_104353_1455f1/outputs/best_metrics.json`
- `run_20260828_104353_1455f1/outputs/final_metrics.json`
- `run_20260828_104353_1455f1/outputs/metrics.jsonl`
- `run_20260828_104353_1455f1/outputs/resource_profile.json`
- `run_20260828_104353_1455f1/outputs/model_summary.json`
- `run_20260828_104353_1455f1/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260828_094949_ad2af0/outputs/best_metrics.json`
