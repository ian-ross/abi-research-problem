# ABI-262 overlap SegFormer line-decoder scout

## Hypothesis

A compact SegFormer-style overlap-attention encoder can model patch-scale cloud context more efficiently than the ABI-260 MaxViT scout while preserving more high-resolution thin-line evidence than the ABI-253 line-memory U-NetFormer branch. Combining overlap patch embeddings, spatial-reduction attention, a high-resolution signed-detail bridge, and a line-aware decoder should improve MIT/Google source-balanced recall/connectivity without candidate-owned thresholding or postprocessing.

## Classification

Family scout: this is an early scout of a compact SegFormer/MiT-like modern backbone. It is not expected to beat the mature ABI-202 whole-validation frontier on the first attempt, but it should provide useful evidence about whether overlap-attention is a better modern-backbone direction than the recent MaxViT and U-NetFormer variants.

## Comparison Target

- ABI-260 compact MaxViT line-context U-Net (`run_20260912_021616_d20946`) for same-budget modern-backbone resource and metric comparison.
- ABI-253 compact line-memory U-NetFormer late36 (`run_20260911_171333_f0b603`) as the strongest recent whole-validation-tested modern-backbone comparator.
- ABI-249 C4 steerable line-context late36 (`run_20260911_111909_dd7ef7`) as the high-precision rotation-aware comparator.
- ABI-202 (`run_20260904_043143_ee0005`) as the aggregate whole-validation frontier reference.

## Expected Effect

The expected effect is a finite, resource-safe modern-backbone scout that improves over ABI-260 in at least one of filtered recall, MIT filtered Dice, or filtered contrail connectivity while retaining bounded predicted-positive fractions and source-informative MIT/Google behavior. A lower score than ABI-202 is acceptable for this first scout; persistent collapse, resource failure, or a clearly weak plateau would stop the exact branch.

## Contract Features Used

- Provider-owned `abi_16ch_plus_sza` input mode only; no longitude or latitude inputs.
- Candidate-derived normalized ABI channels, ABI-channel BTD planes, Solar Geometry Input scalars, and learned 1x1 channel mixtures inside architecture code.
- Trusted `combined_source_balanced` sampling and `random_mirroring` augmentation selected in the manifest.
- Trusted `bce_dice` primary loss, AdamW optimizer, constant learning rate, batch size 4, and exploratory 12-epoch budget.
- Trusted Line and Centerline auxiliary targets via `line_logits` and `centerline_logits` with `weighted_bce` auxiliary losses.

## Implementation sketch

Build normalized ABI channels, approved-channel thermal BTD planes, Solar Geometry Input scalars, and learned 1x1 channel mixtures inside `model.py`. Feed them to a compact four-stage overlap-patch SegFormer encoder with spatial-reduction attention at 128, 64, 32, and 16 pixel scales. Fuse all stages with a SegFormer-style decoder, then restore full 256x256 resolution using a signed-detail bridge and learned orientation context. Emit `mask_logits`, `line_logits`, and `centerline_logits` for trusted Harness losses.

## Safety and candidate boundary

Candidate code defines only model architecture and manifest choices. It does not implement data loading, split logic, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, temporal lookup, downloads, coordinates, Dataset Source identity, resource scheduling, or training loops.

## Budget

Use the default exploratory budget: 1,024 provider-selected samples per Dataset Source/split, 12 epochs, batch size 4, constant learning rate, disabled early stopping, and sequential execution under the active Harness policy. No late-improving budget is requested for this first SegFormer scout.

## Success Criteria

This scout is positive if it completes finite and non-collapsed, remains under the 25M-parameter ceiling and exploratory timeout, and reaches roughly the ABI-260/modern-backbone scout band while improving at least one of recall, MIT filtered Dice, or connectivity without a large precision or false-positive-area collapse. A final-epoch best or clearly rising trajectory would justify one bounded SegFormer-family continuation. Persistent collapse, non-finite behavior, resource failure, or a clearly regressive/plateaued trajectory below the recent modern-backbone scout range would stop this exact branch.

## Fallback Next Decision

If ABI-262 is finite and non-collapsed with a final-epoch best or an improving trajectory near the modern-backbone scout band, keep one bounded SegFormer-family continuation eligible. If it is finite but clearly below ABI-260/ABI-253 without a useful recall/connectivity/source-specific signal, stop this exact overlap-attention branch and broaden to a different mechanism such as temporal attention/change or calibrated line evidence. If it fails contract, shape, resource, or numerical checks, classify the failure before deciding whether a repair Candidate is warranted.
