# ABI-223 temporal-attention fusion U-Net late-improving continuation

## Hypothesis

ABI-222's compact temporal-attention fusion U-Net was still improving at the final exploratory epoch after oscillating between precision- and recall-oriented checkpoints. A longer approved `late_improving` budget can test whether the same provider-owned three-frame temporal-attention mechanism stabilizes into a better source-balanced recall/precision operating point without changing architecture, input authority, loss, augmentation, sampling, scheduler, thresholding, or postprocessing. This is a family-development continuation of ABI-222, not a promotion candidate against the mature ABI-202 frontier.

## Comparison Target

The primary parent and comparison target is ABI-222 (`run_20260908_150315_9aea3f`), whose best capped checkpoint was epoch 12 with `val/filtered_dice` 0.374329, raw Dice 0.392066, filtered precision 0.466148, filtered recall 0.312729, MIT filtered Dice 0.357658, Google filtered Dice 0.416510, and filtered connectivity 0.281396. Temporal-family context includes ABI-220 (`run_20260908_134203_8bbb6f`, best filtered Dice 0.368730), ABI-219 (`run_20260908_130608_80d612`, best 0.367589), ABI-221 (`run_20260908_142018_0ea94f`, best 0.363826), and the matched single-frame temporal-eligible control ABI-218 (`run_20260908_123030_05ad37`, best 0.345570). ABI-202 remains the current mature whole-validation-tested frontier context only.

## Expected Effect

The expected effect is not a structural architecture gain; it is a training-budget test for a late-improving temporal branch. If ABI-222 was truncated, additional trusted epochs should improve or clarify `val/filtered_dice`, reduce epoch-to-epoch precision/recall oscillation, and preserve the controlled margin over ABI-218. Useful outcomes include higher filtered Dice than ABI-222, improved filtered recall without a material precision collapse, stronger MIT/Google balance, or a clear plateau/overfit signal that tells the campaign to broaden to five-frame temporal modeling instead of continuing three-frame attention tuning.

## Implementation Sketch

Reuse ABI-222's `model.py` architecture exactly except for the Candidate identifier. The model consumes only the provider-advertised `abi_16ch_plus_sza_temporal` tensor with offsets `[-1, 0, 1]`, reshapes the channel-stacked tensor into three ABI+SZA frames, constructs bounded finite ABI/SZA/BTD features for each frame, applies shared per-frame projection, computes per-pixel temporal-attention weights relative to the center frame, fuses the attended temporal embedding with bounded signed/absolute change embeddings, and decodes through the same compact U-Net/ASPP path with `mask_logits`, `line_logits`, and `centerline_logits` heads.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal` with provider-owned temporal provisioning.
- `data.frame_selection_policy: temporal_eligible_center`.
- `data.temporal_frame_offsets: [-1, 0, 1]`.
- `data.sampling_policy: combined_source_balanced`.
- `data.augmentation_policy: random_mirroring`.
- `training.loss: bce_dice`, `optimizer: adamw`, `scheduler.policy: constant_lr`.
- Trusted Line and Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02.
- Candidate-local `budget_request.yaml` requesting approved `late_improving` budget class with `requested_max_epochs: 36` and parent Run `run_20260908_150315_9aea3f`.

The Candidate code defines architecture only. It does not implement data loading, temporal lookup, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Budget Requested

Request the approved `late_improving` budget: 36 epochs and the trusted late-improving wall-clock limit, with fallback to the exploratory budget if denied. The manifest retains `max_epochs: 12` because the Harness-owned budget request, not Candidate code, authorizes any extension. Keep batch size 2, constant learning rate 0.0003, disabled early stopping, and the current Harness-owned sample/resource ceilings.

## Success Criteria

Treat ABI-223 as successful late-improving temporal-family evidence if it completes finitely within resource limits and either exceeds ABI-222's capped best `val/filtered_dice` by at least about 0.005, or preserves ABI-222-level filtered Dice while improving at least two of filtered recall, MIT filtered Dice, Google filtered Dice, filtered connectivity, or positive-fraction stability without a material precision collapse. It should also retain a clear margin over ABI-218 on filtered Dice, recall, source-stratified Dice, and connectivity.

## Fallback/Next Decision

If the late-improving request is denied, treat the resulting exploratory-budget Run as the valid bounded result. If ABI-223 fails contract, smoke, finite-state, or resource validation due to Candidate code, create at most one narrow repair that preserves ABI-222's exact temporal-attention hypothesis. If it completes but plateaus, overfits, or loses the matched-control temporal margin, stop close three-frame attention continuation and broaden to a five-frame temporal-difference/attention scout using the allowlisted `[-2, -1, 0, 1, 2]` window. Do not request whole-validation diagnostics unless the capped late-improving Result is strong, source-informative, noncollapsed, and scientifically warrants a trusted full-validation check.
