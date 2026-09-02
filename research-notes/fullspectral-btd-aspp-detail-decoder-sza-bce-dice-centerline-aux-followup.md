# Full-spectral BTD+SZA ASPP/detail decoder BCE-Dice centerline-auxiliary follow-up

research-figures: []

## Scope

This note records ABI-130 after Run `run_20260831_121006_7d24be` completed.

Source Runs:

- ABI-130 ASPP/detail decoder BTD+SZA BCE-Dice centerline-auxiliary follow-up: `run_20260831_121006_7d24be`
- ABI-126 ASPP/detail decoder BCE-Dice centerline-auxiliary comparison target: `run_20260831_085615_d05ab3`
- ABI-126 whole-validation diagnostic reference: `eval_evalreq_abi126_wholeval_failure_buckets_v1`
- ABI-121 ASPP/detail decoder focal-Tversky centerline-auxiliary recall/source-balance comparator: `run_20260831_041559_43da35`
- ABI-068 frequency-gated line U-Net focal-Tversky aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice precision/connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-076 frequency-gated line U-Net SZA focal-Tversky comparison for Solar Geometry Input behavior: `run_20260828_080008_ce4819`
- ABI-127 and ABI-128 as recent ASPP/detail BCE-Dice head/calibration follow-ups: `run_20260831_094013_5ba974` and `run_20260831_103509_961c81`

ABI-130 was a family-development continuation of ABI-126. It kept the compact full-spectral BTD ASPP/detail encoder-decoder, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled manifest change from ABI-126 was `input_mode: abi_16ch_plus_sza`: the model added provider-approved Solar Geometry Input features to the existing raw-plus-BTD front end. This is capped representative evidence, not full-data promotion evidence.

## Contract and resource observation

ABI-130 stayed inside the Candidate Experiment Contract. Candidate code owned only the PyTorch architecture over provider-approved GOES ABI channels 1-16 plus Solar Geometry Input. It used deterministic brightness-temperature-difference planes derived from approved thermal ABI channels and normalized SZA/`cos(SZA)` illumination features. It did not receive longitude, latitude, reconstructed coordinates, Dataset Source identity, candidate-owned data loading, split logic, capped-record selection, sampling implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, filesystem persistence, network access, pretrained weights, or lifecycle behavior.

`resolved_manifest.yaml` records `input_mode: abi_16ch_plus_sza`, `data.sampling_policy: combined_source_balanced`, `data.augmentation_policy: random_mirroring`, `training.loss: bce_dice`, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and provider-derived Centerline Target auxiliary output `centerline_logits` with trusted `weighted_bce` weight 0.02. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records.

`outputs/model_summary.json` reported 9,620,010 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,183.5 seconds total wall time, 991.4 seconds training wall time, 1,190.3 seconds validation wall time, 5,914,883,584 bytes peak CUDA allocated, 6,469,713,920 bytes peak CUDA reserved, and no terminal execution failure. The selected best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, ABI-16+BTD | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260831_041559_43da35` | ABI-121 | ASPP/detail decoder, focal-Tversky, ABI-16+BTD | 12 | 0.3884 | 0.3835 | 0.4005 | 0.3526 | 0.4323 | 0.2315 | 0.00444 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260831_094013_5ba974` | ABI-127 | ABI-126 plus Line+Centerline aux | 9 | 0.3797 | 0.3653 | 0.4150 | 0.4280 | 0.3412 | 0.3054 | 0.00289 |
| `run_20260831_103509_961c81` | ABI-128 | ABI-126 plus calibration-aware margin head | 9 | 0.3787 | 0.3586 | 0.4298 | 0.4120 | 0.3504 | 0.3473 | 0.00308 |
| `run_20260828_080008_ce4819` | ABI-076 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD+SZA | 12 | 0.3790 | 0.3718 | 0.3962 | 0.3463 | 0.4184 | 0.3013 | 0.00438 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |

ABI-130 mostly met the SZA-calibration hypothesis relative to ABI-126. Aggregate filtered Dice improved from 0.3859 to 0.3953 (+0.0094), MIT filtered Dice from 0.3635 to 0.3779 (+0.0144), aggregate filtered recall from 0.3251 to 0.3578 (+0.0328), and MIT filtered recall from 0.2931 to 0.3313 (+0.0382). Google filtered Dice stayed essentially tied, 0.4415 to 0.4404 (-0.0011), while Google filtered recall rose from 0.4185 to 0.4355. This indicates the SZA feature helped the conservative BCE-Dice ASPP/detail branch recover recall and source balance without losing the branch's strong Google performance.

The improvement was not free. Relative to ABI-126, filtered precision decreased from 0.4746 to 0.4415 (-0.0332), filtered connectivity from 0.4517 to 0.3851 (-0.0666), MIT precision from 0.4784 to 0.4397, and Google connectivity from 0.4653 to 0.3984. The filtered predicted-positive fraction rose from 0.00248 to 0.00294, still lower than ABI-068's 0.00357 and far below ABI-121's 0.00444. Thus ABI-130 moved ABI-126 toward a more balanced operating point, but it partially surrendered the extreme precision/connectivity advantage that made ABI-126 a distinctive ASPP/detail comparator.

Relative to ABI-068, ABI-130 is a near-tie on capped aggregate filtered Dice, 0.3953 versus 0.3964 (-0.0011). It improves Google filtered Dice by 0.0243 and filtered precision by 0.0423, while losing MIT filtered Dice by 0.0107, recall by 0.0358, and connectivity by 0.0049. Relative to ABI-066, ABI-130 improves aggregate filtered Dice by 0.0127, MIT filtered Dice by 0.0141, Google filtered Dice by 0.0112, and recall by 0.0211, while slightly trailing precision (-0.0013) and more clearly trailing connectivity (-0.0880). Relative to ABI-121, ABI-130 improves aggregate filtered Dice, Google filtered Dice, precision, connectivity, and positive-area discipline, but remains lower on MIT Dice and recall.

