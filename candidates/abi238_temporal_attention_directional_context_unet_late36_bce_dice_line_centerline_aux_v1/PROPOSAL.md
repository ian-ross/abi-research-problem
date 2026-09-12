# ABI-238 temporal-attention directional-context U-Net late-improving continuation

## Hypothesis

ABI-223 showed that provider-owned three-frame temporal attention can become competitive under the approved late-improving budget, but it still trailed ABI-202 on capped filtered Dice, recall, MIT Dice, and connectivity. A small full-resolution directional-context bridge after the ABI-223 decoder may preserve ABI-223's temporal precision and Google strength while improving thin-line continuity and recall through architecture-internal horizontal, vertical, and dilated diagonal context. This is a family-development continuation of the successful ABI-223 temporal-attention branch, not a promotion claim.

## Comparison Target

The primary parent and comparison target is ABI-223 (`run_20260908_154531_8c7e2b`), whose best/final epoch 36 reached capped `val/filtered_dice` 0.419776, raw Dice 0.438487, filtered precision 0.483764, filtered recall 0.370738, MIT filtered Dice 0.398498, Google filtered Dice 0.476764, and filtered connectivity 0.412427. ABI-202 (`run_20260904_043143_ee0005`) remains the mature single-frame frontier context, with capped filtered Dice 0.427570, higher recall and connectivity, and whole-validation filtered Dice 0.4312. Earlier temporal context includes ABI-222 at 0.374329 filtered Dice and the matched temporal-eligible single-frame control ABI-218 at 0.345570.

## Expected Effect

The expected effect is a modest but diagnostic temporal-family improvement: recover some of ABI-223's remaining recall/connectivity gap without losing its high precision, temporal-family source balance, or resource safety. Useful outcomes include a capped filtered-Dice gain over ABI-223, higher filtered recall at similar precision, stronger MIT Dice, improved connectivity, or clear evidence that adding high-resolution orientation context to this temporal branch does not help and the campaign should pivot to a different temporal mechanism or non-temporal frontier.

## Implementation Sketch

Start from ABI-223's finite temporal-attention fusion U-Net. The model consumes only the provider-advertised `abi_16ch_plus_sza_temporal` tensor with offsets `[-1, 0, 1]`, builds bounded ABI/SZA/BTD features per frame, applies shared per-frame projection, computes per-pixel temporal attention around the center frame, fuses bounded change embeddings, and decodes through the same compact U-Net/ASPP path. ABI-238 adds one residual `HighResolutionDirectionalContext` block after the final decoder/refinement stage. That block uses depthwise horizontal and vertical strip convolutions plus dilated local context branches, gates their fused directional evidence, and adds it back to the full-resolution feature map before the trusted `mask_logits`, `line_logits`, and `centerline_logits` heads.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal` with provider-owned temporal provisioning.
- `data.frame_selection_policy: temporal_eligible_center`.
- `data.temporal_frame_offsets: [-1, 0, 1]`.
- `data.sampling_policy: combined_source_balanced`.
- `data.augmentation_policy: random_mirroring`.
- `training.loss: bce_dice`, `optimizer: adamw`, `scheduler.policy: constant_lr`.
- Trusted Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02.
- Candidate-local `budget_request.yaml` requesting approved `late_improving` budget class with `requested_max_epochs: 36` and parent Run `run_20260908_154531_8c7e2b`.

The Candidate code defines architecture only. It does not implement data loading, temporal lookup, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Budget Requested

Request the approved `late_improving` budget: 36 epochs and the trusted late-improving wall-clock limit, with fallback to the exploratory budget if denied. ABI-223's best checkpoint occurred at the final approved epoch, and ABI-238 is a close continuation with only a small architecture-internal directional-context bridge. The manifest retains `max_epochs: 12` because the Harness-owned budget request, not Candidate code, authorizes any extension. Keep batch size 2, constant learning rate 0.0003, disabled early stopping, and the current Harness-owned sample/resource ceilings.

## Success Criteria

Treat ABI-238 as useful if it completes finitely and either improves ABI-223 capped `val/filtered_dice` by at least about 0.005, or preserves ABI-223-level Dice while improving at least two of filtered recall, MIT filtered Dice, filtered connectivity, or positive-fraction stability without material precision collapse. A result approaching or exceeding ABI-202 capped filtered Dice with source-informative behavior would justify a later trusted diagnostic; lower Dice but improved connectivity/recall may still guide temporal-family development.

## Fallback/Next Decision

If the late-improving request is denied, treat the exploratory-budget Run as the valid bounded result. If ABI-238 fails due to Candidate code, create at most one narrow repair of the directional-context block. If it completes but degrades ABI-223's precision/recall/source balance or shows no useful trajectory, stop this exact high-resolution directional-context branch and broaden to a different temporal mechanism, calibration/uncertainty architecture, or modern lightweight backbone rather than repeating local context tweaks.
