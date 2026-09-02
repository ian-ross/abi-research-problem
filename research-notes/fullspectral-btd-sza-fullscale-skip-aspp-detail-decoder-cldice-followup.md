# Full-spectral BTD+SZA full-scale skip ASPP/detail decoder clDice follow-up

research-figures: []

## Scope

This note records ABI-169 after Run `run_20260901_202820_08734b` completed.

Source Runs:

- ABI-169 full-spectral BTD+SZA full-scale skip ASPP/detail decoder BCE-Dice-clDice Centerline-auxiliary continuation: `run_20260901_202820_08734b`
- ABI-154 full-scale skip ASPP/detail decoder BCE-Dice parent: `run_20260901_071026_32d3ec`
- ABI-153 soft ridge-gate U-Net BCE-Dice-clDice nearby loss-swap comparison: `run_20260901_061306_9b10a4`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice reference: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net focal-Tversky local capped aggregate-Dice reference: `run_20260828_010836_4ccc77`

ABI-169 was a controlled loss-policy continuation of ABI-154. It kept provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features derived only from approved ABI channels, normalized Solar Geometry Input features, the full-scale skip ASPP/detail decoder architecture, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled manifest change was switching the trusted primary loss from `bce_dice` to `bce_dice_cldice`.

## Contract and resource observation

ABI-169 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 9,741,850 parameters, below the 25,000,000-parameter smoke ceiling and matching the ABI-154 parent architecture size. The Run completed on the A100 at batch size 4 with 2,720.0 seconds total wall time, 1,398.7 seconds training wall time, 1,319.1 seconds validation wall time, 17.57 training samples per second, 18.63 validation samples per second, 8,147,817,472 bytes peak CUDA allocated, and 9,632,219,136 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260901_061306_9b10a4` | ABI-153 | soft ridge-gate U-Net, BCE-Dice-clDice, ABI-16+BTD+SZA | 11 | 0.3739 | 0.3701 | 0.3825 | 0.3591 | 0.3899 | 0.3234 | 0.00393 |
| `run_20260901_202820_08734b` | ABI-169 | full-scale skip ASPP/detail decoder, BCE-Dice-clDice, ABI-16+BTD+SZA | 12 | 0.3688 | 0.3645 | 0.3785 | 0.3878 | 0.3515 | 0.2813 | 0.00328 |

ABI-169 did not meet the controlled loss-swap success criteria. Relative to ABI-154, aggregate filtered Dice fell from 0.3944 to 0.3688 (-0.0257), MIT filtered Dice fell from 0.3824 to 0.3645 (-0.0179), Google filtered Dice fell from 0.4260 to 0.3785 (-0.0475), filtered precision fell from 0.4777 to 0.3878 (-0.0899), and filtered connectivity fell from 0.4374 to 0.2813 (-0.1562). Filtered recall increased from 0.3359 to 0.3515 (+0.0156), and predicted-positive fraction increased from 0.00255 to 0.00328, but the recall gain was much too small to offset the loss of precision, source Dice, and connectivity.

Relative to ABI-130, ABI-169 is lower on aggregate filtered Dice (-0.0265), MIT filtered Dice (-0.0134), Google filtered Dice (-0.0619), precision (-0.0537), recall (-0.0063), and connectivity (-0.1038). Relative to ABI-068, it is lower on aggregate/source Dice, precision, recall, and connectivity, with only slightly lower predicted-positive fraction. The run is also weaker than the earlier ABI-153 clDice loss swap: ABI-169 is slightly lower on aggregate/source Dice and materially lower on recall and connectivity, though it is more conservative on precision and predicted-positive fraction.

## ABI-169 trajectory

ABI-169 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.1622, 0.2378, 0.2869, 0.2778, 0.3109, 0.2955, 0.3219, 0.3390, 0.3509, 0.3554, 0.3190, and 0.3688. The final epoch was the selected checkpoint and the best capped filtered Dice for this Run.

The late trajectory remained noisy rather than clearly converged. Epoch 10 reached 0.3554 filtered Dice with the run's strongest connectivity, 0.3387; epoch 11 regressed to 0.3190; epoch 12 recovered to the primary-metric best, but with lower connectivity, 0.2813. At the selected checkpoint, raw Dice was 0.3824, filtered Dice was 0.3688, filtered precision was 0.3878, filtered recall was 0.3515, filtered connectivity was 0.2813, and filtered predicted-positive fraction was 0.00328. Source-stratified filtered Dice was 0.3645 for MIT and 0.3785 for Google. MIT had filtered precision 0.4154, recall 0.3247, connectivity 0.3159, and predicted-positive fraction 0.00422; Google had filtered precision 0.3382, recall 0.4297, connectivity 0.2467, and predicted-positive fraction 0.00235.

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice was 0.3824 versus filtered Dice 0.3688, raw recall was 0.3753 versus filtered recall 0.3515, and raw predicted-positive fraction was 0.00349 versus filtered 0.00328. This does not indicate primary Artifact Filter dependence. The fixed first-four prediction artifacts include one empty/negative perfect case and three near-zero per-sample Dice cases under the `first_n` retention policy; these artifacts are traceability samples and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-169 as a completed, finite, non-collapsed, scientifically negative controlled loss-swap result for the full-scale skip ASPP/detail decoder branch. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The BCE-Dice-clDice loss did not provide the intended continuity improvement on the full-scale skip ASPP/detail architecture. Instead, it shifted the operating point modestly toward recall and larger predicted-positive area while sharply degrading the parent branch's main strength: high precision and high connectivity. This is consistent with the ABI-153 result, where a clDice substitution in a nearby SZA-aware branch did not recover enough useful continuity to compensate for lower source-balanced overlap. For this architecture, the trusted clDice primary loss appears to interfere with the BCE-Dice full-scale skip calibration rather than preserving its connected, precise masks.

The result does not eliminate clDice globally or invalidate the ABI-154 architecture. It specifically weakens simple `bce_dice` to `bce_dice_cldice` swaps on SZA-aware full-scale skip / ridge-adjacent branches with Centerline Target auxiliary supervision at learning rate 0.0003. ABI-154 remains the stronger full-scale skip result, and ABI-068/ABI-130 remain the principal capped references.

## Decision

Do not promote ABI-169 and do not request whole-validation diagnostics for it. Stop the exact ABI-154-to-ABI-169 clDice loss-swap branch. No Capability Request or Campaign Report is required from this result.

For a later Autonomy Step, prefer either the already-motivated whole-validation failure-bucket Evaluation Request for ABI-154, or broaden away from simple clDice substitutions toward a distinct calibration/data-policy/architecture mechanism that preserves ABI-154-like precision and connectivity while recovering recall. Avoid another local clDice-only follow-up unless it changes a materially different factor and has a specific reason to avoid the precision/connectivity collapse seen in ABI-153 and ABI-169.

## Artifact references

- `run_20260901_202820_08734b/outputs/best_metrics.json`
- `run_20260901_202820_08734b/outputs/final_metrics.json`
- `run_20260901_202820_08734b/outputs/metrics.jsonl`
- `run_20260901_202820_08734b/outputs/resource_profile.json`
- `run_20260901_202820_08734b/outputs/model_summary.json`
- `run_20260901_202820_08734b/outputs/prediction_samples/samples.json`
- `run_20260901_202820_08734b/resolved_manifest.yaml`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260901_061306_9b10a4/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
