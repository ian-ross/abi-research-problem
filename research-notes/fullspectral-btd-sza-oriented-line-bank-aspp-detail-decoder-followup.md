# Full-spectral BTD+SZA oriented line-bank ASPP/detail decoder follow-up

research-figures: []

## Scope

This note records ABI-166 after completion of the oriented line-bank ASPP/detail decoder continuation.

Source Runs:

- ABI-166 oriented line-bank ASPP/detail decoder continuation: `run_20260901_173120_9c74ab`
- ABI-154 full-scale skip ASPP/detail decoder high-precision/connectivity reference: `run_20260901_071026_32d3ec`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice reference: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net focal-Tversky capped reference: `run_20260828_010836_4ccc77`
- ABI-165 soft ridge-gate U-Net Line+Centerline auxiliary recent negative continuation: `run_20260901_163629_b45b2d`

ABI-166 kept provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features derived from allowed GOES ABI channels, trusted BCE-Dice primary loss, trusted random mirroring, combined source-balanced traversal, and a low-weight provider-derived Centerline Target auxiliary head. The controlled architecture change was an oriented full-resolution line-bank refinement combining local, horizontal, vertical, and two diagonal feature-context branches before the final mask and centerline heads. The intended test was whether explicit multi-orientation line evidence could improve thin-contrail continuity without relying on candidate-owned thresholding, postprocessing, or extra target derivation.

## Contract and resource observation

ABI-166 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records provider-approved `abi_16ch_plus_sza` input with GOES ABI source channel indices 0-15 plus Solar Geometry source channel index 18; forbidden longitude and latitude source channel indices 16 and 17 are excluded. The model emitted provider-shaped `mask_logits` and `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

ABI-166 reported 9,777,210 parameters, below the 25,000,000-parameter smoke ceiling. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The Run completed 12 epochs at batch size 4 on the A100 with 2,673.3 seconds run wall time, 1,356.8 seconds training wall time, 1,314.2 seconds validation wall time, 18.11 training samples per second, 18.70 validation samples per second, 8,524,755,456 bytes peak CUDA allocated, and 10,366,222,336 bytes peak CUDA reserved.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260901_163629_b45b2d` | ABI-165 | soft ridge-gate U-Net, BCE-Dice, Line+Centerline aux, ABI-16+BTD+SZA | 9 | 0.3887 | 0.3767 | 0.4172 | 0.3874 | 0.3901 | 0.3215 | 0.00365 |
| `run_20260901_173120_9c74ab` | ABI-166 | oriented line-bank ASPP/detail decoder, BCE-Dice, Centerline aux, ABI-16+BTD+SZA | 12 | 0.3785 | 0.3628 | 0.4144 | 0.4077 | 0.3532 | 0.3221 | 0.00314 |

Relative to ABI-154, ABI-166 improved filtered recall by +0.0174 and increased filtered predicted-positive fraction by +0.00059, but filtered Dice fell by -0.0159, MIT filtered Dice by -0.0196, Google filtered Dice by -0.0116, filtered precision by -0.0700, and filtered connectivity by -0.1153. This does not satisfy the intended line-bank criterion of preserving ABI-154's high-connectivity operating point.

Relative to ABI-130, ABI-166 was lower on aggregate filtered Dice (-0.0168), MIT filtered Dice (-0.0151), Google filtered Dice (-0.0260), precision (-0.0338), recall (-0.0046), and connectivity (-0.0630). Relative to ABI-068, ABI-166 had slightly higher precision (+0.0085) and nearly matched Google filtered Dice (-0.0017), but aggregate filtered Dice (-0.0179), MIT filtered Dice (-0.0258), recall (-0.0404), and connectivity (-0.0679) were materially lower. Relative to ABI-165, the oriented line-bank traded higher precision (+0.0203) for lower recall (-0.0369) and lower filtered Dice (-0.0102), while connectivity was effectively unchanged (+0.0006).

## ABI-166 trajectory

ABI-166 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.1909, 0.2614, 0.2730, 0.2900, 0.3231, 0.3598, 0.3545, 0.3598, 0.3648, 0.3308, 0.3670, and 0.3785. The selected best checkpoint was the final epoch 12, so the branch was still improving at the active epoch ceiling.

At the selected checkpoint, filtered precision was 0.4077, filtered recall was 0.3532, filtered connectivity was 0.3221, and filtered predicted-positive fraction was 0.00314. Source-stratified filtered Dice was 0.3628 for MIT and 0.4144 for Google. Raw Dice was 0.3924 versus filtered Dice 0.3785, and raw predicted-positive fraction was 0.00333 versus filtered predicted-positive fraction 0.00314, so Artifact Filter dependence was modest and not the primary explanation for the lower score.

The four retained first-n prediction samples showed one empty/negative sample with perfect Dice and three near-zero-Dice positive samples in `outputs/prediction_samples/samples.json`. Because this fixed retention policy is not source- or morphology-stratified, the samples are only a bounded qualitative warning that early validation positives remained missed; they are not sufficient by themselves to diagnose the family.

## Interpretation

Classify ABI-166 as a completed, finite, non-collapsed but negative-to-mixed family-development result. The oriented line-bank did not deliver the hypothesized continuity improvement: connectivity remained close to ABI-165 and well below ABI-154, ABI-130, and ABI-068. It also did not recover a stronger Dice operating point; the result sits below the current capped leader band despite completing at the final epoch and showing a late upward trajectory.

The useful evidence is mechanistic rather than promotable. Adding explicit horizontal/vertical/diagonal context at the final refinement stage was not enough to preserve high-precision ASPP/detail behavior, and it did not resolve the recurring precision/recall/connectivity trade-off seen in recent local tweaks. Because the final epoch was the best checkpoint, this does not prove that oriented context as a broad idea is exhausted; it does argue against repeating this exact full-resolution oriented line-bank branch unchanged under the same BCE-Dice and Centerline-auxiliary policy.

## Decision

Do not promote ABI-166 and do not repeat this exact oriented line-bank ASPP/detail configuration unchanged. No Capability Request or Campaign Report is required from this result. A whole-validation failure-bucket Evaluation Request is not justified from ABI-166 alone because it is below the capped leaders and its failure mode is already visible in aggregate/source metrics, predicted-positive fraction, trajectory, and fixed prediction samples.

For a later Autonomy Step, prefer broadening beyond local late-stage line/refinement gates on the same ASPP/detail branch. Plausible next hypotheses include a different architecture family that embeds orientation earlier in the encoder/decoder, a calibrated operating-point evaluation for the capped leaders through trusted evaluation paths, or a data/loss/preprocessing comparison that directly targets MIT recall and connectivity without candidate-owned postprocessing.

## Artifact references

- `run_20260901_173120_9c74ab/outputs/best_metrics.json`
- `run_20260901_173120_9c74ab/outputs/final_metrics.json`
- `run_20260901_173120_9c74ab/outputs/metrics.jsonl`
- `run_20260901_173120_9c74ab/outputs/resource_profile.json`
- `run_20260901_173120_9c74ab/outputs/model_summary.json`
- `run_20260901_173120_9c74ab/outputs/prediction_samples/samples.json`
- `run_20260901_173120_9c74ab/resolved_manifest.yaml`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260901_163629_b45b2d/outputs/best_metrics.json`
