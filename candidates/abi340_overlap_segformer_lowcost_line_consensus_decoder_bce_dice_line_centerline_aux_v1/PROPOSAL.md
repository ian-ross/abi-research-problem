# ABI-340 overlap SegFormer low-cost line-consensus decoder

## Hypothesis

A compact overlap-attention SegFormer encoder remains a viable modern-backbone family-development branch because ABI-262 improved over ABI-260 on filtered Dice, recall, and MIT Dice, but its selected checkpoint lost connected thin-line continuity. ABI-263 showed that a heavier high-resolution directional line-state decoder can raise connectivity at some checkpoints, but with high activation cost and worse overlap/source performance. ABI-340 tests whether a lower-cost final logit head with oriented strip consensus can recover some connected-line evidence while preserving ABI-262s overlap-attention recall/MIT behavior.

## Comparison Target

Primary comparison targets are ABI-262 (`run_20260912_040526_92961f`) as the overlap SegFormer parent and ABI-263 (`run_20260912_045029_55c59e`) as the heavier directional-line decoder follow-up. Secondary context is ABI-253 as the compact modern-backbone comparator and ABI-249/ABI-202 as stronger non-modern-backbone references.

## Expected Effect

Expected effect is higher filtered contrail connectivity than ABI-262 with smaller precision/source-Dice loss than ABI-263. Success does not require beating ABI-202 immediately; a useful family-development result would keep ABI-262-like filtered Dice and MIT Dice while moving connectivity toward ABI-253/ABI-263 without broadening negative clutter.

## Implementation Sketch

Use the ABI-262 provider-approved `abi_16ch_plus_sza` overlap SegFormer encoder, signed-detail bridge, all-MLP multi-scale decoder, and trusted Line/Centerline auxiliary outputs. Replace the previous broad evidence-raising head with `ConnectivityPreservingLineConsensusHead`: separate coverage, oriented line-context, and local-detail streams produce bounded positive support only when a learned consensus gate sees agreement among decoder features, strip context, centerline evidence, and local detail. The head emits `mask_logits`, `line_logits`, and `centerline_logits`; it performs no thresholding, morphology, connected components, postprocessing, Artifact Filtering, or target construction.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza`.
- Output form: `mask_logits`.
- Trusted auxiliary targets: Line (`line_logits`) and Centerline (`centerline_logits`) with `weighted_bce` weights 0.01 and 0.02.
- Trusted data policy: `combined_source_balanced` sampling and `random_mirroring` augmentation.
- Trusted training policy: `bce_dice`, AdamW, constant learning rate, batch size 4, max 12 exploratory epochs.
- Candidate code remains architecture-only and does not own data loading, temporal lookup, target derivation, loss, metrics, Artifact Filters, thresholding, postprocessing, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Budget Requested

Default exploratory budget only: 12 epochs, batch size 4, constant learning rate. No late-improving budget is requested for this mechanism-changing modern-backbone continuation.

## Success Criteria

- Complete static validation, smoke testing, and training without contract, numerical, shape, resource, or lifecycle failure.
- Improve ABI-262 filtered connectivity materially while keeping filtered Dice within roughly 0.01 of ABI-262 or improving it.
- Avoid ABI-263s failure mode: high activation cost plus lower aggregate/source Dice. Resource profile should remain closer to ABI-262 than ABI-263 if possible.
- Preserve finite, source-informative predictions without all-negative/all-positive collapse.

## Fallback/Next Decision

If ABI-340 regresses ABI-262 on aggregate/source Dice without a meaningful connectivity gain, stop this exact low-cost line-consensus SegFormer branch. If it improves connectivity with acceptable overlap/source trade-off and the best checkpoint is late or final, consider a bounded late-improving continuation or a failure-bucket diagnostic depending on trajectory. If resource use approaches ABI-263 without stronger metrics, broaden away from SegFormer decoder mechanisms.
