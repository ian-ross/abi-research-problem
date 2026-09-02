# Full-spectral BTD+SZA patch-anomaly ASPP/detail decoder BCE-Dice follow-up

research-figures: []

## Scope

This note records ABI-151 after Run `run_20260901_044007_880e7e` completed.

Source Runs:

- ABI-151 full-spectral BTD+SZA patch-anomaly ASPP/detail decoder BCE-Dice Centerline-auxiliary continuation: `run_20260901_044007_880e7e`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice Centerline-auxiliary comparison target: `run_20260831_121006_7d24be`
- ABI-130 whole-validation diagnostic reference: `eval_evalreq_abi130_wholeval_failure_buckets_v1`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice Centerline-auxiliary precision/connectivity reference: `run_20260831_085615_d05ab3`
- ABI-143 SZA-aware soft ridge-gate U-Net BCE-Dice Centerline-auxiliary reference: `run_20260831_224534_27b73d`
- ABI-068 frequency-gated line U-Net focal-Tversky local capped aggregate-Dice reference: `run_20260828_010836_4ccc77`
- ABI-150 recent negative structure-tensor ASPP/detail repair reference: `run_20260901_034937_91779f`

ABI-151 was a family-development continuation of ABI-130. It kept provider-approved `abi_16ch_plus_sza` input, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, combined source-balanced traversal, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled architecture change was a bounded patch-relative anomaly front end over approved raw ABI channels, thermal BTD planes, and SZA features.

## Contract and resource observation

ABI-151 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records provider-approved `abi_16ch_plus_sza` input with GOES ABI source channel indices 0-15 plus Solar Geometry source channel index 18; forbidden longitude and latitude source channel indices 16 and 17 were excluded. Outputs were primary `mask_logits` and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, trusted random mirroring, target derivation, losses, metrics, thresholding, Artifact Filters, prediction retention, resource placement, and Run lifecycle.

