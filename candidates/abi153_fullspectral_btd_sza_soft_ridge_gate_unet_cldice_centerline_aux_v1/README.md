# ABI-153 Full-Spectral BTD+SZA Soft Ridge-Gate U-Net clDice Centerline Auxiliary v1

ABI-153 is a bounded family-development continuation of ABI-143. It keeps the same provider-approved `abi_16ch_plus_sza` input, full-spectral raw plus thermal BTD plus SZA front end, compact ridge-attention U-Net architecture, neutral-initialized conservative ridge gate, provider-derived Centerline Target auxiliary output at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, and constant learning rate.

The controlled manifest change is the trusted primary loss: ABI-153 changes ABI-143 from `bce_dice` to allowlisted `bce_dice_cldice`. The hypothesis is that clDice's continuity term may recover part of the line-connectivity lost by the soft ridge-gate BCE-Dice branch while preserving ABI-143's MIT recall and near-reference aggregate Dice.

Outputs:

- `mask_logits`: primary Contrail Mask logits.
- `centerline_logits`: provider-derived Centerline Target auxiliary output, `weighted_bce` weight 0.02.

The model receives no longitude, latitude, reconstructed coordinate features, Dataset Source identity, pretrained weights, or runtime downloads. Data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, and Run lifecycle remain provider/Harness-owned.
