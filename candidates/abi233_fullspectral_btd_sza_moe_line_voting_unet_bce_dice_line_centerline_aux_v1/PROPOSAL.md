# ABI-233 full-spectral BTD+SZA MoE line-voting U-Net

## Hypothesis

ABI-232 showed that the spectral/Solar Geometry Input mixture-of-experts branch can recover recall and source-balanced overlap under the approved late-improving budget, but it still trails ABI-202 and ABI-223 on connectivity and Google overlap. A bounded architecture-only continuation that adds differentiable multi-orientation line-voting support at the high-resolution fusion stage should preserve ABI-232's recall while restoring some of ABI-231/epoch-34-style connected-line evidence.

This is a **family-development continuation** of the ABI-231/ABI-232 spectral/SZA-regime MoE family, not a promotion candidate. It tests one architectural factor: explicit differentiable line accumulation inside the model, without changing the trusted data, loss, metric, Artifact Filter, sampling, augmentation, thresholding, or resource policy.

## Comparison Target

Primary comparison targets are:

- ABI-232 (`run_20260910_163616_4f7416`): same MoE family late36 parent; capped best `val/filtered_dice` 0.400942, recall 0.396756, connectivity 0.383636, MIT Dice 0.386542, Google Dice 0.439983.
- ABI-231 (`run_20260910_155936_362435`): first 12-epoch MoE scout; capped best `val/filtered_dice` 0.371985 and higher connectivity signature 0.398515.
- ABI-202 (`run_20260904_043143_ee0005`) and ABI-223 (`run_20260908_154531_8c7e2b`) remain broader frontier context, but ABI-233 is not required to beat these mature capped Results to justify the MoE branch.

## Expected Effect

Expected benefits:

- increase filtered Contrail Connectivity Metric versus ABI-232 by giving the high-resolution decoder an internal horizontal, vertical, diagonal, and anti-diagonal support path;
- retain or improve ABI-232 recall/MIT overlap by gating line support additively rather than using it as postprocessing or hard suppression;
- keep predicted-positive fraction in the same noncollapsed range by learning per-pixel support gates from provider-approved ABI/SZA-derived features.

Possible failure modes are lower precision from overextended line support, no connectivity gain, or regression below ABI-231/ABI-232 same-budget behavior. Those would be scientific negative results for this exact MoE line-voting branch, not a contract or capability blocker.

## Implementation Sketch

Start from the ABI-232 single-frame `abi_16ch_plus_sza` model:

1. keep the normalized ABI+SZA+BTD front end and learned 1x1 channel mixer;
2. keep the spectral/SZA-regime MoE stem, encoder, ASPP bottleneck, decoder, and high-resolution detail bridge;
3. add a compact differentiable `LineVotingSupport` module over the fused high-resolution features using depthwise horizontal/vertical strip convolutions and initialized diagonal/anti-diagonal depthwise convolutions;
4. learn soft orientation weights and sigmoid support gates from model features only;
5. feed the line-supported representation to trusted `mask_logits`, `line_logits`, and `centerline_logits` heads.

Candidate code will expose only `build_model(input_spec, output_spec)` and PyTorch architecture modules. It will not implement data loading, temporal lookup, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`.
- Input mode: provider-owned `abi_16ch_plus_sza` (`[17, 256, 256]`), excluding longitude and latitude.
- Output form: `mask_logits` plus trusted auxiliary `line_logits` and `centerline_logits`.
- Primary loss: trusted `bce_dice`.
- Auxiliary losses: trusted `weighted_bce` for Line Target and Centerline Target with weights 0.01 and 0.02.
- Sampling: trusted `combined_source_balanced`.
- Frame-selection policy: `all_target_frames`.
- Augmentation: trusted `random_mirroring`.
- Optimizer/scheduler: trusted `adamw` with constant learning rate 0.0003.

## Budget Requested

Use the default exploratory budget: 12 epochs, batch size 4, constant learning rate, disabled early stopping, single Harness-owned execution slot, and all current Workspace ceilings. Do not request the `late_improving` budget yet because ABI-233 changes architecture and needs same-budget feasibility/trajectory evidence first.

## Success Criteria

Treat ABI-233 as promising if it completes finite, noncollapsed training and shows at least one of:

- filtered Dice competitive with or above ABI-232's first-12-epoch family behavior while improving connectivity toward ABI-231/ABI-232 epoch-34 levels;
- filtered connectivity above ABI-232 selected checkpoint without a large recall or MIT Dice collapse;
- best checkpoint at or near epoch 12 with source-informative MIT and Google metrics, supporting a later approved late-improving continuation.

It is not required to beat ABI-202 or ABI-223 in this first 12-epoch architecture-change scout.

## Fallback/Next Decision

If ABI-233 fails static validation, smoke testing, or finite-state checks, create a repair Candidate only if the original hypothesis and comparison target can be preserved. If it completes but regresses below ABI-231/ABI-232 without a connectivity or trajectory advantage, classify the exact MoE line-voting continuation as a bad research result and broaden to a materially different Hough/Radon-style line accumulation scout or back to the ABI-223 temporal-attention frontier. If it improves connectivity and remains late-improving/source-informative, consider a close `late_improving` continuation under the approved budget-request path.
