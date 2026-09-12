# ABI-242 temporal recurrent change-state U-Net

## Hypothesis

A compact recurrent temporal state can improve the temporal frontier's recall/connectivity balance by explicitly integrating previous, center, and next ABI+SZA frame evidence around the center ABI Patch. ABI-239/240 showed that low-resolution temporal line accumulation can recover overlap and recall under a longer budget but struggles with selected-checkpoint connectivity. ABI-241 showed that full-resolution temporal-difference skip injection is finite but appears to fragment change evidence rather than preserve coherent line support. A bidirectional ConvGRU-style state over provider-owned frames should offer a different mechanism: learn persistence/change memory at full resolution before the encoder, then let the decoder operate on a single center-anchored temporal state.

This is a **family-development continuation** within the provider-owned temporal modeling frontier, but it is materially different from ABI-239/240 and ABI-241. It uses a compact recurrent state update instead of low-resolution line accumulation, post-decoder directional context, or independent multi-scale change skips.

## Comparison Target

Primary comparison targets are:

- ABI-241 (`run_20260911_050449_17cdcb`), the high-resolution change-skip scout: best capped `val/filtered_dice` 0.384180, filtered recall 0.369412, filtered connectivity 0.238980.
- ABI-240 (`run_20260911_031326_43ed12`), the late36 low-resolution temporal line-accumulator branch: best capped `val/filtered_dice` 0.414892, filtered recall 0.395534, filtered connectivity 0.264863.
- ABI-238 (`run_20260911_004137_f54c45`), the temporal-attention directional-context late36 branch: best capped `val/filtered_dice` 0.420235, filtered connectivity 0.352239.
- ABI-223 (`run_20260908_154531_8c7e2b`), the mature temporal-attention late36 branch: best capped `val/filtered_dice` 0.419776, filtered connectivity 0.412427.
- ABI-202 (`run_20260904_043143_ee0005`) remains the single-frame frontier context, not the sole elimination gate for this exploratory temporal continuation.

## Expected Effect

Expected favorable signal: compared with ABI-241, the recurrent state should reduce fragmented positives by integrating temporal change through gated memory before encoder downsampling rather than injecting independent change skips at multiple scales. Compared with ABI-240, it should keep recall competitive while improving selected-checkpoint connectivity by preserving framewise persistence evidence at 256x256 resolution. Compared with ABI-223/238, it should test whether learned temporal memory offers a better recall/continuity tradeoff than per-pixel temporal attention alone.

A successful exploratory Result need not beat ABI-202 immediately. It should be finite, noncollapsed, source-informative, and either approach the ABI-223/238 capped Dice band or show a better recall/connectivity tradeoff than ABI-241/240 at comparable predicted-positive fraction.

## Implementation Sketch

The Candidate consumes `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` using only provider-supplied ABI channels 1-16 plus per-frame Solar Geometry Input. Per-frame normalized ABI, BTD, and SZA features are built inside the model from candidate-visible channels only.

A shared per-frame projection maps previous, center, and next features into a compact 24-channel embedding. A forward ConvGRU cell processes previous -> center -> next, while a separate backward ConvGRU cell processes next -> center -> previous. The center states from both directions are averaged into a center-anchored recurrent state. Explicit candidate-visible temporal-change features (center minus neighbor mean, next minus previous, and absolute center/neighbor differences) are projected separately. A learned gate combines the center embedding with recurrent temporal state and change evidence, and the fused representation enters a compact U-Net encoder, ASPP bottleneck, and decoder. The model returns `mask_logits`, `line_logits`, and `centerline_logits` only.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Data policy: `frame_selection_policy: temporal_eligible_center`, `temporal_frame_offsets: [-1, 0, 1]`, `sampling_policy: combined_source_balanced`, `augmentation_policy: random_mirroring`.
- Output form: `mask_logits` plus trusted Line and Centerline auxiliary outputs.
- Loss: trusted `bce_dice` primary loss with provider-owned `weighted_bce` auxiliary losses.
- Optimizer/scheduler: AdamW with constant learning rate.
- Candidate code owns only PyTorch model architecture. It does not implement data loading, temporal lookup, cache reads, missing-frame fallback, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Budget Requested

Exploratory default budget only: 12 epochs, batch size 2, constant learning rate, and current Harness-owned resource ceilings. No late-improving budget is requested for this first recurrent-change-state scout. If it is finite, noncollapsed, source-informative, and selects its best checkpoint at or near epoch 12 with an improving or ambiguous trajectory, a later close continuation may request the approved late-improving budget.

## Success Criteria

Continue developing this branch if ABI-242 completes successfully and shows at least one of:

- capped `val/filtered_dice` near the temporal frontier neighborhood, roughly within 0.02 of ABI-223/238, while remaining source-informative on MIT and Google;
- a materially better connectivity/recall balance than ABI-241 and ABI-240, especially filtered connectivity above ABI-240's 0.264863 without severe recall collapse;
- a late-improving trajectory with best checkpoint at epoch 12, finite predictions, and no all-negative/all-positive degeneration;
- diagnostically useful source behavior suggesting recurrent temporal state improves MIT or Google temporal failure modes.

Do not require this exploratory recurrent scout to beat the mature ABI-202 single-frame Result before considering one bounded continuation.

## Fallback/Next Decision

If the Run fails contract, smoke, shape, or numerical checks, classify the failure and submit at most a targeted repair preserving this hypothesis. If it completes but collapses, is non-finite, or clearly plateaus far below the temporal/Radon branches with weak source behavior, stop this exact recurrent-change formulation and broaden to another modern lightweight backbone, a five-frame temporal scout, or a different continuity-preserving temporal/Radon hybrid. If it is finite and late-improving but below ABI-223/238, consider one late36 close continuation only if the approved budget policy criteria are met.
