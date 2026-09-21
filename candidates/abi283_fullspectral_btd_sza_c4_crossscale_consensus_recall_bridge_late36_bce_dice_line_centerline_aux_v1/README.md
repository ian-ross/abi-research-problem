# ABI-283 full-spectral BTD+SZA C4 cross-scale consensus recall bridge U-Net

ABI-283 is a mechanism-changing family-development continuation after ABI-249, ABI-279, and ABI-280 in the C4/rotation-aware line-context family.

ABI-279 showed that adding C4 line/detail residual support can raise fixed-threshold recall and connectivity, but whole-validation diagnostics found lower precision and broader negative-patch clutter. ABI-280 made that bridge more selective, improving MIT/recall but losing connectivity and Google compactness. ABI-283 keeps the same provider-approved full-spectral ABI+SZA input, ABI-channel-derived BTD front end, signed-detail U-Net body, ASPP context, C4 steerable line context, BCE-Dice loss, source-balanced sampling, trusted random mirroring, and trusted Line/Centerline auxiliary heads.

The architectural change is a cross-scale consensus head. It projects half-resolution decoder, quarter-resolution decoder, and ASPP-context features back to full resolution, then adds bounded C4 line/detail recall support only where the full-resolution C4 line context agrees with these multi-scale support features. A small low-consensus clutter veto uses architecture-internal disagreement/detail features.

```text
recall_support = 0.14*consensus*tanh(line_logits)
               + 0.10*consensus*tanh(multiscale_logits)
               + 0.06*consensus*detail_gate*tanh(detail_logits)
clutter_veto   = 0.07*(1 - consensus)*clutter_gate*sigmoid(clutter_logits)
mask_logits    = region_logits + recall_support - clutter_veto
```

This is model-internal logit construction only. The Candidate does not choose thresholds, perform morphology, apply Artifact Filters, postprocess predictions, load data, select samples, implement losses/metrics/augmentation, use coordinates, or schedule resources.

The hypothesis is that cross-scale agreement can preserve more of ABI-249's compact high-precision behavior while retaining ABI-279's useful recall/connectivity movement, especially by reducing ABI-279-style negative-patch clutter and ABI-280-style connectivity instability. A `late_improving` budget request is included because the profiled C4 comparators selected mid/late and this branch is resource-similar. If denied, the Harness should run the manifest's exploratory 12-epoch budget.
