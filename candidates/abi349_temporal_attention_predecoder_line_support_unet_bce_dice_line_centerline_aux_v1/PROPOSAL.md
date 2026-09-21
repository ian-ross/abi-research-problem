# ABI-349 temporal-attention pre-decoder line-support U-Net

## Classification

Family-development continuation in the temporal-attention architecture family, run under the exploratory budget because the mechanism changes where line evidence enters the network.

## Hypothesis

Recent temporal C4 final-head and recall-sidecar variants can recover fixed-threshold recall or suppress negative-patch clutter, but they repeatedly fail to align best filtered Dice with connected thin-line continuity. ABI-345 also showed that adding a center-detail residual at the final head raises recall by broadening the footprint and loses ABI-223/238-style compact connectivity.

ABI-349 tests a different mechanism: keep the ABI-223/238 three-frame temporal-attention anchor, but inject orientation-aware line support into encoder skip features before each decoder fusion. The goal is to raise true contrail evidence as continuous line features before final logits are formed, rather than adding another residual/gain/veto after the decoder.

Expected effect: improve temporal-attention recall/source balance and preserve or recover connectivity relative to ABI-345, while remaining closer to ABI-223/238 compactness than broad temporal C4 recall sidecars.

## Comparison Target

- ABI-223 (`run_20260908_154531_8c7e2b`): temporal-attention connectivity comparator on the temporal-eligible validation population.
- ABI-238 (`run_20260911_004137_f54c45`): directional temporal-attention capped comparator.
- ABI-345 (`run_20260918_133432_9e7947`): negative evidence for final-head center-detail evidence sharpening.
- ABI-324 (`run_20260916_184108_954ec7`): balanced five-frame temporal C4/detail-consensus comparator.
- ABI-348 (`run_20260918_215534_a35ab9`): recent compact high-precision temporal C4 variant with weak connectivity.

## Implementation sketch

Start from the ABI-223/238 compact temporal-attention fusion U-Net over provider-owned offsets `[-1, 0, 1]`. Preserve the finite ABI+SZA+BTD feature builder, shared frame projection, temporal attention/change stem, U-Net encoder, ASPP bottleneck, decoder, and trusted Line/Centerline auxiliary outputs.

Replace the full-resolution-only directional bridge/final-head residual idea with three pre-decoder line-support gates:

1. At encoder scales 2, 1, and 0, compute orientation-aware line support with horizontal, vertical, and dilated diagonal branches.
2. Project the current coarser decoder/context feature to the skip scale.
3. Gate a bounded support update into the skip feature before it is consumed by the decoder fusion block.
4. Form primary mask, Line, and Centerline logits from the final refined decoder feature without candidate-owned thresholds or postprocessing.

The line support is differentiable model architecture. It is not morphology, thresholding, calibration, postprocessing, target derivation, an Artifact Filter, a metric, or a data-selection procedure.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Trusted frame selection: `temporal_eligible_center`.
- Temporal offsets: `[-1, 0, 1]`.
- No longitude/latitude inputs.
- Trusted sampling policy: `combined_source_balanced`.
- Trusted augmentation policy: `random_mirroring`.
- Trusted loss: `bce_dice` with trusted Line and Centerline `weighted_bce` auxiliaries.
- Optimizer/scheduler: AdamW with constant LR.
- Candidate source defines architecture only. It does not implement data loading, temporal lookup, sample selection, augmentation, losses, metrics, Artifact Filters, thresholds, postprocessing, training loops, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Budget Requested

Use the exploratory/default budget: 12 epochs, batch size 2, constant learning rate. Do not request the late-improving budget for this first pre-decoder line-support scout; request a longer continuation only if the exploratory trajectory is finite, source-informative, non-collapsed, and suggests the epoch ceiling is truncating useful learning.

## Success criteria

This Candidate does not need to beat the whole-validation ABI-202 reference to be useful. It is successful enough for further temporal-attention development if it completes finitely and shows several of the following temporal-eligible exploratory signals:

- filtered Dice close to ABI-223/238 despite the shorter exploratory budget, or an improving late trajectory that plausibly warrants late-improving continuation;
- recall improvement over ABI-223/238 without ABI-345-style precision/connectivity collapse;
- connectivity above ABI-345 and trending toward ABI-223/238 rather than ABI-348 compact-C4 weakness;
- MIT filtered Dice or positive-tail behavior improved without catastrophic Google regression;
- predicted-positive footprint consistent with compact line evidence rather than broad recall residual clutter.

Hard-stop evidence for this exact branch would be contract/smoke failure, non-finite behavior, persistent prediction collapse, or a finite result that simply repeats ABI-345's broad footprint with lower aggregate/source Dice and weak connectivity.

## Fallback decision

If ABI-349 is finite and shows useful recall/connectivity trajectory but is undertrained at 12 epochs, propose a late-improving continuation. If it is finite but clearly repeats ABI-345's footprint/connectivity failure, do not submit another simple line-support-gate gain change; broaden to a different temporal alignment mechanism or a single-frame C4 anchor with cross-scale detail support. If it fails contract or smoke testing, repair only the implementation defect while preserving this hypothesis.
