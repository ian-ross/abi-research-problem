# ABI-071 full-spectral BTD frequency-gated line U-Net soft-evidence-gate focal-Tversky continuation

## Hypothesis

This is a **family-development continuation** of the full-spectral BTD frequency-gated line U-Net branch. ABI-068 is the current strongest local whole-validation-tested Candidate by aggregate filtered Dice, but its focal-Tversky recall gain increased negative-patch clutter and reduced precision/connectivity relative to ABI-066. ABI-069 and ABI-070 showed that direct suppressor or output-residual heads can recover only limited precision while costing too much recall or connectivity.

The hypothesis is that a neutral-initialized, low-amplitude, feature-space evidence gate can recover some ABI-066-style precision/connectivity without materially weakening ABI-068's recall-forward focal-Tversky behavior. The gate modulates decoder features before the primary mask head, rather than applying candidate-owned thresholding, postprocessing, Artifact Filters, or hard logit suppression.

## Comparison Target

Primary comparison target: ABI-068 (`run_20260828_010836_4ccc77`), the frequency-gated focal-Tversky branch with whole-validation filtered Dice 0.3951 and capped best-validation filtered Dice 0.3964.

Secondary operating-profile target: ABI-066 (`run_20260827_230540_bf4ce3`), which has lower aggregate filtered Dice than ABI-068 but stronger precision/connectivity and lower predicted-positive burden.

Negative controls for interpretation: ABI-069 confidence suppressor and ABI-070 centerline-guided output residual, both of which failed to improve the ABI-068 tradeoff.

## Expected Effect

Expected successful behavior is a bounded operating-profile shift from ABI-068 toward higher precision or connectivity while preserving most of ABI-068's recall and source-balanced Dice. A useful result would keep aggregate filtered Dice near ABI-068, avoid source-specific collapse, and reduce the filtered predicted-positive fraction or improve filtered precision/connectivity relative to ABI-068.

A negative result would show that even neutral feature-space gating still imposes a recall/connectivity cost, supporting a broader move away from suppressive/gated head changes.

## Implementation Sketch

Start from ABI-068's architecture, input path, trusted loss, and auxiliary-target policy:

- provider-approved `abi_16ch` input only;
- normalized raw ABI channels plus ABI-channel-derived thermal BTD planes and learned 1x1 channel mixing;
- frequency-split stem, high/low frequency decoder fusion, and oriented line refiner retained from ABI-068;
- trusted focal-Tversky primary loss;
- provider-derived `centerline` auxiliary output with trusted `weighted_bce` at weight 0.02.

The controlled architecture change is a `SoftCenterlineEvidenceGate` after frequency-pyramid fusion. It concatenates refined features, local high-frequency detail, and broader smoothed context, predicts a `tanh` feature gate initialized exactly to zero, and applies only a small `0.10 * sigmoid(centerline_logits) * gate * evidence_features` residual to decoder features before the primary mask head. The primary mask head remains direct and the centerline head remains a normal auxiliary output.

## Contract Features Used

- `input_mode: abi_16ch`
- `output_form: mask_logits`
- `data.sampling_policy: combined_source_balanced`
- `data.frame_selection_policy: all_target_frames`
- `data.augmentation_policy: random_mirroring`
- `training.loss: focal_tversky`
- `training.optimizer: adamw`
- `training.scheduler.policy: constant_lr`
- `auxiliary_targets: centerline` with trusted `weighted_bce`, output `centerline_logits`, weight `0.02`

Candidate code defines model architecture only. It does not use longitude or latitude, reconstruct coordinates, implement data loading, sampling, augmentation, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem side effects, network access, or pretrained weights.

## Budget Requested

Use the current Harness-owned representative capped policy and execution ceilings: up to 1,024 records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, constant learning rate 0.0003, disabled early stopping, trusted Docker/A100 execution, 3,600-second training wall-clock budget, and the fixed first-four prediction artifact retention policy. The candidate remains below the 25M-parameter smoke ceiling by construction, with an ABI-068/ABI-070-comparable resource envelope.

## Success Criteria

Treat this as capped family-development evidence, not a promotion claim. A successful continuation should:

- complete finitely with no all-negative/all-positive prediction collapse;
- remain non-catastrophic on both Dataset Sources, preferably MIT and Google filtered Dice both at or above 0.35;
- keep aggregate capped filtered Dice within about 0.01 of ABI-068 or improve it;
- improve at least one of filtered precision, filtered connectivity, or filtered predicted-positive fraction relative to ABI-068 without dropping filtered recall below about 0.37;
- avoid the severe connectivity regression observed in ABI-069 and the larger recall loss observed in ABI-070.

If it exceeds ABI-068 on capped aggregate filtered Dice or matches ABI-068 while improving precision/connectivity/clutter, the next step should be a whole-validation failure-bucket Evaluation Request.

## Fallback/Next Decision

If ABI-071 repeats ABI-069/070-style recall or connectivity degradation, do not continue this exact gating branch. Prefer either a non-suppressive architecture-family scout or a Research Note that broadens the frontier toward different in-contract line-continuity/backbone choices.

If ABI-071 is finite and balanced but only trades precision for recall without net Dice gain, retain it as operating-profile evidence and compare it against ABI-066/ABI-068 before choosing whether diagnostics or a new family scout is more useful.
