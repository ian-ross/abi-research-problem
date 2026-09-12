# ABI-258 temporal attention dual-evidence calibration U-Net

research-figures: []

## Scope

This note records the exploratory Result for ABI-258, Candidate `abi258_temporal_attention_dual_evidence_calibration_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260912_004429_1eee45`.

ABI-258 was a temporal-attention family-development Candidate after ABI-223, ABI-254, ABI-255, and ABI-257. It kept provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`, `frame_selection_policy: temporal_eligible_center`, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, batch size 2, constant learning rate, and trusted Line/Centerline auxiliary outputs. The intended mechanism change was narrow: retain ABI-223-style temporal-attention fusion and replace the final mask head with a bounded dual recall/precision evidence-calibration head that could raise true contrail logits at the trusted 0.5 threshold without candidate-owned thresholding or postprocessing.

Candidate code remained architecture-only and did not implement temporal lookup, cache access, data loading, missing-frame handling, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Execution result

ABI-258 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Input mode: `abi_16ch_plus_sza_temporal` with provider-owned offsets `[-1, 0, 1]`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,139,544, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.32 / 3.61 GB.
- Training wall time: 1,029.8 s; validation wall time: 995.5 s; total Run wall time: 2,027.1 s.

This is valid finite/resource evidence for the dual-evidence calibration head on the temporal-eligible capped validation population. It is not whole-validation promotion evidence.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 11.

| Metric | ABI-258 best epoch 11 | ABI-258 final epoch 12 | ABI-254 center-detail evidence | ABI-257 oriented recurrent | ABI-255 recurrent late36 | ABI-223 temporal-attn late36 | ABI-202 single-frame frontier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.388192 | 0.338822 | 0.393943 | 0.375124 | 0.417348 | 0.419776 | 0.427570 |
| Raw Dice | 0.404756 | 0.356005 | 0.412509 | 0.390882 | 0.435656 | 0.438487 | 0.442746 |
| Filtered precision | 0.422628 | 0.493503 | 0.486613 | 0.391551 | 0.468293 | 0.483764 | 0.439467 |
| Filtered recall | 0.358944 | 0.257966 | 0.330922 | 0.360020 | 0.376400 | 0.370738 | 0.416301 |
| Filtered connectivity | 0.260347 | 0.337831 | 0.365528 | 0.213486 | 0.281116 | 0.412427 | 0.457773 |
| MIT filtered Dice | 0.372045 | 0.318729 | 0.377873 | 0.363565 | 0.400833 | 0.398498 | 0.411992 |
| Google filtered Dice | 0.429000 | 0.391345 | 0.436096 | 0.402919 | 0.463143 | 0.476764 | 0.468151 |
| Filtered predicted-positive fraction | 0.004391 | 0.002702 | 0.003516 | 0.004753 | 0.004155 | 0.003962 | 0.003433 |

Relative to ABI-254, ABI-258's selected checkpoint improved fixed-threshold recall by about +0.0280 and increased predicted-positive fraction by about +0.0009, but regressed filtered Dice by about -0.0058, precision by -0.0640, connectivity by -0.1052, MIT Dice by -0.0058, and Google Dice by -0.0071. Relative to ABI-223, ABI-258 remained lower by about -0.0316 filtered Dice, -0.0611 precision, -0.0118 recall, -0.1521 connectivity, -0.0265 MIT Dice, and -0.0478 Google Dice.

The dual-evidence head therefore met only the weakest part of its success criterion: it recovered some recall relative to ABI-254, but not in a precision- or connectivity-preserving way. It did not approach ABI-223's overlap/connectivity balance and did not improve the temporal-attention frontier.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.215039 | 0.222278 | 0.200105 | 0.214007 | 0.216082 | 0.154579 | 0.005220 |
| 2 | 0.242051 | 0.233694 | 0.262364 | 0.352714 | 0.184244 | 0.270730 | 0.002700 |
| 3 | 0.279457 | 0.270184 | 0.299720 | 0.321167 | 0.247335 | 0.224777 | 0.003981 |
| 4 | 0.296499 | 0.285217 | 0.324137 | 0.383270 | 0.241765 | 0.200570 | 0.003261 |
| 5 | 0.318342 | 0.297365 | 0.371656 | 0.459228 | 0.243607 | 0.298587 | 0.002742 |
| 6 | 0.295922 | 0.297387 | 0.292734 | 0.277426 | 0.317060 | 0.150265 | 0.005908 |
| 7 | 0.329466 | 0.307006 | 0.390535 | 0.550789 | 0.235026 | 0.399815 | 0.002206 |
| 8 | 0.348616 | 0.334799 | 0.381879 | 0.412865 | 0.301670 | 0.271680 | 0.003777 |
| 9 | 0.358265 | 0.351949 | 0.373005 | 0.323164 | 0.401921 | 0.203538 | 0.006429 |
| 10 | 0.372507 | 0.357169 | 0.411672 | 0.457007 | 0.314379 | 0.299148 | 0.003556 |
| 11 | 0.388192 | 0.372045 | 0.429000 | 0.422628 | 0.358944 | 0.260347 | 0.004391 |
| 12 | 0.338822 | 0.318729 | 0.391345 | 0.493503 | 0.257966 | 0.337831 | 0.002702 |

The trajectory is finite and non-collapsed, but it is oscillatory. Epoch 9 reached the highest recall, 0.401921, by expanding predicted positives to 0.006429 and losing precision/connectivity. Epoch 11 recovered the best Dice balance, but connectivity remained weak. The final epoch moved toward a conservative high-precision state with improved connectivity versus epoch 11, but it lost about -0.0494 filtered Dice and -0.1010 recall. This is not a clean late-improving signal for the primary metric.

## Interpretation

Classify ABI-258 as a negative/mixed family-development Result for this exact dual-evidence calibration head. The Run confirms that the mechanism is resource-safe, finite, and source-informative, and that architecture-level evidence heads can move the precision/recall operating point without changing trusted thresholds. However, the learned tradeoff was unstable: recall gains over ABI-254 came with too much precision and continuity loss, while the later high-precision state pruned away too much true contrail coverage.

The result does not eliminate temporal attention modeling. ABI-223 remains the stronger temporal-attention comparator, ABI-255 remains the compact recurrent temporal comparator, and ABI-253 remains the whole-validation-tested U-NetFormer/line-memory comparator. ABI-258 only argues against this exact local mask-head calibration repair as the next temporal-attention path.

## Decision

Do not promote ABI-258. Do not submit an unchanged late36 continuation of this exact dual-evidence calibration head: the selected checkpoint was epoch 11, final epoch 12 regressed sharply on filtered Dice and recall, and the mechanism did not preserve ABI-223-style connectivity.

If the campaign continues with temporal modeling, prefer a more mechanism-changing design rather than another local final-head repair: for example, temporal attention that explicitly preserves connected line evidence through the decoder, a temporal-change/detail branch with stronger MIT recall, or a non-temporal rotation-aware/line-accumulation scout. Any follow-up must continue to avoid Candidate-owned thresholding, postprocessing, losses, metrics, data loading, temporal lookup, temporal selection, coordinates, or resource scheduling.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_004429_1eee45/candidate/PROPOSAL.md`
- `run_20260912_004429_1eee45/candidate/README.md`
- `run_20260912_004429_1eee45/candidate/manifest.yaml`
- `run_20260912_004429_1eee45/resolved_manifest.yaml`
- `run_20260912_004429_1eee45/outputs/model_summary.json`
- `run_20260912_004429_1eee45/outputs/best_metrics.json`
- `run_20260912_004429_1eee45/outputs/final_metrics.json`
- `run_20260912_004429_1eee45/outputs/metrics.jsonl`
- `run_20260912_004429_1eee45/outputs/resource_profile.json`
- `run_20260912_004429_1eee45/outputs/validation_postprocessing/index.json`
- `run_20260912_004429_1eee45/outputs/prediction_samples/samples.json`
- `run_20260911_202724_fee837` for ABI-254 center-detail evidence context
- `run_20260911_235337_128345` for ABI-257 oriented recurrent context
- `run_20260911_210922_27f346` for ABI-255 recurrent late36 comparator context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention late36 comparator context
- `run_20260904_043143_ee0005` for ABI-202 current aggregate whole-validation frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
