# ABI-261 temporal high-resolution line-accumulation recall U-Net

research-figures: []

## Scope

This note records the exploratory Result for ABI-261, Candidate `abi261_temporal_highres_line_accum_recall_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260912_031837_f40c59`.

ABI-261 was a mechanism-changing temporal family-development scout after ABI-240, ABI-255, and ABI-259. It kept provider-owned `abi_16ch_plus_sza_temporal` inputs with offsets `[-1, 0, 1]`, `frame_selection_policy: temporal_eligible_center`, source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, batch size 2, constant learning rate, and trusted Line/Centerline auxiliary outputs. The intended mechanism change was to move differentiable directional line accumulation to the native-resolution stem, add a half-resolution longer-span path, and use a bounded recall-preserving mask head to lift line-supported logits without Candidate-owned thresholding or postprocessing.

Candidate code remained architecture-only and did not implement temporal lookup, cache access, data loading, missing-frame handling, target derivation, losses, metrics, Artifact Filters, thresholding, postprocessing, augmentation transforms, sampling policy, training loops, downloads, coordinates, Dataset Source identity, resource scheduling, or lifecycle behavior.

## Execution result

ABI-261 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key execution facts from Harness-owned artifacts:

- Status: completed.
- Input mode: `abi_16ch_plus_sza_temporal` with provider-owned offsets `[-1, 0, 1]`.
- Effective frame-selection policy: `temporal_eligible_center`.
- Sample counts after temporal eligibility and capped-record selection: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,172,759, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 3.82 / 4.09 GB.
- Training wall time: 1,201.3 s; validation wall time: 1,042.5 s; total Run wall time: 2,245.5 s.

This is valid finite/resource evidence for the temporal high-resolution line-accumulation plus recall-head mechanism on the capped temporal-eligible validation population. It is not whole-validation promotion evidence.

## Best-validation metrics

The best checkpoint by `val/filtered_dice` was epoch 10.

| Metric | ABI-261 best epoch 10 | ABI-261 final epoch 12 | ABI-259 line-support decoder | ABI-240 line-accum late36 | ABI-255 recurrent late36 | ABI-223 temporal-attn late36 | ABI-202 single-frame frontier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.377171 | 0.359877 | 0.381540 | 0.414892 | 0.417348 | 0.419776 | 0.427570 |
| Raw Dice | 0.390749 | 0.374343 | 0.398247 | 0.431959 | 0.435656 | 0.438487 | 0.442746 |
| Filtered precision | 0.361650 | 0.389414 | 0.438659 | 0.436241 | 0.468293 | 0.483764 | 0.439467 |
| Filtered recall | 0.394084 | 0.334504 | 0.337582 | 0.395534 | 0.376400 | 0.370738 | 0.416301 |
| Filtered connectivity | 0.264338 | 0.170716 | 0.331613 | 0.264863 | 0.281116 | 0.412427 | 0.457773 |
| MIT filtered Dice | 0.365117 | 0.344194 | 0.368471 | 0.397067 | 0.400833 | 0.398498 | 0.411992 |
| Google filtered Dice | 0.406542 | 0.398265 | 0.415787 | 0.460659 | 0.463143 | 0.476764 | 0.468151 |
| Filtered predicted-positive fraction | 0.005633 | 0.004441 | 0.003978 | 0.004687 | 0.004155 | 0.003962 | 0.003433 |

Relative to ABI-259, ABI-261 improved recall by about +0.0565 but lost about -0.0044 filtered Dice, -0.0770 precision, -0.0673 connectivity, and source Dice on both MIT and Google. Relative to ABI-240, the selected checkpoint almost exactly matched the low-connectivity value but did so at much lower Dice and precision, and without ABI-240's late-budget near-frontier overlap. Relative to ABI-255 and ABI-223, ABI-261 is substantially behind on aggregate Dice, precision, source Dice, and especially connectivity. It also remains well behind the ABI-202 single-frame frontier.

