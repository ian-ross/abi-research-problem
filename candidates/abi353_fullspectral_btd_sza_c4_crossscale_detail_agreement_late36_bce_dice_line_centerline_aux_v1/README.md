# ABI-353 full-spectral BTD+SZA C4 cross-scale detail agreement late36

ABI-353 is a late-improving family-development continuation of ABI-352 for GOES ABI Contrail Segmentation. It intentionally preserves the ABI-352 single-frame architecture and training policy while requesting the approved `late_improving` budget.

## Motivation

ABI-352 was finite, resource-safe, source-informative, and selected its best checkpoint at the final exploratory epoch 12. Its final state recovered more fixed-threshold recall than ABI-249, while earlier epochs briefly showed more compact/high-connectivity states. The open question is whether longer training can align the epoch-10 compact/connectivity state with the epoch-12 recall/Dice gains rather than prematurely judging the pre-head cross-scale detail-agreement mechanism after one exploratory run.

## Architecture

The model is unchanged from ABI-352:

- provider-approved `abi_16ch_plus_sza` input only;
- finite ABI/Solar Geometry Input normalization with ABI-channel-derived thermal brightness-temperature-difference planes;
- compact encoder/decoder with C4 rotation-shared anisotropic line context;
- pre-head cross-scale detail-agreement fusion of full-resolution decoder features, signed high-resolution detail, stem evidence, and coarser decoder context;
- trusted `mask_logits`, `line_logits`, and `centerline_logits` outputs.

## Contract boundaries

Candidate code defines architecture only. It does not implement data loading, target derivation, sampling, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, training loops, downloads, coordinate inputs, Dataset Source identity, resource scheduling, or lifecycle behavior.

The manifest uses trusted `combined_source_balanced` sampling, `all_target_frames`, `random_mirroring`, BCE-Dice primary loss, Line and Centerline `weighted_bce` auxiliary targets, AdamW, and constant learning rate. A candidate-local budget request asks the Harness for the approved 36-epoch late-improving budget with exploratory fallback if denied.

## Expected evidence

ABI-353 is capped representative evidence, not whole-validation promotion evidence. Success means the late continuation improves ABI-352's source-balanced filtered Dice and either preserves its recall gain with better compactness/connectivity or reveals a clear late-budget failure mode for the cross-scale detail-agreement mechanism.
