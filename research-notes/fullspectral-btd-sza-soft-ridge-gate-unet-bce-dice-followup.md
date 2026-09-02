# Full-spectral BTD+SZA soft ridge-gate U-Net BCE-Dice follow-up

research-figures: []

## Scope

This note records ABI-143 after Run `run_20260831_224534_27b73d` completed.

Source Runs:

- ABI-143 full-spectral BTD+SZA soft ridge-gate U-Net BCE-Dice Centerline-auxiliary continuation: `run_20260831_224534_27b73d`
- ABI-142 multiscale ridge-attention U-Net BCE-Dice predecessor: `run_20260831_215104_d4c318`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice Centerline-auxiliary reference: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice high-precision/connectivity comparator: `run_20260831_085615_d05ab3`

ABI-143 was a controlled family-development continuation of ABI-142. It kept provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features derived only from approved ABI channels, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled architectural change was a neutral-initialized, conservatively bounded final ridge gate.

## Contract and resource observation

ABI-143 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 9,617,130 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,806.6 seconds total wall time, 1,464.0 seconds training wall time, 1,340.4 seconds validation wall time, 6,675,088,896 bytes peak CUDA allocated, 7,327,449,088 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_224534_27b73d` | ABI-143 | soft ridge-gate U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3947 | 0.3815 | 0.4287 | 0.4105 | 0.3801 | 0.3010 | 0.00336 |
| `run_20260831_215104_d4c318` | ABI-142 | multiscale ridge-attention U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3935 | 0.3762 | 0.4373 | 0.4398 | 0.3561 | 0.3819 | 0.00293 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |

ABI-143 is close to the capped reference band but does not beat the current capped best ABI-068 or the strongest SZA-aware ASPP/detail branch ABI-130. Versus ABI-068, ABI-143 is lower by 0.0016 aggregate filtered Dice, 0.0071 MIT filtered Dice, 0.0126 filtered precision, 0.0135 filtered recall, and 0.0890 connectivity, while Google filtered Dice is higher by 0.0126. Versus ABI-130, ABI-143 is lower by only 0.0005 aggregate filtered Dice and has higher MIT Dice and recall, but lower Google Dice, precision, and connectivity.

The controlled soft-gate change did improve aggregate filtered Dice relative to ABI-142 by +0.0012 and MIT filtered Dice by +0.0053. It also increased filtered recall by +0.0240 and the filtered predicted-positive fraction from 0.00293 to 0.00336. The tradeoff is meaningful: Google filtered Dice fell by 0.0086, filtered precision fell by 0.0292, and filtered connectivity fell by 0.0809. This suggests the conservative ridge gate reduced some MIT under-recall from ABI-142 but also weakened the original ridge-attention branch's cleaner line structure.

## ABI-143 trajectory

ABI-143 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.2107, 0.2509, 0.2859, 0.3038, 0.3443, 0.3591, 0.3513, 0.3650, 0.3740, 0.3652, 0.3766, and 0.3947. The final epoch was the selected best checkpoint, and the late improvement from epochs 8-12 argues against an optimization hard stop at the active budget.

The best checkpoint showed source-stratified filtered Dice of 0.3815 for MIT and 0.4287 for Google. MIT had filtered precision 0.4124, recall 0.3549, connectivity 0.3100, and predicted-positive fraction 0.00465. Google had filtered precision 0.4063, recall 0.4539, connectivity 0.2920, and predicted-positive fraction 0.00206. Both Dataset Sources were finite and non-collapsed.

Raw-to-filtered differences were modest at the best checkpoint: raw Dice was 0.4083 versus filtered Dice 0.3947, and raw predicted-positive fraction was 0.00359 versus filtered 0.00336. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples contain one empty-background perfect case and three near-zero overlap cases under the `first_n` retention policy; these bounded artifacts are traceability artifacts and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-143 as a completed, finite, non-collapsed, mixed-positive ridge-family continuation. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch. The controlled soft-gate hypothesis partially worked for aggregate Dice and MIT recall, but the loss of connectivity and Google precision/source balance is enough to avoid treating this branch as a new leading direction.

The ridge-gate family is still not disproven by one scout plus one controlled continuation: both ABI-142 and ABI-143 reached the current capped reference band within roughly 0.003 filtered Dice. However, ABI-143 makes the ridge-gate mechanism's tradeoff clearer. A softer ridge gate moves the operating point toward recall and positive area, while the original ABI-142 behavior retained better precision/connectivity. Future work should not simply repeat the same soft-gate variant; it should either test a distinct connectivity-preserving ridge mechanism or return to the stronger ABI-068/ABI-130 axes.

## Decision

Do not promote ABI-143 from representative capped evidence and do not request whole-validation diagnostics yet. It narrowly misses ABI-068 and ABI-130 on aggregate filtered Dice and lacks a distinctive connectivity or source-balance advantage.

Do not abandon ridge-aware SZA+BCE-Dice modeling solely from this result. If revisited, prefer a bounded, mechanism-specific continuation that preserves the recall gains without sacrificing line connectivity, or broaden back to the frequency-gated/ASPP-detail frontier. No Capability Request, Evaluation Request, or Campaign Report is required from this result.

## Artifact references

- `run_20260831_224534_27b73d/outputs/best_metrics.json`
- `run_20260831_224534_27b73d/outputs/final_metrics.json`
- `run_20260831_224534_27b73d/outputs/metrics.jsonl`
- `run_20260831_224534_27b73d/outputs/resource_profile.json`
- `run_20260831_224534_27b73d/outputs/model_summary.json`
- `run_20260831_224534_27b73d/outputs/prediction_samples/samples.json`
- `run_20260831_224534_27b73d/resolved_manifest.yaml`
- `run_20260831_215104_d4c318/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
