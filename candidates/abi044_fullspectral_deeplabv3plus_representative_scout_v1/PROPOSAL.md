# ABI-044 Full-Spectral DeepLabV3+ Representative Scout v1

## Proposal classification

**Family scout, representative-scout stage.** This is the first scientific feasibility screen for the materially different atrous encoder-decoder family that passed the ABI-043 one-epoch resource pilot. It is not full-data or promotion evidence.

## Hypothesis

A DeepLabV3+ encoder-decoder receiving normalized Full ABI Channel Input can learn thin-contrail features by combining low-level spatial detail with atrous multi-scale context. With 12 epochs over provider-selected representative records, the family should remain finite and non-degenerate while improving its filtered Dice trajectory beyond the one-epoch ABI-043 resource pilot, with useful signal on both MIT and Google Dataset Sources.

## Comparison Target

The family baseline is ABI-043 Run `run_20260813_131515_ff53ab`, which completed the 32-record/source/split resource pilot with 12.37M parameters, 528 MB peak CUDA reservation, aggregate `val/filtered_dice` 0.004403, MIT filtered Dice 0.006732, Google filtered Dice 0.001829, and non-degenerate filtered predicted-positive fraction 0.1270. The current best completed candidate Run remains `run_20260811_160920_07a7f4` (`abi031_mcast11_positive_control_v1`), with bounded `val/dice` 0.1070; canonical MCAST 2.1 filtered Dice 0.3873 is promotion context. The mature comparators are not strict score gates for this first representative family scout.

## Expected Effect

Relative to ABI-043, the larger trusted record set and 12-epoch budget should reduce the pilot's broad overprediction, improve precision and filtered Dice, and establish whether learning remains directional on both Dataset Sources. The architecture should preserve finite/resource behavior at batch size 4. The scout is diagnostically successful if it yields a finite, source-balanced, non-collapsed trajectory that either improves through the final epochs or exposes a convincing family-specific optimization limit.

## Implementation Sketch

- Preserve the ABI-043 randomly initialized SMP DeepLabV3+ ResNet-18 architecture, output stride 16, 256-channel decoder, atrous rates 12/24/36, and one mask-logit output.
- Accept only provider-approved `abi_16ch` tensors and retain the pilot's rounded trusted campaign-context normalization constants.
- Preserve provider-owned `combined_source_balanced` traversal and `random_mirroring` augmentation.
- Preserve trusted `bce_dice`, AdamW at learning rate 0.0003, and batch size 4 so the controlled change is the authorized representative record/epoch budget.
- Request one sequential Run only; no concurrency is authorized for this architecture family.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are excluded.
- Output form: one `[1, 256, 256]` `mask_logits` tensor.
- Provider-owned Leakage-Safe Split, representative capped-record selection, Source-Balanced Sampling, augmentation, targets, trusted loss, metrics, checkpointing, and Artifact Filters.
- No candidate-owned data loading, record selection, sampling implementation, augmentation transforms, losses, metrics, filtering, training loop, pretrained weights, runtime downloads, scheduling, or external persistence.

## Budget Requested

One sequential 12-epoch representative scout using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, and the 3,600-second trusted training timeout. No Experiment Batch, parallel execution, extension, Evaluation, or full-data training is requested.

## Success Criteria

1. Static validation, controlled smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Model parameter count remains at most 25,000,000 and batch size 4 completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite.
4. Predictions do not persistently collapse to all-negative or all-positive masks across the final scout epochs.
5. Aggregate, MIT, and Google filtered metrics plus predicted-positive fractions are complete, and neither Dataset Source has an unexplained catastrophic execution failure.
6. The late training-loss and filtered-Dice trajectories provide directional evidence: continued improvement, a convincing plateau/divergence, or another diagnostically useful family-specific pattern.

## Continuation and hard stop

Low Dice alone does not eliminate this immature family. A finite, improving, source-balanced, novel, noisy, or ambiguous trajectory remains eligible for a separately authorized family-development continuation or extended scout. Eliminate or repair before further family work only for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, convincing plateau/divergence at the scout budget, irreparable output-shape mismatch, or resource failure outside the trusted envelope. No scout result automatically authorizes extension, concurrency, full-data training, or promotion.

## Fallback Next Decision

If a narrow implementation defect occurs while the hypothesis remains intact, classify it and prepare at most one explicit Repair Candidate in a later Autonomy Step. If the Run is finite but ambiguous or still improving, stop and seek separate authorization for one bounded continuation. If it shows a hard stop, document family evidence and broaden the architecture frontier in a later step. If it is unexpectedly strong, request separately authorized focused full-data evidence rather than making a promotion claim from capped data.
