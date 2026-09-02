# ABI-127: ASPP/detail BCE-Dice with Line and Centerline auxiliary supervision

## Hypothesis

ABI-126 showed that the compact full-spectral BTD ASPP/detail decoder with trusted `bce_dice` loss produces a high-precision, high-connectivity, Google-strong operating point, but loses MIT recall relative to ABI-121. Adding a second low-weight provider-derived Line Target auxiliary head to ABI-126 may broaden thin-contrail support enough to recover MIT recall while preserving most of ABI-126's BCE-Dice precision/connectivity discipline.

Proposal class: **family-development continuation** within the full-spectral BTD ASPP/detail decoder family.

## Comparison Target

Primary comparison target: ABI-126 (`run_20260831_085615_d05ab3`), because ABI-127 keeps the ABI-126 architecture/training recipe and changes only the auxiliary supervision set.

Secondary context:

- ABI-121 (`run_20260831_041559_43da35`) as the ASPP/detail focal-Tversky recall/source-balance comparator.
- ABI-120 (`run_20260831_033037_bad0bb`) as the ASPP/detail `bce_dice_cldice` precision-forward scout.
- ABI-068 (`run_20260828_010836_4ccc77`) as the local capped aggregate-Dice frequency-gated reference.
- ABI-066 (`run_20260827_230540_bf4ce3`) as the local capped precision/connectivity reference.

## Expected Effect

The Line Target auxiliary head should provide a slightly wider provider-derived line-support signal than the Centerline Target alone. Under `bce_dice`, this is expected to increase recall, especially MIT filtered recall and MIT filtered Dice, without fully reverting to ABI-121's focal-Tversky high-positive-area, lower-connectivity behavior.

Useful outcomes include any of:

- MIT filtered Dice or MIT filtered recall improves over ABI-126 while aggregate filtered Dice remains within about 0.01 of ABI-126.
- Filtered precision remains above roughly 0.43 or filtered connectivity remains above roughly 0.40 while recall improves over ABI-126.
- Source-stratified behavior explains whether ABI-126's MIT under-recall is responsive to line-support auxiliary supervision rather than requiring a new architecture or data policy.

## Implementation Sketch

Start from ABI-126's compact full-spectral BTD ASPP/detail decoder. Preserve the normalized raw+BTD front end, detail/context stem, three-level encoder, ASPP context block, detail-retaining decoder, and final line-aware refinement. Add one `line_logits` 1x1 output head parallel to the existing `mask_logits` and `centerline_logits` heads. Return a dictionary with exactly `mask_logits`, `centerline_logits`, and `line_logits`.

The manifest keeps ABI-126's provider-approved `abi_16ch` input mode, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and trusted `bce_dice` primary loss. It requests provider-derived Centerline and Line auxiliary targets using trusted `weighted_bce` at weight `0.02` each.

## Contract Features Used

- Provider-approved `abi_16ch` ABI Channel Input only; no longitude, latitude, reconstructed coordinates, or Solar Geometry Input.
- Candidate-owned model architecture only.
- Deterministic BTD feature planes are derived solely from provider-approved ABI channels 1-16 inside the model front end.
- Primary output: `mask_logits` with shape `[1, 256, 256]`.
- Trusted primary loss: `bce_dice`.
- Trusted auxiliary targets: `centerline` -> `centerline_logits`, `line` -> `line_logits`, both using provider/Harness-owned `weighted_bce`.
- Provider/Harness-owned `combined_source_balanced` sampling traversal and `random_mirroring` augmentation.
- Harness-owned metrics, Artifact Filters, capped-record selection, resource placement, execution, lifecycle, and prediction retention.

The candidate does not implement data loading, split logic, capped-record selection, sampling, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, filesystem writes, network access, pretrained weights, resource placement, or lifecycle behavior.

## Budget Requested

Use the active capped representative autonomous budget: up to 1,024 train and validation records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, constant learning rate, disabled early stopping, A100 execution under the 3,600-second Docker timeout, and the 25M-parameter smoke ceiling. Expected parameter count is approximately ABI-126 plus one 1x1 auxiliary head, well below 25M.

## Success Criteria

Treat this as capped representative family-development evidence, not full-data promotion evidence. A useful positive result should train finitely, avoid all-negative/all-positive collapse, remain resource-feasible without retries or timeout, and either improve ABI-126's MIT recall/MIT filtered Dice while retaining most precision/connectivity, or provide a clear source-stratified trade-off that informs the next branch.

A strong capped continuation signal would be aggregate filtered Dice near or above ABI-126 (within about 0.01), MIT filtered Dice above ABI-126's 0.3635, filtered recall above ABI-126's 0.3251, and no severe precision/connectivity collapse relative to ABI-126.

## Fallback/Next Decision

If ABI-127 collapses, fails validation/smoke, produces non-finite state, or sharply loses ABI-126's precision/connectivity without recall recovery, stop this Line+Centerline auxiliary ASPP/detail BCE-Dice branch. Prefer a new architecture mechanism for recall recovery or a bounded whole-validation diagnostic of ABI-126/ABI-121 rather than repeating auxiliary-head additions.

If ABI-127 improves MIT recall while retaining ABI-126-like precision/connectivity, consider one further controlled ASPP/detail continuation focused on source balance or a whole-validation failure-bucket diagnostic before any promotion discussion. Do not treat capped evidence as full-data promotion evidence.
