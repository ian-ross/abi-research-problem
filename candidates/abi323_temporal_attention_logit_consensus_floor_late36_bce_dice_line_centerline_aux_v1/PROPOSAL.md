# Experiment Proposal: ABI-323 temporal-attention logit-consensus floor late36

## Classification

Family-development continuation. ABI-323 is a close, resource-aware continuation of the ABI-223 compact temporal-attention family, not a new data, loss, metric, sampling, or execution policy.

## Hypothesis

ABI-223 remains the temporal-attention comparator, but later temporal variants show a recurring fixed-threshold trade-off: mechanisms that raise recall often broaden clutter or lose connectivity, while compact heads under-recall true thin contrails. ABI-323 tests whether a small architecture-internal logit-consensus floor can raise true thin-contrail logits only when learned line, centerline, high-resolution detail, and decoder-context evidence agree.

## Expected Effect

The expected effect is higher filtered recall or connectivity than ABI-321 and competitive temporal-eligible filtered Dice/source balance versus ABI-223, without excessive filtered predicted-positive fraction or precision collapse.

## Comparison Target

- Primary family comparator: ABI-223 (`run_20260908_154531_8c7e2b`), the temporal-attention diagnostic comparator.
- Local negative control: ABI-321 (`run_20260915_183315_3f1d30`), lightweight temporal-attention center-detail sharpening that became too compact and recall-limited.
- Recent temporal C4 comparators: ABI-306, ABI-309, and ABI-311 for precision/recall/connectivity trade-offs on the temporal-eligible population.
- Whole-validation context only: ABI-202/ABI-249 remain full-validation comparators; this temporal-eligible capped Run is not promotion evidence.

## Implementation sketch

Start from ABI-223's provider-owned three-frame temporal input path: finite per-frame ABI+SZA+BTD feature construction, shared frame projection, per-pixel temporal attention around the center frame, compact U-Net encoder/ASPP decoder, and Line/Centerline auxiliary outputs.

Replace the plain output heads with `ConsensusLogitFloorHead`:

- `region_head` produces the base `mask_logits`.
- `line_head`, `centerline_head`, and `detail_head` produce learned differentiable evidence logits from decoder and center-detail features.
- a learned `consensus_gate` allows a small non-negative residual only when line, centerline, detail, and region evidence agree;
- a learned `conflict_gate` attenuates that residual when local detail and broader region features disagree.

The residual is bounded (`0.18 * consensus_floor`) and uses smooth tensor operations only. It does not implement thresholding, morphology, connected-component logic, postprocessing, Artifact Filtering, custom losses, custom metrics, calibration search, temporal lookup, padding, sampling, target derivation, coordinates, Dataset Source identity, downloads, training loops, scheduler changes, prediction retention, or resource scheduling.

## Contract Features Used

- `input_mode: abi_16ch_plus_sza_temporal`
- `data.frame_selection_policy: temporal_eligible_center`
- `data.temporal_frame_offsets: [-1, 0, 1]`
- `data.sampling_policy: combined_source_balanced`
- `data.augmentation_policy: random_mirroring`
- `training.loss: bce_dice`
- Line auxiliary target with trusted weighted BCE weight `0.01`
- Centerline auxiliary target with trusted weighted BCE weight `0.02`
- AdamW, constant LR `0.0003`, batch size `2`

## Budget Requested

Request the approved `late_improving` budget (`requested_max_epochs: 36`) with fallback to the exploratory budget if denied. ABI-223 selected epoch 36 as best under an approved late36 Run, so a close architectural continuation of that temporal-attention mechanism has parent evidence that the family can use the longer budget. ABI-321 is included as finite resource/context evidence for a small head modification but not as proof that this exact mechanism should be promoted.

## Success criteria

ABI-323 is successful enough for continued consideration if it is finite, non-collapsed, within resource limits, and shows at least one of:

- temporal-eligible filtered Dice near ABI-223 while improving filtered recall or connectivity;
- clear improvement over ABI-321 on aggregate and source-stratified filtered Dice without losing its compactness advantage catastrophically;
- a source-informative late trajectory suggesting the consensus floor stabilizes rather than merely oscillates;
- a diagnostically useful precision/recall/connectivity trade-off not already covered by ABI-306/309/311.

It is not required to beat ABI-202/ABI-249 full-validation scores in this capped temporal-eligible Run.

## Fallback decision

If ABI-323 fails smoke/contract/syntax, classify and repair only if the fix preserves the same hypothesis. If it completes but regresses like ABI-321 or broadens clutter without source/connectivity benefit, record negative evidence and avoid further direct temporal-attention gated-head variants. Broaden next to a materially different continuity mechanism or a single-frame C4/orientation-plus-cross-scale path rather than another unchanged late continuation.
