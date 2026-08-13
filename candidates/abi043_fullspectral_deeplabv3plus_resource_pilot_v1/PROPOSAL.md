# ABI-043 Full-Spectral DeepLabV3+ Resource Pilot v1

## Proposal classification

**Family scout, resource-pilot stage.** This is the first execution of a materially different atrous encoder-decoder family. The one-epoch pilot is finite/resource evidence only, not architecture-ranking or promotion evidence.

## Hypothesis

A DeepLabV3+ encoder-decoder that receives normalized Full ABI Channel Input can combine local low-level detail with atrous multi-scale context, a useful inductive bias for separating thin coherent contrails from cloud edges. Before scientific scouting, the authorized bounded pilot should establish that this family is contract-valid, finite, operationally trainable, and compatible with the current sequential batch/resource envelope.

## Comparison Target

The current best completed candidate Run is `run_20260811_160920_07a7f4` (`abi031_mcast11_positive_control_v1`), with bounded `val/dice` 0.1070; canonical MCAST 2.1 filtered Dice 0.3873 remains promotion context. Neither is a score gate for this resource pilot. The relevant operational comparator is the successful ABI candidate execution path, while the architecture remains an unprofiled resource class.

## Expected Effect

All losses, logits, gradients, parameters, and checkpoint state should remain finite; output shape should remain `[1, 256, 256]`; and the Run should complete within the 25-million-parameter, batch-size-4, one-epoch, 3,600-second trusted envelope. Metric magnitude from this tiny pilot will not be used to rank or eliminate the architecture.

## Implementation Sketch

- Accept only provider-approved `abi_16ch` tensors and normalize all 16 ABI channels with rounded trusted campaign-context summary values.
- Use an SMP DeepLabV3+ model with a randomly initialized ResNet-18 encoder, output stride 16, a 256-channel decoder, atrous rates 12/24/36, and one mask-logit output.
- Select provider-owned `combined_source_balanced` sampling and `random_mirroring` augmentation.
- Select trusted `bce_dice`, AdamW at 0.0003, batch size 4, and one epoch.
- Request sequential execution only; this new family has no concurrency authorization.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude, latitude, and Solar Geometry Input are excluded.
- Output form: one `[1, 256, 256]` `mask_logits` tensor.
- Provider-owned Leakage-Safe Split, capped-record selection, Source-Balanced Sampling, augmentation, targets, trusted loss, metrics, checkpointing, and Artifact Filters.
- No candidate-owned data loading, sampling, augmentation transforms, losses, metrics, filtering, training loop, pretrained weights, runtime downloads, scheduling, or external persistence.

## Budget Requested

One sequential one-epoch resource pilot using at most 32 training and 32 validation ABI Patches per Dataset Source, batch size 4, at most four Harness-selected prediction artifacts, the 25,000,000-parameter smoke ceiling, and the 3,600-second trusted training timeout. No Experiment Batch or parallel execution is requested.

If the pilot passes, a representative scout is a separately authorized later policy stage. This proposal does not request or imply full-data training.

## Success Criteria

1. Static validation, controlled smoke testing, and bounded training complete without contract, shape, resource, or lifecycle failure.
2. Model parameter count is at most 25,000,000 and the requested batch size completes without Resource Failure retry.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state are finite.
4. Run metadata, bounded-record audit metadata, model summary, resource profile, metrics, and bounded prediction artifacts are complete and linked.
5. Any observed score or prediction degeneracy is recorded only as diagnostic pilot context, not as architecture-ranking evidence.

## Continuation and hard stop

After a successful pilot, retain this family as eligible for one separately authorized representative scout using trusted provider-selected records. Do not infer concurrency safety from parameter count or pilot completion. Stop and classify before further family work if the pilot has a hard contract failure, persistent non-finite behavior, an irreparable output-shape mismatch, or a resource failure that cannot fit the current batch/resource envelope. A low one-epoch score alone is not a hard stop.

## Fallback Next Decision

If the pilot exposes a narrow candidate implementation defect while the hypothesis remains intact, prepare one explicit Repair Candidate in a later Autonomy Step. If the architecture exceeds trusted resource or contract capability, classify the failure and request reviewed capability rather than implementing a workaround. If the pilot succeeds, await separate representative-scout authorization and evidence before any scientific comparison.
