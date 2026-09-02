# ABI-148 full-spectral BTD+SZA ASPP/detail decoder low-LR BCE-Dice continuation

ABI-148 is a training-policy family-development continuation of ABI-130. It keeps the ABI-130 full-spectral BTD+SZA ASPP/detail architecture, trusted BCE-Dice primary loss, provider-derived Centerline Target auxiliary output, trusted combined source-balanced sampling, and trusted random mirroring, while lowering the AdamW learning rate from `0.0003` to `0.0002`.

## Candidate contract summary

- Research Problem: `goes_abi_contrail_segmentation`
- Input mode: `abi_16ch_plus_sza`
- Forbidden inputs: longitude and latitude are not used or reconstructed
- Primary output: `mask_logits`
- Auxiliary output: provider-derived Centerline Target via `centerline_logits`
- Primary loss: trusted `bce_dice`
- Auxiliary loss: trusted `weighted_bce` at weight 0.02
- Sampling/augmentation: trusted `combined_source_balanced` traversal with trusted `random_mirroring`
- Budget: batch size 4, max epochs 12, constant learning rate

Candidate code owns only architecture over provider-approved ABI channels 1-16 plus Solar Geometry Input. Provider/Harness code owns data loading, splits, bounded sample selection, sampling implementation, augmentation transforms, losses, metrics, thresholding, Artifact Filters, prediction retention, resource placement, and Run lifecycle.

## Rationale

ABI-130 is the strongest whole-validation-tested SZA-aware ASPP/detail reference, but its epoch trajectory was oscillatory and the whole-validation diagnostic showed a real tradeoff: SZA recovered recall and aggregate Dice relative to ABI-126 while adding negative-patch clutter and losing some connectivity. ABI-147 and nearby micro-architecture edits did not improve this tradeoff. ABI-148 therefore broadens from architecture tweaking to a controlled optimization-policy test: a slightly lower fixed learning rate may preserve ABI-130's default-threshold recall shift while making the BCE-Dice operating point less noisy and less clutter-prone within the same 12-epoch budget.
