# ABI-241 temporal high-resolution change-skip U-Net

## Hypothesis

A temporal model can recover more thin-line continuity than ABI-239/240 by keeping temporal-difference evidence at full 256x256 resolution and injecting it into encoder skip features, rather than pooling line support before the encoder. Provider-owned neighboring ABI frames should expose persistent/advection-consistent contrails and help suppress static cloud/geography cues, while high-resolution change skips should avoid the connectivity loss seen in the low-resolution line accumulator.

This is a **family-development continuation** within the provider-owned temporal modeling frontier, but the mechanism is materially different from ABI-239/240: it adds a full-resolution temporal-difference skip bridge with learned oriented depthwise support, not a low-resolution line accumulator or a post-decoder directional context filter.

## Comparison Target

Primary comparison targets are:

- ABI-240 (`run_20260911_031326_43ed12`), the late36 low-resolution temporal line-accumulator branch: best capped `val/filtered_dice` 0.414892, filtered recall 0.395534, filtered connectivity 0.264863.
- ABI-238 (`run_20260911_004137_f54c45`), the temporal-attention directional-context branch: best capped `val/filtered_dice` 0.420235, filtered connectivity 0.352239.
- ABI-223 (`run_20260908_154531_8c7e2b`), the mature temporal-attention late36 branch: best capped `val/filtered_dice` 0.419776, filtered connectivity 0.412427.
- ABI-202 (`run_20260904_043143_ee0005`) remains the single-frame frontier context, not the sole elimination gate for this exploratory continuation.

## Expected Effect

Expected favorable signal: compared with ABI-240, the high-resolution temporal-difference bridge should preserve or improve filtered recall while increasing filtered connectivity by avoiding premature 4x pooled line support. Compared with ABI-238, it should protect recall by injecting change evidence before and through decoder skips instead of adding a post-decoder context bridge that favored precision and reduced connectivity.

A successful exploratory Result need not beat ABI-202 immediately. It should be finite, noncollapsed, source-informative, and either approach the ABI-223/238 capped Dice band or show a better recall/connectivity tradeoff than ABI-240 at comparable predicted-positive fraction.

## Implementation Sketch

The Candidate consumes `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` using only provider-supplied ABI channels 1-16 plus per-frame Solar Geometry Input. Per-frame normalized ABI, BTD, and SZA features are built inside the model from candidate-visible channels only.

The base temporal-attention stem follows the ABI-223 pattern: shared frame projection, per-pixel attention over previous/center/next embeddings, and signed/absolute change fusion. ABI-241 adds a parallel high-resolution temporal-change bridge. The bridge computes center-minus-neighbor-mean, next-minus-previous, and absolute neighbor differences from the approved feature tensors, projects them at full resolution, applies learned horizontal/vertical/diagonal depthwise support convolutions, and produces multi-scale change skips. Gated skip-fusion modules merge these change skips with encoder features at 256x256, 128x128, and 64x64 before the ASPP decoder. The model returns `mask_logits`, `line_logits`, and `centerline_logits` only.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Data policy: `frame_selection_policy: temporal_eligible_center`, `temporal_frame_offsets: [-1, 0, 1]`, `sampling_policy: combined_source_balanced`, `augmentation_policy: random_mirroring`.
- Output form: `mask_logits` plus trusted Line and Centerline auxiliary outputs.
- Loss: trusted `bce_dice` primary loss with provider-owned `weighted_bce` auxiliary losses.
- Optimizer/scheduler: AdamW with constant learning rate.
- Candidate code owns only PyTorch model architecture. It does not implement data loading, temporal lookup, cache reads, missing-frame fallback, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Budget Requested

Exploratory default budget only: 12 epochs, batch size 2, constant learning rate, and current Harness-owned resource ceilings. No late-improving budget is requested for this first high-resolution change-skip scout. If it is finite, noncollapsed, source-informative, and selects its best checkpoint at or near epoch 12 with improving or ambiguous trajectory, a later close continuation may request the approved late-improving budget.

## Success Criteria

Continue developing this branch if ABI-241 completes successfully and shows at least one of:

- capped `val/filtered_dice` near the temporal frontier neighborhood, roughly within 0.02 of ABI-223/238, while remaining source-informative on MIT and Google;
- a materially better connectivity/recall balance than ABI-240, especially filtered connectivity above ABI-240's 0.264863 without a severe recall collapse;
- a late-improving trajectory with best checkpoint at epoch 12, finite predictions, and no all-negative/all-positive degeneration;
- diagnostically useful source behavior suggesting temporal change skips improve MIT or Google failure modes.

Do not require this exploratory scout to beat the mature ABI-202 single-frame Result before considering one bounded continuation.

## Fallback/Next Decision

If the Run fails contract, smoke, shape, or numerical checks, classify the failure and submit at most a targeted repair preserving this hypothesis. If it completes but collapses, is non-finite, or clearly plateaus far below the temporal/Radon branches with weak source behavior, stop this exact high-resolution change-skip formulation and broaden to another modern temporal backbone or recurrent change block. If it is finite and late-improving but below ABI-223/238, consider one late36 close continuation only if the approved budget policy criteria are met.
