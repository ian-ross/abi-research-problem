# ABI-343 full-spectral BTD+SZA C4 precision-veto recall bridge

ABI-343 is a mechanism-changing continuation of the ABI-249/ABI-342 C4 orientation-prior branch for GOES ABI Contrail Segmentation.

It keeps the trusted single-frame `abi_16ch_plus_sza` input, source-balanced sampling, trusted random mirroring, BCE-Dice loss, Line and Centerline auxiliary targets, AdamW, constant LR, and batch size 4. The architecture starts from the ABI-342 C4 U-Net but replaces the direct recall bridge with a precision-vetoed head:

- anchor mask logits from C4 line-context features;
- positive recall lift only in an anchor-uncertainty band;
- recall lift gated by C4 line evidence and detail agreement;
- small differentiable veto where anchor uncertainty is high but line evidence is low.

The intended diagnostic is whether ABI-342's recall gain can be constrained toward ABI-249's compact high-precision footprint without Candidate-owned thresholding or postprocessing.

See `PROPOSAL.md` for the hypothesis, comparison targets, budget request, success criteria, and fallback decision.
