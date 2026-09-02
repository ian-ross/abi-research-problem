# ABI-174 Full-Spectral BTD+SZA Signed-Detail Line-Consensus Full-Scale Skip ASPP Decoder BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-173 is the strongest whole-validation-tested SZA-aware ASPP/detail aggregate branch observed so far, with whole-validation filtered Dice 0.3973 and useful recall recovery over ABI-154. Its main weakness is that the signed-detail recall recovery increased negative-patch clutter and reduced connectivity relative to ABI-154 and ABI-130. ABI-174 keeps ABI-173's signed-detail branch and trusted training policy, but adds a conservative connectivity-preserving feature calibration mechanism instead of another unconstrained recall expansion.

## Hypothesis

ABI-173 showed that signed positive/negative detail streams can recover fixed-threshold recall, but the decoder/head did not require those recovered positives to agree with connected line-context evidence. A gently initialized line-consensus calibration block after the existing line-aware refinement should preserve the signed-detail recall signal while biasing final features toward structures supported by short and wide horizontal/vertical context. The expected behavior is lower negative-patch clutter and higher connectivity than ABI-173, while maintaining most of ABI-173's aggregate/source Dice and recall gains over ABI-154.

## Comparison Target

The primary comparison target is ABI-173 `abi173_fullspectral_btd_sza_signed_detail_fullscale_skip_aspp_decoder_bce_dice_centerline_aux_v1`, Run `run_20260901_234732_bd5917`: capped filtered Dice 0.3962, MIT/Google filtered Dice 0.3838/0.4269, filtered precision 0.4238, recall 0.3720, connectivity 0.3203, and filtered predicted-positive fraction 0.00318. Whole-validation diagnostics for the same Run reached filtered Dice 0.3973, MIT/Google filtered Dice 0.3870/0.4161, precision 0.4263, recall 0.3719, connectivity 0.3197, and elevated negative-patch false-positive burden.

Secondary references are ABI-154 `run_20260901_071026_32d3ec` as the full-scale skip ASPP/detail precision/connectivity branch, ABI-130 `run_20260831_121006_7d24be` as the prior whole-validation-tested SZA-aware ASPP/detail aggregate branch, and ABI-068 `run_20260828_010836_4ccc77` as the broader capped aggregate/source-balance comparator.

## Expected Effect

A useful outcome would retain aggregate filtered Dice in the ABI-173/154/130/068 band, keep MIT and Google filtered Dice above about 0.38 and 0.41 on the representative cap, and improve ABI-173's precision or connectivity without losing most of its recall recovery. A stronger outcome would approach ABI-154-like connectivity and positive-area discipline while preserving ABI-173-like aggregate Dice and recall. A negative outcome would over-suppress the signed-detail gains, returning to ABI-154-like under-recall, or would add compute/noise without reducing clutter or improving connectivity.

## Implementation Sketch

- Reuse ABI-173's approved-channel front end: normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized Solar Geometry Input, cosine SZA feature, and learned 1x1 projection over approved inputs.
- Preserve ABI-173's signed local and mid-scale detail stems, compact residual encoder, ASPP context, decoder, full-scale skip fusion, and existing line-aware refinement.
- Add `ConservativeLineConsensusCalibration` after the line-aware refinement and before the final heads. It learns short and wide horizontal/vertical context features, fuses them with refined features into a consensus feature, and applies a gently initialized feature-space support gate. The gate only calibrates learned features inside the network; it is not thresholding, postprocessing, or an Artifact Filter.
- Keep primary `mask_logits` and provider-derived `centerline_logits` auxiliary output.
- Keep trusted `bce_dice` primary loss, trusted `weighted_bce` Centerline Target auxiliary weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate 0.0003, batch size 4, max epochs 12, constant scheduler, disabled early stopping, and one sequential representative capped Run.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude, latitude, reconstructed coordinates, and Dataset Source identity are excluded.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared auxiliary `[1, 256, 256]` `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `centerline`, auxiliary loss `weighted_bce`, auxiliary weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, primary and auxiliary target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.

## Budget Requested

One sequential 12-epoch representative capped Run using at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant learning-rate scheduler policy, disabled early stopping, and the 3,600-second trusted training timeout. No full-data claim, Post-Run Evaluation, Experiment Batch, or promotion decision is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 completes inside the trusted runtime envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported, with no Dataset Source-specific catastrophic execution failure.
6. As family-development evidence, the result is useful if it improves ABI-173 precision, connectivity, or predicted-positive discipline while keeping ABI-173-like aggregate/source Dice and recall, or if it clearly maps the cost of adding line-consensus calibration to the signed-detail branch.

## Continuation and hard stop

Continue the signed-detail line-consensus branch only if ABI-174 is finite, non-degenerate, source-informative, and shows improved clutter/connectivity behavior without severe recall loss. Stop or repair this exact branch for hard execution failure, persistent non-finite behavior, persistent prediction collapse, clear optimization failure, severe source-specific collapse, or resource failure outside the trusted envelope. If it completes finite but behaves like another local full-scale-skip under-recall or noisy calibration regression, stop this branch and broaden to a more distinct architecture, data-policy, preprocessing, calibration, or evaluation frontier.

## Fallback/Next Decision

If ABI-174 fails from a narrow implementation defect while the line-consensus hypothesis remains intact, consider at most one explicit Repair Candidate in a later Autonomy Step. If it is scientifically negative, document the result and avoid further local head/stem tweaks unless diagnostics explain why they should avoid the repeated precision/recall/connectivity tradeoff. If it preserves ABI-173's whole-validation-tested aggregate strength while reducing negative-patch clutter or recovering connectivity, request separate whole-validation diagnostics before making any full-data or promotion claim.
