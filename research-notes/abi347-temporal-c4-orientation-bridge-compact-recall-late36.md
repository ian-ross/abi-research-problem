# ABI-347 temporal C4 orientation-bridge compact recall late36

research-figures: []

## Scope

This note records ABI-347, Candidate `abi347_temporal_c4_orientation_bridge_compact_recall_late36_bce_dice_line_centerline_aux_v1`, and Run `run_20260918_192439_aafca3`.

ABI-347 was a mechanism-changing close continuation of the three-frame temporal C4 line-state branch. It kept provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection and offsets `[-1, 0, 1]`, source-balanced sampling, trusted random mirroring, BCE-Dice loss, Line and Centerline auxiliary targets, AdamW with constant LR, and batch size 2. The architectural change replaced ABI-346's connected-recall ladder with an orientation-bridge compact-recall head intended to lift uncertain true contrail segments only where mask, Line, Centerline, and learned multi-orientation bridge evidence agreed, while vetoing weak line/bridge regions.

This is capped temporal-eligible evidence only. It is not whole Working Validation Split promotion evidence and should not be compared as a full-data Result against ABI-202 or ABI-249.

## Execution result

ABI-347 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Requested/effective budget: `late_improving`, approved for 36 epochs from ABI-346, ABI-306, and ABI-324 parent evidence.
- Input mode: `abi_16ch_plus_sza_temporal`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Trusted augmentation policy: `random_mirroring`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,253,085, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: 5,943,645,696 / 6,390,022,144 bytes.
- Training wall time: 5,124.5 s; validation wall time: 3,321.8 s; total Run wall time: 8,448.4 s, within the 10,800 s late-improving timeout.
- Stop reason: max epochs reached; best checkpoint selected by `val/filtered_dice` at epoch 24.

## Best-validation metrics

| Metric | ABI-347 orientation bridge | ABI-346 connected-recall ladder | ABI-306 compact temporal C4 | ABI-324 balanced five-frame C4 | ABI-223 temporal-attention |
| --- | ---: | ---: | ---: | ---: | ---: |
| Best epoch | 24 | 23 | 36 | 27 | 36 |
| Filtered Dice | 0.417249 | 0.427835 | 0.422548 | 0.429430 | 0.419776 |
| MIT filtered Dice | 0.391985 | 0.407956 | 0.402764 | 0.408188 | 0.398498 |
| Google filtered Dice | 0.484335 | 0.480484 | 0.476152 | 0.487231 | 0.476764 |
| Filtered precision | 0.473500 | 0.461087 | 0.493422 | 0.470412 | 0.483764 |
| Filtered recall | 0.372944 | 0.399057 | 0.369478 | 0.395017 | 0.370738 |
| Filtered connectivity | 0.331203 | 0.299258 | 0.299384 | 0.397925 | 0.412427 |
| Filtered predicted-positive pixels | 430,686 | 473,249 | 409,457 | 459,172 | 419,056 |

ABI-347 partially achieved the orientation-bridge objective. Relative to ABI-346, it improved precision by +0.0124, improved connectivity by +0.0319, reduced filtered predicted-positive pixels by 42,563, and improved Google filtered Dice by +0.0039. The cost was substantial: aggregate filtered Dice fell by -0.0106, MIT filtered Dice fell by -0.0160, and recall fell by -0.0261. Relative to ABI-306, ABI-347 recovered a small amount of recall (+0.0035) and connectivity (+0.0318), but lost aggregate Dice (-0.0053), MIT Dice (-0.0108), precision (-0.0199), and compactness (+21,229 filtered predicted-positive pixels).

Compared with broader temporal-family references, ABI-347 remains below ABI-324 on aggregate Dice, MIT Dice, recall, and connectivity, though it is slightly more precise and more compact. It is also below ABI-223's connectivity by -0.0812. The orientation bridge therefore found a cleaner connected state than ABI-346/306, but not a new temporal connectivity comparator.

At the selected checkpoint, raw Dice was 0.435220 versus filtered Dice 0.417249, raw recall was 0.402701 versus filtered recall 0.372944, and raw predicted-positive pixels were 465,100 versus 430,686 filtered. Artifact Filters removed 34,414 predicted-positive pixels and lowered the score; they did not create the Result.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.235483 | 0.237825 | 0.230143 | 0.268284 | 0.209829 | 0.182311 | 0.004043 |
| 5 | 0.349896 | 0.346697 | 0.357042 | 0.335633 | 0.365425 | 0.183567 | 0.005628 |
| 8 | 0.400479 | 0.383968 | 0.443106 | 0.480044 | 0.343539 | 0.364313 | 0.003700 |
| 12 | 0.362881 | 0.339980 | 0.420283 | 0.452334 | 0.302967 | 0.290162 | 0.003463 |
| 17 | 0.404894 | 0.381770 | 0.466638 | 0.485458 | 0.347264 | 0.309316 | 0.003698 |
| 18 | 0.409710 | 0.392182 | 0.453007 | 0.412066 | 0.407381 | 0.279559 | 0.005111 |
| 24 | 0.417249 | 0.391985 | 0.484335 | 0.473500 | 0.372944 | 0.331203 | 0.004072 |
| 26 | 0.416701 | 0.396840 | 0.466925 | 0.451771 | 0.386683 | 0.322762 | 0.004425 |
| 29 | 0.399502 | 0.377420 | 0.454098 | 0.400394 | 0.398614 | 0.224613 | 0.005147 |
| 33 | 0.374294 | 0.347514 | 0.445192 | 0.534715 | 0.287916 | 0.348848 | 0.002784 |
| 34 | 0.413782 | 0.389947 | 0.476042 | 0.445386 | 0.386365 | 0.249927 | 0.004485 |
| 36 | 0.416778 | 0.398577 | 0.465265 | 0.473776 | 0.372022 | 0.242616 | 0.004059 |

