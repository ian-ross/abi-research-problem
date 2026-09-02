# ABI-073 full-spectral BTD frequency-gated line U-Net focal-Tversky with centerline and boundary auxiliaries

## Hypothesis

ABI-068 is the strongest local whole-validation-tested Candidate by filtered Dice so far. It preserved the frequency-gated line U-Net family's source-balanced finite behavior and improved recall over ABI-066, but the full Working Validation Split diagnostic showed higher negative-patch clutter, lower precision, and lower Contrail Connectivity than ABI-066. Recent post-decoder suppression/gating variants (ABI-069/070/071) and the high-capacity steerable-ridge scout (ABI-072) did not improve that trade-off.

This is a **family-development continuation** within the full-spectral BTD frequency-gated line U-Net family. The hypothesis is that adding a very low-weight trusted Boundary Target auxiliary head to ABI-068 can sharpen learned mask features and modestly reduce false-positive clutter while the existing centerline auxiliary head preserves thin-line continuity and focal-Tversky preserves recall.

## Comparison Target

Primary target: ABI-068, `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, because it is the current strongest local whole-validation-tested frequency-gated candidate by aggregate filtered Dice.

Secondary targets: ABI-066 (`run_20260827_230540_bf4ce3`) as the precision/connectivity-forward reference, and ABI-072 (`run_20260828_050329_c01ecf`) as negative evidence that heavier steerable-ridge context increased clutter rather than reducing it. Canonical MCAST 2.1 remains the promotion context; this capped candidate is not a promotion claim.

## Expected Effect

Adding a low-weight boundary auxiliary target is expected to:

- keep ABI-068-like filtered recall and source-balanced Dice through the unchanged focal-Tversky primary loss and centerline auxiliary supervision;
- improve filtered precision or reduce filtered predicted-positive fraction by encouraging sharper spatial support around the Contrail Mask boundary;
- preserve or recover some Contrail Connectivity relative to ABI-068 by retaining the existing centerline auxiliary branch;
- provide a controlled auxiliary-target test without changing provider-owned data loading, sampling, augmentation, target derivation, loss implementations, metrics, thresholding, Artifact Filters, or postprocessing.

## Implementation Sketch

The candidate starts from the ABI-068 `model.py` architecture: normalized full-spectral ABI channels 1-16, explicit thermal BTD planes derived only from approved ABI channels, learned 1x1 spectral mixing, a high/low spatial-frequency split stem, low-frequency-gated skip fusion, multi-dilation coarse context, full-resolution frequency-pyramid fusion, and an oriented high-frequency line refiner.

The model emits primary `mask_logits`, provider-derived `centerline_logits`, and provider-derived `boundary_logits`. The boundary head is a single 1x1 convolution from the same refined feature tensor as the primary and centerline heads, so the architecture change is low-capacity and resource-bounded. The manifest keeps trusted `focal_tversky`, `combined_source_balanced` sampling, trusted `random_mirroring`, AdamW, learning rate 0.0003, batch size 4, 12 epochs, and constant learning rate. The centerline auxiliary weight remains 0.02; the added boundary auxiliary weight is 0.01.

No longitude, latitude, reconstructed coordinate inputs, custom data loaders, custom samplers, custom augmentations, custom losses, target derivation, metrics, threshold selection, Artifact Filters, postprocessing, filesystem writes, network calls, pretrained weights, or training loops are introduced.

## Contract Features Used

- Input mode: provider-approved `abi_16ch` only.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary targets: provider-derived `centerline` output `centerline_logits` with trusted `weighted_bce` at weight 0.02, plus provider-derived `boundary` output `boundary_logits` with trusted `weighted_bce` at weight 0.01.
- Primary loss: trusted `focal_tversky`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, disabled early stopping under the active Workspace Configuration.

## Budget Requested

Run sequentially under the active Workspace Configuration: at most 1,024 provider-selected train and validation records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch, extra concurrency, GPU selection, data-policy change, or full-data promotion evaluation is requested.

## Success Criteria

Useful continuation evidence would be any of:

- best capped `val/filtered_dice` matching or exceeding ABI-068 while reducing filtered predicted-positive fraction or improving filtered precision;
- best capped `val/filtered_dice` within 0.01 of ABI-068 while improving filtered Contrail Connectivity toward ABI-066;
- filtered recall at least 0.38 with filtered precision at least 0.40 and both MIT and Google filtered Dice above 0.35;
- a finite, non-collapsed, late-improving trajectory that shows the boundary auxiliary changes the precision/recall/clutter trade-off without source-catastrophic behavior.

Hard stop evidence for this exact branch would be contract/smoke failure, non-finite behavior, prediction collapse, aggregate filtered Dice below 0.34 without late improvement, a lower-precision higher-clutter result like ABI-071/072, or evidence that adding boundary supervision merely weakens ABI-068 without improving precision, connectivity, or source behavior.

## Fallback/Next Decision

If ABI-073 preserves ABI-068's filtered Dice while recovering precision/connectivity or lowering clutter, request bounded whole-validation failure-bucket diagnostics before any promotion interpretation. If it is finite but weaker, retain ABI-068 as the local aggregate-Dice reference and avoid more auxiliary-head stacking in this branch. If it fails validation or smoke testing, classify and repair only if the original low-weight trusted boundary-auxiliary hypothesis is preserved. If it does not improve the operating profile, broaden to a different in-contract architecture or training-policy axis rather than moving provider-owned losses, data policy, evaluation, thresholding, or Artifact Filters into Candidate code.
