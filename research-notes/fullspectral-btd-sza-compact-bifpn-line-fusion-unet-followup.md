# Full-spectral BTD+SZA compact BiFPN line-fusion U-Net follow-up

research-figures: []

## Scope

This note records the ABI-161/ABI-162 BiFPN line-fusion branch after ABI-161 failed for resource budget and ABI-162 completed.

Source Runs:

- ABI-161 full-spectral BTD+SZA BiFPN line-fusion U-Net scout: `run_20260901_132157_1d849b`
- ABI-162 compact BiFPN line-fusion U-Net resource repair: `run_20260901_142708_a2f6c9`
- ABI-160 mid-level directional-context ASPP/detail decoder immediate predecessor note context: `run_20260901_123418_da6b1e`
- ABI-154 whole-validation-tested full-scale skip ASPP/detail decoder reference: `run_20260901_071026_32d3ec`, Evaluation `eval_evalreq_abi154_wholeval_failure_buckets_v1`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice reference: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate/source-balance reference: `run_20260828_010836_4ccc77`

ABI-162 was a resource-feasibility continuation of ABI-161. It preserved the bidirectional pyramid/context-fusion hypothesis while reducing high-resolution compute: provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD features from approved ABI channels, normalized/cosine Solar Geometry features, a smaller learned 1x1 spectral mixture, compact four-scale residual encoder, positive-weight top-down/bottom-up feature-pyramid fusion, reuse of first-scale encoder features for high-resolution evidence, and a shorter horizontal/vertical line-context final head. The manifest retained trusted `bce_dice`, Centerline auxiliary target weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, 12 epochs, constant learning rate, and disabled early stopping.

## Contract and resource observation

ABI-161 is classified by the Harness as `resource_failure`: the training container exhausted the 3,600-second wall-clock budget and was force-terminated after the 30-second grace period. It had 7,643,218 parameters and reached validation epoch 11 before termination, so the full-width branch is not safe to repeat unchanged under the active budget.

ABI-162 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, GOES ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

