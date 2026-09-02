# Full-spectral BTD+SZA compact sparse-oriented ASPP/detail decoder follow-up

research-figures: []

## Scope

This note records ABI-167 and ABI-168 after ABI-168 completed the compact sparse-oriented ASPP/detail decoder continuation.

Source Runs:

- ABI-167 dense early-oriented ASPP/detail decoder predecessor: `run_20260901_182419_ca8406`
- ABI-168 compact sparse-oriented ASPP/detail decoder continuation: `run_20260901_192929_0da8c3`
- ABI-166 late oriented line-bank ASPP/detail decoder comparison target: `run_20260901_173120_9c74ab`
- ABI-154 full-scale skip ASPP/detail decoder high-precision/connectivity reference: `run_20260901_071026_32d3ec`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice reference: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net focal-Tversky capped reference: `run_20260828_010836_4ccc77`

ABI-167 tried to embed neutral horizontal, vertical, and diagonal oriented context throughout the encoder and decoder, but the Harness classified it as a `resource_failure` after the Docker training wall-clock budget was exhausted. ABI-168 preserved the scientific idea while reducing base width, learned front-end projection width, full-scale skip branch width, and the number of oriented-context placements. It kept provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features from allowed ABI channels, trusted `bce_dice` primary loss, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, disabled early stopping, and the provider-derived `centerline_logits` auxiliary output at weight 0.02.

## Contract and resource observation

ABI-168 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records provider-approved `abi_16ch_plus_sza` input with GOES ABI source channel indices 0-15 plus Solar Geometry source channel index 18; forbidden longitude and latitude source channel indices 16 and 17 are excluded. The model emitted provider-shaped `mask_logits` and `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

ABI-167 reached validation epoch 11 but exhausted the 3,600-second wall-clock budget and was force-terminated after the 30-second grace period. It reported 11,682,019 parameters before failure. ABI-168 reported 6,540,143 parameters, below the 25,000,000-parameter smoke ceiling and substantially smaller than ABI-167. ABI-168 completed all 12 epochs at batch size 4 on the A100 with 2,672.5 seconds total wall time, 1,397.0 seconds training wall time, 1,273.6 seconds validation wall time, 17.59 training samples per second, 19.30 validation samples per second, 9,454,039,040 bytes peak CUDA allocated, and 10,655,629,312 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260901_173120_9c74ab` | ABI-166 | late oriented line-bank ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3785 | 0.3628 | 0.4144 | 0.4077 | 0.3532 | 0.3221 | 0.00314 |
| `run_20260901_192929_0da8c3` | ABI-168 | compact sparse early-oriented ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 9 | 0.3824 | 0.3680 | 0.4178 | 0.4019 | 0.3646 | 0.2609 | 0.00329 |

ABI-168 achieved the resource-repair objective and modestly improved ABI-166's aggregate/source Dice and recall, but it did not satisfy the oriented-context success criteria. Relative to ABI-166, ABI-168 improved aggregate filtered Dice by +0.0039, MIT filtered Dice by +0.0052, Google filtered Dice by +0.0034, filtered recall by +0.0114, and predicted-positive fraction by +0.00015. Those gains came with slightly lower precision (-0.0057) and materially lower filtered connectivity (-0.0612). The earlier sparse placement therefore did not recover the line-continuity behavior that the branch was designed to test.

Relative to ABI-154, ABI-168 improved recall by +0.0288 and predicted-positive fraction by +0.00074, but lost aggregate filtered Dice by -0.0120, MIT Dice by -0.0144, Google Dice by -0.0082, precision by -0.0757, and connectivity by -0.1766. Relative to ABI-130, ABI-168 was similar on recall (+0.0068) but lower on aggregate Dice (-0.0129), MIT Dice (-0.0098), Google Dice (-0.0226), precision (-0.0395), and connectivity (-0.1242). Relative to ABI-068, ABI-168 slightly improved Google Dice (+0.0017) and precision (+0.0028), but lost aggregate Dice (-0.0140), MIT Dice (-0.0206), recall (-0.0290), and connectivity (-0.1292).

ABI-167's best observed validation epoch before timeout was epoch 8 with filtered Dice 0.3804, MIT filtered Dice 0.3729, Google filtered Dice 0.3981, precision 0.4065, recall 0.3574, and connectivity 0.2550. ABI-168 slightly exceeded that incomplete aggregate operating point and improved Google Dice, recall, and connectivity, but not MIT Dice or precision. Because ABI-167 failed terminally, those numbers are only observed trajectory context, not a completed Result.

