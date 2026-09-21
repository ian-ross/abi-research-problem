# ABI-301 compact MoE decoder line-memory U-Net

ABI-301 is a bounded family-development Candidate for GOES ABI Contrail Segmentation. It follows the compact spectral/Solar Geometry Input MoE branch after ABI-269 and ABI-270, but moves line-continuity support from a final conservative orientation head into the decoder stages.

The model consumes provider-approved `abi_16ch_plus_sza` tensors only. It normalizes ABI channels, appends ABI-channel-derived BTD features and Solar Geometry Input features, then uses a compact U-Net with spectral-regime MoE blocks. Decoder stages include differentiable horizontal/vertical/diagonal line-memory blocks so continuity support can shape features before the final mask logits.

The manifest uses trusted `combined_source_balanced` sampling, trusted `random_mirroring`, BCE-Dice primary loss, AdamW, constant learning rate, batch size 4, and trusted Line plus Centerline auxiliary targets. Candidate code does not own data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, sampling implementation, augmentation implementation, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

Comparison targets: ABI-269 compact MoE late36, ABI-270 final-head orientation-consensus test, ABI-265 line-memory comparator, ABI-249 C4 comparator, and ABI-202 aggregate reference.
