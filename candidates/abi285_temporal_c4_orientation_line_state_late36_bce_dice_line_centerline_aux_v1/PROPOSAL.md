# Proposal: ABI-285 temporal C4 orientation line-state late36 U-Net

## Classification

Family-development continuation in the provider-owned temporal ABI input family. This is a close late-improving continuation of ABI-284, not a promotion claim.

## Hypothesis

ABI-284 moved the C4/orientation prior into the early temporal line state and produced a finite, source-informative exploratory Run whose selected checkpoint was the final epoch. It improved the recent temporal C4/detail exploratory branches on filtered Dice, precision, and compactness, and it entered high-connectivity/high-precision regimes at some epochs. The open question is whether the approved late-improving budget can stabilize those regimes while recovering more temporal recall.

ABI-285 tests the same resource-profiled architecture for longer training. The hypothesis is that the early C4 orientation-consensus line-state mechanism is still maturing at 12 epochs and may converge toward a better recall/connectivity compromise by 36 epochs.

## Comparison Target

Primary temporal-family comparison targets:

- ABI-284 (`run_20260913_091156_167372`) as the exploratory parent.
- ABI-274 (`run_20260912_180856_79ba22`) for temporal line-state recall/source balance.
- ABI-223 (`run_20260908_154531_8c7e2b`) for temporal-attention connected-line behavior.
- ABI-275/281/282 for recent temporal C4/detail exploratory branches that ABI-284 improved but did not decisively solve.

ABI-202 remains the whole-validation aggregate reference, but this temporal late-improving continuation should be interpreted first on the provider-owned temporal-eligible capped validation population.

## Implementation Sketch

Keep the ABI-284 model architecture unchanged:

- consume provider-owned `abi_16ch_plus_sza_temporal` input with offsets `[-1, 0, 1]`;
- use trusted `temporal_eligible_center` frame selection;
- build per-frame normalized ABI, BTD, and Solar Geometry Input features;
- compute temporal attention and center/change features;
- build an early line seed from center, attended, and change evidence;
- apply a C4 orientation-consensus line-state module sharing one anisotropic strip filter across 0/90/180/270-degree rotations;
- inject the bounded line state into encoder scales and use simple mask/line/centerline heads.

The only experimental change from ABI-284 is the candidate-local `budget_request.yaml` requesting the approved `late_improving` budget.

## Contract Features Used

The Candidate uses only provider-advertised `abi_16ch_plus_sza_temporal` tensors. The manifest requests trusted `temporal_eligible_center` frame selection, temporal offsets `[-1, 0, 1]`, source-balanced sampling, random mirroring, BCE-Dice primary loss, AdamW, constant learning rate, batch size 2, and trusted Line/Centerline auxiliary targets with weighted BCE. Candidate code does not load data, inspect temporal cache state, download frames, repair/pad temporal neighbors, select samples, implement losses/metrics/augmentation, derive targets, use Dataset Source identity, use longitude/latitude, set thresholds, postprocess predictions, apply Artifact Filters, write external artifacts, choose GPUs, or schedule resources.

## Expected Effect

The intended effect is to determine whether ABI-284's early C4 line-state mechanism can improve after the exploratory ceiling. A useful result would raise filtered Dice, recall, and/or connectivity versus ABI-284 while preserving its compact prediction footprint and precision. The continuation should clarify whether the observed high-connectivity states are trainable into a stable selected checkpoint or are only transient conservative underprediction modes.

## Budget

Request the approved `late_improving` budget: up to 36 epochs and the Harness-owned late timeout. If denied, fall back to the exploratory budget as declared in `budget_request.yaml` and treat that bounded result as valid.

## Success Criteria

A useful late continuation should be finite, non-collapsed, source-informative, and show one or more of:

- improvement over ABI-284 filtered Dice without broadening negative-patch clutter;
- improved filtered recall while keeping precision near ABI-284;
- improved filtered connectivity approaching ABI-223/274 without severe recall collapse;
- a stable selected checkpoint rather than oscillation between conservative high-connectivity and broader high-recall states.

## Fallback Next Decision

Do not promote or repeat the branch unchanged if the longer budget remains below ABI-274/223 while preserving ABI-284's recall/connectivity weakness, collapses into conservative underprediction, broadens false positives, or shows resource/numerical instability. If it improves the temporal-eligible tradeoff materially, consider a bounded temporal-eligible diagnostic request rather than making whole-validation claims from capped evidence.
