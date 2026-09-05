# ABI-183 Full-Spectral BTD+SZA Signed-Detail Full-Scale Skip ASPP Line-Aux BCE-Dice Centerline Auxiliary v1

Controlled family-development continuation of the ABI-181 signed-detail full-scale skip ASPP branch. The architecture, provider-approved `abi_16ch_plus_sza` front end, BCE-Dice loss, source-balanced traversal, trusted random mirroring, learning rate, batch size, and constant scheduler are retained. The only research change is adding a provider-derived Line Target auxiliary head at weight 0.01 alongside the existing Centerline Target auxiliary head at weight 0.02.

The goal is to test whether direct line-mask supervision can improve continuity/MIT-source behavior without moving Artifact Filters, target derivation, losses, sampling, augmentation, thresholding, or training lifecycle into Candidate code.
