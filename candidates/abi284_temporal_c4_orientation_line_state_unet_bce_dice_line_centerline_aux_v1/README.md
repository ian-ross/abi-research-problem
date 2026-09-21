# ABI-284 temporal C4 orientation line-state U-Net

ABI-284 is a mechanism-changing temporal-family continuation after ABI-223, ABI-274, ABI-275, ABI-281, and ABI-282.

ABI-274 showed that an early temporal line-state attention mechanism can recover temporal recall/source balance, but temporal-eligible diagnostics found weak connected-line continuity. ABI-275 and ABI-282 tried adding C4/rotation-aware continuity late in the decoder and did not preserve the desired recall/connectivity tradeoff. ABI-284 moves the orientation prior earlier: it replaces the hand-built horizontal/vertical/diagonal temporal line-state extractor with a rotation-shared C4 orientation-consensus line-state module before the encoder pyramid.

The model consumes only provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]` and trusted `temporal_eligible_center` selection. Per-frame features are normalized ABI channels 1-16, ABI-channel-derived BTD planes, and Solar Geometry Input transforms. The C4 line-state module shares one anisotropic strip filter across 0/90/180/270-degree rotations, learns an orientation attention map, and injects the resulting bounded line state into the encoder scales. The final head remains a simple mask/line/centerline logit head rather than a threshold-like post-decoder residual bridge.

Hypothesis: organizing the early temporal line state with rotation-shared consensus should improve connected thin-line continuity versus ABI-274 without the post-decoder C4 underprediction seen in ABI-282 and without Candidate-owned thresholds, postprocessing, morphology, Artifact Filters, metrics, losses, data loading, temporal lookup, sample selection, coordinates, or resource scheduling.

This is an exploratory 12-epoch capped temporal-eligible scout. If it is finite, non-collapsed, and improves connectivity or the recall/connectivity balance versus ABI-275/281/282 while remaining within useful distance of ABI-223/274, it can justify bounded family development; otherwise the exact early C4 line-state integration should be deprioritized.
