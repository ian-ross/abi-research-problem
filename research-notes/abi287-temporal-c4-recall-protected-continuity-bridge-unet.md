# ABI-287 temporal C4 recall-protected continuity bridge U-Net

research-figures: []

## Scope

This note records ABI-287, Candidate `abi287_temporal_c4_recall_protected_continuity_bridge_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260913_133037_6bd482`.

ABI-287 is a mechanism-changing temporal-family continuation after ABI-286. ABI-286 showed that decoder-resolution continuity evidence can improve connected-line organization relative to the 12-epoch ABI-284 temporal C4 parent, but the bridge traded away too much ABI-285-style recall and source balance. ABI-287 kept the provider-owned `abi_16ch_plus_sza_temporal` input path, offsets `[-1, 0, 1]`, trusted `temporal_eligible_center` selection, temporal attention/change stem, early C4 orientation line state, encoder-scale line-state injection, ASPP bottleneck, high-resolution directional decoder context, and trusted Line plus Centerline auxiliary outputs. Its specific change was a recall-protected full-resolution continuity sidecar: appearance decoder features remain the primary mask path, line-state continuity is added only as a bounded residual, and a small non-negative line-evidence lift is initialized near zero.

The Candidate consumed only provider-owned temporal ABI/Solar Geometry Input tensors. It used source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, temporal lookup, frame repair/padding, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to the full Working Validation Split frontier.

## Execution result