ABI-162 reported 2,058,786 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 1,887.3 seconds total wall time, 693.2 seconds training wall time, 1,192.6 seconds validation wall time, 35.45 training samples per second, 20.61 validation samples per second, 5,259,978,752 bytes peak CUDA allocated, 6,289,358,848 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260901_123418_da6b1e` | ABI-160 | mid-level directional-context ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 11 | 0.3831 | 0.3819 | 0.3861 | 0.4023 | 0.3656 | 0.3252 | 0.00329 |
| `run_20260901_132157_1d849b` | ABI-161 | full BiFPN line-fusion U-Net, BCE-Dice, ABI-16+BTD+SZA | 7 observed | 0.3727 | 0.3653 | 0.3906 | 0.4162 | 0.3375 | 0.2788 | 0.00294 |
| `run_20260901_142708_a2f6c9` | ABI-162 | compact BiFPN line-fusion U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3738 | 0.3576 | 0.4133 | 0.4242 | 0.3342 | 0.3256 | 0.00285 |

ABI-162 achieved the main repair objective: it completed the 12-epoch representative capped run within budget. It also preserved non-degenerate predictions and ended with higher connectivity than ABI-161's best observed epoch (+0.0468) while using far fewer parameters. However, the scientific result is not competitive with the current references. Relative to ABI-068, ABI-162 lost aggregate filtered Dice (-0.0225), MIT Dice (-0.0310), Google Dice (-0.0028), recall (-0.0594), and connectivity (-0.0644), with higher precision (+0.0250). Relative to ABI-130, ABI-162 lost aggregate filtered Dice (-0.0214), MIT Dice (-0.0203), Google Dice (-0.0271), precision (-0.0173), recall (-0.0236), and connectivity (-0.0595). Relative to ABI-154, ABI-162 lost aggregate filtered Dice (-0.0206), MIT Dice (-0.0248), Google Dice (-0.0127), precision (-0.0535), recall (-0.0017), and connectivity (-0.1118).

ABI-162 did not materially outperform ABI-160 either: it lost aggregate filtered Dice (-0.0092), MIT Dice (-0.0243), recall (-0.0314), and nearly matched connectivity (+0.0004), while improving Google Dice (+0.0272) and precision (+0.0219). The compact BiFPN repair therefore shifted the source trade-off toward Google and precision but did not solve the fixed-threshold aggregate/continuity problem.

## ABI-162 trajectory

ABI-162 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.2350, 0.2648, 0.2823, 0.2969, 0.3062, 0.3448, 0.3043, 0.3442, 0.3264, 0.3430, 0.3589, and 0.3738. The selected best checkpoint was the final epoch 12, so the branch was still improving by the active epoch ceiling.

At epoch 12, ABI-162 had raw Dice 0.3884, filtered Dice 0.3738, filtered precision 0.4242, filtered recall 0.3342, filtered connectivity 0.3256, and filtered predicted-positive fraction 0.00285. Source-stratified filtered Dice was 0.3576 for MIT and 0.4133 for Google. Raw-to-filtered differences were modest: raw Dice 0.3884 versus filtered Dice 0.3738, and raw predicted-positive fraction 0.00304 versus filtered 0.00285. This does not indicate primary dependence on Artifact Filters. The fixed first-four retained prediction samples had three near-zero per-sample Dice values and one all-correct sample, but the retention policy is `first_n`, so those bounded samples are traceability artifacts rather than representative qualitative evidence.

## Interpretation

Classify ABI-161 as a resource failure for the full-width BiFPN line-fusion implementation. ABI-162 is a completed, finite, non-collapsed resource repair but a mixed-to-negative scientific result for the compact BiFPN line-fusion branch under the current capped 12-epoch budget.

The outcome is informative. Bidirectional pyramid fusion is resource-feasible after compaction, and ABI-162 shows a clean improving trajectory through epoch 12. That argues against eliminating the whole BiFPN/fusion idea solely on this first compact scout. At the same time, the achieved operating point is substantially below the ABI-068/ABI-130/ABI-154 references and does not recover the precision/connectivity or source balance that would justify promotion or immediate whole-validation diagnostics. The branch appears to need either a different calibration/loss policy or a different high-resolution continuity mechanism rather than another unchanged compact-width repetition.

## Decision

Do not promote ABI-162, do not repeat ABI-161 unchanged under the active wall-clock budget, and do not request whole-validation diagnostics for ABI-162. ABI-162 preserved the broad BiFPN line-fusion scout hypothesis as resource-feasible but did not meet a useful-outcome threshold versus the current capped references.

A next candidate, if the campaign continues within this family, should be a controlled family-development continuation that changes one calibration-relevant factor rather than adding more expensive full-width fusion: for example focal-Tversky on the compact BiFPN branch to test recall recovery, or a lighter non-suppressive line-continuity head that targets the gap to ABI-068/ABI-154 connectivity while preserving the completed ABI-162 resource profile. No Capability Request, Evaluation Request, or Campaign Report is required from ABI-162.

## Artifact references

- `run_20260901_132157_1d849b/outputs/logs/harness_timeout.log`
- `run_20260901_132157_1d849b/outputs/metrics.jsonl`
- `run_20260901_132157_1d849b/outputs/model_summary.json`
- `run_20260901_132157_1d849b/resolved_manifest.yaml`
- `run_20260901_142708_a2f6c9/outputs/best_metrics.json`
- `run_20260901_142708_a2f6c9/outputs/final_metrics.json`
- `run_20260901_142708_a2f6c9/outputs/metrics.jsonl`
- `run_20260901_142708_a2f6c9/outputs/resource_profile.json`
- `run_20260901_142708_a2f6c9/outputs/model_summary.json`
- `run_20260901_142708_a2f6c9/outputs/prediction_samples/samples.json`
- `run_20260901_142708_a2f6c9/resolved_manifest.yaml`
- `run_20260901_123418_da6b1e/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
