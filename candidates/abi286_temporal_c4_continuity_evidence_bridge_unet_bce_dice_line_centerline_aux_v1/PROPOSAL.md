# Proposal: ABI-286 temporal C4 continuity-evidence bridge U-Net

## Classification

Family-development continuation in the provider-owned temporal ABI input family. This is an exploratory capped mechanism test, not a promotion claim.

## Hypothesis

ABI-285 is now the strongest capped temporal-eligible aggregate filtered-Dice comparator and has the best recall among recent temporal comparators, but its failure-bucket review shows the weakest connected-line continuity and broader negative-patch clutter. The hypothesis is that retaining ABI-285's early C4 orientation line-state stem while adding a full-resolution continuity-evidence bridge immediately before the mask head will organize recall-heavy temporal evidence into more continuous thin-line support without moving thresholding or postprocessing into Candidate code.

## Comparison Target

Primary temporal-family comparison targets:

- ABI-285 (`run_20260913_100333_a250df`) for temporal C4 recall/source-balance gains and the failure mode to improve.
- ABI-223 (`run_20260908_154531_8c7e2b`) for cleaner temporal connected-line evidence.
- ABI-274 (`run_20260912_180856_79ba22`) for temporal line-state recall/source behavior.
- ABI-238 (`run_20260911_004137_f54c45`) and ABI-255 (`run_20260911_210922_27f346`) as additional temporal precision/recurrent comparators.

ABI-202 remains the whole-validation aggregate reference, but this Candidate should be interpreted on the provider-owned temporal-eligible capped validation population.

## Implementation Sketch

Start from ABI-285's temporal C4 orientation line-state U-Net using provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`. Keep the per-frame ABI/SZA/BTD feature builder, temporal attention/change stem, early C4 orientation line-state, encoder-scale line-state injection, ASPP bottleneck, and high-resolution directional decoder context.

Change only the architecture after the decoder:

- project the early temporal C4 line state back to full decoder resolution;
- run a second C4 orientation-consensus block over the projected line state conditioned on decoder appearance;
- learn an agreement gate between decoder appearance, early line state, and full-resolution continuity evidence;
- feed the supported continuity feature to a dual evidence head that combines region evidence with line-continuity evidence before producing `mask_logits`;
- keep trusted `line_logits` and `centerline_logits` auxiliary outputs shape-matched to the provider targets.

The continuity bridge is differentiable model logic only. It does not threshold, skeletonize, morphologically connect components, postprocess, apply Artifact Filters, or derive new labels.

## Contract Features Used

The Candidate uses only provider-advertised `abi_16ch_plus_sza_temporal` tensors. The manifest requests trusted `temporal_eligible_center` frame selection, temporal offsets `[-1, 0, 1]`, source-balanced sampling, random mirroring, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, and trusted Line/Centerline auxiliary targets with weighted BCE. Candidate code does not load data, inspect temporal cache state, download frames, repair or pad temporal neighbors, select samples, implement losses/metrics/augmentation, derive targets, use Dataset Source identity, use longitude/latitude, set thresholds, postprocess predictions, apply Artifact Filters, write external artifacts, choose GPUs, or schedule resources.

## Expected Effect

The intended effect is to preserve ABI-285's fixed-threshold recall/source balance while improving filtered connectivity toward ABI-223/238 and reducing the fragmented recall-heavy behavior seen in ABI-285's failure buckets. A useful result would show higher connectivity than ABI-285 with no large recall collapse and no catastrophic MIT/Google imbalance.

## Budget

Use the exploratory/default budget: 12 epochs, batch size 2, constant learning rate, disabled early stopping, and Harness-owned execution/resource limits. Do not request `late_improving` for this first mechanism-changing variant.

## Success Criteria

A useful exploratory result should be finite, non-collapsed, resource-safe, and source-informative. It need not beat the mature temporal comparators immediately, but should show at least one of:

- materially higher filtered connectivity than ABI-285 without losing most of ABI-285's recall;
- a better recall/connectivity tradeoff than ABI-274/285;
- lower negative-patch clutter or a smaller filtered footprint than ABI-285 at comparable Dice;
- an improving or ambiguous epoch-12 trajectory that justifies bounded continuation.

## Fallback Next Decision

Do not repeat this exact bridge unchanged if it merely lowers recall while keeping ABI-285-level weak connectivity, collapses into broad low-precision clutter, underpredicts like conservative C4 branches, or has numerical/resource failure. If finite and late-improving with better connectivity or cleaner clutter, consider a late-improving close continuation or temporal-eligible failure-bucket diagnostics in a later Autonomy Step.
