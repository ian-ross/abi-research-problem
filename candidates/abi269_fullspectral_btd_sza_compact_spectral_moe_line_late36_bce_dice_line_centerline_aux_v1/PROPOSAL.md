# ABI-269 compact spectral-regime MoE line U-Net late-improving continuation

## Hypothesis

ABI-268 repaired ABI-267's spectral-regime mixture-of-experts resource failure by using a compact MoE design that completed the exploratory budget, stayed non-collapsed, and selected epoch 12 as its best checkpoint. The hypothesis for ABI-269 is that the same resource-safe architecture, trained under the approved `late_improving` budget when granted, can convert the final-epoch improvement into higher recall and connected-line evidence while preserving the compact precision/source-balance profile.

This is a **family-development continuation** and late-improving close continuation, not a new architecture family and not a promotion claim. It deliberately preserves the ABI-268 architecture so the controlled factor is additional Harness-owned training budget.

## Comparison Target

Primary comparison target:

- ABI-268 (`run_20260912_113911_7a5f94`): exploratory parent, best epoch 12, capped `val/filtered_dice` 0.398540, filtered precision 0.446572, filtered recall 0.359837, connectivity 0.360615, MIT filtered Dice 0.386144, Google filtered Dice 0.429981, filtered predicted-positive fraction 0.002920.

Family and frontier context:

- ABI-231/232 spectral-regime MoE branch: ABI-232 late36 reached capped filtered Dice 0.400942, recall 0.396756, connectivity 0.383636, MIT 0.386542, Google 0.439983, but with a less compact earlier MoE formulation.
- ABI-265 selective axial line-memory and ABI-249 C4 steerable line-context are stronger recent capped comparators.
- ABI-202 remains the leading whole-validation-tested frontier; it is context, not a hard gate for this late-improving close continuation.

## Expected Effect

If ABI-268 was truncated by the exploratory epoch ceiling, extending the identical compact MoE line U-Net should improve `val/filtered_dice` after epoch 12, especially through recall/connectivity recovery, while retaining the parent's good precision and compact positive-area behavior. A useful positive result would approach or exceed ABI-232's MoE late36 capped aggregate/source metrics with lower resource cost.

A negative result is also useful: if longer training plateaus below ABI-232/ABI-265/ABI-249, degrades source balance, or trades precision for false positives without connectivity gain, then this exact compact MoE branch should stop or require a mechanism change rather than further late-budget repeats.

## Implementation Sketch

Reuse the ABI-268 PyTorch architecture unchanged except for Candidate identity. The model consumes provider-owned `abi_16ch_plus_sza` tensors. Its front end normalizes ABI channels 1-16, derives fixed thermal brightness-temperature-difference planes only from approved ABI channels, encodes Solar Geometry Input as scaled/cosine features, and learns a small 1x1 channel mixture.

The encoder-decoder is a compact U-Net with spectral/SZA-regime MoE blocks in downsampled encoder/bottleneck and low-resolution decoder stages. Gates are learned from provider-approved feature summaries only and choose among local, dilated, and line-oriented transformations. The high-resolution decoder fuses line context and returns `mask_logits`, `line_logits`, and `centerline_logits`.

## Contract Features Used

- `research_problem: goes_abi_contrail_segmentation`.
- `input_mode: abi_16ch_plus_sza`; no longitude or latitude inputs.
- `data.frame_selection_policy: all_target_frames`.
- `output_form: mask_logits`.
- Trusted auxiliary targets: Line Target via `line_logits` and Centerline Target via `centerline_logits` with `weighted_bce` weights 0.01 and 0.02.
- Trusted primary loss: `bce_dice`.
- Trusted optimizer/scheduler: AdamW with constant learning rate 0.0003.
- Trusted provider sampling and augmentation: `combined_source_balanced` and `random_mirroring`.
- Batch size 4 and manifest `max_epochs: 12`; longer execution is requested only through `budget_request.yaml` under the approved late-improving Harness policy.

Candidate code defines architecture only. It does not implement data loading, split logic, sampling, augmentation transforms, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, training loops, downloads, filesystem probes, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Budget Requested

Request the approved `late_improving` budget: up to 36 epochs and the corresponding Harness-owned late-improving timeout, with fallback to the exploratory budget if denied. The request is justified by ABI-268's final-epoch best checkpoint, finite/nondegenerate predictions, source-informative MIT and Google metrics, bounded predicted-positive fraction, and safe resource profile after ABI-267's timeout.

## Success Criteria

Continue or diagnose this branch if the Run is finite, contract-valid, non-collapsed, and any of these hold:

- best `val/filtered_dice` improves meaningfully over ABI-268 while precision and recall remain balanced;
- ABI-269 matches or exceeds ABI-232 MoE late36 on aggregate/source Dice, recall, or connectivity with lower resource cost;
- connectivity improves materially over ABI-268 without a broad predicted-positive-area increase;
- the best checkpoint occurs late with stable MIT and Google metrics, suggesting useful training-budget sensitivity;
- the result becomes close enough to ABI-249/ABI-202 capped frontier context to justify a trusted whole-validation diagnostic.

Do not require ABI-269 to beat the mature ABI-202 whole-validation frontier before using it as bounded family-development evidence.

## Fallback/Next Decision

If the budget request is denied, accept the exploratory run as the bounded result. If ABI-269 fails contract/smoke, repair only if the ABI-268 hypothesis and comparison target are preserved. If it completes but plateaus below ABI-268/ABI-232 or loses precision/source balance without a connectivity gain, stop exact late-budget repeats and consider either a compact connectivity-preserving MoE mechanism change or a broader underexplored family.
