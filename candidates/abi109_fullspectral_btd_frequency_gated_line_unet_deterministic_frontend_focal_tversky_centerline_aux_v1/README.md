# ABI-109 deterministic-front-end frequency-gated line U-Net

ABI-109 is a controlled family-development continuation of ABI-068. It keeps the frequency-gated line U-Net topology, trusted focal-Tversky primary loss, provider-derived Centerline Target auxiliary supervision, combined source-balanced traversal, random mirroring, batch size 4, and 12-epoch capped representative budget.

The single architecture change is in the spectral front end: the learned 1x1 ABI mixer is removed. The model concatenates only deterministic normalized ABI channels 1-16 and explicit thermal BTD planes derived from provider-approved ABI channels. This tests whether the learned mixer contributes to false-positive clutter or numerical sensitivity while retaining the thin-line high/low spatial-frequency mechanism.

Candidate code owns only model architecture and approved manifest choices. It does not implement data loading, split logic, capped-record selection, sampling, augmentation, losses, targets, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem writes, network access, pretrained weights, or longitude/latitude inputs.
