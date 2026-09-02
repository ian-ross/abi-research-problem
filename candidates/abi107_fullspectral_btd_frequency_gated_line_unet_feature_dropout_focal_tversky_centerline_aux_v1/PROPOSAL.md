# ABI-107 — Feature-dropout regularized frequency-gated line U-Net

## Hypothesis

Low-probability channel/spatial feature dropout inside the best capped full-spectral BTD frequency-gated line U-Net will reduce brittle high-resolution clutter and source-specific spectral shortcuts while preserving the ABI-068 focal-Tversky recall operating point. This is a family-development continuation of ABI-068, not a new promotion claim from capped evidence alone.

## Comparison Target

Primary comparison target: ABI-068 (`run_20260828_010836_4ccc77`), the current local capped aggregate filtered-Dice reference for the frequency-gated line U-Net family at 0.3964 filtered Dice, MIT 0.3886, Google 0.4161, precision 0.3992, recall 0.3936, and filtered connectivity 0.3900.

Secondary comparison target: ABI-066 (`run_20260827_230540_bf4ce3`), the same family's precision/connectivity-forward BCE-Dice-clDice reference with 0.3825 filtered Dice, 0.4427 precision, 0.3367 recall, and 0.4731 filtered connectivity.

## Expected Effect

The added dropout should act as architecture-owned regularization rather than provider-owned data augmentation or postprocessing. Expected useful movement is either: (1) retain ABI-068-like aggregate/source filtered Dice while improving precision, connectivity, or positive-area discipline; or (2) reveal that ABI-068's late-improving capped trajectory depends on fragile feature co-adaptation, making a broader calibration/front-end change more appropriate.

## Implementation Sketch

Start from ABI-068's provider-approved `abi_16ch` full-spectral ABI plus deterministic thermal BTD front end, frequency-split stem, U-Net encoder/decoder, dilated bottleneck context, frequency-pyramid fusion, oriented line refiner, primary `mask_logits` head, and `centerline_logits` auxiliary head. Add `nn.Dropout2d` with low probabilities only to intermediate feature tensors after the stem/encoder/context and after final frequency fusion. The dropout modules are part of the neural architecture and are automatically inactive at evaluation time through PyTorch module mode. No target construction, loss logic, thresholding, postprocessing, or sampling behavior is moved into Candidate code.

## Contract Features Used

- Input mode: `abi_16ch` only; longitude/latitude channels are not requested or reconstructed.
- Output form: primary `mask_logits` plus provider-declared `centerline_logits` auxiliary output.
- Trusted primary loss: `focal_tversky`.
- Trusted auxiliary target: `centerline` with Harness-owned `weighted_bce` at weight 0.02.
- Trusted data policies: `combined_source_balanced` sampling and `random_mirroring` augmentation.
- Trusted training policy: AdamW, learning rate 0.0003, batch size 4, max epochs 12, `constant_lr`, disabled early stopping by workspace policy.

## Budget Requested

Use the active representative capped budget: at most 1,024 records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, one sequential Run under the 3,600-second Docker training timeout, fixed first-four prediction artifact retention, and the 25M-parameter smoke ceiling. Parameter count should remain essentially equal to ABI-068 because dropout adds no learned parameters.

## Success Criteria

Useful continuation evidence if the Run completes finitely without all-negative/all-positive collapse and satisfies at least one of:

- aggregate filtered Dice is within 0.01 of ABI-068 while filtered precision or filtered connectivity improves by at least 0.02;
- aggregate filtered Dice improves over ABI-068, with both MIT and Google filtered Dice at least 0.36;
- positive-area burden drops by at least 10% relative to ABI-068's filtered predicted-positive fraction without recall falling below 0.36;
- the trajectory is late-improving and source-balanced with a diagnostically distinct precision/recall/connectivity tradeoff relative to ABI-066/068.

Hard stop for this exact branch if training is non-finite, predictions collapse, either Dataset Source falls below 0.30 filtered Dice, or aggregate filtered Dice is more than 0.03 below ABI-068 without a compensating precision/connectivity gain.

## Fallback/Next Decision

If ABI-107 improves precision/connectivity or positive-area discipline without damaging ABI-068's source balance, continue with one bounded regularization-family follow-up such as dropout placement/probability reduction. If it regresses or merely trades recall for precision below the success criteria, stop this feature-dropout branch and broaden to a materially different contract-compliant calibration, spectral front-end, or architecture-family mechanism rather than repeating small skip/data-policy tweaks.
