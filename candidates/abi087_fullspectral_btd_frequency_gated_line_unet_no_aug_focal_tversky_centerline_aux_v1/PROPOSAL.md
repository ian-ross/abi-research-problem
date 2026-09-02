# Experiment Proposal: ABI-087 frequency-gated line U-Net no-augmentation focal-Tversky continuation

## Hypothesis

ABI-068 remains the strongest capped representative full-spectral BTD frequency-gated line U-Net reference, while several architecture-side refiners and scouts have reduced Dice, precision, connectivity, or source balance. The trusted `random_mirroring` augmentation may be adding variance for a geostationary ABI task where scan direction, cloud texture, illumination, and source-specific acquisition artifacts have physically meaningful orientation. Disabling augmentation while holding the ABI-068 architecture, loss, sampling, learning rate, auxiliary supervision, and resource profile fixed may improve precision/connectivity or source balance by training on the native orientation distribution only.

This is a **family-development continuation** on a trusted data-policy axis, not a promotion claim from capped evidence.

## Comparison Target

Primary comparison target: ABI-068 (`run_20260828_010836_4ccc77`), the same frequency-gated full-spectral BTD architecture using trusted `random_mirroring`, focal-Tversky, and Centerline Target auxiliary weight 0.02.

Secondary references: ABI-066 (`run_20260827_230540_bf4ce3`) as the precision/connectivity-forward frequency-gated reference; ABI-081 (`run_20260829_143707_7c7d44`) showing auxiliary removal did not improve ABI-068; ABI-085 (`run_20260829_181201_01c5e7`) showing lower learning rate did not improve ABI-068; and canonical MCAST 2.1 only as full Working Validation Split promotion context.

## Expected Effect

Removing mirroring should reduce augmentation-induced orientation mismatch and may sharpen the learned native-orientation operating point. Useful evidence would be aggregate filtered Dice close to or above ABI-068, improved filtered precision or Contrail Connectivity Metric without catastrophic recall loss, improved Google or MIT source balance, or a cleaner predicted-positive fraction near ABI-066/068. A negative outcome would still be informative because it would test whether trusted random mirroring is helping or hurting the current strongest local architecture under the representative cap.

## Implementation Sketch

Copy the ABI-068 candidate architecture unchanged: provider-approved `abi_16ch` input; normalized raw ABI channels; explicit ABI-channel-derived thermal BTD planes; learned 1x1 channel mixer; frequency-split stem; residual encoder/decoder; dilated bottleneck context; frequency-pyramid fusion; oriented line refiner; primary `mask_logits`; and provider-derived `centerline_logits` auxiliary output. Change only the manifest `data.augmentation_policy` from `random_mirroring` to trusted `none`.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`
- Input mode: `abi_16ch` only; no longitude or latitude inputs
- Output form: `mask_logits` plus provider-declared `centerline_logits` auxiliary output
- Data policy: provider/Harness-owned `combined_source_balanced` sampling, `all_target_frames`, and trusted `none` augmentation
- Loss policy: trusted `focal_tversky` primary loss and trusted `weighted_bce` centerline auxiliary loss at weight 0.02
- Optimizer/training: Harness-owned AdamW, learning rate 0.0003, batch size 4, max epochs 12, `constant_lr`, disabled early stopping per active configuration
- Candidate code owns only model architecture over approved tensors; it does not implement data loading, sampling, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, or pretrained weights

## Budget Requested

Use the active Workspace Configuration ceilings: 1,024 provider-selected records per Dataset Source and split, 12 epochs, batch size 4, constant learning rate 0.0003, disabled early stopping, one sequential A100 run slot, Docker training wall-clock budget 3,600 seconds, at most four fixed `first_n` prediction artifacts, and the 25,000,000-parameter smoke ceiling. The architecture is ABI-068, previously measured at about 12.09M parameters, so the resource envelope should remain comparable.

## Success Criteria

Treat this as capped family-development evidence. Useful continuation evidence is any of:

- best validation aggregate filtered Dice ties ABI-068 within about 0.01 or improves over it;
- filtered precision or Contrail Connectivity Metric improves over ABI-068 while aggregate filtered Dice remains near the ABI-066/078/081/085 band;
- MIT and Google filtered Dice both stay above about 0.33 with improved source balance relative to ABI-068;
- predicted-positive fraction decreases toward ABI-066 without severe recall loss;
- finite, non-degenerate predictions and a diagnostically clearer trajectory showing whether random mirroring is necessary for this family.

Do not promote from capped evidence alone. Promotion interpretation would require separate whole-validation diagnostics and human review.

## Fallback/Next Decision

If ABI-087 is non-finite, collapses, or clearly underperforms ABI-068/066 without diagnostic benefit, keep trusted `random_mirroring` as the default for this architecture and do not repeat the no-augmentation branch unchanged. If it improves precision/connectivity, source balance, or aggregate Dice, write a Research Note comparing it with ABI-068/066/081/085 and consider a bounded whole-validation diagnostic on the same stable Run identity. If it ties without improving secondary metrics, broaden to another trusted training/data-policy axis or a materially different thin-line architecture rather than adding more output-side refiners.
