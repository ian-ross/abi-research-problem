# ABI-165 Full-Spectral BTD+SZA Soft Ridge-Gate U-Net BCE-Dice Line+Centerline Auxiliary v1

Family-development continuation of ABI-143. The model preserves the SZA-aware full-spectral BTD soft ridge-gate U-Net and trusted BCE-Dice calibration, adding only a low-weight provider-derived Line Target auxiliary head alongside the existing Centerline Target head.

The goal is to test whether trusted line supervision can recover connectivity without Candidate-owned postprocessing, target transforms, threshold changes, data loading, losses, metrics, Artifact Filters, scheduling, pretrained weights, or runtime downloads.

See `PROPOSAL.md` for the hypothesis, comparison targets, contract features, budget, success criteria, and fallback decision.
