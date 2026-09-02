# Full-spectral BTD strip-pooling line U-Net scout

research-figures: []

## Scope

This note records ABI-083 after Run `run_20260829_162522_e7efac` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-080 frequency-gated line U-Net multi-scale logit-consensus follow-up: `run_20260829_133850_54dd6e`
- ABI-082 thermal-only frequency-gated line U-Net follow-up: `run_20260829_152950_e53671`
- ABI-083 strip-pooling/ribbon-context line U-Net scout: `run_20260829_162522_e7efac`

ABI-083 used provider-approved `abi_16ch` input, ABI-channel-derived thermal BTD features, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, trusted `focal_tversky` primary loss, and a provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. The controlled family-scout change was architectural: replace the ABI-068 frequency-gated local high/low-frequency branch with compact row/column strip-pooling context at bottleneck and high-resolution fusion stages. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped scout evidence rather than full-data promotion evidence.

## ABI-083 implementation and resource observation

ABI-083 kept the full-spectral raw-plus-BTD input idea while adding non-coordinate ribbon context over provider-approved ABI tensors. Candidate code owned only the model architecture. It did not introduce candidate-owned data loading, sampling, augmentation, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, or pretrained weights.

Model summary reported 20,809,074 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 2,484.7 seconds wall time, 9,938,403,328 bytes peak CUDA reserved, and no terminal execution failure. The architecture is therefore resource-feasible under the current cap, though it is substantially larger than ABI-066/068-style frequency-gated references.

## Best-validation comparison

| Run | Candidate | Primary architecture/input/loss | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_230540_bf4ce3` | ABI-066 | full-spectral frequency-gated line U-Net, `bce_dice_cldice`, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_010836_4ccc77` | ABI-068 | full-spectral frequency-gated line U-Net, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260829_133850_54dd6e` | ABI-080 | ABI-068 plus multi-scale logit-consensus head, `focal_tversky` | 10 | 0.3623 | 0.3490 | 0.3916 | 0.3698 | 0.3552 | 0.1795 | 0.00348 |
| `run_20260829_152950_e53671` | ABI-082 | thermal-only BTD frequency-gated line U-Net, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3698 | 0.3708 | 0.3678 | 0.3154 | 0.4469 | 0.2031 | 0.00513 |
| `run_20260829_162522_e7efac` | ABI-083 | full-spectral BTD strip-pooling/ribbon-context line U-Net, `focal_tversky`, centerline aux weight 0.02 | 10 | 0.3146 | 0.2934 | 0.3614 | 0.3268 | 0.3033 | 0.2095 | 0.00336 |

ABI-083 completed finite and non-degenerate, but it did not meet the proposal's useful-scout criteria. Aggregate filtered Dice was 0.3146, about -0.0818 below ABI-068 and -0.0477 below ABI-080. MIT filtered Dice was 0.2934, below the proposal's approximate 0.33 Dataset Source floor, while Google filtered Dice was 0.3614. The result is therefore source-imbalanced in the wrong direction for a continuation signal.

The hoped-for precision/connectivity recovery was also weak. ABI-083 had slightly higher connectivity than ABI-080 and ABI-082, but only to 0.2095, still far below ABI-068 at 0.3900 and ABI-066 at 0.4731. Precision was 0.3268, lower than ABI-068, ABI-066, and ABI-080, and only slightly above ABI-082's recall-heavy thermal-only point. This does not support the hypothesis that row/column strip context recovered disciplined line evidence.

## ABI-083 trajectory

ABI-083 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.0718, 0.1000, 0.1546, 0.1808, 0.2510, 0.2263, 0.2483, 0.2720, 0.2948, 0.3146, 0.3004, and 0.2990. The selected checkpoint was epoch 10, after which filtered Dice and connectivity did not recover by epoch 12.

The best epoch's operating point was not an obvious thresholding or single-metric artifact: filtered precision was 0.3268, filtered recall was 0.3033, filtered connectivity was 0.2095, and filtered predicted-positive fraction was 0.00336. Later epochs shifted toward higher recall and lower precision, but aggregate Dice and connectivity declined. The fixed first-four retained prediction samples all had near-zero sample Dice; because prediction retention is fixed `first_n`, these retained samples are bounded artifacts rather than representative qualitative evidence.

## Interpretation

Classify ABI-083 as a negative but informative capped family scout, with scientific outcome `bad_research_result` rather than execution failure. It establishes that the compact strip-pooling/ribbon-context implementation is contract-compliant and resource-feasible, but the architecture underperformed the frequency-gated references on aggregate filtered Dice, MIT source behavior, precision, recall, and connectivity. The small connectivity improvement over recent ABI-080/082 variants is not large enough to justify continuing this exact strip-pooling branch unchanged.

This result does not eliminate all global-context or ribbon-context approaches. It does argue against simply adding row/column strip pooling to a U-Net backbone as the next local continuation. Future work should broaden to a materially different thin-line architecture or a trusted training/calibration/data-policy axis that addresses precision and connectivity without moving thresholding, losses, Artifact Filters, postprocessing, data loading, sampling, augmentation, target derivation, metrics, resource placement, or lifecycle behavior into Candidate code.

Canonical MCAST 2.1 remains the promotion context, and all comparisons here are capped representative family-development evidence rather than full-data promotion claims.

## Decision

Do not promote ABI-083. Do not repeat the exact full-spectral BTD strip-pooling/ribbon-context line U-Net branch unchanged. A subsequent candidate should broaden beyond this exact row/column strip-pooling scout rather than treating this first finite run as proof that all line-context architectures are exhausted.

## Artifact references

- `run_20260829_162522_e7efac/outputs/best_metrics.json`
- `run_20260829_162522_e7efac/outputs/final_metrics.json`
- `run_20260829_162522_e7efac/outputs/metrics.jsonl`
- `run_20260829_162522_e7efac/outputs/resource_profile.json`
- `run_20260829_162522_e7efac/outputs/model_summary.json`
- `run_20260829_162522_e7efac/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260829_133850_54dd6e/outputs/best_metrics.json`
- `run_20260829_152950_e53671/outputs/best_metrics.json`
