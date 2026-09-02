# ABI-178 Thermal BTD Signed-Detail Full-Scale Skip ASPP Decoder BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation / input-preprocessing frontier.** ABI-173 remains the strongest whole-validation-tested SZA-aware ASPP/detail aggregate branch, ABI-154 remains the cleaner SZA-aware precision/connectivity branch, ABI-130 is the prior SZA-aware ASPP/detail reference, and ABI-068 remains the broader capped aggregate/source-balance comparator. ABI-174, ABI-176, and ABI-177 showed that additional local signed-detail/full-scale fusion or recurrent-line ASPP patches did not preserve the strongest aggregate/source tradeoff. ABI-178 broadens the branch by changing the provider-approved input mode to thermal-only ABI channels while retaining the signed-detail ASPP decoder pattern.

## Hypothesis

ABI-173's signed-detail preprocessing recovered useful default-threshold recall, but whole-validation diagnostics showed a material negative-patch false-positive burden and weak connectivity versus ABI-154. Reflective channels and Solar Geometry Input may help some SZA-aware variants but may also provide clutter-sensitive cues that make small non-contrail structures look line-like at the fixed threshold. A thermal-only BTD signed-detail decoder should force the model to use approved ABI channels 7-16, split-window/water-vapor/cloud-phase temperature differences, and patch-local signed thermal anomalies. This may improve source transfer, reduce negative-patch clutter, or recover connectivity without moving thresholding, Artifact Filters, losses, targets, sampling, or metrics into Candidate code.

## Comparison Target

Primary comparison targets are ABI-173 `run_20260901_234732_bd5917` and ABI-154 `run_20260901_071026_32d3ec`. ABI-173 reached capped filtered Dice 0.3962, MIT/Google filtered Dice 0.3838/0.4269, precision 0.4238, recall 0.3720, connectivity 0.3203, and filtered predicted-positive fraction 0.00318; its whole-validation diagnostic reached filtered Dice 0.3973 and documented elevated negative-patch false-positive burden. ABI-154 reached capped filtered Dice 0.3944, MIT/Google filtered Dice 0.3824/0.4260, precision 0.4777, recall 0.3359, connectivity 0.4374, and filtered predicted-positive fraction 0.00255.

Secondary references are ABI-068 `run_20260828_010836_4ccc77` as the broader aggregate/source-balance comparator, ABI-130 `run_20260831_121006_7d24be` as the SZA-aware ASPP/detail aggregate reference, and ABI-177 `run_20260902_035240_71e96b` as the recent recurrent-line negative result. Canonical MCAST summaries remain comparison context only, not promotion authority.

## Expected Effect

A useful result would complete finitely and non-degenerately, remain source-informative, and show whether removing reflective/SZA cues changes the false-positive/recall/connectivity tradeoff. A strong result would stay in the ABI-068/130/154/173 aggregate filtered-Dice band while improving at least one of MIT filtered Dice, connectivity, precision, or filtered predicted-positive fraction relative to ABI-173 without collapsing Google Dice. A negative result would show thermal-only evidence is insufficient for this architecture by falling clearly below the reference band, producing persistent prediction collapse, or trading away both recall and connectivity.

## Implementation Sketch

- Select provider-approved `abi_thermal_10ch` input, exposing only GOES ABI channels 7-16. Do not use Solar Geometry Input, longitude, latitude, reconstructed coordinates, Dataset Source identity, labels, predictions, or external data as features.
- Normalize thermal brightness temperatures using fixed constants derived from the trusted dataset profile's safe-range summary.
- Construct deterministic BTD planes from approved thermal channels only: ABI 13-14, 14-15, 13-15, 11-14, 7-14, 8-10, 8-13, and 9-14 differences, scaled in feature space.
- Add a learned 1x1 projection over normalized thermal channels only, then concatenate normalized channels, BTD planes, and learned thermal mixtures.
- Reuse a compact residual encoder, ASPP bottleneck, decoder, signed local/mid-scale detail stems, full-scale skip aggregation, and a conservative final thermal line calibrator with horizontal, vertical, diagonal/local, and broad context branches.
- Keep trusted `bce_dice` primary loss, trusted `weighted_bce` Centerline Target auxiliary weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant scheduler, disabled early stopping, and one sequential representative capped Run.
- Do not introduce candidate-owned thresholding, Artifact Filters, postprocessing, losses, target derivation, data loading, sampling implementation, augmentation implementation, scheduling, GPU placement, training loops, external persistence, runtime downloads, or pretrained weights.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_thermal_10ch`; only approved ABI channels 7-16 are used. Longitude, latitude, reconstructed coordinates, Dataset Source identity, and Solar Geometry Input are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data claim, Experiment Batch, Post-Run Evaluation, or promotion decision is requested in this handoff.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes inside the trusted runtime envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As input/preprocessing evidence, the result is useful if it improves false-positive discipline, connectivity, MIT Dice, or source balance relative to ABI-173 while remaining near the ABI-068/130/154/173 aggregate band, or if it cleanly shows thermal-only evidence is insufficient for this signed-detail ASPP branch.

## Continuation and hard stop

Continue this thermal-only signed-detail branch only if it is finite, non-degenerate, source-informative, and produces a diagnostically useful false-positive, connectivity, or source-balance difference from ABI-173/154. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. If it completes finite but simply loses both ABI-173 recall and ABI-154 precision/connectivity, stop this branch and broaden again to another in-contract architecture, data-policy, preprocessing, calibration, or evaluation frontier.

## Fallback/Next Decision

If the candidate fails from a narrow implementation defect while the thermal-only preprocessing hypothesis remains intact, consider at most one explicit Repair Candidate in a later Autonomy Step. If it is scientifically negative, document the result and avoid repeating thermal-only signed-detail ASPP unchanged. If it challenges ABI-068/130/154/173 or combines ABI-173-like aggregate Dice with better precision/connectivity/source balance, request separate whole-validation diagnostics before making any full-data or promotion claim.
