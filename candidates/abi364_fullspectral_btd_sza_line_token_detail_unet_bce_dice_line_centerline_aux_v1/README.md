# ABI-364 full-spectral BTD+SZA line-token detail U-Net

ABI-364 is an exploratory family-development Candidate for GOES ABI Contrail Segmentation. It broadens away from recent single-frame C4 anchor/sidecar and source-detail-tail head tuning by placing low-rank row/column line-token support inside the decoder before final logits.

The model consumes only provider-owned `abi_16ch_plus_sza` tensors. It builds normalized ABI, approved-channel BTD, Solar Geometry Input, and learned per-pixel features; uses a compact residual U-Net/ASPP backbone; then fuses cross-scale decoder detail with row and column line tokens plus local strip context. A bounded agreement head combines region, line-token, and signed-detail support into `mask_logits` while exposing trusted `line_logits` and `centerline_logits` auxiliary outputs.

This is an exploratory 12-epoch scout, not a late-budget continuation or promotion claim. Candidate code defines architecture only. It does not implement data loading, sample selection, target derivation, custom losses, metrics, thresholding, postprocessing, Artifact Filters, coordinate inputs, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.
