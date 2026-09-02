# ABI-083 full-spectral BTD strip-pooling line U-Net

ABI-083 is a compact strip-pooling/ribbon-context line U-Net scout for GOES ABI Contrail Segmentation. It keeps provider-approved full-spectral ABI channel input and thermal BTD features, then adds feature-space row/column strip context at bottleneck and final high-resolution fusion stages.

The candidate selects only trusted manifest policies: combined source-balanced sampling, random mirroring, focal-Tversky primary loss, constant learning rate, and a provider-derived centerline auxiliary target. Candidate code owns only the model architecture and does not implement data loading, losses, metrics, Artifact Filters, thresholding, postprocessing, or resource control.
