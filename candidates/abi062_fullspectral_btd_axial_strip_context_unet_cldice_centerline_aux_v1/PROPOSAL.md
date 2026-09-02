# ABI-062 Experiment Proposal: full-spectral BTD axial strip-context U-Net

## Hypothesis

A full-spectral BTD encoder-decoder dominated by axial strip-context blocks can reduce the broad low-level false-positive tendency seen in ABI-058 while preserving thin-line continuity better than additional high-resolution decoder-head tweaks.  Strip pooling supplies long row/column context at each scale without coordinate inputs or candidate-owned postprocessing, and a patch-context channel gate lets the learned representation suppress implausible weak line evidence on mostly negative ABI Patches.

Proposal class: **family scout**.  This is an early probe of a materially different strip-context/attention-like architecture axis after the high-resolution line U-Net branch reached a narrow local whole-validation reference but continued to trade recall, precision, and source balance.

## Comparison Target

Primary comparison target is ABI-058 (`run_20260827_171331_c1769a`), the current whole-validation-tested high-resolution BTD line U-Net local reference: capped best `val/filtered_dice` 0.3248 and whole-validation filtered Dice 0.3233.  Secondary context is ABI-061 (`run_20260827_194725_c1d6c6`), whose focal-Tversky follow-up produced capped filtered Dice 0.3221 with higher Google Dice, precision, and connectivity but weaker MIT recall.

Canonical MCAST 2.1 remains the promotion context at whole-validation filtered Dice 0.3873; ABI-062 is not expected to establish promotion without later full Working Validation Split evaluation.

## Expected Effect

The axial strip-context blocks should improve line-continuity evidence and negative-patch discrimination by combining local features, row-pooled context, column-pooled context, and global patch channel gates.  Expected useful outcomes are one or more of: capped filtered Dice near or above ABI-058, lower filtered predicted-positive fraction at similar recall, higher filtered precision without ABI-061's MIT collapse, or improved filtered Contrail Connectivity with source-balanced MIT/Google Dice.

## Implementation Sketch

Implement `build_model(input_spec, output_spec)` returning a PyTorch module that accepts only provider-approved `abi_16ch` tensors.  The model normalizes ABI channels 1-16, adds explicit thermal BTD planes derived only from those channels, and adds a learned 1x1 channel mixer.  A compact encoder-decoder then applies axial strip-context blocks at full, half, quarter, and eighth resolution.  Each strip block combines residual local features, row-pooled asymmetric context, column-pooled asymmetric context, and a globally pooled channel gate through learned branch weights.  The decoder fuses attention-gated skips and emits `mask_logits` plus a provider-derived `centerline_logits` auxiliary output.

## Contract Features Used

- Input mode: `abi_16ch`; no longitude or latitude inputs.
- Output form: `mask_logits` plus trusted `centerline` auxiliary target output `centerline_logits`.
- Primary loss: trusted `bce_dice_cldice`.
- Auxiliary loss: trusted `weighted_bce` with centerline weight 0.02.
- Data policy: trusted `combined_source_balanced` sampling and trusted `random_mirroring` augmentation.
- Training policy: AdamW, learning rate 0.0003, batch size 4, 12 epochs, constant learning rate scheduler.

Candidate code does not implement data loading, split logic, target derivation, custom losses, augmentation transforms, metrics, thresholding, Artifact Filters, postprocessing, filesystem probes, network calls, or runtime weight downloads.

## Budget Requested

One sequential representative capped Run under the active Workspace Configuration: 1,024 provider-selected records per Dataset Source and split, 12 epochs, batch size 4, constant learning rate, A100 execution, 3,600-second wall-clock limit, and the 25 million-parameter smoke ceiling.  Because this is a materially different strip-context architecture family, it should run sequentially rather than as part of a batch.

## Success Criteria

For promotion consideration, ABI-062 would need to beat or credibly tie ABI-058 on capped `val/filtered_dice`, remain non-degenerate on both Dataset Sources, and justify a later whole-validation diagnostic; eventual promotion would still require full Working Validation Split evidence against MCAST 2.1.

For family-scout continuation, ABI-062 can be useful without beating ABI-058 if it completes finite, avoids persistent all-negative/all-positive collapse, reaches capped filtered Dice within about 0.03 of ABI-058, or shows a distinctive secondary gain such as lower predicted-positive burden, higher precision at comparable recall, improved filtered connectivity, or better source balance than ABI-061.

## Fallback/Next Decision

If ABI-062 fails contract validation or resource smoke checks, repair only the implementation bug while preserving this hypothesis.  If it completes but collapses or diverges, mark the exact branch as stopped and broaden to another architecture or trusted-policy axis.  If it is finite but mixed, compare source-stratified precision/recall/connectivity and decide whether one bounded strip-context family-development follow-up is justified.  If it clearly improves capped aggregate or failure-bucket behavior, request a whole-validation diagnostic before making any promotion claim.