The ABI-076 comparison suggests the effect of Solar Geometry Input is architecture/loss dependent rather than universally recall-heavy. ABI-076's SZA frequency-gated focal-Tversky branch had high recall (0.4184) and higher positive area (0.00438) but lower precision/connectivity and lower aggregate Dice than ABI-068. ABI-130 used SZA more conservatively: recall increased relative to ABI-126, but positive area remained controlled, precision stayed close to ABI-066, and aggregate Dice nearly matched ABI-068.

## ABI-130 trajectory

ABI-130 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.1962, 0.2915, 0.2748, 0.3330, 0.3386, 0.3080, 0.3752, 0.3520, 0.3716, 0.3712, 0.3723, and 0.3953. The selected checkpoint was the final epoch 12, so the branch retained a late improvement signal rather than plateauing or degrading into a clear dead end.

At the selected checkpoint, raw Dice was 0.4101 and filtered Dice was 0.3953. Filtered precision was 0.4415, filtered recall 0.3578, filtered connectivity 0.3851, and filtered predicted-positive fraction 0.00294. Source-stratified filtered Dice was 0.3779 for MIT and 0.4404 for Google. MIT had filtered precision 0.4397, recall 0.3313, connectivity 0.3717, and predicted-positive fraction 0.00407; Google had filtered precision 0.4454, recall 0.4355, connectivity 0.3984, and predicted-positive fraction 0.00181. Both Dataset Sources were finite and non-collapsed. The source split remains asymmetric, but it is less conservative than ABI-126 on MIT and much stronger than ABI-121 on Google precision/connectivity.

Epoch-level behavior was somewhat oscillatory. Epoch 7 already reached 0.3752 filtered Dice, epochs 8-11 hovered around 0.3520-0.3723, and epoch 12 jumped to the selected best. Precision/connectivity also oscillated: epoch 10 had high precision/connectivity but lower recall, while epoch 12 recovered recall and Dice with moderate connectivity. This late non-monotonic improvement makes the result extension-eligible as capped evidence, but it also argues against over-interpreting a single capped checkpoint as a stable promotion-quality endpoint.

Raw-to-filtered differences were modest: raw Dice 0.4101 versus filtered Dice 0.3953, and raw predicted-positive fraction 0.00313 versus filtered 0.00294. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples include one empty/negative perfect sample and three near-zero per-sample Dice examples, but the retention policy is fixed `first_n`, so these bounded artifacts should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-130 as finite, resource-feasible, non-collapsed, and positive capped family-development evidence for Solar Geometry Input in the ASPP/detail BCE-Dice branch. The controlled SZA input change improved the main ABI-126 weakness targeted by the proposal: conservative fixed-threshold recall and MIT under-segmentation. It produced the second-best capped aggregate filtered Dice observed in the current local ranking, only about 0.001 below ABI-068, while preserving ABI-126-like Google strength and enough positive-area discipline to remain distinct from recall-heavy focal-Tversky variants.

ABI-130 is not a promotion claim. Its metrics are from the trusted capped representative 1,024-record-per-Dataset-Source/split policy. Canonical MCAST 2.1 and the full 3,088-sample Working Validation Split remain the promotion context, and whole-validation diagnostics must be requested separately before making any full-data claim.

The main caveat is that ABI-130 traded away part of ABI-126's strongest precision/connectivity advantage. ABI-126 remains the cleaner ASPP/detail precision/connectivity point and already has whole-validation diagnostic support. ABI-130 should be treated as the best ASPP/detail aggregate-Dice/SZA-calibrated capped branch, not as an unambiguous replacement for ABI-126's high-precision operating point or ABI-068's current local aggregate reference.

## Decision

Do not promote ABI-130 from capped evidence. Do not repeat the exact ABI-130 candidate unchanged. Retain ABI-068 as the local capped aggregate-Dice reference, ABI-066 as the precision/connectivity reference, ABI-121 as the ASPP/detail recall/source-balance comparator, ABI-126 as the ASPP/detail high-precision/connectivity and Google-Dice comparator, and ABI-130 as the ASPP/detail SZA-calibrated near-aggregate-reference result.

Because ABI-130 nearly matches ABI-068 on capped aggregate filtered Dice while improving ABI-126's target weakness, a reasonable next handoff is a bounded whole-validation failure-bucket Evaluation Request for `run_20260831_121006_7d24be`. The diagnostic should test whether the capped SZA gain survives on the full Working Validation Split, whether MIT recall meaningfully improves over ABI-126, and whether the connectivity loss versus ABI-126/ABI-066 is acceptable or reveals SZA-induced clutter. If whole-validation confirms the capped pattern, later in-contract work can explore a conservative SZA-aware calibration/continuity variant; if it does not, broaden away from simple ASPP/detail input tweaks.

## Artifact references

- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/final_metrics.json`
- `run_20260831_121006_7d24be/outputs/metrics.jsonl`
- `run_20260831_121006_7d24be/outputs/resource_profile.json`
- `run_20260831_121006_7d24be/outputs/model_summary.json`
- `run_20260831_121006_7d24be/outputs/prediction_samples/samples.json`
- `run_20260831_121006_7d24be/resolved_manifest.yaml`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/evaluations/eval_evalreq_abi126_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_041559_43da35/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
- `run_20260828_080008_ce4819/outputs/best_metrics.json`
- `run_20260831_094013_5ba974/outputs/best_metrics.json`
- `run_20260831_103509_961c81/outputs/best_metrics.json`
