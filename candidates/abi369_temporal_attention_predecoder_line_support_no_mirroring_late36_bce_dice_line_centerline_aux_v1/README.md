# ABI-369 temporal-attention pre-decoder line-support no-mirroring late36

ABI-369 is a controlled data-policy continuation of ABI-350 for GOES ABI Contrail Segmentation. It preserves the ABI-350 architecture and consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`.

## Motivation

ABI-350 is the current strongest capped temporal-eligible comparator, but recent temporal notes show that compact precision, fixed-threshold recall, and connected-line continuity often appear in different epochs. ABI-337 showed that disabling trusted random mirroring on a related temporal five-frame C4/detail-consensus branch produced a small MIT/recall shift while losing some connectivity and increasing clutter. ABI-369 tests the same allowlisted augmentation policy question on the stronger ABI-350 temporal-attention pre-decoder line-support scaffold, where physical GOES scan/illumination orientation might matter differently for attention and line-support gates.

## Architecture

The model is intentionally unchanged from ABI-350:

- finite per-frame ABI/Solar Geometry Input normalization;
- ABI-channel-derived thermal brightness-temperature-difference features;
- shared per-frame embedding and per-pixel temporal attention over `[-1, 0, 1]`;
- center/change fusion, U-Net encoder, and ASPP bottleneck;
- `PreDecoderLineSupportGate` modules at encoder skip scales 2, 1, and 0, using horizontal, vertical, and dilated diagonal line-support branches before decoder fusion;
- trusted `mask_logits`, `line_logits`, and `centerline_logits` outputs.

## Contract boundaries

Candidate code defines architecture only. It does not implement data loading, temporal lookup, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, training loops, downloads, coordinate inputs, Dataset Source identity, resource scheduling, or lifecycle behavior.

The manifest uses trusted `combined_source_balanced` sampling, disables augmentation via the allowlisted `none` policy, selects the trusted `bce_dice` primary loss, Line and Centerline `weighted_bce` auxiliaries, AdamW, constant learning rate, and batch size 2. A candidate-local budget request asks the Harness for the approved late-improving 36-epoch budget with exploratory fallback if denied.

## Expected evidence

ABI-369 is capped temporal-eligible evidence, not whole-validation promotion evidence. Success means preserving or improving ABI-350-like aggregate/source Dice while improving at least one targeted failure mode: MIT filtered Dice, fixed-threshold recall, or connected-line continuity, without a material broadening of filtered predicted-positive pixels or negative-patch clutter. If no-mirroring repeats ABI-337's pattern of small recall shifts with worse connectivity/clutter, the data-policy branch should be treated as characterized negative evidence rather than tuned locally.
