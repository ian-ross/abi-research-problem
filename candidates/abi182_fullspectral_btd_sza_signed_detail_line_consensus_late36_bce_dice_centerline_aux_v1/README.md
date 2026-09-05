# ABI-182 full-spectral BTD+SZA signed-detail line-consensus late36 BCE-Dice centerline auxiliary v1

ABI-182 is an exact architecture close-continuation of ABI-174 with a candidate-local late-improving budget request. It keeps ABI-174's conservative line-consensus feature calibration on top of the signed-detail full-scale skip ASPP decoder, using trusted BCE-Dice primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, and constant learning-rate scheduler.

The research question is whether ABI-174's final-epoch connectivity-improving line-consensus branch was truncated by the exploratory 12-epoch budget. ABI-181 showed that the signed-detail parent can gain materially under the Harness-owned late-improving budget; ABI-182 tests whether the existing line-consensus branch can recover aggregate/source Dice while retaining its connectivity advantage over ABI-173/181.

Comparison references:

- ABI-174 direct parent: `run_20260902_005632_5651ef`; capped final/best epoch 12, filtered Dice 0.3929, connectivity 0.3460.
- ABI-181 current aggregate reference: `run_20260902_150611_cbbf35`; capped best epoch 22 filtered Dice 0.4104 and whole-validation filtered Dice 0.4124, connectivity 0.3676 whole validation.
- ABI-154 precision/connectivity reference: `run_20260901_071026_32d3ec`.
- ABI-068 recall/connectivity and MIT/source-balance comparator: `run_20260828_010836_4ccc77`.

Contract boundaries: input mode `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, Dataset Source identity, labels, predictions, external data, and model weights are not candidate inputs. Outputs are primary `mask_logits` and auxiliary `centerline_logits` only. Candidate source does not implement custom data loading, target derivation, losses, metrics, Artifact Filters, postprocessing, thresholding, sampling, augmentation, resource placement, runtime downloads, pretrained weights, or Run lifecycle behavior.
