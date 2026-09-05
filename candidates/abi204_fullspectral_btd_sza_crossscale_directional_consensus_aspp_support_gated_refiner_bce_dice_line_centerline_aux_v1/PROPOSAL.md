# ABI-204 full-spectral BTD+SZA support-gated cross-scale directional-consensus ASPP

## Proposal classification

**Family-development continuation.** ABI-204 is a controlled exploratory architecture continuation of ABI-202 after ABI-203 showed that post-refinement mask-logit foreground calibration modestly reduced positive area but lost too much recall, Google Dice, and connectivity. It is not a promotion claim and does not request the late-improving budget for this first support-gated refiner probe.

## Hypothesis

ABI-202 is the current whole-validation aggregate filtered-Dice reference, but its failure buckets still show more aggregate false-positive pixels than ABI-184's stricter negative-patch discipline. ABI-203 suggests that acting only at the final mask-logit head is too late and can suppress useful line evidence. A pre-head, feature-space support-gated line refiner may reduce isolated unsupported clutter while preserving ABI-202's cross-scale recall, Google performance, and connectivity: directional and high-frequency detail features are kept strongest when they agree with full-scale/context support, rather than being corrected after the mask logits already exist.

The hypothesis is limited to model architecture. It does not change data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, metrics, Artifact Filters, thresholding, postprocessing, coordinate inputs, scheduler policy, training loop behavior, resource placement, or prediction retention.

## Comparison Target

Primary comparison target: ABI-202 `run_20260904_043143_ee0005`, whose late36 capped selected checkpoint reached `val/filtered_dice` 0.4276 at epoch 34 and whose whole-validation diagnostic reached filtered Dice 0.4312, MIT/Google filtered Dice 0.4141/0.4644, precision 0.4431, recall 0.4199, connectivity 0.4625, and filtered predicted-positive pixels 672,206.

Secondary comparison targets: ABI-203 `run_20260904_073913_3edd12`, the negative post-head foreground-calibration result; ABI-201 `run_20260904_032624_7e855a`, the 12-epoch cross-scale parent; and ABI-184 `run_20260902_213856_2c04ac`, retained as the precision/connectivity and negative-patch-discipline reference.

## Expected Effect

A useful result should complete finitely and test whether support gating before the final mask/auxiliary heads is a better false-positive-control mechanism than ABI-203's post-refinement mask head. Desired evidence is a cleaner precision or predicted-positive-fraction tradeoff than ABI-202/201, without ABI-203's recall/connectivity loss. A negative but informative result would show that extra support gating inside the cross-scale directional-consensus branch still suppresses true contrail evidence, motivating a broader architecture-family or trusted-policy frontier rather than another local gate.

## Implementation Sketch

Start from the validated ABI-202 cross-scale directional-consensus ASPP model, but remove the candidate-local late-budget request and run at the exploratory budget. Keep approved `abi_16ch_plus_sza` inputs, normalized ABI channels 1-16, deterministic ABI-channel-derived thermal BTD planes, normalized/cosine Solar Geometry features, learned 1x1 spectral mixture, signed local/mid-scale detail stem, compact residual encoder, ASPP context, full-scale skip fusion, and `CrossScaleDirectionalConsensusBridge`.

Replace the ordinary `LineAwareRefinement` stage with `SupportGatedLineAwareRefinement`. This architecture-internal module consumes the bridged decoder feature, high-resolution signed detail feature, and full-scale fusion feature. It computes horizontal, vertical, detail, and broad-context features; learns a soft support gate from feature agreement; and uses that gate to modulate the final pre-head representation. It predicts no target of its own and applies no threshold, hard mask, morphological operation, Artifact Filter, geolocation prior, custom loss, or postprocessing. `mask_logits`, `line_logits`, and `centerline_logits` remain ordinary learned heads trained only through trusted primary and provider-derived auxiliary losses.

Keep the manifest choices unchanged from ABI-202 except for the absence of `budget_request.yaml`: trusted `bce_dice`, trusted `combined_source_balanced`, trusted `random_mirroring`, AdamW learning rate 0.0003, batch size 4, provider-derived Line plus Centerline auxiliary targets with `weighted_bce` weights 0.01 and 0.02, exploratory `max_epochs: 12`, and `constant_lr` scheduling.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.02, AdamW, learning rate 0.0003, batch size 4, manifest `max_epochs: 12`, and constant scheduler policy.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, budget approval, effective epoch limit, and prediction retention.
- Candidate code defines model architecture only and contains no data loading, custom losses, custom metrics, Artifact Filters, postprocessing, thresholding, runtime downloads, filesystem persistence, Candidate-owned scheduling, or coordinate features.

## Budget Requested

One sequential representative capped exploratory Run: at most 1,024 training and validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, 12 effective epochs, the 3,600-second exploratory Docker timeout, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant scheduler policy, disabled early stopping, and pinned A100 execution through the Harness. No late-improving budget is requested for this first support-gated refiner probe.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and the Run remains within the trusted exploratory resource envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw and filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. The continuation is promising if it stays near ABI-201/202 family performance while improving precision or reducing filtered predicted-positive fraction, or if it gives diagnostically useful evidence that feature-space support gating suppresses clutter less destructively than ABI-203's mask-head calibration.

## Fallback/Next Decision

If ABI-204 fails validation or smoke because of the new refiner, classify and repair the candidate-local implementation while preserving the support-gated-refiner hypothesis. If it completes but regresses aggregate/source Dice, recall, or connectivity without improving precision or predicted-positive discipline, do not repeat this gate unchanged and broaden to a different architecture family, trusted data/loss policy, or evaluation/calibration frontier. If it improves false-positive discipline while remaining close to ABI-202's aggregate/source metrics, write a Research Note and consider whole-validation failure-bucket diagnostics before any promotion claim.
