# Full-spectral BTD large-kernel line-context net ultra-stable repair

research-figures: []

## Scope

This note records the large-kernel line-context branch after ABI-095 completed Run `run_20260830_012033_a62afb`.

Source Runs:

- ABI-068 frequency-gated line U-Net focal-Tversky capped reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-092 original large-kernel line-context scout: `run_20260830_001308_e99407`
- ABI-093 stable large-kernel syntax attempt: `run_20260830_002454_13b411`
- ABI-094 stable syntax repair: `run_20260830_002805_1d4d0f`
- ABI-095 ultra-stable large-kernel repair: `run_20260830_012033_a62afb`

ABI-095 was a repair candidate for the large-kernel line-context family. It used provider-approved `abi_16ch` input only, deterministic bounded raw ABI and thermal BTD features derived from approved ABI channels, trusted `random_mirroring`, combined source-balanced sampling, batch size 4, constant learning rate 0.00005, 12 epochs, disabled early stopping, trusted `focal_tversky` primary loss, and a provider-derived `centerline` auxiliary target with trusted `weighted_bce` weight 0.02. The Run used the trusted 1,024-record-per-Dataset-Source/split representative cap, so this is capped family-development evidence rather than full-data promotion evidence.

## Repair context and contract observation

ABI-092 and ABI-094 both passed smoke testing but failed during training with Harness-recorded `candidate_bug` non-finite gradients in `gradient.front_end.learned_mixer.0.weight`. ABI-092 failed at epoch 2 batch 212; ABI-094 failed later at epoch 12 batch 376. ABI-093 was a syntax-only smoke failure with `unmatched '}' (model.py, line 296)`. ABI-095 removed the learned 1x1 front-end mixer, reduced base width from 48 to 40, bounded raw/BTD and intermediate activations, reduced residual contribution scales, and lowered learning rate to 0.00005 while preserving the broad axial/local/dilated large-kernel encoder-decoder hypothesis.

ABI-095 stayed inside the Candidate Experiment Contract. Candidate code owned only model architecture over provider-approved ABI tensors and ABI-derived BTD planes. It did not introduce candidate-owned data loading, sampling, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, network access, pretrained weights, or longitude/latitude inputs.

## ABI-095 resource and stability result

The repair achieved its minimum stability objective: `run_20260830_012033_a62afb` completed finitely for all 12 epochs with no all-negative/all-positive terminal collapse. Model summary reported 4,182,442 parameters against the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 2,763.8 seconds wall time and 15,942,549,504 bytes peak CUDA reserved, within the 3,600-second Docker training timeout.

The selected checkpoint was epoch 12, with final and best `val/filtered_dice` both 0.2642. Source-stratified filtered Dice was balanced but low: MIT 0.2655 and Google 0.2614. Filtered precision was 0.2243, filtered recall 0.3214, filtered connectivity 0.1347, and filtered predicted-positive fraction 0.00519.

## Best-validation comparison

| Run | Candidate | Primary branch | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, `focal_tversky`, centerline aux | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, `bce_dice_cldice`, centerline aux | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260830_012033_a62afb` | ABI-095 | ultra-stable large-kernel line-context net, `focal_tversky`, centerline aux | 12 | 0.2642 | 0.2655 | 0.2614 | 0.2243 | 0.3214 | 0.1347 | 0.00519 |

Relative to ABI-068, ABI-095 lost about 0.1322 aggregate filtered Dice, 0.1231 MIT Dice, 0.1547 Google Dice, 0.1749 precision, 0.0722 recall, and 0.2554 connectivity while predicting a larger filtered positive area. Relative to ABI-066, ABI-095 lost about 0.1183 aggregate Dice, 0.0984 MIT Dice, 0.1678 Google Dice, 0.2185 precision, 0.0153 recall, and 0.3384 connectivity, again with a larger filtered positive fraction.

The large-kernel repair therefore did not supply the hoped-for precision/connectivity-forward operating point. The branch is source-balanced but weak on both Dataset Sources and particularly poor on connectivity.

## ABI-095 trajectory

Filtered Dice by epoch was 0.0362, 0.0949, 0.1175, 0.1486, 0.1718, 0.1939, 0.1794, 0.1777, 0.2178, 0.1879, 0.1863, and 0.2642. The final epoch was the best checkpoint, so the run was late-improving rather than diverging. However, the improvement started from a very low floor and remained below the proposal's approximate 0.30 scout floor for both Dataset Sources at epoch 12.

The trajectory suggests the stability repair slowed and bounded optimization enough to finish, but at the cost of underpowered feature discrimination. The low learning rate and removal of the learned mixer removed the observed non-finite failure point, but the remaining deterministic front-end plus heavily damped large-kernel blocks did not recover adequate thin-line precision or continuity within the current 12-epoch constant-LR budget.

## Interpretation

Classify ABI-095 as a successful numerical-stability repair but a negative capped scientific result for this exact ultra-stable large-kernel line-context branch. It passes finite execution and resource feasibility, but it fails the proposal's minimum useful scout criteria because both MIT and Google filtered Dice remain below about 0.30 and secondary precision/connectivity are well below the ABI-068 and ABI-066 references.

ABI-092/094 identify a concrete instability mode for learned front-end large-kernel variants, and ABI-095 shows that simply removing that front-end and heavily damping the architecture makes the branch trainable but not competitive. This is enough to stop repeating the exact large-kernel line-context repair lineage. It is not evidence that every possible large-kernel or line-context idea is impossible, but future work should avoid another small stability-only tweak on this branch unless paired with a materially different hypothesis.

Canonical MCAST 2.1 remains the full Working Validation Split promotion context. All comparisons here are representative capped family-development evidence and are not full-data promotion evidence.

## Decision

Do not promote ABI-095. Do not repeat ABI-095 unchanged, and do not continue the ABI-092/094/095 repair lineage with another minor damping, clamping, or learning-rate-only modification. The branch's best checkpoint is finite and late-improving, but the aggregate and source-stratified scores are too far below ABI-068/066 and below the stated scout floor, with no offsetting precision, connectivity, or positive-area advantage.

A useful next hypothesis should broaden the frontier rather than keep repairing this exact large-kernel implementation. Candidate directions should preserve the successful ABI-068 frequency-gated lessons or test a materially different architecture family/trusted policy axis for the precision-connectivity tradeoff, while keeping thresholding, Artifact Filters, data loading, sampling, augmentation implementation, target derivation, losses, metrics, resource placement, and lifecycle behavior out of Candidate code.

## Artifact references

- `run_20260830_012033_a62afb/outputs/best_metrics.json`
- `run_20260830_012033_a62afb/outputs/final_metrics.json`
- `run_20260830_012033_a62afb/outputs/metrics.jsonl`
- `run_20260830_012033_a62afb/outputs/resource_profile.json`
- `run_20260830_012033_a62afb/outputs/model_summary.json`
- `run_20260830_012033_a62afb/outputs/prediction_samples/samples.json`
- `run_20260830_001308_e99407/outputs/nonfinite_diagnostic.json`
- `run_20260830_002805_1d4d0f/outputs/nonfinite_diagnostic.json`
- `run_20260830_002454_13b411/outputs/logs/smoke_test.log`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
