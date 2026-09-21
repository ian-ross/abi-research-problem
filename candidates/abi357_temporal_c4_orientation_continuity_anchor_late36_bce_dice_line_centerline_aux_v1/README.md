# ABI-357 temporal C4 orientation-continuity anchor late36

ABI-357 is a close, mechanism-changing continuation of ABI-356 for GOES ABI Contrail Segmentation. It keeps provider-owned temporal ABI+Solar Geometry Input tensors with offsets `[-1, 0, 1]`, trusted temporal-eligible center selection, source-balanced sampling, random mirroring, BCE-Dice loss, and Line/Centerline auxiliary targets.

## Mechanism

The model preserves ABI-356's temporal-attention stem, compact U-Net encoder/decoder, ASPP context, and multi-scale temporal-change/detail skip fusion. It adds a final high-resolution `C4ContinuityAnchor` that:

- applies one shared anisotropic strip-context block across four rotated feature views;
- learns soft orientation weights for C4 line context;
- combines weighted, mean, and max orientation context with signed detail;
- gates the compact line context against temporal decoder/high-resolution support before the mask, line, and centerline heads.

The intent is to keep ABI-356's recall-positive temporal evidence while constraining the broad positive footprint and improving connected thin-line continuity.

## Contract boundary

Candidate code defines model architecture only. It does not implement data loading, temporal lookup, target construction, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation, sampling, training loops, coordinates, Dataset Source identity, downloads, resource placement, or lifecycle behavior.

## Budget

`budget_request.yaml` requests the approved late-improving budget using ABI-356 and ABI-350 as parent evidence. If denied, the Harness should run the ordinary exploratory budget.
