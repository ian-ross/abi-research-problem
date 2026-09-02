# Full-spectral BTD+SZA structure-tensor ASPP/detail decoder finite-repair follow-up

research-figures: []

## Scope

This note records ABI-150 after Run `run_20260901_034937_91779f` completed.

Source Runs:

- ABI-150 finite-gradient repair of ABI-149 full-spectral BTD+SZA structure-tensor ASPP/detail decoder: `run_20260901_034937_91779f`
- ABI-149 failed structure-tensor ASPP/detail decoder implementation repaired by ABI-150: `run_20260901_034445_07ce82`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice Centerline-auxiliary comparison target: `run_20260831_121006_7d24be`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice Centerline-auxiliary precision/connectivity reference: `run_20260831_085615_d05ab3`
- ABI-143 SZA-aware soft ridge-gate U-Net BCE-Dice Centerline-auxiliary reference: `run_20260831_224534_27b73d`
- ABI-068 frequency-gated line U-Net focal-Tversky local capped aggregate-Dice reference: `run_20260828_010836_4ccc77`

ABI-150 was a Repair Candidate for ABI-149. ABI-149 failed smoke testing with Harness-classified `candidate_bug` from `non_finite_training_state` in `gradient.front_end.learned_mixer.0.weight`. ABI-150 preserved the structure-tensor hypothesis and comparison target while stabilizing the differentiable Sobel/structure-tensor feature calculation with positive-epsilon square-root and denominator paths plus bounded coherence/orientation/ridge features.

## Contract and resource observation

ABI-150 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records provider-approved `abi_16ch_plus_sza` input, ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, trusted random mirroring, target derivation, losses, metrics, thresholding, Artifact Filters, prediction retention, resource placement, and Run lifecycle.

The repair succeeded operationally. Static/smoke/training completed without recurrence of the ABI-149 non-finite gradient failure. `outputs/model_summary.json` reports 9,627,462 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,454.3 seconds total wall time, 1,178.5 seconds training wall time, 1,273.9 seconds validation wall time, 6,248,402,432 bytes peak CUDA allocated, 6,853,492,736 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The best-validation checkpoint was epoch 9 rather than final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_224534_27b73d` | ABI-143 | soft ridge-gate U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3947 | 0.3815 | 0.4287 | 0.4105 | 0.3801 | 0.3010 | 0.00336 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260901_034937_91779f` | ABI-150 | structure-tensor ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 9 | 0.3638 | 0.3573 | 0.3799 | 0.3554 | 0.3727 | 0.1877 | 0.00380 |

ABI-150 did not meet its scientific continuation criteria. Relative to ABI-130, aggregate filtered Dice fell by 0.0314, MIT filtered Dice by 0.0206, Google filtered Dice by 0.0604, precision by 0.0861, and connectivity by 0.1973. Recall rose by 0.0149, but with a higher predicted-positive fraction and without a compensating Dice, connectivity, source-balance, or precision advantage. Relative to ABI-126, ABI-150 loses aggregate Dice by 0.0220 and connectivity by 0.2640. Relative to ABI-143, it loses aggregate Dice by 0.0309 and connectivity by 0.1132. Relative to ABI-068, it is lower on aggregate/source Dice, precision, recall, and connectivity.

## ABI-150 trajectory

ABI-150 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.2013, 0.2555, 0.2933, 0.2862, 0.2859, 0.3301, 0.3188, 0.3413, 0.3638, 0.3353, 0.3353, and 0.3621. The selected checkpoint was epoch 9; final epoch 12 nearly recovered the selected aggregate Dice but remained lower.

At the selected checkpoint, source-stratified filtered Dice was 0.3573 for MIT and 0.3799 for Google. MIT had filtered precision 0.3661, recall 0.3489, connectivity 0.1973, and predicted-positive fraction 0.00515. Google had filtered precision 0.3329, recall 0.4424, connectivity 0.1781, and predicted-positive fraction 0.00245. The branch is source-informative but not source-balanced in a useful way: Google recall is high, while both source Dice and connectivity remain below the comparison targets.

The final epoch had aggregate filtered Dice 0.3621, MIT/Google filtered Dice 0.3502/0.3910, filtered precision 0.3794, recall 0.3462, connectivity 0.1958, and predicted-positive fraction 0.00331. This late point improved precision and Google Dice relative to epoch 9 but still stayed materially below ABI-130 and did not restore the intended line-connectivity benefit. Raw-to-filtered differences were modest at the selected checkpoint: raw Dice 0.3763 versus filtered Dice 0.3638, and raw predicted-positive fraction 0.00407 versus filtered 0.00380. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples have near-zero per-sample Dice, but they are traceability artifacts under the `first_n` policy and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-150 as a completed, finite, non-collapsed, scientifically negative Repair Candidate. It successfully repaired ABI-149's non-finite smoke failure, so the original failure was a candidate implementation bug rather than a Harness or resource blocker. Scientifically, explicit stabilized structure-tensor features did not improve the SZA-aware ASPP/detail BCE-Dice branch at the representative capped budget. The added line-coherence evidence appears to trade away ABI-130's stronger precision, Google overlap, and especially connectivity without providing enough recall gain to compensate.

This stops the exact ABI-149/ABI-150 structure-tensor ASPP/detail branch. It does not eliminate all structure-aware preprocessing, SZA-aware input use, ASPP/detail decoders, or full-spectral BTD modeling. The result specifically argues against this stabilized structure-tensor front-end attached to the ABI-130-style BCE-Dice ASPP/detail decoder under the current contract, cap, scheduler, and 12-epoch budget.

## Decision

Do not promote ABI-150 and do not request whole-validation diagnostics for it. The Run underperforms ABI-130, ABI-143, ABI-126, and ABI-068 on aggregate filtered Dice and lacks compensating precision, connectivity, source-balance, positive-area discipline, or late-epoch trajectory evidence. It satisfies the proposal hard-stop condition for this exact branch: finite result materially below ABI-130 without compensating precision/connectivity/source-balance gains.

Future work should broaden rather than add further ad-hoc structure-tensor repairs to this branch. Reasonable next frontiers remain distinct architectures, safer calibration mechanisms, data-policy/augmentation tests, or non-suppressive line-context features that preserve ABI-130/ABI-126 connectivity rather than replacing it with low-connectivity local tensor evidence. No Capability Request, Evaluation Request, or Campaign Report is required from ABI-150.

## Artifact references

- `run_20260901_034937_91779f/outputs/best_metrics.json`
- `run_20260901_034937_91779f/outputs/final_metrics.json`
- `run_20260901_034937_91779f/outputs/metrics.jsonl`
- `run_20260901_034937_91779f/outputs/resource_profile.json`
- `run_20260901_034937_91779f/outputs/model_summary.json`
- `run_20260901_034937_91779f/outputs/prediction_samples/samples.json`
- `run_20260901_034937_91779f/resolved_manifest.yaml`
- `run_20260901_034445_07ce82/outputs/logs/smoke_test.log`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260831_224534_27b73d/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
