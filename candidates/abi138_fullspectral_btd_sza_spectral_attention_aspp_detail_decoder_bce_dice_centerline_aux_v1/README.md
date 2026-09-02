# ABI-138 Full-Spectral BTD+SZA Spectral-Attention ASPP/Detail Decoder BCE-Dice Centerline Auxiliary v1

ABI-138 is a family-development continuation of ABI-130. It keeps the SZA-aware full-spectral BTD ASPP/detail decoder, trusted `bce_dice` primary loss, provider-derived `centerline_logits` auxiliary target at weight 0.02, `combined_source_balanced` traversal, `random_mirroring`, AdamW learning rate 0.0003, batch size 4, and the 12-epoch representative capped budget.

The controlled architecture change is upstream: the front end concatenates normalized ABI channels 1-16, deterministic thermal BTD planes, normalized SZA/`cos(SZA)`, and a learned 1x1 spectral/SZA mixture, then applies a neutral-initialized global channel-attention gate. The gate begins at identity scale and can learn solar-conditioned spectral reweighting during training.

Candidate code owns only model architecture over provider-approved inputs. It does not use longitude/latitude inputs, Dataset Source identity, candidate-owned data loading, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, training loops, runtime downloads, pretrained weights, scheduler logic, GPU placement, or external persistence.