The trajectory was finite, non-collapsed, source-informative, and late-budget-dependent, but oscillatory. Epoch 24 was the best aggregate checkpoint and a reasonable compact/connected compromise. Epoch 26 nearly matched the selected filtered Dice with better MIT Dice and recall, but lower Google Dice and slightly lower connectivity. Epoch 33 showed a high-precision/high-connectivity compact state with too little recall. The final epoch nearly tied the selected aggregate Dice and improved MIT Dice, but connectivity fell sharply to 0.2426, so the late run did not converge to a stable connected-line state.

## Prediction sample check

The retained fixed first-four validation samples are Harness traceability artifacts, not representative diagnostics. Their sample Dice values were 0.3726, 0.1818, 0.5865, and 0.3845. These confirm finite non-collapsed predictions, but they should not override aggregate validation metrics or justify Candidate-owned thresholding, postprocessing, Artifact Filters, validation selection, or qualitative cherry-picking.

## Interpretation

Classify ABI-347 as mixed temporal C4 family-development evidence for this exact orientation-bridge compact-recall head. The positive signal is that an explicit multi-orientation bridge can improve the ABI-346/306 connectivity metric while shrinking ABI-346's footprint and preserving reasonable precision. The negative signal is that the improved connectivity did not translate into aggregate/source Dice or stable recall, and the selected checkpoint still trails ABI-324 and ABI-223 by a wide margin on connected-line continuity.

Comparator roles after ABI-347:

- ABI-324 remains the balanced five-frame temporal C4/detail-consensus comparator.
- ABI-306 remains the compact high-precision three-frame temporal C4 comparator.
- ABI-346 remains the stronger three-frame temporal C4 recall/aggregate trade-off, with completed temporal-eligible failure-bucket diagnostics.
- ABI-347 is evidence that orientation-bridge gating can reduce ABI-346's footprint and raise connectivity, but it is not a replacement comparator because it sacrifices too much recall and source-balanced Dice.
- ABI-223 remains the temporal-attention connectivity comparator on the temporal-eligible validation population.

ABI-347 does not justify Candidate-owned thresholds, postprocessing, losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, Dataset Source identity, downloads, resource scheduling, or lifecycle changes.

## Decision

Do not promote ABI-347 and do not submit another unchanged late36 orientation-bridge compact-recall continuation. The mechanism answered its narrow question: bridge gating can make the ABI-346 recall head more compact and somewhat more connected, but this implementation loses too much aggregate/MIT recall evidence and fails to approach ABI-324/223 connectivity.

A future Candidate should be mechanism-changing if this branch is revisited. Useful directions would preserve ABI-347's bridge compactness while adding a stronger true-positive recall path, or switch to a materially different temporal alignment/evidence-sharpening mechanism. Simple bridge gain changes, another uncertainty-band residual, or an unchanged orientation-bridge rerun are not justified by this capped Result. A temporal-eligible failure-bucket diagnostic could be considered only if the campaign specifically needs to quantify whether ABI-347's smaller footprint reduced high-tail negative clutter versus ABI-346; it is not requested here because this Research Note is the single primary handoff.

No Candidate Submission, Experiment Batch Submission, Capability Request, Evaluation Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260918_192439_aafca3/candidate/PROPOSAL.md`
- `run_20260918_192439_aafca3/candidate/README.md`
- `run_20260918_192439_aafca3/candidate/manifest.yaml`
- `run_20260918_192439_aafca3/candidate/budget_request.yaml`
- `run_20260918_192439_aafca3/resolved_manifest.yaml`
- `run_20260918_192439_aafca3/execution.json`
- `run_20260918_192439_aafca3/run_metadata.json`
- `run_20260918_192439_aafca3/outputs/model_summary.json`
- `run_20260918_192439_aafca3/outputs/best_metrics.json`
- `run_20260918_192439_aafca3/outputs/final_metrics.json`
- `run_20260918_192439_aafca3/outputs/metrics.jsonl`
- `run_20260918_192439_aafca3/outputs/resource_profile.json`
- `run_20260918_192439_aafca3/outputs/validation_postprocessing/index.json`
- `run_20260918_192439_aafca3/outputs/prediction_samples/samples.json`
- `run_20260918_152331_c80150/outputs/best_metrics.json` and `/history/research-notes/abi346-temporal-eligible-failure-bucket-review.md` for ABI-346 comparison context
- `run_20260914_124245_de843c/outputs/best_metrics.json` and `/history/research-notes/abi306-temporal-eligible-failure-bucket-review.md` for ABI-306 comparison context
- `run_20260916_184108_954ec7/outputs/best_metrics.json` and `/history/research-notes/abi324-temporal-eligible-failure-bucket-review.md` for ABI-324 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` and `/history/research-notes/abi223-temporal-eligible-failure-bucket-review.md` for ABI-223 comparison context
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
