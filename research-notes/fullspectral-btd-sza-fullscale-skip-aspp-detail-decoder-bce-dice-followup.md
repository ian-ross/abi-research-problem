# Full-spectral BTD+SZA full-scale skip ASPP/detail decoder BCE-Dice centerline-auxiliary follow-up

research-figures: []

## Scope

This note records ABI-154 after Run `run_20260901_071026_32d3ec` completed.

Source Runs:

- ABI-154 full-spectral BTD+SZA full-scale skip ASPP/detail decoder BCE-Dice Centerline-auxiliary continuation: `run_20260901_071026_32d3ec`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice comparison target and whole-validation-tested ASPP/detail reference: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net focal-Tversky local capped aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice precision/connectivity comparator: `run_20260831_085615_d05ab3`
- ABI-143 soft ridge-gate U-Net BCE-Dice nearby SZA-aware ridge comparator: `run_20260831_224534_27b73d`
- ABI-142 multiscale ridge-attention U-Net BCE-Dice nearby SZA-aware comparator: `run_20260831_215104_d4c318`

ABI-154 was a family-development continuation of ABI-130. It kept provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features derived only from approved ABI channels, normalized Solar Geometry Input features, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled architecture change was adding compact full-scale skip aggregation over stem, encoder, ASPP context, decoder, and high-resolution detail features before final mask refinement.

## Contract and resource observation

