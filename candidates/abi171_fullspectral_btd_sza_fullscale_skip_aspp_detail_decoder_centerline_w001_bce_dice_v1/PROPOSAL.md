# ABI-171 Full-Spectral BTD+SZA Full-Scale Skip ASPP/Detail Decoder Centerline Weight 0.01 BCE-Dice v1

## Proposal classification

**Family-development continuation.** ABI-154 is the current whole-validation-tested SZA-aware full-scale-skip ASPP/detail precision/connectivity branch: it nearly ties ABI-130 and ABI-068 on aggregate filtered Dice while improving precision, connectivity, and positive-area discipline, but its fixed-threshold recall is low. Several final-head, data-policy, line-auxiliary, and compact-BiFPN follow-ups did not recover a better trade-off. ABI-171 makes one controlled trusted-manifest change to ABI-154: reduce the existing Centerline Target auxiliary weight from 0.02 to 0.01.

## Hypothesis

ABI-154's full-scale skip fusion produced useful connected, low-clutter masks, but its whole-validation diagnostic showed under-recall and latent lower-threshold Dice. The centerline auxiliary target may be acting as a mild narrow-structure prior that helps connectivity yet encourages conservative mask width/area at the fixed threshold. Lowering its trusted auxiliary weight from 0.02 to 0.01 may relax that pressure enough to recover recall and MIT/source balance while retaining the architecture's BCE-Dice calibration, full-scale context, and negative-patch discipline.

## Comparison Target

The primary comparison target is ABI-154 `abi154_fullspectral_btd_sza_fullscale_skip_aspp_detail_decoder_bce_dice_centerline_aux_v1`, Run `run_20260901_071026_32d3ec`, with capped filtered Dice 0.3944, MIT/Google filtered Dice 0.3824/0.4260, filtered precision 0.4777, recall 0.3359, connectivity 0.4374, and filtered predicted-positive fraction 0.00255. Its whole-validation evaluation reached filtered Dice 0.3941, precision 0.4812, recall 0.3338, connectivity 0.4438, and confirmed under-recall as the main cost.

Secondary references are ABI-130 `run_20260831_121006_7d24be` as the SZA-aware ASPP/detail aggregate/reference branch, ABI-068 `run_20260828_010836_4ccc77` as the local aggregate/source-balance reference, ABI-126 `run_20260831_085615_d05ab3` as the non-SZA precision/connectivity comparator, and ABI-158/ABI-170 as recent negative line-head or compact-BiFPN follow-ups. Canonical MCAST 2.1 remains promotion context only.

## Expected Effect

A useful outcome would improve ABI-154 recall or MIT filtered Dice while keeping aggregate filtered Dice within roughly 0.005 of ABI-154 and preserving most of its precision/connectivity advantage over ABI-130. A stronger outcome would match or exceed ABI-130/ABI-068 aggregate filtered Dice while keeping ABI-154-like positive-area discipline. A negative outcome would show that reducing Centerline Target pressure only degrades connectivity/precision or fails to move recall, narrowing further local auxiliary-weight tuning for this branch.

## Implementation Sketch

- Reuse ABI-154's candidate code unchanged except for the candidate identifier string.
- Keep the normalized full-spectral ABI channels, deterministic thermal BTD planes from approved ABI channels, normalized SZA and `cos(SZA)` features, learned 1x1 spectral projection, compact residual encoder, ASPP bottleneck, full-scale skip fusion, high-resolution detail path, and line-aware final refinement.
- Emit primary `mask_logits` and provider-derived `centerline_logits`.
- Change only the manifest's trusted Centerline Target auxiliary `weighted_bce` weight from 0.02 to 0.01.
- Request one sequential Run; do not add candidate-owned scheduling, GPU placement, postprocessing, thresholding, data loading, loss, target, augmentation, sampling, or metric code.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.01, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
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
6. As family-development evidence, the result is useful if it improves ABI-154 recall, MIT Dice, aggregate Dice, or source balance while preserving at least one of ABI-154's precision/connectivity/positive-area advantages over ABI-130.

## Continuation and hard stop

Continue this auxiliary-weight branch only if ABI-171 is finite, non-degenerate, source-informative, and shows a useful recall/source-balance shift without collapsing ABI-154's precision/connectivity profile. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. If it completes finite but loses ABI-154's connectivity/precision without a recall or Dice gain, stop the local centerline-weight tuning path and broaden away from full-scale-skip auxiliary adjustments.

## Fallback/Next Decision

If this candidate fails from a narrow implementation defect while the centerline-weight hypothesis remains intact, consider at most one explicit Repair Candidate in a later Autonomy Step. If it is scientifically negative, document the result and broaden to another contract-compliant architecture, calibration, data-policy, loss/front-end, or preprocessing frontier rather than repeating local auxiliary-weight changes. If it unexpectedly challenges current references on capped and source-stratified metrics, request separate whole-validation diagnostics before making any full-data or promotion claim.
