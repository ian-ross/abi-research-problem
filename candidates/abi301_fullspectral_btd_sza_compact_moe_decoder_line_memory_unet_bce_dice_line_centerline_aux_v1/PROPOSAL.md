# ABI-301 compact MoE decoder line-memory U-Net

## Hypothesis

Family-development continuation. ABI-269 showed that the compact spectral/Solar Geometry Input MoE branch can recover aggregate/source balance under longer training, but its connected-line continuity remained weak. ABI-270 showed that appending a conservative multi-orientation consensus head at the final high-resolution stage does not repair that weakness. ABI-301 tests whether integrating lightweight multi-orientation line memory through decoder stages, before final logits are formed, can couple continuity support to recall rather than treating line evidence as a late veto/head.

## Comparison Target

Primary comparison target is the compact MoE lineage: ABI-269 late36 (`run_20260912_121857_19f67d`) and ABI-270 exploratory (`run_20260912_151011_98165f`). Secondary context is ABI-265 selective axial line-memory, ABI-249 C4/rotation-aware comparator, and ABI-202 aggregate reference.

## Expected Effect

Expected capped exploratory effect is higher connected-line continuity than ABI-269/270 while retaining at least ABI-268/269-like source balance and avoiding ABI-270's large precision/source drop. The desired mechanism is decoder-level recurrent line support that shapes region evidence before the final mask head, not Candidate-owned thresholding or postprocessing.

## Implementation Sketch

Start from the resource-profiled compact ABI+SZA BTD/Solar Geometry Input MoE U-Net body. Replace the final-only orientation-consensus head with a `DirectionalLineMemoryBlock` inserted in decoder stages and final fusion. The block uses horizontal, vertical, local diagonal, and dilated diagonal depthwise branches, learns branch agreement from internal logits, and gates a residual memory update. The final head emits `mask_logits`, `line_logits`, and `centerline_logits`; the mask receives only small bounded auxiliary-logit support.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza`; no longitude/latitude channels.
- `output_form: mask_logits` with trusted Line and Centerline auxiliary targets.
- Trusted `combined_source_balanced` sampling and `random_mirroring` augmentation.
- Trusted `bce_dice` primary loss, AdamW optimizer, constant learning-rate scheduler.
- Candidate code defines architecture only and does not implement data loading, sample selection, augmentation, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, downloads, Dataset Source identity, coordinates, resource placement, or lifecycle control.

## Budget Requested

Exploratory/default budget only: 12 epochs, batch size 4, constant learning rate. No late-improving budget is requested for this first integrated decoder-line-memory test.

## Success Criteria

Continue this exact branch only if the capped Run is finite, non-collapsed, source-informative, and either: (1) improves ABI-269/270 connectivity without a major filtered-Dice/source-balance loss, or (2) shows a late, improving trajectory where recall and connectivity rise together. A promotion-like result would need to approach ABI-249/202 aggregate/source scores while adding connectivity evidence, but beating mature incumbents is not required for this exploratory mechanism test.

## Fallback/Next Decision

If ABI-301 repeats ABI-270's lower precision/source-balance result, peaks early, or merely trades recall against connectivity, stop this compact MoE line-continuity branch rather than requesting an unchanged late36 continuation. Future work should broaden to a different mechanism, such as temporal attention with recall-preserving line organization or a C4/orientation prior with earlier evidence calibration.
