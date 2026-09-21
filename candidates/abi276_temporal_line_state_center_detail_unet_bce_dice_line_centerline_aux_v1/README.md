# ABI-276 temporal line-state center-detail U-Net

ABI-276 is a mechanism-changing family-development continuation for GOES ABI Contrail Segmentation. It preserves ABI-274's provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`, trusted `temporal_eligible_center` selection, source-balanced sampling, random mirroring, BCE-Dice primary loss, AdamW constant learning rate, batch size 2, and trusted Line/Centerline auxiliary outputs.

The architectural change is to anchor ABI-274's temporal line state to center-frame high-resolution detail earlier in the network. A center-frame detail stem derives bounded local residual evidence from approved normalized ABI/SZA/BTD features, forms compact horizontal/vertical/diagonal detail support, and injects that detail state together with the temporal line state at every encoder scale. The full-resolution detail state is also included in the final refinement before the shared mask/Line/Centerline heads.

This tests whether center-frame thin-structure evidence can improve ABI-274's weak connected-line continuity and avoid the failed ABI-275 pattern of adding a post-decoder C4 bridge too late.

## Contract boundary

This Candidate does not implement data loading, temporal lookup, temporal padding or repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinate inputs, Dataset Source identity, resource scheduling, or lifecycle behavior.
