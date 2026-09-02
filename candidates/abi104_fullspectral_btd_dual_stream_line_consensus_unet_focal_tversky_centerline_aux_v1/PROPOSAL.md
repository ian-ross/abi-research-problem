# ABI-104 full-spectral BTD dual-stream line-consensus U-Net

## Hypothesis

ABI-103 showed that separating reflective ABI channels, thermal ABI channels, and deterministic thermal BTD planes before fusion is feasible and can keep recall alive, but its selected checkpoint had low precision and weak Contrail Connectivity Metric: filtered Dice 0.3305, filtered precision 0.2715, filtered recall 0.4225, filtered connectivity 0.1742, MIT filtered Dice 0.3248, and Google filtered Dice 0.3427. ABI-068 remains the capped aggregate-Dice reference at filtered Dice 0.3964, while ABI-066 remains the precision/connectivity reference at filtered precision 0.4427 and connectivity 0.4731.

ABI-104 is a **family-development continuation** of the ABI-103 dual-stream spectral-specialization scout. It keeps ABI-103's in-contract spectral separation but strengthens the final full-resolution decoder. The hypothesis is that a consensus-gated line decoder can retain ABI-103's recall-forward spectral evidence while suppressing blob-like clutter and improving line continuity, without candidate-owned thresholding, postprocessing, Artifact Filters, losses, metrics, sampling, or data loading.

## Comparison Target

Primary local target: ABI-103, `abi103_fullspectral_btd_dual_stream_spectral_gate_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260830_074456_5e0e5c`, because ABI-104 directly tests whether a stronger line-consensus decoder repairs ABI-103's low-precision/low-connectivity failure mode.

Secondary local targets: ABI-068, Run `run_20260828_010836_4ccc77`, as the current capped aggregate-Dice frequency-gated reference, and ABI-066, Run `run_20260827_230540_bf4ce3`, as the precision/connectivity reference. ABI-102 and ABI-103 are context for recent spectral/modern-block scouts that were finite but below target. Canonical MCAST 2.1 remains the full Working Validation Split promotion context; this continuation requests only capped representative evidence.

## Expected Effect

The consensus-gated line decoder is expected to:

- increase filtered precision relative to ABI-103 by requiring high-resolution detail, smoothed context, and oriented line branches to agree in feature space;
- improve Contrail Connectivity Metric relative to ABI-103 by using wider horizontal/vertical line branches and a broad dilated branch at full resolution;
- preserve much of ABI-103's recall benefit through trusted focal-Tversky loss and non-hard, continuous feature gating initialized around a neutral scale;
- remain diagnostically distinct from ABI-068/066 because it tests spectral-specialization plus decoder-level line consensus rather than another small output head, sampling-policy change, or learning-rate tweak;
- remain within the current resource envelope by reducing base width from ABI-103 while adding the consensus refinement block.

## Implementation Sketch

The candidate uses provider-approved `abi_16ch` input only. Candidate code normalizes the 16 approved ABI channels with bounded constants from the dataset profile and constructs deterministic thermal BTD planes from approved ABI channels only. A reflective stem consumes ABI channels 1-6, a thermal stem consumes ABI channels 7-16, and a BTD stem consumes selected approved-channel thermal differences. Bounded cross-stream gates fuse these streams before a compact residual U-Net with low-frequency-gated skip fusion and dilated line context.

ABI-104 changes ABI-103's final refinement by using a consensus-gated line decoder. It first forms a full-resolution multi-scale consensus tensor, then derives high-pass detail, smoothed context, horizontal line evidence, vertical line evidence, and broad dilated evidence. A learned soft orientation weighting and a continuous support gate refine the features before the primary and centerline heads. The support gate is internal differentiable architecture, not thresholding or postprocessing. The model emits primary `mask_logits` and provider-derived `centerline_logits`.

The manifest uses trusted `focal_tversky`, trusted `random_mirroring`, provider-owned `combined_source_balanced` traversal, AdamW learning rate 0.0003, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and a trusted provider-derived `centerline` auxiliary target with `weighted_bce` weight 0.02. No candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, threshold selection, Artifact Filters, postprocessing, filesystem writes, network calls, pretrained weights, or training loop logic are introduced. The model does not receive longitude, latitude, or reconstructed coordinate inputs.

## Contract Features Used

- Input mode: `abi_16ch` only; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target emitted as `centerline_logits` with trusted `weighted_bce` at weight 0.02.
- Primary loss: trusted `focal_tversky`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping under the current Workspace Configuration.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch, extra concurrency, GPU selection, data-policy change, or full-data promotion evaluation is requested.

## Success Criteria

Useful family-development evidence would be any of:

- improve ABI-103 aggregate capped best `val/filtered_dice` by at least 0.025 while keeping both Dataset Sources above 0.32 filtered Dice;
- improve ABI-103 filtered precision by at least 0.04 or filtered connectivity by at least 0.08 without dropping recall below 0.36;
- reach within 0.03 capped filtered Dice of ABI-068 with a distinctive precision/connectivity or source-balance advantage;
- show a late-improving, non-collapsed trajectory that keeps filtered predicted-positive fraction below ABI-103's 0.00564 while improving at least one of Dice, precision, or connectivity.

Hard stop evidence for this exact continuation would be smoke failure, non-finite behavior, persistent all-negative/all-positive prediction collapse, aggregate filtered Dice below 0.30 with no late improvement, either Dataset Source below 0.25 filtered Dice, or a low-precision/high-positive-area regime that fails to improve ABI-103's failure mode.

## Fallback/Next Decision

If ABI-104 improves ABI-103's precision/connectivity while preserving recall and source balance, consider one bounded follow-up that tunes the same consensus mechanism or request targeted diagnostics only if it approaches ABI-068/066. If ABI-104 remains finite but still low in precision/connectivity, treat the dual-stream spectral-specialization branch as insufficient without a materially different decoder and broaden the frontier. If it fails contract validation or smoke testing, classify the failure and repair only if the original spectral-specialization plus line-consensus hypothesis is preserved. Do not move provider-owned thresholding, Artifact Filters, data loading, sampling, augmentation, target derivation, losses, metrics, resource placement, or lifecycle behavior into Candidate code.
