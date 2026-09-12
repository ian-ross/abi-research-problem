# ABI-250 full-spectral BTD+SZA C4 recall-bridge U-Net

## Hypothesis

ABI-249 showed that the C4 rotation-shared line-context family can reach strong whole-validation precision and compact false-positive behavior, but it trails ABI-202 mainly because fixed-threshold recall and connectivity are too low, especially on MIT. ABI-250 tests whether a mechanism-changing high-resolution support bridge before the C4 head can recover true contrail coverage while preserving the C4 orientation prior's precision discipline. This is a **family-development continuation**, not a promotion claim.

## Comparison Target

The direct family target is ABI-249 (`run_20260911_111909_dd7ef7`), which reached capped `val/filtered_dice` 0.416400 at epoch 31 and whole-validation filtered Dice 0.4197, with strong precision but lower recall/connectivity than ABI-202. ABI-248 (`run_20260911_102833_5db7f8`) is the exploratory C4 parent. ABI-202 (`run_20260904_043143_ee0005`) remains the aggregate whole-validation frontier context, and ABI-184 remains the negative-patch/connectivity comparator.

## Expected Effect

The added full-scale fusion and zero-initialized recall bridge should feed the C4 line-context head with decoder, signed-detail, stem, and all-scale support features rather than the parent decoder/detail/stem fusion alone. Expected benefits are higher filtered recall, MIT filtered Dice, and connectivity relative to ABI-249. The risk is that extra high-resolution support increases false positives and erodes ABI-249's precision advantage.

## Implementation Sketch

Start from the ABI-249 architecture and keep the approved `abi_16ch_plus_sza` input, normalized raw ABI/SZA plus ABI-channel-derived BTD front end, C4 rotation-shared anisotropic line-context head, trusted Line and Centerline auxiliary outputs, BCE-Dice loss, AdamW constant learning rate, batch size 4, source-balanced sampling, and trusted random mirroring.

Add two architecture-only modules: `FullScaleSkipFusion`, which projects stem, encoder, context, decoder, and high-resolution detail features to mask resolution and fuses them with convolutions; and `RecallPreservingSupportBridge`, which combines decoder, signed-detail, full-scale support, horizontal/vertical line context, and a learned sigmoid feature gate. Its residual projection is zero-initialized and bounded by `tanh`; it does not threshold, postprocess, filter, derive targets, or alter sampling.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza`; no longitude/latitude, Dataset Source identity, scene identity, or route/location priors.
- Provider-owned sampling: `combined_source_balanced` with `all_target_frames` frame selection.
- Provider-owned augmentation: `random_mirroring` only.
- Trusted loss/optimizer/scheduler: `bce_dice`, AdamW, constant learning rate.
- Trusted auxiliary targets: Line Target and Centerline Target via `weighted_bce`.
- Candidate code defines architecture only; it does not implement data loading, target derivation, losses, metrics, Artifact Filters, postprocessing, thresholding, sampling, augmentation transforms, training loops, downloads, filesystem probes, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Budget Requested

Use the default exploratory budget: 12 epochs, batch size 4, constant learning rate, disabled early stopping, provider-owned capped selection, and the configured A100 execution policy. Do not request the late-improving budget on this first mechanism-changing branch; if ABI-250 is finite, non-collapsed, and late-improving, a later step can decide whether a late36 continuation is justified.

## Success Criteria

Treat ABI-250 as useful family-development evidence if it completes finitely and is source-informative, and if it improves recall, connectivity, or MIT filtered Dice relative to ABI-249's weakness without a large precision collapse. A capped `val/filtered_dice` in the high 0.39s or better with an improving or ambiguous trajectory would keep the branch eligible for bounded continuation. Promotion would require later whole-validation evidence and operator review; capped evidence alone is not promotion evidence.

## Fallback/Next Decision

If ABI-250 fails contract, smoke, numerical, or resource validation, repair the exact bug only if the C4 recall-bridge hypothesis is preserved. If it completes but collapses or clearly loses ABI-249's precision without recovering recall/connectivity, stop this branch and broaden again rather than shuffling auxiliary heads. If it is finite and late-improving at epoch 12, consider a late36 close-continuation in a future Autonomy Step.
