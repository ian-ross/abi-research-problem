# ABI-225 temporal five-frame attention/difference U-Net google-only repair

## Hypothesis

ABI-224 attempted the next temporal-family broadening step after ABI-223: replace the successful three-frame temporal-attention window `[-1, 0, 1]` with the allowlisted five-frame window `[-2, -1, 0, 1, 2]` while retaining compact attention/difference fusion. The Run failed before training because the trusted provider reported no MIT samples available for the five-frame temporal-eligible center population under `combined_source_balanced` sampling. This is a narrow repair of that manifest-level Candidate bug.

The scientific hypothesis is unchanged for the available five-frame population: wider provider-owned temporal context may expose persistence/advection evidence that improves thin-line recall or continuity relative to three-frame temporal attention. Because the repaired population is Google-only, this is **family scout / repair feasibility evidence**, not a source-balanced promotion candidate.

## Comparison Target

The immediate failed parent is ABI-224, Run `run_20260908_172818_76b0fc`. The temporal-family comparison target is ABI-223, Run `run_20260908_154531_8c7e2b`, which reached capped best `val/filtered_dice` 0.419776 at epoch 36 with Google filtered Dice 0.476764, filtered precision 0.483764, filtered recall 0.370738, and filtered connectivity 0.412427 on the three-frame `[-1, 0, 1]` source-balanced temporal-eligible population. Additional context is ABI-222, Run `run_20260908_150315_9aea3f`, with Google filtered Dice 0.416510 at 12 epochs, and ABI-218, Run `run_20260908_123030_05ad37`, as the matched temporal-eligible single-frame control with Google filtered Dice 0.385184.

ABI-202 remains the mature single-frame whole-validation frontier context only. ABI-225 cannot make a source-balanced or whole-validation promotion claim because it intentionally uses `google_only` sampling to match the provider-available five-frame population.

## Expected Effect

If longer temporal context contains useful persistence/advection evidence, the repaired five-frame scout should complete finitely and improve Google filtered Dice, filtered recall, or Contrail Connectivity relative to the 12-epoch temporal-family controls, without expanding predicted-positive fraction into a low-precision regime. Even if it does not beat ABI-223's late36 Google metric, it can establish whether the five-frame architecture/input is resource-safe and worth a future trusted source-availability or source-balanced follow-up.

## Implementation Sketch

Reuse the ABI-224 model unchanged except for the candidate identifier: reshape the provider-stacked tensor into five 17-channel ABI+SZA frames in ascending offset order; build bounded normalized ABI channels, ABI-derived thermal BTD planes, scaled SZA, and cosine SZA features per frame; project frames with shared weights; score each frame against the center embedding with per-pixel temporal attention; fuse attended evidence with near/far signed and absolute temporal-difference features; and decode through a compact U-Net/ASPP module to `mask_logits`, `line_logits`, and `centerline_logits`.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal` with provider-owned temporal provisioning.
- `data.frame_selection_policy: temporal_eligible_center`.
- `data.temporal_frame_offsets: [-2, -1, 0, 1, 2]` from the allowlisted temporal windows.
- `data.sampling_policy: google_only`, the narrow repair for the provider-reported no-MIT five-frame eligible population.
- `data.augmentation_policy: random_mirroring`.
- `training.loss: bce_dice`, `optimizer: adamw`, `scheduler.policy: constant_lr`.
- Trusted Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02.

The Candidate code defines architecture only. It does not implement data loading, temporal lookup, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy implementation, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Budget Requested

Use the exploratory/default budget: 12 epochs, batch size 2, constant learning rate 0.0003, disabled early stopping, and the current Harness-owned sample/resource ceilings. No `late_improving` budget is requested because this is a repaired five-frame scout with changed eligible population and unprofiled five-frame resource behavior. Run sequentially.

## Success Criteria

Treat ABI-225 as useful repaired five-frame evidence if it completes within resource limits with finite, noncollapsed predictions and source-appropriate metrics. Positive signs include Google filtered Dice above the ABI-218 single-frame control and/or ABI-222 12-epoch attention metric, improved Google filtered recall or connectivity, and modest predicted-positive fraction. A lower but finite Result can still be useful resource evidence for the five-frame branch; a collapse, non-finite state, or failure to learn on Google-only data should stop this exact repair branch.

## Fallback/Next Decision

If ABI-225 fails for a Candidate code issue, classify the failure before attempting any further repair. If it fails because five-frame temporal eligibility/sampling remains unavailable even for Google-only, write a Capability Request for trusted per-source temporal eligibility disclosure rather than guessing at data policy. If it completes and is competitive on Google-only metrics, a later step may request either trusted source-availability diagnostics or a separate source-comparable control; do not promote from this repaired google-only capped scout alone.
