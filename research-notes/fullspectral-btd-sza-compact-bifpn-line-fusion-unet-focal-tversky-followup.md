# Full-spectral BTD+SZA compact BiFPN line-fusion U-Net focal-Tversky follow-up

research-figures: []

## Scope

This note records ABI-163 after completion of the compact BiFPN line-fusion focal-Tversky continuation.

Source Runs:

- ABI-163 compact BiFPN line-fusion U-Net focal-Tversky continuation: `run_20260901_150632_dc4961`
- ABI-162 compact BiFPN line-fusion U-Net BCE-Dice comparison target: `run_20260901_142708_a2f6c9`
- ABI-161 full-width BiFPN line-fusion U-Net resource-failed scout: `run_20260901_132157_1d849b`
- ABI-160 mid-level directional-context ASPP/detail decoder reference: `run_20260901_123418_da6b1e`
- ABI-154 full-scale skip ASPP/detail decoder reference: `run_20260901_071026_32d3ec`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice reference: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net focal-Tversky capped reference: `run_20260828_010836_4ccc77`

ABI-163 preserved ABI-162's compact resource-feasible BiFPN architecture and changed only the trusted primary loss from `bce_dice` to `focal_tversky`. The intended test was whether the compact bidirectional pyramid branch was under-recalled because of the BCE-Dice loss axis rather than because of the architecture topology.

## Contract and resource observation

ABI-163 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records provider-approved `abi_16ch_plus_sza` input with GOES ABI source channel indices 0-15 plus Solar Geometry source channel index 18; forbidden longitude and latitude source channel indices 16 and 17 are excluded. The model outputs `mask_logits` and provider-derived `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

ABI-163 reported 2,058,786 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 1,853.4 seconds total wall time, 694.8 seconds training wall time, 1,157.0 seconds validation wall time, 35.37 training samples per second, 21.24 validation samples per second, 5,259,978,752 bytes peak CUDA allocated, 6,289,358,848 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260901_123418_da6b1e` | ABI-160 | mid-level directional-context ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 11 | 0.3831 | 0.3819 | 0.3861 | 0.4023 | 0.3656 | 0.3252 | 0.00329 |
| `run_20260901_142708_a2f6c9` | ABI-162 | compact BiFPN line-fusion U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3738 | 0.3576 | 0.4133 | 0.4242 | 0.3342 | 0.3256 | 0.00285 |
| `run_20260901_150632_dc4961` | ABI-163 | compact BiFPN line-fusion U-Net, focal-Tversky, ABI-16+BTD+SZA | 11 | 0.3462 | 0.3568 | 0.3232 | 0.2889 | 0.4320 | 0.1540 | 0.00542 |

The loss-axis change had the expected direction on recall but not on the primary Result. Relative to ABI-162, ABI-163 improved filtered recall by +0.0978 and increased filtered predicted-positive fraction from 0.00285 to 0.00542. However, filtered precision fell by -0.1353, aggregate filtered Dice fell by -0.0276, Google filtered Dice fell by -0.0901, MIT filtered Dice was effectively flat to slightly lower (-0.0008), and filtered connectivity fell by -0.1716. This is not a promotion candidate and does not beat the current capped references.

Relative to ABI-068, ABI-163 lost aggregate filtered Dice (-0.0501), MIT Dice (-0.0318), Google Dice (-0.0929), precision (-0.1103), and connectivity (-0.2360), while recall was higher (+0.0384). Relative to ABI-154, ABI-163 lost aggregate filtered Dice (-0.0482), MIT Dice (-0.0256), Google Dice (-0.1028), precision (-0.1888), and connectivity (-0.2835), while recall was higher (+0.0961). The focal-Tversky BiFPN branch therefore recovered sensitivity by accepting substantially more clutter and weaker connected line structure.

## ABI-163 trajectory

ABI-163 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.1649, 0.1744, 0.2241, 0.2610, 0.2792, 0.2235, 0.2638, 0.3396, 0.3118, 0.2981, 0.3462, and 0.3416. The selected best checkpoint was epoch 11, with a small final-epoch primary-metric decline but continued validation-loss improvement.

At the best epoch, filtered precision was 0.2889, filtered recall was 0.4320, filtered connectivity was 0.1540, and filtered predicted-positive fraction was 0.00542. Source-stratified filtered Dice was 0.3568 for MIT and 0.3232 for Google. At the final epoch, aggregate filtered Dice was 0.3416, filtered precision 0.2968, filtered recall 0.4023, filtered connectivity 0.1884, MIT filtered Dice 0.3508, and Google filtered Dice 0.3227. Raw-to-filtered differences were modest at final epoch (raw Dice 0.3523 versus filtered Dice 0.3416; raw recall 0.4295 versus filtered recall 0.4023), so the poor outcome is not primarily explained by Artifact Filter dependence.

## Interpretation

Classify ABI-163 as a completed, finite, non-collapsed but negative scientific result for the focal-Tversky loss axis on the compact BiFPN line-fusion branch. It answers the specific ABI-162 follow-up question: focal-Tversky can recover recall, but in this topology it does so by over-predicting and losing precision, Google-side Dice, and connected thin-line quality. The branch did not show a useful recall/precision balance or continuity recovery under the capped 12-epoch budget.

This does not invalidate focal-Tversky in general, because ABI-068 remains the current best capped Result with focal-Tversky in a different frequency-gated line U-Net architecture. The negative evidence is specific to applying focal-Tversky to ABI-162's compact BiFPN line-fusion topology.

## Decision

Do not promote ABI-163 and do not repeat the compact BiFPN focal-Tversky loss branch unchanged. ABI-163 also does not justify whole-validation diagnostics: the primary capped result is substantially below ABI-068/ABI-130/ABI-154, and the observed failure mode is already clear from aggregate/source metrics and trajectory.

The compact BiFPN branch now has one BCE-Dice run that was precision-skewed but under-recalled, and one focal-Tversky run that overcorrected toward recall with poor precision and connectivity. A further BiFPN continuation would need a genuinely different lightweight calibration/continuity mechanism with strong rationale; otherwise the next autonomy step should broaden away from compact BiFPN toward another architecture, data-policy, loss, or preprocessing frontier rather than spending another run on this exact branch. No Capability Request, Evaluation Request, or Campaign Report is required from ABI-163.

## Artifact references

- `run_20260901_150632_dc4961/outputs/best_metrics.json`
- `run_20260901_150632_dc4961/outputs/final_metrics.json`
- `run_20260901_150632_dc4961/outputs/metrics.jsonl`
- `run_20260901_150632_dc4961/outputs/resource_profile.json`
- `run_20260901_150632_dc4961/outputs/model_summary.json`
- `run_20260901_150632_dc4961/outputs/prediction_samples/samples.json`
- `run_20260901_150632_dc4961/resolved_manifest.yaml`
- `run_20260901_142708_a2f6c9/outputs/best_metrics.json`
- `run_20260901_142708_a2f6c9/outputs/final_metrics.json`
- `run_20260901_132157_1d849b/outputs/logs/harness_timeout.log`
- `run_20260901_123418_da6b1e/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
