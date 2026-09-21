# ABI-280 full-spectral BTD+SZA C4 selective-consensus recall bridge U-Net

ABI-280 is a mechanism-changing family-development continuation after ABI-249 and ABI-279 in the C4/rotation-aware line-context family.

ABI-279 showed that adding line/detail residual support to the ABI-249 C4 orientation prior can raise fixed-threshold recall and connectivity, but whole-validation diagnostics found lower precision and broader negative-patch clutter. ABI-280 keeps the same provider-approved full-spectral ABI+SZA input, ABI-channel-derived BTD front end, signed-detail U-Net body, ASPP context, C4 steerable line context, BCE-Dice loss, source-balanced sampling, trusted random mirroring, and trusted Line/Centerline auxiliary heads.

The architectural change is a more selective final head. Instead of always adding the line/detail residuals, ABI-280 predicts a learned consensus gate from region, line-context, and detail features. It adds smaller bounded recall support only where that learned evidence agrees, and applies a small bounded low-consensus clutter veto:

```text
recall_support = 0.16*consensus*tanh(line_logits) + 0.10*consensus*detail_gate*tanh(detail_logits)
clutter_veto   = 0.10*(1 - consensus)*clutter_gate*sigmoid(clutter_logits)
mask_logits    = region_logits + recall_support - clutter_veto
```

This is architecture-internal logit construction only. The Candidate does not choose thresholds, perform morphology, apply Artifact Filters, postprocess predictions, load data, select samples, implement losses/metrics/augmentation, use coordinates, or schedule resources.

The hypothesis is that ABI-280 can preserve more of ABI-249's compact high-precision behavior while retaining part of ABI-279's recall/connectivity lift. A `late_improving` budget request is included because the profiled C4 comparator selected late and ABI-279 required late-budget evidence to characterize the operating-point tradeoff. If denied, the Harness should run the manifest's exploratory 12-epoch budget.
