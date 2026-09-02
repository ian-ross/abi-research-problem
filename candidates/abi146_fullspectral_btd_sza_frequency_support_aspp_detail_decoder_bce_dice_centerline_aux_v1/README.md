# ABI-146 full-spectral BTD+SZA frequency-support ASPP/detail decoder BCE-Dice centerline auxiliary

Family-development continuation for GOES ABI Contrail Segmentation. This candidate preserves ABI-130's SZA-aware compact ASPP/detail encoder-decoder, trusted BCE-Dice primary loss, combined source-balanced traversal, trusted random mirroring, and low-weight provider-derived Centerline Target auxiliary head.

The controlled change is an additive frequency-support fusion block after the existing line-aware refinement. The block builds high-frequency detail, low-frequency cloud-context, horizontal, vertical, and dilated feature views from the decoded feature map and adds a bounded `0.15 * tanh(...)` feature residual before the mask and centerline heads. It does not threshold, postprocess, filter artifacts, derive new targets, or change loss computation.

The hypothesis is that ABI-130's whole-validation-confirmed SZA calibration can retain default-threshold recall while a non-suppressive frequency/context residual recovers some ABI-126/ABI-066 connectivity and negative-patch discipline. The model receives only provider-approved GOES ABI channels 1-16 plus Solar Geometry Input; it receives no longitude, latitude, reconstructed coordinate features, or Dataset Source identity.

All data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, and Run lifecycle remain provider/Harness-owned.
