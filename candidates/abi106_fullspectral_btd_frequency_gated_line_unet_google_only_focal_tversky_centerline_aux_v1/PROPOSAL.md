# ABI-106 full-spectral BTD frequency-gated line U-Net Google-only continuation

## Hypothesis

ABI-068 remains the strongest local capped aggregate filtered-Dice reference in the full-spectral BTD frequency-gated line U-Net branch, but later architecture refinements aimed at precision/connectivity have mostly failed to improve it. A safer next axis is a provider-owned data-policy test rather than another candidate-owned late head or gate. ABI-106 keeps the ABI-068 architecture, trusted focal-Tversky primary loss, provider-derived Centerline Target auxiliary supervision, random mirroring, learning rate, and resource profile, but changes the trusted training traversal from `combined_source_balanced` to `google_only`.

This is a **family-development continuation** within the full-spectral BTD frequency-gated line U-Net family. The hypothesis is not that a source-specialized sampler is promotion-ready, but that Google-only training can reveal whether the branch has a cleaner Google-source operating point that source-balanced traversal is diluting. If the run improves Google filtered Dice, precision, connectivity, or positive-area discipline without catastrophic MIT transfer, it would motivate a later trusted data-policy or source-mixture Capability Request rather than candidate-owned sampling code.

## Comparison Target

Primary local target: ABI-068, `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, because it is the strongest capped aggregate frequency-gated focal-Tversky reference.

Secondary local targets: ABI-066, `abi066_fullspectral_btd_frequency_gated_line_unet_cldice_centerline_aux_v1`, Run `run_20260827_230540_bf4ce3`, because it remains the precision/connectivity-forward reference; and ABI-096, `abi096_fullspectral_btd_frequency_gated_line_unet_detshuffle_focal_tversky_centerline_aux_v1`, because it tested a different trusted data traversal without source specialization. Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-106 is capped data-policy evidence, not a full-data promotion claim.

## Expected Effect

Google-only trusted sampling is expected to:

- improve or clarify Google-source filtered Dice relative to ABI-068s capped Google value while retaining the same architecture;
- test whether source-balanced replacement sampling is trading away Google precision/connectivity or positive-area discipline;
- expose the MIT transfer cost of a source-specialized focal-Tversky branch using Harness-owned validation metrics;
- avoid another candidate-owned postprocessing, thresholding, Artifact Filter, output-head, or sampler workaround;
- keep resource use close to ABI-068 because the model code is unchanged.

## Implementation Sketch

The candidate uses provider-approved `abi_16ch` input only. The architecture is copied from ABI-068: normalized ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, learned 1x1 spectral mixing, high/low frequency split stem, multi-dilation coarse context, decoder skip fusion, full-resolution frequency-pyramid fusion, and oriented line refinement. It emits primary `mask_logits` plus provider-derived `centerline_logits`.

The controlled manifest change is `data.sampling_policy: google_only`. Candidate code does not implement source selection or sampler weights; those remain provider/Harness-owned. No candidate-owned data loading, split logic, capped-record selection, augmentation transforms, target derivation, losses, metrics, threshold selection, Artifact Filters, postprocessing, filesystem writes, network calls, pretrained weights, or training loop logic are introduced. The model does not receive longitude, latitude, or reconstructed coordinate inputs.

## Contract Features Used

- Input mode: `abi_16ch` only; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target emitted as `centerline_logits` with trusted `weighted_bce` at weight 0.02.
- Primary loss: trusted `focal_tversky`.
- Data policy: provider-owned `google_only` sampling and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping under the current Workspace Configuration.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch, extra concurrency, GPU selection, custom evaluation, source-mixture implementation, or full-data promotion evaluation is requested.

## Success Criteria

Useful continuation evidence would be any of:

- Google capped `val/source/google/filtered_dice` improves over ABI-068 by at least 0.01 while aggregate filtered Dice remains within 0.03 of ABI-068;
- filtered precision or Contrail Connectivity improves over ABI-068 by at least 0.03 with filtered recall remaining at least 0.34;
- filtered predicted-positive fraction falls at least 10% below ABI-068 while both MIT and Google filtered Dice remain at least 0.32;
- the run remains finite, non-collapsed, late-improving, and shows diagnostically useful source asymmetry that could justify a trusted source-mixture Capability Request.

Hard stop evidence for this exact data-policy branch would be smoke failure, non-finite behavior, prediction collapse, aggregate filtered Dice below 0.33 without late improvement, MIT filtered Dice below 0.25, Google filtered Dice failing to approach ABI-068, or a larger predicted-positive burden with lower precision/connectivity than ABI-068.

## Fallback/Next Decision

If ABI-106 improves Google behavior or positive-area discipline without catastrophic MIT transfer, compare it with ABI-068/066 and consider whether the next safe handoff should be a source-mixture Capability Request or a complementary MIT-only scout. If it is finite but non-improving, prefer the existing source-balanced policy and stop this exact Google-only branch. If it fails contract validation or smoke testing, classify the failure and repair only if the original provider-owned data-policy hypothesis and Comparison Target are preserved. Do not move sampling, augmentation, data loading, metrics, thresholds, Artifact Filters, target derivation, resource placement, or lifecycle behavior into Candidate code.
