# ABI-262 overlap SegFormer line decoder

research-figures: []

## Scope

This note records the exploratory Result for ABI-262, Candidate `abi262_fullspectral_btd_sza_overlap_segformer_line_decoder_bce_dice_line_centerline_aux_v1`, Run `run_20260912_040526_92961f`.

ABI-262 was a compact SegFormer/MiT-style modern-backbone family scout. It tested whether overlap patch embeddings, spatial-reduction attention, a high-resolution signed-detail bridge, and a line-aware decoder could improve patch-scale cloud context and thin Contrail Mask evidence relative to the ABI-260 compact MaxViT scout and the recent ABI-253 line-memory U-NetFormer branch. It used provider-owned `abi_16ch_plus_sza` inputs, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, batch size 4, constant learning rate, and trusted Line/Centerline auxiliary targets.

Candidate code remained architecture-only and did not implement data loading, split logic, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, temporal lookup, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Execution result

ABI-262 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 1,727,689, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 9.69 / 10.65 GB.
- Training wall time: 1,001.5 s; validation wall time: 1,231.5 s; total Run wall time: 2,234.6 s.

This is valid finite/resource evidence for a compact overlap-attention SegFormer-like single-frame family on the capped representative validation population. It is not whole-validation promotion evidence.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was the final exploratory epoch 12.

| Metric | ABI-262 best/final epoch 12 | ABI-260 MaxViT scout | ABI-253 line-memory U-NetFormer | ABI-249 C4 steerable line-context | ABI-202 whole-val frontier |
| --- | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.396950 | 0.381455 | 0.408323 | 0.416400 | 0.427570 |
| Raw Dice | 0.410777 | 0.395228 | 0.423530 | 0.432320 | 0.442746 |
| Filtered precision | 0.400782 | 0.408841 | 0.444837 | 0.480886 | 0.439467 |
| Filtered recall | 0.393191 | 0.357507 | 0.377349 | 0.367165 | 0.416301 |
| Filtered connectivity | 0.231960 | 0.326157 | 0.326698 | 0.392524 | 0.457773 |
| MIT filtered Dice | 0.388968 | 0.365482 | 0.394406 | 0.396436 | 0.411992 |
| Google filtered Dice | 0.416932 | 0.419710 | 0.442587 | 0.468855 | 0.468151 |
| Filtered predicted-positive fraction | 0.003555 | 0.003169 | 0.003074 | 0.002767 | 0.003433 |

Relative to ABI-260, ABI-262 improves filtered Dice by about +0.0155, recall by about +0.0357, and MIT filtered Dice by about +0.0235, with only a small precision decrease. However, it loses about -0.0942 connectivity and is slightly lower on Google filtered Dice. Relative to ABI-253, ABI-262 is lower by about -0.0114 filtered Dice, -0.0441 precision, -0.0947 connectivity, -0.0054 MIT Dice, and -0.0257 Google Dice, while improving recall by about +0.0158. Relative to ABI-249 and ABI-202, ABI-262 remains clearly behind on aggregate Dice, source-stratified Dice, precision, and especially connectivity.

The scout therefore delivered the intended recall and MIT-overlap improvement over ABI-260, but did not preserve the line-continuity strength expected from the line-aware decoder.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.207754 | 0.223817 | 0.179521 | 0.187040 | 0.233628 | 0.124940 | 0.004526 |
| 2 | 0.233530 | 0.248038 | 0.209568 | 0.191431 | 0.299365 | 0.113426 | 0.005667 |
| 3 | 0.290840 | 0.297640 | 0.278499 | 0.258341 | 0.332693 | 0.134827 | 0.004667 |
| 4 | 0.300484 | 0.303468 | 0.294926 | 0.276670 | 0.328784 | 0.152091 | 0.004306 |
| 5 | 0.323218 | 0.304758 | 0.364540 | 0.411085 | 0.266298 | 0.312310 | 0.002347 |
| 6 | 0.352426 | 0.345368 | 0.368499 | 0.366847 | 0.339095 | 0.290119 | 0.003350 |
| 7 | 0.365173 | 0.355263 | 0.387957 | 0.401856 | 0.334627 | 0.281380 | 0.003017 |
| 8 | 0.350668 | 0.353551 | 0.344722 | 0.347473 | 0.353922 | 0.187748 | 0.003691 |
| 9 | 0.392013 | 0.380292 | 0.420999 | 0.433306 | 0.357906 | 0.277975 | 0.002993 |
| 10 | 0.322977 | 0.318489 | 0.331664 | 0.313341 | 0.333225 | 0.202315 | 0.003854 |
| 11 | 0.378243 | 0.382902 | 0.367878 | 0.334601 | 0.434978 | 0.180971 | 0.004711 |
| 12 | 0.396950 | 0.388968 | 0.416932 | 0.400782 | 0.393191 | 0.231960 | 0.003555 |

