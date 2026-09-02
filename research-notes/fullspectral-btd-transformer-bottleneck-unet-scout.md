# Full-spectral BTD transformer-bottleneck U-Net scout

research-figures: []

## Scope

This note records ABI-086 after Run `run_20260829_190432_3d626f` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-081 no-auxiliary focal-Tversky continuation: `run_20260829_143707_7c7d44`
- ABI-083 strip-pooling/ribbon-context line U-Net scout: `run_20260829_162522_e7efac`
- ABI-084 multi-resolution line-HRNet scout: `run_20260829_171549_19184b`
- ABI-085 low-learning-rate ABI-068 continuation: `run_20260829_181201_01c5e7`
- ABI-086 transformer-bottleneck U-Net scout: `run_20260829_190432_3d626f`

ABI-086 used provider-approved `abi_16ch` input only, ABI-channel-derived thermal brightness-temperature-difference features, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, trusted `focal_tversky` primary loss, and a provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. The controlled scout change was architectural: insert compact global self-attention at the 1/16-resolution bottleneck before U-Net decoding. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped scout evidence rather than full-data promotion evidence.

## ABI-086 implementation and resource observation

ABI-086 stayed inside the Candidate Experiment Contract. Candidate code owned only the model architecture over provider-approved ABI tensors. It did not introduce candidate-owned data loading, sampling, augmentation, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, or pretrained weights, and it did not request or reconstruct longitude/latitude inputs.

Model summary reported 12,972,714 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 1,594.7 seconds wall time, 3,969,908,736 bytes peak CUDA reserved, and no terminal execution failure. The transformer-bottleneck implementation is therefore resource-feasible under the current representative cap and substantially lighter at runtime than the recent multi-resolution line-HRNet scout.

## Best-validation comparison

| Run | Candidate | Primary architecture/input/loss | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_230540_bf4ce3` | ABI-066 | full-spectral frequency-gated line U-Net, `bce_dice_cldice`, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_010836_4ccc77` | ABI-068 | full-spectral frequency-gated line U-Net, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260829_143707_7c7d44` | ABI-081 | ABI-068 architecture, no auxiliary head, `focal_tversky` | 9 | 0.3809 | 0.3624 | 0.4279 | 0.3797 | 0.3822 | 0.3893 | 0.00365 |
| `run_20260829_162522_e7efac` | ABI-083 | full-spectral BTD strip-pooling/ribbon-context line U-Net, `focal_tversky`, centerline aux weight 0.02 | 10 | 0.3146 | 0.2934 | 0.3614 | 0.3268 | 0.3033 | 0.2095 | 0.00336 |
| `run_20260829_171549_19184b` | ABI-084 | full-spectral BTD multi-resolution line-HRNet, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3188 | 0.3327 | 0.2905 | 0.2427 | 0.4643 | 0.1448 | 0.00693 |
| `run_20260829_181201_01c5e7` | ABI-085 | ABI-068 architecture, lower learning rate 0.0001, `focal_tversky` | 12 | 0.3826 | 0.3733 | 0.4059 | 0.3693 | 0.3968 | 0.3698 | 0.00398 |
| `run_20260829_190432_3d626f` | ABI-086 | full-spectral BTD transformer-bottleneck U-Net, `focal_tversky`, centerline aux weight 0.02 | 5 | 0.3113 | 0.3057 | 0.3257 | 0.3405 | 0.2868 | 0.2080 | 0.00305 |

ABI-086 completed finite and non-degenerate, but it did not meet the proposal's useful-scout criteria. Best aggregate filtered Dice was 0.3113, about -0.0850 below ABI-068 and -0.0712 below ABI-066/085. Both source-specific Dice values were below the approximate 0.33 scout floor: MIT 0.3057 and Google 0.3257. This source behavior is not catastrophic collapse, but it is weaker than the frequency-gated references and not a convincing continuation signal for this exact branch.

The intended precision/connectivity benefit also did not appear. ABI-086's best filtered precision was 0.3405, recall 0.2868, connectivity 0.2080, and filtered predicted-positive fraction 0.00305. Compared with ABI-068, it reduced predicted-positive burden slightly but lost Dice, precision, recall, and connectivity. Compared with ABI-083/084, it showed a more balanced source split than either of those scouts, but not enough aggregate or secondary-metric strength to justify repeating the same bottleneck-attention design unchanged.

## ABI-086 trajectory

The selected checkpoint was epoch 5. Final epoch 12 degraded to aggregate filtered Dice 0.3024, precision 0.2298, recall 0.4420, connectivity 0.1191, and filtered predicted-positive fraction 0.00697. Source metrics at the final checkpoint were MIT filtered Dice 0.3062 and Google filtered Dice 0.2939. The late-epoch movement therefore shifted toward larger positive area and higher recall but lower precision/connectivity rather than improving the proposed global-context false-positive suppression behavior.

The retained fixed first-four prediction samples all had near-zero sample Dice in `outputs/prediction_samples/samples.json`. Because prediction retention is fixed `first_n`, these are bounded artifacts and not representative qualitative evidence, but they are consistent with the Run not producing a compelling checkpoint-level scout result.

## Interpretation

Classify ABI-086 as a negative but informative capped family scout, with scientific outcome `bad_research_result` rather than execution failure. It establishes that a compact transformer-bottleneck U-Net over full-spectral BTD features is contract-compliant and resource-feasible, but the capped Result underperformed the frequency-gated references on aggregate filtered Dice, both Dataset Sources, precision, recall, and connectivity.

This first scout does not eliminate all attention or transformer-style approaches. It does argue against repeating this exact low-resolution global self-attention bottleneck unchanged under the current capped budget. The evidence suggests that attention only at the coarsest bottleneck did not add enough line-preserving or false-positive-suppressing signal, and later epochs became recall-heavy without preserving connectivity.

Canonical MCAST 2.1 remains the promotion context, and all comparisons here are capped representative family-development evidence rather than full-data promotion claims.

## Decision

Do not promote ABI-086. Do not repeat the exact full-spectral BTD transformer-bottleneck U-Net branch unchanged. Prefer broadening away from another single bottleneck-context insertion toward either a materially different architecture family or a trusted training/calibration/data-policy axis that can address precision, connectivity, and Dataset Source balance without moving thresholding, losses, Artifact Filters, postprocessing, data loading, sampling, augmentation, target derivation, metrics, resource placement, or lifecycle behavior into Candidate code.

## Artifact references

- `run_20260829_190432_3d626f/outputs/best_metrics.json`
- `run_20260829_190432_3d626f/outputs/final_metrics.json`
- `run_20260829_190432_3d626f/outputs/metrics.jsonl`
- `run_20260829_190432_3d626f/outputs/resource_profile.json`
- `run_20260829_190432_3d626f/outputs/model_summary.json`
- `run_20260829_190432_3d626f/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260829_143707_7c7d44/outputs/best_metrics.json`
- `run_20260829_162522_e7efac/outputs/best_metrics.json`
- `run_20260829_171549_19184b/outputs/best_metrics.json`
- `run_20260829_181201_01c5e7/outputs/best_metrics.json`
