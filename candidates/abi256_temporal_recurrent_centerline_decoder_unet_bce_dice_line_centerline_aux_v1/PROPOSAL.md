# ABI-256 temporal recurrent centerline-decoder U-Net

## Hypothesis

ABI-255 showed that compact bidirectional recurrent temporal state can reach near-frontier temporal-eligible overlap, but its diagnostics identified weak thin-line connectivity and broad low-confidence negative-patch clutter. A high-resolution centerline-preserving decoder bridge may raise true contrail evidence at the trusted threshold and improve continuity without repeating the exact ABI-255 late-budget branch.

This is a **family-development continuation** within temporal recurrent modeling and a mechanism change, not a promotion claim.

## Comparison Target

Primary comparison targets are ABI-255 (`run_20260911_210922_27f346`) as the recurrent late36 parent, ABI-223/238 as stronger temporal-attention connectivity comparators, ABI-240 as the temporal line-accumulator recall comparator, and ABI-202 as whole-validation frontier context.

## Expected Effect

The desired signal is higher filtered connectivity and equal or better filtered Dice than ABI-255's recurrent branch at exploratory scale, while preserving non-collapsed MIT and Google Dice. A useful result may also reduce the threshold-diagnostic pattern seen in ABI-255 by converting lower-confidence line evidence into fixed-threshold logits. Low score alone will not eliminate temporal recurrent modeling, but worse connectivity with larger predicted-positive area would stop this exact decoder bridge.

## Implementation Sketch

The Candidate consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]`. It preserves ABI-255's finite per-frame ABI+BTD+Solar Geometry Input feature builder and compact bidirectional ConvGRU change-state stem. After the ASPP U-Net decoder, a new high-resolution centerline bridge combines the refined decoder, full-resolution skip, temporal-stem features, and learnable horizontal/vertical/dilated directional convolutions. The bridge enhances mask features and supplies `line_logits` and `centerline_logits` auxiliary features. This is model architecture only, not thresholding or postprocessing.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Data policy: `frame_selection_policy: temporal_eligible_center`, `temporal_frame_offsets: [-1, 0, 1]`, `sampling_policy: combined_source_balanced`, `augmentation_policy: random_mirroring`.
- Output form: `mask_logits` plus trusted Line and Centerline auxiliary outputs.
- Loss: trusted `bce_dice` primary loss with provider-owned `weighted_bce` auxiliary losses.
- Optimizer/scheduler: AdamW with constant learning rate.
- Candidate code owns only PyTorch model architecture.

## Budget Requested

Use the default exploratory budget: 12 epochs, batch size 2, constant learning rate, and Harness-owned resource limits. No late-improving budget is requested for this mechanism-changing scout.

## Success Criteria

Continue this branch only if ABI-256 completes finitely and shows at least one of: improved connectivity over ABI-255 without severe filtered-Dice loss, improved filtered Dice over the ABI-242/255 recurrent family at a non-collapsed MIT/Google split, or a late-improving trajectory suitable for a future approved close-continuation request. Promotion would require later trusted diagnostics and is not claimed from this capped temporal-eligible Run.

## Fallback/Next Decision

If ABI-256 fails contract/smoke/shape/numerical checks, classify and repair only if the centerline-decoder hypothesis is preserved. If it completes but worsens ABI-255's connectivity or merely increases diffuse positives, stop this exact bridge and broaden to a different temporal-attention/change mechanism or non-temporal architecture family.
