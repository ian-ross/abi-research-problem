# Proposal: ABI-251 full-spectral BTD+SZA line-memory U-NetFormer

## Classification

Family scout — modern lightweight segmentation backbone with local shifted-window attention plus global line-memory context. This broadens away from the recently saturated ABI-202/184 ASPP/detail/refiner frontier and away from the exact ABI-249 C4 support-bridge continuation that ABI-250 failed to improve.

## Hypothesis

Thin contrail segmentation may benefit from a compact U-NetFormer-style backbone that can exchange evidence across local attention windows while also carrying long row/column line context. ABI-244 showed shifted-window attention is trainable and recall-positive in the temporal setting, but did not improve connectivity; ABI-249 showed orientation/line priors can produce compact high-precision predictions, but ABI-250's high-resolution C4 bridge was costly and negative. ABI-251 tests a different, lower-cost line-continuity mechanism: differentiable row/column line-memory blocks inside a single-frame ABI+SZA shifted-window encoder-decoder.

## Comparison Target

- Primary frontier context: ABI-202 (`run_20260904_043143_ee0005`) for aggregate capped/whole-validation filtered Dice, recall, and connectivity.
- High-precision line-prior context: ABI-249 (`run_20260911_111909_dd7ef7`) for compact prediction and precision behavior.
- Modern attention resource/mechanism context: ABI-244 (`run_20260911_072719_ade068`) for shifted-window attention compatibility.
- Negative local continuation context: ABI-250 (`run_20260911_135022_457598`) for the failed C4 recall-bridge mechanism this scout avoids.

## Expected Effect

The shifted-window encoder should preserve local thin-line evidence while allowing local neighborhoods to cross fixed window seams. The row/column line-memory blocks should improve continuity and connected support without C4 rotation-sharing cost or candidate-owned postprocessing. The calibrated recall/precision feature-fusion head should raise useful contrail logits at the fixed primary threshold while retaining some of ABI-249's compact high-precision discipline.

Expected useful evidence is source-informative, non-collapsed capped validation with a recall/connectivity profile that is competitive with recent line-prior and modern-attention scouts, even if this first scout does not beat the mature ABI-202 frontier.

## Contract Features Used

- Provider-approved input mode: `abi_16ch_plus_sza` with GOES ABI channels 1-16 plus Solar Geometry Input only.
- Manifest-selected trusted sampling: `combined_source_balanced`.
- Manifest-selected trusted frame policy: `all_target_frames`.
- Manifest-selected trusted augmentation: `random_mirroring`.
- Manifest-selected trusted primary loss: `bce_dice`.
- Manifest-declared trusted auxiliary targets: Line Target (`line_logits`, weighted BCE 0.01) and Centerline Target (`centerline_logits`, weighted BCE 0.02).
- Harness-owned AdamW optimizer, constant learning-rate scheduler, batch size 4, and 12-epoch exploratory budget.

Candidate code remains architecture-only. It must not implement data loading, target derivation, custom losses, metrics, Artifact Filters, morphology, thresholding, postprocessing, augmentation transforms, sampling policies, training loops, downloads, filesystem probes, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Implementation Sketch

- Build normalized ABI channels, approved-channel thermal BTD planes, scaled/cosine Solar Geometry Input, and learned 1x1 channel-mixer features inside the model.
- Use a compact hierarchical U-NetFormer encoder-decoder with shifted-window self-attention at each scale.
- Add differentiable `LineMemoryBlock` modules that combine horizontal/vertical depthwise strip context with row/column pooled feature memory.
- Use trusted Line and Centerline auxiliary outputs declared in the manifest.
- Use a calibrated recall/precision feature-fusion head that operates only on learned features and emits logits; it does not change thresholds or postprocess masks.

## Budget

Default exploratory budget: 12 epochs, batch size 4, constant learning rate, capped provider-selected records. No late-improving budget request in the initial scout.

## Success Criteria

Success does not require beating ABI-202 immediately. A useful scout result would be finite, non-collapsed, source-informative learning with bounded predicted-positive fractions and at least one of:

- filtered Dice within roughly 0.03 of ABI-202 while showing competitive recall/connectivity;
- a precision/recall tradeoff that complements ABI-249 without ABI-250's resource cost;
- or a late-improving trajectory with best epoch near epoch 12 that justifies one controlled late36 continuation.

Hard stop evidence for this exact branch would include smoke/contract failure, non-finite training, persistent all-negative/all-positive prediction collapse, source-catastrophic behavior, or a clearly plateaued exploratory result far below both the modern-attention and line-prior comparators.

## Fallback Next Decision

If ABI-251 is finite but weaker than comparators with no late-improving trajectory, stop this exact line-memory U-NetFormer branch and broaden to a different underexplored family rather than mutating auxiliary weights. If it is finite and close but truncated, consider one late-improving close-continuation. If it fails contract/smoke due to candidate code, repair the candidate while preserving the same hypothesis and comparison target. If the contract blocks the hypothesis, write a Capability Request instead of bypassing Harness ownership.