## ABI-168 trajectory

ABI-168 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.1723, 0.2874, 0.3089, 0.2981, 0.3358, 0.3443, 0.3581, 0.3568, 0.3824, 0.3240, 0.3785, and 0.3646. The selected best checkpoint was epoch 9; the final epoch did not preserve the best operating point.

At the best checkpoint, filtered precision was 0.4019, filtered recall was 0.3646, filtered connectivity was 0.2609, and filtered predicted-positive fraction was 0.00329. Source-stratified filtered Dice was 0.3680 for MIT and 0.4178 for Google. At final epoch 12, aggregate filtered Dice fell to 0.3646, with precision 0.4274, recall 0.3180, connectivity 0.2421, MIT filtered Dice 0.3490, and Google filtered Dice 0.4027. The final checkpoint became more conservative and under-recalled without improving connectivity.

Raw-to-filtered differences were modest. At the selected checkpoint, raw Dice was 0.3960 versus filtered Dice 0.3824, raw recall 0.3895 versus filtered recall 0.3646, and raw predicted-positive fraction 0.00350 versus filtered 0.00329. At final epoch, raw Dice was 0.3793 versus filtered Dice 0.3646, raw recall 0.3399 versus filtered recall 0.3180, and raw predicted-positive fraction 0.00287 versus filtered 0.00270. The result is therefore not primarily explained by Artifact Filter dependence.

The four retained first-n prediction samples in `outputs/prediction_samples/samples.json` all had near-zero per-sample Dice. Because the retention policy is fixed `first_n` rather than source- or morphology-stratified, these samples are only bounded traceability artifacts and should not be treated as representative evidence. They do, however, remain consistent with the recurring warning that early validation positives are often missed by recent ASPP/detail refinements.

## Interpretation

Classify ABI-167 as a Harness-recorded `resource_failure` for the dense early-oriented ASPP/detail implementation under the active 3,600-second budget. Classify ABI-168 as a completed, finite, non-collapsed resource repair but a mixed-to-negative scientific result for sparse early-oriented context in this ASPP/detail branch.

The compact sparse design is a viable execution platform: it finished comfortably inside the wall-clock budget and produced a capped Result in the same broad range as ABI-166. Scientifically, however, it did not support the core oriented-context hypothesis. The key expected gain was connectivity closer to ABI-130 or ABI-154 while preserving competitive filtered Dice; instead, connectivity fell below both ABI-166 and all principal references, and the best aggregate Dice remained outside the current leader band. The result suggests that moving oriented context earlier in this branch changes calibration modestly but does not by itself produce connected thin-line masks.

This does not eliminate all oriented or line-aware architecture families, because other completed families retain stronger connectivity/primary-metric behavior. It does weaken the case for more local ASPP/detail oriented-context variants that only alter oriented block density, placement, or width under the same BCE-Dice Centerline-auxiliary policy.

## Decision

Do not promote ABI-168, do not repeat ABI-167 unchanged, and do not request whole-validation diagnostics for ABI-168. ABI-168 answered the immediate repair question by making the branch resource-safe, but it failed the useful-outcome test because it remained below ABI-068/130/154 on aggregate Dice and far below them on connectivity.

No Capability Request or Campaign Report is required from this result. For a later Autonomy Step, prefer broadening away from local ASPP/detail oriented-context repairs. Plausible contract-compliant next directions include a different compact architecture family for high-resolution continuity, a trusted evaluation request for operating-point/calibration diagnostics on current capped leaders, or a data/loss/preprocessing comparison that directly targets MIT recall and connectivity without candidate-owned postprocessing.

## Artifact references

- `run_20260901_182419_ca8406/outputs/logs/harness_timeout.log`
- `run_20260901_182419_ca8406/outputs/metrics.jsonl`
- `run_20260901_182419_ca8406/outputs/model_summary.json`
- `run_20260901_182419_ca8406/resolved_manifest.yaml`
- `run_20260901_192929_0da8c3/outputs/best_metrics.json`
- `run_20260901_192929_0da8c3/outputs/final_metrics.json`
- `run_20260901_192929_0da8c3/outputs/metrics.jsonl`
- `run_20260901_192929_0da8c3/outputs/resource_profile.json`
- `run_20260901_192929_0da8c3/outputs/model_summary.json`
- `run_20260901_192929_0da8c3/outputs/prediction_samples/samples.json`
- `run_20260901_192929_0da8c3/resolved_manifest.yaml`
- `run_20260901_173120_9c74ab/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
