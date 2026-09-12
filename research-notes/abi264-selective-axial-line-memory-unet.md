# ABI-264 selective axial line-memory U-Net

research-figures: []

## Scope

This note records the exploratory Result for ABI-264, Candidate `abi264_fullspectral_btd_sza_selective_axial_line_memory_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260912_055445_9221de`.

ABI-264 was a bounded single-frame family scout for a compact state-space-style line-continuity mechanism. It consumed only provider-owned `abi_16ch_plus_sza` inputs, used source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, batch size 4, constant learning rate, and trusted Line/Centerline auxiliary outputs. The mechanism change was `SelectiveAxialLineMemory`: gated differentiable prefix-average feature states along rows and columns at multiple U-Net scales, fused with local line convolutions and signed-detail evidence.

Candidate code remained architecture-only and did not implement data loading, split logic, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, temporal lookup, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Execution result

ABI-264 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 5,017,094, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 17.42 / 18.93 GB.
- Training wall time: 1,633.5 s; validation wall time: 1,411.5 s; total Run wall time: 3,047.1 s.

This is valid finite/resource evidence for selective axial line-memory on the capped representative validation population. It is not whole-validation promotion evidence.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was the final exploratory epoch 12.

| Metric | ABI-264 epoch 12 | ABI-262 overlap SegFormer | ABI-263 directional SegFormer | ABI-260 compact MaxViT | ABI-253 line-memory U-NetFormer | ABI-249 C4 line-context | ABI-202 frontier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.407091 | 0.396950 | 0.379436 | 0.381455 | 0.408323 | 0.416400 | 0.427570 |
| Raw Dice | 0.421174 | 0.410777 | 0.392687 | 0.394386 | 0.423530 | 0.432320 | 0.442746 |
| Filtered precision | 0.399434 | 0.400782 | 0.378366 | 0.408841 | 0.444837 | 0.480886 | 0.439467 |
| Filtered recall | 0.415047 | 0.393191 | 0.380513 | 0.357507 | 0.377349 | 0.367165 | 0.416301 |
| Filtered connectivity | 0.410422 | 0.231960 | 0.274668 | 0.326157 | 0.326698 | 0.392524 | 0.457773 |
| MIT filtered Dice | 0.398792 | 0.388968 | 0.373046 | 0.365482 | 0.394406 | 0.396436 | 0.411992 |
| Google filtered Dice | 0.428117 | 0.416932 | 0.394107 | 0.419710 | 0.442587 | 0.468855 | 0.468151 |
| Filtered predicted-positive fraction | 0.003765 | 0.003555 | 0.003644 | 0.003115 | 0.003074 | 0.002767 | 0.003433 |

ABI-264 is a positive broad-scout Result. Relative to ABI-262 it improved filtered Dice by about +0.0101, recall by +0.0219, connectivity by +0.1785, MIT Dice by +0.0098, and Google Dice by +0.0112 with essentially unchanged precision. Relative to ABI-263 it improved every listed metric except resource cost remains in the same high-memory class. Relative to ABI-260 it improved Dice by +0.0256 and connectivity by +0.0843, with lower precision but substantially higher recall.

ABI-264 is roughly tied with ABI-253 on aggregate capped Dice, but has higher recall (+0.0377), higher connectivity (+0.0837), and slightly higher MIT Dice, while ABI-253 remains stronger on precision and Google Dice. ABI-264 is still below the mature ABI-249/ABI-202 aggregate frontier, especially on precision and Google source Dice, but its connectivity already exceeds ABI-249's capped best and is close to ABI-202 recall.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.217656 | 0.224156 | 0.205027 | 0.206481 | 0.230110 | 0.124173 | 0.004038 |
| 2 | 0.275155 | 0.279865 | 0.265959 | 0.271065 | 0.279370 | 0.153424 | 0.003735 |
| 3 | 0.294406 | 0.302015 | 0.279558 | 0.251176 | 0.355610 | 0.152209 | 0.005130 |
| 4 | 0.313439 | 0.313176 | 0.313989 | 0.279969 | 0.355998 | 0.171605 | 0.004608 |
| 5 | 0.316082 | 0.296205 | 0.362248 | 0.402417 | 0.260249 | 0.313482 | 0.002343 |
| 6 | 0.348115 | 0.359788 | 0.324474 | 0.306745 | 0.402383 | 0.191061 | 0.004753 |
| 7 | 0.342681 | 0.346373 | 0.334976 | 0.300987 | 0.397784 | 0.165283 | 0.004789 |
| 8 | 0.353977 | 0.340604 | 0.385429 | 0.422800 | 0.304423 | 0.270307 | 0.002609 |
| 9 | 0.362896 | 0.348622 | 0.397305 | 0.395260 | 0.335431 | 0.242510 | 0.003075 |
| 10 | 0.310565 | 0.318101 | 0.296480 | 0.283710 | 0.343035 | 0.172647 | 0.004381 |
| 11 | 0.376867 | 0.377899 | 0.374430 | 0.340395 | 0.422091 | 0.205670 | 0.004493 |
| 12 | 0.407091 | 0.398792 | 0.428117 | 0.399434 | 0.415047 | 0.410422 | 0.003765 |

