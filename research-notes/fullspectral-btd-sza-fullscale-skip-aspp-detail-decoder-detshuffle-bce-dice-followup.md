# Full-spectral BTD+SZA full-scale skip ASPP/detail decoder deterministic-shuffle BCE-Dice follow-up

research-figures: []

## Scope

This note records ABI-157 after Run `run_20260901_095946_b45eb3` completed.

Source Runs:

- ABI-157 deterministic-shuffle full-scale skip ASPP/detail decoder continuation: `run_20260901_095946_b45eb3`
- ABI-154 full-scale skip ASPP/detail decoder precision/connectivity target and whole-validation-tested branch: `run_20260901_071026_32d3ec`, Evaluation `eval_evalreq_abi154_wholeval_failure_buckets_v1`
- ABI-155 final-head recall-calibration continuation: `run_20260901_081321_b38989`
- ABI-156 feature-calibrated full-scale skip continuation: `run_20260901_090713_9c7d32`
- ABI-130 SZA-aware ASPP/detail decoder BCE-Dice aggregate/reference branch: `run_20260831_121006_7d24be`
- ABI-068 frequency-gated line U-Net focal-Tversky capped aggregate/source-balance reference: `run_20260828_010836_4ccc77`
- ABI-126 non-SZA ASPP/detail decoder BCE-Dice precision/connectivity comparator: `run_20260831_085615_d05ab3`

ABI-157 was a family-development data-policy continuation of ABI-154. It kept the same provider-approved `abi_16ch_plus_sza` input, deterministic thermal BTD features from approved ABI channels, normalized Solar Geometry Input features, full-scale skip ASPP/detail decoder architecture, trusted `bce_dice` primary loss, provider-derived Centerline Target auxiliary supervision at weight 0.02, trusted random mirroring, AdamW learning rate `0.0003`, batch size 4, max epochs 12, constant learning rate, disabled early stopping, and the trusted 1,024-record-per-Dataset-Source/split representative cap. The controlled manifest change was switching the provider-owned training traversal from `combined_source_balanced` to `deterministic_shuffle`.

## Contract and resource observation

ABI-157 stayed inside the Candidate Experiment Contract. `outputs/model_summary.json` records input mode `abi_16ch_plus_sza`, approved ABI source channel indices 0-15 plus Solar Geometry source channel index 18, forbidden longitude and latitude source channel indices 16 and 17 excluded, primary `mask_logits`, and provider-derived auxiliary `centerline_logits`. Provider/Harness code retained ownership of data loading, Leakage-Safe Split, capped-record selection, sampling traversal implementation, augmentation transforms, target derivation, losses, metrics, thresholding, Artifact Filters, postprocessing, prediction retention, resource placement, and Run lifecycle.

`outputs/model_summary.json` reported 9,741,850 parameters, below the 25,000,000-parameter smoke ceiling. The Run completed on the A100 at batch size 4 with 2,582.5 seconds total wall time, 19.41 training samples per second, 18.70 validation samples per second, 8,020,934,144 bytes peak CUDA allocated, 9,439,281,152 bytes peak CUDA reserved, and no terminal execution failure. The trusted bounded-record policy selected 1,024 records per Dataset Source and Leakage-Safe Split, for 2,048 train and 2,048 validation records. The selected best-validation checkpoint was epoch 10 rather than the final epoch.

## Best-validation comparison

| Run | Candidate | Primary architecture/loss/input | Best epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Filtered connectivity | Filtered predicted-positive fraction |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `run_20260828_010836_4ccc77` | ABI-068 | frequency-gated line U-Net, focal-Tversky, ABI-16+BTD | 12 | 0.3964 | 0.3886 | 0.4161 | 0.3992 | 0.3936 | 0.3900 | 0.00357 |
| `run_20260831_121006_7d24be` | ABI-130 | ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3953 | 0.3779 | 0.4404 | 0.4415 | 0.3578 | 0.3851 | 0.00294 |
| `run_20260901_071026_32d3ec` | ABI-154 | full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3944 | 0.3824 | 0.4260 | 0.4777 | 0.3359 | 0.4374 | 0.00255 |
| `run_20260901_081321_b38989` | ABI-155 | final-head recall-calibrated full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 12 | 0.3834 | 0.3669 | 0.4252 | 0.4685 | 0.3244 | 0.3641 | 0.00251 |
| `run_20260901_090713_9c7d32` | ABI-156 | feature-calibrated full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 9 | 0.3926 | 0.3762 | 0.4353 | 0.4491 | 0.3487 | 0.3884 | 0.00281 |
| `run_20260901_095946_b45eb3` | ABI-157 | deterministic-shuffle full-scale skip ASPP/detail decoder, BCE-Dice, ABI-16+BTD+SZA | 10 | 0.3730 | 0.3595 | 0.4063 | 0.4559 | 0.3157 | 0.3163 | 0.00251 |

ABI-157 did not support the deterministic-shuffle traversal hypothesis at the selected checkpoint. Relative to ABI-154, aggregate filtered Dice fell from 0.3944 to 0.3730 (-0.0214), MIT filtered Dice fell from 0.3824 to 0.3595 (-0.0229), Google filtered Dice fell from 0.4260 to 0.4063 (-0.0198), filtered precision fell from 0.4777 to 0.4559 (-0.0218), filtered recall fell from 0.3359 to 0.3157 (-0.0202), and filtered connectivity fell from 0.4374 to 0.3163 (-0.1211). The filtered predicted-positive fraction stayed nearly identical at 0.00251 versus ABI-154's 0.00255, so the lower recall and connectivity were not compensated by useful positive-area expansion.

