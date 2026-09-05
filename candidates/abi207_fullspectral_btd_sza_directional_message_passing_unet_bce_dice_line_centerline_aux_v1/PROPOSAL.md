# ABI-207 directional message-passing U-Net scout

## Hypothesis

A compact multi-scale directional message-passing U-Net can preserve the source-balanced recall and connectivity strengths of the ABI-202 cross-scale directional-consensus ASPP reference while reducing reliance on heavy local refiner complexity. Passing learned horizontal, vertical, diagonal, and broad-context messages at several encoder scales should help thin contrail structures remain continuous across gaps without using Candidate-owned Artifact Filters, thresholds, or coordinate priors.

Proposal classification: **family scout**. This is a materially different architecture-family probe, not a promotion claim against the heavily developed ABI-202 incumbent.

## Comparison Target

Primary comparison target: ABI-202 Run `run_20260904_043143_ee0005`, the current whole-validation aggregate filtered-Dice reference for the late36 cross-scale directional-consensus ASPP branch.

Secondary comparison targets: ABI-201 Run `run_20260904_032624_7e855a` as the exploratory same-family parent, ABI-184 Run `run_20260902_213856_2c04ac` as the precision/connectivity and negative-patch-discipline reference, and ABI-206 Run `run_20260904_105645_8f8ab1` as evidence that additional boundary pressure did not cleanly solve clutter.

## Expected Effect

Expected positive effects are improved or diagnostically different filtered contrail connectivity, source-balanced MIT/Google behavior, and positive-patch continuity at a lower parameter/runtime profile than the recent ABI-202-derived refiner variants. The exploratory scout is not required to beat ABI-202 immediately. A useful result would be finite, non-collapsed predictions with filtered Dice near the mature frontier or a distinctive connectivity/recall tradeoff that justifies one or two bounded family-development continuations.

Failure evidence sufficient to stop this exact branch includes non-finite behavior, contract failure, persistent all-negative/all-positive prediction collapse, a clear optimization plateau/divergence, or a completed exploratory result far below the line-aware U-Net family frontier without compensating connectivity/source-balance strengths.

## Implementation Sketch

Implement `build_model(input_spec, output_spec)` returning a PyTorch module. The model uses provider-approved `abi_16ch_plus_sza` tensors only, constructs normalized ABI, BTD, SZA, and learned spectral-mixture features from those channels, and feeds them through a compact base-width-32 encoder-decoder. Directional message-passing blocks at multiple scales learn horizontal, vertical, diagonal-shift, and broad-context features, fuse them with a bounded residual, and then decode through full-scale skip fusion and a final line-aware refinement. The model returns exactly `mask_logits`, `line_logits`, and `centerline_logits`.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza`
- `output_form: mask_logits`
- Trusted primary loss `bce_dice`
- Trusted auxiliary targets `line` and `centerline` with `weighted_bce`
- Trusted `combined_source_balanced` sampling traversal
- Trusted `random_mirroring` augmentation
- AdamW learning rate 0.0003, batch size 4, max epochs 12
- `constant_lr` scheduler and disabled early stopping under the active Workspace Configuration

Candidate code does not implement data loading, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, sampling behavior, augmentation, coordinate features, resource scheduling, training loops, filesystem persistence, network access, or runtime downloads.

## Budget Requested

Request the default exploratory budget only: 12 epochs, batch size 4, constant learning rate, and the active Harness-owned timeout/parameter/GPU limits. No late-improving budget is requested for this first scout.

## Success Criteria

For this scout, success means a completed finite Run with non-collapsed predictions and a meaningful source-informative operating point. Continuation is justified if capped `val/filtered_dice` is within roughly 0.04 of ABI-201/202 exploratory-scale references, or if connectivity/recall/source balance is distinctly stronger than comparable exploratory line-aware scouts despite lower aggregate Dice. A final-epoch best checkpoint, improving late trajectory, or strong MIT/Google balance would support a bounded continuation before judging the family.

Promotion is not expected from this scout. Promotion consideration would require later whole-validation diagnostic evidence competitive with ABI-202 and without catastrophic Dataset Source failures or excessive Artifact Filter dependence.

## Fallback/Next Decision

If ABI-207 fails contract/smoke or shows non-finite behavior, classify the failure and either repair candidate code if the hypothesis is preserved or abandon the exact implementation. If it completes but is clearly weak and offers no connectivity/source-balance advantage, stop this exact branch and broaden to another architecture family or trusted policy frontier. If it is finite and promising, consider one controlled family-development continuation before any late-improving budget request.
