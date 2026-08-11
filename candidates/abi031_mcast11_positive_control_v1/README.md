# ABI-031 MCAST 1.1-lineage positive control

This manually authored Candidate tests the trusted Candidate Execution path with a familiar segmentation architecture. It derives the three MCAST 1.1 spectral planes from the provider-approved `abi_16ch` tensor, applies fixed MCAST 1.1 normalization, and feeds them to a randomly initialized SMP U-Net with a ResNet-18 encoder and one mask-logit output.

The Candidate contains no checkpoint or file loading and does not import the provider's Baseline Segmenter. It receives no longitude or latitude. The provider and Harness retain ownership of data loading, targets, loss, metrics, Artifact Filters, Baseline Segmenters, source-balanced sampling, augmentation, optimization, device placement, retries, execution, and evaluation.

This is a reliability positive control, not a retrained MCAST release. Passing its preregistered finite/non-degenerate criteria does not require beating canonical MCAST and does not authorize promotion or autonomous iteration.
