# ABI-362 full-spectral BTD+SZA C4 decoupled anchor/recall-sidecar late36

This Candidate is a close, mechanism-changing continuation of the single-frame C4/orientation-prior branch after ABI-353, ABI-342, ABI-343, and ABI-249.

## Scientific intent

ABI-353 recovered positive-tail recall relative to ABI-249 but paid with extra negative-patch clutter, lower compact precision, and weaker connectivity. ABI-342/343 showed that direct recall bridges and precision vetoes tend to oscillate between broad recall states and compact low-recall states. ABI-362 therefore separates the final mask evidence into:

1. a compact C4 anchor logit, and
2. a bounded recall sidecar that can add only gated, architecture-internal residual evidence near the anchor's smooth uncertainty band.

The goal is to keep ABI-249/ABI-353 compact line evidence while recovering useful threshold-0.5 positives without Candidate-owned thresholds, postprocessing, Artifact Filters, custom losses, data loading, or sampling.

## Contract choices

- `input_mode`: `abi_16ch_plus_sza`
- `output_form`: `mask_logits`
- trusted sampling policy: `combined_source_balanced`
- trusted augmentation: `random_mirroring`
- trusted primary loss: `bce_dice`
- trusted auxiliary targets: Line (`line_logits`) and Centerline (`centerline_logits`) with `weighted_bce`
- optimizer/scheduler: AdamW, constant learning rate
- batch size: 4

The Candidate consumes only provider-approved ABI channels 1-16 plus Solar Geometry Input. It does not use longitude, latitude, Dataset Source identity, temporal lookup, custom data loading, target derivation, metric code, Artifact Filters, threshold selection, postprocessing, downloads, or resource scheduling.

## Architecture summary

The model reuses the ABI-353 full-spectral BTD+SZA front end, signed-detail residual U-Net, ASPP bottleneck, and cross-scale C4/detail agreement module. The new `DecoupledAnchorRecallSidecarHead` predicts an anchor mask logit from compact C4/context features, predicts a bounded `tanh` recall delta from line/detail features, and adds the delta only through a learned agreement gate and the smooth anchor uncertainty band `4*p*(1-p)`.

## Budget request

The manifest remains valid under the exploratory 12-epoch budget. A `late_improving` request is included because the immediate C4/detail parents selected late checkpoints: ABI-353 at epoch 34, ABI-342 at epoch 36, and ABI-343 at epoch 32. If the Harness denies the request, the exploratory fallback is the bounded result.
