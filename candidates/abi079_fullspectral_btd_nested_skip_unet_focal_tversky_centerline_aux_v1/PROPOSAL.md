# ABI-079 full-spectral BTD nested-skip U-Net scout

## Hypothesis

ABI-068 remains the strongest local whole-validation-tested Candidate by primary filtered Dice, but recent ABI-069 through ABI-078 continuations show a repeated local pattern: adding late suppressors, gates, extra inputs, axial/oriented necks, or simple loss swaps does not recover ABI-066's precision/connectivity while preserving ABI-068's recall and source balance. A broader in-contract step is to replace ABI-068's frequency-gated late-refiner architecture with a compact UNet++-style nested decoder that repeatedly fuses high-resolution ABI/BTD evidence with deeper cloud-context features before the final mask head.

This is a **family scout** for a nested-skip encoder-decoder family, not a full-data promotion claim. The expected value is diagnostic: test whether dense multi-depth skip refinement can reduce negative-patch clutter and improve connectivity/precision without candidate-owned thresholding, Artifact Filters, postprocessing, losses, data loading, or target derivation.

## Comparison Target

Primary local target: ABI-068, `abi068_fullspectral_btd_frequency_gated_line_unet_focal_tversky_centerline_aux_v1`, Run `run_20260828_010836_4ccc77`, because it is the current strongest local whole-validation-tested frequency-gated Candidate by aggregate filtered Dice and has full Working Validation Split diagnostics.

Secondary local target: ABI-066, `abi066_fullspectral_btd_frequency_gated_line_unet_cldice_centerline_aux_v1`, Run `run_20260827_230540_bf4ce3`, because it is the precision/connectivity-forward reference. ABI-076 through ABI-078 are recent evidence that simple SZA, axial-neck, and BCE-Dice modifications do not solve the ABI-068 operating-profile trade-off. Canonical MCAST 2.1 remains promotion context only.

## Expected Effect

The nested-skip scout is expected to:

- preserve full-resolution thin-line detail through repeated shallow/deep decoder fusion rather than one late refiner;
- let deeper cloud-context features suppress ambiguous cloud-edge false positives before final mask emission;
- retain ABI-068's focal-Tversky recall-oriented objective and centerline auxiliary supervision while changing the architecture family;
- improve filtered precision, filtered Contrail Connectivity, or negative-patch clutter relative to ABI-068 without requiring candidate-owned thresholds or postprocessing;
- remain resource-safe by using a compact base width and no pretrained encoder or external weights.

## Implementation Sketch

The candidate uses provider-approved `abi_16ch` input only. `model.py` normalizes ABI channels 1-16 using campaign-context safe ranges, derives thermal brightness-temperature-difference planes only from those approved channels, and adds learned 1x1 spectral projections. A compact four-level encoder builds full-, half-, quarter-, and eighth-resolution features. The decoder uses UNet++-style nested fusion nodes: each node concatenates same-depth earlier features with upsampled deeper features and refines them with residual convolution blocks. A final multi-depth aggregator combines several full-resolution nested nodes plus projected deeper context before emitting `mask_logits` and `centerline_logits`.

No candidate-owned data loading, split logic, sampling, augmentation transforms, losses, target derivation, metrics, threshold selection, Artifact Filters, postprocessing, filesystem writes, network calls, pretrained weights, or training loop logic are introduced. The model does not receive longitude, latitude, or reconstructed coordinate inputs.

## Contract Features Used

- Input mode: `abi_16ch` only; no longitude/latitude or coordinate-derived inputs.
- Output form: primary `mask_logits` with shape `[1, 256, 256]`.
- Auxiliary target: provider-derived `centerline` target emitted as `centerline_logits` with trusted `weighted_bce` at weight 0.02.
- Primary loss: trusted `focal_tversky`.
- Data policy: provider-owned `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Optimizer/training policy: `adamw`, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate scheduler, and disabled early stopping under the current Workspace Configuration.

## Budget Requested

Run sequentially under the current Workspace Configuration: at most 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, 3,600-second Docker training timeout, fixed first-four prediction artifacts, constant learning rate, disabled early stopping, and the 25M-parameter smoke ceiling. No Experiment Batch, extra concurrency, GPU selection, data-policy change, or full-data promotion evaluation is requested.

Because this is a materially different architecture family with no reviewed resource profile, it should remain sequential until the trusted Harness records resource behavior.

## Success Criteria

Strong scout evidence would be any of:

- capped best `val/filtered_dice` within 0.02 of ABI-068 while improving filtered precision or filtered Contrail Connectivity by at least 0.03;
- capped best `val/filtered_dice` at or above ABI-066 with lower filtered predicted-positive fraction than ABI-068;
- both MIT and Google filtered Dice above 0.35 with no all-negative/all-positive prediction collapse;
- a finite, late-improving trajectory that suggests a bounded nested-skip family-development follow-up even if it does not beat ABI-068 immediately.

Hard stop evidence for this exact scout would be smoke failure, parameter/resource infeasibility, non-finite behavior, prediction collapse, aggregate filtered Dice below 0.30 with no late improvement, or a clearly more permissive positive-area profile than ABI-068 without compensating Dice/connectivity gains.

## Fallback/Next Decision

If ABI-079 is finite and close to ABI-068 while improving precision/connectivity or reducing predicted-positive burden, continue the nested-skip family with one bounded follow-up or request whole-validation failure-bucket diagnostics if it becomes a local promotion candidate. If it underperforms but improves late and remains source-balanced, treat it as scout evidence rather than eliminating the family after one run. If it fails resource or smoke checks, repair only if the nested-skip hypothesis and comparison target are preserved; otherwise broaden to another architecture family or trusted training-policy axis.
