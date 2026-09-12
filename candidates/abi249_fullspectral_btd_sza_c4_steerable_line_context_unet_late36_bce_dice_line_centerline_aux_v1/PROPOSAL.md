# ABI-249 full-spectral BTD+SZA C4 steerable line-context U-Net late36

## Hypothesis

ABI-248 established finite, source-informative evidence for a C4 rotation-shared anisotropic line-context block, but its best checkpoint occurred at the final exploratory epoch. A longer approved late-improving budget may let the exact C4 steerable branch recover recall and continuity while preserving its compact predicted-positive fraction, precision, and source balance. This is a **family-development continuation** of ABI-248, not a promotion claim.

## Comparison Target

The direct parent and comparison target is ABI-248 (`run_20260911_102833_5db7f8`), which reached capped `val/filtered_dice` 0.383829 at epoch 12 with MIT filtered Dice 0.373157, Google filtered Dice 0.411614, filtered precision 0.454139, filtered recall 0.332372, filtered connectivity 0.327777, and a filtered predicted-positive fraction of 0.002652. ABI-202 (`run_20260904_043143_ee0005`) remains mature single-frame frontier context with capped filtered Dice 0.427570 and stronger recall/connectivity. Rotation-aware family context includes ABI-142/143 and ABI-207/208.

## Expected Effect

The expected effect is not an architecture novelty change but an epoch-budget test: if ABI-248 was truncated, ABI-249 should improve filtered Dice, recall, and/or connectivity after epoch 12 without a precision collapse or source-specific degeneration. Useful evidence includes improvement over ABI-248 on capped filtered Dice, source Dice, recall, or connectivity; a late finite trajectory clarifying whether C4 line context needs more optimization; or evidence that the exact branch plateaus and should be replaced by a mechanism-changing recall-preserving variant.

## Implementation Sketch

Use the exact ABI-248 architecture. The model consumes provider-approved `abi_16ch_plus_sza` tensors, normalizes ABI channels, appends approved-channel thermal BTD planes plus scaled/cosine Solar Geometry Input, and learns a small 1x1 channel mixer. A compact U-Net/ASPP encoder-decoder fuses signed-detail and full-resolution decoder features. The C4 steerable line-context block rotates feature maps by 0/90/180/270 degrees, applies a shared anisotropic strip-context subnetwork to each orientation, inverse-rotates features, and fuses orientation contexts with learned soft weights plus mean/max summaries. The model emits primary `mask_logits` and trusted auxiliary `line_logits`/`centerline_logits`.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza`; no longitude/latitude or Dataset Source identity.
- Provider-owned sampling: `combined_source_balanced` with `all_target_frames` frame selection.
- Provider-owned augmentation: `random_mirroring` only.
- Trusted loss/optimizer/scheduler: `bce_dice`, AdamW, constant learning rate.
- Trusted auxiliary targets: Line Target and Centerline Target via `weighted_bce`.
- Candidate-local `budget_request.yaml` requesting approved `late_improving` budget class with `requested_max_epochs: 36` and parent Run `run_20260911_102833_5db7f8`.
- Candidate code defines architecture only; it does not implement data loading, target derivation, losses, metrics, Artifact Filters, postprocessing, thresholding, sampling, augmentation transforms, training loops, downloads, filesystem probes, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Budget Requested

Request the approved `late_improving` budget: 36 epochs and the trusted late-improving wall-clock limit, with fallback to the exploratory budget if denied. The manifest retains `max_epochs: 12` because the Harness-owned budget request, not Candidate code, authorizes any extension. Keep batch size 4, constant learning rate 0.0003, disabled early stopping, and the current Harness-owned sample/resource ceilings.

## Success Criteria

Treat ABI-249 as useful family-development evidence if it completes finitely and improves ABI-248 on capped `val/filtered_dice` by about 0.005 or more, improves recall or connectivity without material precision/source-balance collapse, or shows a clear late trajectory that distinguishes budget truncation from plateau. A score approaching the ABI-202/ABI-223 frontier would justify considering trusted whole-validation diagnostics; a finite but plateaued or degraded result should stop the exact C4 late-budget branch and redirect to a mechanism-changing recall-preserving C4/detail variant or broader architecture scout.

## Fallback/Next Decision

If the late-improving request is denied, treat the exploratory-budget Run as the valid bounded result. If ABI-249 fails due to a Candidate bug while preserving the hypothesis, submit at most one narrow repair. If it completes but does not improve overlap/recall/connectivity, stop the exact unchanged C4 steerable continuation and broaden rather than repeat local budget or auxiliary-head tweaks. If the contract blocks richer group-equivariant operators, create a Capability Request instead of bypassing the boundary.
