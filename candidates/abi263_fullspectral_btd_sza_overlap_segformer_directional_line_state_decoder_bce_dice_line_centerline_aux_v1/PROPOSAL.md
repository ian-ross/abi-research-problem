# ABI-263 overlap SegFormer directional line-state decoder continuation

## Hypothesis

ABI-262 showed that compact overlap-attention can improve recall and MIT filtered Dice over the ABI-260 MaxViT scout, but its selected checkpoint lost too much Contrail Connectivity. A SegFormer-family continuation that preserves a high-resolution directional line state from the signed-detail/stem features through both 128px and 256px decoder fusion should recover connected thin-line structure while keeping ABI-262's resource-efficient overlap-attention and recall behavior.

## Classification

Family-development continuation: this is a bounded continuation of the ABI-262 compact SegFormer/MiT-style modern-backbone family, not a promotion candidate. The hypothesis changes the decoder/connectivity mechanism rather than merely adding epochs to ABI-262.

## Comparison Target

- ABI-262 overlap SegFormer line decoder (`run_20260912_040526_92961f`) as the direct parent and one-factor family baseline.
- ABI-253 compact line-memory U-NetFormer late36 (`run_20260911_171333_f0b603`) as the stronger recent modern-backbone comparator.
- ABI-249 C4 steerable line-context late36 (`run_20260911_111909_dd7ef7`) as the high-precision/rotation-aware comparator.
- ABI-202 (`run_20260904_043143_ee0005`) as the aggregate whole-validation frontier reference.

## Expected Effect

The expected effect is to keep ABI-262's finite, compact, source-informative overlap-attention behavior while increasing filtered contrail connectivity and precision at similar predicted-positive fraction. A useful continuation would close part of ABI-262's roughly 0.09 connectivity gap to ABI-253 and improve aggregate filtered Dice versus ABI-262 without sacrificing its MIT/recall gains. It is acceptable if the candidate remains below ABI-202; the main decision is whether the SegFormer family can preserve line continuity after a mechanism change.

## Implementation Sketch

Start from the ABI-262 normalized ABI+SZA and ABI-channel BTD front end and four-stage overlap-patch SegFormer encoder. Replace the plain line decoder with a directional line-state decoder: build a 256x256 oriented state from the signed-detail and stem features, carry a downsampled line state into 128px multi-scale fusion through a learned gate/update, then re-inject the 256px line state after full-resolution detail fusion. Revise the logit head to combine recall, line, and centerline paths through an agreement gate so lower-confidence recall evidence is raised mainly where the line/centerline path supports it. Emit `mask_logits`, `line_logits`, and `centerline_logits` for trusted Harness losses.

## Contract Features Used

- Provider-owned `abi_16ch_plus_sza` input mode only; no longitude or latitude inputs.
- Candidate-derived normalized ABI channels, ABI-channel BTD planes, Solar Geometry Input scalars, and learned 1x1 channel mixtures inside architecture code.
- Trusted `combined_source_balanced` sampling and `random_mirroring` augmentation selected in the manifest.
- Trusted `bce_dice` primary loss, AdamW optimizer, constant learning rate, batch size 4, and exploratory 12-epoch budget.
- Trusted Line and Centerline auxiliary targets via `line_logits` and `centerline_logits` with `weighted_bce` auxiliary losses.

## Budget Requested

Use the default exploratory budget: 1,024 provider-selected samples per Dataset Source/split, 12 epochs, batch size 4, constant learning rate, disabled early stopping, and sequential execution under the active Harness policy. No late-improving budget is requested because the mechanism should first prove it improves ABI-262 connectivity under the exploratory budget.

## Success Criteria

ABI-263 is positive if it completes finite and non-collapsed, remains under the 25M-parameter ceiling and exploratory timeout, improves ABI-262 filtered connectivity materially without a large precision or source-Dice regression, and preferably improves aggregate filtered Dice over ABI-262. It remains useful if it matches ABI-262 Dice while showing cleaner connectivity/precision tradeoffs. A final-epoch best or clearly rising trajectory near or above ABI-262 would justify considering a late-improving or further one-factor continuation.

## Fallback/Next Decision

If ABI-263 improves ABI-262 connectivity and aggregate/source Dice, keep the SegFormer family eligible for one bounded continuation or diagnostic request depending on score. If it improves connectivity but loses too much recall/Dice, consider one architecture-level calibration/decoder adjustment rather than an unchanged repeat. If it is finite but remains below ABI-262 or has the same weak connectivity, stop this exact SegFormer decoder branch and broaden to temporal change/calibration, rotation-aware line accumulation, or another modern-backbone family. If it fails contract, shape, resource, or numerical checks, classify the failure before deciding whether a repair Candidate is warranted.

## Safety and Candidate Boundary

Candidate code defines only model architecture and manifest choices. It does not implement data loading, split logic, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, temporal lookup, downloads, coordinates, Dataset Source identity, resource scheduling, or training loops.
