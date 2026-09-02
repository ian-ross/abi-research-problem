# ABI-139 full-spectral BTD+SZA nested-skip U-Net BCE-Dice continuation

## Hypothesis

ABI-079 showed that the compact nested-skip U-Net family is resource-feasible and finite, but its focal-Tversky scout was too permissive: capped filtered Dice 0.2984, precision 0.2284, connectivity 0.1265, and predicted-positive fraction 0.00682. Later ABI-130 showed that adding provider-approved Solar Geometry Input and using trusted BCE-Dice can improve default-threshold calibration in the ASPP/detail branch, reaching capped filtered Dice 0.3953 and whole-validation filtered Dice 0.3954 with much better precision and positive-area discipline than recall-heavy branches.

ABI-139 is a **family-development continuation** of the nested-skip family and a broadened alternative to the recently negative SZA-aware ASPP/detail local-head tweaks. The hypothesis is that applying the ABI-130 calibration axis--`abi_16ch_plus_sza` input, deterministic thermal BTD/SZA features, and trusted `bce_dice`--to the ABI-079 nested-skip architecture will reduce the permissive positive-area profile and recover Google/precision behavior while preserving the nested decoder's high-resolution multi-depth evidence path.

## Comparison Target

Primary family target: ABI-079, `abi079_fullspectral_btd_nested_skip_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_104353_1455f1`, because it is the resource-feasible nested-skip scout that needs a specific precision/connectivity corrective hypothesis before further nested-skip work.

Primary calibration target: ABI-130, `abi130_fullspectral_btd_aspp_detail_decoder_sza_bce_dice_centerline_aux_v1`, Run `run_20260831_121006_7d24be` plus Evaluation `eval_evalreq_abi130_wholeval_failure_buckets_v1`, because it is the best SZA-aware ASPP/detail default-threshold reference with whole-validation diagnostic support.

Additional references: ABI-068 (`run_20260828_010836_4ccc77`) as the current capped aggregate/source-balance reference, ABI-066 (`run_20260827_230540_bf4ce3`) as the precision/connectivity-forward reference, and ABI-126 (`run_20260831_085615_d05ab3`) as the non-SZA ASPP/detail high-precision/connectivity comparator. Canonical MCAST 2.1 remains promotion context only.

## Expected Effect

The expected effect is not simply that a lightly tuned nested-skip continuation beats all mature references. Useful evidence would be:

- a large improvement over ABI-079 in filtered precision, filtered Dice, Google filtered Dice, connectivity, and predicted-positive fraction;
- a cleaner default-threshold operating point than ABI-079 because BCE-Dice and SZA temper the focal-Tversky recall-heavy profile;
- retention of multi-depth high-resolution decoder fusion as a distinct architecture path rather than another local ABI-130 ASPP/detail head tweak;
- finite, source-balanced behavior that clarifies whether the nested-skip family deserves one more bounded continuation or should be deprioritized.

## Implementation Sketch

`model.py` keeps the ABI-079 compact four-level UNet++-style nested decoder: encoder features at full, half, quarter, and eighth resolution; nested fusion nodes that combine same-depth and upsampled deeper features; and a final multi-depth evidence fusion block with horizontal/vertical high-resolution detail context.

The front end changes to provider-approved `abi_16ch_plus_sza`. It normalizes ABI channels 1-16 with fixed campaign-context-scale constants, derives thermal brightness-temperature-difference planes only from approved ABI channels, adds normalized SZA and `cos(SZA)`, and applies a learned 1x1 spectral/SZA mixer. The model emits primary `mask_logits` and provider-derived `centerline_logits` auxiliary output.

No candidate-owned data loading, split logic, sampling implementation, augmentation transforms, losses, target derivation, metrics, threshold selection, Artifact Filters, postprocessing, filesystem writes, network calls, pretrained weights, or training-loop logic are introduced. The model does not receive longitude, latitude, Dataset Source identity, or reconstructed coordinate inputs.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza`; provider-approved GOES ABI channels 1-16 plus Solar Geometry Input only.
- Forbidden inputs: no longitude, latitude, coordinate-derived feature, Dataset Source feature, or hidden geolocation proxy.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target emitted as `centerline_logits` with trusted `weighted_bce` at weight 0.02.
- Primary loss: trusted `bce_dice`.
- Data policy: provider-owned `combined_source_balanced` traversal and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping under the active Workspace Configuration.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch, extra concurrency, GPU selection, data-policy override, or full-data promotion evaluation is requested in this handoff.

ABI-079's nested-skip architecture already completed with about 6.63M parameters and feasible A100 memory. ABI-139 adds one provider-approved SZA plane and two derived SZA features at the front end, so it should remain well inside the parameter smoke ceiling; the Harness remains responsible for actual resource validation.

## Success Criteria

Strong family-development evidence would be any of:

- capped best `val/filtered_dice` improving ABI-079 by at least 0.05 while cutting filtered predicted-positive fraction by at least 0.0015;
- filtered precision at least 0.35 and filtered connectivity at least 0.30 with both MIT and Google filtered Dice above 0.35;
- aggregate filtered Dice within 0.02 of ABI-130 or ABI-068 while preserving a distinct precision/recall/connectivity trade-off;
- finite late-improving trajectory and non-collapsed source-stratified metrics that suggest a bounded nested-skip follow-up, even if it does not immediately beat ABI-130 or ABI-068.

Hard stop evidence for this exact branch would be smoke failure, parameter/resource infeasibility, non-finite training, persistent all-negative or all-positive predictions, aggregate filtered Dice below 0.32 with no late improvement, or continued ABI-079-like excessive positive area without compensating recall/connectivity gains.

## Fallback/Next Decision

If ABI-139 materially repairs ABI-079's permissive clutter while remaining source-balanced, consider one bounded nested-skip continuation or a whole-validation failure-bucket Evaluation Request only if it becomes locally competitive with ABI-130/ABI-068. If it is finite but merely partial, record it as nested-skip family evidence and compare its operating point against ABI-079, ABI-130, ABI-068, ABI-066, and ABI-126 before deciding further allocation. If it fails the hard-stop criteria, do not repeat this SZA+BCE nested-skip branch unchanged; broaden to another architecture, preprocessing/calibration, trusted loss, or data-policy frontier within the Candidate Experiment Contract.
