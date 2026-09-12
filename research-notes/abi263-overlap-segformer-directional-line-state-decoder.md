# ABI-263 overlap SegFormer directional line-state decoder

research-figures: []

## Scope

This note records the exploratory Result for ABI-263, Candidate `abi263_fullspectral_btd_sza_overlap_segformer_directional_line_state_decoder_bce_dice_line_centerline_aux_v1`, Run `run_20260912_045029_55c59e`.

ABI-263 was a SegFormer-family continuation after ABI-262. It kept provider-owned `abi_16ch_plus_sza` inputs, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, batch size 4, constant learning rate, and trusted Line/Centerline auxiliary outputs. The mechanism change was a high-resolution directional line-state decoder intended to preserve connected thin-line structure while retaining ABI-262's overlap-attention recall behavior.

Candidate code remained architecture-only and did not implement data loading, split logic, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, temporal lookup, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Execution result

ABI-263 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Input mode: `abi_16ch_plus_sza`.
- Effective frame-selection policy: `all_target_frames`.
- Sample counts after capped-record selection: 2,048 train and 2,048 validation ABI Patches.
- Parameter count: 2,321,214, below the 25,000,000-parameter ceiling.
- Batch size: 4.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 18.32 / 19.18 GB.
- Training wall time: 1,779.5 s; validation wall time: 1,523.7 s; total Run wall time: 3,305.0 s.

This is valid finite/resource evidence for the compact overlap-attention SegFormer plus directional line-state decoder on the capped representative validation population. It is not whole-validation promotion evidence.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 8; the final epoch 12 regressed.

| Metric | ABI-263 best epoch 8 | ABI-263 final epoch 12 | ABI-262 parent | ABI-253 line-memory U-NetFormer | ABI-249 C4 steerable line-context | ABI-202 whole-val frontier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.379436 | 0.365631 | 0.396950 | 0.408323 | 0.416400 | 0.427570 |
| Raw Dice | 0.392687 | 0.380272 | 0.410777 | 0.423530 | 0.432320 | 0.442746 |
| Filtered precision | 0.378366 | 0.417973 | 0.400782 | 0.444837 | 0.480886 | 0.439467 |
| Filtered recall | 0.380513 | 0.324939 | 0.393191 | 0.377349 | 0.367165 | 0.416301 |
| Filtered connectivity | 0.274668 | 0.214166 | 0.231960 | 0.326698 | 0.392524 | 0.457773 |
| MIT filtered Dice | 0.373046 | 0.351120 | 0.388968 | 0.394406 | 0.396436 | 0.411992 |
| Google filtered Dice | 0.394107 | 0.399927 | 0.416932 | 0.442587 | 0.468855 | 0.468151 |
| Filtered predicted-positive fraction | 0.003644 | 0.002817 | 0.003555 | 0.003074 | 0.002767 | 0.003433 |

Relative to ABI-262, ABI-263 improved selected-checkpoint filtered connectivity by about +0.0427, but lost about -0.0175 filtered Dice, -0.0224 precision, -0.0127 recall, -0.0159 MIT Dice, and -0.0228 Google Dice. Relative to ABI-253, it is lower by about -0.0289 filtered Dice, -0.0665 precision, -0.0520 connectivity, -0.0214 MIT Dice, and -0.0485 Google Dice, while recall is only slightly higher. It remains farther behind ABI-249 and ABI-202, especially on connectivity and source-stratified Dice.

