# Proposal: ABI-252 compact full-spectral BTD+SZA line-memory U-NetFormer

## Classification

Family-development continuation after the ABI-251 resource failure. This is not a Repair Candidate lineage entry because ABI-251 failed from Harness-recorded `resource_failure`, not a candidate bug or contract issue. The proposal preserves ABI-251's scientific hypothesis while reducing the attention/high-resolution compute enough to seek a complete exploratory Run.

## Hypothesis

ABI-251 reached useful partial evidence before timeout: by epoch 9 it was finite, source-informative, non-collapsed, and still improving to capped `val/filtered_dice` 0.3747, Google 0.4089, MIT 0.3605, precision 0.3973, recall 0.3546, and connectivity 0.3243. The exact model was too slow for the 3,600-second exploratory wall-clock budget and was force-terminated during epoch 10.

The hypothesis is that a narrower line-memory U-NetFormer can retain the useful ABI-251 mechanism—shifted-window low-resolution attention plus differentiable row/column line memory—while avoiding the expensive full-resolution shifted-window attention and 32-channel high-resolution path that prevented a complete 12-epoch result.

## Comparison Target

- ABI-251 (`run_20260911_150455_d03b0f`) as the resource-failed parent and partial line-memory U-NetFormer comparator.
- ABI-244 (`run_20260911_072719_ade068`) as the closest completed shifted-window U-NetFormer precedent.
- ABI-249 (`run_20260911_111909_dd7ef7`) as the high-precision line-prior comparator.
- ABI-202 (`run_20260904_043143_ee0005`) as the current aggregate whole-validation frontier context.

## Expected Effect

The compact model should finish within the exploratory budget by lowering the base width from 32 to 24, reducing learned mixer width from 16 to 12, and removing full-resolution shifted-window attention from the stem/final refiner while keeping line-memory context and lower-resolution shifted-window attention where global context is cheaper. If the ABI-251 partial trajectory reflected a real mechanism rather than only excess capacity, ABI-252 should produce a complete finite scout near or above ABI-251's epoch-9 partial score with bounded predicted-positive fractions and source-informative MIT/Google metrics.

## Implementation Sketch

- Use provider-approved `abi_16ch_plus_sza` tensors only.
- Build normalized GOES ABI channels 1-16, approved-channel thermal BTD planes, Solar Geometry Input features, and learned 1x1 channel mixtures inside the model.
- Keep a hierarchical U-NetFormer encoder-decoder with shifted-window attention at downsampled scales and bottleneck context.
- Keep differentiable row/column `LineMemoryBlock` modules as architecture-internal feature logic.
- Remove the most expensive full-resolution shifted-window attention blocks and narrow the high-resolution path.
- Return `mask_logits`, `line_logits`, and `centerline_logits` for trusted Harness/provider losses.

## Contract Features Used

- Provider-approved input mode: `abi_16ch_plus_sza`; candidate-visible channels are GOES ABI channels 1-16 plus Solar Geometry Input only.
- Manifest-selected trusted sampling: `combined_source_balanced`.
- Manifest-selected trusted frame policy: `all_target_frames`.
- Manifest-selected trusted augmentation: `random_mirroring`.
- Manifest-selected trusted primary loss: `bce_dice`.
- Manifest-declared trusted auxiliary targets: Line Target (`line_logits`, weighted BCE 0.01) and Centerline Target (`centerline_logits`, weighted BCE 0.02).
- Harness-owned AdamW optimizer, constant learning-rate scheduler, batch size 4, disabled early stopping, resource limits, metrics, Artifact Filters, and lifecycle.

Candidate code remains architecture-only. It does not implement data loading, target derivation, custom losses, metrics, Artifact Filters, morphology, thresholding, postprocessing, augmentation transforms, sampling policies, training loops, downloads, filesystem probes, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Budget Requested

Default exploratory budget only: 12 epochs, batch size 4, constant learning rate, capped provider-selected records, and the configured 3,600-second Docker timeout. No late-improving budget is requested because the motivating ABI-251 Run did not complete and the immediate question is resource-compatible feasibility.

## Success Criteria

A useful result does not need to beat ABI-202. ABI-252 should be considered successful evidence for this compact branch if it completes the exploratory budget without contract, numerical, or resource failure and shows at least one of:

- `val/filtered_dice` at or above ABI-251's partial epoch-9 value while reaching all 12 epochs;
- a comparable or better precision/recall/connectivity profile than ABI-244's completed shifted-window scout with lower single-frame resource cost;
- or a clearly late-improving, non-collapsed trajectory near epoch 12 that could justify a future close continuation under the approved late-improving policy.

Hard stop evidence for this compact branch would include another resource timeout, smoke/contract failure, non-finite training, persistent prediction collapse, source-catastrophic behavior, or a completed trajectory that remains far below ABI-244/ABI-251 partial evidence without a late-improving signal.

## Fallback/Next Decision

If ABI-252 completes and is finite but weaker with no late-improving signal, stop the line-memory U-NetFormer branch and broaden to a different underexplored family rather than repeatedly trimming attention. If it completes and preserves ABI-251's improving trajectory, consider one late-improving close-continuation only if Harness policy approves based on completed parent evidence. If it again fails from resource exhaustion, treat the high-resolution line-memory U-NetFormer mechanism as resource-infeasible under the current exploratory limits and broaden rather than requesting a Candidate-owned scheduling workaround.
