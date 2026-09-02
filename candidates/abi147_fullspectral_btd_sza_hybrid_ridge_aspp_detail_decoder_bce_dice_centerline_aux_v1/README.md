# ABI-147 full-spectral BTD+SZA hybrid ridge-ASPP/detail decoder

ABI-147 is a family-development continuation of the SZA-aware full-spectral BTD BCE-Dice frontier. It fuses ABI-130-style context/detail evidence with ABI-143-style horizontal and vertical ridge residuals at the model stem, then uses a compact ASPP/detail decoder and a line-aware refinement head.

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

Candidate code owns only architecture. Provider/Harness code owns data, splits, bounded sample selection, sampling implementation, augmentation transforms, losses, metrics, thresholding, Artifact Filters, prediction retention, resource placement, and Run lifecycle.

## Rationale

ABI-130 reached a strong capped BCE-Dice SZA-aware operating point with high Google filtered Dice and good calibration, while ABI-143 showed ridge-aware SZA+BCE-Dice features could recover some MIT recall. ABI-147 tests whether moving non-suppressive ridge residual evidence into the stem can recover some of ABI-143's MIT/source-balance benefits while keeping the ASPP/detail decoder calibration of ABI-130 and avoiding the late conservative suppression seen in ABI-146.
