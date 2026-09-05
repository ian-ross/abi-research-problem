# ABI-181 full-spectral BTD+SZA signed-detail full-scale skip ASPP late36 BCE-Dice centerline auxiliary v1

ABI-181 is an exact architecture close-continuation of ABI-173 with a candidate-local late-improving budget request. It keeps the signed high-resolution detail streams, full-scale skip ASPP decoder, trusted BCE-Dice primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced sampling traversal, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, and constant learning-rate scheduler.

The only intended research change from ABI-173 is the Harness-reviewed training budget class requested in `budget_request.yaml`: run up to 36 epochs if the late-improving budget is granted, otherwise fall back to the exploratory budget. Candidate source does not implement any custom training loop, data loading, target derivation, loss, metric, Artifact Filter, postprocessing, thresholding, sampling, augmentation, resource placement, runtime downloads, pretrained weights, or coordinate features.

Comparison references:

- Parent ABI-173: `run_20260901_234732_bd5917`; capped best epoch 12, filtered Dice 0.3962, whole-validation filtered Dice 0.3973.
- ABI-154 precision/connectivity reference: `run_20260901_071026_32d3ec`.
- ABI-130 prior SZA-aware ASPP/detail aggregate reference: `run_20260831_121006_7d24be`.
- ABI-068 broader capped aggregate/source-balance comparator: `run_20260828_010836_4ccc77`.

Contract boundaries: input mode `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, Dataset Source identity, labels, predictions, external data, and model weights are not candidate inputs. Outputs are primary `mask_logits` and auxiliary `centerline_logits` only.
