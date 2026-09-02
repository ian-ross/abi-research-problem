# Full-spectral BTD+SZA ASPP/detail decoder no-augmentation follow-up

research-figures: []

## Scope

This note records ABI-152 after Run `run_20260901_052814_d8e50a` completed.

Source Runs:

- ABI-152 full-spectral BTD+SZA ASPP/detail decoder no-augmentation BCE-Dice Centerline-auxiliary continuation: `run_20260901_052814_d8e50a`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice Centerline-auxiliary comparison target: `run_20260831_121006_7d24be`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice Centerline-auxiliary precision/connectivity reference: `run_20260831_085615_d05ab3`
- ABI-143 SZA-aware soft ridge-gate U-Net BCE-Dice Centerline-auxiliary near-best reference: `run_20260831_224534_27b73d`
- ABI-068 frequency-gated line U-Net focal-Tversky current local capped aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-087 no-augmentation frequency-gated focal-Tversky reference: `run_20260829_193824_241e30`
- ABI-151 recent SZA patch-anomaly ASPP/detail negative reference: `run_20260901_044007_880e7e`

ABI-152 was a controlled augmentation-policy continuation of ABI-130. It kept provider-approved `abi_16ch_plus_sza`, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled manifest change was disabling trusted `random_mirroring` and using trusted augmentation policy `none`.

## Contract and resource observation

ABI-152 stayed inside the Candidate Experiment Contract. It used only GOES ABI channels 1-16 plus Solar Geometry Input; forbidden longitude and latitude inputs remained excluded. Candidate code emitted primary `mask_logits` and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, target derivation, losses, metrics, thresholding, Artifact Filters, prediction retention, resource placement, and Run lifecycle.

The Run completed operationally. It trained 12 epochs on the A100 at batch size 4 with 2,048 train and 2,048 validation records under the provider-owned capped-record policy. `outputs/resource_profile.json` reports 2,216.8 seconds total wall time, 994.7 seconds training wall time, 1,220.2 seconds validation wall time, 5,914,883,584 bytes peak CUDA allocated, 6,469,713,920 bytes peak CUDA reserved, and completed status. The best-validation checkpoint was epoch 11; the final epoch 12 did not retain the selected aggregate filtered Dice.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA, random mirroring | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_224534_27b73d` | ABI-143 | soft ridge-gate U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3947 | 0.3815 | 0.4287 | 0.4105 | 0.3801 | 0.3010 | 0.00336 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260829_193824_241e30` | ABI-087 | frequency-gated line U-Net, focal-Tversky, no augmentation | 11 | 0.3704 | 0.3701 | 0.3710 | 0.3158 | 0.4478 | 0.2479 | 0.00514 |
| `run_20260901_044007_880e7e` | ABI-151 | patch-anomaly ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 8 | 0.3774 | 0.3673 | 0.4006 | 0.3947 | 0.3616 | 0.3317 | 0.00332 |
| `run_20260901_052814_d8e50a` | ABI-152 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA, no augmentation | 11 | 0.3846 | 0.3717 | 0.4181 | 0.4379 | 0.3429 | 0.3602 | 0.00284 |

ABI-152 did not meet its comparison-target success criteria. Relative to ABI-130, best-validation aggregate filtered Dice fell by 0.0106, MIT filtered Dice by 0.0062, Google filtered Dice by 0.0223, filtered precision by 0.0036, filtered recall by 0.0149, and connectivity by 0.0249. The selected checkpoint did slightly lower filtered predicted-positive fraction from 0.00294 to 0.00284, but that small positive-area discipline gain is not enough to offset the lower aggregate/source Dice, recall, and connectivity.

