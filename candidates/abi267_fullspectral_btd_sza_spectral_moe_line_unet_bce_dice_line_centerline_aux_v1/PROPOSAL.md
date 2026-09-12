# ABI-267 spectral-regime mixture-of-experts line U-Net

## Classification

Family scout. ABI-267 starts a bounded single-frame spectral/SZA-state mixture-of-experts branch, an underexplored in-contract direction relative to the heavily tuned ABI-202/ABI-249 spectral-ASPP/C4 frontier and recent temporal/attention scouts.

## Hypothesis

Thin contrails occupy different observable regimes across reflective/thermal channels and Solar Geometry Input. A compact architecture-internal mixture of spatial experts gated only by provider-approved ABI+SZA features may improve fixed-threshold source balance and precision/recall calibration without using Dataset Source identity, coordinates, scene identity, route priors, candidate-owned thresholding, postprocessing, data loading, losses, metrics, Artifact Filters, or sampling logic.

## Comparison target

Primary comparison targets are ABI-202 (`run_20260904_043143_ee0005`) as the current whole-validation aggregate frontier, ABI-249 (`run_20260911_111909_dd7ef7`) as the high-precision C4 comparator, and ABI-265 (`run_20260912_065321_ceab64`) as the recent line-memory capped continuation. Because ABI-267 is a first MoE scout, continuation decisions should also compare against early broad scouts rather than requiring it to beat the mature frontier immediately.

## Expected effect

The spectral/SZA expert gates should learn local operating regimes from normalized ABI channels, thermal brightness-temperature differences, and SZA-derived features. The expert blocks combine local detail, dilated context, and line-oriented evidence, aiming to preserve contrail continuity while selecting regime-specific feature transformations. Success would appear as finite non-collapsed predictions, useful MIT and Google metrics, and either a capped filtered Dice near the modern scout band or a diagnostically useful improvement in source balance, recall/precision tradeoff, or connectivity.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`.
- Input mode: `abi_16ch_plus_sza`; no longitude/latitude, Dataset Source identity, scene identity, or route/location priors.
- Output form: `mask_logits` plus trusted auxiliary `line_logits` and `centerline_logits`.
- Trusted loss/optimizer/scheduler choices: `bce_dice`, AdamW, constant learning rate.
- Trusted data choices: `combined_source_balanced`, `all_target_frames`, `random_mirroring`.
- Harness-owned resource limits: exploratory 12 epochs, batch size 4, fixed GPU/resource policy, provider-owned metrics and Artifact Filters.

## Implementation sketch

- Use provider-owned `abi_16ch_plus_sza` input only.
- Normalize ABI channels with fixed snapshot-scale constants; derive BTD planes only from approved ABI channels; include scaled SZA and cosine SZA.
- Use a compact U-Net with learned `RegimeMoEBlock` modules at encoder/decoder scales. Each block computes softmax expert gates from current features and mixes four bounded convolutional experts.
- Add a differentiable line-context decoder/head with horizontal/vertical strip convolutions and trusted Line plus Centerline auxiliary outputs.
- Select only trusted manifest options: source-balanced sampling, random mirroring, BCE-Dice primary loss, AdamW constant learning rate, batch size 4, and 12 exploratory epochs.

## Constraints

Candidate code remains architecture-only. It must not load data, select samples, derive targets, implement losses/metrics/Artifact Filters/thresholds/postprocessing/augmentation transforms, use longitude/latitude, use Dataset Source identity, discover temporal frames, download resources, write external artifacts, select GPUs, or manage lifecycle behavior.

## Budget

Exploratory/default budget: 12 epochs, batch size 4, constant learning rate, within the 25M parameter and 3,600-second exploratory ceilings. No late-improving budget is requested for this first MoE scout.

## Success Criteria

Continue the MoE family only if the run is finite/resource-safe and non-collapsed and shows one of: capped filtered Dice in the broad-scout/near-frontier band, improved source balance, useful connectivity, or a clearly improving trajectory that suggests one mechanism-changing continuation.

## Fallback Next Decision

Hard stop conditions for this exact branch are smoke/contract failure, non-finite training, persistent all-negative/all-positive collapse, severe source-specific collapse, or a clearly plateaued result far below comparable broad scouts without compensating diagnostic value. If ABI-267 is finite but only mixed, prefer one mechanism-changing MoE continuation focused on preserving connectivity or source balance; otherwise broaden to another underexplored family rather than repeating the same design unchanged.
