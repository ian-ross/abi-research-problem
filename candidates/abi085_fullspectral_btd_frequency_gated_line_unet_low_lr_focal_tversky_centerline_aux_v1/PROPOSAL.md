# ABI-085: frequency-gated line U-Net low-learning-rate focal-Tversky continuation

## Hypothesis

ABI-068 is the strongest capped representative full-spectral BTD frequency-gated line U-Net result so far, but its epoch trajectory was non-monotonic and it traded away some ABI-066 precision/connectivity for recall. A lower trusted AdamW learning rate of 0.0001, with the same architecture, input, sampling, augmentation, focal-Tversky primary loss, and Centerline Target auxiliary weight, may stabilize the focal-Tversky branch enough to recover precision/connectivity or Google-source behavior while retaining useful recall.

This is a **family-development continuation** on the trusted training-policy axis, not a promotion claim from capped evidence.

## Comparison Target

Primary comparison target: ABI-068 (`run_20260828_010836_4ccc77`), the same frequency-gated full-spectral BTD architecture at learning rate 0.0003 with trusted focal-Tversky and centerline auxiliary weight 0.02.

Secondary references: ABI-066 (`run_20260827_230540_bf4ce3`) as the precision/connectivity-forward frequency-gated reference, ABI-078 (`run_20260828_094949_ad2af0`) as the BCE-Dice loss-swap reference, and canonical MCAST 2.1 only as full Working Validation Split promotion context.

## Expected Effect

Lowering the learning rate should reduce late-epoch oscillation and the recall-heavy positive-area drift observed in several focal-Tversky branches. Useful outcomes include any of: aggregate filtered Dice close to or above ABI-068, improved filtered precision/connectivity over ABI-068 without catastrophic recall loss, improved Google filtered Dice, or a smoother finite trajectory indicating that the ABI-068 branch remains tunable under Harness-owned training policy.

## Implementation Sketch

Copy the ABI-068 candidate architecture unchanged: provider-approved `abi_16ch` input; normalized raw channels; explicit ABI-channel-derived thermal BTD planes; learned 1x1 channel mixer; frequency-split stem; residual encoder/decoder; dilated bottleneck context; frequency-pyramid fusion; oriented line refiner; primary `mask_logits`; and trusted provider-derived `centerline_logits` auxiliary output. Change only `training.learning_rate` from 0.0003 to 0.0001 in the manifest.

## Contract Features Used

- Input mode: `abi_16ch` only; no longitude or latitude inputs.
- Output form: `mask_logits` plus provider-declared `centerline_logits` auxiliary output.
- Data policy: provider/Harness-owned `combined_source_balanced` sampling, `all_target_frames`, and `random_mirroring` augmentation.
- Loss policy: trusted `focal_tversky` primary loss and trusted `weighted_bce` centerline auxiliary loss at weight 0.02.
- Optimizer/training: Harness-owned AdamW, constant learning rate, batch size 4, max epochs 12, disabled early stopping per active configuration.
- Candidate code owns only model architecture over approved tensors; it does not implement data loading, sampling, augmentation, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, or pretrained weights.

## Budget Requested

Use the active Workspace Configuration ceilings: 1,024 provider-selected records per Dataset Source and split, 12 epochs, batch size 4, constant learning rate, disabled early stopping, one A100 run slot, Docker training wall-clock budget 3,600 seconds, at most four fixed `first_n` prediction artifacts, and the 25,000,000-parameter smoke ceiling. The model is the ABI-068 architecture previously measured at about 12.09M parameters and should remain within the profiled resource envelope.

## Success Criteria

Treat this as capped family-development evidence. Useful continuation evidence is any of:

- best validation aggregate filtered Dice at least approximately tied with ABI-068 (within about 0.01) or improved over it;
- filtered precision or Contrail Connectivity Metric improved over ABI-068 while aggregate filtered Dice remains near the ABI-066/078 band;
- Google filtered Dice improves over ABI-068 without a MIT catastrophic source drop;
- finite, non-degenerate predictions with both MIT and Google filtered Dice above about 0.33 and a smoother trajectory than ABI-068.

Do not promote from capped evidence alone. A promotion interpretation would require separate whole-validation diagnostics and human review.

## Fallback/Next Decision

If ABI-085 is non-finite, collapses, or clearly underperforms ABI-068/066 without diagnostic benefit, do not repeat this exact low-learning-rate branch. If it improves precision/connectivity or source balance, request or run bounded follow-up diagnostics on the same stable Run identity before considering further frequency-gated training-policy development. If it is merely tied, prefer broadening to another trusted training/data-policy axis or a materially different thin-line architecture rather than adding more output-side refinement modules.
