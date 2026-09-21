# ABI-291 temporal five-frame persistence-attention directional U-Net

research-figures: []

## Scope

This note records ABI-291, Candidate `abi291_temporal_fiveframe_persistence_attention_directional_unet_bce_dice_line_centerline_aux_v1`, Run `run_20260913_211453_8c6c4e`.

ABI-291 was an exploratory temporal-family scout extending the ABI-238 temporal-attention directional U-Net idea from the provider-owned three-frame window `[-1, 0, 1]` to the allowlisted five-frame window `[-2, -1, 0, 1, 2]`. The hypothesis was that persistence attention and center-vs-neighbor change features over a wider temporal context might distinguish persistent thin contrail evidence from one-frame cloud-edge clutter while remaining fully inside the Candidate model boundary.

The Candidate consumed only provider-owned `abi_16ch_plus_sza_temporal` tensors with trusted `temporal_eligible_center` selection. It used source-balanced sampling, trusted random mirroring, BCE-Dice primary loss, AdamW with constant learning rate, batch size 2, and trusted Line plus Centerline auxiliary targets. Candidate code did not own data loading, temporal lookup, missing-frame repair, sample selection, augmentation transforms, losses, metrics, Artifact Filters, thresholds, postprocessing, target derivation, coordinates, Dataset Source identity, downloads, resource scheduling, prediction retention, or lifecycle behavior.

This is capped temporal-eligible feasibility evidence only. It is not whole-validation promotion evidence and is not directly comparable to the full Working Validation Split frontier.

## Execution result

ABI-291 completed without contract, smoke, shape, numerical, resource, or lifecycle failure.

Key Harness-owned execution facts:

- Status: completed.
- Budget: exploratory/default, 12 epochs.
- Input mode: `abi_16ch_plus_sza_temporal` with 85 input channels from five ABI+Solar Geometry Input frames.
- Effective frame-selection policy: `temporal_eligible_center`.
- Effective temporal offsets: `[-2, -1, 0, 1, 2]`.
- Temporal-eligible capped sample counts: 2,048 train and 1,614 validation ABI Patches.
- Parameter count: 3,136,612, below the 25,000,000-parameter ceiling.
- Batch size: 2.
- Device: A100 CUDA.
- Peak CUDA allocated/reserved memory: about 4.01 / 4.31 GiB.
- Training wall time: 1,108.6 s; validation wall time: 1,031.3 s; total Run wall time: 2,141.5 s, within the exploratory timeout.
- Best checkpoint selected by `val/filtered_dice` at epoch 10.

## Best-validation metrics

| Metric | ABI-291 best epoch 10 | ABI-291 final epoch 12 | ABI-238 temporal directional-context late36 | ABI-223 temporal attention late36 | ABI-285 temporal C4 late36 | ABI-290 precision-gated temporal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Filtered Dice | 0.358719 | 0.319996 | 0.420235 | 0.419776 | 0.422195 | 0.379803 |
| Raw Dice | 0.376631 | 0.336009 | 0.438718 | 0.438487 | 0.439439 | 0.394762 |
| Filtered precision | 0.495053 | 0.458860 | 0.488730 | 0.483764 | 0.448400 | 0.384437 |
| Filtered recall | 0.281261 | 0.245655 | 0.368578 | 0.370738 | 0.398883 | 0.375279 |
| Filtered connectivity | 0.295736 | 0.217001 | 0.352239 | 0.412427 | 0.243387 | 0.245732 |
| MIT filtered Dice | 0.336776 | 0.298176 | 0.405383 | 0.398498 | 0.400831 | 0.368809 |
| Google filtered Dice | 0.414922 | 0.373350 | 0.460838 | 0.476764 | 0.477410 | 0.406267 |
| Filtered predicted-positive fraction | 0.002937 | 0.002768 | 0.003899 | 0.003962 | 0.004599 | 0.005046 |
| Filtered predicted-positive pixels | 310,668 | 292,741 | 412,381 | 419,056 | 486,427 | 533,786 |

