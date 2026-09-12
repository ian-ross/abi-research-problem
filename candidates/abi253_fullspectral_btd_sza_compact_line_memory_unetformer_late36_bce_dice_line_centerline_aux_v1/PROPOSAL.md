# Proposal: ABI-253 compact full-spectral BTD+SZA line-memory U-NetFormer late36

## Classification

Family-development continuation. ABI-253 is an exact close continuation of ABI-252 using the approved `late_improving` budget. It is not a Repair Candidate because ABI-252 completed successfully; the only intended change is the Harness-owned budget request.

## Hypothesis

ABI-252 made the line-memory U-NetFormer branch resource-compatible and produced finite, non-collapsed, source-informative exploratory evidence. Its best checkpoint occurred near the end of the 12-epoch budget at epoch 10 (`val/filtered_dice` 0.3878), epoch 11 was nearly tied (0.3870), and epoch 12 shifted to the run's highest recall while retaining viable MIT and Google performance. The hypothesis is that this late-ambiguous trajectory is truncated by the exploratory epoch ceiling, and that the same compact row/column line-memory plus low-resolution shifted-window-attention mechanism can improve or stabilize with additional epochs without adding architecture cost.

## Comparison Target

- ABI-252 (`run_20260911_161019_8c76cd`) as the completed compact line-memory U-NetFormer parent.
- ABI-244 (`run_20260911_072719_ade068`) as the closest completed shifted-window U-NetFormer comparator.
- ABI-249 (`run_20260911_111909_dd7ef7`) as the high-precision rotation-aware line-prior comparator.
- ABI-202 (`run_20260904_043143_ee0005`) as the current aggregate whole-validation frontier context.

## Expected Effect

Additional trusted training epochs should clarify whether ABI-252's epoch-10/11 near-peak and epoch-12 recall shift mature into a stable improvement over ABI-244's capped U-NetFormer result. A successful late run would preserve ABI-252's bounded predicted-positive fraction and source-informative behavior while improving filtered Dice, recall, or connectivity without sacrificing the branch's precision advantage.

## Implementation Sketch

- Use provider-approved `abi_16ch_plus_sza` tensors only.
- Keep ABI-252's normalized GOES ABI channels 1-16, approved-channel thermal BTD planes, Solar Geometry Input features, and learned 1x1 channel mixtures.
- Keep ABI-252's compact hierarchical U-NetFormer encoder-decoder with shifted-window attention only at downsampled scales and bottleneck context.
- Keep differentiable row/column `LineMemoryBlock` modules as architecture-internal feature logic.
- Return `mask_logits`, `line_logits`, and `centerline_logits` for trusted Harness/provider losses.
- Add candidate-local `budget_request.yaml` for the approved `late_improving` budget citing parent Run `run_20260911_161019_8c76cd`.

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

Request the approved `late_improving` budget: up to 36 epochs and the corresponding Harness-owned timeout, with `fallback_if_denied: run_exploratory_budget`. The manifest remains within the ordinary allowlist (batch size 4, constant learning rate, source-balanced capped records); the budget request is the only intended budget change.

## Success Criteria

ABI-253 does not need to beat ABI-202 to be scientifically useful. It should be considered successful family-development evidence if it completes finitely and shows at least one of:

- a capped `val/filtered_dice` improvement over ABI-252 and ABI-244 while retaining source-informative MIT/Google behavior;
- improved recall or Contrail Connectivity Metric relative to ABI-252 without reverting to excessive predicted-positive fractions;
- or a stable late trajectory that indicates the compact line-memory U-NetFormer can serve as a viable comparator to the temporal and C4 line-prior branches.

Hard stop evidence would include resource timeout under the late budget, non-finite training, persistent prediction collapse, source-catastrophic behavior, or a convincing plateau below ABI-244/ABI-252 with no secondary-metric advantage.

## Fallback/Next Decision

If the late-improving budget is denied, accept the exploratory fallback as the valid bounded result. If ABI-253 plateaus below ABI-244 or fails from resource limits, stop the compact line-memory U-NetFormer branch and broaden to another underexplored family rather than adding attention or Candidate-owned scheduling workarounds. If ABI-253 improves materially, consider a trusted diagnostic request rather than immediate promotion, because capped Runs remain feasibility evidence.
