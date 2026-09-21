# ABI-345 temporal-attention center-detail evidence sharpening late36

## Classification

Family-development continuation in the temporal-attention architecture family.

## Hypothesis

ABI-223 remains the strongest temporal-attention connectivity comparator: it is compact and precise on the temporal-eligible validation population, but its fixed-threshold recall trails newer temporal C4 recall diagnostics. Recent ABI-341/344 sidecar experiments showed that broad residual recall paths can reduce positive-tail misses but also create negative-patch clutter and weak connectivity. ABI-345 tests a narrower alternative: preserve the ABI-223 three-frame temporal-attention backbone and add a bounded center-detail evidence-sharpening head that can adjust uncertain mask logits only when refined decoder features agree with high-resolution center/detail and temporal-stem evidence.

Expected effect: improve fixed-threshold recall and MIT/source-balanced filtered Dice over ABI-223 without the broad-footprint connectivity loss seen in ABI-341/344.

## Comparison Target

- ABI-223 (`run_20260908_154531_8c7e2b`): temporal-attention connectivity comparator on temporal-eligible validation.
- ABI-238 (`run_20260911_004137_f54c45`): stronger directional temporal-attention capped comparator.
- ABI-324 (`run_20260916_184108_954ec7`): balanced five-frame temporal C4/detail-consensus comparator.
- ABI-325 (`run_20260916_212722_d66d93`): positive-tail broad-footprint recall diagnostic.
- ABI-341/ABI-344: cautionary evidence for residual recall heads that improve positive-tail counts at excessive clutter/connectivity cost.

## Implementation sketch

Start from the ABI-223 compact temporal-attention fusion U-Net over provider-owned offsets `[-1, 0, 1]`. Keep the same finite ABI+SZA+BTD feature builder, shared frame projection, per-pixel temporal attention, center/change fusion, U-Net encoder/ASPP/decoder, and trusted Line/Centerline auxiliary outputs.

Replace the direct heads with `CenterDetailEvidenceSharpeningHead`:

1. Produce an anchor mask logit from refined decoder features.
2. Build a high-resolution evidence tensor from refined decoder, decoder skip, encoder scale-0, and temporal-stem features.
3. Predict Line and Centerline auxiliary logits from that evidence tensor.
4. Add a small bounded signed support residual to the anchor only through an agreement gate and an anchor-uncertainty factor.

The residual is differentiable model logic and stays inside `mask_logits`; it is not thresholding, postprocessing, calibration outside the model, morphology, an Artifact Filter, target derivation, or metric logic.

## Contract Features Used

- Input mode: `abi_16ch_plus_sza_temporal`.
- Trusted frame selection: `temporal_eligible_center`.
- Temporal offsets: `[-1, 0, 1]`.
- No longitude/latitude inputs.
- Trusted sampling policy: `combined_source_balanced`.
- Trusted augmentation policy: `random_mirroring`.
- Trusted loss: `bce_dice` with trusted Line and Centerline `weighted_bce` auxiliaries.
- Optimizer/scheduler: AdamW with constant LR.
- Candidate source defines architecture only. It does not implement data loading, temporal lookup, sample selection, augmentation, losses, metrics, Artifact Filters, thresholds, postprocessing, training loops, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Budget Requested

Request the approved `late_improving` budget for 36 epochs using ABI-223 as parent evidence. ABI-223 selected its final late-budget epoch as best checkpoint and remains compact/connectivity-strong but recall-limited. ABI-345 is a close continuation that changes only the architecture-internal head while preserving the trusted data/loss/resource profile. If the request is denied, run under the exploratory budget and treat that bounded result as valid feasibility evidence.

## Success criteria

This Candidate does not need to beat the whole-validation ABI-202 reference to be useful. It is successful enough for further temporal-attention development if it completes finitely and shows most of the following capped temporal-eligible signals:

- filtered Dice at or above ABI-223/238 temporal-attention comparators, or a clear source-balanced improvement over ABI-223;
- filtered recall meaningfully above ABI-223 while keeping precision close to ABI-223 rather than shifting into ABI-325/341/344 broad-footprint behavior;
- filtered connectivity close to ABI-223 and above ABI-341/344;
- MIT filtered Dice or positive-tail behavior improved without catastrophic Google regression;
- filtered predicted-positive footprint and negative-patch clutter consistent with compact evidence rather than broad residual recall.

Hard-stop evidence for this exact branch would be non-finite behavior, smoke/contract failure, persistent prediction collapse, or a finite result that repeats ABI-341/344-style broad clutter with lower aggregate/source Dice and low connectivity.

## Fallback decision

If ABI-345 is finite but below ABI-223/238 with no recall/connectivity/source advantage, do not submit an unchanged late36 continuation. Broaden away from this head, either toward a materially different temporal alignment/evidence-sharpening mechanism or a non-temporal C4/orientation-recall mechanism. If it improves recall while preserving compact connectivity but remains short of ABI-324, request a bounded temporal-eligible failure-bucket diagnostic before another continuation.