The intended line-state mechanism therefore partially improved ABI-262's weak connectivity, but not enough to compensate for lower overlap, precision, and source performance.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.204905 | 0.221694 | 0.177536 | 0.171331 | 0.254845 | 0.090635 | 0.005390 |
| 2 | 0.287769 | 0.283603 | 0.296551 | 0.293009 | 0.282713 | 0.179803 | 0.003496 |
| 3 | 0.301399 | 0.313188 | 0.278459 | 0.250879 | 0.377396 | 0.165595 | 0.005451 |
| 4 | 0.309979 | 0.312302 | 0.305427 | 0.280223 | 0.346805 | 0.164143 | 0.004485 |
| 5 | 0.318454 | 0.318440 | 0.318484 | 0.329885 | 0.307789 | 0.166316 | 0.003381 |
| 6 | 0.346380 | 0.347013 | 0.345092 | 0.308535 | 0.394809 | 0.174516 | 0.004637 |
| 7 | 0.372156 | 0.365345 | 0.387500 | 0.358100 | 0.387360 | 0.204169 | 0.003920 |
| 8 | 0.379436 | 0.373046 | 0.394107 | 0.378366 | 0.380513 | 0.274668 | 0.003644 |
| 9 | 0.354875 | 0.333143 | 0.409645 | 0.463217 | 0.287607 | 0.373662 | 0.002250 |
| 10 | 0.369210 | 0.355316 | 0.400672 | 0.427187 | 0.325089 | 0.239279 | 0.002758 |
| 11 | 0.361206 | 0.347897 | 0.391691 | 0.344847 | 0.379195 | 0.220277 | 0.003985 |
| 12 | 0.365631 | 0.351120 | 0.399927 | 0.417973 | 0.324939 | 0.214166 | 0.002817 |

The trajectory is finite and non-collapsed, with both Dataset Sources learning. Filtered Dice rises through epoch 8, but the final four epochs do not establish a late-improving case. The most interesting sign is epoch 9: connectivity jumps to 0.3737 and precision to 0.4632, but recall, MIT Dice, and aggregate Dice drop sharply. This suggests the line-state branch can create cleaner connected structures, but the current gating/decoder trades off too much area coverage and source balance.

## Interpretation

Classify ABI-263 as mixed/negative for this exact SegFormer directional line-state decoder. It answers the ABI-262 follow-up question: adding explicit high-resolution line state can improve connectivity, but this implementation did not preserve enough overlap, recall, or source-stratified performance to strengthen the SegFormer branch. The high memory footprint is also materially worse than ABI-262 despite a compact parameter count, so further attention/line-state additions should be justified by stronger metric evidence.

This Result does not eliminate modern lightweight segmentation backbones or architecture-internal line-state reasoning. It does argue against an unchanged ABI-263 repeat and against simply adding more epochs: the best checkpoint was epoch 8, final Dice and connectivity were lower, and the main failure is a mechanism tradeoff rather than truncated learning.

## Decision

Do not promote ABI-263. Do not request a late36 budget or whole-validation diagnostic for this Candidate.

Stop the exact ABI-262/263 SegFormer directional-line decoder branch unless a future hypothesis makes a clear mechanism change to decouple connectivity from coverage. A reasonable next step is to broaden away from this local branch toward another underexplored family, such as temporal change/calibration, rotation-aware line accumulation, or a different modern backbone with lower activation cost. Any follow-up must continue to avoid Candidate-owned thresholding, postprocessing, losses, metrics, Artifact Filters, target derivation, data loading, coordinates, or resource scheduling.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_045029_55c59e/candidate/PROPOSAL.md`
- `run_20260912_045029_55c59e/candidate/README.md`
- `run_20260912_045029_55c59e/candidate/manifest.yaml`
- `run_20260912_045029_55c59e/resolved_manifest.yaml`
- `run_20260912_045029_55c59e/outputs/model_summary.json`
- `run_20260912_045029_55c59e/outputs/best_metrics.json`
- `run_20260912_045029_55c59e/outputs/final_metrics.json`
- `run_20260912_045029_55c59e/outputs/metrics.jsonl`
- `run_20260912_045029_55c59e/outputs/resource_profile.json`
- `run_20260912_045029_55c59e/outputs/validation_postprocessing/index.json`
- `run_20260912_045029_55c59e/outputs/prediction_samples/samples.json`
- `run_20260912_040526_92961f` for ABI-262 parent comparator context
- `run_20260911_171333_f0b603` for ABI-253 line-memory U-NetFormer comparator context
- `run_20260911_111909_dd7ef7` for ABI-249 C4 steerable line-context comparator context
- `run_20260904_043143_ee0005` for ABI-202 current aggregate whole-validation frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
