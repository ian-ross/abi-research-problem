# ABI-123: full-spectral BTD frequency-gated line U-Net with patch objectness gate

## Hypothesis

A neutral-initialized patch-level objectness gate on the current best full-spectral BTD frequency-gated line U-Net can reduce the widespread negative-patch clutter seen in whole-validation diagnostics while preserving ABI-068's line continuity and focal-Tversky recall. This is a family-development continuation, not a promotion claim; it tests whether global patch evidence can calibrate mask logits without candidate-owned thresholding, postprocessing, Artifact Filters, losses, sampling, metrics, or target derivation.

## Comparison Target

Primary comparison target: ABI-068 `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1` / `run_20260828_010836_4ccc77`, the local capped aggregate-Dice reference (best filtered Dice 0.3964, MIT 0.3886, Google 0.4161, precision 0.3992, recall 0.3936, connectivity 0.3900).

Secondary references: ABI-066 `run_20260827_230540_bf4ce3` for precision/connectivity behavior and ABI-121 whole-validation diagnostics for the negative-patch clutter failure mode.

## Expected Effect

The patch objectness gate should learn from global decoder features whether an ABI Patch contains credible contrail evidence and add a bounded negative log-bias when global evidence is weak. Because the gate is initialized near neutral, the expected early behavior is close to ABI-068 rather than a hard suppressor. A useful result would lower filtered predicted-positive fraction and/or improve precision while keeping aggregate filtered Dice within 0.01 of ABI-068 and avoiding MIT/Google source imbalance.

## Implementation Sketch

Start from ABI-068's normalized raw plus BTD front end, learned spectral mixer, frequency-split stem, encoder/decoder, frequency-pyramid fusion, focal-Tversky primary loss, and Centerline Target auxiliary head. Replace only the primary `mask_head` with `PatchObjectnessMaskHead`: a local 1x1 mask-logit head plus a small MLP over adaptive average and max pooled refined features. The MLP's final layer is zero-weighted with bias 4.0 so the sigmoid objectness gate starts at about 0.98; its log is added to local mask logits as an in-model calibration term.

## Contract Features Used

- Provider-approved `abi_16ch` ABI Channel Input only; no longitude, latitude, or reconstructed coordinate features.
- Candidate-owned code is limited to PyTorch model architecture and deterministic BTD combinations from approved channels.
- Trusted `focal_tversky` primary loss.
- Provider-derived `centerline` auxiliary target with `centerline_logits`, trusted `weighted_bce`, and weight 0.02.
- Trusted `combined_source_balanced` sampling and `random_mirroring` augmentation selected in the manifest.
- Harness-owned metrics, Artifact Filters, capped-record selection, scheduler, early-stopping state, resource placement, execution, and lifecycle.

## Budget Requested

Use the active Workspace Configuration ceilings: provider-selected representative cap of 1,024 train and validation records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, constant learning rate, disabled early stopping, 25M-parameter smoke ceiling, 3,600-second Docker training timeout, A100 execution, and four fixed first-n prediction artifacts. No concurrency or GPU placement is requested by candidate code.

## Success Criteria

Continue this branch if the run completes finitely and non-degenerately, stays under the parameter/time budget, keeps both MIT and Google filtered Dice above 0.36, and either (a) achieves aggregate filtered Dice within 0.01 of ABI-068 with improved precision or lower filtered predicted-positive fraction, or (b) improves aggregate filtered Dice over ABI-068 without a precision/connectivity collapse. Treat improved whole-validation diagnostic motivation as secondary unless capped metrics first justify it.

## Fallback/Next Decision

If the gate suppresses useful line evidence, lowers connectivity materially, causes all-negative collapse, or misses ABI-068 by more than about 0.02 aggregate filtered Dice without a clear precision/positive-area gain, stop this exact patch-objectness gate branch. Then broaden away from suppressive heads toward a different in-contract calibration mechanism or request targeted diagnostics only for a stronger capped candidate.
