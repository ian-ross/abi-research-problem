# Full-spectral BTD frequency-gated line U-Net multi-scale logit-consensus follow-up

research-figures: []

## Scope

This note records ABI-080 after Run `run_20260829_133850_54dd6e` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice and whole-validation reference: `run_20260828_010836_4ccc77`
- ABI-078 frequency-gated line U-Net BCE-Dice loss-swap reference: `run_20260828_094949_ad2af0`
- ABI-079 nested-skip U-Net scout: `run_20260828_104353_1455f1`
- ABI-080 multi-scale logit-consensus continuation: `run_20260829_133850_54dd6e`

ABI-080 used provider-approved `abi_16ch` input, ABI-channel-derived thermal BTD features, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, trusted `focal_tversky` primary loss, and the provider-derived `centerline` auxiliary target with trusted `weighted_bce` at weight 0.02. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-development evidence rather than full-data promotion evidence.

## ABI-080 implementation and resource observation

ABI-080 was a targeted continuation of ABI-068. It kept the frequency-gated line U-Net backbone, BTD/mixer front end, trusted focal-Tversky loss, and centerline auxiliary output. The controlled architecture change was replacing the single final mask head with a lightweight `MultiScaleLogitConsensusHead` that blends local-detail, broad-context, and oriented-ridge mask logits through an in-model soft gate.

The intended effect was to reduce uncorroborated high-frequency false positives and recover some of ABI-066's precision/connectivity while preserving ABI-068's focal-Tversky recall. This was an architecture-only change: no candidate-owned data loading, sampling, augmentation, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, or pretrained weights were introduced. The trusted model summary recorded `abi_16ch` input shape `[16, 256, 256]`, primary `mask_logits`, one `centerline_logits` auxiliary output, and forbidden source channel indices 16 and 17 excluded.

Model summary reported 12,313,552 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 3,076.4 seconds wall time, 11,028,922,368 bytes peak CUDA reserved, one completed effective-batch-size-4 attempt, and no terminal execution failure. The head is therefore contract-feasible but materially slower/heavier than the earlier ABI-068/078 frequency-gated variants.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260828_094949_ad2af0` | ABI-078 | ABI-068 architecture with `bce_dice` primary loss | 11 | 0.3816 | 0.3704 | 0.4093 | 0.4072 | 0.3590 | 0.3061 | 0.00320 |
| `run_20260828_104353_1455f1` | ABI-079 | compact nested-skip U-Net, `focal_tversky`, centerline aux weight 0.02 | 9 | 0.2984 | 0.3153 | 0.2650 | 0.2284 | 0.4300 | 0.1265 | 0.00682 |
| `run_20260829_133850_54dd6e` | ABI-080 | ABI-068 plus multi-scale logit-consensus head | 10 | 0.3623 | 0.3490 | 0.3916 | 0.3698 | 0.3552 | 0.1795 | 0.00348 |

ABI-080 did not meet the consensus-head success criteria. Relative to ABI-068, aggregate filtered Dice fell by about -0.0341, MIT filtered Dice by -0.0396, Google filtered Dice by -0.0245, filtered precision by -0.0294, filtered recall by -0.0384, and filtered connectivity by -0.2105. The filtered predicted-positive fraction was only slightly lower than ABI-068, 0.00348 versus 0.00357, so the head did not buy enough positive-area reduction to justify the metric losses.

Relative to ABI-066, ABI-080 was lower on aggregate filtered Dice by about -0.0202, lower on MIT by -0.0148, lower on Google by -0.0376, lower on precision by -0.0729, lower on connectivity by -0.2936, and more permissive in predicted-positive fraction. Relative to ABI-078, it lost aggregate Dice, both source Dice values, precision, recall, connectivity, and positive-area control. It is better than ABI-079's permissive nested-skip scout, but not competitive with the strongest frequency-gated references.

## ABI-080 trajectory

ABI-080 trained finitely and avoided all-negative/all-positive collapse. Filtered Dice by epoch was 0.1568, 0.2717, 0.2696, 0.3035, 0.3089, 0.2902, 0.3478, 0.3476, 0.3557, 0.3623, 0.3531, and 0.3210. The selected checkpoint was epoch 10; epochs 11 and 12 regressed, with final filtered Dice 0.3210.

At the selected checkpoint, both Dataset Sources stayed non-catastrophic: MIT filtered Dice was 0.3490 and Google filtered Dice was 0.3916. The operating point was not collapsed, but it was also not the intended cleaner consensus profile: filtered precision was 0.3698, filtered recall was 0.3552, filtered connectivity was 0.1795, and filtered predicted-positive fraction was 0.00348. Final epoch behavior worsened to 0.3210 filtered Dice, 0.2784 precision, 0.3791 recall, 0.1320 connectivity, and 0.00493 filtered predicted-positive fraction.

The fixed first-four retained prediction samples all had near-zero sample Dice. Because prediction retention is `first_n`, these are bounded retained artifacts rather than representative qualitative evidence; aggregate and source-stratified validation metrics carry the decision.

## Interpretation

Classify ABI-080 as a negative capped family-development continuation of the ABI-068 frequency-gated branch. It remained finite, source-balanced, non-collapsed, and contract-feasible, but the multi-scale logit-consensus head did not recover ABI-066/078-style precision or connectivity and did not preserve ABI-068's aggregate Dice/recall. Its late regression suggests the head may be adding optimization or calibration instability rather than robust false-positive suppression.

This result does not eliminate the broader full-spectral BTD or frequency-gated line U-Net families: ABI-068 remains positive capped evidence and has whole-validation diagnostic support, while ABI-066 remains the precision/connectivity-forward reference. It does provide enough negative evidence to stop this exact consensus-head branch unless a future hypothesis has a specific corrective mechanism beyond adding more output-side agreement modules.

Canonical MCAST 2.1 remains the promotion context, and all comparisons here are capped representative family-development evidence rather than full-data promotion claims.

## Decision

Do not promote ABI-080. Do not repeat the exact multi-scale logit-consensus mask-head branch unchanged. Prefer broadening away from late/output-side refinement around ABI-068 and toward either a different architecture family or a simpler training/calibration frontier that directly addresses the precision/connectivity tradeoff without moving thresholding, losses, Artifact Filters, postprocessing, data loading, sampling, augmentation, target derivation, metrics, resource placement, or lifecycle behavior into Candidate code.

## Artifact references

- `run_20260829_133850_54dd6e/outputs/best_metrics.json`
- `run_20260829_133850_54dd6e/outputs/final_metrics.json`
- `run_20260829_133850_54dd6e/outputs/metrics.jsonl`
- `run_20260829_133850_54dd6e/outputs/resource_profile.json`
- `run_20260829_133850_54dd6e/outputs/model_summary.json`
- `run_20260829_133850_54dd6e/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260828_094949_ad2af0/outputs/best_metrics.json`
- `run_20260828_104353_1455f1/outputs/best_metrics.json`
