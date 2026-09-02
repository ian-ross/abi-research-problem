# Full-spectral BTD+SZA soft ridge-gate U-Net line+centerline auxiliary follow-up

research-figures: []

## Scope

This note records ABI-165 after completion of the soft ridge-gate U-Net Line+Centerline auxiliary continuation.

Source Runs:

- ABI-165 soft ridge-gate U-Net BCE-Dice Line+Centerline auxiliary continuation: `run_20260901_163629_b45b2d`
- ABI-143 soft ridge-gate U-Net BCE-Dice Centerline-only comparison target: `run_20260831_224534_27b73d`
- ABI-153 soft ridge-gate U-Net BCE-Dice-clDice Centerline-only loss-axis reference: `run_20260901_061306_9b10a4`
- ABI-142 multiscale ridge-attention U-Net predecessor: `run_20260831_215104_d4c318`
- ABI-154 full-scale skip ASPP/detail decoder high-connectivity reference: `run_20260901_071026_32d3ec`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice reference: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net focal-Tversky capped reference: `run_20260828_010836_4ccc77`

ABI-165 kept ABI-143's SZA-aware full-spectral BTD soft ridge-gate architecture and trusted BCE-Dice primary loss, then added a provider-derived `line_logits` auxiliary head at weight 0.01 beside the existing `centerline_logits` auxiliary head at weight 0.02. The intended test was whether low-weight Line Target supervision could improve connected line structure without disrupting ABI-143's near-best aggregate/source balance.

## Contract and resource observation

