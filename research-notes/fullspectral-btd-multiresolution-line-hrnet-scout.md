# Full-spectral BTD multi-resolution line-HRNet scout

research-figures: []

## Scope

This note records ABI-084 after Run `run_20260829_171549_19184b` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-081 no-auxiliary focal-Tversky continuation: `run_20260829_143707_7c7d44`
- ABI-082 thermal-only frequency-gated line U-Net follow-up: `run_20260829_152950_e53671`
- ABI-083 strip-pooling/ribbon-context line U-Net scout: `run_20260829_162522_e7efac`
- ABI-084 multi-resolution line-HRNet scout: `run_20260829_171549_19184b`

ABI-084 used provider-approved `abi_16ch` input, ABI-channel-derived thermal BTD features, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, trusted `focal_tversky` primary loss, and a provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. The controlled family-scout change was architectural: keep a high-resolution branch active while repeatedly fusing medium/low-resolution cloud context in a compact HRNet-style model. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped scout evidence rather than full-data promotion evidence.

## ABI-084 implementation and resource observation

ABI-084 stayed inside the Candidate Experiment Contract. Candidate code owned only the model architecture over provider-approved ABI tensors. It did not introduce candidate-owned data loading, sampling, augmentation, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, or pretrained weights, and it did not request or reconstruct longitude/latitude inputs.

Model summary reported 5,429,778 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 2,959.6 seconds wall time, 14,214,496,256 bytes peak CUDA reserved, and no terminal execution failure. The architecture is therefore resource-feasible under the current cap, though slower and more memory-heavy than several frequency-gated references despite the lower parameter count.

## Best-validation comparison

| Run | Candidate | Primary architecture/input/loss | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_230540_bf4ce3` | ABI-066 | full-spectral frequency-gated line U-Net, `bce_dice_cldice`, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_010836_4ccc77` | ABI-068 | full-spectral frequency-gated line U-Net, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260829_143707_7c7d44` | ABI-081 | ABI-068 architecture, no auxiliary head, `focal_tversky` | 9 | 0.3809 | 0.3624 | 0.4279 | 0.3797 | 0.3822 | 0.3893 | 0.00365 |
| `run_20260829_152950_e53671` | ABI-082 | thermal-only BTD frequency-gated line U-Net, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3698 | 0.3708 | 0.3678 | 0.3154 | 0.4469 | 0.2031 | 0.00513 |
| `run_20260829_162522_e7efac` | ABI-083 | full-spectral BTD strip-pooling/ribbon-context line U-Net, `focal_tversky`, centerline aux weight 0.02 | 10 | 0.3146 | 0.2934 | 0.3614 | 0.3268 | 0.3033 | 0.2095 | 0.00336 |
| `run_20260829_171549_19184b` | ABI-084 | full-spectral BTD multi-resolution line-HRNet, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3188 | 0.3327 | 0.2905 | 0.2427 | 0.4643 | 0.1448 | 0.00693 |

ABI-084 completed finite and non-degenerate, but it did not meet the proposal's useful-scout criteria. Aggregate filtered Dice was 0.3188, about -0.0776 below ABI-068 and -0.0637 below ABI-066. MIT filtered Dice reached 0.3327, barely above the proposal's approximate 0.33 source floor, but Google filtered Dice was only 0.2905, below the source floor and far below ABI-066/068/081.

The intended precision/connectivity advantage did not appear. ABI-084 had the highest recall in this local comparison, 0.4643, but this came with the lowest precision, 0.2427, the lowest connectivity, 0.1448, and the largest filtered predicted-positive fraction, 0.00693. Relative to ABI-083, the multi-resolution branch improved aggregate and MIT Dice slightly and recovered recall, but lost Google Dice, precision, connectivity, and positive-area discipline.

## ABI-084 trajectory

ABI-084 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.1085, 0.1326, 0.1726, 0.2319, 0.2330, 0.1634, 0.1801, 0.2676, 0.2975, 0.2026, 0.2719, and 0.3188. The selected checkpoint was the final epoch 12 after a non-monotonic trajectory.

The final checkpoint was recall-heavy rather than cleanly line-preserving: filtered precision 0.2427, filtered recall 0.4643, filtered connectivity 0.1448, and filtered predicted-positive fraction 0.00693. Source behavior was imbalanced in the opposite direction from ABI-083, with MIT filtered Dice 0.3327 and Google filtered Dice 0.2905. The fixed first-four retained prediction samples all had near-zero sample Dice; because prediction retention is fixed `first_n`, these retained samples are bounded artifacts rather than representative qualitative evidence.

## Interpretation

Classify ABI-084 as a negative but informative capped family scout, with scientific outcome `bad_research_result` rather than execution failure. It establishes that this compact multi-resolution line-HRNet implementation is contract-compliant and resource-feasible, but the capped Result underperformed the frequency-gated references on aggregate filtered Dice, Google source behavior, precision, connectivity, and predicted-positive burden.

This first scout does not eliminate all multi-resolution or HRNet-style approaches. It does argue against repeating this exact high-resolution/medium/low-resolution fusion design unchanged under the current capped budget. The evidence suggests that the implemented fusion stages increased recall and positive area without learning enough discriminative line continuity or cloud/background suppression.

Canonical MCAST 2.1 remains the promotion context, and all comparisons here are capped representative family-development evidence rather than full-data promotion claims.

## Decision

Do not promote ABI-084. Do not repeat the exact full-spectral BTD multi-resolution line-HRNet branch unchanged. Prefer broadening to a different thin-line architecture or a trusted training/calibration/data-policy axis that can address precision, connectivity, and Google-source behavior without moving thresholding, losses, Artifact Filters, postprocessing, data loading, sampling, augmentation, target derivation, metrics, resource placement, or lifecycle behavior into Candidate code.

## Artifact references

- `run_20260829_171549_19184b/outputs/best_metrics.json`
- `run_20260829_171549_19184b/outputs/final_metrics.json`
- `run_20260829_171549_19184b/outputs/metrics.jsonl`
- `run_20260829_171549_19184b/outputs/resource_profile.json`
- `run_20260829_171549_19184b/outputs/model_summary.json`
- `run_20260829_171549_19184b/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260829_143707_7c7d44/outputs/best_metrics.json`
- `run_20260829_152950_e53671/outputs/best_metrics.json`
- `run_20260829_162522_e7efac/outputs/best_metrics.json`
