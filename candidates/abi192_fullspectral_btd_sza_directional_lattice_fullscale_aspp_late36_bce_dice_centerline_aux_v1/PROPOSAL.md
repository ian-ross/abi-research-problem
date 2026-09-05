# ABI-192 Full-Spectral BTD+SZA Directional-Lattice Full-Scale ASPP Late36 BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-192 is a close late-improving continuation of ABI-191, not a promotion claim. It preserves the ABI-191 directional-lattice signed-detail full-scale skip ASPP architecture and changes only the Harness-reviewed budget request. The aim is to test whether ABI-191's final-epoch jump is a real late-learning signal or a noisy capped exploratory fluctuation.

## Hypothesis

ABI-191 selected epoch 12 as its best checkpoint after filtered Dice improved from 0.3567 at epoch 11 to 0.4041 at epoch 12. It stayed finite and non-collapsed, improved filtered recall relative to ABI-181, improved MIT filtered Dice relative to ABI-184/188/189, and avoided the severe connectivity collapse seen in ABI-190. A trusted `late_improving` continuation should determine whether the same directional-lattice bridge can stabilize into ABI-181-level aggregate overlap while retaining better MIT/source-balance behavior, without changing architecture, loss, data policy, augmentation, scheduler, or candidate-owned runtime behavior.

## Comparison Target

The parent and primary within-branch comparison target is ABI-191 `run_20260903_075132_5cff8c`: capped filtered Dice 0.4041, raw Dice 0.4180, MIT/Google filtered Dice 0.3939/0.4297, filtered precision 0.4036, recall 0.4045, connectivity 0.3554, filtered predicted-positive fraction 0.00363, and best checkpoint at epoch 12.

The main family reference is ABI-181 `run_20260902_150611_cbbf35`, the whole-validation-tested aggregate filtered-Dice reference: capped filtered Dice 0.4104, MIT/Google filtered Dice 0.3962/0.4486, filtered precision 0.4423, recall 0.3828, connectivity 0.3639, and filtered predicted-positive fraction 0.00314. ABI-184 `run_20260902_213856_2c04ac` remains the whole-validation-tested precision/connectivity reference with capped filtered Dice 0.4066, precision 0.4850, recall 0.3500, connectivity 0.4634, and predicted-positive fraction 0.00261. ABI-188/189 provide detached line-logit-fusion references, and ABI-068 remains a broader line-U-Net source-balance/connectivity comparator.

## Expected Effect

A positive late36 result would improve ABI-191's aggregate filtered Dice and either approach or exceed ABI-181's capped aggregate filtered Dice while preserving ABI-191's MIT filtered Dice and recall advantages. The strongest result would keep filtered predicted-positive fraction disciplined, recover or improve connectivity toward ABI-181/184, and avoid a precision/Google-source collapse. A useful negative result would show that ABI-191's epoch-12 jump was a noisy ceiling or that continued training turns the directional lattice into the same recall-vs-connectivity tradeoff seen in other line-support branches.

## Implementation Sketch

- Reuse ABI-191 model code unchanged except for the candidate identifier string: normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized/cosine Solar Geometry Input, learned spectral projection, signed local/mid-scale detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, `DirectionalLatticeBridge`, line-aware final refinement, primary `mask_logits`, and provider-derived `centerline_logits` auxiliary output.
- Keep trusted manifest choices identical to ABI-191: `abi_16ch_plus_sza`, `bce_dice`, `combined_source_balanced`, `random_mirroring`, AdamW, learning rate 0.0003, batch size 4, manifest max epochs 12, constant learning rate, and disabled early stopping.
- Add candidate-local `budget_request.yaml` with `schema_version: candidate_budget_request.v1`, `budget_class: late_improving`, `requested_max_epochs: 36`, parent Run `run_20260903_075132_5cff8c`, and `fallback_if_denied: run_exploratory_budget`.
- Do not implement Candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, scheduler policy, GPU placement, runtime downloads, pretrained weights, coordinate inputs, or external persistence.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` auxiliary output `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline` with `weighted_bce` weight 0.02, AdamW, learning rate 0.0003, batch size 4, manifest max epochs 12, constant learning-rate policy, and disabled early stopping.
- Trusted budget request: `late_improving` with requested max epochs 36 and exploratory fallback if denied.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.

## Budget Requested

One sequential representative capped late-improving Run: at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, requested max epochs 36 under the trusted `late_improving` budget class, 10,800 seconds late-budget wall-clock ceiling when enforced, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant scheduler policy, disabled early stopping, and Harness-owned GPU placement. If the Harness denies the request, use `fallback_if_denied: run_exploratory_budget`; do not stop for human approval solely because the longer budget was denied.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. The late-improving budget request is accepted or cleanly falls back to the exploratory budget through Harness policy; Candidate code does not implement any budget workaround.
3. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 remains inside the trusted resource envelope.
4. Primary and auxiliary losses, logits, gradients, parameters, metrics, and checkpoint state remain finite.
5. Final predictions do not persistently collapse to all-negative or all-positive masks.
6. Family-development success is met if ABI-192 improves ABI-191's capped filtered Dice while retaining non-degenerate source-stratified performance and preferably approaches ABI-181 aggregate Dice or ABI-184 connectivity/precision.
7. Promotion would require later whole-validation diagnostics and human review; this capped late36 Run alone is not promotion evidence.

## Fallback/Next Decision

If ABI-192 improves ABI-191 and remains close to or above ABI-181 on capped aggregate filtered Dice without source or connectivity regression, request a trusted whole-validation diagnostic in a later Autonomy Step. If it improves recall but loses connectivity/precision like ABI-189, or plateaus below ABI-181/184, stop this directional-lattice late-budget branch and broaden to a different high-resolution line-aware architecture, data-policy probe, or allowlisted loss/auxiliary configuration. If it fails by contract, shape, numerical, resource, or lifecycle criteria, classify the failure before proposing any repair.
