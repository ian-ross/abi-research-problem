# Proposal: ABI-284 temporal C4 orientation line-state U-Net

## Classification

Family-development continuation in the provider-owned temporal ABI input family. This is not a promotion claim; it is an exploratory, capped mechanism test.

## Hypothesis

ABI-274's early temporal line-state attention improved temporal-eligible recall/source behavior but had weak connected-line continuity. ABI-275 and ABI-282 showed that adding C4/rotation-aware continuity after the decoder tends to trade away recall or underpredict. ABI-284 tests whether moving the C4 prior earlier, into the temporal line state before the encoder pyramid, can organize temporal evidence into more continuous thin-line support while preserving ABI-274-style recall.

## Comparison Target

Primary temporal-family comparison targets:

- ABI-274 (`run_20260912_180856_79ba22`) for temporal recall/source balance.
- ABI-223 (`run_20260908_154531_8c7e2b`) for temporal-attention connected-line behavior.
- ABI-275/281/282 for recent temporal C4/detail integration attempts that did not reach the comparator band.

ABI-202 remains the whole-validation aggregate reference, but this temporal scout should be interpreted on the provider-owned temporal-eligible capped validation population.

## Implementation Sketch

Start from the ABI-274 temporal line-state attention U-Net pattern with provider-owned `abi_16ch_plus_sza_temporal` inputs, offsets `[-1, 0, 1]`, trusted `temporal_eligible_center` selection, source-balanced sampling, BCE-Dice loss, random mirroring, and trusted Line/Centerline auxiliary targets.

Replace the stem's hand-built horizontal/vertical/diagonal line-state branch with an early C4 orientation-consensus line-state module:

- project each temporal frame into ABI/SZA/BTD features;
- compute temporal attention and change features as in ABI-274;
- build a line seed from center/attended/change evidence;
- apply one shared anisotropic strip filter over 0/90/180/270-degree rotated feature maps;
- learn per-orientation attention and a consensus gate using the appearance stream;
- inject this bounded early line state into all encoder scales;
- keep the final segmentation head simple, avoiding post-decoder threshold-like residual boosting.

## Contract Features Used

The Candidate uses only provider-advertised `abi_16ch_plus_sza_temporal` tensors. The manifest requests trusted `temporal_eligible_center` frame selection, temporal offsets `[-1, 0, 1]`, source-balanced sampling, random mirroring, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, and trusted Line/Centerline auxiliary targets with weighted BCE. Candidate code does not load data, inspect temporal cache state, download frames, repair/pad temporal neighbors, select samples, implement losses/metrics/augmentation, derive targets, use Dataset Source identity, use longitude/latitude, set thresholds, postprocess predictions, apply Artifact Filters, write external artifacts, choose GPUs, or schedule resources.

## Expected Effect

The intended effect is higher filtered contrail connectivity and cleaner line continuity than ABI-274/275/281/282 while preserving more temporal recall than the post-decoder C4/detail branches. The result should reveal whether early orientation consensus organizes temporal evidence better than late C4 bridges.

## Budget

Use the exploratory/default budget: 12 epochs, batch size 2, constant learning rate, disabled early stopping, and Harness-owned execution/resource limits. Do not request `late_improving` until an exploratory result is finite, non-collapsed, near the temporal comparator band, and still improving or ambiguous near epoch 12.

## Success Criteria

A useful scout may not beat ABI-223/274 immediately, but should be finite, non-collapsed, source-informative, and show one of:

- improved filtered connectivity versus ABI-275/281/282 without a large recall collapse;
- a better recall/connectivity tradeoff than ABI-274's low-connectivity operating point;
- source-informative MIT and Google metrics without catastrophic source failure;
- a late or ambiguous trajectory that suggests the early C4 line-state mechanism is still maturing.

## Fallback Next Decision

Hard stop or deprioritize this exact branch if it underperforms ABI-275/281/282 on filtered Dice and connectivity, collapses into broad low-precision predictions, behaves like conservative underprediction, or shows numerical/resource instability. If it is finite and improves connectivity or the recall/connectivity tradeoff, consider a bounded family-development continuation or late-improving request only after observing the exploratory trajectory.
