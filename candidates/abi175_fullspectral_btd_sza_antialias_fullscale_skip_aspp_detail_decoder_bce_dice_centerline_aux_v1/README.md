# ABI-175 Full-Spectral BTD+SZA Anti-Aliased Full-Scale Skip ASPP/Detail Decoder BCE-Dice Centerline Auxiliary v1

This Candidate is a controlled family-development continuation of the SZA-aware ASPP/detail evidence path. It keeps the ABI-154 full-scale skip ASPP/detail architecture, provider-approved `abi_16ch_plus_sza` input, deterministic BTD features derived only from approved GOES ABI channels, trusted `bce_dice` primary loss, and provider-derived Centerline Target auxiliary supervision, but replaces each encoder max-pooling downsample with fixed binomial anti-aliased feature downsampling before residual encoding.

The hypothesis is that low-pass anti-aliasing before downsampling can preserve thin contrail evidence more consistently through the encoder, recovering some default-threshold recall without the local head/stem tradeoffs that weakened recent ABI-173/174 signed-detail variants.
