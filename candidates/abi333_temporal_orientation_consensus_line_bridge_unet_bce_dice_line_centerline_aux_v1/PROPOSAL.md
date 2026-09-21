# ABI-333 temporal orientation-consensus line bridge U-Net

## Classification

ABI-333 is a **family-development continuation** in the temporal architecture family. It is mechanism-changing relative to the ABI-331/332 compact three-frame persistence/detail line-gate branch, not an unchanged late continuation and not a promotion candidate.

## Hypothesis

ABI-332 validated that the compact three-frame temporal persistence/detail mechanism is resource-safe and late-improving, but its remaining weakness is connected thin-line support: the late36 continuation improved recall and source Dice but left connectivity below ABI-324 and ABI-223. The next useful question is whether the cheap three-frame branch can gain connected-line evidence through architecture-level orientation consensus rather than another longer-budget rerun.

ABI-333 adds a bounded differentiable orientation-consensus bridge over horizontal, vertical, and diagonal line features in the final head. The hypothesis is that requiring agreement among multiple oriented line views, center-frame detail, and temporal persistence support will raise true contrail logits at the fixed Harness threshold while avoiding the broad-footprint behavior seen in positive-tail reinjection variants.

## Comparison Target

Primary local comparisons are:

- ABI-332, the direct late36 compact three-frame persistence/detail parent.
- ABI-331, the exploratory parent for resource and early-trajectory comparison.
- ABI-319, a stronger three-frame shift-bank/C4 comparator.
- ABI-324, the strongest recent balanced five-frame temporal C4 aggregate/connectivity comparator.
- ABI-223, the temporal-attention connectivity comparator.

This remains capped temporal-eligible feasibility evidence. It is not whole Working Validation Split promotion evidence against ABI-202/249.

## Expected Effect

The desired signature is a finite, source-informative 12-epoch scout that improves ABI-331/332 connectivity or recall/precision balance without increasing the filtered predicted-positive footprint into ABI-325-style broad clutter. A useful positive result would approach ABI-319/324 on aggregate/source Dice while narrowing the connectivity gap to ABI-223. A negative result would show that orientation consensus in the compact three-frame head is insufficient: either precision drops from broader predictions, recall remains below temporal C4 comparators, or connectivity does not improve.

## Implementation Sketch

- Use provider-stacked `[-1, 0, 1]` ABI+Solar Geometry frames with the ABI-331/332 finite per-frame ABI/BTD/Solar Geometry feature builder.
- Reuse the compact temporal persistence/detail stem, U-Net encoder/decoder, ASPP context, and center-detail branch that completed within the exploratory and late-improving budgets.
- Replace the final line-context path with an orientation-consensus bridge: horizontal, vertical, near-diagonal, and wide-diagonal feature branches each emit an orientation support logit; their bounded consensus probability gates a positive line/detail/temporal residual in the primary mask logits.
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

Use the default exploratory budget: 12 epochs, batch size 2, provider-selected temporal-eligible capped records, constant learning rate, and the Harness-owned exploratory timeout. No late-improving budget is requested for this first mechanism-changing scout.

## Success Criteria

ABI-333 is useful if it:

1. completes without contract, numerical, resource, or lifecycle failure;
2. produces finite non-collapsed source-informative predictions;
3. improves over ABI-331/332 on connectivity, recall/precision balance, or compact source-balanced filtered Dice;
4. narrows the gap to ABI-319/324/223 without ABI-325-like footprint broadening; or
5. cleanly shows that compact orientation-consensus head support is not enough, motivating a different temporal attention/alignment or policy direction.

It does not need to beat ABI-324 or ABI-202 to be scientifically useful because this is a bounded mechanism scout.

## Fallback/Next Decision

If ABI-333 fails for a candidate bug or contract issue, submit a narrow repair only if the hypothesis and comparison target remain intact. If it fails for resource reasons, stop this exact orientation-consensus head variant rather than requesting Candidate-owned scheduling. If it completes with finite but sub-frontier evidence, classify whether orientation consensus specifically improved connectivity or merely widened predictions before deciding on any bounded family-development continuation.
