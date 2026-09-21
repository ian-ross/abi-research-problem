# ABI-346 temporal C4 connected-recall ladder late36 U-Net

## Hypothesis

Family-development continuation. ABI-346 is a close but mechanism-changing continuation of ABI-306, the current compact high-precision temporal C4 comparator. ABI-306's failure-bucket diagnostic showed that its gain was not a recall breakthrough: it reduced ABI-285-like clutter and improved precision, but left an under-recall positive-tail and had a larger low-threshold diagnostic Dice reserve than the trusted fixed 0.5 threshold operating point. The hypothesis is that a connected-recall ladder head can raise true contrail evidence to the fixed threshold while preserving ABI-306's compactness: a base mask anchor remains the default, while a bounded non-negative recall lift is applied only in a soft uncertainty band when internal mask, Line, Centerline, and local continuity evidence agree, with a small low-line-evidence clutter veto.

## Comparison Target

Primary comparison target: ABI-306 (`run_20260914_124245_de843c`) on the same provider-owned temporal-eligible validation population for offsets `[-1, 0, 1]`.

Secondary context: ABI-285 as the broader recall-heavy temporal C4 predecessor, ABI-223/238 as temporal-attention connectivity/precision comparators, and ABI-324/337 as five-frame temporal C4/detail-consensus comparators. This is capped temporal-eligible feasibility evidence only, not whole Working Validation Split promotion evidence against ABI-202 or ABI-249.

## Expected Effect

Expected favorable pattern: filtered recall and MIT-positive-tail behavior improve relative to ABI-306 without returning to ABI-285's broad footprint. Success would look like filtered Dice at or above ABI-306, recall closer to ABI-285/255, precision remaining near ABI-306, filtered predicted-positive pixels remaining near the ABI-306/223/238 compact range, and connectivity improving rather than regressing.

Expected risk: the recall ladder may repeat the common temporal-family failure mode by broadening predictions, increasing negative-patch clutter, or lowering connected-line continuity. If it behaves like a broad residual head, it should be treated as negative evidence for this exact head.

## Implementation Sketch

Start from ABI-306's resource-profiled temporal C4 line-state U-Net:

- provider-owned `abi_16ch_plus_sza_temporal` tensor, offsets `[-1, 0, 1]`, split into previous/center/next frames inside the model only;
- per-frame finite ABI/Solar Geometry Input normalization plus ABI-channel-derived BTD features;
- temporal attention/change stem with C4 orientation-consensus line state;
- compact encoder/decoder with early line-state injection, ASPP bottleneck, and high-resolution directional context.

Replace only the final dual-evidence residual head with `ConnectedRecallLadderHead`:

- base mask, Line, and Centerline logits from shared decoder features;
- local horizontal/vertical continuity context from differentiable depthwise convolutions;
- an uncertainty-band scalar derived from the base mask probability, used only as architecture-internal gating, not as Candidate-owned thresholding or postprocessing;
- bounded non-negative recall support gated by mask/Line/Centerline/continuity agreement;
- bounded low-line-evidence clutter veto that is suppressed around confident base-mask anchors.

The model still returns only `mask_logits`, `line_logits`, and `centerline_logits` for Harness-owned losses and metrics.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal`
- `data.frame_selection_policy: temporal_eligible_center`
- `data.temporal_frame_offsets: [-1, 0, 1]`
- `data.sampling_policy: combined_source_balanced`
- `data.augmentation_policy: random_mirroring`
- `training.loss: bce_dice`
- `training.optimizer: adamw`
- `training.scheduler.policy: constant_lr`
- `auxiliary_targets`: trusted Line and Centerline targets with weighted BCE
- Candidate-owned code defines architecture only. It does not load data, inspect temporal caches, choose samples, define losses/metrics/thresholds, implement Artifact Filters/postprocessing, use coordinates or Dataset Source identity, download weights, schedule resources, or alter lifecycle behavior.

## Budget Requested

Request the approved `late_improving` budget for 36 epochs using `budget_request.yaml`. Justification: ABI-306 selected its best checkpoint at epoch 36 and the temporal C4 family has repeatedly required late-budget evidence to separate compact/high-precision states from recall-heavy states. If the Harness denies the request, run under the exploratory budget and treat the resulting capped evidence as valid.

## Success Criteria

ABI-346 is worth follow-up if it is finite, resource-safe, non-collapsed, source-informative, and shows at least one of:

- filtered Dice at or above ABI-306 with no material loss of source balance;
- filtered recall meaningfully above ABI-306 while preserving most of ABI-306's precision and compact filtered-positive footprint;
- connectivity above ABI-306 without sacrificing aggregate/source filtered Dice;
- a late-improving trajectory that identifies a compact connected-recall state not present in ABI-306.

It does not need to beat mature whole-validation references in this capped temporal-eligible step, but it must improve the ABI-306 trade-off or reveal a diagnostically useful failure mode.

## Fallback/Next Decision

If ABI-346 regresses by broadening predictions, increasing negative-patch clutter, or losing connectivity, do not submit another unchanged connected-recall ladder continuation. Use it as evidence that ABI-306-style low-threshold reserve is not easily recoverable through this head. If it improves recall/continuity while remaining compact, request a temporal-eligible failure-bucket diagnostic in a later step before making comparator claims. If it fails contract/smoke/numerical checks, classify the failure and create a repair only if the original hypothesis and comparison target can be preserved.
