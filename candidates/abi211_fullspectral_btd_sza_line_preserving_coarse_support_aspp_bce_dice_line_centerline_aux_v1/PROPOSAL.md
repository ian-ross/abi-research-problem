# ABI-211 full-spectral BTD+SZA line-preserving coarse-support ASPP

## Proposal classification

**Family-development continuation.** ABI-211 continues the ABI-201/202 cross-scale directional-consensus ASPP family after recent local clutter-control probes showed mixed or negative tradeoffs. It is not a promotion claim and does not request the late-improving budget.

## Hypothesis

ABI-202 remains the strongest recent whole-validation aggregate filtered-Dice reference, but its diagnostics leave room for better false-positive discipline while preserving source-balanced recall and thin-line connectivity. Recent probes give a consistent lesson: foreground/boundary/support constraints can reduce predicted-positive area or raise precision, but when they act too close to the final mask or too broadly through support expansion they suppress MIT recall, Google performance, or connectivity.

A better in-contract continuation is to make coarse support a bounded feature-space cue while explicitly preserving the signed-detail/line stream. ABI-211 keeps the ABI-202 full-spectral BTD+SZA signed-detail ASPP decoder pattern but replaces the parent cross-scale directional consensus bridge with a lighter line-preserving coarse-support bridge. The bridge uses smoothed decoder/stem/full-scale features only as an additive support residual; it does not threshold, filter, postprocess, or zero the decoder/detail path. Reducing base width from 36 to 34 should offset bridge cost and keep the exploratory run within the near-timeout resource envelope.

## Comparison Target

Primary comparison target: ABI-202 `run_20260904_043143_ee0005`, the late36 cross-scale directional-consensus ASPP reference, with capped best `val/filtered_dice` 0.4276 at epoch 34 and whole-validation filtered Dice 0.4312, MIT/Google 0.4141/0.4644, precision 0.4431, recall 0.4199, and connectivity 0.4625.

Secondary comparison targets:

- ABI-201 `run_20260904_032624_7e855a`, the same-family 12-epoch exploratory parent, capped best filtered Dice 0.3958 with precision 0.4587, recall 0.3481, and connectivity 0.4630.
- ABI-203 `run_20260904_073913_3edd12`, foreground-calibrated head probe, capped best filtered Dice 0.4023 with improved MIT but weaker Google/connectivity than ABI-202.
- ABI-206 `run_20260904_105645_8f8ab1`, boundary auxiliary probe, which tightened area/precision but over-constrained MIT recall.
- ABI-210 `run_20260904_152018_ce1309`, compact spectral-ridge support probe, which completed but behaved as a recall-biased support expander with weak connectivity.
- ABI-184 `run_20260902_213856_2c04ac`, precision/connectivity and low-positive-area reference.

## Expected Effect

The expected signal is not immediate superiority over late36 ABI-202. A useful exploratory result would be finite, non-collapsed, and source-informative, with filtered Dice near or above the ABI-201/203 exploratory range while improving at least one of precision, filtered predicted-positive fraction, or connectivity without the recall/connectivity failures seen in ABI-206/208/210. Because the bridge is zero-initialized and bounded, early behavior should stay close to the parent decoder rather than introducing a new numerical or shape risk.

## Implementation Sketch

Start from the ABI-202 architecture and unchanged manifest policy. Keep provider-approved `abi_16ch_plus_sza` inputs, ABI channel normalization, deterministic BTD planes derived only from approved ABI channels, normalized/cosine Solar Geometry Input, signed local/mid-scale detail stems, residual encoder, ASPP context, full-scale skip fusion, line-aware final refinement, and primary plus Line/Centerline auxiliary heads.

Make architecture-only changes:

1. Replace `CrossScaleDirectionalConsensusBridge` with `LinePreservingCoarseSupportBridge`.
2. In that bridge, compute detail features from signed-detail local residuals, coarse support from smoothed decoder/stem/full-scale features, and a learned support gate from absolute feature disagreements.
3. Add only a bounded, zero-initialized residual to the decoder features; coarse support scales a support branch but cannot erase the decoder/detail stream.
4. Reduce base feature width from 36 to 34 to lower runtime/parameter risk under the exploratory timeout.

The candidate predicts no auxiliary support target and performs no data loading, target derivation, sampling, augmentation, loss computation, metric computation, thresholding, postprocessing, Artifact Filtering, coordinate reconstruction, runtime downloads, persistence writes, or resource scheduling.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.02, AdamW, learning rate 0.0003, batch size 4, manifest `max_epochs: 12`, and `constant_lr` scheduler.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, budget approval, and prediction retention.
- Candidate code defines model architecture only and contains no data loading, custom losses, custom metrics, Artifact Filters, postprocessing, thresholding, runtime downloads, filesystem persistence, Candidate-owned scheduling, or coordinate features.

## Budget Requested

One sequential exploratory capped Run: at most 1,024 training and validation ABI Patches per Dataset Source and Leakage-Safe Split, 12 effective epochs, batch size 4, 3,600-second Docker timeout, at most four Harness-selected `first_n` prediction artifacts, 25,000,000-parameter smoke ceiling, constant scheduler policy, disabled early stopping, and pinned A100 execution through the Harness. No late-improving budget is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and runtime stays within the exploratory 3,600-second wall-clock envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw/filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. The continuation is promising if it improves over ABI-201/203 on aggregate filtered Dice or offers a clearer precision/connectivity/positive-area tradeoff without large source-balanced recall loss.

## Fallback/Next Decision

If ABI-211 fails validation or smoke, classify the exact candidate-local issue before further action. If it exhausts wall-clock, treat this bridge as too expensive under the current exploratory budget and prefer a more compact scout rather than requesting a scheduling workaround. If it completes but repeats the ABI-206/208 pattern of low recall or the ABI-210 pattern of poor connectivity, do not request late36 for this exact branch. If it completes near ABI-202/203 with improved precision, connectivity, or area discipline and a late-improving source-balanced trajectory, write a Research Note and consider a future diagnostic or late-improving close continuation under the approved criteria.
