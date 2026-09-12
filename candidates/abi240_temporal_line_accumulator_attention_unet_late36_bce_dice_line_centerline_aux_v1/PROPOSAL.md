# ABI-240 temporal line-accumulator attention U-Net late36

## Hypothesis

ABI-239's low-resolution differentiable multi-orientation line accumulator improved the ABI-223/ABI-238 matched 12-epoch temporal checkpoints on filtered Dice, recall, MIT Dice, and Google Dice, selected the final exploratory epoch, and ended with declining train and validation losses. A late-improving close continuation should test whether the same pre-encoder temporal/Radon mechanism keeps improving toward the ABI-223 temporal frontier or whether its weak connectivity is a durable branch limitation.

This is a **family-development continuation**, not a promotion candidate and not a new family scout. It intentionally changes only the approved budget request while preserving ABI-239's architecture and trusted data/loss/training choices.

## Comparison Target

Primary comparison is ABI-239 (`run_20260911_023156_f7eb6b`), the exploratory parent that selected epoch 12 with finite, noncollapsed, source-informative metrics. Secondary temporal context is ABI-223 late36 (`run_20260908_154531_8c7e2b`) as the strongest temporal-attention parent and ABI-238 late36 (`run_20260911_004137_f54c45`) as the directional-context continuation that traded away connectivity. ABI-202 (`run_20260904_043143_ee0005`) remains the mature single-frame frontier context.

## Expected Effect

The favorable signal is a late-budget gain over ABI-239 in filtered Dice, recall, and source-stratified Dice, ideally with connectivity moving closer to ABI-223 instead of remaining near ABI-239's exploratory level. Useful evidence does not require beating ABI-202 immediately; it requires a finite, noncollapsed, source-informative trajectory that clarifies whether pre-encoder line accumulation is budget-truncated or intrinsically connectivity-limited.

## Implementation Sketch

Reuse ABI-239's model unchanged: three provider-supplied ABI+SZA frames are converted to per-frame approved-channel/BTD features, fused by temporal attention/change streams, passed through a low-resolution differentiable multi-orientation line accumulator, and decoded by a compact U-Net/ASPP head with Line and Centerline auxiliary outputs. The line accumulator remains internal differentiable model logic, not thresholding, morphology, an Artifact Filter, or postprocessing.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal` with provider-owned channel-stacked temporal frames.
- `data.frame_selection_policy: temporal_eligible_center` and `data.temporal_frame_offsets: [-1, 0, 1]`.
- `data.sampling_policy: combined_source_balanced` and `data.augmentation_policy: random_mirroring`, both trusted provider/Harness policies.
- `output_form: mask_logits` plus trusted `line_logits` and `centerline_logits` auxiliary targets with `weighted_bce` losses.
- Trusted `bce_dice` primary loss, AdamW optimizer, constant learning-rate scheduler, batch size 2, and the manifest exploratory max-epoch field paired with a Harness-validated `late_improving` budget request.

Candidate source will not implement data loading, temporal lookup, cache probing, target construction, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Budget Requested

Request the approved `late_improving` budget for 36 epochs through candidate-local `budget_request.yaml`, with ABI-239 (`run_20260911_023156_f7eb6b`) as parent evidence. If the Harness denies the request, run under the exploratory fallback and treat that bounded Result as valid.

## Success Criteria

Classify ABI-240 as promising if it completes within resource limits, remains finite and noncollapsed, preserves source-informative MIT and Google filtered Dice, and improves ABI-239 by a meaningful margin in filtered Dice/recall while avoiding further connectivity loss. A result approaching ABI-223's late36 filtered Dice or connectivity would justify later diagnostic priority; a result below ABI-223 but clearly above ABI-239 may justify one more controlled architecture continuation.

## Fallback/Next Decision

If ABI-240 fails contract/smoke/numerical checks, repair only candidate-code defects while preserving ABI-239's hypothesis. If it is finite but plateaus below ABI-223 or continues to show weak connectivity despite the longer budget, stop this exact low-resolution line-accumulator branch and broaden to a materially different temporal mechanism or modern lightweight backbone. Promotion or whole-validation diagnostics require later evidence comparable to the ABI-202/ABI-223 frontier, not this budget request alone.