The Run completed operationally. `outputs/model_summary.json` reports 9,626,250 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,367.7 seconds total wall time, 1,136.4 seconds training wall time, 1,229.5 seconds validation wall time, 6,047,888,896 bytes peak CUDA allocated, 6,633,291,776 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The best-validation checkpoint was epoch 8 rather than final epoch 12.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260831_224534_27b73d` | ABI-143 | soft ridge-gate U-Net, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3947 | 0.3815 | 0.4287 | 0.4105 | 0.3801 | 0.3010 | 0.00336 |
| `run_20260831_085615_d05ab3` | ABI-126 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD | 12 | 0.3859 | 0.3635 | 0.4415 | 0.4746 | 0.3251 | 0.4517 | 0.00248 |
| `run_20260901_034937_91779f` | ABI-150 | structure-tensor ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 9 | 0.3638 | 0.3573 | 0.3799 | 0.3554 | 0.3727 | 0.1877 | 0.00380 |
| `run_20260901_044007_880e7e` | ABI-151 | patch-anomaly ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 8 | 0.3774 | 0.3673 | 0.4006 | 0.3947 | 0.3616 | 0.3317 | 0.00332 |

ABI-151 did not meet its success criteria. Relative to ABI-130, best-validation aggregate filtered Dice fell by 0.0178, MIT filtered Dice by 0.0106, Google filtered Dice by 0.0397, precision by 0.0468, and connectivity by 0.0534. Filtered recall rose only 0.0038 and the filtered predicted-positive fraction increased from 0.00294 to 0.00332, so the anomaly front end did not provide a useful recall/precision or source-balance tradeoff.

Relative to ABI-126, ABI-151 improves MIT filtered Dice by 0.0037 and recall by 0.0366, but loses aggregate Dice by 0.0084, Google Dice by 0.0408, precision by 0.0799, connectivity by 0.1200, and positive-area discipline. Relative to ABI-143, ABI-151 has slightly higher connectivity but lower aggregate/source Dice, precision, and recall. Relative to ABI-068, ABI-151 is lower on aggregate/source Dice, precision, recall, and connectivity. ABI-151 does improve over ABI-150's negative structure-tensor repair on aggregate, MIT, Google, precision, and connectivity, but remains materially below the active comparison targets.

## ABI-151 trajectory

ABI-151 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.1741, 0.2891, 0.3230, 0.3413, 0.3137, 0.3483, 0.3222, 0.3774, 0.3654, 0.3648, 0.3584, and 0.3621. The selected checkpoint was epoch 8; epochs 9-12 did not recover the selected aggregate Dice.

At the selected checkpoint, source-stratified filtered Dice was 0.3673 for MIT and 0.4006 for Google. MIT had filtered precision 0.4169, recall 0.3282, connectivity 0.3586, and predicted-positive fraction 0.00425. Google had filtered precision 0.3552, recall 0.4595, connectivity 0.3048, and predicted-positive fraction 0.00239. The branch is source-informative but not improved: Google recall is high, while precision, Google Dice, and connectivity remain below ABI-130.

The final epoch shifted to a conservative high-precision/high-connectivity point but at too much recall cost: filtered Dice 0.3621, MIT/Google filtered Dice 0.3358/0.4268, filtered precision 0.4761, recall 0.2921, connectivity 0.4213, and filtered predicted-positive fraction 0.00222. That final checkpoint has better precision/connectivity than ABI-130, but its aggregate Dice is 0.0332 lower and MIT recall/Dice collapse relative to ABI-130, so it is not a useful selected operating point under the trusted checkpoint metric.

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice 0.3911 versus filtered Dice 0.3774, and raw predicted-positive fraction 0.00353 versus filtered 0.00332. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction samples include one empty/negative perfect sample and three near-zero per-sample Dice examples, but these are traceability artifacts under the `first_n` policy and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-151 as a completed, finite, non-collapsed, scientifically negative family-development result for the SZA-aware ASPP/detail BCE-Dice branch. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch. The bounded patch-relative anomaly features did not recover ABI-130's precision/connectivity/clutter weaknesses while preserving its aggregate and Google Dice.

The result narrows this exact patch-anomaly ASPP/detail branch. It does not eliminate patch-relative features generally, SZA-aware input use, full-spectral BTD modeling, or ASPP/detail decoders. It specifically argues against attaching this bounded anomaly front end to the ABI-130-style BCE-Dice ASPP/detail decoder under the current cap, scheduler, augmentation, sampling policy, and 12-epoch budget.

## Decision

Do not promote ABI-151 and do not request whole-validation diagnostics for it. The Run is materially below ABI-130, ABI-143, ABI-126, and ABI-068 on aggregate filtered Dice and lacks a compensating selected-checkpoint precision, connectivity, source-balance, positive-area, or trajectory advantage. The final-epoch precision/connectivity signal is diagnostic, but it is coupled to under-recall and lower aggregate/MIT Dice.

Stop the exact patch-anomaly SZA ASPP/detail BCE-Dice branch. Future work should broaden away from additional ad-hoc SZA-aware ASPP/detail front-end tweaks unless a new hypothesis directly targets the now-repeated calibration/connectivity tradeoff. Reasonable next frontiers remain a different architecture family, data-policy or augmentation tests, safer calibration mechanisms, or preprocessing/front-end designs that preserve ABI-130 recall without lowering Google Dice and connectivity. No Capability Request, Evaluation Request, or Campaign Report is required from ABI-151.

## Artifact references

- `run_20260901_044007_880e7e/outputs/best_metrics.json`
- `run_20260901_044007_880e7e/outputs/final_metrics.json`
- `run_20260901_044007_880e7e/outputs/metrics.jsonl`
- `run_20260901_044007_880e7e/outputs/resource_profile.json`
- `run_20260901_044007_880e7e/outputs/model_summary.json`
- `run_20260901_044007_880e7e/outputs/prediction_samples/samples.json`
- `run_20260901_044007_880e7e/resolved_manifest.yaml`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/evaluations/eval_evalreq_abi130_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
- `run_20260831_224534_27b73d/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260901_034937_91779f/outputs/best_metrics.json`
