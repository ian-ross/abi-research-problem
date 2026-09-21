# ABI-303 full-spectral BTD+SZA C4 centerline-protected recall bridge U-Net

ABI-303 is a bounded C4/orientation-prior family-development continuation after ABI-283 and ABI-292. ABI-283 found a compact high-precision, high-connectivity C4 operating point but under-recalled true contrails; ABI-292 loosened support through a soft-band head and recovered too little recall while losing connectivity and precision. ABI-303 tests a mechanism-changing middle path: keep C4 steerable line context, but add bounded recall support from a learned centerline/detail stream when it agrees with line and multiscale decoder evidence.

The model consumes only provider-approved `abi_16ch_plus_sza` tensors. It normalizes ABI channels 1-16, derives fixed brightness-temperature-difference planes from approved channels, uses Solar Geometry Input, and learns a small 1x1 channel mixture. It does not consume longitude, latitude, Dataset Source identity, scene identifiers, patch paths, temporal cache state, or raw data roots.

The architecture is a compact signed-detail U-Net with ASPP context and a C4 rotation-shared line-context head. The new head differs from ABI-283/292 by introducing:

- a `centerline_refine` stream built from C4 line context, high-resolution detail, signed local detail, and multiscale decoder support;
- a precision gate driven by line/context/multiscale agreement and disagreement features;
- a recall gate driven by region, line, detail, centerline, and multiscale features;
- bounded residual support from line, centerline, detail, and multiscale logits; and
- a smaller learned disagreement veto than ABI-283 to reduce underprediction.

All recall/precision behavior remains ordinary differentiable model logic. Candidate code does not choose thresholds, postprocess predictions, perform morphology, implement losses, own Artifact Filters, select samples, implement augmentation, derive targets, load data, download resources, or schedule execution.

The manifest uses trusted `combined_source_balanced` sampling, trusted `random_mirroring` augmentation, trusted BCE-Dice loss, AdamW with constant learning rate, batch size 4, and trusted Line plus Centerline auxiliary targets. This first ABI-303 run requests only the default exploratory 12-epoch budget; a late-improving continuation would require separate Run evidence of finite, non-collapsed, source-informative late improvement.
