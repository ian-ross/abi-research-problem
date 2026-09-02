# ABI-177 Full-Spectral BTD+SZA Recurrent Line-Refinement ASPP Decoder BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-176 stopped the local signed context-fusion branch: it improved precision and Google Dice but reduced aggregate Dice, MIT Dice, recall, and connectivity relative to ABI-173. ABI-173 remains the strongest whole-validation-tested SZA-aware ASPP/detail aggregate branch, ABI-154 remains the SZA-aware precision/connectivity reference, ABI-130 remains the prior SZA-aware ASPP/detail aggregate reference, and ABI-068 remains the broader capped aggregate/source-balance comparator. ABI-177 broadens beyond another signed-detail/full-scale fusion patch by testing a recurrent, non-thresholded line-propagation decoder with a compact thermal-anchor support branch.

## Hypothesis

Recent SZA-aware ASPP/detail variants often trade recall, precision, and connectivity through one-shot fusion or suppressive gates. ABI-176 suggested that broader context can reduce clutter but also weakens MIT recall and thin-line continuity. A shared recurrent line-refinement head may let the model propagate coherent horizontal, vertical, and diagonal/local line evidence over multiple additive feature updates while a thermal-anchor branch supplies conservative cloud/ice support. This should recover connectivity and recall without candidate-owned thresholding, Artifact Filters, or postprocessing.

## Comparison Target

Primary comparison targets are ABI-173 `run_20260901_234732_bd5917` and ABI-176 `run_20260902_025056_9e87d5`. ABI-173 reached capped filtered Dice 0.3962, MIT/Google filtered Dice 0.3838/0.4269, precision 0.4238, recall 0.3720, connectivity 0.3203, and predicted-positive fraction 0.00318. ABI-176 reached capped filtered Dice 0.3902, MIT/Google filtered Dice 0.3739/0.4300, precision 0.4377, recall 0.3519, connectivity 0.2866, and predicted-positive fraction 0.00291.

Secondary references are ABI-154 `run_20260901_071026_32d3ec` as the high-precision/high-connectivity SZA-aware full-scale skip branch, ABI-130 `run_20260831_121006_7d24be` as the prior SZA-aware ASPP/detail aggregate reference, ABI-174/175 as negative local signed-detail follow-ups, and ABI-068 `run_20260828_010836_4ccc77` as the broader capped aggregate/source-balance comparator. Canonical MCAST summaries remain context only.

## Expected Effect

A useful outcome would remain finite, non-degenerate, and in the ABI-130/154/173 aggregate band while improving at least one of connectivity, recall, or source balance relative to ABI-176. A strong outcome would approach ABI-173 aggregate filtered Dice while increasing connectivity toward ABI-154/068 levels and keeping both Dataset Source filtered Dice values above roughly 0.38. A negative outcome would either repeat the recent conservative failure mode with lower recall/MIT Dice, create permissive positive-area clutter without overlap gain, or exceed the runtime envelope.

## Implementation Sketch

- Reuse the approved `abi_16ch_plus_sza` front end: normalized GOES ABI channels 1-16, deterministic thermal BTD planes from approved ABI channels only, normalized SZA, cosine SZA, and a learned 1x1 projection over provider-approved input channels.
- Use a compact residual encoder plus ASPP bottleneck and decoder over the full front-end features.
- Add a separate `ThermalAnchorSupport` branch that slices only normalized thermal ABI features, deterministic BTD planes, and Solar Geometry features from the approved front end, then produces a compact support feature map. It does not receive longitude, latitude, Dataset Source identity, labels, or predictions.
- Replace the recent signed-detail/fusion patch with `RecurrentLineRefinement`: three shared additive update steps combining the decoder state, thermal-anchor support, broad context, horizontal strip evidence, vertical strip evidence, and diagonal/local line evidence. The updates are bounded by `tanh` and added in feature space before normal primary and auxiliary heads.
- Keep trusted `bce_dice` primary loss, trusted `weighted_bce` Centerline Target auxiliary weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant scheduler, disabled early stopping, and one sequential representative capped Run.
- Do not introduce candidate-owned thresholding, Artifact Filters, postprocessing, losses, target derivation, data loading, sampling implementation, augmentation implementation, scheduling, GPU placement, training loops, external persistence, runtime downloads, or pretrained weights.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
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
6. As family-development evidence, the result is useful if it improves connectivity, recall, or source balance relative to ABI-176 without falling clearly below the ABI-130/154/173 aggregate band.

## Continuation and hard stop

Continue this recurrent line-refinement branch only if it is finite, non-degenerate, source-informative, and shows a diagnostically useful connectivity/recall/source-balance difference from ABI-173/176. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. If it completes finite but simply repeats a conservative or clutter-forward regression, stop this branch and broaden again to another in-contract architecture, data-policy, preprocessing, calibration, or evaluation frontier.

## Fallback/Next Decision

If the candidate fails from a narrow implementation defect while the recurrent line-refinement hypothesis remains intact, consider at most one explicit Repair Candidate in a later Autonomy Step. If it is scientifically negative, document the result and avoid further local recurrent refinements unless new diagnostics identify a fixable failure mode. If it challenges ABI-068/130/154/173 or combines ABI-173-like aggregate Dice with improved connectivity/source balance, request separate whole-validation diagnostics before making any full-data or promotion claim.
