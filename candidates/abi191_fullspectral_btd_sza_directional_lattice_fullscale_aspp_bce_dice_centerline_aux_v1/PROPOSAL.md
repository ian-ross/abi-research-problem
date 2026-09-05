# ABI-191 Full-Spectral BTD+SZA Directional-Lattice Full-Scale ASPP BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-191 is a controlled exploratory continuation from the ABI-181 signed-detail full-scale skip ASPP branch. It is not a promotion claim and not a late-budget request. It follows the ABI-181 and ABI-184 whole-validation lessons: ABI-181 is the aggregate filtered-Dice reference but remains weak on connected-line structure and MIT positives, while direct Line Target supervision and later mask/logit calibration variants improved some precision/connectivity or recall signals at unacceptable tradeoff cost.

## Hypothesis

A conservative multi-orientation directional lattice bridge can improve connected thin-line support and MIT-source detail while preserving ABI-181's Centerline-only recall/precision balance. Unlike ABI-184, ABI-191 does not add Line Target auxiliary supervision that may make the fixed-threshold mask too conservative. Unlike ABI-188/189/190, it does not add auxiliary logits or a line-specific calibration module around the mask head; it uses architecture-internal horizontal, vertical, and diagonal feature propagation before the existing final line-aware refinement.

## Comparison Target

The primary comparison target is ABI-181 `run_20260902_150611_cbbf35`, the strongest whole-validation-tested aggregate filtered-Dice reference: capped filtered Dice 0.4104, MIT/Google filtered Dice 0.3962/0.4486, filtered precision 0.4423, recall 0.3828, connectivity 0.3639, and filtered predicted-positive fraction 0.00314; whole-validation filtered Dice 0.4124 with precision 0.4466, recall 0.3832, and connectivity 0.3676.

Secondary references are ABI-184 `run_20260902_213856_2c04ac`, the Line plus Centerline precision/connectivity reference with whole-validation filtered Dice 0.4093, precision 0.4893, recall 0.3517, and connectivity 0.4763; ABI-190 `run_20260903_064825_5a446f`, the negative feature-level line-calibration reference; and ABI-068 `run_20260828_010836_4ccc77`, the broader frequency-gated line-U-Net recall/connectivity and MIT-source comparator.

## Expected Effect

A positive result would remain finite and non-collapsed while improving ABI-181's capped filtered connectivity and/or MIT filtered Dice without losing more than about 0.01 aggregate filtered Dice. The strongest outcome would keep ABI-181-like aggregate/source Dice, precision, recall, and positive-area discipline while moving connectivity toward ABI-184. A useful negative result would show that another conservative high-resolution architectural line-support mechanism still cannot improve connectivity without softening or fragmenting the mask, motivating a broader architecture or policy frontier.

## Implementation Sketch

- Reuse the ABI-181 signed-detail full-scale skip ASPP architecture: normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized and cosine Solar Geometry Input features, learned spectral projection, signed local/mid-scale positive and negative detail streams, compact residual encoder, ASPP bottleneck, full-scale skip fusion, line-aware final refinement, primary mask head, and Centerline auxiliary head.
- Insert `DirectionalLatticeBridge` after full-scale skip feature projection and before the existing final line-aware refinement.
- The bridge builds high-resolution local-detail, learned horizontal, learned vertical, and zero-padded diagonal feature-neighborhood branches. It fuses them with broad context and applies a zero-initialized `1x1` residual projection bounded by `tanh` with scale 0.2, keeping the initial function close to ABI-181 while allowing trusted training losses to learn connected-line support.
- Preserve only provider-derived Centerline Target auxiliary supervision with trusted `weighted_bce` weight 0.02; do not add Line Target supervision in this candidate.
- Keep trusted manifest choices unchanged from ABI-181 except for no late-budget request: `abi_16ch_plus_sza`, `bce_dice`, `combined_source_balanced`, `random_mirroring`, AdamW, learning rate 0.0003, batch size 4, manifest max epochs 12, constant learning rate, and disabled early stopping.
- Do not implement Candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, scheduler policy, GPU placement, runtime downloads, pretrained weights, coordinate inputs, or external persistence.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` auxiliary output `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline` with `weighted_bce` weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.

## Budget Requested

One sequential representative capped exploratory Run: at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, max epochs 12, 3,600 seconds Docker training wall-clock budget when enforced, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant scheduler policy, disabled early stopping, and Harness-owned GPU placement. No `late_improving` budget is requested for this material architecture variant, and no full-data claim, promotion decision, Experiment Batch, or Candidate-owned budget change is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 remains inside the trusted resource envelope.
3. Primary and auxiliary losses, logits, gradients, parameters, metrics, and checkpoint state remain finite.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw/filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. Family-development success is met if ABI-191 improves ABI-181 filtered connectivity or MIT filtered Dice while retaining aggregate filtered Dice within about 0.01 of ABI-181; a smaller positive signal is useful if the best epoch is late and non-collapsed, making it eligible for a later `late_improving` request.
7. Promotion would require later whole-validation diagnostics and human review; this capped exploratory Run alone is not promotion evidence.

## Fallback/Next Decision

If ABI-191 improves connectivity or MIT overlap without large aggregate/source Dice, precision, recall, or positive-area loss, consider a late-improving continuation only if the selected checkpoint is near epoch 12 with a finite improving trajectory; otherwise consider whole-validation diagnostics only after strong capped evidence. If it regresses like ABI-190, expands positives with low connectivity, or shows no useful trajectory, stop this directional-lattice branch and broaden to a different high-resolution line-aware architecture, data-policy probe, or provider-allowlisted loss/auxiliary configuration. If it fails by contract, shape, numerical, resource, or lifecycle criteria, classify the failure before proposing any repair.
