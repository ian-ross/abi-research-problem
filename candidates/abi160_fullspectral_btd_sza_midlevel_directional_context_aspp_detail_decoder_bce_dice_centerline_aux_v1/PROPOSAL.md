# ABI-160 Proposal: full-spectral BTD+SZA mid-level directional-context ASPP/detail decoder

## Hypothesis

ABI-159 and other local full-scale skip continuations showed that late recall bridges and extra auxiliary heads tend to broaden the fixed-threshold positive area while damaging precision and Contrail Connectivity. A more useful intervention may be to strengthen line-oriented evidence before the deepest ASPP bottleneck, while the feature map still preserves 64 x 64 spatial detail. ABI-160 tests whether a bounded mid-level horizontal/vertical/dilated context residual can improve thin-contrail continuity and default-threshold recall without giving back ABI-130/ABI-154-style source balance and negative-patch discipline.

Classification: **family-development continuation** of the SZA-aware ASPP/detail decoder family. It is not a promotion claim from capped evidence.

## Comparison Target

Primary comparison targets are ABI-130 (`run_20260831_121006_7d24be`) as the SZA-aware ASPP/detail aggregate/reference branch, ABI-154 (`run_20260901_071026_32d3ec`) as the whole-validation-tested precision/connectivity branch, and ABI-068 (`run_20260828_010836_4ccc77`) as the local capped aggregate/source-balance reference. ABI-159 is the immediate negative control for a late coarse-recall bridge.

## Expected Effect

The expected useful outcome is higher filtered recall and/or filtered Contrail Connectivity than ABI-130 with aggregate filtered Dice within roughly 0.005-0.010 of ABI-130/ABI-154, while preserving MIT and Google filtered Dice above about 0.37 and 0.41 respectively. Unlike ABI-159, the directional support is injected before ASPP bottlenecking rather than as a final positive-area bridge, so it should support continuous thin-line features without substantially increasing negative-patch clutter.

## Implementation Sketch

Start from the ABI-130 SZA-aware ASPP/detail decoder. Keep the normalized ABI channel front end, deterministic approved-channel thermal BTD planes, normalized Solar Geometry Input features, high-resolution detail path, ASPP context, decoder fusion, and final line-aware refinement. Add a `MidlevelDirectionalContext` module after the 64 x 64 encoder stage (`enc2`) and before the deepest downsampling/ASPP stage. The module fuses local 1x1 projection, horizontal 1x11 context, vertical 11x1 context, dilated 3x3 context, and smoothed broad context, then adds a small clamped residual to the encoder feature map. The candidate returns `mask_logits` and the provider-declared `centerline_logits` auxiliary output.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza` only; no longitude or latitude inputs.
- Output form: `mask_logits` primary output plus provider-declared `centerline_logits` auxiliary output.
- Primary loss: trusted `bce_dice`.
- Auxiliary target: trusted provider-derived `centerline` with `weighted_bce`, weight 0.02.
- Sampling traversal: trusted `combined_source_balanced`.
- Augmentation: trusted `random_mirroring`.
- Optimizer/training: AdamW, learning rate 0.0003, batch size 4, max epochs 12, `constant_lr` scheduler, disabled early stopping.
- Candidate code defines only architecture and approved manifest selections. Provider/Harness retains data loading, Leakage-Safe Split, capped-record selection, sampling implementation, augmentation implementation, target derivation, losses, metrics, thresholding, Artifact Filters, prediction retention, resource placement, and lifecycle.

## Budget Requested

Run one capped representative Candidate Experiment under the active Workspace Configuration: up to 1,024 records per Dataset Source and Leakage-Safe Split, max 12 epochs, batch size 4, constant learning rate, disabled early stopping, fixed first-four prediction retention, 25M-parameter smoke ceiling, one A100 GPU selected by the Harness, and 3,600-second Docker training timeout.

## Success Criteria

Useful continuation evidence is any of:

- aggregate filtered Dice matching or exceeding ABI-130/ABI-154 within about 0.005 while improving filtered recall or Contrail Connectivity;
- MIT filtered Dice at least 0.38 and Google filtered Dice at least 0.42 with no persistent all-negative/all-positive collapse;
- a finite improving epoch-12 trajectory with filtered precision at least 0.43 and recall at least 0.35, indicating a better calibrated default-threshold trade-off than ABI-159;
- diagnostically useful source-balanced behavior that separates pre-bottleneck directional context from late full-scale skip/recall-bridge failures.

Promotion would still require operator-reviewed full-validation diagnostics and comparison with canonical MCAST context.

## Fallback/Next Decision

If ABI-160 fails, collapses, becomes non-finite, or repeats ABI-159's precision/connectivity loss, do not repeat this exact mid-level directional-context branch unchanged. Prefer broadening to a different preprocessing/front-end inductive bias, data-policy/loss axis, or another architecture family rather than adding more late gates to the full-scale skip ASPP/detail branch. If ABI-160 preserves precision/connectivity while improving recall or source balance, consider a narrow follow-up or a whole-validation failure-bucket Evaluation Request in a later Autonomy Step.
