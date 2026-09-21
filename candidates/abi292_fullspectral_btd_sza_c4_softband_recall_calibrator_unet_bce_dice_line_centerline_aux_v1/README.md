# ABI-292 C4 soft-band recall calibrator U-Net

Family-development continuation after ABI-283 in the full-spectral BTD+SZA C4/orientation-prior branch.

ABI-292 keeps the ABI-283 resource-profiled C4 U-Net body and changes the mask head. The new head adds bounded detail/line recall support in a differentiable soft evidence band that decays with learned region-logit confidence and is vetoed by learned clutter disagreement. The goal is to recover part of ABI-283's lost fixed-threshold recall while preserving compact high-precision, high-connectivity C4 behavior.

Contract boundary:

- input mode: `abi_16ch_plus_sza` only;
- no longitude/latitude, Dataset Source identity, data loading, temporal lookup, sampling implementation, augmentation implementation, custom losses, custom metrics, thresholds, postprocessing, Artifact Filters, downloads, or resource scheduling;
- trusted `combined_source_balanced` sampling and `random_mirroring` augmentation;
- trusted `bce_dice` primary loss with Line and Centerline auxiliary targets;
- exploratory 12-epoch budget, no late-improving request.

Primary comparisons: ABI-283, ABI-249, and ABI-202. See `PROPOSAL.md` for criteria.
