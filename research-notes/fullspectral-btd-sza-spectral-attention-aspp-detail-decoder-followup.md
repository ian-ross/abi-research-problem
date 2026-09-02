# Full-spectral BTD+SZA spectral-attention ASPP/detail decoder follow-up

research-figures: []

## Scope

This note records ABI-138 after Run `run_20260831_185000_419505` completed.

Source Runs:

- ABI-138 SZA-aware spectral-attention ASPP/detail decoder BCE-Dice Centerline-auxiliary continuation: `run_20260831_185000_419505`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice Centerline-auxiliary comparison target: `run_20260831_121006_7d24be`
- ABI-137 negative output-side adaptive-logit comparator: `run_20260831_180256_71be83`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice Centerline-auxiliary high-precision/connectivity comparator: `run_20260831_085615_d05ab3`
- ABI-068 frequency-gated line U-Net focal-Tversky local capped aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-066 frequency-gated line U-Net BCE-Dice-clDice high-connectivity reference: `run_20260827_230540_bf4ce3`
- ABI-130 whole-validation diagnostic reference: `eval_evalreq_abi130_wholeval_failure_buckets_v1`

ABI-138 was a family-development continuation of ABI-130. It kept ABI-130's provider-approved `abi_16ch_plus_sza` input, deterministic raw ABI plus thermal brightness-temperature-difference plus Solar Geometry front end, compact ASPP/detail encoder-decoder, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled architecture change was a neutral-initialized, solar-conditioned spectral-attention front end intended to learn when to emphasize approved ABI, BTD, SZA, and learned spectral-mixture features before the encoder.

## Contract and resource observation

ABI-138 stayed inside the Candidate Experiment Contract. Candidate code owned only the PyTorch architecture over provider-approved GOES ABI channels 1-16 plus Solar Geometry Input. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, combined source-balanced traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, resource placement, prediction retention, filesystem lifecycle, and Run execution.

