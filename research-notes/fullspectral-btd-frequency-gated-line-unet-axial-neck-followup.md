# Full-spectral BTD frequency-gated line U-Net axial-neck follow-up

research-figures: []

## Scope

This note records ABI-077 after Run `run_20260828_085236_b7d0f8` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice and whole-validation reference: `run_20260828_010836_4ccc77`
- ABI-073 boundary-auxiliary comparison: `run_20260828_055812_4ba74e`
- ABI-076 SZA-input follow-up: `run_20260828_080008_ce4819`
- ABI-077 axial-continuity-neck follow-up: `run_20260828_085236_b7d0f8`

ABI-077 used provider-approved `abi_16ch` input, ABI-channel-derived thermal BTD features, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, trusted `focal_tversky` primary loss, and the provider-derived `centerline` auxiliary target at trusted `weighted_bce` weight 0.02. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-development evidence rather than full-data promotion evidence.

## ABI-077 implementation and resource observation

ABI-077 started from the ABI-068 frequency-gated line U-Net backbone and added a low-capacity `AxialContinuityNeck` after full-resolution frequency-pyramid fusion and before the primary/centerline heads. The neck computes detail features and mixes short horizontal, short vertical, dilated horizontal, and dilated vertical context back into the refined tensor with a bounded learned residual scale. The intended effect was to improve local line continuity and reduce isolated clutter without adding another output-head stack or candidate-owned postprocessing.

The Run stayed inside the Candidate Experiment Contract: no longitude/latitude inputs, no reconstructed coordinate inputs, no candidate-owned data loading, no custom loss or target derivation, no candidate-owned augmentation, no metrics, no thresholding, no Artifact Filters, no postprocessing, no network access, and no pretrained weights. The trusted model summary recorded `abi_16ch` input shape `[16, 256, 256]`, primary `mask_logits`, one `centerline_logits` auxiliary output, and forbidden source channel indices 16 and 17 excluded.

Model summary reported 12,297,354 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on an A100 with 2,971.2 seconds wall time, 10,619,977,728 bytes peak CUDA reserved, and no terminal execution failure.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260828_080008_ce4819` | ABI-076 | ABI-068 plus provider-approved SZA input | 12 | 0.3790 | 0.3718 | 0.3962 | 0.3463 | 0.4184 | 0.3013 | 0.00438 |
| `run_20260828_085236_b7d0f8` | ABI-077 | ABI-068 plus residual axial-continuity neck | 11 | 0.3615 | 0.3682 | 0.3461 | 0.2990 | 0.4568 | 0.1902 | 0.00554 |

ABI-077 did not satisfy its main continuation criteria. Relative to ABI-068, aggregate filtered Dice fell by about -0.0349, MIT filtered Dice by about -0.0204, Google filtered Dice by about -0.0700, filtered precision by about -0.1001, and filtered connectivity by about -0.1998. Filtered recall improved by about +0.0632, but the filtered predicted-positive fraction rose from 0.00357 to 0.00554, indicating a much more permissive operating point rather than a cleaner continuity/precision trade-off.

Relative to ABI-066, ABI-077 improved recall by about +0.1201 and slightly exceeded MIT filtered Dice by about +0.0044, but it lost aggregate filtered Dice (-0.0211), Google filtered Dice (-0.0831), precision (-0.1437), connectivity (-0.2828), and predicted more than twice the filtered positive fraction. Relative to ABI-076, ABI-077 moved still further recall-forward, but lost aggregate Dice (-0.0175), Google Dice (-0.0501), precision (-0.0472), and connectivity (-0.1111).

## ABI-077 trajectory

ABI-077 trained finitely and avoided all-negative/all-positive prediction collapse. Filtered Dice by epoch was 0.1840, 0.2402, 0.2590, 0.2515, 0.3133, 0.2905, 0.2730, 0.3121, 0.3560, 0.3359, 0.3615, and 0.3587 at epoch 12. The best checkpoint was epoch 11, with the final epoch nearly tied but not better.

At the best checkpoint, MIT filtered Dice was 0.3682 and Google filtered Dice was 0.3461. This avoided a hard source-specific collapse, but the Google score was materially weaker than the ABI-068, ABI-066, ABI-073, and ABI-076 references. The operating profile was strongly recall-forward: filtered recall reached 0.4568 while filtered precision fell to 0.2990, filtered connectivity to 0.1902, and filtered predicted-positive fraction to 0.00554. The aggregate curve improved late, but the improvement came with broad positive support rather than with the intended precision or line-connectivity recovery.

The fixed first-four retained prediction artifacts should not be treated as representative qualitative evidence. The useful evidence for this capped Run is the aggregate/source-stratified validation metrics, non-degenerate predicted-positive fractions, resource profile, and epoch trajectory above.

## Interpretation

Classify ABI-077 as negative capped family-development evidence for this exact residual axial-continuity neck, not as an execution failure and not as evidence against all continuity-oriented architectures. The candidate completed reliably within contract and resource limits, remained finite, and was still non-collapsed. However, the axial neck amplified the recall-forward/clutter-permissive pattern already seen in ABI-076 and ABI-072: higher recall and higher positive area, but lower filtered Dice, precision, Google-source strength, and connectivity than the ABI-068 reference.

This result strengthens the emerging local pattern that adding late feature refiners, gates, suppressors, auxiliary-head stacks, or orientation/axial modules to the current frequency-gated focal-Tversky branch is not improving ABI-068's capped operating point. ABI-068 remains the strongest local frequency-gated reference by capped aggregate filtered Dice and has whole-validation diagnostics on the canonical 3,088-sample Working Validation Split. ABI-066 remains the precision/connectivity-forward local reference. Canonical MCAST 2.1 remains promotion context; this capped result should not be interpreted as full-data promotion evidence.

## Decision

Do not promote ABI-077 and do not request whole-validation diagnostics for this exact Run. Do not continue the same axial-neck branch unchanged: it failed to recover precision/connectivity and introduced a more permissive positive-area profile.

The next useful research step should broaden away from additional late feature refiners on ABI-068. In-contract alternatives include returning to a loss/auxiliary-weight axis that targets precision/connectivity without extra head or neck capacity, scouting a materially different encoder-decoder family with an explicitly bounded resource profile, or writing a focused analysis that consolidates the frequency-gated branch evidence before selecting the next family. Any follow-up should continue preserving provider/Harness ownership of data loading, sampling, augmentation, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle.

## Artifact references

- `run_20260828_085236_b7d0f8/outputs/best_metrics.json`
- `run_20260828_085236_b7d0f8/outputs/final_metrics.json`
- `run_20260828_085236_b7d0f8/outputs/metrics.jsonl`
- `run_20260828_085236_b7d0f8/outputs/resource_profile.json`
- `run_20260828_085236_b7d0f8/outputs/model_summary.json`
- `run_20260828_085236_b7d0f8/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260828_055812_4ba74e/outputs/best_metrics.json`
- `run_20260828_080008_ce4819/outputs/best_metrics.json`
