# ABI-342 full-spectral BTD+SZA C4 recall bridge late36

## Hypothesis

ABI-249 showed that single-frame C4/rotation-shared line context can produce compact, high-precision predictions, but its fixed-threshold recall remains below the ABI-202 aggregate reference and the ABI-223 temporal-attention diagnostic comparator. ABI-341 showed that recall routing can reduce positive-tail misses, but broad temporal soft-band lifting creates unacceptable negative-patch clutter and weak connectivity. ABI-342 tests a narrower non-temporal mechanism: keep ABI-249's compact C4 orientation prior as the anchor, then add a bounded signed recall residual that is continuously gated by C4 line context and trusted Line auxiliary evidence. The hypothesis is that orientation-supported evidence can raise true thin-line logits at threshold 0.5 while avoiding the broad-footprint failure mode of recent temporal recall routers.

This is a **family-development continuation** of the C4/orientation-prior branch, not a promotion claim.

## Comparison Target

The direct comparison target is ABI-249 (`run_20260911_111909_dd7ef7`), the high-precision C4 comparator. ABI-249 reached capped best `val/filtered_dice` 0.4164 at epoch 31 with MIT filtered Dice 0.3964, Google filtered Dice 0.4689, filtered precision 0.4809, filtered recall 0.3672, filtered connectivity 0.3925, and compact filtered predicted-positive fraction. Whole-validation diagnostics later gave filtered Dice 0.4197, precision 0.4865, recall 0.3690, and connectivity 0.3975. ABI-202 remains aggregate whole-validation reference context; ABI-223 remains temporal-eligible temporal-attention context; ABI-341 is negative evidence for broad temporal recall routing.

## Expected Effect

Expected useful evidence is improved fixed-threshold recall over ABI-249 without losing its compact precision and source balance. A successful run should move recall toward ABI-202/ABI-223 levels while keeping filtered precision close to ABI-249 and avoiding the ABI-341 pattern of many additional negative-patch false-positive pixels. A neutral or negative result would still clarify whether C4 orientation priors can support recall repair without temporal context.

## Implementation Sketch

Start from the ABI-249 architecture. The model consumes only provider-approved `abi_16ch_plus_sza` tensors, normalizes ABI channels, appends ABI-channel-derived thermal BTD planes plus scaled/cosine Solar Geometry Input, and uses a learned 1x1 channel mixer. A compact U-Net/ASPP encoder-decoder fuses signed-detail, context, and full-resolution features. The C4 line-context block rotates decoder features by 0/90/180/270 degrees, applies a shared anisotropic strip block, inverse-rotates the features, and fuses learned weighted/mean/max orientation context.

The architectural change is `C4RecallBridgeMaskHead`. It produces an ABI-249-like compact anchor mask from the decoded features plus C4 line context. A second recall branch sees the anchor features, C4 line context, and signed local detail. The final `mask_logits` are the anchor logits plus a bounded signed residual (`0.75 * tanh(delta)`) multiplied by a continuous evidence gate derived from anchor, line-context, recall features, and the model's Line auxiliary logits. This is model architecture, not thresholding or postprocessing.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza`; no longitude, latitude, Dataset Source identity, scene identity, or route/location prior.
- Provider-owned data selection: `combined_source_balanced` sampling with `all_target_frames` frame selection.
- Provider-owned augmentation: `random_mirroring` only.
- Trusted loss/optimizer/scheduler: `bce_dice`, AdamW, constant learning rate.
- Trusted auxiliary targets: Line Target and Centerline Target through `weighted_bce` with manifest-declared weights.
- Candidate-local `budget_request.yaml` requests the approved `late_improving` budget class with `requested_max_epochs: 36` because the direct C4 parent ABI-249 selected epoch 31 as best.
- Candidate code defines architecture only; it does not implement data loading, target derivation, losses, metrics, Artifact Filters, postprocessing, thresholding, sampling, augmentation transforms, training loops, downloads, filesystem probes, coordinates, resource scheduling, or lifecycle behavior.

## Budget Requested

Request the approved `late_improving` budget: 36 epochs and the trusted late-improving wall-clock limit, with fallback to the exploratory budget if denied. The manifest keeps `max_epochs: 12` because the Harness-owned budget request, not Candidate code, authorizes any extension. Keep batch size 4, learning rate 0.0003, disabled early stopping, current sample ceilings, four retained predictions, and the Harness-owned GPU/resource policy.

## Success Criteria

Treat ABI-342 as useful C4-family evidence if it completes finitely and improves ABI-249's capped filtered recall by at least about 0.015 without dropping filtered precision below roughly 0.45, or improves capped filtered Dice/connectivity without a material source-specific collapse. A strong result near or above ABI-249 aggregate Dice with higher recall would justify a trusted diagnostic request. A finite but cluttered result, especially one with ABI-341-like broad predicted-positive inflation, should stop this exact recall-bridge head.

## Fallback/Next Decision

If the late-improving request is denied, treat the exploratory-budget Run as valid bounded evidence. If the candidate fails from a narrow Candidate bug while preserving the hypothesis, allow at most one repair. If it completes but merely trades ABI-249 precision/connectivity for noisy broad recall, do not repeat simple residual/gate scaling; broaden to temporal attention evidence sharpening, a different line-continuity mechanism, or a data/loss/augmentation policy allowed by the trusted contract. If richer group-equivariant operators or new calibration/loss behavior are required, write a Capability Request instead of bypassing the boundary.