`outputs/model_summary.json` reported 9,622,772 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,155.5 seconds total wall time, 997.4 seconds training wall time, 1,156.0 seconds validation wall time, 5,958,964,736 bytes peak CUDA allocated, 6,513,754,112 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The best-validation checkpoint was epoch 11; the final epoch 12 regressed.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260827_230540_bf4ce3` | ABI-066 | frequency-gated line U-Net, BCE-Dice-clDice, ABI-16+BTD | 12 | 0.3825 | 0.3638 | 0.4292 | 0.4427 | 0.3367 | 0.4731 | 0.00276 |
| `run_20260831_180256_71be83` | ABI-137 | ABI-130 plus adaptive output-side logit head | 12 | 0.3779 | 0.3694 | 0.3988 | 0.3988 | 0.3590 | 0.2561 | 0.00326 |
| `run_20260831_185000_419505` | ABI-138 | ABI-130 plus neutral SZA-conditioned spectral attention | 11 | 0.3774 | 0.3712 | 0.3921 | 0.4051 | 0.3533 | 0.2519 | 0.00316 |

ABI-138 did not meet the spectral-attention hypothesis relative to ABI-130. Aggregate filtered Dice fell from 0.3953 to 0.3774 (-0.0178), Google filtered Dice fell from 0.4404 to 0.3921 (-0.0482), filtered precision fell from 0.4415 to 0.4051 (-0.0364), filtered recall fell from 0.3578 to 0.3533 (-0.0045), filtered connectivity fell from 0.3851 to 0.2519 (-0.1332), and filtered predicted-positive fraction rose from 0.00294 to 0.00316. MIT filtered Dice was somewhat closer to ABI-130, 0.3712 versus 0.3779 (-0.0067), but that modest MIT retention did not offset the aggregate, Google, precision, and connectivity losses.

Relative to ABI-137, the upstream spectral-attention change landed at nearly the same aggregate quality as the negative output-side adaptive-logit head. ABI-138 slightly improved precision and positive-area discipline relative to ABI-137, but it reduced recall, Google filtered Dice, and connectivity. This suggests the neutral front-end gate did not preserve ABI-130's useful SZA-aware operating point; it behaved like another local calibration tweak whose learned reweighting damaged the branch's strongest Google/source-transfer signal.

Relative to ABI-126 and ABI-066, ABI-138 also failed to recover the high precision/connectivity behavior that motivates the ASPP/detail and clDice references. Relative to ABI-068, it remained below the local capped aggregate-Dice/source-balance reference on aggregate filtered Dice, MIT filtered Dice, Google filtered Dice, recall, connectivity, and positive-area discipline.

## ABI-138 trajectory

ABI-138 trained finitely and avoided persistent all-negative or all-positive collapse. Filtered Dice by epoch was 0.1880, 0.2671, 0.2955, 0.3214, 0.3254, 0.3536, 0.3370, 0.3595, 0.3652, 0.3698, 0.3774, and 0.3548. The selected checkpoint was epoch 11, not the final epoch. Final epoch 12 fell to filtered Dice 0.3548, with filtered precision 0.4248, recall 0.3046, connectivity 0.2471, MIT filtered Dice 0.3434, and Google filtered Dice 0.3818.

The trajectory was finite and mostly improving through epoch 11, so this is not a numerical or optimization-collapse failure. However, the late improvement did not reach ABI-130's fixed-threshold operating point, and the epoch-12 regression weakens the continuation case. The best checkpoint showed source-stratified filtered Dice of 0.3712 for MIT and 0.3921 for Google. MIT had filtered precision 0.4288, recall 0.3272, connectivity 0.2932, and predicted-positive fraction 0.00412. Google had filtered precision 0.3607, recall 0.4295, connectivity 0.2105, and predicted-positive fraction 0.00220. Both Dataset Sources were finite and non-collapsed, but Google lost the main ABI-130 advantage, and connectivity was low on both sources.

Raw-to-filtered differences were modest at the best checkpoint: raw Dice was 0.3922 versus filtered Dice 0.3774, and raw predicted-positive fraction was 0.00336 versus filtered 0.00316. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples all have near-zero per-sample Dice under the `first_n` retention policy; these bounded artifacts are traceability artifacts and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-138 as a completed, finite, non-collapsed, but negative family-development result for this exact neutral SZA-conditioned spectral-attention front end. It is not a candidate bug, contract violation, resource failure, or Harness failure. The branch answered the narrow front-end calibration question: adding neutral learned channel attention over ABI+BTD+SZA features did not retain ABI-130 within the proposed 0.01 aggregate filtered-Dice band and did not improve the meaningful diagnostics it targeted. Instead, it materially lost Google Dice and line connectivity while landing near the already-negative ABI-137 output-head variant.

This strengthens the recent pattern from ABI-131 through ABI-138: incremental local continuity, agreement, auxiliary, traversal, objectness-gate, output-logit, and front-end spectral-attention changes around the SZA-aware ASPP/detail BCE-Dice branch have not improved on ABI-130. ABI-130 remains the best SZA-aware ASPP/detail capped reference with whole-validation diagnostic support. ABI-126 remains the ASPP/detail high-precision/connectivity comparator, ABI-066 remains the high-connectivity reference, and ABI-068 remains the current capped aggregate filtered-Dice reference.

## Decision

Do not promote ABI-138. Do not request whole-validation diagnostics for ABI-138 from this capped result, because it failed the controlled comparison against ABI-130 and did not establish a distinctive useful operating point. Do not repeat the exact neutral SZA-conditioned spectral-attention front end unchanged.

For a later Autonomy Step, broaden away from incremental SZA-aware ASPP/detail local calibration changes. A stronger next hypothesis should use a distinct architecture, preprocessing/calibration mechanism, loss/data-policy frontier, or other in-contract idea that targets false positives and line connectivity without candidate-owned thresholding, postprocessing, Artifact Filters, data loading, sampling, target derivation, or metrics.

No new Capability Request, Evaluation Request, or Campaign Report is required from this result.

## Artifact references

- `run_20260831_185000_419505/outputs/best_metrics.json`
- `run_20260831_185000_419505/outputs/final_metrics.json`
- `run_20260831_185000_419505/outputs/metrics.jsonl`
- `run_20260831_185000_419505/outputs/resource_profile.json`
- `run_20260831_185000_419505/outputs/model_summary.json`
- `run_20260831_185000_419505/outputs/prediction_samples/samples.json`
- `run_20260831_185000_419505/resolved_manifest.yaml`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_180256_71be83/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260827_230540_bf4ce3/outputs/best_metrics.json`