ABI-154 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 9,741,850 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,560.6 seconds total wall time, 1,265.1 seconds training wall time, 1,293.4 seconds validation wall time, 8,020,934,144 bytes peak CUDA allocated, 9,439,281,152 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_224534_27b73d` | ABI-143 | soft ridge-gate U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3947 | 0.3815 | 0.4287 | 0.4105 | 0.3801 | 0.3010 | 0.00336 |
| `run_20260831_215104_d4c318` | ABI-142 | multiscale ridge-attention U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3935 | 0.3762 | 0.4373 | 0.4398 | 0.3561 | 0.3819 | 0.00293 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |

ABI-154 is a useful but mixed controlled continuation. Relative to ABI-130, aggregate filtered Dice is slightly lower, 0.3944 versus 0.3953 (-0.0009), and Google filtered Dice falls from 0.4404 to 0.4260 (-0.0144). The full-scale skip module does improve the intended calibration/connectivity side of the trade-off: MIT filtered Dice rises from 0.3779 to 0.3824 (+0.0045), filtered precision rises from 0.4415 to 0.4777 (+0.0362), filtered connectivity rises from 0.3851 to 0.4374 (+0.0524), and filtered predicted-positive fraction drops from 0.00294 to 0.00255. Filtered recall falls from 0.3578 to 0.3359 (-0.0220), so the gain is not an aggregate-Dice improvement; it is a shift toward a cleaner, more connected, lower-positive-area operating point.

Relative to ABI-068, ABI-154 is lower on aggregate filtered Dice (-0.0020), MIT filtered Dice (-0.0062), and recall (-0.0577), but improves Google filtered Dice (+0.0099), precision (+0.0785), connectivity (+0.0474), and positive-area discipline. Relative to ABI-126, ABI-154 improves aggregate Dice (+0.0085), MIT Dice (+0.0189), recall (+0.0108), and raw Dice, while staying slightly lower on Google Dice (-0.0154), precision (-0.0070), connectivity (-0.0143), and positive-area fraction (+0.00007). This places ABI-154 between ABI-126's precision/connectivity-forward branch and ABI-130's SZA-calibrated recall branch.

ABI-154 also improves substantially over nearby ridge-style SZA branches on connectivity and positive-area discipline. It trails ABI-143 by only 0.0003 aggregate filtered Dice while improving precision by 0.0671 and connectivity by 0.1365, with lower predicted-positive fraction. It improves over ABI-142 by 0.0009 aggregate filtered Dice, 0.0062 MIT Dice, 0.0379 precision, 0.0555 connectivity, and lower positive area, while trailing ABI-142's Google Dice by 0.0113.

## ABI-154 trajectory

ABI-154 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.2040, 0.2936, 0.3050, 0.3404, 0.3347, 0.3674, 0.3766, 0.3796, 0.3247, 0.3662, 0.3593, and 0.3944. The final epoch was the selected checkpoint and the best capped filtered Dice for this Run.

The late trajectory is non-monotonic but extension-informative rather than exhausted. Epochs 6-8 entered the 0.367-0.380 band, epochs 9-11 regressed, and epoch 12 recovered to the selected best with the run's strongest precision/connectivity profile. The final checkpoint has raw Dice 0.4108, filtered Dice 0.3944, filtered precision 0.4777, filtered recall 0.3359, filtered connectivity 0.4374, and filtered predicted-positive fraction 0.00255. Source-stratified filtered Dice was 0.3824 for MIT and 0.4260 for Google. MIT had filtered precision 0.4825, recall 0.3167, connectivity 0.4068, and predicted-positive fraction 0.00355; Google had filtered precision 0.4667, recall 0.3919, connectivity 0.4681, and predicted-positive fraction 0.00155.

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice was 0.4108 versus filtered Dice 0.3944, and raw predicted-positive fraction was 0.00272 versus filtered 0.00255. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction artifacts include one empty/negative perfect case and three near-zero per-sample Dice cases under the `first_n` retention policy; these artifacts are traceability samples and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-154 as a completed, finite, non-collapsed, scientifically positive-but-mixed family-development result for SZA-aware ASPP/detail decoding. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The full-scale skip aggregation did not improve the primary capped filtered Dice over ABI-130 or ABI-068. However, it met the proposal's useful-outcome pattern: aggregate Dice stayed within 0.001 of ABI-130 while precision, connectivity, MIT Dice, and positive-area discipline improved. The result suggests all-scale decoder fusion can recover a meaningful part of ABI-126/ABI-066-style precision/connectivity without fully reverting to ABI-126's lower aggregate/MIT Dice. The main cost is lower Google Dice and recall relative to ABI-130.

ABI-154 should therefore be retained as the strongest SZA-aware ASPP/detail precision/connectivity continuation, not as a promoted model or a replacement for ABI-068 and ABI-130. It is capped representative evidence only. Canonical MCAST 2.1 and whole Working Validation Split diagnostics remain the promotion context, and no full-data claim follows from this Run.

## Decision

Do not promote ABI-154 from capped evidence and do not repeat the exact candidate unchanged. Retain ABI-068 as the local capped aggregate/source-balance reference, ABI-130 as the whole-validation-tested SZA-aware ASPP/detail aggregate/reference branch, ABI-126 as the ASPP/detail precision/connectivity comparator, and ABI-154 as a new capped SZA-aware full-scale-skip precision/connectivity branch.

Because ABI-154 nearly ties ABI-130 on capped aggregate filtered Dice while materially improving precision, connectivity, MIT Dice, and positive-area discipline, the next useful handoff is a bounded whole-validation failure-bucket Evaluation Request for `run_20260901_071026_32d3ec`. That diagnostic should test whether the capped precision/connectivity gains survive on the full 3,088-sample Working Validation Split, whether the Google Dice/recall loss versus ABI-130 is tolerable, and whether negative-patch clutter improves relative to ABI-130 without reintroducing ABI-126-style MIT under-recall. No Capability Request or Campaign Report is required from ABI-154.

## Artifact references

- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/final_metrics.json`
- `run_20260901_071026_32d3ec/outputs/metrics.jsonl`
- `run_20260901_071026_32d3ec/outputs/resource_profile.json`
- `run_20260901_071026_32d3ec/outputs/model_summary.json`
- `run_20260901_071026_32d3ec/outputs/prediction_samples/samples.json`
- `run_20260901_071026_32d3ec/resolved_manifest.yaml`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260831_224534_27b73d/outputs/best_metrics.json`
- `run_20260831_215104_d4c318/outputs/best_metrics.json`
