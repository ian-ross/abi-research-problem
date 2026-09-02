# ABI-077 full-spectral BTD frequency-gated line U-Net axial-neck focal-Tversky continuation

## Hypothesis

ABI-068 is the current strongest local whole-validation-tested frequency-gated reference by filtered Dice: its full Working Validation Split diagnostic reached filtered Dice 0.3951 with balanced MIT/Google behavior and stable threshold response. Its main weakness relative to ABI-066 is lower precision/connectivity and more negative-patch clutter. ABI-076 showed that simple SZA input expansion mainly moved the same backbone toward higher recall and lower precision/connectivity, while ABI-069/070/071/073 suggest that additional suppressive heads, centerline-guided mask heads, soft gates, and auxiliary-head stacking do not improve the ABI-068 operating point.

This is a **family-development continuation** within the full-spectral BTD frequency-gated line U-Net family. The proposal tests a low-capacity feature-side axial continuity neck: short and dilated horizontal/vertical context mixed residually after full-resolution frequency-pyramid fusion and before the primary/centerline heads. The expected value is to encourage local line continuity and suppress isolated clutter through learned features, without candidate-owned thresholding, postprocessing, Artifact Filters, losses, target derivation, or data policy.

## Comparison Target

Primary local target: ABI-068, `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, because it is the strongest local whole-validation-tested Candidate by aggregate filtered Dice and the direct architectural parent.

Secondary local targets: ABI-066, Run `run_20260827_230540_bf4ce3`, as the precision/connectivity-forward frequency-gated reference; ABI-070/073/076 as negative or mixed evidence for head stacking, boundary auxiliary stacking, and SZA-only expansion. Canonical MCAST 2.1 remains the human-reviewed promotion context, but this capped Run is family-development evidence rather than a full-data promotion claim.

## Expected Effect

Adding the axial continuity neck is expected to:

- preserve ABI-068's focal-Tversky recall-forward behavior and source-balanced filtered Dice;
- recover some precision and Contrail Connectivity by giving the final feature tensor short and dilated horizontal/vertical line-context before logits;
- avoid the broad clutter profile of ABI-072 by keeping the module low-capacity and localized after frequency-pyramid fusion rather than inserting heavy oriented blocks throughout the backbone;
- avoid the negative pattern from ABI-069/070/071/073 by not adding a separate suppressor, centerline-guided mask head, soft-evidence output gate, or additional auxiliary target;
- remain resource-safe by adding only a small residual neck to the already profiled ABI-068 architecture.

## Implementation Sketch

The candidate uses provider-approved `abi_16ch` input only. The front end normalizes ABI channels 1-16, derives fixed thermal BTD planes only from those approved ABI channels, and uses the existing learned 1x1 spectral mixer. The backbone remains ABI-068's high/low spatial-frequency split stem, low-frequency-gated skip fusion, dilated bottleneck context, full-resolution frequency-pyramid fusion, and oriented high-frequency line refiner.

The controlled architecture change is an `AxialContinuityNeck` after frequency-pyramid fusion. It computes a detail tensor, applies short horizontal, short vertical, dilated horizontal, and dilated vertical convolutions, concatenates those features with the original refined tensor, mixes them through a residual block, and adds the update with a bounded learnable residual scale. The model emits primary `mask_logits` and provider-derived `centerline_logits` only.

No candidate-owned data loading, split logic, sampling, augmentation transforms, losses, target derivation, metrics, threshold selection, Artifact Filters, postprocessing, filesystem writes, network calls, pretrained weights, or training loop logic are introduced. The model does not receive longitude, latitude, or reconstructed coordinate inputs.

## Contract Features Used

- Input mode: `abi_16ch` only; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target emitted as `centerline_logits` with trusted `weighted_bce` at weight 0.02.
- Primary loss: trusted `focal_tversky`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping under the current Workspace Configuration.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch, extra concurrency, GPU selection, data-policy change, or full-data promotion evaluation is requested.

## Success Criteria

Strong continuation evidence would be any of:

- capped best `val/filtered_dice` matching or exceeding ABI-068 while improving filtered precision or filtered Contrail Connectivity;
- capped best `val/filtered_dice` within 0.01 of ABI-068 with filtered precision at least 0.41 and filtered recall at least 0.38;
- reducing filtered predicted-positive fraction or negative-patch clutter proxies without falling below 0.38 aggregate filtered Dice;
- both MIT and Google filtered Dice above 0.35 with a finite, non-collapsed, late-improving trajectory.

Hard stop evidence for this exact branch would be smoke failure, non-finite behavior, prediction collapse, resource timeout, aggregate filtered Dice below 0.34 with no late improvement, or an ABI-072-like clutter profile with materially higher predicted-positive fraction and lower precision/connectivity than ABI-068.

## Fallback/Next Decision

If ABI-077 improves ABI-068's precision/connectivity trade-off while preserving source balance, request bounded whole-validation diagnostics before any promotion interpretation. If it behaves like ABI-072 or the suppressive-head variants, retain ABI-068 as the aggregate-Dice frequency-gated reference and broaden to a materially different in-contract architecture or training-policy axis rather than adding more local gates or heads. If it fails contract validation or smoke testing, classify the failure and repair only if the original low-capacity axial-neck hypothesis is preserved.