The trajectory is finite, source-informative, and non-collapsed. It has noisy mid-run behavior, including a large dip at epoch 10, but recovers to the best aggregate checkpoint at epoch 12. The final-epoch best is a genuine late-improvement signal for aggregate filtered Dice and MIT Dice. Connectivity behaves differently: it peaks at epoch 5, stays useful at epochs 6-7 and 9, and then falls well below ABI-260/ABI-253 by the selected checkpoint. Epoch 11 has the highest recall, but with weaker precision, larger predicted-positive fraction, and poor connectivity.

## Interpretation

Classify ABI-262 as a mixed but useful first SegFormer-style scout. The positive evidence is that overlap attention is contract-compliant, resource-safe, finite, compact, and better than ABI-260 on capped filtered Dice, recall, and MIT filtered Dice. It also reaches a stronger final-epoch filtered-Dice band than the first MaxViT scout while using fewer parameters and less wall time.

The negative evidence is that ABI-262 does not yet clear the stronger ABI-253 modern-backbone comparator, does not approach the ABI-249/ABI-202 frontier, and fails the intended connectivity improvement. The selected checkpoint appears to raise area recall more than connected thin-line structure. Because this is an early modern-backbone family scout with a final-epoch best and clear improvement over ABI-260, low score versus the mature frontier is not by itself a hard stop for SegFormer-like overlap attention. The exact decoder/line-continuity mechanism, however, should not be repeated unchanged.

## Decision

Do not promote ABI-262. Do not request whole-validation diagnostics yet: the capped score is below ABI-253/ABI-249/ABI-202 and the connectivity deficit is already clear.

Keep one bounded SegFormer-family continuation eligible if the next hypothesis changes the mechanism toward connectivity preservation rather than merely adding epochs. A plausible follow-up would retain the resource-efficient overlap-attention encoder but revise the decoder to preserve high-resolution line state or add an architecture-internal directional/centerline consistency path that does not implement Candidate-owned thresholding, postprocessing, losses, metrics, Artifact Filters, target derivation, data loading, coordinates, or resource scheduling. If the campaign instead broadens, prefer another underexplored mechanism such as temporal change/calibration or rotation-aware line accumulation.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_040526_92961f/candidate/PROPOSAL.md`
- `run_20260912_040526_92961f/candidate/README.md`
- `run_20260912_040526_92961f/candidate/manifest.yaml`
- `run_20260912_040526_92961f/resolved_manifest.yaml`
- `run_20260912_040526_92961f/outputs/model_summary.json`
- `run_20260912_040526_92961f/outputs/best_metrics.json`
- `run_20260912_040526_92961f/outputs/final_metrics.json`
- `run_20260912_040526_92961f/outputs/metrics.jsonl`
- `run_20260912_040526_92961f/outputs/resource_profile.json`
- `run_20260912_040526_92961f/outputs/validation_postprocessing/index.json`
- `run_20260912_040526_92961f/outputs/prediction_samples/samples.json`
- `run_20260912_021616_d20946` for ABI-260 compact MaxViT comparator context
- `run_20260911_171333_f0b603` for ABI-253 line-memory U-NetFormer comparator context
- `run_20260911_111909_dd7ef7` for ABI-249 C4 steerable line-context comparator context
- `run_20260904_043143_ee0005` for ABI-202 current aggregate whole-validation frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
