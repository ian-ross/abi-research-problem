# ABI-153 Full-Spectral BTD+SZA Soft Ridge-Gate U-Net clDice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-143 produced a finite, non-collapsed SZA-aware ridge-family result within the current capped reference band, but its soft-gate BCE-Dice operating point traded away much of ABI-142/ABI-126/ABI-066 connectivity. ABI-153 keeps the ABI-143 architecture, input mode, auxiliary target, data policy, optimizer, learning rate, batch size, and epoch budget fixed while changing only the trusted primary loss from `bce_dice` to `bce_dice_cldice`.

## Hypothesis

The ABI-143 soft ridge-gate helped MIT recall and kept aggregate filtered Dice close to ABI-068/ABI-130, but its lower filtered connectivity suggests the BCE-Dice objective did not sufficiently reward thin-line continuity in the ridge-aware SZA branch. The allowlisted `bce_dice_cldice` primary loss should add trusted continuity pressure without moving line processing into candidate-owned postprocessing. If the architecture's ridge evidence is useful, the loss change may recover filtered connectivity or precision/connectivity balance while preserving ABI-143's finite trajectory and source-informative behavior.

## Comparison Target

The primary comparison target is ABI-143, Run `run_20260831_224534_27b73d`: capped filtered Dice 0.3947, MIT/Google filtered Dice 0.3815/0.4287, filtered precision 0.4105, filtered recall 0.3801, filtered connectivity 0.3010, and filtered predicted-positive fraction 0.00336. Secondary references are ABI-142 `run_20260831_215104_d4c318` for the ridge-attention BCE-Dice scout with better connectivity, ABI-130 `run_20260831_121006_7d24be` for the SZA-aware ASPP/detail near-reference branch, ABI-126 `run_20260831_085615_d05ab3` and ABI-066 `run_20260827_230540_bf4ce3` for high-precision/connectivity behavior, and ABI-068 `run_20260828_010836_4ccc77` as the local capped aggregate-Dice reference. Canonical MCAST 2.1 remains the full Working Validation Split promotion context; ABI-153 requests only capped family-development evidence.

## Expected Effect

A useful result would train finitely and keep the ridge-family branch in the ABI-142/ABI-143 capped band while improving filtered connectivity, precision/connectivity balance, or positive-area discipline. The targeted improvement is not merely higher recall: ABI-153 should avoid the diffuse-clutter failure mode seen in several recall-forward branches. The clDice term may lower aggregate Dice if it over-regularizes thin lines or conflicts with the centerline auxiliary head; that outcome would be informative hard-stop evidence for this exact loss swap but would not eliminate ridge-aware SZA modeling broadly.

## Implementation Sketch

- Reuse ABI-143's torch-only compact SZA-aware ridge-attention U-Net: normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized SZA and `cos(SZA)`, learned 1x1 approved-channel mixture, early ridge/context/detail stem, three-level encoder/decoder, dilated bottleneck context, high-resolution ridge path, and neutral-initialized conservative final ridge gate bounded near identity.
- Use provider-approved `abi_16ch_plus_sza` input only; exclude longitude, latitude, reconstructed coordinates, and Dataset Source identity.
- Emit exactly the primary `mask_logits` and provider-declared auxiliary `centerline_logits` outputs.
- Change only the trusted primary loss in `manifest.yaml` from `bce_dice` to `bce_dice_cldice`.
- Preserve provider-derived Centerline Target `weighted_bce` auxiliary loss at weight 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.
- Request one sequential Run only; no Experiment Batch, candidate-owned resource scheduling, custom loss, target derivation, thresholding, Artifact Filter, or postprocessing is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, primary loss `bce_dice_cldice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, thresholding, postprocessing, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, or external persistence.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data evidence, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains below the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As ridge-family continuation evidence, the branch is useful if it ties ABI-143 within about 0.007 aggregate filtered Dice while improving filtered connectivity by at least about 0.04, improves precision/connectivity balance at similar recall, improves positive-area discipline without collapsing recall, or otherwise lands near ABI-068/ABI-130 with a distinctive source/connectivity trade-off.

## Continuation and hard stop

Stop this exact loss-swap branch for hard execution failure, persistent non-finite behavior, persistent all-negative or all-positive prediction collapse, clear optimization failure, severe Dataset Source-specific collapse, or resource failure outside the trusted envelope. Also stop the exact branch if it is finite but materially worse than ABI-143/ABI-142 without a connectivity, precision, source-balance, positive-area, or late-trajectory advantage. If it improves connectivity while remaining in the current capped reference band, a later Autonomy Step may request whole-validation diagnostics or propose a more focused in-contract continuation. Do not claim promotion from capped evidence.

## Fallback/Next Decision

If ABI-153 fails because of a narrow implementation defect while the controlled loss-swap hypothesis remains intact, prepare at most one explicit Repair Candidate in a later Autonomy Step. If it completes finite but clDice over-regularizes the SZA ridge branch or repeats prior clDice underperformance, write a Research Note and broaden to a distinct architecture, data-policy, calibration, or preprocessing/front-end frontier rather than repeating simple loss swaps. If it unexpectedly improves capped aggregate/source/connectivity behavior versus ABI-143 and remains competitive with ABI-068/ABI-130, request separately authorized whole-validation diagnostics before any promotion interpretation.
