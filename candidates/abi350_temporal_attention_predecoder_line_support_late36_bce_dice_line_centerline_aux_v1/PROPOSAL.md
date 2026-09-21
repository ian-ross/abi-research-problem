# ABI-350 temporal-attention pre-decoder line-support late36

## Classification

Family-development continuation in the temporal-attention architecture family. This is a close late-improving continuation of ABI-349, not a promotion claim and not a whole-validation Result.

## Hypothesis

ABI-349 moved orientation-aware line support into encoder skip features before decoder fusion. Under only 12 exploratory epochs it produced a compact, finite, source-informative checkpoint selected at the final epoch, with stronger same-budget filtered Dice, recall, precision, and connectivity than ABI-223/238/345 at epoch 12. The late-budget hypothesis is that the same pre-decoder support mechanism is undertrained: with 36 epochs, it may close the recall and connectivity gaps to mature temporal-attention comparators without the broad-footprint failure mode seen in final-head recall sidecars.

Expected effect: improve ABI-349 aggregate/source filtered Dice, recall, and connectivity while keeping predicted-positive footprint close to compact temporal-attention behavior rather than broad ABI-345/344-style area growth.

## Comparison Target

- ABI-349 (`run_20260919_004607_f785f8`): direct exploratory parent and primary family baseline.
- ABI-223 (`run_20260908_154531_8c7e2b`): temporal-attention connectivity comparator on the temporal-eligible validation population.
- ABI-238 (`run_20260911_004137_f54c45`): directional temporal-attention capped comparator.
- ABI-345 (`run_20260918_133432_9e7947`): negative evidence for final-head center-detail sharpening.
- ABI-324 (`run_20260916_184108_954ec7`): current balanced five-frame temporal C4/detail-consensus comparator.

## Implementation sketch

Preserve ABI-349 exactly except for Candidate identity and late-improving budget request. The model keeps the three-frame provider-owned temporal input, finite ABI+SZA+BTD feature builder, shared frame projection, per-pixel temporal attention/change stem, U-Net encoder, ASPP bottleneck, three decoder stages, and trusted mask/Line/Centerline heads.

At encoder scales 2, 1, and 0, `PreDecoderLineSupportGate` computes horizontal, vertical, and dilated diagonal line-support features from the encoder skip, combines them with the coarser decoder/context state, and gates a bounded support update into the skip before decoder fusion. This remains differentiable model architecture only; it is not thresholding, morphology, calibration, postprocessing, target derivation, an Artifact Filter, a metric, or data selection.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Trusted frame selection: `temporal_eligible_center`.
- Temporal offsets: `[-1, 0, 1]`.
- No longitude/latitude inputs.
- Trusted sampling policy: `combined_source_balanced`.
- Trusted augmentation policy: `random_mirroring`.
- Trusted loss: `bce_dice` with trusted Line and Centerline `weighted_bce` auxiliaries.
- Optimizer/scheduler: AdamW with constant LR.
- Candidate source defines architecture only and does not implement data loading, temporal lookup, sample selection, augmentation, losses, metrics, Artifact Filters, thresholds, postprocessing, training loops, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Budget Requested

Request the Harness-owned `late_improving` budget for 36 epochs via `budget_request.yaml`, with exploratory fallback if denied. The request is justified by ABI-349's final-epoch best checkpoint, finite non-collapsed predictions, viable MIT/Google behavior, and favorable same-budget trajectory versus prior temporal-attention branches.

## Success criteria

ABI-350 is useful if it completes finitely and shows at least several of:

- improved filtered Dice, MIT/Google Dice, recall, or connectivity over ABI-349;
- recall/connectivity closing toward ABI-223/238 without a major precision or footprint collapse;
- compact predicted-positive fraction closer to ABI-223/238 than ABI-345/344 broad recall variants;
- source-balanced behavior with no MIT or Google collapse;
- a late trajectory that clarifies whether pre-decoder line support is a viable temporal-attention continuation.

Hard-stop evidence for this exact branch would be contract/smoke failure, non-finite behavior, persistent prediction collapse, or a finite late-budget plateau below ABI-223/238 that repeats ABI-345-style broad footprint or ABI-348-style weak connectivity.

## Fallback decision

If ABI-350 improves materially over ABI-349 but remains below ABI-223/238 in connectivity, request temporal-eligible failure-bucket diagnostics before more close continuations. If it plateaus or trades compactness for broad clutter, do not submit another simple gate-strength continuation; broaden to a different temporal alignment/change mechanism or a single-frame C4 anchor with cross-scale detail support. If the Harness denies the late budget, treat the exploratory fallback as the bounded Result and continue from its evidence.
