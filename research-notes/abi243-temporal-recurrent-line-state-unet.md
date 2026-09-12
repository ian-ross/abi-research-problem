# ABI-243 temporal recurrent line-state U-Net

research-figures: []

## Scope

This note records the bounded exploratory Result for ABI-243, Candidate `abi243_temporal_recurrent_line_state_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260911_063601_913208`.

ABI-243 tested whether adding an oriented, full-resolution line-state pyramid to ABI-242's compact recurrent temporal stem could improve continuity without losing source-informative temporal overlap/recall. The Candidate consumed provider-owned `abi_16ch_plus_sza_temporal` tensors with offsets `[-1, 0, 1]`, `temporal_eligible_center` frame selection, source-balanced sampling, trusted random mirroring, BCE-Dice loss, AdamW with constant learning rate, batch size 2, and trusted Line/Centerline auxiliary outputs. Candidate code remained architecture-only and did not implement temporal lookup, cache reads, data loading, missing-frame repair, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, or resource scheduling.

## Execution result

ABI-243 completed the 12-epoch exploratory budget without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from the Run artifacts:

- Status: completed.
- Budget request: exploratory default; no late-improving budget requested.
- Input mode: `abi_16ch_plus_sza_temporal` with three provider-supplied ABI+SZA frames.
- Temporal offsets: `[-1, 0, 1]`; target frame offset `0`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after provider-owned temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 5,046,651, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 4.79 / 5.15 GiB.
- Training wall time: 1,449.0 s; validation wall time: 1,112.2 s; total Run wall time: 2,563.0 s.

This is successful finite/resource evidence for the oriented line-state recurrent temporal branch. Resource use stayed well inside the trusted memory and exploratory timeout ceilings.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 11, not the final epoch 12.

| Metric | ABI-243 best epoch 11 | ABI-243 final epoch 12 |
| --- | ---: | ---: |
| Filtered Dice | 0.382393 | 0.350496 |
| Raw Dice | 0.397046 | 0.366056 |
| Filtered IoU | 0.236394 | 0.212486 |
| Filtered precision | 0.374530 | 0.414783 |
| Filtered recall | 0.390593 | 0.303463 |
| Filtered contrail connectivity | 0.185217 | 0.229998 |
| Filtered predicted-positive fraction | 0.005391 | 0.003782 |
| Raw predicted-positive fraction | 0.005809 | 0.004066 |
| MIT filtered Dice | 0.377394 | 0.328768 |
| Google filtered Dice | 0.394677 | 0.404453 |
| MIT filtered recall | 0.366078 | 0.271135 |
| Google filtered recall | 0.463531 | 0.399644 |
| Train loss | 0.815859 | 0.795507 |
| Validation loss | 0.857316 | 0.870940 |

The selected checkpoint is finite, noncollapsed, and source-informative. It keeps nontrivial filtered Dice and recall on both MIT and Google. However, the intended continuity mechanism did not succeed at the selected checkpoint: filtered connectivity is 0.185217, below ABI-242's 0.201293 and ABI-241's 0.238980. Final epoch connectivity is higher, but it comes with a large drop in filtered Dice and recall.

## Learning trajectory

| Epoch | Filtered Dice | Raw Dice | Filtered precision | Filtered recall | MIT filtered Dice | Google filtered Dice | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.209342 | 0.218571 | 0.263532 | 0.173637 | 0.203382 | 0.222717 | 0.124946 | 0.003406 |
| 2 | 0.206271 | 0.214191 | 0.213485 | 0.199529 | 0.198071 | 0.222627 | 0.112443 | 0.004832 |
| 3 | 0.294785 | 0.308707 | 0.371693 | 0.244247 | 0.278258 | 0.333424 | 0.245979 | 0.003397 |
| 4 | 0.275127 | 0.287226 | 0.336846 | 0.232522 | 0.259613 | 0.310374 | 0.154416 | 0.003569 |
| 5 | 0.348259 | 0.362597 | 0.379546 | 0.321738 | 0.338098 | 0.372530 | 0.181958 | 0.004382 |
| 6 | 0.336546 | 0.351812 | 0.406570 | 0.287099 | 0.317185 | 0.383167 | 0.172443 | 0.003650 |
| 7 | 0.256351 | 0.271134 | 0.553892 | 0.166767 | 0.234513 | 0.314215 | 0.321163 | 0.001556 |
| 8 | 0.370944 | 0.388296 | 0.466492 | 0.307883 | 0.356035 | 0.409657 | 0.229448 | 0.003412 |
| 9 | 0.374011 | 0.387575 | 0.346730 | 0.405951 | 0.361065 | 0.405031 | 0.196715 | 0.006053 |
| 10 | 0.379442 | 0.394997 | 0.412217 | 0.351496 | 0.358431 | 0.432219 | 0.271735 | 0.004408 |
| 11 | 0.382393 | 0.397046 | 0.374530 | 0.390593 | 0.377394 | 0.394677 | 0.185217 | 0.005391 |
| 12 | 0.350496 | 0.366056 | 0.414783 | 0.303463 | 0.328768 | 0.404453 | 0.229998 | 0.003782 |

