# ABI-212 compact full-spectral BTD+SZA line-preserving coarse-support ASPP

## Proposal classification

**Family-development continuation.** ABI-212 continues the ABI-211 line-preserving coarse-support ASPP branch after ABI-211 failed with a Harness-recorded `resource_failure` from wall-clock exhaustion. This is not a repair Candidate in the candidate-bug sense, not a promotion claim, and does not request the late-improving budget.

## Hypothesis

ABI-202 is the current strongest whole-validation aggregate filtered-Dice reference, but its diagnostics still leave a false-positive burden relative to ABI-184. ABI-211 tested a coarse-support bridge that used broad context only as a bounded additive feature cue, preserving the signed-detail/line stream instead of using support to threshold or erase mask evidence. That exact implementation was too slow: Run `run_20260904_162059_678c48` reached finite validation through epoch 11 but exhausted the 3,600-second exploratory wall-clock budget during epoch 12 training.

The partial ABI-211 trajectory was not a hard scientific failure: validation filtered Dice reached 0.3778 at epoch 9 with Google filtered Dice 0.4233, precision 0.4584, recall 0.3213, connectivity 0.3793, and a low 0.00254 filtered predicted-positive fraction. ABI-212 therefore tests whether a compact version can complete the exploratory budget while preserving the useful low-area, line-preserving support signal.

## Comparison Target

Primary comparison target: ABI-211 `run_20260904_162059_678c48`, a wall-clock-failed branch with best observed partial validation filtered Dice 0.3778 at epoch 9 and no complete final Result.

Scientific comparison targets:

- ABI-202 `run_20260904_043143_ee0005`, current whole-validation aggregate reference: capped best `val/filtered_dice` 0.4276 at epoch 34 and whole-validation filtered Dice 0.4312.
- ABI-201 `run_20260904_032624_7e855a`, same-family 12-epoch exploratory parent: capped filtered Dice 0.3958, precision 0.4587, recall 0.3481, connectivity 0.4630.
- ABI-203 `run_20260904_073913_3edd12`, foreground-calibrated exploratory continuation: capped filtered Dice 0.4023.
- ABI-210 `run_20260904_152018_ce1309`, compact spectral-ridge support continuation: capped filtered Dice 0.3952 but weak connectivity 0.2515.
- ABI-184 `run_20260902_213856_2c04ac`, precision/connectivity and strict negative-patch-discipline reference.

## Expected Effect

A useful ABI-212 result should first solve the resource question: complete 12 exploratory epochs inside the 3,600-second wall-clock budget without numerical, contract, or lifecycle failure. Scientifically, success does not require immediately beating late36 ABI-202. The useful signal is a complete, finite, non-collapsed Result that stays near or above ABI-211's partial best and approaches the ABI-201/203 exploratory range while retaining ABI-211's low predicted-positive area and precision/connectivity discipline better than ABI-210.

## Implementation Sketch

Start from ABI-211 and keep the same in-contract data, loss, auxiliary-target, optimizer, scheduler, augmentation, and input-mode choices. Make only architecture-local compaction changes:

1. Reduce the learned front-end projection from 16 to 12 channels.
2. Reduce the encoder/decoder base width from 34 to 28.
3. Reduce full-scale fusion branch width from 16 to 12.
4. Use depthwise horizontal/vertical directional convolutions in the final line refiner and the coarse-support bridge.
5. Simplify the coarse-support bridge from six fused feature groups to five and reduce broad smoothing kernels while retaining a zero-initialized bounded residual.

The bridge still uses only decoder, signed-detail, stem, and full-scale features derived from provider-approved ABI/SZA inputs. It predicts no support target, applies no thresholding or postprocessing, and cannot remove the decoder/detail stream.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary targets `line` and `centerline`, auxiliary loss `weighted_bce`, auxiliary weights 0.01 and 0.02, AdamW, learning rate 0.0003, batch size 4, manifest `max_epochs: 12`, and `constant_lr` scheduler.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, budget approval, and prediction retention.
- Candidate code defines model architecture only and contains no data loading, custom losses, custom metrics, Artifact Filters, postprocessing, thresholding, runtime downloads, filesystem persistence, Candidate-owned scheduling, or coordinate features.

## Budget Requested

One sequential exploratory capped Run: at most 1,024 training and validation ABI Patches per Dataset Source and Leakage-Safe Split, 12 effective epochs, batch size 4, 3,600-second Docker timeout, at most four Harness-selected `first_n` prediction artifacts, 25,000,000-parameter smoke ceiling, constant scheduler policy, disabled early stopping, and pinned A100 execution through the Harness. No late-improving budget is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and runtime stays within the exploratory 3,600-second wall-clock envelope.
3. Losses, logits, gradients, parameters, metrics, and checkpoint state remain finite for primary and auxiliary outputs.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw/filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. The continuation is promising if it improves over ABI-211's partial best, completes near ABI-201/203 exploratory Dice, or offers a clearer precision/connectivity/positive-area tradeoff without large source-balanced recall loss.

## Fallback/Next Decision

If ABI-212 still exhausts wall-clock, classify the compact line-preserving coarse-support branch as too expensive under the active exploratory envelope and broaden away rather than requesting Candidate-owned scheduling or another resource workaround. If it completes but falls below ABI-211's partial signal or repeats ABI-210's weak-connectivity support-expansion pattern, do not continue this branch. If it completes with source-informative metrics near ABI-201/203 and improved area/precision/connectivity tradeoffs, write a Research Note and consider either whole-validation diagnostics or a future late-improving close continuation only if the trajectory meets the approved late-budget criteria.
