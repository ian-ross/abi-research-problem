# Full-spectral BTD+SZA signed context-fusion ASPP decoder follow-up

research-figures: []

## Scope

This note records ABI-176 after Run `run_20260902_025056_9e87d5` completed.

Source Runs:

- ABI-176 signed context-fusion ASPP decoder BCE-Dice Centerline-auxiliary continuation: `run_20260902_025056_9e87d5`
- ABI-173 signed-detail full-scale skip ASPP decoder parent and whole-validation-tested SZA-aware ASPP/detail aggregate branch: `run_20260901_234732_bd5917`; Evaluation `eval_evalreq_abi173_wholeval_failure_buckets_v1`
- ABI-154 full-scale skip ASPP/detail decoder precision/connectivity reference: `run_20260901_071026_32d3ec`
- ABI-130 SZA-aware ASPP/detail decoder aggregate reference: `run_20260831_121006_7d24be`
- ABI-174 signed-detail line-consensus follow-up: `run_20260902_005632_5651ef`
- ABI-175 anti-aliased full-scale skip follow-up: `run_20260902_015941_3ebc45`
- ABI-068 frequency-gated line U-Net broader capped aggregate/source-balance comparator: `run_20260828_010836_4ccc77`

ABI-176 was a family-development continuation of ABI-173. It kept provider-approved `abi_16ch_plus_sza` input, normalized GOES ABI channels 1-16, deterministic thermal BTD planes derived only from approved ABI channels, normalized/cosine Solar Geometry Input features, signed positive/negative detail stems, compact residual encoder, ASPP context, full-scale skip aggregation, line-aware final refinement, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, trusted `bce_dice` primary loss, and provider-derived Centerline Target auxiliary supervision at weight 0.02. The controlled architecture change was `SignedContextFusion`: shared-width projections of decoder/detail/stem/full-scale features, a neutral context gate from decoder/stem/full-scale/broad context, bounded signed-detail calibration, and horizontal/vertical detail-context branches before the existing line-aware refinement.

## Contract and resource observation

ABI-176 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Candidate code did not implement data loading, Leakage-Safe Split logic, capped-record selection, sampling implementation, augmentation transforms, losses, target derivation, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, or Run lifecycle.

`outputs/model_summary.json` reported 9,964,210 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 3,057.5 seconds total wall time, 1,685.5 seconds training wall time, 1,369.8 seconds validation wall time, 14.58 training samples per second, 17.94 validation samples per second, 10,173,999,616 bytes peak CUDA allocated, and 11,649,679,360 bytes peak CUDA reserved. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was the final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260901_234732_bd5917` | ABI-173 | signed-detail full-scale skip ASPP decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3962 | 0.3838 | 0.4269 | 0.4238 | 0.3720 | 0.3203 | 0.00318 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260902_005632_5651ef` | ABI-174 | signed-detail line-consensus full-scale skip ASPP decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3929 | 0.3833 | 0.4178 | 0.4158 | 0.3724 | 0.3460 | 0.00325 |
| `run_20260902_025056_9e87d5` | ABI-176 | signed context-fusion ASPP decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3902 | 0.3739 | 0.4300 | 0.4377 | 0.3519 | 0.2866 | 0.00291 |
| `run_20260902_015941_3ebc45` | ABI-175 | anti-aliased full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3817 | 0.3687 | 0.4175 | 0.5035 | 0.3073 | 0.4929 | 0.00221 |

ABI-176 is finite and non-degenerate, but mixed-to-negative for its stated context-balanced signed-detail hypothesis. Relative to ABI-173, context fusion improved filtered precision from 0.4238 to 0.4377 (+0.0139), reduced filtered predicted-positive fraction from 0.00318 to 0.00291, and slightly improved Google filtered Dice from 0.4269 to 0.4300. However, it reduced aggregate filtered Dice from 0.3962 to 0.3902 (-0.0060), MIT filtered Dice from 0.3838 to 0.3739 (-0.0100), recall from 0.3720 to 0.3519 (-0.0201), and connectivity from 0.3203 to 0.2866 (-0.0338). It therefore did not preserve ABI-173's recall or recover connectivity.

Relative to ABI-154, ABI-176 has modestly higher recall (+0.0161) and Google filtered Dice (+0.0039), but lower aggregate filtered Dice (-0.0042), MIT filtered Dice (-0.0085), precision (-0.0400), connectivity (-0.1509), and positive-area discipline. Relative to ABI-130, ABI-176 is lower on aggregate filtered Dice, both source-stratified Dice values, precision, recall, and especially connectivity. Relative to ABI-068, it is higher on Google filtered Dice and precision but lower on aggregate filtered Dice, MIT filtered Dice, recall, and connectivity.

