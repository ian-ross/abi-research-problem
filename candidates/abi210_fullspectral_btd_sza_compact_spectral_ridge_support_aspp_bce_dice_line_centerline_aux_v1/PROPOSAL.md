# ABI-210 compact full-spectral BTD+SZA spectral-ridge support ASPP

## Proposal classification

**Family-development continuation / resource-safe reformulation.** ABI-210 continues the ABI-201/202 cross-scale directional-consensus ASPP family after ABI-209 failed with a Harness-recorded `resource_failure` caused by exhausting the 3,600-second exploratory wall-clock budget. It is not a promotion claim and does not request the late-improving budget.

## Hypothesis

ABI-202 remains the strongest cross-scale directional-consensus ASPP reference, with useful source-balanced recall and connectivity, but its whole-validation diagnostic showed room for better precision and predicted-positive discipline. ABI-209 tested representation-level spectral-ridge support and produced finite partial validation through epoch 11, including a best observed epoch-9 filtered Dice of about 0.3695 and high-precision epoch-7 behavior, but the full candidate did not fit the exploratory wall-clock envelope.

A compact spectral-ridge support bridge can preserve the scientific question while making the resource profile safe: keep ABI-202's approved full-spectral BTD+SZA, signed-detail, ASPP, full-scale skip, and cross-scale consensus structure; retain the spectral/ridge feature-space support cue; but reduce activation width and the support-bridge smoothing cost so the run can complete 12 epochs. If the compact bridge still improves precision or positive-area discipline without the severe recall/connectivity loss seen in ABI-204/206/208, then spectral/ridge representation support remains worth developing. If it completes but stays far below ABI-202/203, the result argues against this local clutter-control branch rather than against the broader ABI-202 family.

## Comparison Target

Primary comparison target: ABI-202 `run_20260904_043143_ee0005`, the late36 cross-scale directional-consensus ASPP reference, with capped best `val/filtered_dice` 0.4276 at epoch 34 and whole-validation filtered Dice 0.4312, MIT/Google 0.4141/0.4644, precision 0.4431, recall 0.4199, and connectivity 0.4625.

Secondary comparison targets:

- ABI-209 `run_20260904_141405_62591c`, the resource-failed full-width spectral-ridge support attempt, for resource and partial-trajectory comparison only.
- ABI-203 `run_20260904_073913_3edd12`, foreground-calibrated head probe, capped best filtered Dice 0.4023 with precision 0.4332 and recall 0.3756.
- ABI-204 `run_20260904_084637_a1c72c` and ABI-206 `run_20260904_105645_8f8ab1`, negative support/boundary probes that reduced area or increased precision at excessive recall/connectivity cost.
- ABI-184 `run_20260902_213856_2c04ac`, precision/connectivity and low-positive-area reference.

## Expected Effect

The first requirement is operational: complete static validation, smoke, and the 12-epoch capped exploratory Run inside the Harness resource envelope. Scientifically, a useful signal would be a finite, non-collapsed, source-informative trajectory with lower filtered predicted-positive fraction or higher precision than ABI-202/203 while retaining substantially more recall/connectivity than ABI-204/206/208. Because compacting may reduce representational capacity, improvement over ABI-202 is not required for this exploratory run; completing near ABI-203 with better positive-area discipline would be enough to justify a note or diagnostic decision.

## Implementation Sketch

Start from ABI-209's architecture-only source, which itself started from ABI-202. Keep provider-approved `abi_16ch_plus_sza` input, normalization of ABI channels 1-16, deterministic BTD planes derived only from approved ABI channels, normalized and cosine Solar Geometry Input, signed local/mid-scale detail stems, residual encoder, ASPP context, full-scale skip fusion, `CrossScaleDirectionalConsensusBridge`, `SpectralRidgeSupportBridge`, line-aware final refinement, and primary plus Line/Centerline auxiliary heads.

Make only resource-safety changes inside model architecture:

1. Reduce learned front-end projection width from 16 to 12 channels.
2. Reduce base feature width from 36 to 32 channels across stem, encoder, decoder, full-scale fusion, consensus, support, refinement, and heads.
3. Replace the spectral-support bridge's broad full-scale smoothing window from 31 to 15 pixels, keeping it a representation feature and not a postprocessor.

The candidate still predicts no auxiliary support target and performs no thresholding, postprocessing, Artifact Filtering, data loading, target derivation, sampling, augmentation, loss computation, metric computation, coordinate reconstruction, runtime downloads, persistence writes, or resource scheduling.

Keep manifest policy unchanged from the in-contract ABI-202/209 family: trusted `bce_dice`, `combined_source_balanced`, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, constant scheduler, disabled early stopping, manifest `max_epochs: 12`, and provider-derived Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.02, AdamW, learning rate 0.0003, batch size 4, manifest `max_epochs: 12`, and `constant_lr` scheduler.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, budget approval, and prediction retention.
- Candidate code defines model architecture only and contains no data loading, custom losses, custom metrics, Artifact Filters, postprocessing, thresholding, runtime downloads, filesystem persistence, Candidate-owned scheduling, or coordinate features.

## Budget Requested

One sequential exploratory capped Run: at most 1,024 training and validation ABI Patches per Dataset Source and Leakage-Safe Split, 12 effective epochs, batch size 4, 3,600-second Docker timeout, at most four Harness-selected `first_n` prediction artifacts, 25,000,000-parameter smoke ceiling, constant scheduler policy, disabled early stopping, and pinned A100 execution through the Harness. No late-improving budget is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and runtime stays within the exploratory 3,600-second wall-clock envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. The continuation is promising if it improves on the resource-failed ABI-209 completion state, approaches ABI-203's aggregate filtered Dice with better precision/positive-area discipline, or shows a late-improving, source-balanced trajectory near epoch 12.

## Fallback/Next Decision

If ABI-210 fails validation or smoke, classify the exact candidate-local implementation issue before any further action. If it again exhausts wall-clock, treat spectral-ridge support at this resolution as too expensive under the current exploratory budget and broaden away from this branch rather than requesting a scheduling workaround. If it completes but shows ABI-204/206/208-style recall or connectivity suppression, do not request late36 and move to a broader architecture, training/data/loss-policy, or evaluation frontier. If it completes with useful precision/area discipline near ABI-203 or a clearly late-improving trajectory, write a Research Note and consider a future whole-validation failure-bucket evaluation or late-improving close continuation only if the approved criteria are met.
