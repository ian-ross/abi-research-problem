# ABI-305 temporal attention line-memory calibrated U-Net

ABI-305 is a bounded temporal family-development Candidate for GOES ABI Contrail Segmentation. It returns to the ABI-223/238 temporal-attention backbone after recent local-correlation, five-frame additive, and C4 recall-bridge continuations repeatedly traded recall against precision or connectivity.

The model consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` selection. It keeps shared per-frame ABI/Solar Geometry Input feature construction, temporal-attention fusion, compact U-Net/ASPP decoding, and high-resolution directional context. The mechanism change is an internal multi-orientation line-memory calibration head: horizontal, vertical, and dilated diagonal line-memory features provide bounded recall support while a learned precision/disagreement gate can reduce support from inconsistent features.

This is architecture logic over provider-visible tensors and logits. It is not Candidate-owned thresholding, postprocessing, morphology, a loss, a metric, an Artifact Filter, or sample selection.

The intended effect is to recover some ABI-285-style fixed-threshold recall while preserving more ABI-223/238-style precision and connected-line continuity than the ABI-296/299 local-correlation branch or the ABI-304 five-frame additive branch.

Candidate code does not own temporal lookup, data loading, target derivation, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, coordinates, downloads, resource scheduling, prediction retention, or lifecycle behavior.

The Candidate uses trusted `combined_source_balanced` sampling, trusted `random_mirroring`, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, 12 exploratory epochs, and trusted Line plus Centerline auxiliary targets.