Compared with the two immediate local follow-ups, ABI-176 is better balanced than ABI-175's very conservative anti-aliased downsampling branch, but it is lower than ABI-174 on aggregate filtered Dice, MIT filtered Dice, recall, and connectivity while improving Google Dice, precision, and positive-area discipline. The signed context gate therefore appears to suppress some clutter, but not in a way that improves the full aggregate/source/connectivity tradeoff.

## ABI-176 trajectory

ABI-176 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.2357, 0.3090, 0.2969, 0.3289, 0.3411, 0.3723, 0.3832, 0.3648, 0.3835, 0.3621, 0.3633, and 0.3902. The final epoch was both the selected checkpoint and the Run maximum.

The trajectory is not a hard optimization or numerical failure: training loss declined from 0.9727 to 0.8455, validation loss declined to 0.8813, and the selected checkpoint occurred at epoch 12. The epoch path was somewhat oscillatory after epoch 6, alternating between higher-recall/lower-precision and higher-precision/lower-recall regimes, but it ended with the best aggregate filtered Dice.

At the selected checkpoint, raw Dice was 0.4050, filtered Dice was 0.3902, filtered precision was 0.4377, filtered recall was 0.3519, filtered connectivity was 0.2866, and filtered predicted-positive fraction was 0.00291. Source-stratified filtered Dice was 0.3739 for MIT and 0.4300 for Google. MIT had filtered precision 0.4475, recall 0.3211, connectivity 0.3183, and predicted-positive fraction 0.00388; Google had filtered precision 0.4183, recall 0.4423, connectivity 0.2548, and predicted-positive fraction 0.00195.

Raw-to-filtered differences were modest: raw Dice was 0.4050 versus filtered Dice 0.3902, raw recall was 0.3758 versus filtered recall 0.3519, and raw predicted-positive fraction was 0.00310 versus filtered 0.00291. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples include one empty/negative perfect case and three near-zero per-sample Dice cases under the `first_n` retention policy; these artifacts are traceability samples and should not be treated as representative qualitative evidence for the full validation distribution.

## Interpretation

Classify ABI-176 as a completed, finite, non-collapsed capped family-development result, but not a successful signed context-fusion continuation. The context-balanced fusion produced some intended clutter discipline relative to ABI-173, visible in higher precision and lower predicted-positive fraction, and the Google split remained strong. The same change also reduced MIT performance, recall, and connectivity enough to lower aggregate filtered Dice below the strongest capped references.

The result suggests that locally gating signed-detail evidence with broader context can improve calibration on some positives or on the Google source, but it also weakens thin-line continuity and MIT recall. This is a different failure mode from ABI-175's overly conservative high-precision branch and ABI-174's weak late line-consensus patch, but it still supports the same branch-level conclusion: another local signed-detail/full-scale fusion tweak is a lower-priority use of the next capped run unless new diagnostics identify a specific fixable failure mode.

## Decision

Do not promote ABI-176, do not repeat it unchanged, and do not request whole-validation diagnostics for ABI-176 from this capped result alone. Stop this exact signed context-fusion branch under the proposal's negative-outcome criterion: it completed finitely but did not demonstrate a better precision/recall/connectivity tradeoff than ABI-173 or the broader ABI-068/130/154 references.

Retain ABI-068 and ABI-173 as the strongest capped aggregate/source-balance references, ABI-173 as the whole-validation-tested SZA-aware ASPP/detail aggregate branch, ABI-154 as the SZA-aware ASPP/detail precision/connectivity branch, and ABI-130 as the prior SZA-aware ASPP/detail aggregate reference. A reasonable next hypothesis should broaden beyond additional local signed-detail/full-scale fusion patches toward a more distinct architecture, data-policy, preprocessing, calibration, or evaluation frontier already allowed by the trusted contract. No Capability Request or Campaign Report is required from this result.

## Artifact references

- `run_20260902_025056_9e87d5/outputs/best_metrics.json`
- `run_20260902_025056_9e87d5/outputs/final_metrics.json`
- `run_20260902_025056_9e87d5/outputs/metrics.jsonl`
- `run_20260902_025056_9e87d5/outputs/resource_profile.json`
- `run_20260902_025056_9e87d5/outputs/model_summary.json`
- `run_20260902_025056_9e87d5/outputs/prediction_samples/samples.json`
- `run_20260902_025056_9e87d5/outputs/validation_postprocessing/epoch_012.json`
- `run_20260902_025056_9e87d5/resolved_manifest.yaml`
- `run_20260901_234732_bd5917/outputs/best_metrics.json`
- `run_20260901_234732_bd5917/outputs/evaluations/eval_evalreq_abi173_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260902_005632_5651ef/outputs/best_metrics.json`
- `run_20260902_015941_3ebc45/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