The trajectory is noisy rather than cleanly late-improving. Filtered Dice rises through epoch 11, while train loss continues to improve through epoch 12; validation loss and filtered Dice then regress at the final epoch. Connectivity has several disconnected local peaks, including epoch 7 and epoch 10, but these do not align with the selected overlap/recall checkpoint. This mismatch suggests that the line-state branch can affect predicted structure but is not coherently coupled to the segmentation objective at the checkpoint selected by filtered Dice.

## Comparison context

| Metric | ABI-243 line-state recurrent | ABI-242 recurrent change-state | ABI-241 high-res change skip | ABI-240 line-accum late36 | ABI-238 temporal directional late36 | ABI-223 temporal attention late36 | ABI-202 single-frame frontier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Run | `run_20260911_063601_913208` | `run_20260911_055200_52c75f` | `run_20260911_050449_17cdcb` | `run_20260911_031326_43ed12` | `run_20260911_004137_f54c45` | `run_20260908_154531_8c7e2b` | `run_20260904_043143_ee0005` |
| Best epoch | 11 | 12 | 11 | 29 | 29 | 36 | 34 |
| Filtered Dice | 0.382393 | 0.376521 | 0.384180 | 0.414892 | 0.420235 | 0.419776 | 0.427570 |
| Raw Dice | 0.397046 | 0.391788 | 0.399916 | 0.431959 | 0.438718 | 0.438487 | 0.442746 |
| Filtered precision | 0.374530 | 0.384767 | 0.400177 | 0.436241 | 0.488730 | 0.483764 | 0.439467 |
| Filtered recall | 0.390593 | 0.368620 | 0.369412 | 0.395534 | 0.368578 | 0.370738 | 0.416301 |
| Filtered connectivity | 0.185217 | 0.201293 | 0.238980 | 0.264863 | 0.352239 | 0.412427 | 0.457773 |
| MIT filtered Dice | 0.377394 | 0.367296 | 0.377453 | 0.397067 | 0.405383 | 0.398498 | 0.411992 |
| Google filtered Dice | 0.394677 | 0.398964 | 0.401490 | 0.460659 | 0.460838 | 0.476764 | 0.468151 |
| Filtered predicted-positive fraction | 0.005391 | 0.004953 | 0.004772 | 0.004687 | 0.003899 | 0.003962 | 0.003433 |

ABI-243 improves ABI-242's selected filtered Dice by +0.005872 and filtered recall by +0.021973, but loses precision by -0.010237, increases predicted-positive fraction, and reduces connectivity by -0.016076. Relative to ABI-241, ABI-243 is nearly tied on filtered Dice (-0.001787) but has lower precision, larger predicted-positive area, and much lower connectivity (-0.053763). Relative to ABI-240/238/223 and the ABI-202 single-frame frontier, ABI-243 remains well behind on filtered Dice, precision, source-stratified Google Dice, and especially connectivity.

## Interpretation

Classify ABI-243 as a finite, nondegenerate but scientifically weak family-development Result. It partially preserves ABI-242's late-overlap signal and improves recall, so it is not a collapse or resource failure. But the central hypothesis was continuity recovery, and selected-checkpoint connectivity moved in the wrong direction. The branch's higher recall appears to come from a larger predicted-positive fraction and lower precision, not from cleaner connected thin-line segmentation.

This result does not eliminate temporal recurrent modeling as a broader family: ABI-242 and ABI-243 both show source-informative temporal learning under capped evidence. It does weaken the exact full-resolution oriented line-state skip-gating mechanism. The failure mode is not lack of trainability; it is objective/selection mismatch and fragmented or over-broad positives at the best filtered-Dice operating point.

## Decision

Do not promote ABI-243 and do not request whole-validation diagnostics from this capped Result alone. Do not request a late36 continuation of this exact line-state coupling: the best checkpoint is not the final epoch, final validation regresses, and the continuity criterion is not met.

Stop the exact ABI-243 oriented line-state recurrent branch. Continue broadening within temporal modeling only through a materially different mechanism, such as a modern lightweight temporal backbone, a five-frame recurrent/attention model with explicit high-resolution continuity preservation, or a calibration/selection-aware architecture that avoids trading connectivity for larger predicted-positive area. Any next Candidate should be a sequential scout or a tightly justified one-factor continuation, not an unchanged budget extension.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260911_063601_913208/candidate/PROPOSAL.md`
- `run_20260911_063601_913208/candidate/README.md`
- `run_20260911_063601_913208/candidate/manifest.yaml`
- `run_20260911_063601_913208/resolved_manifest.yaml`
- `run_20260911_063601_913208/outputs/model_summary.json`
- `run_20260911_063601_913208/outputs/best_metrics.json`
- `run_20260911_063601_913208/outputs/final_metrics.json`
- `run_20260911_063601_913208/outputs/metrics.jsonl`
- `run_20260911_063601_913208/outputs/resource_profile.json`
- `run_20260911_063601_913208/outputs/validation_postprocessing/index.json`
- `run_20260911_063601_913208/outputs/prediction_samples/samples.json`
- `run_20260911_055200_52c75f` for ABI-242 recurrent temporal change-state context
- `run_20260911_050449_17cdcb` for ABI-241 high-resolution temporal change-skip context
- `run_20260911_031326_43ed12` for ABI-240 temporal line-accumulator late36 context
- `run_20260911_004137_f54c45` for ABI-238 temporal directional-context late36 context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention late36 context
- `run_20260904_043143_ee0005` for ABI-202 single-frame frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
