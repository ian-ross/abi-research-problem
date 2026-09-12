# ABI-243 temporal recurrent line-state U-Net

## Hypothesis

A continuity-preserving oriented line-state pyramid coupled into the decoder can recover the weak Contrail Connectivity Metric observed in ABI-242's recurrent temporal scout without discarding its final-epoch overlap/recall learning signal. ABI-242 showed that a compact bidirectional ConvGRU over provider-owned previous/center/next ABI+SZA frames was finite, source-informative, and best at epoch 12, but selected-checkpoint connectivity was only 0.201293. ABI-241's independent high-resolution change skips and ABI-239/240's low-resolution line accumulator also failed to preserve selected-checkpoint line continuity. ABI-243 keeps ABI-242's recurrent temporal stem but adds an architecture-internal, differentiable, full-resolution oriented line-state branch that is carried through U-Net skip scales and gates decoder fusion.

This is a **family-development continuation** within the temporal recurrent/change frontier. It is not an unchanged late-budget repeat of ABI-242; it changes the continuity mechanism while keeping the trusted temporal input, loss, sampling, augmentation, optimizer, and auxiliary-output policy fixed.

## Comparison Target

Primary comparison targets are:

- ABI-242 (`run_20260911_055200_52c75f`), recurrent change-state scout: best capped `val/filtered_dice` 0.376521, filtered recall 0.368620, filtered connectivity 0.201293, best epoch 12.
- ABI-241 (`run_20260911_050449_17cdcb`), high-resolution change-skip scout: best capped `val/filtered_dice` 0.384180, filtered recall 0.369412, filtered connectivity 0.238980.
- ABI-240 (`run_20260911_031326_43ed12`), late36 temporal line-accumulator branch: best capped `val/filtered_dice` 0.414892, filtered recall 0.395534, filtered connectivity 0.264863.
- ABI-223/238 temporal-attention late36 Results remain the mature temporal frontier, with ABI-223 connectivity 0.412427 and ABI-238 filtered Dice 0.420235.
- ABI-202 (`run_20260904_043143_ee0005`) remains the single-frame frontier context, not the sole elimination gate for this exploratory continuation.

## Expected Effect

The oriented line-state branch should make decoder features less fragmented by preserving horizontal, vertical, and longer dilated local-line evidence at full resolution and at each skip scale. Compared with ABI-242, the desired effect is higher selected-checkpoint connectivity and precision at similar recall and predicted-positive fraction. Compared with ABI-241 and ABI-240, the line-state decoder coupling should test whether line continuity is better protected when it is a persistent feature path rather than a post-hoc line accumulator or independent change skip.

A successful exploratory Result need not beat ABI-202 immediately. It should complete finite/resource-safe training, avoid prediction collapse, remain source-informative on both MIT and Google, and show either a better connectivity/recall balance than ABI-242/241 or a late-improving trajectory that justifies one future close continuation.

## Implementation Sketch

The Candidate consumes `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` using only provider-supplied ABI channels 1-16 plus per-frame Solar Geometry Input. Per-frame normalized ABI, approved-channel brightness-temperature-difference features, and SZA features are built from candidate-visible channels only.

ABI-243 keeps ABI-242's bidirectional ConvGRU-style temporal stem: previous, center, and next frame embeddings are processed by forward/backward convolutional recurrent cells; the center state is fused with explicit signed and absolute temporal-change evidence. The new architecture-internal line-state path applies differentiable oriented depthwise convolution branches to the full-resolution temporal stem, including horizontal, vertical, and dilated local-line branches. That line state is downsampled into a pyramid aligned with the U-Net skip scales. Decoder fusion gates each encoder skip against the matching line-state feature, and the bottleneck is similarly gated with the coarsest line state. The final mask head receives a line-refined feature, while trusted `line_logits` and `centerline_logits` auxiliary heads are returned for provider-owned auxiliary losses.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Data policy: `frame_selection_policy: temporal_eligible_center`, `temporal_frame_offsets: [-1, 0, 1]`, `sampling_policy: combined_source_balanced`, `augmentation_policy: random_mirroring`.
- Output form: `mask_logits` plus trusted Line and Centerline auxiliary outputs.
- Loss: trusted `bce_dice` primary loss with provider-owned `weighted_bce` auxiliary losses.
- Optimizer/scheduler: AdamW with constant learning rate.
- Candidate code owns only PyTorch model architecture. It does not implement data loading, temporal lookup, cache reads, missing-frame fallback, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Budget Requested

Exploratory default budget only: 12 epochs, batch size 2, constant learning rate, and current Harness-owned resource ceilings. No late-improving budget is requested because ABI-243 changes the continuity mechanism relative to ABI-242. If it is finite, noncollapsed, source-informative, and selects its best checkpoint at or near epoch 12 with an improving or ambiguous trajectory, a later close continuation may request the approved late-improving budget.

## Success Criteria

Continue developing this branch if ABI-243 completes successfully and shows at least one of:

- improved selected-checkpoint filtered connectivity over ABI-242's 0.201293 and preferably over ABI-241's 0.238980 without a severe recall drop;
- capped `val/filtered_dice` at least comparable to ABI-242/241 while improving precision or predicted-positive compactness;
- source-informative MIT and Google filtered Dice/recall with no all-negative or all-positive degeneration;
- a late-improving or ambiguous trajectory with best checkpoint near epoch 12 that would justify a future close late36 budget request.

Do not require this exploratory continuation to beat the mature ABI-202 or ABI-223/238 Results before considering one bounded follow-up.

## Fallback/Next Decision

If the Run fails contract, smoke, shape, numerical, or resource checks, classify the failure and submit at most a targeted repair preserving this hypothesis. If it completes but collapses, clearly plateaus, or remains connectivity-weak while losing ABI-242's overlap/recall signal, stop this exact line-state coupling and broaden to a five-frame temporal scout or a modern lightweight temporal backbone. If it improves connectivity but remains budget-truncated at epoch 12, consider one close late36 continuation under the approved late-improving budget policy.
