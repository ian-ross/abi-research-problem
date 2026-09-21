# ABI-354 temporal-attention encoder change-line agreement U-Net

## Hypothesis

ABI-350 showed that pre-decoder temporal-attention line support can produce the strongest capped temporal-eligible filtered Dice so far, but its selected checkpoint remained connectivity-limited and MIT-positive-tail failures persisted. ABI-351 then showed that adding a continuity bridge after the decoder is too late and widens the footprint without improving connected-line evidence. This family-development continuation tests whether moving temporal change/detail line agreement to the encoder entry, before skip features are formed, can make continuous center-frame contrail evidence available throughout the encoder-decoder while preserving ABI-350's compact pre-decoder line-support anchor.

## Comparison Target

Primary comparison is ABI-350 (`run_20260919_013306_9ca44e`) on the trusted temporal-eligible capped validation population. Secondary comparisons are ABI-324 for balanced temporal C4/detail consensus, ABI-223 for temporal-attention connectivity, ABI-348 for compact temporal C4 behavior, and ABI-351 as the negative post-decoder continuity-bridge control.

## Expected Effect

The encoder-entry change/line agreement bridge should raise true contrail logits at fixed threshold 0.5 for temporally persistent or changing thin-line segments before the decoder chooses skip features. Desired effects are higher filtered connectivity and MIT positive-tail recall than ABI-350 without ABI-351-style footprint widening, and aggregate filtered Dice remaining near the ABI-350/ABI-324 temporal comparator band.

## Implementation Sketch

Start from the ABI-350 temporal-attention pre-decoder line-support U-Net. Keep provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]`, the learned per-frame ABI/SZA/BTD feature builder, temporal attention stem, compact encoder, ASPP context, pre-decoder line-support gates, and Line/Centerline auxiliary heads. Add a differentiable `EncoderEntryChangeLineAgreement` block immediately after the temporal stem and before the encoder. It projects the center-frame feature tensor, computes bounded provider-visible temporal change features (`center - neighbor_mean`, `next - previous`, and neighbor absolute differences), runs orientation-aware line support on the stem/center anchor, and injects a gated support residual into the stem. No thresholding, postprocessing, morphology, temporal lookup, data loading, target construction, custom loss, metric, Artifact Filter, coordinates, Dataset Source identity, filesystem probing, or network access is added.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`.
- Input mode: provider-owned `abi_16ch_plus_sza_temporal`.
- Data policy: trusted `combined_source_balanced` sampling, `temporal_eligible_center` frame selection, offsets `[-1, 0, 1]`, and trusted `random_mirroring` augmentation.
- Output form: `mask_logits` with provider-declared Line and Centerline auxiliary outputs.
- Loss/optimizer/scheduler: trusted `bce_dice`, auxiliary `weighted_bce`, AdamW, constant learning rate.
- Candidate code defines only architecture over Harness-supplied tensors.

## Budget Requested

Exploratory default budget: 12 epochs, batch size 2, constant learning rate 0.0003. No `late_improving` budget is requested because this is a mechanism-changing follow-up after ABI-351 rather than an unchanged close continuation.

## Success Criteria

Treat this as temporal-family development, not immediate promotion. A useful result would be finite, non-collapsed training under resource limits and one or more of: filtered Dice close to the ABI-350/ABI-324 comparator band, filtered connectivity above ABI-350 and approaching ABI-324/ABI-223, fewer complete positive misses or low-connectivity positives than ABI-350, improved MIT filtered Dice/positive-tail behavior, or a late-improving trajectory that justifies a future approved late-budget continuation. A hard stop is justified if the Run fails contract/smoke/numerical checks, collapses to all-negative/all-positive predictions, clearly widens negative-patch clutter while reducing connectivity as ABI-351 did, or plateaus far below ABI-349/351 without a diagnostic secondary-metric gain.

## Fallback/Next Decision

If ABI-354 improves connectivity or MIT positive-tail evidence without excessive footprint growth, consider a late-improving continuation or a focused temporal-eligible failure-bucket evaluation. If it repeats ABI-351's broad low-connectivity failure, stop this exact encoder-entry bridge and broaden to a different mechanism such as an alignment/change module inside multi-scale fusion or a modern lightweight backbone with an explicit line-continuity decoder. Do not use Candidate-owned thresholding, postprocessing, losses, metrics, data selection, Artifact Filters, or temporal provisioning as a fallback.
