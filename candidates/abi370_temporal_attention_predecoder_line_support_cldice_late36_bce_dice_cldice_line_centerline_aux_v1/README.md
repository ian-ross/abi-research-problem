# ABI-370 temporal-attention pre-decoder line-support clDice late36

ABI-370 is a controlled trusted-loss continuation of ABI-350 for GOES ABI Contrail Segmentation. It preserves the ABI-350 architecture and consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`.

## Motivation

ABI-350 is a strong capped temporal-eligible line-support comparator, but recent temporal results repeatedly separate compact connected-line states from broader high-recall states. ABI-369 showed that disabling mirroring can raise MIT Dice and recall but hurts aggregate/source balance, precision, and connectivity. ABI-370 tests whether the trusted allowlisted `bce_dice_cldice` primary loss can move the same ABI-350 scaffold toward connected thin-line continuity without Candidate-owned postprocessing or threshold changes.

## Architecture

The model architecture is intentionally unchanged from ABI-350:

- finite per-frame ABI/Solar Geometry Input normalization;
- ABI-channel-derived thermal brightness-temperature-difference features;
- shared per-frame embedding and per-pixel temporal attention over `[-1, 0, 1]`;
- center/change fusion, U-Net encoder, and ASPP bottleneck;
- `PreDecoderLineSupportGate` modules at encoder skip scales 2, 1, and 0, using horizontal, vertical, and dilated diagonal line-support branches before decoder fusion;
- trusted `mask_logits`, `line_logits`, and `centerline_logits` outputs.

## Contract boundaries

Candidate code defines architecture only. It does not implement data loading, temporal lookup, sample selection, augmentation, losses, metrics, Artifact Filters, thresholds, postprocessing, training loops, downloads, coordinate inputs, Dataset Source identity, resource scheduling, or lifecycle behavior.

The manifest uses trusted `combined_source_balanced` sampling, `random_mirroring` augmentation, trusted `bce_dice_cldice` primary loss, Line and Centerline `weighted_bce` auxiliaries, AdamW, and constant learning rate. A candidate-local budget request asks the Harness for the approved late-improving 36-epoch budget with exploratory fallback if denied.

## Expected evidence

ABI-370 is capped temporal-eligible evidence, not whole-validation promotion evidence. Success means the trusted clDice loss improves filtered connectivity or preserves compact line continuity relative to ABI-350 while maintaining useful MIT/Google source balance and avoiding ABI-356/369-style broad low-precision footprints.
