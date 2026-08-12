# ABI-032 MCAST 1.1 focal-Tversky continuation

## Proposal classification

**Family-development continuation.** This is a controlled loss-policy follow-up to the passed `abi031_mcast11_positive_control_v1` MCAST 1.1-lineage model, not a promotion candidate.

## Hypothesis

Keeping the ABI-031 architecture, fixed MCAST 1.1 spectral transforms, input mode, sampling policy, optimizer, learning rate, batch size, and three-epoch schedule unchanged while replacing trusted `bce_dice` with trusted recall-oriented `focal_tversky` will reduce the dominant false-negative error and improve filtered recall on both Dataset Sources without returning to degenerate all-positive or all-negative predictions.

## Comparison Target

The family baseline is `run_20260811_160920_07a7f4`, whose full-validation Result was filtered Dice 0.1021, filtered precision 0.1067, filtered recall 0.0979, and filtered Contrail Connectivity Metric 0.1536. Its MIT and Google filtered Dice were 0.1105 and 0.0912. Canonical MCAST 2.1 filtered Dice 0.3873 remains the promotion reference, but this bounded continuation is judged first against the ABI-031 family baseline and its low-recall failure mode.

The current Agent Control Boundary caps each Dataset Source at 128 samples, whereas ABI-031 used 1,024 per source. Any score comparison is therefore directional rather than promotion-grade; the primary value of this Run is whether the loss changes recall and prediction non-degeneracy under the current bounded policy.

## Expected Effect

Trusted focal Tversky uses alpha 0.3 and beta 0.7, weighting false negatives more strongly than false positives. It should shift the ABI-031 model away from its low-recall operating point. A useful continuation should increase filtered recall on both MIT and Google while retaining finite optimization, a bounded predicted-positive rate, and enough precision to avoid a major filtered-Dice collapse.

## Implementation Sketch

- Reuse ABI-031's provider-approved `abi_16ch` input and derive only C11, C14, and C13-C15.
- Apply the same fixed MCAST 1.1 means and standard deviations.
- Use the same randomly initialized SMP U-Net with ResNet-18 encoder and one `mask_logits` output.
- Keep provider-owned `combined_source_balanced` sampling, no augmentation, AdamW at 0.001, batch size 4, and three epochs.
- Change exactly one manifest factor: primary loss from `bce_dice` to allowlisted `focal_tversky`.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch`; longitude and latitude remain excluded.
- Output form: one `[1, 256, 256]` `mask_logits` tensor.
- Provider-owned Leakage-Safe Split, Source-Balanced Sampling, trusted loss, metrics, checkpointing, and Artifact Filters.
- No candidate-owned data loading, loss, metric, sampling, augmentation, filtering, training loop, pretrained weights, runtime downloads, or external persistence.

## Budget Requested

One sequential Run under the generated boundary: at most 128 training and validation samples per Dataset Source, three epochs, batch size 4, and the Harness-owned 1,800-second Candidate training wall-clock budget. The architecture is source-identical to the measured 14,328,209-parameter ABI-031 model and remains below the 25,000,000-parameter smoke ceiling. No Experiment Batch or concurrency is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete with finite state and non-degenerate predictions.
2. Aggregate and source-stratified filtered recall are materially positive; neither Dataset Source collapses to an all-negative prediction.
3. The predicted-positive rate remains bounded, and filtered precision does not collapse to an all-positive regime.
4. Relative to the ABI-031 low-recall signature, the Result shows a directional recall gain without a catastrophic filtered-Dice or connectivity regression, accounting for the tighter sample cap.
5. Raw-versus-filtered metrics do not indicate excessive Artifact Filter dependence.

## Continuation and hard stop

Continue MCAST-family loss development only if focal Tversky produces a useful recall shift with finite, non-degenerate behavior. Stop this loss branch if it causes all-positive saturation, source-specific collapse, or a clear Dice/connectivity regression with no recall benefit. A mixed Result should motivate a separate, one-factor continuity-loss or augmentation proposal rather than hidden changes to this Candidate.

## Fallback Next Decision

If focal Tversky improves recall but overpredicts, propose a separate calibration or loss comparison within trusted capabilities. If it does not improve the low-recall signature, broaden to the approved `bce_dice_cldice` continuity objective or a different thermal high-resolution architecture family. Contract or Harness failures require classification and must not be treated as scientific evidence.