ABI-291 is a clear negative result for the five-frame persistence-attention extension as implemented. The selected checkpoint is compact and high-precision, with precision slightly above ABI-238/223 and a smaller filtered predicted-positive footprint, but it gives up too much recall and source-stratified Dice. Relative to ABI-238, ABI-291 is lower on filtered Dice by about 0.0615, recall by 0.0873, connectivity by 0.0565, MIT Dice by 0.0686, and Google Dice by 0.0459. Relative to ABI-223, it is similarly weaker on aggregate/source Dice, recall, and connectivity. Relative to recent ABI-290, ABI-291 improves precision and compactness but loses aggregate Dice, recall, MIT Dice, and selected-checkpoint connectivity.

The one favorable comparison is that ABI-291's selected checkpoint has better connectivity than ABI-285 and ABI-290 while using a much smaller predicted-positive footprint than several recent temporal mechanism tests. That is not enough to justify continuation: the five-frame branch did not approach the temporal comparator band and did not solve the fixed-threshold recall gap.

## Learning trajectory

| Epoch | Filtered Dice | MIT filtered Dice | Google filtered Dice | Filtered precision | Filtered recall | Connectivity | Filtered positive fraction |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.224095 | 0.211027 | 0.256533 | 0.303275 | 0.177701 | 0.221349 | 0.003029 |
| 2 | 0.278370 | 0.269387 | 0.298802 | 0.314556 | 0.249651 | 0.200497 | 0.004103 |
| 3 | 0.272467 | 0.257519 | 0.305601 | 0.322545 | 0.235849 | 0.174013 | 0.003780 |
| 4 | 0.271374 | 0.247668 | 0.329777 | 0.406834 | 0.203587 | 0.226750 | 0.002587 |
| 5 | 0.269235 | 0.244454 | 0.336337 | 0.532090 | 0.180210 | 0.309896 | 0.001751 |
| 6 | 0.323126 | 0.317193 | 0.337411 | 0.373771 | 0.284568 | 0.222818 | 0.003936 |
| 7 | 0.348446 | 0.326391 | 0.406242 | 0.466501 | 0.278075 | 0.296582 | 0.003082 |
| 8 | 0.358143 | 0.339426 | 0.408684 | 0.493051 | 0.281201 | 0.341820 | 0.002948 |
| 9 | 0.345300 | 0.335145 | 0.369243 | 0.319685 | 0.375378 | 0.189541 | 0.006070 |
| 10 | 0.358719 | 0.336776 | 0.414922 | 0.495053 | 0.281261 | 0.295736 | 0.002937 |
| 11 | 0.330085 | 0.308697 | 0.380566 | 0.380336 | 0.291563 | 0.159000 | 0.003963 |
| 12 | 0.319996 | 0.298176 | 0.373350 | 0.458860 | 0.245655 | 0.217001 | 0.002768 |

The trajectory is finite and non-collapsed, but not late-improving. Epochs 7, 8, and 10 form the strongest compact states; epoch 8 has the best connectivity and nearly the same Dice as the selected checkpoint. Epoch 9 briefly recovers recall to 0.3754, comparable to ABI-238/223, but only by doubling the footprint to a filtered predicted-positive fraction of 0.00607, dropping precision to 0.3197, and reducing connectivity to 0.1895. The final two epochs regress in aggregate Dice, MIT/Google Dice, recall, and connectivity. This indicates an unstable precision/recall trade-off rather than a longer-context persistence representation that cleanly improves contrail evidence.

Raw-to-filtered differences are modest and conservative at the selected checkpoint: raw Dice 0.3766 versus filtered Dice 0.3587, and raw predicted-positive pixels 334,662 versus filtered predicted-positive pixels 310,668. Artifact Filters lower rather than create the selected Result.

## Prediction sample check

The retained first-four validation prediction samples are fixed `first_n` traceability artifacts, not representative diagnostics. Their sample Dice values were 0.1351, 0.3146, 0.6381, and 0.3891. They are consistent with finite non-collapsed predictions and include one strong retained sample, but the weak first sample and the aggregate metrics do not support promotion or diagnostics.

