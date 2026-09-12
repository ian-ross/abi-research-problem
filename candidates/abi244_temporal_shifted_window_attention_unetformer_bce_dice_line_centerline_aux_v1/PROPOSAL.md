# ABI-244 temporal shifted-window attention U-NetFormer

## Hypothesis

A compact shifted-window temporal U-NetFormer can preserve ABI-229's local-attention connectivity signal while reducing fixed 8x8 window-boundary fragmentation. Shifted Swin-style windows over the ABI-223/229 three-frame temporal-attention/change stem should let thin contrail evidence cross local attention windows without moving Artifact Filtering, morphology, or thresholding into Candidate code.

Classification: **family-development continuation** within the temporal/modern-backbone branch. It is not a promotion candidate; it is a bounded scout of a materially changed attention mechanism after ABI-229's non-shifted window model was finite and connectivity-positive but below the temporal late36 frontier.

## Comparison Target

Primary comparison targets are ABI-229 (`run_20260910_141659_818da0`) for same-budget non-shifted temporal window attention, ABI-223 (`run_20260908_154531_8c7e2b`) as the capped temporal-family late36 frontier, ABI-238 (`run_20260911_004137_f54c45`) as the stronger but connectivity-regressed temporal directional continuation, and ABI-202 (`run_20260904_043143_ee0005`) as the mature single-frame frontier context.

## Expected Effect

Expected benefits relative to ABI-229 are improved filtered contrail connectivity and source-balanced filtered Dice by allowing line evidence to cross window seams. The desired signature is not merely more predicted-positive area: filtered recall should improve or remain stable without a large precision collapse, MIT and Google filtered Dice should remain non-catastrophic, and filtered predicted-positive fraction should stay in the temporal-frontier range. A neutral but useful result would show whether shifted local attention is compatible with provider-owned temporal tensors within the exploratory budget.

## Implementation Sketch

Start from the validated ABI-229 compact temporal window-attention U-NetFormer. Keep the provider-owned `[-1, 0, 1]` ABI+SZA temporal tensor, per-frame finite ABI/SZA/BTD feature builder, temporal attention/change fusion stem, hierarchical U-NetFormer encoder, atrous bottleneck, decoder, and Line/Centerline auxiliary heads. Replace the non-shifted local attention blocks with same-cost shifted-window attention blocks using an internal attention mask that prevents cyclic-wrap interactions across shifted-window seams. The candidate remains a PyTorch architecture with `build_model(input_spec, output_spec)` only.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal`
- `data.frame_selection_policy: temporal_eligible_center`
- `data.temporal_frame_offsets: [-1, 0, 1]`
- `data.sampling_policy: combined_source_balanced`
- `data.augmentation_policy: random_mirroring`
- `training.loss: bce_dice`
- `training.optimizer: adamw`
- `training.scheduler.policy: constant_lr`
- `training.batch_size: 2`
- trusted Line and Centerline auxiliary targets with `weighted_bce`

Candidate code does not implement data loading, temporal lookup, cache reads, missing-frame fallback, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Budget Requested

Request the default exploratory budget: 12 epochs, batch size 2, constant learning rate 0.0003, and no `late_improving` budget request. The branch changes architecture and should first produce bounded sequential resource and trajectory evidence before any longer continuation is considered.

## Success Criteria

A strong scout result would exceed ABI-229's best filtered Dice (0.376958) and filtered connectivity (0.313635) while keeping noncollapsed predictions and source-informative MIT/Google filtered Dice. A particularly promising result would approach the ABI-223/238 temporal late36 capped primary metric without losing ABI-223's connectivity advantage. Continuation can also be justified if the best checkpoint occurs at epoch 12 with finite noncollapsed predictions and an improving or ambiguous trajectory, even if it remains below ABI-223.

## Fallback/Next Decision

If the Run fails static validation or smoke because of Candidate code, create a repair Candidate preserving this hypothesis. If it completes but collapses, becomes non-finite, or clearly underperforms ABI-229 on both filtered Dice and connectivity, stop this shifted-window branch. If it is finite, source-informative, and improves ABI-229 connectivity or primary metric, consider either a late-improving continuation only if the approved criteria are met, or a tighter modern-backbone follow-up that preserves the successful shifted-attention mechanism while improving recall/precision balance.
