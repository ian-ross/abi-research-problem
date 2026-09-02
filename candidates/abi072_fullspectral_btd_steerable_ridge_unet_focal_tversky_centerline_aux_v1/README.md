# ABI-072 full-spectral BTD steerable ridge U-Net

ABI-072 is a bounded family scout for GOES ABI Contrail Segmentation. It uses provider-approved `abi_16ch` tensors only, normalizes channels 1-16, appends ABI-channel-derived thermal BTD planes, and learns an additional 1x1 spectral mixture.

The architecture is a compact U-Net with non-suppressive steerable ridge-context blocks in the stem, encoder, bottleneck, decoder, and multi-scale head. Each ridge block softly mixes local, horizontal, vertical, and diagonal line-context branches to test whether oriented backbone context can recover precision/connectivity without candidate-owned thresholding, Artifact Filters, or postprocessing.

Contract choices:

- trusted `focal_tversky` primary loss;
- provider/Harness-owned `combined_source_balanced` sampling and `random_mirroring` augmentation;
- provider-derived `centerline` auxiliary target as `centerline_logits`, `weighted_bce` weight 0.02;
- batch size 4, 12 epochs, constant learning rate 0.0003.

The comparison targets are ABI-068 for aggregate Dice/recall-forward behavior and ABI-066 for precision/connectivity-forward behavior. This is capped scout evidence only, not a promotion claim.