The high-resolution recall head therefore met only the recall-preservation part of its intended effect. It did not convert native-resolution directional support into a cleaner or more connected trusted-threshold Contrail Mask.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.202892 | 0.206776 | 0.194708 | 0.216816 | 0.190649 | 0.141423 | 0.004546 |
| 2 | 0.229636 | 0.218361 | 0.258433 | 0.385880 | 0.163453 | 0.284131 | 0.002190 |
| 3 | 0.277523 | 0.279801 | 0.272935 | 0.266714 | 0.289246 | 0.150819 | 0.005606 |
| 4 | 0.256858 | 0.241981 | 0.288260 | 0.288565 | 0.231429 | 0.158819 | 0.004146 |
| 5 | 0.269589 | 0.251936 | 0.313446 | 0.440333 | 0.194262 | 0.213830 | 0.002281 |
| 6 | 0.336823 | 0.324361 | 0.367002 | 0.382643 | 0.300804 | 0.201140 | 0.004064 |
| 7 | 0.316194 | 0.298821 | 0.358322 | 0.394771 | 0.263705 | 0.170477 | 0.003453 |
| 8 | 0.354113 | 0.340546 | 0.389524 | 0.463668 | 0.286435 | 0.297791 | 0.003194 |
| 9 | 0.338460 | 0.328488 | 0.360371 | 0.304627 | 0.380747 | 0.186310 | 0.006461 |
| 10 | 0.377171 | 0.365117 | 0.406542 | 0.361650 | 0.394084 | 0.264338 | 0.005633 |
| 11 | 0.352162 | 0.340513 | 0.381518 | 0.370077 | 0.335902 | 0.201682 | 0.004692 |
| 12 | 0.359877 | 0.344194 | 0.398265 | 0.389414 | 0.334504 | 0.170716 | 0.004441 |

The trajectory is finite and non-collapsed, but not late-improving. Filtered Dice peaks at epoch 10 and then regresses by epochs 11-12. The highest connectivity checkpoint is epoch 8 at 0.297791, but that checkpoint is lower in Dice and recall than epoch 10. Epoch 9 and epoch 10 show the intended recall expansion, but this comes with a larger predicted-positive fraction and weaker precision/connectivity rather than a cleaner connected line structure.

Source behavior remains informative rather than catastrophic: both MIT and Google improve from early epochs and have nonzero viable Dice, with Google stronger than MIT at the selected checkpoint. However, the source gap and both absolute source scores are weaker than the stronger temporal comparators.

## Interpretation

Classify ABI-261 as a negative/mixed family-development Result for this exact high-resolution line-accumulation plus recall-preserving mask-head mechanism. The positive evidence is that the architecture is contract-compliant, resource-safe, finite, and capable of raising recall without prediction collapse. The negative evidence is more important scientifically: the added native-resolution line support did not improve fixed-threshold connectivity, precision, or source-stratified overlap. The mechanism mostly broadened predicted positives rather than forming better connected contrail structures.

This does not eliminate temporal modeling, temporal attention, high-resolution line reasoning, or recall-preserving evidence heads as broader classes. It only argues against this exact combination as the next continuation. ABI-223 remains the stronger temporal-attention comparator for connectivity, ABI-255 remains the compact recurrent temporal comparator for near-frontier overlap, ABI-240 remains the line-accumulation recall comparator, and ABI-202 remains the whole-validation aggregate frontier.

## Decision

Do not promote ABI-261. Do not submit an unchanged late36 continuation: the best checkpoint is epoch 10, final epoch 12 is lower, and the intended connectivity improvement did not appear even though recall increased. A late36 repeat would be addressing the wrong failure mode.

If the campaign continues with temporal modeling, prefer a different mechanism rather than another local recall-head or line-accumulator tweak. Plausible in-contract directions include a line-aware recurrent state with explicit centerline-preserving decoder features, a temporal model that sharpens lower-confidence evidence at threshold 0.5 while controlling negative-patch clutter, or a non-temporal rotation-aware/modern-backbone scout. Any follow-up must continue to avoid Candidate-owned thresholding, postprocessing, losses, metrics, data loading, temporal lookup, temporal selection, coordinates, or resource scheduling.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260912_031837_f40c59/candidate/PROPOSAL.md`
- `run_20260912_031837_f40c59/candidate/README.md`
- `run_20260912_031837_f40c59/candidate/manifest.yaml`
- `run_20260912_031837_f40c59/resolved_manifest.yaml`
- `run_20260912_031837_f40c59/outputs/model_summary.json`
- `run_20260912_031837_f40c59/outputs/best_metrics.json`
- `run_20260912_031837_f40c59/outputs/final_metrics.json`
- `run_20260912_031837_f40c59/outputs/metrics.jsonl`
- `run_20260912_031837_f40c59/outputs/resource_profile.json`
- `run_20260912_031837_f40c59/outputs/validation_postprocessing/index.json`
- `run_20260912_031837_f40c59/outputs/prediction_samples/samples.json`
- `run_20260912_012708_f5897e` for ABI-259 temporal line-support comparator context
- `run_20260911_031326_43ed12` for ABI-240 temporal line-accumulator late36 comparator context
- `run_20260911_210922_27f346` for ABI-255 recurrent late36 comparator context
- `run_20260908_154531_8c7e2b` for ABI-223 temporal-attention late36 comparator context
- `run_20260904_043143_ee0005` for ABI-202 current aggregate whole-validation frontier context
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
