# ABI-037 MCAST 1.1 BCE-Dice-clDice continuation

## Proposal classification

**Family-development continuation.** This is a controlled continuity-loss follow-up within the MCAST 1.1-lineage family, not a promotion candidate.

## Hypothesis

Keeping the ABI-032 architecture, fixed MCAST 1.1 spectral transforms, input mode, sampling policy, optimizer, learning rate, batch size, and three-epoch schedule unchanged while replacing trusted `focal_tversky` with trusted `bce_dice_cldice` will improve thin-structure continuity and precision-recall balance. The BCE and Dice terms should restrain the focal-Tversky overprediction signature, while clDice should preserve connected Contrail Mask structures rather than returning to the low-recall ABI-031 operating point.

## Comparison Target

The primary controlled comparison is `run_20260812_121722_8d6cd3` (ABI-032), which used the same 128-samples-per-Dataset-Source boundary and reached filtered Dice 0.0462, precision 0.0251, recall 0.2925, and Contrail Connectivity 0.0664. Its source-stratified filtered Dice was 0.0903 on MIT and 0.0213 on Google.

`run_20260811_160920_07a7f4` (ABI-031, trusted `bce_dice`) remains the family Result at filtered Dice 0.1028 and connectivity 0.1573, but it used 1,024 samples per Dataset Source and is not directly comparable to the current bounded Run. Canonical MCAST 2.1 filtered Dice 0.3873 remains the promotion reference.

## Expected Effect

Relative to ABI-032, the continuity objective should increase filtered Contrail Connectivity and filtered Dice by reducing diffuse false positives while retaining materially positive recall on both MIT and Google. The desired signature is an intermediate precision-recall point between ABI-031 and ABI-032, not an all-negative or all-positive collapse.

## Implementation Sketch

- Reuse the provider-approved `abi_16ch` input and derive only C11, C14, and C13-C15.
- Apply the same fixed MCAST 1.1 means and standard deviations.
- Use the same randomly initialized SMP U-Net with ResNet-18 encoder and one `mask_logits` output.
- Keep provider-owned `combined_source_balanced` sampling, no augmentation, AdamW at 0.001, batch size 4, and three epochs.
- Change exactly one manifest factor from ABI-032: primary loss from `focal_tversky` to allowlisted `bce_dice_cldice`.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude and latitude remain excluded.
- Output form: one `[1, 256, 256]` `mask_logits` tensor.
- Provider-owned Leakage-Safe Split, Source-Balanced Sampling, trusted loss, metrics, checkpointing, and Artifact Filters.
- No candidate-owned data loading, loss, metric, sampling, augmentation, filtering, training loop, pretrained weights, runtime downloads, or external persistence.

## Budget Requested

One sequential Run under the active bounded authorization: at most 128 training and validation samples per Dataset Source, three epochs, batch size 4, two Harness-selected prediction samples, and the Harness-owned 1,800-second Candidate training wall-clock budget. The architecture is source-equivalent to the measured 14,328,209-parameter ABI-031/ABI-032 model and remains below the 25,000,000-parameter smoke ceiling. No Experiment Batch or concurrency is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete with finite state and non-degenerate predictions.
2. Aggregate and source-stratified filtered recall remain materially positive; neither Dataset Source collapses to all-negative predictions.
3. Filtered precision improves directionally over ABI-032 without sacrificing the majority of ABI-032's aggregate filtered recall.
4. Filtered Dice and Contrail Connectivity improve directionally over ABI-032 under the same bounded sample and epoch policy.
5. Raw-versus-filtered metrics do not indicate excessive Artifact Filter dependence.

## Continuation and hard stop

Continue continuity-loss development only if the Run is finite, non-degenerate, and improves at least one of filtered Dice or Contrail Connectivity without source-specific collapse. Stop this exact loss branch if it produces non-finite training, all-negative saturation, all-positive saturation, or a clear Dice/connectivity regression with no precision-recall benefit. A mixed Result should motivate a separate one-factor augmentation or input-policy proposal rather than hidden changes to this Candidate.

## Fallback Next Decision

If `bce_dice_cldice` improves connectivity but recall falls too far, propose a separate trusted augmentation or input-front-end continuation. If it fails to improve either Dice or connectivity, broaden to random mirroring, thermal-only input, learned channel mixing, or a different high-resolution architecture family. Contract or Harness failures require classification and must not be treated as scientific evidence.
