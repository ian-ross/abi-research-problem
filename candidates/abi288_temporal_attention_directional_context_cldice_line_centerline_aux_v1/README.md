# ABI-288 temporal attention directional-context clDice scout

ABI-288 is a loss-policy mechanism scout for GOES ABI Contrail Segmentation. It reuses the resource-profiled ABI-238 temporal-attention directional-context U-Net architecture over provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`, but changes the trusted primary loss from `bce_dice` to provider-owned `bce_dice_cldice`.

Hypothesis: ABI-238 and ABI-223 already provide strong temporal-attention evidence, but recent temporal C4/continuity branches showed that adding more line architecture often destabilizes precision/recall. A trusted clDice term may apply connectivity pressure during training while leaving architecture, thresholds, metrics, Artifact Filters, data loading, temporal lookup, sampling, and postprocessing under Harness/provider ownership.

This is an exploratory/default-budget Candidate, not a promotion claim. The comparison target is ABI-238 for temporal directional context and ABI-223/285 for temporal-family connectivity/recall behavior. Continuation evidence would be finite, source-informative training with improved connected-line continuity or a better Dice/connectivity tradeoff, not merely beating the whole-validation ABI-202 reference.
