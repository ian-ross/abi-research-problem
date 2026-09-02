# ABI-073 full-spectral BTD frequency-gated line U-Net focal-Tversky with centerline and boundary auxiliaries

Family-development Candidate for GOES ABI Contrail Segmentation. This candidate keeps the ABI-068 frequency-gated line U-Net backbone, full-spectral ABI input, ABI-channel-derived BTD front end, trusted focal-Tversky primary loss, and trusted centerline auxiliary head at weight 0.02. It adds one low-weight provider-derived Boundary Target auxiliary head at weight 0.01.

The hypothesis is that a small trusted boundary-supervision signal can sharpen the focal-Tversky recall-forward ABI-068 operating point and reduce negative-patch clutter without moving thresholding, Artifact Filters, postprocessing, target derivation, losses, sampling, or augmentation into Candidate code. The model receives only provider-approved ABI channels 1-16 plus BTD planes derived from those same channels; it receives no longitude, latitude, or reconstructed coordinate inputs.

All data loading, split logic, sampling, augmentation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned.