## Interpretation

Classify ABI-291 as a finite, resource-safe, scientifically negative temporal-window scout. The five-frame input is operationally feasible under the exploratory resource limits, but the tested persistence-attention/change-feature implementation is more conservative than useful: it can form compact high-precision predictions, yet it suppresses true contrail recall and does not match the ABI-223/238 temporal comparator band. The model appears to alternate between compact precision/connectivity states and broad recall states, similar to ABI-290, rather than learning stable connected thin-line evidence from the extra temporal context.

This result does not eliminate all five-frame temporal modeling, but it argues against an unchanged late36 continuation of ABI-291. Any future five-frame work should be mechanism-changing and should directly address the observed recall suppression, for example with a different motion/change representation, explicit center-frame detail preservation, or a calibration-style dual-operating-point head that does not simply trade recall for compactness. Another reasonable next step is to broaden away from temporal-attention variants, since recent ABI-288 through ABI-291 tests have repeatedly moved along a precision/recall curve without displacing ABI-223/238 or ABI-285.

Any future Candidate must still avoid Candidate-owned thresholds, postprocessing, custom losses, metrics, Artifact Filters, data loading, temporal lookup, sample selection, coordinates, or resource scheduling.

## Decision

Do not promote ABI-291. Do not request temporal-eligible or whole-validation failure-bucket diagnostics for this capped temporal-eligible result. Do not request an unchanged late-improving continuation of the ABI-291 five-frame persistence-attention branch. Treat ABI-291 as evidence that the tested five-frame extension is feasible but not scientifically competitive, and prefer a mechanism-changing pivot rather than spending the approved late-improving budget here.

No Candidate Submission, Experiment Batch Submission, Evaluation Request, Capability Request, or Campaign Report is created in this Autonomy Step. This Research Note is the only primary handoff for the current Autonomy Step.

## Artifact references

- `run_20260913_211453_8c6c4e/candidate/PROPOSAL.md`
- `run_20260913_211453_8c6c4e/candidate/README.md`
- `run_20260913_211453_8c6c4e/candidate/manifest.yaml`
- `run_20260913_211453_8c6c4e/resolved_manifest.yaml`
- `run_20260913_211453_8c6c4e/execution.json`
- `run_20260913_211453_8c6c4e/outputs/model_summary.json`
- `run_20260913_211453_8c6c4e/outputs/best_metrics.json`
- `run_20260913_211453_8c6c4e/outputs/final_metrics.json`
- `run_20260913_211453_8c6c4e/outputs/metrics.jsonl`
- `run_20260913_211453_8c6c4e/outputs/resource_profile.json`
- `run_20260913_211453_8c6c4e/outputs/validation_postprocessing/index.json`
- `run_20260913_211453_8c6c4e/outputs/prediction_samples/samples.json`
- `run_20260911_004137_f54c45/outputs/best_metrics.json` for ABI-238 temporal directional-context comparison context
- `run_20260908_154531_8c7e2b/outputs/best_metrics.json` for ABI-223 temporal-attention comparison context
- `run_20260913_100333_a250df/outputs/best_metrics.json` for ABI-285 temporal C4 late36 comparison context
- `run_20260913_202938_44793e/outputs/best_metrics.json` for ABI-290 precision-gated temporal comparison context
- `/history/research-notes/abi288-temporal-attention-directional-context-cldice.md`
- `/history/research-notes/abi289-temporal-attention-dual-evidence-recall-continuity-unet.md`
- `/history/research-notes/abi290-temporal-attention-precision-gated-continuity-unet.md`
- `/reference/EXPERIMENT_INDEX.md`
- `/research-problem/abi_contrail/brief/goes-abi-contrail-segmentation.md`
- `/research-problem/abi_contrail/profile/agent-campaign-context.v1.json`
- `/research-problem/abi_contrail/profile/temporal-eligibility-profile.v1.json`
