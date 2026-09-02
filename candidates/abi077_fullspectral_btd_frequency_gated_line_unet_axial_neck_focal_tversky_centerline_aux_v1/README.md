# ABI-077 full-spectral BTD frequency-gated line U-Net axial-neck focal-Tversky continuation

Family-development Candidate for GOES ABI Contrail Segmentation. This candidate starts from ABI-068, the current strongest local whole-validation-tested frequency-gated reference by filtered Dice, and adds a low-capacity residual axial-continuity neck before the primary and centerline heads.

The neck mixes short and dilated horizontal/vertical context over the refined full-resolution features. The intended test is whether a lightweight feature-side continuity module can recover some ABI-066-like precision/connectivity and reduce negative-patch clutter while preserving ABI-068's focal-Tversky recall and source-balanced Dice. It is not an extra threshold, postprocessor, Artifact Filter, custom loss, or candidate-owned target transform.

The model uses only provider-approved ABI channels 1-16 plus BTD features derived from those same approved ABI channels; it receives no longitude, latitude, or reconstructed coordinate inputs. It emits `mask_logits` and provider-derived `centerline_logits` with the trusted weighted-BCE centerline auxiliary loss at weight 0.02.

All data loading, split logic, sampling, augmentation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, and Run lifecycle remain provider/Harness-owned.
