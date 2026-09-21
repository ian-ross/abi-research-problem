# ABI-306 temporal C4 dual-evidence recall-calibrated line-state late36 U-Net

## Classification

Family-development continuation. ABI-306 is a mechanism-changing continuation of the ABI-285 temporal C4 orientation line-state branch, not an unchanged rerun. It keeps the provider-owned three-frame temporal input and early C4 line-state backbone, then changes the final architecture head to learn a bounded mask-logit residual gated by agreement among the base mask, Line auxiliary, and Centerline auxiliary evidence.

## Hypothesis

ABI-285 reached the strongest capped temporal-eligible aggregate filtered Dice in the current temporal branch, but its selected epoch-32 recall/source-balance gains came with weak connected-line continuity. Earlier epochs showed compact high-precision/high-connectivity states with inadequate recall. The hypothesis is that a learned dual-evidence logit calibration head can recover part of ABI-285's epoch-32 fixed-threshold recall while using internal line/centerline evidence to avoid another broad low-connectivity footprint.

The mechanism is architecture-internal only: the model emits logits, and the Harness still owns the fixed threshold, losses, metrics, Artifact Filters, prediction retention, and validation.

## Comparison Target

Primary comparison target: ABI-285 (`run_20260913_100333_a250df`), the temporal C4 line-state parent and capped temporal-eligible aggregate comparator.

Secondary context:

- ABI-223 (`run_20260908_154531_8c7e2b`) and ABI-238 (`run_20260911_004137_f54c45`) as temporal-attention precision/connectivity comparators.
- ABI-296/299 and ABI-305 as recent temporal local-correlation/calibration context showing the precision-recall-connectivity trade-off.

## Expected Effect

Expected useful evidence would be one of:

- filtered Dice near ABI-285 while improving filtered connectivity and precision;
- filtered recall near ABI-285 while reducing the filtered predicted-positive footprint or clutter;
- a clearly different source-balanced trajectory that couples recall to line/centerline evidence rather than sliding along the existing compact-versus-recall trade-off.

A successful result need not beat ABI-202 whole-validation reference because this is temporal-eligible capped family development, not full-data promotion evidence.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal`.
- `data.frame_selection_policy: temporal_eligible_center`.
- `data.temporal_frame_offsets: [-1, 0, 1]`.
- Trusted `combined_source_balanced` sampling.
- Trusted `random_mirroring` augmentation.
- Trusted `bce_dice` primary loss.
- Trusted Line and Centerline auxiliary targets with weighted BCE auxiliary losses.
- AdamW, constant learning rate, batch size 2, and Harness-owned resource/lifecycle limits.

Candidate code defines only model architecture. It does not own data loading, temporal lookup, temporal cache access, frame repair/padding, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, longitude/latitude, Dataset Source identity, downloads, resource scheduling, training loops, or prediction retention.

## Implementation Sketch

Start from the resource-profiled ABI-285 temporal C4 orientation line-state U-Net:

- keep normalized ABI+SZA+BTD per-frame features, temporal attention/change fusion, early C4 orientation-consensus line state, line-state injection, ASPP bottleneck, and high-resolution directional context;
- replace the simple final segmentation head with `DualEvidenceRecallCalibratedHead`:
  - shared decoder features produce base mask logits, residual recall logits, Line logits, and Centerline logits;
  - a learned gate consumes shared features plus sigmoid(base mask), sigmoid(Line), and sigmoid(Centerline) evidence;
  - final mask logits are `base_mask + bounded gated residual`, with no thresholding, morphology, postprocessing, or Artifact Filter logic in Candidate code.

## Budget Requested

Request the approved `late_improving` budget for 36 epochs because ABI-285, the direct parent branch, required the late budget to move from ABI-284's exploratory filtered Dice 0.3901 to ABI-285's epoch-32 filtered Dice 0.4222, and the selected checkpoint occurred well after epoch 12. ABI-306 is close enough in architecture and resource profile to need the same maturity test, but it changes the head mechanism to address ABI-285's documented connectivity weakness. If the Harness denies the request, run under the exploratory budget and treat that result as valid bounded evidence.

## Success Criteria

ABI-306 is successful enough for continued consideration if it is finite, resource-safe, non-collapsed, source-informative, and improves the ABI-285 trade-off on at least one central axis: higher filtered Dice, higher connectivity at comparable recall, higher precision at comparable recall, better MIT/Google balance, or a late-improving trajectory that supports a more focused follow-up.

## Fallback Next Decision

Stop this exact head if it repeats ABI-305-like compact precision without recall, ABI-296/299-like broad local-correlation clutter, or an oscillatory trajectory that does not improve ABI-285's recall/connectivity balance. If the Candidate fails contract or smoke validation due to a candidate-owned bug, repair the minimal defect while preserving this hypothesis; if it fails due to an unavailable trusted capability, create a Capability Request rather than working around the boundary.