The trajectory is finite, non-collapsed, and source-informative. It is also unusually late-improving: the best aggregate Dice, raw Dice, connectivity, MIT Dice, and Google Dice all occur at the final epoch. Epoch 10 is a transient regression rather than a plateau; epochs 11-12 recover sharply, and epoch 12 combines high recall with the first strong connectivity value for this branch.

The late jump means ABI-264 should not be treated as a completed final verdict on selective axial line-memory. Under the current budget policy, the run has the evidence pattern that can justify a close-continuation or late-improving request: final-epoch best checkpoint, finite/nondegenerate predictions, both Dataset Sources informative, and an improving rather than plateaued trajectory.

## Interpretation

Classify ABI-264 as a promising positive scout for low-cost architecture-internal line-memory. It validates the core idea better than the recent overlap-attention and MaxViT broad scouts: long row/column feature state can improve continuity and recall without Candidate-owned morphology, thresholding, postprocessing, or Artifact Filtering.

The main weakness is not collapse but calibration/precision and Google-source gap relative to ABI-249/ABI-202. ABI-264 predicts a somewhat larger positive fraction than ABI-249/ABI-202, which is consistent with its high recall and lower precision. The mechanism therefore appears recall/connectivity-favorable and may need a precision-preserving continuation rather than a wholesale branch stop.

Resource behavior is acceptable under the active A100 exploratory ceiling, but the activation footprint is still high: memory is only modestly below ABI-263 and higher than ABI-262/260. Future variants should avoid simply adding more high-resolution state blocks unless the goal is an explicitly justified late-improving close continuation.

## Decision

Do not promote ABI-264 from capped exploratory evidence, and do not request whole-validation diagnostics before one more bounded development step.

Continue the selective axial line-memory family. The preferred next hypothesis is a close ABI-264 continuation that preserves the successful axial memory core while improving precision/calibration or extending training under the approved `late_improving` budget if the Harness accepts the final-epoch improvement evidence. A safe continuation should remain in-contract: provider-owned `abi_16ch_plus_sza`, no coordinates, no Candidate-owned sampling/loss/metric/Artifact Filter/postprocessing, and no resource scheduling logic.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_055445_9221de/candidate/PROPOSAL.md`
- `run_20260912_055445_9221de/candidate/README.md`
- `run_20260912_055445_9221de/candidate/manifest.yaml`
- `run_20260912_055445_9221de/resolved_manifest.yaml`
- `run_20260912_055445_9221de/outputs/model_summary.json`
- `run_20260912_055445_9221de/outputs/best_metrics.json`
- `run_20260912_055445_9221de/outputs/final_metrics.json`
- `run_20260912_055445_9221de/outputs/metrics.jsonl`
- `run_20260912_055445_9221de/outputs/resource_profile.json`
- `run_20260912_055445_9221de/outputs/validation_postprocessing/index.json`
- `run_20260912_055445_9221de/outputs/prediction_samples/samples.json`
- `run_20260912_040526_92961f` for ABI-262 overlap SegFormer comparator context
- `run_20260912_045029_55c59e` for ABI-263 directional SegFormer comparator context
- `run_20260912_021616_d20946` for ABI-260 compact MaxViT comparator context
- `run_20260911_171333_f0b603` for ABI-253 line-memory U-NetFormer comparator context
- `run_20260911_111909_dd7ef7` for ABI-249 C4 steerable line-context comparator context
- `run_20260904_043143_ee0005` for ABI-202 current aggregate whole-validation frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
