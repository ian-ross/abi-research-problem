# ABI-285 temporal C4 orientation line-state late36 U-Net

ABI-285 is a close late-improving continuation of ABI-284, the temporal C4 orientation-consensus line-state U-Net.

ABI-284 showed finite, resource-safe, non-collapsed behavior and selected its best checkpoint at the final exploratory epoch 12. It improved the recent temporal C4/detail exploratory branches (ABI-275/281/282) on filtered Dice, precision, and compactness, and it exhibited intermittent high-connectivity/high-precision states. It still trailed ABI-274 and ABI-223 on temporal-eligible filtered Dice, recall, and connected-line continuity, so this continuation is not a promotion claim.

The model architecture is intentionally unchanged from ABI-284. It consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` frame selection. Per-frame features are normalized ABI channels 1-16, ABI-channel-derived BTD planes, and Solar Geometry Input transforms. The early C4 orientation-consensus line-state module shares one anisotropic strip filter across 0/90/180/270-degree rotations, learns an orientation attention map, and injects the resulting bounded line state into the encoder scales.

Hypothesis: ABI-284's final-epoch best and oscillatory late trajectory indicate that the early orientation line-state mechanism may need the approved late-improving budget to stabilize a useful compromise. Longer training may recover more ABI-274 recall and ABI-223 continuity while preserving ABI-284's compact high-precision behavior.

This Candidate uses a `late_improving` budget request. It does not move thresholds, postprocessing, morphology, Artifact Filters, metrics, losses, data loading, temporal lookup, temporal repair/padding, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior into Candidate code.
