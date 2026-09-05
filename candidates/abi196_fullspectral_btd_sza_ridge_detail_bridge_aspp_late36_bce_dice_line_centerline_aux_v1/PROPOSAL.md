# ABI-196 ridge-preserving detail bridge ASPP late36 continuation

## Proposal classification

**Family-development continuation with late-improving budget request.** ABI-196 is an exact architecture close-continuation of ABI-195. It uses the operator-addressed late-improving budget surface to test whether ABI-195 final-epoch high-precision/high-connectivity recovery was truncated by the 12-epoch exploratory budget or was a capped-subset fluctuation.

## Hypothesis

ABI-195 `RidgePreservingDetailBridge` repaired the ABI-194 clutter-gate connectivity regression and reached its best filtered Dice, precision, and connectivity at epoch 12 while retaining a low predicted-positive fraction. Under the Harness-owned late-improving budget, the exact same finite, resource-safe architecture may improve recall and source balance without losing the disciplined precision/connectivity operating point, or may reveal plateau/overfit behavior that justifies broadening away from this bridge branch.

## Comparison Target

The primary comparison target is ABI-195 `run_20260903_135523_8976a0`: capped best epoch 12, filtered Dice 0.3891, MIT/Google filtered Dice 0.3706/0.4369, filtered precision 0.4649, filtered recall 0.3346, filtered connectivity 0.4391, and filtered predicted-positive fraction 0.002608. Secondary references are ABI-181 `run_20260902_150611_cbbf35` as the current whole-validation aggregate filtered-Dice reference, ABI-184 `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference, ABI-192 `run_20260903_085513_f395ad` as the recall-balanced directional-context comparator, and ABI-194 `run_20260903_125403_548c08` as the negative clutter-gate result.

## Expected Effect

A positive outcome would preserve ABI-195 low-positive, high-precision, high-connectivity behavior while recovering recall and MIT/source balance as training continues beyond the exploratory ceiling. A negative but useful outcome would show that the ridge-detail bridge plateaus, overfits, loses precision/connectivity, or cannot close the filtered-Dice gap to ABI-181/184/192 under longer training.

## Implementation Sketch

Reuse ABI-195 model architecture unchanged: approved `abi_16ch_plus_sza` input, normalized raw ABI channels, deterministic ABI-channel-derived thermal BTD planes, SZA features, learned channel projection, signed local/mid-scale detail streams, compact residual encoder, ASPP context, full-scale skip fusion, `RidgePreservingDetailBridge`, final line-aware refinement, primary `mask_logits`, and auxiliary `line_logits` plus `centerline_logits`. Keep trusted manifest choices unchanged: `bce_dice`, Line Target weighted BCE at 0.01, Centerline Target weighted BCE at 0.02, `combined_source_balanced`, `random_mirroring`, AdamW, learning rate 0.0003, batch size 4, and `constant_lr`. Add only candidate-local `budget_request.yaml` requesting `late_improving` 36 epochs with parent Run `run_20260903_135523_8976a0` and fallback `run_exploratory_budget`.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs requested through the late-improving budget, constant scheduler policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.
- Candidate code defines model architecture only and contains no data loading, custom losses, custom metrics, Artifact Filters, postprocessing, thresholding, runtime downloads, filesystem persistence, Candidate-owned scheduling, or coordinate features.

## Budget Requested

One sequential representative capped late-improving Run with at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, up to 36 epochs if the Harness grants `budget_request.yaml`, 10,800 seconds wall-clock budget under the trusted late-improving policy, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant scheduler policy, and disabled early stopping. If the request is denied, run the same Candidate under the exploratory budget. No full-data claim, promotion decision, Experiment Batch, or Candidate-owned budget change is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 remains inside the trusted late-improving runtime envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. As late-improving evidence, the Run is promising if it improves beyond ABI-195 filtered Dice while preserving its precision/connectivity strengths, or if it clearly distinguishes continued learning from plateau/overfit/degradation for this exact ridge-detail bridge branch.

## Fallback/Next Decision

If the late-improving budget is denied, accept the exploratory-budget Run as the valid bounded result and do not stop for human approval solely because of denial. If ABI-196 improves capped filtered Dice or materially clarifies precision/recall/connectivity, write a Research Note and consider a later whole-validation failure-bucket diagnostic before any promotion claim. If it plateaus or degrades, broaden away from this exact bridge branch toward a distinct high-resolution architecture, trusted data/loss-policy probe, preprocessing/calibration frontier, or evaluation request rather than adding another local gate.
