# ABI-279 full-spectral BTD+SZA C4 dual-evidence recall bridge U-Net

ABI-279 is a close, mechanism-changing continuation of ABI-249, the high-precision C4/rotation-aware comparator. It keeps the ABI-249 full-spectral BTD+SZA front end, signed-detail U-Net body, ASPP context, C4 steerable line context, source-balanced training policy, BCE-Dice loss, and trusted Line/Centerline auxiliary heads.

The only architectural change is the final head. Instead of using a single refined mask head, ABI-279 predicts broad region evidence and line/detail evidence separately, then adds small bounded learned residual support to `mask_logits`:

```text
mask_logits = region_logits + 0.20*tanh(line_logits) + 0.15*gate*tanh(detail_logits)
```

The gate is learned from region, detail, and C4 line-context features. This is architecture-internal evidence fusion, not candidate-owned thresholding, morphology, postprocessing, or Artifact Filtering.

The hypothesis is that ABI-249's compact high-precision orientation prior can gain fixed-threshold recall and connected thin-line continuity without widening negative-patch clutter. A `late_improving` budget request is included because ABI-249 selected its best checkpoint at epoch 31 and this Candidate remains in that profiled C4 lineage. If denied, the Harness should run the manifest's exploratory 12-epoch budget.
