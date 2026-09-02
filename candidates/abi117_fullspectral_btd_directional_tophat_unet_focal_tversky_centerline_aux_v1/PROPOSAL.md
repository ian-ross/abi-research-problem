# ABI-117 directional-top-hat line U-Net continuation

## Hypothesis

A stem-level directional top-hat feature extractor over provider-approved full-spectral ABI and thermal BTD evidence will preserve ABI-068's focal-Tversky recall and source-balanced Dice while recovering some precision/connectivity lost to negative-patch clutter. Recent post-decoder ridge/detail gates and output-head suppressors tended to expand recall-heavy positive area or damage connectivity; ABI-117 moves the oriented residual mechanism earlier, as additive feature evidence before encoding, rather than as a late suppressive head or Artifact Filter surrogate.

This is a **family-development continuation** within the full-spectral BTD frequency-gated line U-Net family, not a promotion claim from capped evidence.

## Comparison Target

Primary comparison target: ABI-068 (`run_20260828_010836_4ccc77`), the current strongest local whole-validation-tested aggregate-Dice reference for this family.

Secondary comparison target: ABI-066 (`run_20260827_230540_bf4ce3`), the precision/connectivity-forward reference.

Recent negative context includes ABI-069/110 output-head suppression, ABI-113 patch-anomaly front-end widening, and ABI-116 post-decoder scale-selective ridge gating.

## Expected Effect

Expected positive signal is a cleaner feature representation for thin linear BTD residuals that reduces diffuse cloud-edge clutter without shrinking true contrail lines. Desired effects are:

- filtered Dice competitive with ABI-068, ideally within 0.01 while improving at least one of precision, connectivity, or predicted-positive fraction;
- MIT and Google filtered Dice both non-catastrophic and preferably above 0.36;
- filtered predicted-positive fraction no larger than ABI-068's 0.00357 unless recall and Dice both improve;
- no reliance on Artifact Filters, threshold changes, or candidate-owned postprocessing.

## Implementation Sketch

Start from the ABI-068 frequency-gated line U-Net topology and retain the focal-Tversky primary loss plus Centerline Target auxiliary output. Modify only model architecture:

1. Keep normalized ABI channels 1-16 and deterministic thermal BTD planes from approved ABI channel pairs.
2. Add a bounded directional-top-hat projection in the front end: local BTD residuals, horizontal residuals, vertical residuals, and broad-minus-local context are projected with a learned 1x1 mixer.
3. Replace the original three-branch frequency stem with a five-branch `DirectionalTopHatStem` that fuses raw, local-detail, broad-context, horizontal-top-hat, and vertical-top-hat projections before the existing encoder.
4. Leave the decoder, frequency pyramid fusion, `mask_logits`, and `centerline_logits` contract unchanged.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; no longitude or latitude inputs and no reconstructed coordinates.
- Output form: primary `mask_logits` with provider-declared auxiliary `centerline_logits`.
- Trusted primary loss: `focal_tversky`.
- Trusted auxiliary target/loss: `centerline` with `weighted_bce`, weight 0.02.
- Trusted data policy: `combined_source_balanced` sampling and `random_mirroring` augmentation.
- Harness-owned metrics, Artifact Filters, capped-record selection, training loop, resource placement, and lifecycle.

## Budget Requested

Use the active Workspace Configuration ceilings: 1,024 records per Dataset Source and split, 12 epochs, batch size 4, constant learning rate, disabled early stopping, one A100 under Harness ownership, 3,600-second Docker training timeout, and the fixed first-four prediction artifact retention policy. The model is intended to remain well below the 25M-parameter smoke ceiling.

## Success Criteria

Classify ABI-117 as useful family-development evidence if it completes finitely, avoids all-negative/all-positive collapse, respects the contract, and meets either:

- aggregate filtered Dice at least 0.386 with MIT and Google filtered Dice both at least 0.36 and no large precision/connectivity regression versus ABI-068; or
- aggregate filtered Dice at least 0.38 while improving filtered precision, filtered connectivity, or filtered predicted-positive fraction relative to ABI-068 enough to create a plausible cleaner operating point.

A stronger result would match or exceed ABI-068 aggregate filtered Dice while improving at least one ABI-066-associated secondary metric.

## Fallback/Next Decision

If ABI-117 is non-finite, collapses, exceeds the smoke/resource limits, or produces source-catastrophic behavior, stop this exact directional-top-hat branch and classify the failure before any repair. If it is finite but below 0.38 aggregate filtered Dice without a secondary-metric gain, do not request whole-validation diagnostics and broaden to a different architecture family or trusted loss/data-policy axis. If it is competitive with ABI-068 or provides a substantially cleaner precision/connectivity profile, request a bounded whole-validation failure-bucket evaluation before any promotion interpretation.
