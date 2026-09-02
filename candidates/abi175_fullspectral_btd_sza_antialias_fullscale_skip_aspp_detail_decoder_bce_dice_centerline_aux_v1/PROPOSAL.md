# ABI-175 Full-Spectral BTD+SZA Anti-Aliased Full-Scale Skip ASPP/Detail Decoder BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-154 remains the whole-validation-tested SZA-aware ASPP/detail precision/connectivity reference, while ABI-173 is the whole-validation-tested SZA-aware ASPP/detail aggregate branch with useful recall recovery but higher negative-patch clutter and lower connectivity. ABI-174 showed that another local signed-detail line-consensus head is not the best next move. ABI-175 instead changes the encoder downsampling mechanism in the ABI-154 lineage so thin-line evidence is preserved before bottlenecking and full-scale skip fusion, rather than adding another terminal head or candidate-owned calibration/postprocessing step.

## Hypothesis

Max-pooling in the SZA-aware full-scale skip ASPP/detail encoder may discard or alias narrow contrail structures before the ASPP bottleneck and decoder can combine local detail with context. Replacing max-pool downsampling with fixed binomial anti-aliased downsampling should make encoder features less sensitive to one-pixel alignment while retaining ABI-154's BCE-Dice calibration, full-scale skip precision, and centerline auxiliary supervision. The expected effect is a modest default-threshold recall and MIT/source-balance recovery relative to ABI-154 without the precision/connectivity loss seen in ABI-173 and ABI-174.

## Comparison Target

Primary comparison target: ABI-154 `abi154_fullspectral_btd_sza_fullscale_skip_aspp_detail_decoder_bce_dice_centerline_aux_v1`, Run `run_20260901_071026_32d3ec`, with capped filtered Dice 0.3944, MIT/Google filtered Dice 0.3824/0.4260, filtered precision 0.4777, recall 0.3359, connectivity 0.4374, and filtered predicted-positive fraction 0.00255. Whole-validation diagnostics for ABI-154 reached filtered Dice 0.3941, precision 0.4812, recall 0.3338, connectivity 0.4438, and low negative-patch clutter.

Secondary references are ABI-173 `run_20260901_234732_bd5917` as the signed-detail recall/aggregate branch, ABI-174 `run_20260902_005632_5651ef` as the negative local line-consensus follow-up, ABI-130 `run_20260831_121006_7d24be` as the prior SZA-aware ASPP/detail aggregate reference, and ABI-068 `run_20260828_010836_4ccc77` as the broader capped aggregate/source-balance comparator.

## Expected Effect

A useful outcome would keep aggregate filtered Dice in the ABI-154/130/173/068 band while raising recall versus ABI-154 by about 0.01-0.03, keeping connectivity closer to ABI-154 than ABI-173/174, and avoiding a large increase in filtered predicted-positive fraction. A stronger outcome would preserve ABI-154-like precision/connectivity while recovering ABI-173-like MIT/aggregate overlap. A negative outcome would show that anti-aliased encoder preservation either acts like another under-recall conservative branch or loosens positive-area discipline without improving filtered Dice.

## Implementation Sketch

- Reuse the ABI-154 provider-approved front end: normalized GOES ABI channels 1-16, thermal brightness-temperature-difference planes derived only from approved ABI channels, normalized Solar Geometry Input plus cosine SZA, and a learned 1x1 projection over approved input tensors.
- Keep the ABI-154 detail/context stem, residual encoder widths, ASPP bottleneck, decoder fusion, high-resolution detail path, full-scale skip fusion, line-aware refinement, primary `mask_logits`, and provider-derived `centerline_logits` auxiliary output.
- Replace each encoder `MaxPool2d(2)` with `AntiAliasedDownsample`: a fixed, non-trainable 3x3 binomial low-pass depthwise convolution applied with stride 2 to learned feature maps before the residual encoder block. This is an architecture-only feature transform, not data loading, target derivation, thresholding, postprocessing, or an Artifact Filter.
- Keep trusted `bce_dice` primary loss, trusted `weighted_bce` Centerline Target auxiliary weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, disabled early stopping, and a single sequential representative capped Run.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted Docker training timeout. No full-data claim, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes inside the trusted runtime envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it improves ABI-154 recall or MIT/source balance while keeping aggregate Dice within about 0.005-0.010 of ABI-154 and preserving substantially more precision/connectivity than ABI-173/174, or if it clearly maps the cost of anti-aliased feature downsampling in this branch.

## Continuation and hard stop

Continue the anti-aliased full-scale skip branch only if ABI-175 is finite, non-degenerate, source-informative, and shows a recall/source-balance gain without severe loss of ABI-154's precision/connectivity. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, shape/contract errors, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. If it completes finite but fails to improve the ABI-154 tradeoff, stop this downsampling-only branch and broaden to a different architecture, preprocessing, loss, data-policy, or evaluation frontier.

## Fallback/Next Decision

If ABI-175 fails from a narrow implementation defect while the anti-aliased downsampling hypothesis remains intact, consider at most one explicit Repair Candidate in a later Autonomy Step. If it is scientifically negative, retain ABI-154 as the precision/connectivity reference, ABI-173 as the signed-detail aggregate branch, ABI-130 as the prior SZA-aware ASPP/detail aggregate reference, and ABI-068 as the broader capped aggregate/source-balance comparator. If ABI-175 preserves ABI-154-like precision/connectivity while recovering recall or source balance, request separate whole-validation diagnostics before making any full-data or promotion claim.
