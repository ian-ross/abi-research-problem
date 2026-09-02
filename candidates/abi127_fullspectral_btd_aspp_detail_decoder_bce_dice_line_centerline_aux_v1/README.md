# ABI-127 full-spectral BTD ASPP/detail decoder BCE-Dice Line+Centerline auxiliary

ABI-127 is a controlled family-development continuation of ABI-126. It keeps the compact full-spectral BTD ASPP/detail decoder and trusted `bce_dice` primary loss, then adds a provider-derived low-weight Line Target auxiliary head alongside the existing Centerline Target head.

## Intended comparison

Primary target: ABI-126 (`run_20260831_085615_d05ab3`). ABI-126 produced strong capped precision/connectivity and Google filtered Dice but weaker MIT recall. ABI-127 tests whether wider trusted line-support supervision can recover some MIT recall without giving up BCE-Dice positive-area discipline.

## Contract boundaries

- Input mode: `abi_16ch`; no longitude, latitude, reconstructed coordinates, or unapproved inputs.
- Outputs: `mask_logits`, `centerline_logits`, and `line_logits`.
- Losses and auxiliary targets are manifest-selected from provider/Harness allowlists.
- Candidate code defines only the PyTorch model architecture and deterministic channel combinations from approved ABI channels.
- Data loading, splits, capped-record selection, sampling policy, augmentation, target derivation, losses, metrics, Artifact Filters, resource placement, execution, and lifecycle remain provider/Harness-owned.

## Expected evidence

This is capped representative evidence only. Useful outcomes are finite/non-collapsed training, resource feasibility under the active 25M-parameter and 3,600-second limits, and source-stratified insight into whether line auxiliary supervision improves ABI-126's MIT recall while preserving precision/connectivity.
