# ABI-150 Repair Proposal: finite-gradient structure-tensor ASPP/detail decoder

## Hypothesis

ABI-149 tested a full-spectral BTD+SZA ASPP/detail decoder with differentiable structure-tensor line evidence, but Run `run_20260901_034445_07ce82` failed during smoke testing with Harness-recorded `candidate_bug`: `non_finite_training_state` in `gradient.front_end.learned_mixer.0.weight` at the synthetic backward pass. The failure is consistent with an unstable zero-gradient path through the structure-tensor contrast calculation, where `sqrt(clamp(x, min=0))` can create non-finite derivatives when the Sobel energy is exactly zero.

ABI-150 is a **Repair Candidate / family-development repair**. It preserves ABI-149's hypothesis that explicit local line-coherence features can help the SZA-aware ASPP/detail decoder distinguish elongated contrail evidence from blob-like cloud clutter, while repairing only the finite-gradient structure-tensor calculation. It does not request new authority, losses, data access, postprocessing, thresholds, Artifact Filters, or resource policy changes.

## Comparison Target

The primary comparison target remains ABI-130 `abi130_fullspectral_btd_aspp_detail_decoder_sza_bce_dice_centerline_aux_v1`, Run `run_20260831_121006_7d24be`: capped filtered Dice 0.3953, MIT/Google filtered Dice 0.3779/0.4404, filtered precision 0.4415, filtered recall 0.3578, filtered connectivity 0.3851, and filtered predicted-positive fraction 0.00294.

Secondary references remain ABI-068 `run_20260828_010836_4ccc77` for local capped aggregate Dice and MIT/source balance, ABI-126 `run_20260831_085615_d05ab3` for ASPP/detail precision/connectivity, ABI-066 `run_20260827_230540_bf4ce3` for high-connectivity behavior, ABI-143 `run_20260831_224534_27b73d` for the best recent SZA-aware ridge-family BCE-Dice point, and ABI-149 `run_20260901_034445_07ce82` as the failed structure-tensor implementation being repaired. Canonical MCAST 2.1 remains full Working Validation Split promotion context only.

## Expected Effect

The expected repair effect is finite static/smoke/training behavior without changing the intended scientific operating point. Adding a small positive epsilon inside the structure-tensor contrast square root should remove the non-finite derivative path. Epsilon-stabilized denominators and bounded coherence/orientation/ridge features should prevent large gradients from low-energy synthetic or real patches while retaining line energy and orientation evidence.

If the repair works, ABI-150 should provide the missing interpretable representative capped evidence for the ABI-149 structure-tensor hypothesis. A useful scientific result would near-tie ABI-130 aggregate filtered Dice within about 0.005 while improving filtered connectivity, precision, positive-area discipline, MIT source balance, or late-epoch trajectory; improve aggregate filtered Dice over ABI-130; or provide clear negative evidence that explicit structure-tensor features do not help this SZA-aware BCE-Dice ASPP/detail branch.

## Implementation Sketch

- Reuse ABI-149's compact torch-only ABI-130-derived ASPP/detail encoder-decoder: normalized ABI spectral features, deterministic thermal BTD planes from approved ABI channels, normalized Solar Geometry Input features, learned 1x1 spectral projection, full-resolution detail/context stem, residual encoder, ASPP bottleneck, bilinear decoder fusions, high-resolution detail path, line-aware refinement, primary `mask_logits`, and auxiliary `centerline_logits`.
- Keep the differentiable structure-tensor front end, but repair the finite-gradient path: compute Sobel `gx`/`gy`, smoothed `jxx`/`jyy`/`jxy`, nonnegative trace, contrast as `sqrt(delta^2 + 4*jxy^2 + 1e-6)`, and ratio features using `trace + 1e-3` rather than a hard zero-adjacent denominator.
- Bound coherence to `[0, 1]`, orientation and diagonal balance to `[-1, 1]`, and ridge residual magnitude to a finite range before concatenation.
- Preserve trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision with trusted `weighted_bce` weight 0.02, `combined_source_balanced` traversal, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap.
- Request one sequential Run only; no Experiment Batch, candidate-owned scheduling, GPU placement, or resource retry is requested.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping.
- Repair lineage: original proposal/candidate ABI-149; motivating Run `run_20260901_034445_07ce82`; failure classification `candidate_bug`; original hypothesis and comparison target preserved.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, thresholding, postprocessing, resource limits, execution lifecycle, and prediction retention.
- Candidate code does not implement data loading, record selection, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, pretrained weights, runtime downloads, scheduling, GPU placement, external persistence, or coordinate-derived features.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data evidence, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. The ABI-149 non-finite gradient failure in `front_end.learned_mixer.0.weight` does not recur, and all losses, logits, gradients, parameters, metrics, and checkpoints remain finite.
3. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes without Resource Failure retry.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it near-ties ABI-130 aggregate filtered Dice while improving connectivity, precision, predicted-positive discipline, source balance, or late-epoch trajectory; improves aggregate filtered Dice over ABI-130; or supplies clear negative evidence about explicit structure-tensor features under SZA-aware BCE-Dice training.

## Continuation and hard stop

Continue only if ABI-150 is finite, non-degenerate, source-informative, and improves a meaningful ABI-130-relative diagnostic: aggregate Dice, connectivity, precision/recall balance, positive-area stability, MIT recall/source balance, or late-epoch trajectory. Stop this exact branch if the same non-finite smoke failure recurs, if a new persistent non-finite or prediction-collapse failure appears, if resource use exceeds the trusted envelope, or if a finite result is materially below ABI-130 on aggregate Dice without compensating precision/connectivity/source-balance gains. A negative finite result stops this exact structure-tensor ASPP/detail branch but does not eliminate structure-aware preprocessing or SZA-aware modeling globally.

## Fallback/Next Decision

If this repair fails because the stabilized structure-tensor calculation still creates non-finite gradients, classify the failure and stop this exact structure-tensor implementation rather than adding ad-hoc candidate-owned postprocessing or resource workarounds. If it completes finite but structure features trade away ABI-130's Google/calibration advantage or worsen connectivity, document that result and broaden to a different contract-compliant architecture, input/front-end, data-policy, augmentation, or calibration frontier. If it unexpectedly challenges ABI-068/ABI-130 or MCAST context, request separately authorized whole-validation diagnostics rather than claiming promotion from capped data.
