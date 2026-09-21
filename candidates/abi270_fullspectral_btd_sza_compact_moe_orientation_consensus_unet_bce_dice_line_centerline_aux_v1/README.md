# ABI-270 compact MoE orientation-consensus U-Net

ABI-270 is a mechanism-changing exploratory continuation of ABI-269's compact spectral/Solar Geometry Input MoE branch. It keeps the resource-safe compact MoE body but replaces the final line head with a conservative high-resolution multi-orientation consensus head intended to recover connected thin-line continuity without candidate-owned thresholding or postprocessing.

The Candidate consumes provider-owned `abi_16ch_plus_sza` tensors only and emits `mask_logits`, `line_logits`, and `centerline_logits`. It uses trusted source-balanced sampling, random mirroring, BCE-Dice primary loss, weighted-BCE Line and Centerline auxiliaries, AdamW, constant learning rate, batch size 4, and the exploratory 12-epoch budget.

Comparison targets are ABI-269, ABI-268, ABI-265, ABI-249, and ABI-202. Capped Run evidence from this Candidate is feasibility/family-development evidence, not whole-validation promotion evidence.
