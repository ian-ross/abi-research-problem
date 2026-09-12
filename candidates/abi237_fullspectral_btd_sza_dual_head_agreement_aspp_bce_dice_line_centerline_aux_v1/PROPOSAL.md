# ABI-237 full-spectral BTD+SZA dual-head agreement ASPP scout

## Hypothesis

A compact internal agreement/calibration architecture can improve the precision/recall tradeoff of the single-frame BTD+Solar Geometry Input family without moving threshold selection or postprocessing into Candidate code. ABI-237 separates high-recall detail/context evidence from line-aware precision evidence, learns a feature-space agreement gate, and emits one fused `mask_logits` tensor plus trusted Line and Centerline auxiliary outputs.

## Classification

Family scout / early family-development broadening. This is not another local Radon gate tweak after ABI-236; it tests the underexplored matched calibration/uncertainty direction using only provider-approved `abi_16ch_plus_sza` tensors.

## Comparison target

Primary context is the current capped frontier (`abi202_fullspectral_btd_sza_crossscale_directional_consensus_aspp_late36_bce_dice_line_centerline_aux_v1`, Run `run_20260904_043143_ee0005`) and the recent non-frontier but relevant single-frame branches: ABI-235 Radon late36, ABI-236 recall-bypass Radon, and ABI-232 spectral-regime MoE late36. ABI-237 is expected first as a 12-epoch feasibility scout, not a required immediate promotion candidate against the mature ABI-202 incumbent.

## Expected effect

The recall branch should preserve faint local detail and full-scale context when the line-aware branch is too conservative. The precision branch should keep elongated structure and reduce diffuse false positives. The learned agreement gate should fuse them in logits/features, not by thresholding, morphology, Artifact Filters, or candidate-owned calibration. Useful evidence would be noncollapsed predictions, balanced MIT/Google metrics, and a filtered Dice/recall/connectivity profile competitive with recent single-frame scouts.

## Implementation sketch

- Normalize ABI channels 1-16 using bounded profile-derived constants, append approved-channel thermal BTD planes, normalized Solar Geometry Input, cosine Solar Geometry Input, and a learned 1x1 channel mixer.
- Use a residual U-Net with signed-detail stem, ASPP bottleneck, decoder skips, and full-scale feature fusion.
- Build two internal feature branches: a recall branch that emphasizes high-resolution detail/context and a precision branch with line-aware horizontal/vertical context.
- Learn a per-pixel/channel agreement gate from both branch features and their absolute difference; fuse features before producing the single required `mask_logits` output.
- Emit `line_logits` and `centerline_logits` only for trusted provider-derived auxiliary targets.

## Contract Features Used

- Provider-owned `abi_16ch_plus_sza` input mode with ABI channels 1-16 plus Solar Geometry Input; no longitude or latitude inputs.
- Trusted `combined_source_balanced` sampling policy, `all_target_frames` frame policy, and `random_mirroring` augmentation policy.
- Trusted `bce_dice` primary loss with provider-derived Line and Centerline auxiliary targets using allowlisted `weighted_bce` auxiliary losses.
- Harness-owned capped-record selection, metrics, Artifact Filters, checkpoint selection by `val/filtered_dice`, execution, and resource limits.

Candidate code defines only model architecture and allowlisted manifest choices. It does not implement data loading, split logic, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, runtime weight loading, coordinate inputs, Dataset Source identity, temporal cache access, or resource scheduling.

## Budget

Use the default exploratory budget: 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, constant learning rate, disabled early stopping, and one sequential Run. Do not request late-improving budget until this exact branch supplies finite, noncollapsed, final-epoch or late-upward evidence.

## Success Criteria

Continue the branch only if the Run is finite, resource-safe, noncollapsed, source-informative, and shows at least one of: filtered Dice in the neighborhood of recent broad scouts (roughly >= ABI-236's 0.384 capped filtered Dice), improved recall/connectivity balance versus ABI-236 or ABI-232, or a late trajectory suggesting the exploratory budget is truncating learning.

## Fallback Next Decision

Hard stop this exact branch on contract failure, non-finite training, persistent all-negative/all-positive predictions, severe source-specific collapse, or a clear plateau well below the recent scout neighborhood. If the branch is merely low-scoring but finite and diagnostically distinct, broaden next to a modern lightweight backbone or a temporal/Radon hybrid rather than making another local agreement-gate tweak.
