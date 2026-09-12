# ABI-248 full-spectral BTD+SZA C4 steerable line-context U-Net

## Hypothesis

A compact group-shared, rotation-aware line-context block can improve thin-contrail continuity and orientation robustness relative to hand-separated horizontal/vertical line refiners without moving Artifact Filtering, thresholding, morphology, or data augmentation into Candidate code. This is a **family scout** in the underexplored rotation-aware line-network direction, not a promotion candidate expected to immediately beat the mature ABI-202 late36 single-frame frontier.

## Comparison Target

Primary comparison target is the current whole-validation-tested frontier, ABI-202 (`run_20260904_043143_ee0005`, whole-validation filtered Dice 0.4312; capped best `val/filtered_dice` 0.4276). Family-context comparisons are ABI-142/143 rotation/ridge-style single-frame scouts and ABI-207/208 directional-message U-Net variants, which showed resource-safe source-informative behavior but did not establish a C4 parameter-shared steerable line branch.

## Expected Effect

The candidate should preserve the source-balanced precision/recall discipline of the full-spectral BTD+SZA BCE-Dice ASPP family while improving orientation balance and Contrail Connectivity Metric through a differentiable C4 line-context module. Success does not require beating ABI-202 on the first scout; useful evidence includes finite training, non-collapsed predictions, filtered Dice within the broader single-frame scout band, improved connectivity or source balance over ABI-207/208-like directional U-Nets, or a late/ambiguous trajectory justifying bounded family development.

## Implementation Sketch

Use provider-approved `abi_16ch_plus_sza` tensors. Normalize ABI channels, append approved-channel thermal BTD planes, add scaled/cosine Solar Geometry Input, and learn a small 1x1 channel mixer. Feed the resulting features through a compact U-Net/ASPP encoder-decoder. At full resolution, fuse decoder, signed-detail, and stem features, then apply a C4 steerable line-context block: rotate feature maps by 0/90/180/270 degrees, apply a shared anisotropic strip-context subnetwork to each orientation, inverse-rotate features, and fuse orientation contexts with learned soft weights plus mean/max summaries. Emit primary `mask_logits` and trusted auxiliary `line_logits`/`centerline_logits`.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza`; no longitude/latitude or Dataset Source identity.
- Provider-owned sampling: `combined_source_balanced` with `all_target_frames` frame selection.
- Provider-owned augmentation: `random_mirroring` only.
- Trusted loss/optimizer/scheduler: `bce_dice`, AdamW, constant learning rate.
- Trusted auxiliary targets: Line Target and Centerline Target via `weighted_bce`.
- Candidate code defines architecture only; it does not implement data loading, temporal lookup, target derivation, losses, metrics, Artifact Filters, postprocessing, thresholding, sampling, augmentation transforms, training loops, downloads, filesystem probes, coordinates, or resource scheduling.

## Budget Requested

Exploratory default budget: 12 epochs, batch size 4, 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, constant learning rate, no early stopping, pinned trusted execution resources. No late-improving budget is requested for this first C4 steerable scout.

## Success Criteria

Treat the Result as promising family evidence if it completes without contract/smoke/numerical/resource failure, remains noncollapsed, and either (a) reaches roughly the best broad single-frame scout range (`val/filtered_dice` about 0.38 or better), (b) improves filtered connectivity/source balance relative to ABI-207/208-style directional-message U-Nets at comparable Dice, or (c) has a final/late best checkpoint with source-informative metrics and no degeneracy that supports one bounded continuation. A lower but finite result with a clear optimization trajectory may still justify one mechanism-changing continuation; persistent collapse, non-finite behavior, resource infeasibility, or clearly poor source-stratified metrics would stop this exact scout.

## Fallback/Next Decision

If ABI-248 is finite but weak, record a Research Note and either stop the exact C4 steerable formulation or change the mechanism toward richer learned orientation banks/diagonal context. If it is competitive or diagnostically strong, consider one family-development continuation or a late-improving budget only if the selected checkpoint and trajectory satisfy the approved late-improving criteria. If it fails for a Candidate bug while preserving the hypothesis, submit at most a repair candidate; if the contract blocks richer group-equivariant operators, create a Capability Request instead of bypassing the boundary.
