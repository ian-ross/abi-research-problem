# Full-spectral BTD frequency-gated line U-Net BCE-Dice follow-up

research-figures: []

## Scope

This note records ABI-078 after Run `run_20260828_094949_ad2af0` completed.

Source Runs:

- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice and whole-validation reference: `run_20260828_010836_4ccc77`
- ABI-076 SZA-input follow-up: `run_20260828_080008_ce4819`
- ABI-077 axial-continuity-neck follow-up: `run_20260828_085236_b7d0f8`
- ABI-078 BCE-Dice loss-swap follow-up: `run_20260828_094949_ad2af0`

ABI-078 used provider-approved `abi_16ch` input, ABI-channel-derived thermal BTD features, combined source-balanced sampling, trusted random mirroring, batch size 4, constant learning rate 0.0003, 12 epochs, disabled early stopping, trusted `bce_dice` primary loss, and the provider-derived `centerline` auxiliary target at trusted `weighted_bce` weight 0.02. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-development evidence rather than full-data promotion evidence.

## ABI-078 implementation and resource observation

ABI-078 intentionally kept ABI-068's frequency-gated line U-Net architecture and centerline auxiliary output unchanged. The controlled change was only the trusted primary loss: ABI-068 used `focal_tversky`, while ABI-078 used `bce_dice`. The intended effect was to reduce ABI-068's recall-forward positive-area pressure and recover some precision or connectivity without adding another late refiner, suppressor head, auxiliary target, SZA input, or candidate-owned threshold/postprocessing path.

The Run stayed inside the Candidate Experiment Contract: no longitude/latitude inputs, no reconstructed coordinate inputs, no candidate-owned data loading, no custom loss or target derivation, no candidate-owned augmentation, no metrics, no thresholding, no Artifact Filters, no postprocessing, no network access, and no pretrained weights. The trusted model summary recorded `abi_16ch` input shape `[16, 256, 256]`, primary `mask_logits`, one `centerline_logits` auxiliary output, and forbidden source channel indices 16 and 17 excluded.

Model summary reported 12,087,561 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on an A100 with 2,693.2 seconds wall time, 9,539,944,448 bytes peak CUDA reserved, and no terminal execution failure.

## Best-validation comparison

