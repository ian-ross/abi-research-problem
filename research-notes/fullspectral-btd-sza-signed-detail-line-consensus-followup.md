# Full-spectral BTD+SZA signed-detail line-consensus full-scale skip ASPP decoder follow-up

research-figures: []

## Scope

This note records ABI-174 after Run `run_20260902_005632_5651ef` completed.

Source Runs:

- ABI-174 signed-detail line-consensus full-scale skip ASPP decoder BCE-Dice Centerline-auxiliary continuation: `run_20260902_005632_5651ef`
- ABI-173 signed-detail full-scale skip ASPP decoder parent and whole-validation-tested SZA-aware ASPP/detail aggregate reference: `run_20260901_234732_bd5917`; Evaluation `eval_evalreq_abi173_wholeval_failure_buckets_v1`
- ABI-154 full-scale skip ASPP/detail decoder precision/connectivity reference: `run_20260901_071026_32d3ec`
- ABI-130 SZA-aware ASPP/detail decoder aggregate reference: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net broader capped aggregate/source-balance comparator: `run_20260828_010836_4ccc77`
- ABI-170 compact BiFPN multiscale line-head comparison: `run_20260901_212305_8ff75d`
- ABI-171 full-scale skip ASPP/detail centerline-weight 0.01 comparison: `run_20260901_220525_8c0116`
- ABI-172 full-scale skip ASPP/detail focal-Tversky comparison: `run_20260901_225502_53acd2`

ABI-174 was a family-development continuation of ABI-173. It kept provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized/cosine Solar Geometry Input features, signed local and mid-scale detail streams, compact residual encoder, ASPP context, full-scale skip fusion, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, trusted `bce_dice` primary loss, and provider-derived Centerline Target auxiliary supervision at weight 0.02. The controlled architecture change was adding a conservative line-consensus feature calibration block after ABI-173's line-aware refinement, intended to recover connectivity or clutter discipline without losing ABI-173's signed-detail recall gains.

## Contract and resource observation

ABI-174 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 10,078,210 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 3,245.3 seconds total wall time, 1,778.1 seconds training wall time, 1,465.0 seconds validation wall time, 13.82 training samples per second, 16.78 validation samples per second, 11,014,247,936 bytes peak CUDA allocated, and 13,172,211,712 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260901_234732_bd5917` | ABI-173 | signed-detail full-scale skip ASPP decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3962 | 0.3838 | 0.4269 | 0.4238 | 0.3720 | 0.3203 | 0.00318 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260902_005632_5651ef` | ABI-174 | signed-detail line-consensus full-scale skip ASPP decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3929 | 0.3833 | 0.4178 | 0.4158 | 0.3724 | 0.3460 | 0.00325 |
| `run_20260901_220525_8c0116` | ABI-171 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA, centerline w0.01 | 8 | 0.3816 | 0.3703 | 0.4086 | 0.4101 | 0.3569 | 0.3473 | 0.00315 |
| `run_20260901_212305_8ff75d` | ABI-170 | compact BiFPN multiscale line-head, BCE-Dice, ABI-16+BTD+SZA | 9 | 0.3674 | 0.3511 | 0.4067 | 0.4148 | 0.3298 | 0.2155 | 0.00288 |
| `run_20260901_225502_53acd2` | ABI-172 | full-scale skip ASPP/detail decoder, focal-Tversky, ABI-16+BTD+SZA | 10 | 0.3578 | 0.3552 | 0.3631 | 0.3185 | 0.4081 | 0.2312 | 0.00464 |

ABI-174 is a finite but scientifically mixed-to-negative capped continuation. Relative to ABI-173, the line-consensus calibration recovered some connectivity, from 0.3203 to 0.3460 (+0.0257), while preserving essentially the same recall, 0.3720 to 0.3724. However, it did not reduce clutter or preserve aggregate overlap: filtered Dice fell from 0.3962 to 0.3929 (-0.0033), Google filtered Dice from 0.4269 to 0.4178 (-0.0090), precision from 0.4238 to 0.4158 (-0.0079), and filtered predicted-positive fraction rose slightly from 0.00318 to 0.00325. MIT filtered Dice was effectively flat but marginally lower, 0.3838 to 0.3833.

