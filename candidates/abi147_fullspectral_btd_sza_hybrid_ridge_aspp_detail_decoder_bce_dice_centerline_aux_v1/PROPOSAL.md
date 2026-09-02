# ABI-147 full-spectral BTD+SZA hybrid ridge-ASPP/detail decoder

## Hypothesis

ABI-130 showed that adding provider-approved Solar Geometry Input to the full-spectral BTD ASPP/detail decoder can produce a strong, high-Google-Dice and calibrated BCE-Dice operating point, while ABI-143 showed that ridge-aware SZA+BCE-Dice features can recover MIT recall and stay close to the capped reference band but lose connectivity/precision. ABI-147 tests whether a non-suppressive hybrid stem that fuses ABI-130-style context/detail features with ABI-143-style axis-aligned ridge residual evidence before the ASPP/detail decoder can preserve ABI-130's calibration while recovering some ABI-143 MIT recall.

## Proposal classification

Family-development continuation. This is a controlled continuation across the mature SZA-aware full-spectral BTD BCE-Dice frontier, not a promotion claim from capped evidence. It combines mechanisms already resource-observed in ABI-130/ABI-143-like candidates, but the exact hybrid architecture should still run sequentially under the active Agent Control Boundary cap.

## Comparison Target

Primary comparison target: ABI-130 (`run_20260831_121006_7d24be`), the strongest SZA-aware ASPP/detail BCE-Dice branch.

Secondary references:

- ABI-143 (`run_20260831_224534_27b73d`) for ridge-aware SZA+BCE-Dice MIT-recall behavior.
- ABI-068 (`run_20260828_010836_4ccc77`) as the current capped aggregate filtered-Dice reference.
- ABI-126 (`run_20260831_085615_d05ab3`) as the non-SZA ASPP/detail BCE-Dice precision/connectivity comparator.
- ABI-146 (`run_20260901_012037_c302cc`) as negative evidence against adding a late frequency-support path to ABI-130.

## Expected Effect

The hybrid stem should increase line/detail evidence at the encoder input without applying candidate-owned thresholding, postprocessing, Artifact Filters, or sampling changes. Expected useful behavior is a modest increase in MIT filtered Dice/recall relative to ABI-130, smaller Google-Dice loss than ABI-143, and no collapse in filtered predicted-positive fraction. Because ABI-146 made a late frequency-support path too conservative, ABI-147 places ridge evidence at the stem and fuses it non-suppressively rather than gating logits or shrinking final features.

## Implementation Sketch

- Use provider-approved `abi_16ch_plus_sza` input only: ABI channels 1-16 plus Solar Geometry Input; longitude/latitude channels remain excluded.
- Build normalized raw ABI planes, thermal BTD planes from approved ABI channels, normalized SZA, cosine SZA, and a learned 1x1 mixture.
- Replace the plain ASPP/detail stem with `HybridRidgeDetailStem`, concatenating raw projection, local detail residual, broad smoothed context, horizontal ridge residual, and vertical ridge residual.
- Keep the compact encoder, ASPP bottleneck, decoder skip fusion, high-resolution detail branch, line-aware refinement, mask head, and provider-derived `centerline_logits` auxiliary output.
- Use trusted `bce_dice` primary loss and trusted Centerline Target weighted BCE auxiliary loss at weight 0.02.

## Contract Features Used

Candidate code defines architecture only. It does not implement or modify data loading, Leakage-Safe Split construction, capped-record selection, sampling traversal, augmentation transforms, target derivation, loss functions, metrics, thresholding, Artifact Filters, Baseline Segmenters, prediction retention, training loops, resource placement, retry policy, or Run lifecycle. All BTD and ridge/context features are computed only from provider-approved ABI/SZA tensors. No longitude, latitude, raw dataset path, external file access, network access, pretrained weight download, or custom persistence is used.

## Budget Requested

Use the active trusted Workspace Configuration ceilings: 1,024 provider-selected records per Dataset Source and Leakage-Safe Split, 12 epochs, batch size 4, constant learning rate, disabled early stopping, four fixed `first_n` retained predictions, 25M parameter smoke ceiling, A100 execution, and sequential Run execution under the Agent-visible concurrency cap of one.

## Success Criteria

ABI-147 is useful if it remains finite and non-collapsed and achieves at least one of:

- improves ABI-130 MIT filtered Dice or MIT filtered recall without losing more than about 0.01 aggregate filtered Dice;
- matches or exceeds ABI-143 aggregate filtered Dice while improving its filtered connectivity or Google filtered Dice;
- lands within about 0.01 of ABI-068 aggregate filtered Dice with a clearer source-balanced or connectivity tradeoff.

Hard stop conditions for this exact branch are non-finite training, contract/resource failure, persistent all-negative/all-positive predictions, aggregate filtered Dice well below ABI-130/ABI-143 with no source or connectivity advantage, or a strongly conservative recall/connectivity regression like ABI-146.

## Fallback decision

If ABI-147 underperforms without a useful source/connectivity tradeoff, stop this hybrid ridge-ASPP stem branch and broaden away from SZA-aware BCE-Dice micro-architecture changes. Reasonable next frontiers would be a distinct preprocessing/front-end scout, a calibration/evaluation request for ABI-130-style candidates, or a new architecture family focused on thin-line continuity without late suppressive gates.
