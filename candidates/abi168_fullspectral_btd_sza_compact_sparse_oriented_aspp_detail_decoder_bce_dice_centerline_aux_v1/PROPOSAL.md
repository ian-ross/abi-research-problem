# ABI-168 full-spectral BTD+SZA compact sparse-oriented ASPP/detail decoder

## Hypothesis

Family-development continuation. ABI-167 attempted to move horizontal/vertical/diagonal line context from a late refinement head into many encoder and decoder stages, but the Run was classified as a `resource_failure` after exhausting the 3,600-second wall-clock budget. ABI-168 tests a resource-safe version of the same scientific idea: sparse early oriented context at selected high- and mid-resolution stages may preserve useful line-shape evidence before ASPP/detail fusion without the every-scale overhead that prevented ABI-167 from finishing.

## Comparison Target

Primary comparison targets are ABI-068 (`run_20260828_010836_4ccc77`) as the current capped filtered-Dice/source-balance reference, ABI-130 (`run_20260831_121006_7d24be`) as the SZA-aware ASPP/detail BCE-Dice reference, ABI-154 (`run_20260901_071026_32d3ec`) as the high-precision/high-connectivity full-scale skip ASPP/detail reference, ABI-166 (`run_20260901_173120_9c74ab`) as the negative late-oriented-line-bank predecessor, and ABI-167 (`run_20260901_182419_ca8406`) as the dense early-oriented resource failure.

## Expected Effect

The compact sparse-oriented design should complete within the active wall-clock budget while retaining enough pre-bottleneck oriented feature shaping to test whether earlier line context helps thin Contrail Mask continuity. Useful evidence would be finite, non-collapsed training; filtered Dice in or near the current leader band; filtered connectivity closer to ABI-130/154 than ABI-166; and no large precision loss or predicted-positive inflation. If the sparse design finishes but remains below ABI-166/154 on both Dice and connectivity, that would weaken the case for further oriented-context work in this ASPP/detail branch.

## Implementation Sketch

Start from ABI-167's provider-approved full-spectral BTD+SZA ASPP/detail decoder. Keep normalized ABI channels, deterministic thermal BTD planes from allowed GOES ABI channels, normalized and cosine Solar Geometry Input, detail/context stems, ASPP bottleneck, decoder, full-scale skip fusion, final line-aware refinement, and `mask_logits` plus `centerline_logits` outputs. Reduce model width from base 40 to base 32, reduce the learned front-end projection from 16 to 12 channels, and reduce full-scale skip branch width from 16 to 12. Replace every-scale oriented blocks with sparse neutral additive oriented blocks only after the stem, encoder scales 1 and 2, decoder scale 1, and high-resolution detail branch. The oriented blocks still use local residual, horizontal, vertical, and fixed diagonal/anti-diagonal averages with a bounded learnable residual scale. No data loading, target construction, loss, thresholding, postprocessing, sampling, or augmentation logic is added to Candidate code.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza`; no longitude or latitude inputs.
- `output_form: mask_logits` plus provider-derived `centerline_logits` auxiliary output.
- Trusted primary loss `bce_dice` and trusted auxiliary loss `weighted_bce` for `centerline` at weight 0.02.
- Provider/Harness-owned `combined_source_balanced` sampling traversal and `random_mirroring` augmentation.
- Candidate code owns architecture only; it does not implement data loading, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, sampling, augmentation, resource placement, network access, or pretrained weights.

## Budget Requested

Use the active bounded representative policy: 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, max 12 epochs, batch size 4, constant learning rate 0.0003, AdamW, disabled early stopping, A100 placement owned by the Harness, 3,600-second training timeout, and the configured first-four prediction retention policy.

## Success Criteria

Treat this as capped family-development evidence, not promotion-grade full-data evidence. Success requires a completed finite non-collapsed Run and no contract/resource failure. Scientifically useful continuation evidence would be aggregate `val/filtered_dice` within roughly 0.005-0.010 of ABI-068/130/154, filtered connectivity above ABI-166 and preferably near ABI-130, MIT and Google filtered Dice both remaining in the current competitive band, modest raw-to-filtered dependence, and filtered predicted-positive fraction comparable to recent BCE-Dice leaders. A smaller resource footprint with similar Dice/connectivity to ABI-166 is still useful because it gives a viable platform for one subsequent loss or placement follow-up.

## Fallback/Next Decision

If ABI-168 still times out, treat the dense/sparse early-oriented ASPP/detail branch as resource-incompatible at the current representative budget and broaden to a different compact architecture family rather than adding more oriented blocks. If it completes finitely but underperforms ABI-166 and ABI-154 on both filtered Dice and connectivity, do not keep local oriented-context variants in this branch. If it completes near the leader band or shows a clear connectivity/source-balance gain, consider one controlled follow-up such as focal-Tversky or a single placement/width adjustment, still under Harness-owned limits.
