# ABI-182 Full-Spectral BTD+SZA Signed-Detail Line-Consensus Late36 BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation with late-improving budget request.** ABI-182 is an exact architecture close-continuation of ABI-174, using the operator-addressed late-improving budget surface. It is not a new family and not a promotion claim; it asks whether an already finite, resource-safe, connectivity-improving line-consensus branch was truncated at the exploratory epoch ceiling.

## Hypothesis

ABI-181 established that the signed-detail full-scale skip ASPP branch can improve materially under 36 trusted epochs and that its whole-validation gains survive, but the full-validation failure-bucket review still identifies connected-line structure and MIT/source balance as remaining weaknesses. ABI-174 added a conservative line-consensus calibration block to ABI-173 and improved capped connectivity over ABI-173 from 0.3203 to 0.3460 while preserving recall, but it ended at its best epoch after a large epoch-12 jump and stayed below the parent on aggregate/source Dice. The hypothesis is that ABI-174's line-consensus branch may need the same late-improving budget that benefited ABI-181 to recover aggregate/source overlap while retaining its connectivity advantage.

## Comparison Target

The primary comparison target is ABI-174 `run_20260902_005632_5651ef`: capped best/final epoch 12, filtered Dice 0.3929, MIT/Google filtered Dice 0.3833/0.4178, filtered precision 0.4158, recall 0.3724, connectivity 0.3460, and filtered predicted-positive fraction 0.00325. The main current aggregate target is ABI-181 `run_20260902_150611_cbbf35`: capped filtered Dice 0.4104 at epoch 22 and whole-validation filtered Dice 0.4124, with whole-validation connectivity 0.3676. Secondary references are ABI-154 `run_20260901_071026_32d3ec` for precision/connectivity, ABI-068 `run_20260828_010836_4ccc77` for recall/connectivity and MIT/source balance, and canonical MCAST summaries from the trusted campaign context.

## Expected Effect

A positive outcome would show a finite, non-collapsed extended trajectory where ABI-182 improves materially over ABI-174's 12-epoch capped aggregate and source-stratified filtered Dice while preserving or improving ABI-174's connectivity. A strong outcome would approach ABI-181 aggregate/source Dice while improving ABI-181 connectivity or MIT/source balance without a large increase in filtered predicted-positive fraction. A negative but useful outcome would show that the line-consensus branch's 12-epoch aggregate deficit persists, that later epochs overfit/oscillate, or that connectivity gains come only with unacceptable precision/source/positive-area costs.

## Implementation Sketch

- Reuse ABI-174 model architecture unchanged: approved-channel normalized ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized and cosine Solar Geometry Input features, learned 1x1 spectral projection, signed local/mid-scale positive and negative detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, line-aware refinement, conservative line-consensus calibration, primary `mask_logits`, and auxiliary `centerline_logits`.
- Keep trusted manifest choices unchanged: `bce_dice`, Centerline Target `weighted_bce` at weight 0.02, `combined_source_balanced`, `random_mirroring`, AdamW, learning rate 0.0003, batch size 4, and `constant_lr`.
- Include candidate-local `budget_request.yaml` with `budget_class: late_improving`, `requested_max_epochs: 36`, parent Runs `run_20260902_005632_5651ef` and `run_20260902_150611_cbbf35`, and fallback `run_exploratory_budget`.
- Do not implement Candidate-owned training loops, data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, scheduler policy, GPU placement, runtime downloads, pretrained weights, coordinates, or external persistence.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, constant learning-rate policy, disabled early stopping, and max epochs requested through the late-improving budget.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.

## Budget Requested

One sequential representative capped late-improving Run with at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, up to 36 epochs if the Harness grants `budget_request.yaml`, 10,800 seconds wall-clock budget under the trusted late-improving policy, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant scheduler policy, and disabled early stopping. If the request is denied, run the same Candidate under the exploratory budget. No full-data claim, promotion decision, Experiment Batch, or Candidate-owned budget change is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains below the 25,000,000 smoke ceiling and batch size 4 remains inside the trusted late-improving runtime envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. The Run is useful if it clearly improves over ABI-174, clarifies whether ABI-174 was epoch-truncated, or identifies a stable connectivity/precision/source tradeoff relative to ABI-181, ABI-154, and ABI-068.

## Continuation and hard stop

Continue the line-consensus budget branch only if ABI-182 is finite, non-degenerate, source-informative, and improves ABI-174 or materially clarifies the aggregate/connectivity tradeoff without severe positive-area expansion. Stop or repair for hard execution failure, persistent non-finite behavior, persistent prediction collapse, resource failure, clear overfitting/divergence, severe source-specific collapse, or large positive-area expansion without overlap improvement. Low score alone is not a family-level elimination rule, but repeating this exact architecture again after a completed 36-epoch trajectory should require new diagnostic evidence.

## Fallback/Next Decision

If the late-improving budget is denied, accept the exploratory-budget Run as the valid bounded result and do not stop for human approval solely because of denial. If ABI-182 materially improves over ABI-174 and either approaches ABI-181 aggregate/source Dice or improves ABI-181 connectivity/MIT balance, consider a later whole-validation failure-bucket Evaluation Request before any promotion claim. If it plateaus or degrades, broaden away from line-consensus/signed-detail continuations toward a different architecture, data-policy, preprocessing, calibration, loss/auxiliary, or evaluation frontier.
