# ABI-157 Full-Spectral BTD+SZA Full-Scale Skip ASPP/Detail Decoder Deterministic-Shuffle BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-154 is the whole-validation-tested SZA-aware full-scale-skip ASPP/detail precision/connectivity branch: it nearly tied ABI-130 on aggregate filtered Dice while improving precision, connectivity, MIT Dice, and positive-area discipline, but it remained under-recall-prone at the fixed threshold. ABI-155 and ABI-156 showed that local final-head and feature-calibration patches did not recover recall without giving back the branchs precision/connectivity. ABI-157 broadens from local architecture patches to a controlled provider-owned data traversal change while preserving the ABI-154 model architecture.

## Hypothesis

ABI-154s whole-validation diagnostic suggests the full-scale skip architecture has useful negative-patch discipline and connectivity, but its selected operating point is conservative. The `combined_source_balanced` traversal explicitly interleaves Dataset Sources and positive-patch preference over the already selected capped records. Because the representative cap already selects equal counts per Dataset Source and preserves positive/negative coverage, the simpler trusted `deterministic_shuffle` traversal may reduce ordering-induced calibration oscillation and expose the model to a less structured epoch sequence. This could recover fixed-threshold recall or source balance while preserving ABI-154s precision/connectivity branch. A negative result would show that ABI-154s under-recall is architectural/calibration-driven rather than a traversal artifact.

## Comparison Target

The primary comparison target is ABI-154 `abi154_fullspectral_btd_sza_fullscale_skip_aspp_detail_decoder_bce_dice_centerline_aux_v1`, Run `run_20260901_071026_32d3ec`: capped filtered Dice 0.3944, MIT/Google filtered Dice 0.3824/0.4260, filtered precision 0.4777, recall 0.3359, connectivity 0.4374, and filtered predicted-positive fraction 0.00255. Its whole-validation diagnostic reached filtered Dice 0.3941, precision 0.4812, recall 0.3338, connectivity 0.4438, and confirmed the precision/connectivity trade-off with conservative recall.

Secondary references are ABI-130 `run_20260831_121006_7d24be` as the SZA-aware ASPP/detail aggregate/reference branch, ABI-068 `run_20260828_010836_4ccc77` as the local capped aggregate/source-balance reference, ABI-126 `run_20260831_085615_d05ab3` as the ASPP/detail precision/connectivity comparator, ABI-148 `run_20260901_025820_cd85e5` as a negative low-learning-rate traversal-stability attempt on ABI-130, and ABI-156 `run_20260901_090713_9c7d32` as the failed feature-calibration continuation.

## Expected Effect

A useful outcome would keep ABI-154-like precision/connectivity or positive-area discipline while improving filtered recall, MIT filtered Dice, aggregate filtered Dice, late-epoch stability, or Google/MIT balance. A stronger outcome would match or improve ABI-130/ABI-068 capped aggregate filtered Dice without losing ABI-154s high precision and connectivity. A negative outcome would materially lower aggregate/source filtered Dice or connectivity without recall recovery, implying that deterministic traversal is not a good way to repair ABI-154s conservative default-threshold operating point.

## Implementation Sketch

- Reuse ABI-154s model code unchanged except for candidate identity strings: normalized full-spectral raw features, deterministic thermal BTD planes from approved ABI channels, normalized SZA and `cos(SZA)` features, learned 1x1 spectral projection, residual encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail/context stem, full-scale skip fusion, line-aware refinement, and primary/centerline heads.
- Change only the trusted manifest sampling policy from `combined_source_balanced` to `deterministic_shuffle`.
- Keep provider-approved `abi_16ch_plus_sza` input, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping.
- Emit primary `mask_logits` and provider-derived auxiliary `centerline_logits` only.
- Request one sequential Run; no candidate-owned scheduling, GPU placement, data loading, sampling implementation, postprocessing, thresholding, loss, target, augmentation, or metric code is introduced.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `deterministic_shuffle`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data claim, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes inside the trusted runtime envelope already demonstrated by ABI-154/156.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it improves ABI-154 filtered recall, MIT Dice, aggregate Dice, source balance, trajectory stability, or retains its precision/connectivity/positive-area strength while clarifying whether traversal policy affects the conservative operating point.

## Continuation and hard stop

Continue this data-policy branch only if ABI-157 is finite, non-degenerate, source-informative, and preserves at least one useful ABI-154-relative diagnostic such as precision, connectivity, positive-area discipline, recall recovery, source balance, or late-epoch stability. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. If it completes finite but falls materially below ABI-154 and ABI-130 without a compensating recall/source/stability gain, stop the exact deterministic-shuffle full-scale-skip variant and broaden away from this branch.

## Fallback/Next Decision

If this candidate fails from a narrow implementation defect while the data-policy hypothesis remains intact, consider at most one explicit Repair Candidate in a later Autonomy Step. If it is scientifically negative, document the result and broaden to another contract-compliant architecture, calibration, loss/auxiliary, preprocessing, or data-policy frontier rather than repeating ad-hoc full-scale-skip calibration changes. If it unexpectedly challenges current references on capped and source-stratified metrics, request separate whole-validation diagnostics before making any full-data or promotion claim.
