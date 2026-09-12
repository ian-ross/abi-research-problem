# ABI-264 selective axial line-memory U-Net

## Hypothesis

A compact single-frame architecture with differentiable selective axial line-memory scans can recover some of the line continuity that recent modern-backbone and temporal local-continuity branches missed, while avoiding the activation cost of SegFormer-style high-resolution attention. The model should learn long horizontal/vertical contrail support through gated prefix-averaged feature state, not through Candidate-owned thresholding, postprocessing, morphology, target derivation, losses, metrics, or Artifact Filters.

This is a **family scout** for a low-cost state-space-style line-memory mechanism. It is not expected to beat the mature ABI-202 frontier on the first attempt; continuation should depend on resource safety, nondegeneracy, connectivity/recall evidence, and whether it improves on recent broad scouts with similar budget.

## Comparison Target

Primary comparison targets are recent bounded scouts that motivated broadening:

- ABI-263 (`run_20260912_045029_55c59e`): overlap SegFormer with directional line-state decoder, capped best `val/filtered_dice` 0.3794 and connectivity 0.2747, high memory cost.
- ABI-262 (`run_20260912_040526_92961f`): overlap SegFormer line decoder, capped best 0.3970 with weak connectivity 0.2320.
- ABI-260 (`run_20260912_021616_d20946`): compact MaxViT line-context scout, capped best 0.3815 and connectivity 0.3262.
- ABI-249 (`run_20260911_111909_dd7ef7`) and ABI-202 (`run_20260904_043143_ee0005`) remain stronger C4 and aggregate frontier context, not hard first-scout gates.

## Expected Effect

The selective axial line-memory blocks should propagate learned line evidence across long image rows and columns at multiple U-Net scales. Compared with ABI-262/263, the expected benefit is better fixed-threshold connectivity and comparable or lower resource use because the long-context operation uses prefix averages and 1x1/depthwise convolutions rather than dense attention over large spatial grids. Compared with ABI-260, success would mean similar or better filtered Dice with improved MIT recall/connectivity or a clearer noncollapsed trajectory.

A negative result would still be useful if it shows that low-cost state-space-style line scans do not preserve enough precision/recall balance, helping decide whether future effort should return to temporal diagnostics or other modern backbones.

## Implementation Sketch

Implement `build_model(input_spec, output_spec)` returning a PyTorch module that consumes provider-owned `abi_16ch_plus_sza` tensors. The front end normalizes ABI channels 1-16, adds fixed ABI-channel thermal BTD feature planes derived only from approved channels, includes Solar Geometry Input as scaled/cosine features, and learns a small 1x1 channel mixture.

The encoder-decoder is a compact U-Net. Each scale uses `SelectiveAxialLineMemory`: learned value/gate projections form differentiable prefix-averaged feature states left-to-right, right-to-left, top-to-bottom, and bottom-to-top, then fuse these long-line contexts with local depthwise line convolutions. A signed-detail bridge preserves high-resolution local contrast. The output head returns `mask_logits`, `line_logits`, and `centerline_logits`; the mask logit includes bounded architecture-level recall/line evidence terms only.

## Contract Features Used

- `research_problem: goes_abi_contrail_segmentation`
- `input_mode: abi_16ch_plus_sza`; no longitude or latitude inputs.
- `output_form: mask_logits`.
- Trusted auxiliary targets: Line Target via `line_logits` and Centerline Target via `centerline_logits` with `weighted_bce` weights 0.01 and 0.02.
- Trusted primary loss: `bce_dice`.
- Trusted optimizer/scheduler: AdamW with constant learning rate 0.0003.
- Trusted provider sampling and augmentation: `combined_source_balanced` and `random_mirroring`.
- Batch size 4, max epochs 12, within current exploratory ceilings.

Candidate code defines architecture only. It does not implement data loading, split logic, sampling, augmentation transforms, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, training loops, downloads, filesystem probes, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Budget Requested

Use the default exploratory budget: 12 epochs, batch size 4, constant learning rate, and the active Workspace Configuration's sample, timeout, prediction-retention, GPU, and parameter ceilings. No late-improving budget is requested for this first scout.

## Success Criteria

Continue the mechanism only if the Run is finite, contract-valid, noncollapsed, and at least one of these holds:

- capped `val/filtered_dice` is competitive with recent broad scouts, roughly ABI-260/262 range, while connectivity exceeds ABI-262/263;
- connectivity approaches or exceeds ABI-260 without a large precision/recall collapse;
- MIT and Google filtered Dice are both source-informative and the learning curve is still improving at epoch 12;
- resource use is clearly lower than ABI-263-style high-resolution attention while producing diagnostically useful long-line behavior.

Do not require this first state-space-style scout to beat ABI-202 or ABI-249 before any family-development consideration.

## Fallback/Next Decision

If ABI-264 fails contract or smoke validation, submit a repair only if the original hypothesis and comparison target are preserved. If it completes but collapses, is non-finite, or stays clearly below ABI-260/262 without a connectivity or source-balance advantage, stop this exact selective axial line-memory branch. If it is finite with useful connectivity or late-improving evidence, consider one bounded mechanism-changing continuation or a late-improving request only when the Harness-recorded trajectory justifies it under current policy.
