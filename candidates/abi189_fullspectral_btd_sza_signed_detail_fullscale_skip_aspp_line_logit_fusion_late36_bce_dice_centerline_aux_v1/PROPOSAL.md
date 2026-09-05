# ABI-189 Full-Spectral BTD+SZA Signed-Detail Full-Scale Skip ASPP Line-Logit Fusion Late36 BCE-Dice Centerline Auxiliary v1

## Proposal classification

**Family-development continuation.** ABI-189 is a close late-improving continuation of ABI-188, not a new architecture family and not a promotion claim. It preserves the ABI-188 signed-detail full-scale skip ASPP architecture and detached auxiliary-logit mask fusion mechanism exactly, and changes only the candidate-local reviewed budget-request path to test whether ABI-188 final-epoch improvement was truncated by the 12-epoch exploratory ceiling.

## Hypothesis

ABI-188 showed that a small bounded positive residual from detached `line_logits` and `centerline_logits` can soften the ABI-183/184 primary mask operating point without the severe connectivity collapse of ABI-187 focal-Tversky. It selected epoch 12, the final exploratory epoch, after a late filtered-Dice jump from 0.3631 to 0.4013. A 36-epoch trusted late-improving continuation may determine whether the same mechanism can recover ABI-181/184-level capped filtered Dice while preserving ABI-188 MIT recall gain and useful line connectivity, or whether the epoch-12 jump was representative-subset noise.

## Comparison Target

The primary parent is ABI-188 `run_20260903_031950_88e745`: exploratory best epoch 12, capped filtered Dice 0.4013, raw Dice 0.4160, MIT/Google filtered Dice 0.3898/0.4317, filtered precision 0.4250, recall 0.3801, connectivity 0.3903, and filtered predicted-positive fraction 0.00324. It improved ABI-183 on aggregate filtered Dice, MIT filtered Dice, and recall, but remained below ABI-184 late36 precision/connectivity reference and ABI-181 late36 aggregate reference.

Key references are ABI-184 `run_20260902_213856_2c04ac` with late36 filtered Dice 0.4066, precision 0.4850, recall 0.3500, connectivity 0.4634, and filtered predicted-positive fraction 0.00261; ABI-181 `run_20260902_150611_cbbf35` with late36 filtered Dice 0.4104, precision 0.4423, recall 0.3828, connectivity 0.3639, and whole-validation filtered Dice 0.4124; ABI-183 `run_20260902_204128_bba815` as the exploratory Line plus Centerline parent; ABI-187 `run_20260903_022247_88e0dc` as the focal-Tversky connectivity-collapse negative reference; and ABI-068 `run_20260828_010836_4ccc77` as a source-balanced line-U-Net recall/connectivity comparator.

## Expected Effect

A positive outcome would remain finite and non-collapsed while improving ABI-188 aggregate/source filtered Dice or preserving its recall with better precision/connectivity under longer optimization. The strongest outcome would approach ABI-181/184 aggregate filtered Dice while retaining at least ABI-068-level connectivity and avoiding ABI-187-style positive-area expansion. A negative but useful outcome would show that detached auxiliary-logit fusion plateaus below the late36 references, expands positives, or loses connectivity, supporting a stop on this exact mask-logit-fusion branch and a broader architecture/data-policy frontier.

## Implementation Sketch

- Reuse ABI-188 model code unchanged: normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized and cosine Solar Geometry Input, learned spectral projection, signed local/mid-scale positive and negative detail streams, compact residual encoder, ASPP bottleneck, decoder, full-scale skip fusion, line-aware final refinement, and primary/auxiliary heads.
- Emit `line_logits` and `centerline_logits` exactly as provider-declared auxiliary outputs with trusted `weighted_bce` losses at weights 0.01 and 0.02.
- Preserve ABI-188 mask-logit fusion: `mask_logits = base_mask_logits + 0.25 * relu(tanh(line_logits.detach())) + 0.10 * relu(tanh(centerline_logits.detach()))`.
- Keep trusted manifest choices unchanged: `abi_16ch_plus_sza`, `bce_dice`, `combined_source_balanced`, `random_mirroring`, AdamW, learning rate 0.0003, batch size 4, manifest max epochs 12, constant learning rate, and disabled early stopping.
- Add only candidate-local `budget_request.yaml` requesting the reviewed `late_improving` budget for 36 effective epochs, with fallback to the exploratory budget if denied.
- Do not implement Candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, scheduler policy, GPU placement, runtime downloads, pretrained weights, coordinate inputs, or external persistence.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation` v0.
- Input mode: `abi_16ch_plus_sza`; longitude and latitude source channels are excluded and are not reconstructed.
- Output form: primary `[1, 256, 256]` `mask_logits` plus provider-declared `[1, 256, 256]` auxiliary outputs `line_logits` and `centerline_logits`.
- Trusted manifest choices: `combined_source_balanced`, `random_mirroring`, `bce_dice`, auxiliary target `line` with `weighted_bce` weight 0.01, auxiliary target `centerline` with `weighted_bce` weight 0.02, AdamW, learning rate 0.0003, batch size 4, max epochs 12, constant learning-rate policy, and disabled early stopping.
- Candidate-local budget request: `late_improving`, requested max epochs 36, parent Run `run_20260903_031950_88e745`, fallback `run_exploratory_budget` if denied.
- Provider/Harness owns Leakage-Safe Split, capped-record selection, sampling implementation, augmentation transforms, target derivation, loss implementations, metrics, checkpointing, Artifact Filters, resource limits, execution lifecycle, and prediction retention.

## Budget Requested

One sequential representative capped Run with the reviewed late-improving budget request: at most 1,024 training and 1,024 validation ABI Patches per Dataset Source and Leakage-Safe Split, batch size 4, requested effective max epochs 36, requested 10,800 seconds Docker training wall-clock budget, at most four Harness-selected `first_n` prediction artifacts, the 25,000,000-parameter smoke ceiling, constant scheduler policy, disabled early stopping, and Harness-owned GPU placement. If the Harness denies the request, run under the exploratory budget and treat that result as valid bounded evidence. No full-data claim, promotion decision, Experiment Batch, or Candidate-owned budget change is requested.

## Success Criteria

1. Static validation, smoke testing, and bounded training complete without contract, shape, resource, numerical, or lifecycle failure.
2. Parameter count remains within the 25,000,000 smoke ceiling and batch size 4 remains inside the trusted resource envelope.
3. Primary and auxiliary losses, logits, gradients, parameters, metrics, and checkpoint state remain finite.
4. Final predictions do not persistently collapse to all-negative or all-positive masks.
5. Aggregate, MIT, and Google raw/filtered metrics plus predicted-positive fractions are reported with no Dataset Source-specific catastrophic failure.
6. Family-development success is met if the late-improving continuation improves ABI-188 aggregate/source filtered Dice or preserves ABI-188 recall while improving precision/connectivity and maintaining at least ABI-068-level connectivity. Promotion would require later whole-validation diagnostics and human review; this capped Run alone is not promotion evidence.

## Fallback/Next Decision

If ABI-189 improves aggregate/source filtered Dice while retaining non-collapsed recall and line connectivity, consider a bounded whole-validation Evaluation Request in a later Autonomy Step to test whether the capped tradeoff survives the full Working Validation Split. If it plateaus below ABI-181/184, expands positive-area clutter, or loses the connectivity advantage, stop this exact detached auxiliary-logit-fusion branch rather than repeating it unchanged. If it fails by contract, shape, numerical, resource, or lifecycle criteria, classify the failure before proposing any repair.
