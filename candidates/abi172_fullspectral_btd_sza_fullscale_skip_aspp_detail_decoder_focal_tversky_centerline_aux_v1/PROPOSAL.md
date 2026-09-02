# ABI-172 Full-Spectral BTD+SZA Full-Scale Skip ASPP/Detail Decoder Focal-Tversky Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-154 is the whole-validation-tested SZA-aware full-scale skip ASPP/detail precision/connectivity branch: it preserved aggregate Dice near ABI-130 while improving precision, connectivity, MIT Dice, and positive-area discipline, but it remained under-recall at the fixed threshold. ABI-171 showed that simply lowering the Centerline Target auxiliary weight does not recover a stable trade-off. ABI-172 keeps the ABI-154 architecture and Centerline Target weight fixed, changing only the trusted primary loss from `bce_dice` to `focal_tversky` to test whether the provider-owned loss can recover recall while retaining the full-scale skip branch's cleaner masks.

## Hypothesis

ABI-154's full-validation threshold sweep showed latent lower-threshold recall and Dice, suggesting useful contrail evidence exists but the fixed-threshold operating point is conservative. Focal-Tversky loss has previously produced stronger recall-oriented behavior in the ABI-068 family. Applying the trusted focal-Tversky objective to the full-scale skip ASPP/detail decoder may shift the default-threshold logits toward missed positive-patch contrails while the architecture's full-scale fusion and centerline auxiliary supervision preserve enough precision/connectivity to avoid the clutter expansion seen in simpler local calibration and auxiliary-head variants.

## Comparison Target

The primary comparison target is ABI-154 `abi154_fullspectral_btd_sza_fullscale_skip_aspp_detail_decoder_bce_dice_centerline_aux_v1`, Run `run_20260901_071026_32d3ec`: capped filtered Dice 0.3944, MIT/Google filtered Dice 0.3824/0.4260, filtered precision 0.4777, recall 0.3359, connectivity 0.4374, and filtered predicted-positive fraction 0.00255. Its whole-validation diagnostic reached filtered Dice 0.3941, precision 0.4812, recall 0.3338, connectivity 0.4438, and confirmed under-recall as the main cost.

Secondary references are ABI-130 `run_20260831_121006_7d24be` as the SZA-aware ASPP/detail aggregate/reference branch, ABI-068 `run_20260828_010836_4ccc77` as the local aggregate/source-balance focal-Tversky reference, ABI-169 `run_20260901_202820_08734b` as the negative clDice loss-swap on the same architecture, and ABI-171 `run_20260901_220525_8c0116` as the negative centerline-weight-only attempt. Canonical MCAST 2.1 remains promotion context only.

## Expected Effect

A useful outcome would raise filtered recall by at least roughly 0.02 over ABI-154 while keeping aggregate filtered Dice near the ABI-130/ABI-154/ABI-068 band, preserving source-stratified Dice on both MIT and Google, and not collapsing connectivity below roughly the ABI-130/ABI-068 range. A stronger outcome would improve aggregate filtered Dice or MIT recall while retaining ABI-154-like precision/connectivity. A negative outcome would over-shift toward expansive low-precision predictions, reduce connectivity like the ABI-169 clDice swap, or fail to recover recall despite changing the trusted primary loss.

## Implementation Sketch

- Reuse ABI-154's model architecture unchanged: normalized full-spectral ABI features, deterministic thermal BTD planes from provider-approved ABI channels, normalized and cosine Solar Geometry Input features, learned 1x1 approved-channel projection, compact residual encoder, ASPP context, high-resolution detail path, full-scale skip fusion, and line-aware final refinement.
- Emit primary `mask_logits` and provider-derived auxiliary `centerline_logits` only.
- Change only the manifest-selected trusted primary loss from `bce_dice` to `focal_tversky`.
- Keep `centerline` auxiliary supervision with trusted `weighted_bce` at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning rate, and disabled early stopping.
- Request one sequential Run; no candidate-owned scheduling, GPU placement, postprocessing, thresholding, data loading, target derivation, loss implementation, augmentation implementation, sampling implementation, or metric code is introduced.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `focal_tversky`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data claim, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes inside the trusted runtime envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it recovers recall over ABI-154 while preserving enough precision, connectivity, source balance, and aggregate filtered Dice to distinguish it from the negative ABI-169/171 branches.

## Continuation and hard stop

Continue this loss-policy branch only if ABI-172 is finite, non-degenerate, source-informative, and shows a diagnostically useful recall/default-threshold shift without severe precision, connectivity, or source-specific collapse. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. If it completes finite but simply trades ABI-154 precision/connectivity for lower aggregate Dice without useful recall/source-balance recovery, stop the exact full-scale skip focal-Tversky branch and broaden to a different calibration, architecture, data-policy, preprocessing, or evaluation frontier.

## Fallback/Next Decision

If this candidate fails from a narrow implementation defect while the controlled loss-swap hypothesis remains intact, consider at most one explicit Repair Candidate in a later Autonomy Step. If it is scientifically negative, document the result and avoid further simple loss-only swaps on ABI-154 unless a new mechanism explains why it should avoid the observed failure. If it unexpectedly challenges current capped references or combines ABI-154-like precision/connectivity with ABI-068-like recall, request separate whole-validation diagnostics before making any full-data or promotion claim.
