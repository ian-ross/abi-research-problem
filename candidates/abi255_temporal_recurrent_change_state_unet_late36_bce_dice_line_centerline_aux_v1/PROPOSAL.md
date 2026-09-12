# ABI-255 temporal recurrent change-state U-Net late36

## Hypothesis

ABI-242's compact bidirectional ConvGRU-style temporal state was finite, source-informative, and reached its best filtered Dice, raw Dice, training loss, and validation loss at epoch 12. A late-improving close continuation can test whether that final-epoch overlap signal matures into a competitive temporal recurrent Result, or whether weak connectivity remains a hard stop for this exact mechanism.

This is a **family-development continuation** and exact late-budget continuation of ABI-242, not a promotion claim.

## Comparison Target

Primary comparison targets are ABI-242 (`run_20260911_055200_52c75f`) as the parent scout, ABI-241 high-resolution change-skip, ABI-240 temporal line-accumulator late36, ABI-223/238 temporal-attention late36 comparators, and ABI-202 as the current single-frame whole-validation frontier context.

## Expected Effect

The desired signal is continued improvement in filtered Dice and source-stratified MIT/Google behavior beyond ABI-242's epoch-12 checkpoint while avoiding prediction collapse. A stronger result would also improve connectivity relative to ABI-242, but the late-budget question is bounded: determine whether the recurrent change-state branch was budget-truncated for overlap before deciding whether a redesigned line-aware recurrent mechanism is needed.

## Implementation Sketch

The architecture is unchanged from ABI-242. The Candidate consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]`. Per-frame normalized ABI, BTD, and Solar Geometry Input features are built from candidate-visible channels. Shared per-frame projections feed forward and backward ConvGRU cells; center states, center-frame embedding, and explicit signed/absolute temporal-change features are fused by a learned gate before a compact U-Net/ASPP decoder. The model returns `mask_logits`, `line_logits`, and `centerline_logits`.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Data policy: `frame_selection_policy: temporal_eligible_center`, `temporal_frame_offsets: [-1, 0, 1]`, `sampling_policy: combined_source_balanced`, `augmentation_policy: random_mirroring`.
- Output form: `mask_logits` plus trusted Line and Centerline auxiliary outputs.
- Loss: trusted `bce_dice` primary loss with provider-owned `weighted_bce` auxiliary losses.
- Optimizer/scheduler: AdamW with constant learning rate.
- Candidate code owns only PyTorch model architecture.

## Budget Requested

Request the approved `late_improving` budget for 36 epochs via `budget_request.yaml`, citing parent Run `run_20260911_055200_52c75f`. If denied, fall back to the exploratory budget.

## Success Criteria

Continue considering recurrent temporal mechanisms if ABI-255 completes finitely and materially improves ABI-242's capped filtered Dice, preserves non-collapsed MIT and Google behavior, or improves connectivity without severe recall loss. It need not beat ABI-202 to be useful family evidence, but a promotion-level claim would require later trusted diagnostics.

## Fallback/Next Decision

If ABI-255 fails contract/smoke/shape/numerical checks, classify and repair only if the original hypothesis is preserved. If it completes but remains far below ABI-223/238 with weak connectivity, stop this exact recurrent change-state branch and redesign the temporal recurrent mechanism rather than requesting another unchanged budget extension.
