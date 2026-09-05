# ABI-193 Full-Spectral BTD+SZA Signed-Detail Full-Scale Skip ASPP Boundary+Centerline Auxiliary v1

## Proposal classification

**Family-development continuation / trusted auxiliary-policy probe.** ABI-193 keeps the finite, resource-safe ABI-181 signed-detail full-scale skip ASPP architecture and changes only the auxiliary-output policy by adding a low-weight provider-derived Boundary Target head alongside the existing Centerline Target head. It is not a promotion claim and does not request late-improving budget.

## Hypothesis

ABI-181 remains the strongest whole-validation-tested aggregate filtered-Dice reference in this lineage, while ABI-184 shows that additional line supervision can improve precision, connectivity, and negative-patch discipline at a recall cost. ABI-192 preserved more positive-patch recall but worsened negative-patch clutter and did not match ABI-184 connectivity. A low-weight Boundary Target auxiliary head should encourage sharper mask edges and suppress diffuse cloud-edge clutter, while the Centerline Target preserves thin-line localization and the primary BCE-Dice loss preserves region overlap.

## Comparison Target

Primary comparison target: ABI-181 `run_20260902_150611_cbbf35`, with capped best filtered Dice 0.4104 and whole-validation filtered Dice 0.4124. Secondary references are ABI-184 `run_20260902_213856_2c04ac` for precision/connectivity and negative-patch discipline, ABI-192 `run_20260903_085513_f395ad` for recall/positive-patch median behavior, and canonical MCAST 1.1/2.1 summaries from the Research Problem campaign context.

## Expected Effect

A useful positive outcome would reduce filtered predicted-positive fraction or improve precision/connectivity relative to ABI-181/192 without the large recall loss seen in ABI-184. A diagnostically useful negative outcome would show that boundary auxiliary supervision over-constrains thin contrails, reducing recall or source balance, which would argue against further boundary-target probes in this branch.

## Implementation Sketch

- Reuse ABI-181 architecture: approved `abi_16ch_plus_sza` input, normalized ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, Solar Geometry Input features, learned 1x1 spectral projection, signed local/mid-scale detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, and line-aware refinement.
- Add a trainable `boundary_logits` auxiliary head from the same refined feature tensor as `mask_logits` and `centerline_logits`.
- Select trusted auxiliary targets in the manifest: Boundary Target `weighted_bce` at weight 0.01 and Centerline Target `weighted_bce` at weight 0.02.
- Keep trusted `bce_dice`, `combined_source_balanced`, `random_mirroring`, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning rate, and disabled early stopping.
- Do not implement Candidate-owned data loading, split logic, capped-record selection, sampling, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, scheduler policy, GPU placement, runtime downloads, pretrained weights, coordinates, or external persistence.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-derived `[1, 256, 256]` `boundary_logits` and `centerline_logits` auxiliary outputs.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `boundary` and `centerline`, auxiliary loss `weighted_bce`, AdamW, learning rate 0.0003, batch size 4, max epochs 12, and constant learning-rate policy.

## Budget Requested

One sequential exploratory capped Run under the active Workspace Configuration: at most 1,024 training and validation ABI Patches per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, 25,000,000-parameter smoke ceiling, fixed `first_n` prediction retention, constant scheduler, and disabled early stopping. No late-improving budget, full-data claim, promotion decision, Experiment Batch, or Candidate-owned budget change is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameters remain below the 25,000,000 smoke ceiling and batch size 4 remains resource-safe.
3. Primary and auxiliary losses, logits, gradients, metrics, and checkpoint state remain finite.
4. Predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw/filtered metrics plus predicted-positive fractions are source-informative.
6. The branch is useful if it improves precision/connectivity or negative-patch discipline relative to ABI-181/192 while keeping aggregate filtered Dice within about 0.01 of ABI-181 or improving over ABI-184 recall.

## Continuation and hard stop

Continue only if the exploratory Run is finite, non-collapsed, source-informative, and shows a better precision/recall/connectivity tradeoff than the existing ABI-181/184/192 references. Stop this exact boundary+centerline auxiliary probe for hard execution failure, non-finite behavior, persistent prediction collapse, severe Dataset Source-specific collapse, clear optimization failure, or a material recall/connectivity regression without negative-clutter improvement.

## Fallback/Next Decision

If ABI-193 improves capped aggregate/source behavior or materially clarifies negative-patch clutter, request a bounded whole-validation failure-bucket diagnostic before any promotion interpretation. If it regresses, broaden away from auxiliary-target tweaks toward a different high-resolution line-aware architecture, an allowed loss-policy probe, or a new preprocessing/front-end inductive bias within the Candidate Contract.
