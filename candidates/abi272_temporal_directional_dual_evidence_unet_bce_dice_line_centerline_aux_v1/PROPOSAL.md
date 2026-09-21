# ABI-272 temporal directional dual-evidence U-Net

## Hypothesis

ABI-238 showed that temporal attention plus a full-resolution directional-context bridge can preserve high precision in the temporal family, but it still leaves fixed-threshold recall and connected-line continuity below the ABI-202 aggregate reference. ABI-271 showed that simply selecting trusted focal-Tversky loss broadens positives and harms precision/connectivity. A differentiable dual-evidence head that couples the primary mask logits to learned line and centerline evidence should selectively lift true thin contrail logits where region and line support agree, improving recall without the clutter expansion seen in ABI-271.

Classification: family-development continuation within the resource-profiled ABI-223/238 temporal-attention family.

## Comparison Target

Primary comparison target: ABI-238 (`run_20260911_004137_f54c45`) as the strongest recent temporal directional-context continuation.

Secondary temporal comparisons: ABI-223 (`run_20260908_154531_8c7e2b`) for the temporal-attention comparator and ABI-271 (`run_20260912_155232_ec268d`) for the negative trusted-loss recall test. ABI-202 (`run_20260904_043143_ee0005`) remains the aggregate reference, but ABI-272 is exploratory capped temporal-eligible evidence rather than a promotion claim.

## Expected Effect

The expected effect is a better precision/recall/connectivity balance than ABI-271 and a recall/connectivity lift over ABI-238 without large growth in filtered predicted-positive fraction. Useful evidence would include finite, non-collapsed temporal-eligible validation behavior, MIT/Google source-informative metrics, and stable bounded resource use comparable to ABI-238/271.

## Implementation Sketch

Start from the ABI-238 compact temporal-attention U-Net over provider-stacked `[-1, 0, 1]` ABI+Solar Geometry Input frames. Keep the existing finite per-frame ABI/SZA/BTD feature builder, temporal-attention stem, U-Net encoder/ASPP decoder, and high-resolution directional-context bridge. Replace the independent final `mask_logits`, `line_logits`, and `centerline_logits` heads with `DualEvidenceSegmentationHead`: a shared refinement trunk emits a region mask logit, separate line and centerline branches emit the trusted auxiliary logits, and a small learned agreement gate adds bounded `tanh`-limited line/centerline residuals to the region logit. This is architecture-level logit formation only; it does not select thresholds or apply postprocessing.

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

Exploratory/default budget only: 12 epochs, batch size 2, constant learning rate, and the active capped provider-selected sample limits. No `late_improving` budget is requested for this first mechanism-changing dual-evidence head. A later close continuation should request the approved 36-epoch budget only if this exploratory Run is finite, source-informative, non-collapsed, and selected near the epoch ceiling with an improving or ambiguous trajectory.

## Success Criteria

Success for continued temporal-family development does not require beating ABI-202 immediately. Continue only if ABI-272 is finite and source-informative and shows at least one of: improved filtered recall over ABI-238 without ABI-271-level precision collapse, improved connectivity over ABI-238/271, comparable or better filtered Dice than ABI-238's 12-epoch temporal-family baseline, or a late/ambiguous improving trajectory with bounded filtered predicted-positive fraction. Promotion-level interest would require approaching ABI-223/238 late36 capped Dice while improving recall/connectivity and preserving source balance.

## Fallback/Next Decision

If ABI-272 regresses like ABI-271 by expanding positives, lowering precision, and not improving connectivity, stop this exact dual-evidence-head branch. If it is finite but under-tuned with a clear late trajectory and non-degenerate source metrics, consider one late-improving close continuation. If it improves recall but not connectivity, the next temporal hypothesis should move line support earlier into the decoder or temporal stem. If temporal dual-evidence remains weak, broaden to a different architecture family rather than repeating trusted-loss or final-head-only changes.
