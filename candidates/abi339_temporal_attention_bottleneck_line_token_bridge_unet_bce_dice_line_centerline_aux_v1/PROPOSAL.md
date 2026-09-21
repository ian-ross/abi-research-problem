# ABI-339 temporal-attention bottleneck line-token bridge U-Net

## Classification

ABI-339 is a **family scout / family-development continuation** in the temporal-attention architecture family. It is mechanism-changing relative to ABI-223-style temporal attention and to the recent ABI-329/330 strip-token failures: it tests a cheap bottleneck-only line-token bridge, not another full-resolution strip-token hierarchy or a local residual-head continuation of ABI-324/338.

## Hypothesis

Recent temporal C4/detail-consensus variants can raise aggregate temporal-eligible filtered Dice, but repeatedly split into compact high-connectivity/low-recall states and broader higher-recall fragmented states. ABI-329/330 showed that full-resolution multi-scale strip-token line mixing is too expensive under the exploratory timeout, while ABI-333 showed that a final-head orientation bridge alone mainly broadened predictions without improving connected-line continuity.

ABI-339 tests whether a low-resolution temporal-attention backbone can receive long-axis line context cheaply at the bottleneck. The bottleneck row/column token bridge summarizes decoder-context features across image rows and columns at the 32x32 scale, fuses those tokens with local temporal-attention features, and returns the result to the normal U-Net decoder. The hypothesis is that line-continuity evidence injected before decoding can improve fixed-threshold connected true-positive evidence and source balance without the full-resolution cost or clutter broadening of prior strip-token/head-only approaches.

## Comparison Target

Primary local comparisons are:

- ABI-223, the temporal-attention connectivity comparator on the temporal-eligible validation population.
- ABI-238, the directional temporal-attention comparator.
- ABI-324, the strongest recent balanced five-frame temporal C4/detail-consensus comparator.
- ABI-333, the head-only orientation-consensus scout that failed to improve connected support.
- ABI-329/330, resource-failed strip-token line-mixer attempts that motivate the bottleneck-only cost control.

This remains capped temporal-eligible feasibility evidence. It is not whole Working Validation Split promotion evidence against ABI-202 or ABI-249.

## Expected Effect

The desired signature is a resource-safe 12-epoch scout that preserves ABI-223-style compactness and temporal-attention connectivity while improving aggregate/source Dice or recall. A positive result would show higher connectivity or a better precision/recall trade-off than ABI-333 and approach ABI-223/238 without ABI-329/330 timeout behavior. A negative result would show that bottleneck-only row/column line tokens are insufficient: metrics remain below ABI-223/324, connectivity does not improve, or the footprint broadens without source-balanced Dice gains.

## Implementation Sketch

- Use provider-stacked `[-1, 0, 1]` ABI+Solar Geometry temporal frames with the ABI-223 finite per-frame ABI/BTD/Solar Geometry feature builder.
- Reuse the ABI-223 compact temporal-attention fusion stem, U-Net encoder/decoder, and ASPP bottleneck context.
- Add a `BottleneckLineTokenBridge` after ASPP at the 32x32 bottleneck: row and column token summaries are expanded back to the bottleneck grid, fused with local features and token disagreement through learned convolutions, and added through a bounded learned gate.
- Keep Line and Centerline auxiliary outputs from the decoder for trusted auxiliary supervision.
- Keep all thresholding, losses, metrics, Artifact Filters, sample selection, temporal lookup, and execution lifecycle in trusted Harness/provider code.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Trusted frame selection: `data.frame_selection_policy: temporal_eligible_center`.
- Trusted temporal offsets: `[-1, 0, 1]`.
- Trusted sampling policy: `combined_source_balanced`.
- Trusted augmentation policy: `random_mirroring`.
- Trusted primary loss: `bce_dice`.
- Trusted auxiliary targets: Line Target (`line_logits`, weighted BCE 0.01) and Centerline Target (`centerline_logits`, weighted BCE 0.02).
- Trusted optimizer/scheduler: AdamW with constant learning rate 0.0003.

Candidate code must not own data loading, temporal lookup, S3/NetCDF access, sample selection, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, coordinate inputs, Dataset Source identity, downloads, resource scheduling, training loops, prediction retention, or lifecycle behavior.

## Budget Requested

Use the default exploratory budget: 12 epochs, batch size 2, provider-selected temporal-eligible capped records, constant learning rate, and the Harness-owned exploratory timeout. No late-improving budget is requested for this first bottleneck line-token scout.

## Success Criteria

ABI-339 is useful if it:

1. completes without contract, numerical, resource, or lifecycle failure;
2. produces finite non-collapsed source-informative predictions;
3. avoids ABI-329/330-style timeout/resource failure;
4. improves over ABI-333 on aggregate/source Dice, connectivity, or precision/recall balance without broad clutter; or
5. provides clear negative evidence that cheap bottleneck row/column token context is not enough, motivating a different temporal attention/alignment or trusted policy direction.

It does not need to beat ABI-324 or ABI-202 to be scientifically useful because this is a bounded mechanism scout.

## Fallback/Next Decision

If ABI-339 fails for a candidate bug or contract issue, submit a narrow repair only if the hypothesis and comparison target remain intact. If it fails for resource reasons, stop this bottleneck line-token branch rather than requesting Candidate-owned scheduling. If it completes finite but sub-frontier, classify whether bottleneck line tokens improved connected-line evidence or merely shifted footprint before deciding on any late-improving continuation.
