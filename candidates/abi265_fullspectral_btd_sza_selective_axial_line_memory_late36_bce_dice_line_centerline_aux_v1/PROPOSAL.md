# ABI-265 selective axial line-memory U-Net late-improving continuation

## Hypothesis

ABI-264 validated a compact single-frame selective axial line-memory mechanism: it completed safely, stayed noncollapsed, improved recent SegFormer/MaxViT broad scouts, and selected epoch 12 as its best checkpoint with a sharp late jump in filtered Dice and connectivity. The hypothesis for ABI-265 is that the same architecture, trained under the approved `late_improving` budget when granted, can turn the final-epoch improvement into a more stable precision/recall/source-balanced trajectory without adding Candidate-owned postprocessing or changing trusted data/loss/metric policy.

This is a **family-development continuation** and late-improving close continuation, not a new architecture family and not a promotion claim. It deliberately preserves the ABI-264 architecture so the controlled factor is additional Harness-owned training budget.

## Comparison Target

Primary comparison target:

- ABI-264 (`run_20260912_055445_9221de`): exploratory parent, best epoch 12, capped `val/filtered_dice` 0.407091, filtered precision 0.399434, filtered recall 0.415047, connectivity 0.410422, MIT filtered Dice 0.398792, Google filtered Dice 0.428117.

Broader context:

- ABI-262/263 overlap-SegFormer scouts and ABI-260 compact MaxViT scout, which ABI-264 improved on aggregate Dice and especially connectivity.
- ABI-249 C4 steerable line-context late run and ABI-202 aggregate frontier remain stronger mature context and are not hard gates for this close continuation.

## Expected Effect

If ABI-264 was truncated by the exploratory epoch ceiling, extending the identical selective axial line-memory U-Net should preserve its recall/connectivity advantage while improving calibration/precision and source balance. Success would look like a best checkpoint after epoch 12, higher or more stable `val/filtered_dice`, and no collapse in filtered precision, recall, or MIT/Google metrics.

A negative result is also useful: if extended training plateaus, diverges, or trades too much precision for recall, then the exact ABI-264 branch should shift to a mechanism change or stop rather than consuming more late-budget repeats.

## Implementation Sketch

Reuse the ABI-264 PyTorch architecture unchanged except for Candidate identity. The model consumes provider-owned `abi_16ch_plus_sza` tensors. Its front end normalizes ABI channels 1-16, derives fixed thermal BTD planes only from approved ABI channels, encodes Solar Geometry Input as scaled/cosine features, and learns a small 1x1 channel mixture.

The encoder-decoder is a compact U-Net with `SelectiveAxialLineMemory` blocks at multiple scales. These blocks compute learned-gated differentiable prefix-average feature states along rows and columns, fuse long-line context with local depthwise line convolutions, and retain high-resolution signed-detail evidence. The output head returns `mask_logits`, `line_logits`, and `centerline_logits`.

## Contract Features Used

- `research_problem: goes_abi_contrail_segmentation`
- `input_mode: abi_16ch_plus_sza`; no longitude or latitude inputs.
- `data.frame_selection_policy: all_target_frames`.
- `output_form: mask_logits`.
- Trusted auxiliary targets: Line Target via `line_logits` and Centerline Target via `centerline_logits` with `weighted_bce` weights 0.01 and 0.02.
- Trusted primary loss: `bce_dice`.
- Trusted optimizer/scheduler: AdamW with constant learning rate 0.0003.
- Trusted provider sampling and augmentation: `combined_source_balanced` and `random_mirroring`.
- Batch size 4 and manifest `max_epochs: 12`; longer execution is requested only through `budget_request.yaml` under the approved late-improving Harness policy.

Candidate code defines architecture only. It does not implement data loading, split logic, sampling, augmentation transforms, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, training loops, downloads, filesystem probes, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Budget Requested

Request the approved `late_improving` budget: up to 36 epochs and the corresponding Harness-owned late-improving timeout, with fallback to the exploratory budget if denied. The request is justified by ABI-264's final-epoch best checkpoint, finite/nondegenerate predictions, source-informative MIT and Google metrics, bounded predicted-positive fraction, and strong epoch-12 recovery.

## Success Criteria

Continue or diagnose this branch if the Run is finite, contract-valid, noncollapsed, and any of these hold:

- best `val/filtered_dice` improves over ABI-264 by a meaningful margin while precision and recall remain balanced;
- connectivity remains near or above ABI-264 while precision improves or source balance improves;
- the best checkpoint occurs late with stable MIT and Google metrics, suggesting remaining training-budget sensitivity;
- the result becomes close enough to ABI-249/ABI-202 capped frontier context to justify a trusted whole-validation diagnostic.

Do not require ABI-265 to beat mature ABI-202 whole-validation evidence before treating the selective axial line-memory family as worth one further bounded development decision.

## Fallback/Next Decision

If the budget request is denied, accept the exploratory run as the bounded result. If ABI-265 fails contract/smoke, repair only if the ABI-264 hypothesis and comparison target are preserved. If it completes but plateaus below ABI-264 or loses precision/source balance while not improving connectivity, stop exact late-budget repeats and consider either a precision-preserving architecture change or a different underexplored family.
