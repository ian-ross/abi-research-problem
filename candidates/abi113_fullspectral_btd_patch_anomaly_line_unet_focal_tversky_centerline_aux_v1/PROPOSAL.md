# ABI-113 full-spectral BTD patch-anomaly line U-Net focal-Tversky continuation

## Hypothesis

ABI-068 remains the capped aggregate filtered-Dice reference, while ABI-066 remains the precision/connectivity reference. Recent local head, deterministic-front-end, soft thermal-support, and line-propagation changes did not recover a better tradeoff. A different in-contract continuation is to keep ABI-068's successful full-spectral BTD frequency-gated encoder/decoder, focal-Tversky loss, learned spectral mixer, and Centerline Target auxiliary supervision, but add patch-relative anomaly features beside fixed normalized raw and BTD features.

This is a **family-development continuation** within the full-spectral BTD frequency-gated line U-Net family. It is not a full-data promotion claim. The hypothesis is that per-patch z-scored raw-channel and BTD anomaly planes will make thin-contrail evidence less sensitive to Dataset Source and scene-background radiance shifts, improving source balance, precision/connectivity, or late-epoch stability without moving thresholding, Artifact Filters, losses, metrics, data loading, or sampling into Candidate code.

## Comparison Target

Primary local target: ABI-068, `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, because it is the current capped aggregate-Dice reference for this family.

Secondary target: ABI-066, Run `run_20260827_230540_bf4ce3`, because it is the precision/connectivity reference. Recent negative evidence from ABI-109 through ABI-112 motivates a front-end anomaly representation rather than another local output-head, soft thermal support, or line-propagation refiner. Canonical MCAST 2.1 remains the full Working Validation Split promotion context; this Run is capped representative feasibility evidence only.

## Expected Effect

The patch-anomaly front end is expected to:

- preserve ABI-068's fixed normalized raw channels, thermal BTD planes, learned 1x1 mixing, frequency-split stem, U-Net body, and oriented line refiner;
- add local per-patch standardized raw/BTD contrast features so thin cold/cloud-phase anomalies remain visible across MIT and Google background shifts;
- improve source balance or filtered precision/connectivity at comparable recall by separating local contrast evidence from absolute radiance background;
- avoid ABI-109's deterministic-front-end weakness by keeping a learned 1x1 mixer;
- stay resource-compatible with prior approximately 12M-parameter frequency-gated variants because the change only widens the model-owned front-end projection.

## Implementation Sketch

The candidate uses provider-approved `abi_16ch` input only. It computes fixed normalized GOES ABI channels 1-16 using the same bounded profile-derived constants as ABI-068, computes eight deterministic thermal BTD planes from approved ABI channels, computes per-patch z-scored raw-channel anomaly planes, and computes per-patch z-scored BTD anomaly planes. The z-scored anomaly features are clamped to a bounded range for numerical stability. A small learned 1x1 mixer operates over the concatenated fixed and anomaly features, and the existing ABI-068-like frequency-gated line U-Net consumes the resulting feature stack.

The model emits primary `mask_logits` and trusted provider-derived `centerline_logits`. No candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, threshold selection, Artifact Filters, postprocessing, filesystem writes, network calls, pretrained weights, or training loop logic are introduced. The model does not receive longitude, latitude, or reconstructed coordinate inputs.

## Contract Features Used

- Input mode: `abi_16ch` only; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` emitted as `centerline_logits` with trusted `weighted_bce` at weight 0.02.
- Primary loss: trusted `focal_tversky`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping under the current Workspace Configuration.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch, extra concurrency, GPU selection, data-policy change, custom evaluation, or full-data promotion evaluation is requested.

## Success Criteria

Useful continuation evidence would be any of:

- capped best `val/filtered_dice` within 0.01 of ABI-068 while improving filtered precision, filtered connectivity, or MIT/Google source balance;
- capped best `val/filtered_dice` exceeding ABI-066 while retaining filtered connectivity above 0.39;
- both MIT and Google filtered Dice above 0.38 with no prediction collapse and filtered predicted-positive fraction no larger than ABI-105's recall-forward profile;
- a finite, late-improving trajectory that identifies a better precision/connectivity versus recall tradeoff than ABI-109 through ABI-112.

Hard stop evidence for this exact branch would be smoke failure, non-finite behavior, persistent all-negative or all-positive collapse, aggregate filtered Dice below 0.37 with no compensating secondary metric, source-specific catastrophic degradation, or a larger positive-area/low-precision shift than ABI-068 without a connectivity gain.

## Fallback Next Decision

If ABI-113 improves source balance, filtered precision, or connectivity while retaining ABI-068-like aggregate behavior, consider a bounded whole-validation failure-bucket Evaluation Request before any promotion interpretation. If it is finite but misses all useful-continuation criteria, stop this exact patch-anomaly front-end branch and broaden to another materially different calibration, data-policy, or architecture mechanism. If it fails contract validation or smoke testing, classify and repair only if the original patch-relative anomaly hypothesis is preserved.
