# Full-spectral BTD+SZA additive ridge-residual U-Net BCE-Dice follow-up

research-figures: []

## Scope

This note records ABI-144 after Run `run_20260831_234016_e7916c` completed.

Source Runs:

- ABI-144 full-spectral BTD+SZA additive ridge-residual U-Net BCE-Dice Centerline-auxiliary continuation: `run_20260831_234016_e7916c`
- ABI-143 soft ridge-gate U-Net BCE-Dice predecessor: `run_20260831_224534_27b73d`
- ABI-142 multiscale ridge-attention U-Net BCE-Dice predecessor: `run_20260831_215104_d4c318`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice Centerline-auxiliary reference: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate-Dice reference: `run_20260828_010836_4ccc77`

ABI-144 was a controlled family-development continuation of ABI-143. It kept provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features derived only from approved ABI channels, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled architectural change was to remove ABI-143's multiplicative final ridge gate and replace it with a neutral-initialized additive residual ridge path bounded by `0.1 * tanh(...)`.

## Contract and resource observation

ABI-144 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 9,617,130 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,785.4 seconds total wall time, 1,461.1 seconds training wall time, 1,322.4 seconds validation wall time, 6,675,088,896 bytes peak CUDA allocated, 7,327,449,088 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_224534_27b73d` | ABI-143 | soft ridge-gate U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3947 | 0.3815 | 0.4287 | 0.4105 | 0.3801 | 0.3010 | 0.00336 |
| `run_20260831_215104_d4c318` | ABI-142 | multiscale ridge-attention U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3935 | 0.3762 | 0.4373 | 0.4398 | 0.3561 | 0.3819 | 0.00293 |
| `run_20260831_234016_e7916c` | ABI-144 | additive ridge-residual U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3839 | 0.3644 | 0.4335 | 0.4796 | 0.3200 | 0.3778 | 0.00242 |

ABI-144 completed reliably but did not meet its mechanism-specific success criterion. Versus ABI-143, aggregate filtered Dice fell by 0.0109, MIT filtered Dice by 0.0171, filtered recall by 0.0601, and filtered predicted-positive fraction by 0.00094. The additive residual did recover much of ABI-142's connectivity behavior relative to ABI-143 (+0.0768), and it improved filtered precision by +0.0691, but this came from a more conservative operating point rather than a better aggregate/source-balanced trade-off.

Versus ABI-142, ABI-144 is lower by 0.0097 aggregate filtered Dice and 0.0117 MIT filtered Dice, while Google filtered Dice is only 0.0039 lower and filtered precision is 0.0399 higher. Versus ABI-130, ABI-144 is lower by 0.0114 aggregate filtered Dice, 0.0134 MIT filtered Dice, 0.0069 Google filtered Dice, and 0.0378 filtered recall, while precision is higher by 0.0382. Versus the local capped reference ABI-068, ABI-144 is lower by 0.0125 aggregate filtered Dice, 0.0242 MIT filtered Dice, and 0.0736 filtered recall, despite higher precision and comparable connectivity.

## ABI-144 trajectory

ABI-144 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.2101, 0.2646, 0.3047, 0.3483, 0.3534, 0.3753, 0.3692, 0.3662, 0.3672, 0.3530, 0.3783, and 0.3839. The final epoch was the selected best checkpoint, so the branch was still improving late, but it remained below the predecessor and reference band at the active budget.

The best checkpoint showed source-stratified filtered Dice of 0.3644 for MIT and 0.4335 for Google. MIT had filtered precision 0.4824, recall 0.2928, connectivity 0.3663, and predicted-positive fraction 0.00328. Google had filtered precision 0.4738, recall 0.3995, connectivity 0.3893, and predicted-positive fraction 0.00156. Both Dataset Sources were finite and non-collapsed, but the conservative positive area particularly hurt MIT recall.

Raw-to-filtered differences were modest at the best checkpoint: raw Dice was 0.3991 versus filtered Dice 0.3839, and raw predicted-positive fraction was 0.00258 versus filtered 0.00242. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples remain traceability artifacts under the `first_n` retention policy and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-144 as a completed, finite, non-collapsed, negative mechanism test for additive ridge-residual refinement. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch. The result supports the interpretation that the neutral additive ridge residual preserved connectivity and increased precision relative to ABI-143, but did so by reducing predicted-positive area and recall enough to lower aggregate and MIT filtered Dice.

The exact additive ridge-residual branch should not be repeated or promoted from representative capped evidence. It clarifies that the ridge-family issue is not merely multiplicative suppression; replacing the gate with a bounded additive path moved the model toward high precision and lower recall without improving the capped source-balanced objective. Future work should broaden away from final ridge-gate/refinement tuning unless it introduces a clearly distinct recall-preserving mechanism.

## Decision

Do not promote ABI-144 and do not request whole-validation diagnostics. It underperforms ABI-143, ABI-142, ABI-130, and ABI-068 on aggregate filtered Dice, and its precision/connectivity recovery is not enough to offset the loss of recall and MIT Dice.

Do not abandon SZA+BCE-Dice or BTD line-aware modeling globally. The useful next frontier is not another small ridge-gate variant; prefer broadening to a different architecture/front-end/data-policy/calibration mechanism, or returning to stronger ABI-068/ABI-130 axes with a change targeted at recall-source balance. No Capability Request, Evaluation Request, or Campaign Report is required from this result.

## Artifact references

- `run_20260831_234016_e7916c/outputs/best_metrics.json`
- `run_20260831_234016_e7916c/outputs/final_metrics.json`
- `run_20260831_234016_e7916c/outputs/metrics.jsonl`
- `run_20260831_234016_e7916c/outputs/resource_profile.json`
- `run_20260831_234016_e7916c/outputs/model_summary.json`
- `run_20260831_234016_e7916c/outputs/prediction_samples/samples.json`
- `run_20260831_234016_e7916c/resolved_manifest.yaml`
- `run_20260831_224534_27b73d/outputs/best_metrics.json`
- `run_20260831_215104_d4c318/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