Relative to ABI-156, ABI-157 also regressed: aggregate filtered Dice fell by 0.0195, MIT filtered Dice by 0.0167, Google filtered Dice by 0.0290, recall by 0.0330, and connectivity by 0.0721, while precision rose only modestly. Relative to ABI-130 and ABI-068, ABI-157 is materially lower on aggregate/source filtered Dice, recall, and connectivity. Relative to ABI-126, ABI-157 keeps similar positive-area discipline and slightly lower precision, but trails ABI-126's filtered Dice, Google Dice, recall, and connectivity.

## ABI-157 trajectory

ABI-157 trained finitely and avoided persistent all-negative or all-positive prediction collapse. Filtered Dice by epoch was 0.2049, 0.1969, 0.2809, 0.3023, 0.3230, 0.3368, 0.3335, 0.3682, 0.3691, 0.3730, 0.3660, and 0.3619. The selected best checkpoint was epoch 10, followed by two lower final epochs.

The epoch-level trajectory shows a real mid-run improvement but a weaker ceiling than ABI-154/156 and no stable terminal gain. Epoch 10 combined filtered Dice 0.3730, filtered precision 0.4559, filtered recall 0.3157, filtered connectivity 0.3163, and filtered predicted-positive fraction 0.00251. Source-stratified filtered Dice was 0.3595 for MIT and 0.4063 for Google. MIT had filtered precision 0.4727, recall 0.2900, connectivity 0.3243, and predicted-positive fraction 0.00331; Google had filtered precision 0.4231, recall 0.3908, connectivity 0.3084, and predicted-positive fraction 0.00171.

The final epoch shifted toward higher recall and more predicted positives but lower precision/connectivity: filtered Dice 0.3619, precision 0.3407, recall 0.3860, connectivity 0.1699, and filtered predicted-positive fraction 0.00411. That final operating point does show that deterministic shuffle can expose a higher-recall state late in training, but the cost in precision and especially connectivity is too large to count as a useful repair of ABI-154's conservative fixed-threshold behavior.

Raw-to-filtered differences were modest at the selected checkpoint: raw Dice was 0.3879 versus filtered Dice 0.3730, and raw predicted-positive fraction was 0.00267 versus filtered 0.00251. This does not indicate primary Artifact Filter dependence. The fixed first-four retained prediction artifacts remain traceability samples under the `first_n` retention policy and should not be treated as representative qualitative evidence.

## Interpretation

Classify ABI-157 as a completed, finite, non-collapsed, scientifically negative result for the exact deterministic-shuffle full-scale-skip ASPP/detail variant. It is not a candidate bug, contract violation, resource failure, Harness failure, non-finite failure, or prediction-collapse branch.

The result is scientifically informative because it separates traversal policy from the local full-scale skip architecture. The representative cap already balanced Dataset Source counts and preserved positive/negative coverage, but replacing `combined_source_balanced` traversal with `deterministic_shuffle` did not recover ABI-154's under-recall at the selected best checkpoint and substantially damaged the branch's distinctive connectivity. The final epoch's high-recall/low-connectivity shift suggests ordering can affect calibration dynamics, but not in a way that improves the fixed-threshold trade-off under the current 12-epoch budget.

ABI-154 remains the whole-validation-tested full-scale skip precision/connectivity reference. ABI-130 remains the SZA-aware ASPP/detail aggregate/reference branch. ABI-068 remains the local capped aggregate/source-balance reference. ABI-156 remains evidence that feature-level calibration is more useful than final-head calibration inside the full-scale skip branch, but neither local calibration nor deterministic traversal produced an aggregate improvement over ABI-154/130/068.

## Decision

Do not promote ABI-157, do not request whole-validation diagnostics for it, and do not repeat this exact deterministic-shuffle full-scale-skip variant unchanged. It failed the proposed useful-outcome test: it did not improve ABI-154 recall at the selected checkpoint, did not preserve ABI-154 connectivity, and did not challenge ABI-130 or ABI-068 on capped aggregate/source-stratified metrics.

The next useful direction should broaden away from deterministic-shuffle repairs of the full-scale skip branch. Contract-compliant options include a different architecture that improves recall before the final fused features while preserving line continuity, a loss/auxiliary combination that targets the precision-recall-connectivity trade-off without candidate-owned thresholding, or a preprocessing/front-end inductive bias that separates thin contrail evidence from cloud-edge clutter without moving Artifact Filters into candidate code. No Capability Request, Evaluation Request, or Campaign Report is required from ABI-157.

## Artifact references

- `run_20260901_095946_b45eb3/outputs/best_metrics.json`
- `run_20260901_095946_b45eb3/outputs/final_metrics.json`
- `run_20260901_095946_b45eb3/outputs/metrics.jsonl`
- `run_20260901_095946_b45eb3/outputs/resource_profile.json`
- `run_20260901_095946_b45eb3/outputs/model_summary.json`
- `run_20260901_095946_b45eb3/outputs/prediction_samples/samples.json`
- `run_20260901_095946_b45eb3/resolved_manifest.yaml`
- `run_20260901_071026_32d3ec/outputs/best_metrics.json`
- `run_20260901_071026_32d3ec/outputs/evaluations/eval_evalreq_abi154_wholeval_failure_buckets_v1/aggregate_metrics.json`
- `run_20260901_081321_b38989/outputs/best_metrics.json`
- `run_20260901_090713_9c7d32/outputs/best_metrics.json`
- `run_20260831_121006_7d24be/outputs/best_metrics.json`
- `run_20260828_010836_4ccc77/outputs/best_metrics.json`
- `run_20260831_085615_d05ab3/outputs/best_metrics.json`