ABI-287 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal` with 51 input channels.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-1, 0, 1]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 4,328,348, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 7.18 / 7.57 GiB.
- Training wall time: 1,917.3 s; validation wall time: 1,130.3 s; total Run wall time: 3,049.6 s, within the exploratory timeout.
- Best checkpoint selected by `val/filtered_dice` at epoch 11.

## Best-validation metrics

| Metric | ABI-287 best epoch 11 | ABI-287 final epoch 12 | ABI-286 continuity bridge | ABI-284 temporal C4 exploratory | ABI-285 temporal C4 late36 | ABI-274 temporal line-state late36 | ABI-223 temporal attention late36 | ABI-238 temporal directional-context late36 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.386937 | 0.354123 | 0.393183 | 0.390090 | 0.422195 | 0.419364 | 0.419776 | 0.420235 |
| Raw Dice | 0.403084 | 0.370534 | 0.409514 | 0.408012 | 0.439439 | 0.436760 | 0.438487 | 0.438718 |
| Filtered precision | 0.425221 | 0.443798 | 0.419944 | 0.475285 | 0.448400 | 0.454127 | 0.483764 | 0.488730 |
| Filtered recall | 0.354978 | 0.294597 | 0.369628 | 0.330796 | 0.398883 | 0.389545 | 0.370738 | 0.368578 |
| Filtered connectivity | 0.222259 | 0.224674 | 0.280479 | 0.254710 | 0.243387 | 0.282911 | 0.412427 | 0.352239 |
| MIT filtered Dice | 0.372922 | 0.338499 | 0.381112 | 0.371847 | 0.400831 | 0.399386 | 0.398498 | 0.405383 |
| Google filtered Dice | 0.422601 | 0.394124 | 0.424115 | 0.436956 | 0.477410 | 0.472606 | 0.476764 | 0.460838 |
| Filtered predicted-positive fraction | 0.004316 | 0.003432 | 0.004550 | 0.003598 | 0.004599 | 0.004434 | 0.003962 | 0.003899 |
| Filtered predicted-positive pixels | 456,483 | 363,001 | 481,295 | 380,578 | 486,427 | 469,049 | 419,056 | 412,381 |

ABI-287 did not repair ABI-286. Relative to ABI-286's best checkpoint, ABI-287's selected checkpoint is lower on filtered Dice (-0.0062), recall (-0.0147), MIT Dice (-0.0082), Google Dice (-0.0015), and connectivity (-0.0582), with only a small precision increase (+0.0053). Relative to ABI-284, it is lower on aggregate filtered Dice (-0.0032) and connectivity (-0.0325), though it has modestly higher recall (+0.0242) and almost equal MIT Dice (+0.0011). Relative to ABI-285 and ABI-274/223/238 temporal comparators, ABI-287 remains well below the temporal-eligible frontier on both aggregate Dice and connected-line continuity.

The intended non-suppressive evidence lift avoided broad all-positive clutter: selected filtered predicted-positive fraction was 0.004316, similar to ABI-286/285/274 and only slightly above ABI-223/238. However, the recall protection was not strong enough to recover ABI-286's best recall, and the continuity sidecar weakened rather than preserved connected-line evidence.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.204939 | 0.217255 | 0.181686 | 0.171797 | 0.253925 | 0.127137 | 0.007641 |
| 2 | 0.221243 | 0.204815 | 0.265945 | 0.472635 | 0.144424 | 0.407817 | 0.001580 |
| 3 | 0.315815 | 0.308306 | 0.332455 | 0.325374 | 0.306802 | 0.203947 | 0.004875 |
| 4 | 0.323942 | 0.306614 | 0.366824 | 0.434909 | 0.258091 | 0.267075 | 0.003068 |
| 5 | 0.335154 | 0.315945 | 0.384517 | 0.480694 | 0.257262 | 0.275074 | 0.002767 |
| 6 | 0.363061 | 0.348381 | 0.400557 | 0.403940 | 0.329695 | 0.249726 | 0.004219 |
| 7 | 0.339584 | 0.318011 | 0.395753 | 0.486759 | 0.260746 | 0.334117 | 0.002769 |
| 8 | 0.376998 | 0.361594 | 0.419188 | 0.470681 | 0.314417 | 0.359246 | 0.003453 |
| 9 | 0.377461 | 0.368580 | 0.400054 | 0.373568 | 0.381436 | 0.203972 | 0.005278 |
| 10 | 0.380190 | 0.369140 | 0.408402 | 0.397159 | 0.364612 | 0.231776 | 0.004746 |
| 11 | 0.386937 | 0.372922 | 0.422601 | 0.425221 | 0.354978 | 0.222259 | 0.004316 |
| 12 | 0.354123 | 0.338499 | 0.394124 | 0.443798 | 0.294597 | 0.224674 | 0.003432 |

The run is finite, non-collapsed, and source-informative, but the trajectory is not late-improving in the useful sense. Aggregate Dice rises through epoch 11, then drops sharply at epoch 12 while train loss continues decreasing. The best-recall epoch is epoch 9, but it has weaker connectivity and lower Dice than epoch 11. Connectivity spikes at epochs 2, 7, and 8, but those states do not coincide with the selected aggregate-Dice optimum and do not remain stable. Epoch 12 shifts toward a more compact, lower-recall prediction state without gaining meaningful continuity.

Raw-to-filtered differences are modest and conservative at the selected checkpoint: raw Dice 0.4031 versus filtered Dice 0.3869, and raw predicted-positive pixels 492,783 versus filtered predicted-positive pixels 456,483. Artifact Filters lower rather than create the selected Result.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.2650, 0.3684, 0.6116, and 0.3420. They are consistent with finite non-collapsed predictions and one strong retained example, but lower than ABI-286's corresponding first-four sample Dice values on three of four samples and do not support promotion or diagnostics by themselves.

## Interpretation

Classify ABI-287 as a finite, resource-safe, negative mechanism test for the recall-protected continuity-sidecar variant. The sidecar did not recover ABI-285-style recall/source balance, did not improve on ABI-286's best recall or connectivity, and did not beat the immediate ABI-284 exploratory parent on aggregate Dice. Its main useful evidence is that simply making the continuity bridge less suppressive and adding a small non-negative line-evidence lift is insufficient; in this implementation, the architecture still fails to align recall and connected-line support at the fixed 0.5 threshold.

The branch should not receive an unchanged late36 continuation. Although the selected checkpoint is near the end of the exploratory budget, the final epoch regresses sharply and the mechanism is already below ABI-286 on the targeted repair dimensions. Future temporal work should change mechanism rather than repeat this variant: for example, use temporal attention/change sharpening that keeps line evidence separate from mask evidence until late logits, a less C4-heavy center-detail temporal branch, or explicit dual-path recall/continuity heads whose evidence is merged without thresholding, postprocessing, custom losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, or resource scheduling.

## Decision

Do not promote ABI-287. Do not request whole-validation or temporal-eligible failure-bucket diagnostics for this capped temporal-eligible result. Do not request a late-improving continuation of the unchanged ABI-287 branch. Treat the ABI-287 mechanism as a characterized negative continuation after ABI-286 and broaden the next temporal-family hypothesis or switch families rather than spending another Run on the same recall-protected continuity sidecar.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260913_133037_6bd482/candidate/PROPOSAL.md`
- `run_20260913_133037_6bd482/candidate/README.md`
- `run_20260913_133037_6bd482/candidate/manifest.yaml`
- `run_20260913_133037_6bd482/resolved_manifest.yaml`
- `run_20260913_133037_6bd482/execution.json`
- `run_20260913_133037_6bd482/outputs/model_summary.json`
- `run_20260913_133037_6bd482/outputs/best_metrics.json`
- `run_20260913_133037_6bd482/outputs/final_metrics.json`
- `run_20260913_133037_6bd482/outputs/metrics.jsonl`
- `run_20260913_133037_6bd482/outputs/resource_profile.json`
- `run_20260913_133037_6bd482/outputs/validation_postprocessing/index.json`
- `run_20260913_133037_6bd482/outputs/prediction_samples/samples.json`
- `run_20260913_123056_4152f3/outputs/best_metrics.json` for ABI-286 continuity-bridge comparison context
- `run_20260913_091156_167372/outputs/best_metrics.json` for ABI-284 temporal C4 exploratory comparison context
- `run_20260913_100333_a250df/outputs/best_metrics.json` for ABI-285 temporal C4 late36 comparison context
- `run_20260912_180856_79ba22/outputs/best_metrics.json` for ABI-274 temporal line-state late36 comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention late36 comparison context
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 temporal directional-context late36 comparison context
- `/history/research-notes/abi285-temporal-eligible-failure-bucket-review.md`
- `/history/research-notes/abi286-temporal-c4-continuity-evidence-bridge-unet.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
