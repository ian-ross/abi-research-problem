# ABI-257 temporal oriented recurrent line-state U-Net

## Hypothesis

ABI-255 showed that compact bidirectional ConvGRU temporal change state can mature into a near-frontier temporal overlap Result, but ABI-255/ABI-256 diagnostics indicate the remaining weakness is thin-line continuity and diffuse low-confidence evidence. ABI-257 tests whether putting oriented line evidence inside the recurrent temporal state, before encoder/decoder compression, improves connectivity and threshold-0.5 evidence without candidate-owned postprocessing.

## Classification

Family-development continuation within the provider-owned temporal recurrent family. This is a mechanism-changing continuation after ABI-255 and ABI-256, not an unchanged late36 rerun.

## Comparison Target

Primary family targets:

- ABI-255 (`run_20260911_210922_27f346`): compact recurrent change-state late36 temporal comparator.
- ABI-256 (`run_20260911_230821_08caf0`): decoder-side centerline bridge that did not improve the recurrent branch.

Contextual targets:

- ABI-223/238/240 temporal attention/line comparators for connectivity.
- ABI-202 single-frame whole-validation frontier for mature incumbent context only.

## Expected Effect

Compared with ABI-255, ABI-257 should preserve source-informative temporal overlap while increasing filtered contrail connectivity and reducing fragmentation at the fixed trusted threshold. Compared with ABI-256, moving line memory into the recurrent stem should avoid the unstable decoder-side precision/connectivity versus recall tradeoff.

## Implementation Sketch

Use the same compact temporal recurrent U-Net skeleton as ABI-255. Replace the temporal stem with an oriented recurrent line-state stem:

1. Build finite ABI/SZA/BTD features independently for provider-supplied previous, center, and next frames.
2. Project each frame into a compact embedding.
3. Run bidirectional ConvGRU cells across `[-1, 0, 1]` to form a center recurrent state.
4. Apply a learnable oriented line bank to each frame embedding using horizontal, vertical, and dilated diagonal depthwise context.
5. Form a center-anchored temporal line delta from center line evidence minus the neighbor mean line evidence.
6. Fuse the line state, recurrent state, center embedding, and explicit before/after change evidence before the encoder.
7. Decode with the compact U-Net decoder and trusted `mask_logits`, `line_logits`, and `centerline_logits` heads.

This is differentiable architecture-internal feature extraction, not morphology, thresholding, postprocessing, or an Artifact Filter.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Temporal frame offsets: `[-1, 0, 1]`.
- Frame-selection policy: `temporal_eligible_center`.
- Sampling policy: `combined_source_balanced`.
- Augmentation policy: trusted `random_mirroring`.
- Primary loss: trusted `bce_dice`.
- Auxiliary targets: trusted `line` and `centerline` with `weighted_bce`.
- Optimizer/scheduler: AdamW with constant learning rate.
- Exploratory/default budget: 12 epochs, batch size 2.

Candidate code defines model architecture only. It does not implement data loading, temporal lookup, cache access, missing-frame handling, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior. Longitude and latitude are not inputs.

## Budget

Exploratory/default budget: 12 epochs, batch size 2. No late-improving request is included. If the 12-epoch trajectory is finite, non-collapsed, near ABI-255/ABI-223 temporal evidence, and still improving at the ceiling, a later step may consider an approved `late_improving` close-continuation request.

## Success Criteria

Useful family-development evidence if ABI-257 is finite/resource-safe and satisfies one or more of:

- improves connectivity over ABI-255 at comparable temporal-eligible filtered Dice and source behavior;
- improves filtered Dice over ABI-256 while avoiding a collapse in recall;
- approaches ABI-223/238 connectivity more closely than ABI-255 without severe MIT or Google regression;
- shows a clearly late-improving, non-collapsed trajectory justifying a later bounded late36 continuation.

Hard stop for this exact mechanism if it has resource failure, non-finite behavior, persistent prediction collapse, or clearly regresses both overlap and connectivity relative to ABI-255/256 without an improving trajectory.

## Fallback Next Decision

If ABI-257 is finite and improves connectivity but remains under-trained, consider a later `late_improving` close continuation only if Harness metrics show a late-improving non-collapsed trajectory. If it regresses both overlap and connectivity, stop this exact stem and broaden to a temporal attention/change architecture or non-temporal rotation-aware line scout. If it fails by candidate bug, repair only the bug while preserving this hypothesis and comparison target. If the contract blocks execution, create a Capability Request rather than moving provider-owned behavior into candidate code.
