# ABI Spectral Residual U-Net Scout v1

## Proposal classification

**Family scout.** This is the first scientific candidate in the spectral residual encoder-decoder family. It is not required to beat a mature Baseline Segmenter on its first bounded Run.

## Hypothesis

A compact residual U-Net that combines normalized Full ABI Channel Input, explicit thermal brightness-temperature differences, and learned 1x1 channel mixtures can avoid the manual canary's all-negative collapse while preserving thin contrail structure. Provider-owned Source-Balanced Sampling, random mirroring, and `bce_dice_cldice` should improve cross-source learning and continuity without moving data, loss, augmentation, metric, or Artifact Filter authority into candidate code.

## Comparison Target

The promotion reference is canonical MCAST 2.1 at aggregate filtered Dice 0.3873 on registry `abi-mcast-working-validation-v1`, with MCAST 1.1 as a connectivity-oriented comparator. The immediate family-scout reference is the ABI-025 lifecycle canary, whose near-zero Dice resulted from all-negative predictions and was not a scientific baseline. Decisions will inspect raw and filtered Dice, recall, Contrail Connectivity Metric, source-stratified MIT and Google metrics, threshold behavior, and learning curves.

## Expected Effect

The spectral front end should expose cirrus, ice-phase, window, and water-vapor evidence at compatible numeric scales while retaining learned channel combinations. Residual skip paths and only three downsampling stages should preserve narrow linear structures; dilated bottleneck context should distinguish coherent contrails from local cloud edges. The connectivity-aware trusted loss should discourage fragmented masks.

## Implementation Sketch

- Accept only provider-approved `abi_16ch` tensors; longitude and latitude are never inputs.
- Normalize the 16 approved channels using rounded source-balanced summary values from the trusted campaign context.
- Concatenate selected normalized ABI bands, five explicit thermal differences, and 16 learned 1x1 mixtures.
- Use a compact 32/64/128-channel residual encoder, a 192-channel multi-dilation bottleneck, symmetric skip-connected decoder, and one `mask_logits` head.
- Select provider-owned `combined_source_balanced` sampling, `random_mirroring`, and `bce_dice_cldice` through the manifest.
- Use Harness-owned AdamW at learning rate 0.0003, batch size 4, for at most 12 epochs.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0
- Input mode: `abi_16ch`; output form: `mask_logits`
- Provider-owned Leakage-Safe Split and equal default MIT/Google source mixture
- Provider-owned `random_mirroring` augmentation
- Trusted `bce_dice_cldice` loss and `val/filtered_dice` checkpoint selection
- Provider/Harness-owned metrics, Artifact Filters, Baseline Segmenters, optimizer loop, and sampling implementation
- No custom loaders, losses, metrics, filters, target transforms, geographic inputs, pretrained weights, runtime downloads, or network access

## Budget Requested

Run one bounded scout with at most 1,024 training ABI Patches per Dataset Source, the available bounded validation subset, 12 epochs, batch size 4, and normal Harness resource limits. If the scout is non-degenerate, allow at most two later family-development Runs: one controlled spectral/loss ablation and one capacity or training-policy refinement. Full Working Validation Split Post-Run Evaluation is warranted only after a completed scout with useful validation behavior.

## Success Criteria

1. Static validation, controlled smoke testing, and bounded training complete without resource or contract failure.
2. Predictions are non-degenerate: both positive and negative pixels occur on validation data, with materially positive filtered recall and Dice.
3. MIT and Google source-stratified filtered Dice are each at least 0.15, or the aggregate filtered Dice reaches 0.20 with a clearly improving learning curve.
4. Raw-versus-filtered behavior does not indicate excessive dependence on Artifact Filters.
5. Connectivity or thin-structure diagnostics provide a useful basis for the bounded family-development decision, even if the scout does not beat MCAST 2.1.

## Continuation and Hard Stop

Continue within the family when the Run is non-degenerate and meets criterion 3, shows a strong connectivity/source-specific advantage, or remains clearly learning-limited at epoch 12. Use the two-Run follow-up budget for one-factor changes only. Stop this family after the scout if it repeats all-negative collapse, has aggregate filtered Dice below 0.05 without an improving curve, or fails catastrophically on either Dataset Source for an architectural reason. Contract, Harness, or resource failures require classification rather than scientific abandonment.

## Fallback Next Decision

If the scout trains but lacks useful signal, broaden to a different family such as a thermal-only high-resolution line model or an auxiliary centerline/boundary model. If a required capability is unavailable, issue a Capability Request rather than implementing a candidate-owned workaround.
