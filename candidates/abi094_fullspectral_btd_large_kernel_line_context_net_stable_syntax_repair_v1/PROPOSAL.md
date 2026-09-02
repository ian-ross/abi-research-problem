# ABI-094 Repair Proposal: ABI-093 syntax repair for stable full-spectral BTD large-kernel line-context net

## Hypothesis

A syntax-only repair of ABI-093 can provide the intended finite evidence for the same ABI-092/ABI-093 large-kernel line-context family-scout hypothesis. The underlying hypothesis is unchanged: axial horizontal, vertical, local, and dilated convolutional context throughout a compact encoder-decoder may accumulate elongated contrail evidence before final mask prediction, improving the capped precision/connectivity tradeoff without candidate-owned thresholding or Artifact Filters.

Proposal class: **repair candidate / family scout repair**. ABI-093 (`run_20260830_002454_13b411`) failed smoke testing with Harness-recorded `candidate_bug` due to a `SyntaxError: unmatched '}'` at the `StableFullSpectralBTDLargeKernelLineContextNet` class docstring. ABI-094 changes only that candidate-source syntax defect and declares repair lineage to ABI-093; it preserves the comparison target, input mode, full-spectral BTD front end, centerline auxiliary target, focal-Tversky loss, source-balanced sampling, trusted augmentation, learning rate, and residual-scaled large-kernel line-context architecture.

## Comparison Target

Primary comparison targets remain:

- ABI-068 / `run_20260828_010836_4ccc77`, the strongest capped frequency-gated focal-Tversky reference by `val/filtered_dice`.
- ABI-066 / `run_20260827_230540_bf4ce3`, the precision/connectivity-forward frequency-gated `bce_dice_cldice` reference.
- ABI-092 / `run_20260830_001308_e99407`, the failed large-kernel line-context scout whose non-finite training state motivated ABI-093.
- ABI-093 / `run_20260830_002454_13b411`, the syntax-broken stability repair that ABI-094 fixes.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. ABI-094 uses the representative capped policy and must not be interpreted as a full-data promotion result.

## Expected Effect

The expected first effect is that static validation and smoke import proceed past the ABI-093 class-definition syntax error, allowing the Harness to evaluate whether the residual-scaled large-kernel architecture actually trains finitely. Because the architecture and manifest are otherwise unchanged from ABI-093, any successful Run should answer the ABI-093 repair question rather than introduce a new scientific branch.

If the repair trains finitely, useful scientific evidence would be either a non-collapsed operating point near the ABI-068/066 band or a distinctive large-kernel profile: improved filtered precision/connectivity or lower filtered predicted-positive fraction without source-specific collapse.

## Implementation Sketch

The model keeps ABI-093's normalized full-spectral BTD front end over `abi_16ch`, explicit thermal BTD planes, learned 1x1 channel mixer, compact residual-scaled large-kernel encoder-decoder, low-resolution pyramid context, multi-scale line head, primary `mask_logits`, and provider-derived `centerline_logits` auxiliary output.

The only source fix is removal of the stray `},{` after the `StableFullSpectralBTDLargeKernelLineContextNet` class docstring. The manifest adds explicit repair lineage for ABI-093's smoke failure while leaving the trusted training/data/loss choices unchanged.

The candidate does not implement data loading, split logic, sampling policy, augmentation transforms, target derivation, losses, metrics, thresholds, Artifact Filters, postprocessing, resource placement, filesystem probes, network access, runtime weight downloads, or longitude/latitude-derived features.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; candidate receives only ABI channels 1-16.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target via `centerline_logits`, trusted `weighted_bce`, weight 0.02.
- Sampling policy: provider/Harness-owned `combined_source_balanced`.
- Augmentation policy: trusted `random_mirroring`.
- Primary loss: trusted `focal_tversky`.
- Optimizer: `adamw`.
- Scheduler: `constant_lr`.
- Repair lineage: ABI-093 smoke failure classified as `candidate_bug`.

## Budget Requested

One sequential representative capped Run under the active Workspace Configuration: 1,024 provider-selected train and validation records per Dataset Source/split, batch size 4, 12 epochs, constant learning rate 0.0001, disabled early stopping, Docker training wall-clock timeout of 3,600 seconds, max four fixed `first_n` prediction artifacts, pinned A100 execution, and the 25M-parameter smoke budget.

## Success Criteria

Minimum repair criteria: static contract validation passes, syntax compilation passes, smoke test stays under the 25M-parameter budget, training completes finitely under the wall-clock limit, predictions are non-degenerate, and both MIT and Google capped validation filtered Dice remain above approximately 0.30.

Useful family-continuation criteria: at least one of the following holds without a source-specific collapse: aggregate `val/filtered_dice` is within about 0.03 of ABI-068 after the stabilization change; filtered precision or Contrail Connectivity improves over ABI-068 at similar recall; filtered predicted-positive fraction is lower than ABI-068 with no larger than about 0.03 aggregate Dice loss; or the trajectory is late-improving enough to justify one bounded continuation. Promotion-like interpretation would require later whole-validation diagnostics and human review, not this capped scout repair alone.

## Fallback/Next Decision

If ABI-094 still fails static validation, smoke, or finite-state checks, stop this exact large-kernel line-context implementation and broaden to a different architecture or trusted policy axis rather than retrying or increasing Candidate-owned resource use. If it trains but shows persistent all-negative/all-positive collapse, non-finite behavior, a clear source-specific catastrophe, or filtered Dice far below the 0.30 scout floor, do not repeat this exact branch. If it is finite but below ABI-068 while providing a distinctive precision/connectivity or positive-area benefit, write a Research Note and consider one bounded family-development continuation. If it is simply lower on aggregate Dice and secondary metrics, broaden the frontier rather than adding more output-side gates.
