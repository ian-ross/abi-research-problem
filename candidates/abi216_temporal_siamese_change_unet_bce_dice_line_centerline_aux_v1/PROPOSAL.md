# ABI-216 temporal Siamese change U-Net

## Hypothesis

A compact shared-weight temporal encoder over provider-owned `[-1, 0, 1]` ABI+SZA frames can learn motion/change cues that are not available to the mature single-frame ABI-202 family. Center-minus-neighbor residual streams should help separate persistent or advecting contrail structure from static geographic edges, fixed scan artifacts, and one-frame cloud-edge clutter while preserving the center-frame Contrail Mask target.

## Classification

Family scout. ABI-215 established temporal lifecycle access but was intentionally too small to be segmentation evidence. ABI-216 is the first real temporal/change segmentation scout in this campaign, so it is not required to beat the late36 ABI-202 incumbent in one exploratory run.

## Comparison Target

Primary scientific context is ABI-202 (`run_20260904_043143_ee0005`), the current best whole-validation-tested single-frame candidate. ABI-215 (`run_20260908_111425_74e4ec`) is only the temporal provisioning baseline: ABI-216 should improve substantially over the canary's near-zero Dice and demonstrate whether temporal features can train within the active resource envelope.

## Expected Effect

The model may initially trail ABI-202 because the temporal-eligible subset and temporal encoder are newly scouted. Useful evidence would be finite learning, non-collapsed predicted-positive fractions, source-informative MIT/Google metrics, and capped filtered Dice that approaches established non-temporal scouts while showing different recall/connectivity behavior. The expected benefit, if present, is better recall for faint moving/persistent contrails and fewer static-line false positives via learned center-minus-neighbor residuals.

## Implementation Sketch

Consume the trusted 51-channel tensor only. Reshape it into three ordered 17-channel frames, normalize each frame's ABI channels and Solar Geometry Input, derive fixed ABI-channel BTD planes per frame, and pass every frame through the same small convolutional encoder. At each encoder scale, fuse the previous, center, and next features with differentiable temporal summaries: center feature, temporal mean, center-minus-previous, next-minus-center, and next-minus-previous. Decode the fused multi-scale representation with a compact U-Net/ASPP head and emit `mask_logits`, `line_logits`, and `centerline_logits` for trusted auxiliary supervision.

## Contract Features Used

- Research Problem: `goes_abi_contrail_segmentation`
- Input mode: `abi_16ch_plus_sza_temporal`
- Temporal frame offsets: `[-1, 0, 1]`
- Frame selection policy: `temporal_eligible_center`
- Output form: `mask_logits`
- Trusted auxiliary targets: Line Target and Centerline Target with weighted BCE
- Provider-owned `combined_source_balanced` traversal and `random_mirroring` augmentation
- Provider-owned `bce_dice` primary loss
- Harness-owned AdamW optimizer, constant learning-rate scheduler, metrics, Artifact Filters, capped-record selection, GPU placement, and lifecycle
- No candidate-owned data loading, temporal lookup, cache reads, frame padding/repair, split logic, target derivation, losses, metrics, thresholding, postprocessing, Artifact Filters, sampling, augmentation implementation, coordinates, pretrained weights, runtime downloads, training loop, persistence, or scheduling

## Budget Requested

Use the exploratory/default Candidate budget: 12 epochs, batch size 2, learning rate 0.0003, active 1,024-per-Dataset-Source train/validation caps, constant learning rate, disabled early stopping, fixed prediction-retention policy, and Harness-owned sequential execution. Batch size 2 is chosen because true temporal encoders are not yet resource-profiled.

## Success Criteria

Continue temporal family development if the Run completes without Resource Failure, candidate bug, contract violation, non-finite state, or persistent all-positive/all-negative prediction collapse and shows at least one of:

1. Capped `val/filtered_dice` materially above the ABI-215 canary and within range of early single-frame scouts (roughly >= 0.20) with finite source-stratified metrics.
2. Improving or ambiguous late trajectory at epoch 12 with nondegenerate predicted-positive fractions.
3. Distinctive recall or connectivity behavior that suggests temporal evidence is useful even if aggregate Dice trails ABI-202.

Hard-stop this exact branch only for execution/resource failure that cannot be repaired compactly, non-finite training, persistent prediction collapse, or a clear plateau/divergence with poor source behavior. Do not reject temporal modeling solely because this first scout fails to beat ABI-202.

## Fallback Next Decision

If ABI-216 is resource-heavy or wall-clock limited, repair by reducing base width or removing one encoder scale while preserving the temporal hypothesis. If it is finite but under-tuned, compare trajectories and source behavior before deciding between a compact continuation, a matched single-frame temporal-eligible control, or a richer temporal attention/ConvGRU scout.