Relative to ABI-154, ABI-174 preserves the signed-detail branch's recall recovery (+0.0365 filtered recall), but does not keep ABI-154's precision, connectivity, or positive-area discipline. It is lower than ABI-154 by 0.0015 filtered Dice, 0.0618 precision, and 0.0915 connectivity, with a higher predicted-positive fraction. Relative to ABI-130, ABI-174 is lower on aggregate and Google filtered Dice, precision, connectivity, and positive-area discipline, while retaining modestly higher MIT filtered Dice and recall. Relative to ABI-068, ABI-174 is lower on aggregate filtered Dice, MIT filtered Dice, recall, and connectivity, while higher on precision and Google filtered Dice.

## ABI-174 trajectory

ABI-174 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.2041, 0.2833, 0.3164, 0.3144, 0.3003, 0.3284, 0.3575, 0.3629, 0.3643, 0.3613, 0.3609, and 0.3929. The final epoch was both the selected checkpoint and the Run maximum.

The trajectory is not a hard optimization failure: training loss declined from 0.9815 to 0.8520, and the final epoch showed a meaningful jump in filtered Dice after a shallow epoch 8-11 plateau. At the selected checkpoint, raw Dice was 0.4077, filtered Dice was 0.3929, filtered precision was 0.4158, filtered recall was 0.3724, filtered connectivity was 0.3460, and filtered predicted-positive fraction was 0.00325. Source-stratified filtered Dice was 0.3833 for MIT and 0.4178 for Google. MIT had filtered precision 0.4205, recall 0.3523, connectivity 0.3457, and predicted-positive fraction 0.00452; Google had filtered precision 0.4052, recall 0.4313, connectivity 0.3463, and predicted-positive fraction 0.00197.

Raw-to-filtered differences were modest: raw Dice was 0.4077 versus filtered Dice 0.3929, raw recall was 0.3992 versus filtered recall 0.3724, and raw predicted-positive fraction was 0.00347 versus filtered 0.00325. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples include two empty/negative perfect cases and two near-zero per-sample Dice cases under the `first_n` retention policy; these artifacts are traceability samples and should not be treated as representative qualitative evidence for the full validation distribution.

## Interpretation

Classify ABI-174 as a completed, finite, non-collapsed capped family-development result, but not as a successful continuation of the ABI-173 signed-detail branch. The line-consensus feature calibration achieved one intended directional effect by improving connectivity versus ABI-173, yet the improvement was too small to approach ABI-154 or ABI-130 connectivity, and it came without the requested clutter or aggregate Dice preservation. The added block also increased wall time and peak memory relative to ABI-173 while leaving the branch below the strongest capped and whole-validation-tested references.

The main design lesson is that a local post-refinement line-consensus gate can slightly improve connected-line evidence, but it is not sufficient to solve the ABI-173 false-positive/connectivity tradeoff. Another local head or stem tweak in the same signed-detail/full-scale-skip branch is unlikely to be the next best use of capped-run budget unless whole-validation diagnostics identify a specific fixable failure mode. The signed-detail idea remains useful because ABI-173's whole-validation gains survived, but ABI-174 does not strengthen the case for this specific line-consensus variant.

## Decision

Do not promote ABI-174, do not repeat it unchanged, and do not request whole-validation diagnostics for ABI-174 from this capped result alone. Retain ABI-173 as the whole-validation-tested SZA-aware ASPP/detail aggregate branch, ABI-154 as the SZA-aware ASPP/detail precision/connectivity branch, ABI-130 as the prior SZA-aware ASPP/detail aggregate reference, and ABI-068 as the capped aggregate/source-balance comparator.

A reasonable next hypothesis should broaden beyond another local signed-detail head tweak: either a more distinct connectivity-preserving decoder, a different calibration/preprocessing route, or a data/loss frontier already allowed by the trusted contract. No Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260902_005632_5651ef/outputs/best_metrics.json`
- `run_20260902_005632_5651ef/outputs/final_metrics.json`
- `run_20260902_005632_5651ef/outputs/metrics.jsonl`
- `run_20260902_005632_5651ef/outputs/resource_profile.json`
- `run_20260902_005632_5651ef/outputs/model_summary.json`
- `run_20260902_005632_5651ef/outputs/prediction_samples/samples.json`
- `run_20260902_005632_5651ef/outputs/validation_postprocessing/epoch_012.json`
- `run_20260902_005632_5651ef/resolved_manifest.yaml`
- `run_20260901_234732_bd5917/outputs/best_metrics.json`
- `run_20260901_234732_bd5917/outputs/evaluations/eval_evalreq_abi173_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260901_212305_8ff75d/outputs/best_metrics.json`
- `run_20260901_220525_8c0116/outputs/best_metrics.json`
- `run_20260901_225502_53acd2/outputs/best_metrics.json`
