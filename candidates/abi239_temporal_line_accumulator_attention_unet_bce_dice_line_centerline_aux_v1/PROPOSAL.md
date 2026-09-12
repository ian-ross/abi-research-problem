# ABI-239 temporal line-accumulator attention U-Net

## Hypothesis

A low-resolution differentiable multi-orientation line accumulator inserted immediately after ABI-223-style temporal-attention fusion and before encoder downsampling will preserve more thin contrail continuity than ABI-238 post-decoder directional-context bridge. Accumulating line evidence at the feature level should help the temporal branch recover ABI-223 connectivity while keeping the high precision and source-informative behavior seen in ABI-223/ABI-238.

## Comparison Target

Primary comparison is ABI-223 (`run_20260908_154531_8c7e2b`), the current strong temporal-attention family Result under late-improving budget. Secondary context is ABI-238 (`run_20260911_004137_f54c45`), which slightly improved MIT Dice/precision but regressed recall and connectivity after adding post-decoder directional context, and ABI-202 (`run_20260904_043143_ee0005`) as the mature single-frame frontier.

## Expected Effect

The expected favorable signal is higher filtered contrail connectivity and/or recall than ABI-238 at comparable predicted-positive fraction, without source collapse. Because ABI-239 is a new temporal/Radon-hybrid mechanism run under exploratory budget, it is not required to beat ABI-223 late36 or ABI-202 immediately. Useful evidence includes a finite, noncollapsed, source-balanced trajectory; best epoch near the exploratory ceiling; connectivity or recall improvement over ABI-238 exploratory-scale behavior; or clear diagnosis that line accumulation harms temporal attention.

## Implementation Sketch

Start from the compact ABI-223 temporal-attention U-Net over three provider-supplied ABI+SZA frames. Preserve the temporal frame feature builder, temporal attention/change fusion, encoder/ASPP/decoder, and Line/Centerline auxiliary heads. Add a small `LowResolutionLineAccumulator` after temporal fusion: project fused features, average-pool to low resolution, differentiably average shifted feature maps along horizontal, vertical, and diagonal orientation families, upsample the orientation support, and fuse it back with a learned sigmoid residual gate before encoder downsampling. This is architecture-internal tensor computation only, not morphology, thresholding, an Artifact Filter, or postprocessing.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal` with provider-owned channel-stacked temporal frames.
- `data.frame_selection_policy: temporal_eligible_center` and `data.temporal_frame_offsets: [-1, 0, 1]`.
- `data.sampling_policy: combined_source_balanced` and `data.augmentation_policy: random_mirroring`, both trusted provider/Harness policies.
- `output_form: mask_logits` plus trusted `line_logits` and `centerline_logits` auxiliary targets with `weighted_bce` losses.
- Trusted `bce_dice` primary loss, AdamW optimizer, constant learning-rate scheduler, batch size 2, and 12 exploratory epochs.

Candidate source will not implement data loading, temporal lookup, cache probing, target construction, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Budget Requested

Exploratory default budget: 12 epochs, batch size 2, constant learning rate. No late-improving budget is requested because the line accumulator is a material architecture change rather than an unchanged close continuation. If the Run is finite, noncollapsed, and selects its best checkpoint near epoch 12, a later separate Candidate may request the approved late-improving continuation budget.

## Success Criteria

Classify ABI-239 as promising if it completes within resource limits, remains finite and noncollapsed, preserves source-informative MIT and Google filtered Dice, and shows at least one of: improved filtered connectivity or recall relative to ABI-238 connectivity-regressed direction, filtered Dice within roughly 0.03 of ABI-223 late36 despite exploratory budget, or a late-improving trajectory that justifies a close late36 continuation. Promotion would require later evidence comparable to or better than ABI-202/ABI-223 on capped and, if requested, whole-validation diagnostics.

## Fallback/Next Decision

If ABI-239 fails contract/smoke/numerical checks, repair only candidate-code defects while preserving this hypothesis. If it is finite but clearly suppresses recall/connectivity or collapses source-specific performance, stop this exact low-resolution accumulator branch and broaden to a different temporal mechanism or modern lightweight backbone. If it is finite and late-improving but not yet competitive, consider a single late36 continuation under the approved budget-request path. If it ties ABI-223/ABI-238 with better connectivity, consider follow-up diagnostics before promotion claims.
