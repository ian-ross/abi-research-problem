# ABI-044 Full-Spectral DeepLabV3+ Representative Scout v1

This Candidate is the separately authorized 12-epoch representative scout for the full-spectral DeepLabV3+ ResNet-18 family that passed the ABI-043 resource pilot. It preserves the pilot architecture and optimization choices while expanding only the trusted Harness-owned record and epoch budgets.

The Candidate normalizes all 16 provider-approved ABI channels and produces one Contrail Mask logit plane. It never receives longitude, latitude, or Solar Geometry Input and loads no files, checkpoints, pretrained weights, or network resources. The provider and Harness retain ownership of data loading, Leakage-Safe Splits, capped-record selection, Source-Balanced Sampling, augmentation, targets, loss, metrics, Artifact Filters, optimization, device placement, resource enforcement, prediction retention, and execution.

The scout requests provider-owned representative selection of at most 1,024 records per Dataset Source and split, 12 epochs, batch size 4, and sequential execution. Its evidence is a capped family-feasibility screen, not full-data or promotion evidence. Low Dice alone is not an elimination criterion; continuation decisions must also consider finite behavior, collapse, optimization trend, source balance, and diagnostic differences.