| Run | Candidate | Primary change | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux weight 0.02 | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, `focal_tversky`, centerline aux weight 0.02 | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260828_080008_ce4819` | ABI-076 | ABI-068 plus provider-approved SZA input | 12 | 0.3790 | 0.3718 | 0.3962 | 0.3463 | 0.4184 | 0.3013 | 0.00438 |
| `run_20260828_085236_b7d0f8` | ABI-077 | ABI-068 plus residual axial-continuity neck | 11 | 0.3615 | 0.3682 | 0.3461 | 0.2990 | 0.4568 | 0.1902 | 0.00554 |
| `run_20260828_094949_ad2af0` | ABI-078 | ABI-068 architecture with `bce_dice` primary loss | 11 | 0.3816 | 0.3704 | 0.4093 | 0.4072 | 0.3590 | 0.3061 | 0.00320 |

ABI-078 is a mixed controlled-loss result. Relative to ABI-068, aggregate filtered Dice fell by about -0.0148, MIT filtered Dice by about -0.0182, Google filtered Dice by about -0.0069, filtered recall by about -0.0346, and filtered connectivity by about -0.0839. Filtered precision improved only slightly by about +0.0080, while filtered predicted-positive fraction dropped from 0.00357 to 0.00320.

Relative to ABI-066, ABI-078 nearly tied aggregate filtered Dice within about -0.0009 and improved MIT filtered Dice by about +0.0066 and recall by about +0.0223. It did not recover the intended ABI-066-style precision/connectivity profile: filtered precision remained about -0.0355 below ABI-066, connectivity was about -0.1670 below ABI-066, Google filtered Dice was about -0.0199 below ABI-066, and filtered predicted-positive fraction remained higher than ABI-066.

Relative to the recent ABI-076 and ABI-077 variants, ABI-078 moved away from the highly permissive recall-forward profile. It has lower recall than those two Runs, but better aggregate filtered Dice, better precision, better connectivity, and lower predicted-positive fraction. This supports the idea that simpler loss-axis moves are currently cleaner than adding late feature refiners or extra input/refiner capacity to ABI-068, even though the BCE-Dice loss did not surpass the ABI-068 reference.

## ABI-078 trajectory

ABI-078 trained finitely and avoided all-negative/all-positive prediction collapse. Filtered Dice by epoch was 0.2179, 0.3053, 0.3117, 0.3367, 0.3464, 0.3607, 0.3581, 0.3663, 0.3636, 0.3710, 0.3816, and 0.3752. The selected best checkpoint was epoch 11, with the final epoch slightly lower on aggregate filtered Dice but higher on precision, connectivity, and Google filtered Dice.

At the best checkpoint, both Dataset Sources were non-catastrophic: MIT filtered Dice was 0.3704 and Google filtered Dice was 0.4093. The operating point was less recall-forward than ABI-068: filtered recall was 0.3590, filtered precision was 0.4072, and filtered predicted-positive fraction was 0.00320. The fixed first-four retained prediction artifacts include one empty-mask perfect case and three near-zero sample Dice cases; as with the preceding notes, they are first-n retention artifacts rather than representative qualitative evidence.

The final epoch is diagnostically interesting but not a selected improvement: aggregate filtered Dice fell to 0.3752, MIT filtered Dice fell to 0.3553, and recall fell to 0.3146, while Google filtered Dice rose to 0.4250, precision rose to 0.4647, connectivity rose to 0.3723, and filtered predicted-positive fraction fell to 0.00245. This suggests BCE-Dice may continue moving the model toward a cleaner, more conservative threshold-0.5 operating point, but under the current fixed 12-epoch policy the best checkpoint remains below ABI-068 on the primary metric.

## Interpretation

Classify ABI-078 as mixed capped family-development evidence for the frequency-gated line U-Net branch. It partially validates the loss-swap hypothesis by reducing predicted-positive burden relative to ABI-068 and avoiding the broad permissive profiles seen in ABI-076 and ABI-077. It also satisfies the proposal's non-degenerate source-balance criterion, with both MIT and Google filtered Dice above 0.35 and aggregate filtered precision above 0.40.

However, ABI-078 does not provide the intended strong precision/connectivity recovery. It is just under ABI-066 on aggregate filtered Dice, materially below ABI-066 on connectivity, and below ABI-068 on the primary metric, recall, MIT Dice, Google Dice, and connectivity. ABI-068 therefore remains the strongest local whole-validation-tested aggregate-Dice reference, while ABI-066 remains the precision/connectivity-forward reference. Canonical MCAST 2.1 remains promotion context; this capped Run should not be interpreted as full-data promotion evidence.

## Decision

Do not promote ABI-078 from this capped Run. Do not continue the exact BCE-Dice loss-swap branch unchanged as a primary improvement path, because the cleaner positive-area profile did not recover enough precision/connectivity to offset the aggregate Dice and recall loss versus ABI-068.

The result is still useful enough to preserve as a conservative operating-point reference. A later bounded whole-validation failure-bucket diagnostic could be justified if the campaign needs to quantify whether ABI-078 actually reduces negative-patch clutter or improves threshold stability on the full Working Validation Split. The next architecture-development step should otherwise broaden beyond more late add-on modules around ABI-068 and consider a materially different family or a simpler training-policy/loss-axis comparison that targets ABI-068's precision/connectivity loss while preserving its full-validation aggregate strength. Any follow-up should continue preserving provider/Harness ownership of data loading, sampling, augmentation, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle.

## Artifact references

- `run_20260828_094949_ad2af0/outputs/best_metrics.json`
- `run_20260828_094949_ad2af0/outputs/final_metrics.json`
- `run_20260828_094949_ad2af0/outputs/metrics.jsonl`
- `run_20260828_094949_ad2af0/outputs/resource_profile.json`
- `run_20260828_094949_ad2af0/outputs/model_summary.json`
- `run_20260828_094949_ad2af0/outputs/prediction_samples/samples.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/evaluations/eval_evalreq_abi068_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/evaluations/eval_evalreq_abi066_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260828_080008_ce4819/outputs/best_metrics.json`
- `run_20260828_085236_b7d0f8/outputs/best_metrics.json`
