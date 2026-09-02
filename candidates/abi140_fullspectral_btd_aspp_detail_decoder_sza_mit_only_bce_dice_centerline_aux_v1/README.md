# ABI-140 Full-spectral BTD+SZA ASPP/detail decoder MIT-only BCE-Dice Centerline auxiliary

ABI-140 is a data-policy continuation of ABI-130. It keeps the same provider-approved `abi_16ch_plus_sza` input, deterministic ABI-channel normalization, thermal brightness-temperature-difference planes, SZA-derived features, compact ASPP/detail decoder, trusted `bce_dice` primary loss, and provider-derived Centerline Target auxiliary head at weight 0.02.

The only intended manifest change from ABI-130 is selecting the trusted provider/Harness `mit_only` sampling traversal instead of `combined_source_balanced`. Candidate code does not implement sampling, data loading, target derivation, losses, metrics, augmentation, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or longitude/latitude features.

This capped representative run should test whether ABI-130s weaker MIT recall/source balance is a training-mixture effect or an architecture/loss limitation, while explicitly measuring the Google transfer cost.
