# Full-spectral BTD+SZA compact BiFPN multiscale line-head follow-up

research-figures: []

## Scope

This note records ABI-170 after Run `run_20260901_212305_8ff75d` completed.

Source Runs:

- ABI-170 compact BiFPN multiscale line-continuity head continuation: `run_20260901_212305_8ff75d`
- ABI-162 compact BiFPN line-fusion BCE-Dice parent: `run_20260901_142708_a2f6c9`
- ABI-163 compact BiFPN line-fusion focal-Tversky comparison: `run_20260901_150632_dc4961`
- ABI-154 full-scale skip ASPP/detail decoder BCE-Dice reference: `run_20260901_071026_32d3ec`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice reference: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net focal-Tversky current capped aggregate-Dice reference: `run_20260828_010836_4ccc77`

ABI-170 was a controlled architecture continuation of ABI-162. It kept provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD features derived only from approved ABI channels, normalized/cosine Solar Geometry Input features, compact residual encoder, positive normalized BiFPN top-down/bottom-up fusion, BCE-Dice primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled change was replacing ABI-162's short line-context head with a lightweight multiscale horizontal/vertical line-continuity head.

## Contract and resource observation

ABI-170 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved GOES ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 2,255,842 parameters, below the 25,000,000-parameter smoke ceiling and only modestly larger than ABI-162/ABI-163's 2,058,786-parameter compact BiFPN shape. The Run completed on the A100 at batch size 4 with 1,983.0 seconds total wall time, 811.5 seconds training wall time, 1,169.9 seconds validation wall time, 30.28 training samples per second, 21.01 validation samples per second, 6,336,093,696 bytes peak CUDA allocated, and 7,509,901,312 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 9 rather than the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260901_142708_a2f6c9` | ABI-162 | compact BiFPN line-fusion U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3738 | 0.3576 | 0.4133 | 0.4242 | 0.3342 | 0.3256 | 0.00285 |
| `run_20260901_150632_dc4961` | ABI-163 | compact BiFPN line-fusion U-Net, focal-Tversky, ABI-16+BTD+SZA | 11 | 0.3462 | 0.3568 | 0.3232 | 0.2889 | 0.4320 | 0.1540 | 0.00542 |
| `run_20260901_212305_8ff75d` | ABI-170 | compact BiFPN multiscale line head, BCE-Dice, ABI-16+BTD+SZA | 9 | 0.3674 | 0.3511 | 0.4067 | 0.4148 | 0.3298 | 0.2155 | 0.00288 |

ABI-170 did not meet its useful-outcome criteria. Relative to ABI-162, aggregate filtered Dice fell from 0.3738 to 0.3674 (-0.0064), MIT filtered Dice fell from 0.3576 to 0.3511 (-0.0066), Google filtered Dice fell from 0.4133 to 0.4067 (-0.0066), filtered precision fell from 0.4242 to 0.4148 (-0.0094), filtered recall fell from 0.3342 to 0.3298 (-0.0044), and filtered connectivity fell from 0.3256 to 0.2155 (-0.1101). Filtered predicted-positive fraction stayed essentially unchanged at 0.00288 versus ABI-162's 0.00285, so the regression is not an ABI-163-like overprediction failure; it is a weaker line/connectivity result at a similar operating area.

Relative to ABI-163, ABI-170 recovered precision (+0.1259), Google filtered Dice (+0.0835), and aggregate Dice (+0.0212) while reducing predicted-positive fraction. However, ABI-170 did not preserve ABI-163's recall, and it still trailed ABI-162's BCE-Dice parent on the intended connectivity target. Relative to the stronger capped references, ABI-170 remains below ABI-068, ABI-130, and ABI-154 on aggregate filtered Dice, both source-stratified Dice values, recall, and connectivity. It is also below ABI-130 and ABI-154 on precision.

## ABI-170 trajectory

ABI-170 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.2025, 0.2723, 0.2845, 0.3034, 0.3101, 0.2489, 0.3373, 0.3480, 0.3674, 0.3202, 0.3643, and 0.3582. The selected best checkpoint was epoch 9. The run showed meaningful learning from epoch 1 to epoch 9, but the late trajectory was noisy and did not improve the primary metric over the ABI-162 parent.

