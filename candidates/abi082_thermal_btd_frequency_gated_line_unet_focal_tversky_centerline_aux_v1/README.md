# ABI-082 Thermal BTD frequency-gated line U-Net

ABI-082 is a bounded family-development continuation of the ABI-068 frequency-gated line U-Net branch. It changes the approved input mode from full ABI channels to `abi_thermal_10ch`, retaining only ABI channels 7-16 plus ABI-channel-derived thermal BTD planes and learned 1x1 thermal mixing.

The model keeps the ABI-068 frequency-split stem, residual encoder/decoder, frequency-pyramid fusion, oriented line refiner, trusted `focal_tversky` primary loss, and provider-derived `centerline_logits` auxiliary output with trusted `weighted_bce` weight 0.02.

Contract boundaries:

- no longitude or latitude inputs;
- no candidate-owned data loading, sampling, augmentation, target derivation, losses, metrics, thresholding, Artifact Filters, or postprocessing;
- no network access or pretrained weights;
- batch size 4, 12 epochs, constant learning rate 0.0003, and source-balanced sampling within the active Workspace Configuration.

Primary comparison target: ABI-068 (`run_20260828_010836_4ccc77`). Secondary references: ABI-066 precision/connectivity reference and ABI-081 no-auxiliary focal-Tversky continuation.
