# Full-spectral BTD+SZA hybrid ridge-ASPP/detail decoder BCE-Dice follow-up

research-figures: []

## Scope

This note records ABI-147 after Run `run_20260901_021228_9ca4b9` completed.

Source Runs:

- ABI-147 full-spectral BTD+SZA hybrid ridge-ASPP/detail decoder BCE-Dice Centerline-auxiliary continuation: `run_20260901_021228_9ca4b9`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice Centerline-auxiliary comparison target: `run_20260831_121006_7d24be`
- ABI-143 SZA-aware soft ridge-gate U-Net BCE-Dice Centerline-auxiliary ridge reference: `run_20260831_224534_27b73d`
- ABI-146 SZA-aware frequency-support ASPP/detail decoder BCE-Dice negative continuation reference: `run_20260901_012037_c302cc`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice Centerline-auxiliary precision/connectivity reference: `run_20260831_085615_d05ab3`
- ABI-068 frequency-gated line U-Net focal-Tversky local capped aggregate-Dice reference: `run_20260828_010836_4ccc77`

ABI-147 was a family-development continuation of the SZA-aware full-spectral BTD BCE-Dice frontier. It kept provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features derived only from approved ABI channels, Solar Geometry Input features, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled architecture change was to fuse ABI-130-style context/detail evidence with ABI-143-style horizontal and vertical ridge residual evidence in a non-suppressive hybrid stem before the ASPP/detail decoder.

## Contract and resource observation

ABI-147 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 9,652,330 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,247.2 seconds total wall time, 1,037.1 seconds training wall time, 1,208.0 seconds validation wall time, 6,254,019,584 bytes peak CUDA allocated, 7,335,837,696 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_224534_27b73d` | ABI-143 | soft ridge-gate U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3947 | 0.3815 | 0.4287 | 0.4105 | 0.3801 | 0.3010 | 0.00336 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260901_021228_9ca4b9` | ABI-147 | hybrid ridge-ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3804 | 0.3705 | 0.4051 | 0.4260 | 0.3436 | 0.2849 | 0.00292 |
| `run_20260901_012037_c302cc` | ABI-146 | ASPP/detail decoder + frequency support, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3497 | 0.3260 | 0.4095 | 0.4914 | 0.2714 | 0.3125 | 0.00200 |

ABI-147 improved materially on the conservative ABI-146 frequency-support branch, gaining 0.0307 aggregate filtered Dice and 0.0722 filtered recall. That shows the stem-level non-suppressive ridge fusion was less damaging than late frequency-support fusion. However, ABI-147 did not meet its stated success criteria relative to the intended ABI-130 and ABI-143 comparisons.

Relative to ABI-130, ABI-147 lost 0.0149 aggregate filtered Dice, 0.0074 MIT filtered Dice, 0.0353 Google filtered Dice, 0.0155 precision, 0.0142 recall, and 0.1002 connectivity while leaving predicted-positive fraction essentially unchanged. Relative to ABI-143, ABI-147 lost 0.0144 aggregate filtered Dice, 0.0111 MIT filtered Dice, 0.0237 Google filtered Dice, 0.0365 recall, and 0.0161 connectivity; the 0.0154 precision gain was not enough to offset the overlap and source losses. Relative to ABI-126, ABI-147 slightly improved MIT Dice and recall but lost 0.0055 aggregate filtered Dice, 0.0364 Google filtered Dice, 0.0487 precision, and 0.1668 connectivity. Relative to ABI-068, ABI-147 remained lower on aggregate/source Dice, recall, and connectivity.

## ABI-147 trajectory

ABI-147 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.1879, 0.2464, 0.2933, 0.3123, 0.3415, 0.3265, 0.3381, 0.3559, 0.3761, 0.3482, 0.3750, and 0.3804. The selected checkpoint was epoch 12. The trajectory recovered after an epoch-10 dip and was still improving late, but by the active 12-epoch cap it remained below ABI-130, ABI-143, ABI-126, and ABI-068.

At the selected checkpoint, source-stratified filtered Dice was 0.3705 for MIT and 0.4051 for Google. MIT had filtered precision 0.4388, recall 0.3205, connectivity 0.3284, and predicted-positive fraction 0.00353. Google had filtered precision 0.3993, recall 0.4111, connectivity 0.2413, and predicted-positive fraction 0.00168. The branch is not numerically failed or collapsed; its failure mode is that the hybrid stem weakens Google overlap and source-balanced connectivity without delivering the intended MIT recall recovery.

Raw-to-filtered differences were modest at the best checkpoint: raw Dice was 0.3946 versus filtered Dice 0.3804, and raw predicted-positive fraction was 0.00316 versus filtered 0.00292. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples remain traceability artifacts under the `first_n` retention policy and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-147 as a completed, finite, non-collapsed, negative controlled architecture-continuation result for the SZA-aware ASPP/detail/ridge BCE-Dice branch. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch. It did confirm that non-suppressive stem-level ridge evidence is safer than the late conservative ABI-146 frequency-support addition, but the hybrid did not preserve ABI-130's Google/calibration advantage or ABI-143's MIT-recall behavior.

This narrows the SZA-aware BCE-Dice micro-architecture branch rather than eliminating all full-spectral BTD+SZA modeling. ABI-130 remains the stronger SZA-aware ASPP/detail point, ABI-143 remains the stronger ridge-aware BCE-Dice point, ABI-126 remains the stronger ASPP/detail precision/connectivity comparator, and ABI-068 remains the local capped aggregate filtered-Dice reference. The last several SZA-aware BCE-Dice refinements have tended to trade small precision or structural changes against source/connection losses, so future work should broaden beyond additional minor ridge/detail/stem edits unless a new mechanism directly targets the observed source-balanced connectivity gap.

## Decision

Do not promote ABI-147 and do not request whole-validation diagnostics for it. The run underperforms ABI-130, ABI-143, ABI-126, and ABI-068 on aggregate filtered Dice and has no compensating MIT, Google, recall, or connectivity advantage. It satisfies the proposal's hard-stop condition for this exact hybrid ridge-ASPP stem branch: aggregate filtered Dice is below ABI-130/ABI-143 and the intended source/connectivity tradeoff did not appear.

Stop this exact hybrid ridge-ASPP stem continuation branch. Future work should broaden away from SZA-aware BCE-Dice micro-architecture tweaks toward a distinct architecture family, preprocessing/front-end, training-policy/data-policy, calibration, mining, or diagnostic frontier under the existing contract. No Capability Request, Evaluation Request, or Campaign Report is required from ABI-147.

## Artifact references

- `run_20260901_021228_9ca4b9/outputs/best_metrics.json`
- `run_20260901_021228_9ca4b9/outputs/final_metrics.json`
- `run_20260901_021228_9ca4b9/outputs/metrics.jsonl`
- `run_20260901_021228_9ca4b9/outputs/resource_profile.json`
- `run_20260901_021228_9ca4b9/outputs/model_summary.json`
- `run_20260901_021228_9ca4b9/outputs/prediction_samples/samples.json`
- `run_20260901_021228_9ca4b9/resolved_manifest.yaml`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_224534_27b73d/outputs/best_metrics.json`
- `run_20260901_012037_c302cc/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