At the best epoch, raw Dice was 0.3820, filtered Dice was 0.3674, filtered precision was 0.4148, filtered recall was 0.3298, filtered connectivity was 0.2155, and filtered predicted-positive fraction was 0.00288. Source-stratified filtered Dice was 0.3511 for MIT and 0.4067 for Google. MIT had filtered precision 0.4260, recall 0.2986, connectivity 0.2435, and predicted-positive fraction 0.00379. Google had filtered precision 0.3934, recall 0.4210, connectivity 0.1875, and predicted-positive fraction 0.00198.

The final epoch shifted to a more conservative operating point but still did not rescue the hypothesis: final filtered Dice was 0.3582, MIT/Google filtered Dice was 0.3405/0.3997, filtered precision was 0.4422, filtered recall was 0.3010, filtered connectivity was 0.2555, and filtered predicted-positive fraction was 0.00247. Final connectivity improved over epoch 9 but remained substantially below ABI-162's 0.3256 and below ABI-068/130/154. Raw-to-filtered differences were modest at the selected checkpoint: raw Dice was 0.3820 versus filtered Dice 0.3674, raw recall 0.3526 versus filtered recall 0.3298, and raw predicted-positive fraction 0.00307 versus filtered 0.00288. This does not indicate primary Artifact Filter dependence.

The fixed first-four retained prediction samples all have near-zero per-sample Dice under the `first_n` retention policy. These artifacts remain useful for traceability, but they should not be treated as representative qualitative evidence for the full validation distribution.

## Interpretation

Classify ABI-170 as a completed, finite, non-collapsed, scientifically negative result for the compact BiFPN multiscale line-head continuation. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The result answers the ABI-162 follow-up hypothesis negatively. Adding a stronger multiscale horizontal/vertical feature-space line-continuity head did not improve the compact BiFPN branch's connectivity, source balance, or aggregate fixed-threshold overlap. Instead, it preserved roughly the same predicted-positive area as ABI-162 while lowering connectivity and slightly lowering both Dataset Source Dice values. This suggests the compact BiFPN bottleneck/fusion topology is not merely missing a larger terminal line-support head; its weaker continuity is likely upstream in feature organization, calibration, or loss/data-policy interaction.

The broader compact BiFPN branch now has three bounded observations: ABI-161 full-width timed out; ABI-162 compact BCE-Dice completed and improved through epoch 12 but was below the main references; ABI-163 focal-Tversky over-shifted toward recall with poor precision/connectivity; ABI-170's multiscale line-head attempt did not improve ABI-162. Low score alone was not used to abandon the family after one run, but this sequence is enough to stop the exact compact BiFPN line-head tuning path unless a later hypothesis changes a more fundamental factor.

## Decision

Do not promote ABI-170 and do not request whole-validation diagnostics for it. Stop the exact ABI-170 multiscale line-head branch. No Capability Request or Campaign Report is required from this result.

For a later Autonomy Step, prefer broadening away from compact BiFPN terminal line-head tuning. Reasonable next frontiers include the already motivated ABI-154 whole-validation failure-bucket evidence path, a different calibration/data-policy mechanism that preserves ABI-154-like precision/connectivity while recovering recall, or a new architecture family with a more explicit high-resolution thin-line representation. Avoid another local compact BiFPN head-only follow-up unless it changes a materially different factor and has a specific reason to overcome the ABI-162/163/170 failure modes.

## Artifact references

- `run_20260901_212305_8ff75d/outputs/best_metrics.json`
- `run_20260901_212305_8ff75d/outputs/final_metrics.json`
- `run_20260901_212305_8ff75d/outputs/metrics.jsonl`
- `run_20260901_212305_8ff75d/outputs/resource_profile.json`
- `run_20260901_212305_8ff75d/outputs/model_summary.json`
- `run_20260901_212305_8ff75d/outputs/prediction_samples/samples.json`
- `run_20260901_212305_8ff75d/resolved_manifest.yaml`
- `run_20260901_142708_a2f6c9/outputs/best_metrics.json`
- `run_20260901_150632_dc4961/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
