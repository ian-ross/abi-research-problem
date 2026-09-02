# Full-spectral BTD+SZA soft ridge-gate U-Net clDice Centerline-auxiliary follow-up

research-figures: []

## Scope

This note records ABI-153 after Run `run_20260901_061306_9b10a4` completed.

Source Runs:

- ABI-153 full-spectral BTD+SZA soft ridge-gate U-Net BCE-Dice-clDice Centerline-auxiliary continuation: `run_20260901_061306_9b10a4`
- ABI-143 soft ridge-gate U-Net BCE-Dice comparison target: `run_20260831_224534_27b73d`
- ABI-142 multiscale ridge-attention U-Net BCE-Dice predecessor: `run_20260831_215104_d4c318`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice near-reference branch: `run_20260831_121006_7d24be`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice high-precision/connectivity comparator: `run_20260831_085615_d05ab3`
- ABI-068 frequency-gated line U-Net focal-Tversky local capped aggregate-Dice reference: `run_20260828_010836_4ccc77`

ABI-153 was a controlled loss-policy continuation of ABI-143. It kept provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features derived only from approved ABI channels, normalized Solar Geometry Input features, the soft ridge-gate U-Net architecture, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled manifest change was switching the trusted primary loss from `bce_dice` to `bce_dice_cldice`.

## Contract and resource observation

ABI-153 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 9,617,130 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,943.9 seconds total wall time, 1,596.1 seconds training wall time, 1,345.8 seconds validation wall time, 6,760,061,952 bytes peak CUDA allocated, 7,520,387,072 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The best-validation checkpoint was epoch 11; final epoch 12 regressed on the trusted checkpoint metric.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_224534_27b73d` | ABI-143 | soft ridge-gate U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3947 | 0.3815 | 0.4287 | 0.4105 | 0.3801 | 0.3010 | 0.00336 |
| `run_20260831_215104_d4c318` | ABI-142 | multiscale ridge-attention U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3935 | 0.3762 | 0.4373 | 0.4398 | 0.3561 | 0.3819 | 0.00293 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260901_061306_9b10a4` | ABI-153 | soft ridge-gate U-Net, BCE-Dice-clDice, ABI-16+BTD+SZA | 11 | 0.3739 | 0.3701 | 0.3825 | 0.3591 | 0.3899 | 0.3234 | 0.00393 |

ABI-153 did not meet the controlled loss-swap success criteria. Relative to ABI-143, aggregate filtered Dice fell by 0.0209, MIT filtered Dice by 0.0114, Google filtered Dice by 0.0462, and filtered precision by 0.0514. Filtered recall rose by 0.0098 and filtered connectivity rose by 0.0225, but the proposal asked for the branch to remain within about 0.007 aggregate filtered Dice while improving connectivity by about 0.04, or otherwise show a better precision/connectivity balance. ABI-153 did neither: the continuity/recalibration gain was smaller than targeted and came with materially worse aggregate/source overlap and positive-area discipline.

Relative to ABI-142, ABI-153 is lower by 0.0196 aggregate filtered Dice, 0.0061 MIT Dice, 0.0548 Google Dice, 0.0806 precision, and 0.0585 connectivity, while recall is higher by 0.0338. Relative to ABI-130, ABI-153 is lower by 0.0214 aggregate Dice, 0.0579 Google Dice, 0.0823 precision, and 0.0616 connectivity, with only a recall gain. Relative to ABI-126, ABI-153 improves MIT Dice and recall but remains below ABI-126 on aggregate Dice, Google Dice, precision, connectivity, and positive-area discipline. Relative to the local capped reference ABI-068, ABI-153 is lower on aggregate/source Dice, precision, recall, and connectivity.

## ABI-153 trajectory

ABI-153 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.2246, 0.2858, 0.3027, 0.3322, 0.3432, 0.2833, 0.3534, 0.3396, 0.3606, 0.3696, 0.3739, and 0.3320. The selected checkpoint was epoch 11. The final epoch dropped sharply in aggregate filtered Dice and recall, so the run does not show a clean late upward trajectory at the active budget.

At the selected checkpoint, source-stratified filtered Dice was 0.3701 for MIT and 0.3825 for Google. MIT had filtered precision 0.3812, recall 0.3596, connectivity 0.3778, and predicted-positive fraction 0.00510. Google had filtered precision 0.3186, recall 0.4785, connectivity 0.2690, and predicted-positive fraction 0.00277. The branch remained source-informative, but the high Google recall/low Google precision profile and elevated predicted-positive fraction indicate a more permissive operating point rather than a cleaner line-continuity solution.

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice was 0.3868 versus filtered Dice 0.3739, and raw predicted-positive fraction was 0.00419 versus filtered 0.00393. This does not indicate primary Artifact Filter dependence. The fixed first-four prediction artifacts include one empty-background perfect case and three near-zero overlap cases under the `first_n` retention policy; these artifacts are traceability samples and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-153 as a completed, finite, non-collapsed, scientifically negative controlled loss-swap result for the SZA-aware soft ridge-gate branch. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The BCE-Dice-clDice loss did apply useful continuity/recall pressure relative to ABI-143, but not enough to offset the loss of precision, Google Dice, and aggregate filtered Dice. This is consistent with prior clDice branches that often move the operating point toward permissive thin-line predictions without improving the trusted capped primary metric. The exact ABI-143-to-ABI-153 loss swap should therefore stop.

The result should not eliminate ridge-aware SZA modeling or clDice globally. It does narrow this specific combination: soft ridge gate plus Centerline Target auxiliary plus BCE-Dice-clDice at learning rate 0.0003 produced a lower-quality recall-forward tradeoff than the ABI-143 BCE-Dice comparison target and did not recover ABI-142/ABI-126/ABI-068 connectivity in a source-balanced way.

## Decision

Do not promote ABI-153 and do not request whole-validation diagnostics for it. Stop the exact soft ridge-gate BCE-Dice-clDice loss-swap branch. Future work should broaden away from simple clDice substitutions on this ridge branch and toward a distinct architecture/front-end/calibration/data-policy mechanism, or return to the stronger ABI-068 and ABI-130 axes with a targeted change that preserves precision and Google Dice while improving connectivity. No Capability Request, Evaluation Request, or Campaign Report is required from ABI-153.

## Artifact references

- `run_20260901_061306_9b10a4/outputs/best_metrics.json`
- `run_20260901_061306_9b10a4/outputs/final_metrics.json`
- `run_20260901_061306_9b10a4/outputs/metrics.jsonl`
- `run_20260901_061306_9b10a4/outputs/resource_profile.json`
- `run_20260901_061306_9b10a4/outputs/model_summary.json`
- `run_20260901_061306_9b10a4/outputs/prediction_samples/samples.json`
- `run_20260901_061306_9b10a4/resolved_manifest.yaml`
- `run_20260831_224534_27b73d/outputs/best_metrics.json`
- `run_20260831_215104_d4c318/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
