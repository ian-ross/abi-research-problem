# ABI-355 temporal-attention multi-scale change-line fusion

## Classification

Family-development continuation in the temporal-attention architecture family. This is an exploratory mechanism-changing follow-up after ABI-350/351/354, not a promotion claim and not whole-validation evidence.

## Hypothesis

ABI-350 demonstrated that pre-decoder line support can become a strong temporal-attention branch under late training. ABI-351's final continuity bridge and ABI-354's encoder-entry change-line agreement did not solve the precision/recall/connectivity coupling problem. The hypothesis for ABI-355 is that temporal change and center-frame detail evidence should enter at the multi-scale decoder skip-fusion points: late enough to avoid perturbing the temporal stem/encoder anchor, but early enough to raise true contrail line evidence before final mask logits.

Expected effect: improve fixed-threshold recall and connected thin-line continuity relative to ABI-349/351/354 exploratory variants while avoiding ABI-344-style broad negative-patch footprint growth. A strong exploratory result would justify a later `late_improving` request; this submission does not request it.

## Comparison Target

- ABI-350 (`run_20260919_013306_9ca44e`): strong late-budget temporal-attention line-support comparator.
- ABI-354 (`run_20260919_080945_2ab8be`): negative evidence for injecting temporal change before encoder skip formation.
- ABI-351 (`run_20260919_034932_017f6a`): negative evidence for a post-decoder continuity bridge.
- ABI-349 (`run_20260919_004607_f785f8`): exploratory parent for pre-decoder line support.
- ABI-223 (`run_20260908_154531_8c7e2b`): temporal-attention connectivity comparator.
- ABI-324/348: temporal C4/detail-consensus comparators for balanced five-frame and compact behavior.

## Implementation sketch

Start from the ABI-350 temporal-attention U-Net scaffold: provider-owned three-frame ABI+SZA input, finite per-frame ABI normalization, ABI-channel-derived BTD planes, SZA transforms, shared frame embedding, per-pixel temporal attention/change stem, single-stream U-Net encoder, ASPP bottleneck, three decoder stages, and trusted mask/Line/Centerline heads.

Replace the simple pre-decoder line-support gates with `MultiScaleTemporalChangeLineFusion` modules at encoder skip scales 2, 1, and 0. Each module projects the coarser decoder/context state, center-frame detail features, and temporal-change features to the skip scale, combines them with orientation-aware line support from the skip, and applies a bounded gated update before decoder fusion. Temporal-change features are computed only from candidate-visible provider-supplied temporal frames: center minus neighbor mean, next minus previous, and absolute center-neighbor differences.

This is architecture-internal differentiable feature construction. It is not candidate-owned temporal lookup, data loading, sample selection, target derivation, thresholding, morphology, postprocessing, metrics, losses, Artifact Filters, coordinate use, Dataset Source identity use, downloads, resource scheduling, or lifecycle control.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Trusted frame selection: `temporal_eligible_center`.
- Temporal offsets: `[-1, 0, 1]`.
- No longitude/latitude inputs.
- Trusted sampling policy: `combined_source_balanced`.
- Trusted augmentation policy: `random_mirroring`.
- Trusted loss: `bce_dice` with trusted Line and Centerline `weighted_bce` auxiliaries.
- Optimizer/scheduler: AdamW with constant LR.
- Exploratory budget: 12 epochs, batch size 2.

## Budget Requested

Use the default exploratory budget only. ABI-355 is a mechanism-changing placement test with unproven trajectory; a late-improving budget should be considered only if this exploratory run is finite, source-informative, non-collapsed, and selected near the epoch ceiling with unresolved improvement.

## Success criteria

ABI-355 is useful if it completes finitely and shows at least several of:

- higher filtered Dice, recall, or connectivity than ABI-349/351/354 exploratory temporal-attention variants;
- MIT and Google source behavior without collapse;
- predicted-positive footprint closer to ABI-350/223 compact behavior than broad temporal recall sidecars;
- improved coupling of recall and connectivity at the selected checkpoint, rather than transient high-connectivity epochs with low recall;
- a late, improving or ambiguous trajectory that justifies bounded family development.

Hard-stop evidence for this exact branch would be contract/smoke failure, non-finite behavior, persistent all-negative/all-positive predictions, a clear plateau far below ABI-349/351/354, or another repetition of broad clutter without connected-line benefit.

## Fallback decision

If ABI-355 improves exploratory temporal-attention behavior and peaks near epoch 12, consider a late-improving continuation. If it is finite but weak, do not repeat simple gate-strength or placement variants; broaden toward a new temporal alignment/change module or a single-frame compact C4 anchor with separate recall sidecar. If it fails contract or smoke validation, repair only the implementation defect without changing the hypothesis.
