# ABI-043 Full-Spectral DeepLabV3+ Resource Pilot v1

This Candidate is the authorized one-epoch resource pilot for a new full-spectral DeepLabV3+ architecture family. It normalizes all 16 provider-approved ABI channels and feeds them to a randomly initialized SMP DeepLabV3+ model with a ResNet-18 encoder and one Contrail Mask logit output.

The Candidate never receives longitude or latitude and loads no files, checkpoints, or pretrained weights. The provider and Harness retain ownership of data loading, Leakage-Safe Splits, bounded-record selection, Source-Balanced Sampling, augmentation, targets, loss, metrics, Artifact Filters, optimization, device placement, resource enforcement, prediction retention, and execution.

This pilot is limited to one epoch, at most 32 records per Dataset Source and split, batch size 4, sequential execution, and current trusted resource ceilings. Successful completion provides finite and resource evidence only. It does not authorize concurrency, a representative scout, full-data training, architecture ranking, or promotion.
