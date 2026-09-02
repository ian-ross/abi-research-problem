# ABI-110 full-spectral BTD frequency-gated line U-Net dual-logit margin

ABI-110 is a controlled family-development continuation of ABI-068. It keeps the ABI-068 full-spectral ABI + thermal BTD frequency-gated line U-Net backbone, trusted `focal_tversky` primary loss, trusted `combined_source_balanced` traversal, trusted `random_mirroring`, and provider-derived Centerline Target auxiliary head.

The only architecture change is the primary mask head. Instead of a single 1x1 `mask_logits` head, the model predicts two evidence planes and returns a fixed half-scale foreground-minus-background margin as `mask_logits`. The intent is to test whether explicit learned background evidence can improve precision, connectivity, or positive-area discipline without candidate-owned thresholding, postprocessing, Artifact Filters, losses, metrics, target derivation, data loading, sampling implementation, augmentation implementation, resource placement, pretrained weights, network access, or longitude/latitude inputs.

See `PROPOSAL.md` for the preregistered comparison target, success criteria, and fallback decision.