ABI-165 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records provider-approved `abi_16ch_plus_sza` input with GOES ABI source channel indices 0-15 plus Solar Geometry source channel index 18; forbidden longitude and latitude source channel indices 16 and 17 are excluded. The model outputs provider-shaped `mask_logits`, `line_logits`, and `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

ABI-165 reported 9,617,171 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed at batch size 4 on the A100 with 2,757.9 seconds total wall time, 1,468.2 seconds training wall time, 1,287.6 seconds validation wall time, 16.74 training samples per second, 19.09 validation samples per second, 6,676,141,056 bytes peak CUDA allocated, 7,329,546,240 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_224534_27b73d` | ABI-143 | soft ridge-gate U-Net, BCE-Dice, Centerline aux, ABI-16+BTD+SZA | 12 | 0.3947 | 0.3815 | 0.4287 | 0.4105 | 0.3801 | 0.3010 | 0.00336 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260831_215104_d4c318` | ABI-142 | multiscale ridge-attention U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3935 | 0.3762 | 0.4373 | 0.4398 | 0.3561 | 0.3819 | 0.00293 |
| `run_20260901_163629_b45b2d` | ABI-165 | soft ridge-gate U-Net, BCE-Dice, Line+Centerline aux, ABI-16+BTD+SZA | 9 | 0.3887 | 0.3767 | 0.4172 | 0.3874 | 0.3901 | 0.3215 | 0.00365 |
| `run_20260901_061306_9b10a4` | ABI-153 | soft ridge-gate U-Net, BCE-Dice-clDice, Centerline aux, ABI-16+BTD+SZA | 11 | 0.3739 | 0.3701 | 0.3825 | 0.3591 | 0.3899 | 0.3234 | 0.00393 |

Relative to ABI-143, ABI-165 improved filtered recall by +0.0100, filtered connectivity by +0.0205, and filtered predicted-positive fraction by +0.00029. Those gains were too small to preserve the primary Result: aggregate filtered Dice fell by -0.0060, MIT filtered Dice by -0.0048, Google filtered Dice by -0.0116, and filtered precision by -0.0232. Relative to ABI-068, ABI-165 was close on recall (-0.0035) and slightly higher on Google filtered Dice (+0.0011), but it remained lower on aggregate filtered Dice (-0.0076), MIT filtered Dice (-0.0119), precision (-0.0118), and connectivity (-0.0686). Relative to ABI-154, ABI-165 traded much higher recall (+0.0543) for much lower precision (-0.0903) and connectivity (-0.1160).

## ABI-165 trajectory

ABI-165 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.2208, 0.2744, 0.3118, 0.3298, 0.3525, 0.3594, 0.3620, 0.3587, 0.3887, 0.3685, 0.3566, and 0.3808. The selected best checkpoint was epoch 9; the final epoch partially recovered from the epoch 10-11 dip but remained below the selected best.

At the best epoch, filtered precision was 0.3874, filtered recall was 0.3901, filtered connectivity was 0.3215, and filtered predicted-positive fraction was 0.00365. Source-stratified filtered Dice was 0.3767 for MIT and 0.4172 for Google. At final epoch, aggregate filtered Dice was 0.3808, precision 0.4681, recall 0.3209, connectivity 0.3414, MIT filtered Dice 0.3638, and Google filtered Dice 0.4233. The final checkpoint became more precision-skewed and under-recalled than the selected best while connectivity increased slightly. Raw-to-filtered differences at final epoch were modest (raw Dice 0.3958 versus filtered Dice 0.3808; raw recall 0.3422 versus filtered recall 0.3209), so the result is not primarily explained by Artifact Filter dependence.

The four retained first-n prediction samples all had near-zero per-sample Dice in `outputs/prediction_samples/samples.json`. Because this fixed retention policy is not source- or morphology-stratified, these examples are useful only as a bounded qualitative warning that the early validation samples remained missed; they are not sufficient by themselves to diagnose the family.

## Interpretation

Classify ABI-165 as a completed, finite, non-collapsed but mixed-to-negative family-development result. The added Line Target supervision moved the soft ridge-gate branch in the intended direction for connected-line diagnostic and recall relative to ABI-143, but the improvement was not large enough to offset lost precision and lost aggregate/source filtered Dice. The best checkpoint remains in the broad capped reference band but does not challenge ABI-068, ABI-130, ABI-143, or ABI-154 on primary filtered Dice.

The result answers the narrow ABI-165 question: low-weight Line+Centerline auxiliary supervision can nudge the soft ridge-gate architecture toward more recalled, more connected masks, but in this configuration it does not deliver a better operating point than Centerline-only BCE-Dice. ABI-153 already showed that the clDice loss-axis continuation did not rescue this branch, and ABI-165 shows that simply adding a low-weight Line Target auxiliary is also insufficient.

## Decision

Do not promote ABI-165 and do not repeat this exact Line+Centerline auxiliary combination unchanged. No Capability Request or Campaign Report is required. Whole-validation diagnostics are not justified from ABI-165 alone because it is below the current capped leaders and its trade-off is already visible in aggregate/source metrics and trajectory.

For a later Autonomy Step, prefer broadening away from local soft ridge-gate auxiliary tweaks unless a new mechanism directly addresses the precision/connectivity trade-off. Plausible next frontiers include a different high-resolution line-continuity architecture, a calibrated threshold/operating-point study through trusted evaluation paths, a data-policy comparison if allowed by the Harness, or another preprocessing/channel-mixing family that is not just a weight tweak on the same ridge-gate branch.

## Artifact references

- `run_20260901_163629_b45b2d/outputs/best_metrics.json`
- `run_20260901_163629_b45b2d/outputs/final_metrics.json`
- `run_20260901_163629_b45b2d/outputs/metrics.jsonl`
- `run_20260901_163629_b45b2d/outputs/resource_profile.json`
- `run_20260901_163629_b45b2d/outputs/model_summary.json`
- `run_20260901_163629_b45b2d/outputs/prediction_samples/samples.json`
- `run_20260901_163629_b45b2d/resolved_manifest.yaml`
- `run_20260831_224534_27b73d/outputs/best_metrics.json`
- `run_20260901_061306_9b10a4/outputs/best_metrics.json`
- `run_20260831_215104_d4c318/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
