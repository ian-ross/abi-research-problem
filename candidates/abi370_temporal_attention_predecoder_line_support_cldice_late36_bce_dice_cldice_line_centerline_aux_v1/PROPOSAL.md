# ABI-370 temporal-attention pre-decoder line-support clDice late36

## Classification

Family-development continuation in the temporal-attention / pre-decoder line-support family. This is a trusted-loss mechanism test, not a promotion claim and not whole-validation evidence.

## Hypothesis

ABI-350 remains the strongest capped temporal-eligible line-support scaffold, but recent ABI-356/359/367/369 evidence shows a recurring split between compact high-connectivity states and broader high-recall states. ABI-369 confirmed that a data-policy-only change can improve MIT Dice and recall but sacrifices Google balance, precision, and connectivity. The next bounded question is whether switching ABI-350 from trusted `bce_dice` to the allowlisted `bce_dice_cldice` primary loss can push the same architecture toward connected thin-line continuity while retaining enough fixed-threshold recall.

Expected effect: improve or preserve ABI-350-style source-balanced filtered Dice while raising filtered connectivity, and avoid the broad low-precision footprint seen in recall-heavy temporal variants.

## Comparison Target

- ABI-350 (`run_20260919_013306_9ca44e`): direct architecture parent and capped temporal-eligible comparator.
- ABI-369 (`run_20260920_155638_988238`): no-mirroring data-policy continuation showing the recall/connectivity trade-off.
- ABI-356 (`run_20260919_095725_843317`): recall-biased temporal comparator with weak connectivity.
- ABI-223 (`run_20260908_154531_8c7e2b`): mature temporal-attention connectivity comparator.

## Implementation sketch

Preserve ABI-350 model architecture exactly: finite ABI+SZA+BTD per-frame feature builder, shared frame projection, per-pixel temporal attention/change stem, U-Net encoder, ASPP bottleneck, pre-decoder orientation line-support gates at scales 2/1/0, and trusted `mask_logits`, `line_logits`, and `centerline_logits` outputs.

The controlled change is manifest-only: select the trusted allowlisted `bce_dice_cldice` primary loss instead of `bce_dice`. The Candidate does not implement a custom loss; clDice remains Harness/provider-owned. Line and Centerline auxiliary targets remain provider-derived `weighted_bce` auxiliaries with the same weights as ABI-350.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Trusted frame selection: `temporal_eligible_center`.
- Temporal offsets: `[-1, 0, 1]`.
- No longitude/latitude inputs.
- Trusted sampling policy: `combined_source_balanced`.
- Trusted augmentation policy: `random_mirroring`.
- Trusted primary loss: `bce_dice_cldice`.
- Trusted auxiliary targets: Line and Centerline with `weighted_bce`.
- Optimizer/scheduler: AdamW with constant learning rate.
- Candidate source defines architecture only and does not implement data loading, temporal lookup, sample selection, augmentation, losses, metrics, Artifact Filters, thresholds, postprocessing, training loops, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Budget Requested

Request the Harness-owned `late_improving` budget for 36 epochs via `budget_request.yaml`, with exploratory fallback if denied. ABI-350's selected checkpoint was late at epoch 33, and the relevant failure mode is a late-budget recall/connectivity trade-off; a 12-epoch exploratory comparison would likely understate the trusted-loss effect.

## Success criteria

ABI-370 is useful if it completes finitely and shows at least several of:

- improved filtered connectivity versus ABI-350 without a large filtered-Dice or source-balance regression;
- equal or better MIT/Google source balance than ABI-369 while avoiding ABI-369's connectivity drop;
- a more compact predicted-positive footprint than ABI-356/369 at comparable recall;
- no persistent prediction collapse, non-finite behavior, or source-specific catastrophic failure;
- a learning trajectory clarifying whether trusted clDice helps the temporal line-support scaffold combine compactness, continuity, and recall.

Hard-stop evidence for this exact branch would be contract/smoke failure, non-finite behavior, persistent prediction collapse, or a finite late-budget plateau below ABI-350/223 with no connectivity benefit and a broader clutter footprint.

## Fallback decision

If ABI-370 improves connectivity while preserving most ABI-350 Dice/source balance, request temporal-eligible failure-bucket diagnostics before more close continuations. If it broadens predictions or loses source balance without connectivity gains, do not submit another ABI-350 loss-only continuation; broaden to a different temporal backbone, single-frame recall/connectivity mechanism, or another trusted policy specifically tied to the observed failure mode. If the Harness denies the late budget, treat the exploratory fallback as the bounded Result and continue from its evidence.
