# ABI-181 Full-Spectral BTD+SZA Signed-Detail Full-Scale Skip ASPP Late36 BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation with late-improving budget request.** ABI-181 is an exact architecture close-continuation of ABI-173. It does not introduce a new model family or new Candidate-owned authority; it uses the operator-addressed late-improving budget surface to test whether ABI-173's final-epoch improvement was truncation by the 12-epoch exploratory budget or a short-budget fluctuation.

## Hypothesis

ABI-173's signed positive/negative local and mid-scale detail streams recovered fixed-threshold recall and produced the strongest whole-validation-tested SZA-aware ASPP/detail aggregate branch, but its 12-epoch Run selected the final epoch and improved sharply from epoch 11 to epoch 12. Under the Harness-owned late-improving budget, the exact same finite, resource-safe architecture may continue improving calibration and overlap, or may reveal overfitting/plateau behavior that would not be visible at the exploratory ceiling. The useful research signal is the trajectory under more trusted epochs, not a Candidate-code change.

## Comparison Target

The primary comparison target is ABI-173 `run_20260901_234732_bd5917`: capped best epoch 12, filtered Dice 0.3962, MIT/Google filtered Dice 0.3838/0.4269, filtered precision 0.4238, recall 0.3720, connectivity 0.3203, and whole-validation diagnostic filtered Dice 0.3973. Secondary references are ABI-154 `run_20260901_071026_32d3ec` for precision/connectivity, ABI-130 `run_20260831_121006_7d24be` as the prior SZA-aware ASPP/detail aggregate reference, ABI-068 `run_20260828_010836_4ccc77` as the broader capped aggregate/source-balance comparator, and ABI-179/180 as recent UPerNet evidence that local context-pyramid continuation did not displace ABI-173.

## Expected Effect

A positive outcome would keep finite, non-collapsed predictions and improve or clarify ABI-173's capped filtered-Dice trajectory beyond epoch 12 while preserving source-informative MIT and Google metrics. A stronger outcome would improve aggregate filtered Dice without expanding filtered predicted-positive fraction materially or further degrading connectivity. A negative but useful outcome would show plateau, degradation, overfitting, source-specific loss, or positive-area expansion under longer training, supporting a return to architecture or data-policy broadening rather than further same-branch epochs.

## Implementation Sketch

- Reuse ABI-173 model architecture unchanged: approved-channel normalized ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized and cosine Solar Geometry Input features, learned 1x1 spectral projection, signed local/mid-scale positive and negative detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, line-aware final refinement, primary `mask_logits`, and auxiliary `centerline_logits`.
- Keep trusted manifest choices unchanged except the requested epoch count under the operator-addressed late-improving budget: `bce_dice`, Centerline Target `weighted_bce` at weight 0.02, `combined_source_balanced`, `random_mirroring`, AdamW, learning rate 0.0003, batch size 4, and `constant_lr`.
- Include candidate-local `budget_request.yaml` with `budget_class: late_improving`, `requested_max_epochs: 36`, parent Run `run_20260901_234732_bd5917`, and fallback `run_exploratory_budget`.
- Do not implement Candidate-owned training loops, data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, scheduler policy, GPU placement, runtime downloads, pretrained weights, coordinates, or external persistence.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs requested through the late-improving budget, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.

## Budget Requested

One sequential representative capped late-improving Run with at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, up to 36 epochs if the Harness grants `budget_request.yaml`, 10,800 seconds wall-clock budget under the trusted late-improving policy, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant scheduler policy, and disabled early stopping. If the request is denied, run the same Candidate under the exploratory budget. No full-data claim, promotion decision, Experiment Batch, or Candidate-owned budget change is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 remains inside the trusted late-improving runtime envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. As late-improving evidence, the Run is useful if it distinguishes continued improvement from plateau/overfit/degradation relative to ABI-173's epoch-12 capped result.

## Continuation and hard stop

Continue this exact longer-training branch only if the extended trajectory is finite, non-degenerate, source-informative, and improves or clarifies ABI-173 without severe false-positive or connectivity regression. Stop or repair for hard execution failure, persistent non-finite behavior, persistent prediction collapse, resource failure, clear overfitting/divergence, severe source-specific collapse, or large positive-area expansion without overlap improvement. Extended-budget results remain capped representative feasibility evidence and must not be treated as full-data promotion evidence.

## Fallback/Next Decision

If the late-improving budget is denied, accept the exploratory-budget Run as the valid bounded result and do not stop for human approval solely because of denial. If ABI-181 improves capped filtered Dice or materially clarifies precision/recall/connectivity, request a later whole-validation failure-bucket diagnostic before any promotion claim. If it plateaus or degrades, broaden away from longer-training continuations toward distinct architecture, data-policy, preprocessing, calibration, loss/auxiliary, or evaluation frontiers.