Relative to ABI-126, ABI-152 slightly improves MIT filtered Dice and recall, but loses aggregate filtered Dice by 0.0012, Google Dice by 0.0234, precision by 0.0367, connectivity by 0.0915, and positive-area discipline. Relative to ABI-143 and ABI-068, ABI-152 is lower on aggregate filtered Dice, MIT Dice, recall, and connectivity. It does improve over ABI-151's patch-anomaly SZA ASPP/detail branch on aggregate/source Dice, precision, connectivity, and predicted-positive discipline, but that is a recovery from a negative tweak rather than an improvement over the active ABI-130 comparison target.

## ABI-152 trajectory

ABI-152 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.2298, 0.2757, 0.3147, 0.3203, 0.3417, 0.3719, 0.3709, 0.3701, 0.3707, 0.3684, 0.3846, and 0.3771. The trajectory improved through epoch 11 but did not reach ABI-130 or ABI-068.

At the selected checkpoint, source-stratified filtered Dice was 0.3717 for MIT and 0.4181 for Google. MIT had filtered precision 0.4424, recall 0.3204, connectivity 0.3462, and predicted-positive fraction 0.00391. Google had filtered precision 0.4280, recall 0.4086, connectivity 0.3742, and predicted-positive fraction 0.00176. The result remains source-informative and non-degenerate, with better Google than MIT behavior, but no source-stratified improvement sufficient to continue this exact no-augmentation ABI-130 branch.

The final epoch shifted toward higher precision/connectivity but lower recall: final filtered Dice 0.3771, filtered precision 0.4490, recall 0.3250, connectivity 0.4179, and filtered predicted-positive fraction 0.00262. That final checkpoint has better connectivity and slightly better precision/positive-area discipline than ABI-130, but the aggregate filtered Dice gap is 0.0182 and MIT filtered Dice is only 0.3585. Under the trusted checkpoint metric, this is a diagnostic precision/connectivity tradeoff rather than a useful selected operating point.

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice 0.3994 versus filtered Dice 0.3846, and raw predicted-positive fraction 0.00303 versus filtered 0.00284. This does not suggest primary Artifact Filter dependence. The fixed first-four prediction artifacts remain traceability artifacts under the `first_n` retention policy and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-152 as a completed, finite, non-collapsed, scientifically negative family-development result for the no-augmentation SZA-aware ASPP/detail BCE-Dice branch. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The result suggests trusted random mirroring was not the main cause of ABI-130's remaining calibration/connectivity tradeoff. Disabling mirroring slightly reduced selected-checkpoint predicted-positive area and the final epoch improved connectivity, but the selected and final checkpoints both lost too much aggregate/source Dice and recall. Together with ABI-087's prior no-augmentation evidence in a different family, this argues against spending more immediate steps on no-augmentation as a general fix under the current cap, scheduler, sampling, and 12-epoch budget.

## Decision

Do not promote ABI-152 and do not request whole-validation diagnostics for it. Stop the exact no-augmentation SZA ASPP/detail BCE-Dice branch. Future work should broaden away from further ad-hoc ABI-130 augmentation/front-end tweaks unless a new hypothesis directly targets the observed precision/connectivity versus recall tradeoff without reducing Google Dice. Reasonable next frontiers include a distinct architecture family, safer calibration/head design, loss/auxiliary-target choices, trusted data-policy tests, or preprocessing/front-end designs that preserve ABI-130 recall while improving connectivity and positive-area discipline.

No Capability Request, Evaluation Request, or Campaign Report is required from ABI-152.

## Artifact references

- `run_20260901_052814_d8e50a/outputs/best_metrics.json`
- `run_20260901_052814_d8e50a/outputs/final_metrics.json`
- `run_20260901_052814_d8e50a/outputs/metrics.jsonl`
- `run_20260901_052814_d8e50a/outputs/resource_profile.json`
- `run_20260901_052814_d8e50a/outputs/model_summary.json`
- `run_20260901_052814_d8e50a/outputs/prediction_samples/samples.json`
- `run_20260901_052814_d8e50a/resolved_manifest.yaml`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260831_224534_27b73d/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260829_193824_241e30/outputs/best_metrics.json`
- `run_20260901_044007_880e7e/outputs/best_metrics.json`
