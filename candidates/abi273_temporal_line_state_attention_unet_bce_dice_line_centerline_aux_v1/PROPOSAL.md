# ABI-273 temporal line-state attention U-Net

## Hypothesis

ABI-223/238 showed that provider-owned three-frame temporal attention can be a strong temporal-family comparator, but recent ABI-271/272 evidence shows that loss-only recall pressure and final-head dual-evidence residuals are too late: they broaden positives or calibrate the output without improving connected thin-line continuity. ABI-273 tests whether line support must be carried as an explicit early temporal state, injected into the encoder pyramid before decoding, so the decoder sees motion/change evidence and center-frame line evidence at every scale rather than only at the final mask head.

Classification: mechanism-changing family-development continuation within the resource-profiled ABI-223/238 temporal-attention family.

## Comparison Target

Primary comparison target: ABI-238 (`run_20260911_004137_f54c45`) as the strongest recent temporal directional-context late36 comparator.

Secondary comparisons: ABI-223 (`run_20260908_154531_8c7e2b`) for the temporal-attention comparator, ABI-259 (`run_20260912_012708_f5897e`) for decoder-side line-support evidence, ABI-261 (`run_20260912_031837_f40c59`) for high-resolution line-accumulation recall evidence, and ABI-272 (`run_20260912_163151_b5c94d`) for the negative final-head dual-evidence result. ABI-202 (`run_20260904_043143_ee0005`) remains the aggregate reference, but ABI-273 is exploratory capped temporal-eligible evidence rather than a promotion claim.

## Expected Effect

The expected effect is a better threshold-0.5 precision/recall/connectivity balance than ABI-272 and ABI-259 by moving line evidence upstream. Useful evidence would include finite, non-collapsed temporal-eligible validation behavior, MIT/Google source-informative metrics, bounded predicted-positive fraction, improved connectivity over ABI-272/259 without ABI-271-like precision collapse, and resource use comparable to prior compact temporal candidates.

## Implementation Sketch

Start from the ABI-272 compact temporal-attention U-Net over provider-stacked `[-1, 0, 1]` ABI+Solar Geometry Input frames. Keep the finite per-frame ABI/SZA/BTD feature builder, temporal attention, U-Net encoder/ASPP decoder, BCE-Dice loss, trusted augmentation, and Line/Centerline auxiliary targets. Replace the final dual-evidence head with an early `TemporalLineStateStem`: temporal attention forms an appearance stream, temporal difference features form a change stream, and an orientation-aware line-state branch derives a bounded full-resolution line state before the encoder. A lightweight `LineStateInjector` injects the pooled line state into each encoder scale through learned gates. The final head is a simple shared segmentation/auxiliary head, not a threshold selector or postprocessing step.

This differs from ABI-259 because line support is not decoder-only; it differs from ABI-261 because there is no explicit recall-boosting mask head; it differs from ABI-272 because line/centerline evidence does not add a final residual to the mask logit.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Provider-owned frame selection: `temporal_eligible_center`.
- Allowed temporal frame offsets: `[-1, 0, 1]`.
- Output form: `mask_logits` with trusted auxiliary `line_logits` and `centerline_logits`.
- Trusted sampling policy: `combined_source_balanced`.
- Trusted augmentation policy: `random_mirroring`.
- Trusted primary loss: `bce_dice`.
- Trusted auxiliary loss: `weighted_bce` for Line and Centerline targets.
- Optimizer/scheduler: AdamW with constant learning rate.

Candidate code does not own data loading, temporal lookup, frame repair, sampling implementation, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle behavior.

## Budget Requested

Exploratory/default budget only: 12 epochs, batch size 2, constant learning rate, and the active capped provider-selected sample limits. No `late_improving` budget is requested for this first early-line-state mechanism. A later close continuation should request the approved 36-epoch budget only if this exploratory Run is finite, source-informative, non-collapsed, and selected near the epoch ceiling with an improving or ambiguous trajectory.

## Success Criteria

Success for continued temporal-family development does not require beating ABI-202 immediately. Continue only if ABI-273 is finite and source-informative and shows at least one of: improved connectivity over ABI-272/259 at a useful recall level, improved filtered Dice over ABI-272 with no large predicted-positive expansion, comparable or better recall than ABI-238 without ABI-271-level precision collapse, or a late/ambiguous improving trajectory with bounded resource use. Promotion-level interest would require approaching ABI-223/238 late36 capped Dice while improving recall/connectivity and preserving source balance.

## Fallback/Next Decision

If ABI-273 is finite but still trades between compact high-connectivity/low-recall states and broad low-connectivity states, stop this exact early-line-state injector. If it improves source balance or connectivity but remains under-trained with a clear late trajectory, consider one late-improving close continuation under the approved budget-request path. If it collapses, over-expands positives, or resource use approaches timeout, broaden away from temporal line-state variants rather than repeating final-head or loss-only changes.
