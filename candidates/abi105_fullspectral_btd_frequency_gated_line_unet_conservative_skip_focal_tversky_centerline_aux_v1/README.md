# ABI-105 full-spectral BTD frequency-gated line U-Net conservative-skip continuation

Family-development Candidate for GOES ABI Contrail Segmentation. This candidate starts from ABI-068, the current strongest local full-validation-tested frequency-gated focal-Tversky reference, and changes the decoder skip fusion so high-resolution skip features can be retained or attenuated but not amplified.

ABI-068's skip gate multiplied skip features by `0.5 + sigmoid(gate)`, allowing up to 1.5x amplification. ABI-105 instead uses `0.35 + 0.65 * sigmoid(gate)`, a bounded non-amplifying range of 0.35x to 1.0x. The hypothesis is that false-positive clutter and recall-heavy positive-area expansion may be reduced earlier in the decoder without adding another late mask-head, output-side consensus module, postprocessing step, custom threshold, custom loss, or candidate-owned Artifact Filter.

The model uses only provider-approved GOES ABI channels 1-16 plus deterministic BTD planes derived from those same channels. It emits `mask_logits` and provider-derived `centerline_logits`; it receives no longitude, latitude, or reconstructed coordinate inputs.

All data loading, split logic, capped-record selection, sampling implementation, augmentation implementation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned.
